"""Session-scoped avatar management for the website (/me dashboard).

The desktop client uploads avatars through ``api/avatar.py`` with a minted
Bearer token. This module is the browser-cookie counterpart: a browser session
(``session["_id"]``) uploads on the website and the image becomes that
session's portable avatar - shown in the nav today, and (later phases)
projected onto the slots that session plays.

Storage, validation and NSFW screening are reused from ``api/avatar.py``; only
the owner differs. To avoid a schema migration on the existing avatar tables,
each session's web uploads are owned by a stable per-session ``AvatarToken``
(identified by its ``note``), and the currently-selected image is recorded in
the new ``SessionAvatar`` table.
"""
import os
from urllib.parse import urlparse

from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_limiter.util import get_remote_address
from sqlalchemy import select

from Utils import utcnow
from WebHostLib import app, limiter
from WebHostLib.api.avatar import (
    AvatarUploadError,
    avatar_public_url,
    read_avatar_upload,
    store_avatar,
)
from WebHostLib.models import (
    Avatar,
    AvatarToken,
    Lobby,
    LobbyPlayer,
    Room,
    SessionAvatar,
    SlotAvatar,
    commit,
    db,
)

#: Prefix for the ``AvatarToken.note`` that owns a session's website uploads.
_SESSION_TOKEN_NOTE = "session-avatar"


def _session_token(session_id) -> AvatarToken:
    """Return the AvatarToken owning this session's web uploads, creating it once.

    Avatar rows require a token owner (``Avatar.owner_token_id`` is NOT NULL);
    rather than alter that table we keep one stable token per session, keyed by
    a ``note`` marker since the token has no session column.
    """
    note = f"{_SESSION_TOKEN_NOTE}:{session_id}"
    token = AvatarToken.get(note=note)
    if token is None:
        token = AvatarToken(note=note)
    return token


def _delete_avatar(avatar: Avatar) -> None:
    """Delete an Avatar row and its on-disk PNG (best effort on the file)."""
    upload_dir = os.path.abspath(app.config["AVATAR_UPLOAD_FOLDER"])
    path = os.path.join(upload_dir, f"{avatar.id.hex}.png")
    try:
        os.remove(path)
    except OSError:
        pass
    avatar.delete()


def session_avatar_url(session_id) -> "str | None":
    """Same-origin URL of a session's current avatar, or None if it has none.

    Returns a root-relative path served by ``avatar_serve`` (or the nginx alias
    in production) - suitable for an ``<img src>`` on our own pages, as opposed
    to the absolute cross-host wire URL clients embed in ``profile_data``.
    """
    record = SessionAvatar.get(session_id=session_id)
    if record is None:
        return None
    return url_for("avatar_serve", avatar_url_id=f"{record.avatar_id.hex}.png")


@app.context_processor
def inject_slot_avatar_url() -> dict:
    """Feed baseHeader's nav avatar with the current session's chosen avatar."""
    try:
        return {"slot_avatar_url": session_avatar_url(session["_id"])}
    except Exception:
        return {"slot_avatar_url": None}


def mwgg_viewer_avatar_url() -> str:
    """Absolute, client-renderable avatar URL for the current session, or "".

    Exposed as a Jinja global so the mwgg:// room links can carry ``&avatar=``;
    the desktop client persists it to client.avatar on launch (gated by its own
    safe_avatar_source).
    """
    try:
        record = SessionAvatar.get(session_id=session["_id"])
        if record is None:
            return ""
        return avatar_public_url(record.avatar_id)
    except Exception:
        return ""


app.jinja_env.globals["mwgg_viewer_avatar_url"] = mwgg_viewer_avatar_url


@app.route("/me/avatar", methods=["GET"])
def me_avatar():
    return render_template(
        "me_avatar.html",
        avatar_url=session_avatar_url(session["_id"]),
        session_key=session["_id"],
    )


@app.route("/me/avatar", methods=["POST"])
@limiter.limit("10 per hour")
def me_avatar_upload():
    token = _session_token(session["_id"])
    try:
        raw = read_avatar_upload(request)
        avatar = store_avatar(raw, token)
    except AvatarUploadError as exc:
        flash(exc.message)
        return redirect(url_for("me_avatar"))

    # Repoint this session at the new avatar before deleting the old one, so the
    # SessionAvatar FK never dangles.
    record = SessionAvatar.get(session_id=session["_id"])
    previous_avatar = record.avatar if record is not None else None
    if record is None:
        SessionAvatar(session_id=session["_id"], avatar=avatar)
    else:
        record.avatar = avatar
        record.updated_at = utcnow()
    commit()

    if previous_avatar is not None:
        _delete_avatar(previous_avatar)
        commit()

    flash("Avatar updated.")
    return redirect(url_for("me_avatar"))


@app.route("/me/avatar/remove", methods=["POST"])
def me_avatar_remove():
    record = SessionAvatar.get(session_id=session["_id"])
    if record is not None:
        previous_avatar = record.avatar
        record.delete()
        commit()
        _delete_avatar(previous_avatar)
        commit()
        flash("Avatar removed.")
    return redirect(url_for("me_avatar"))


# ---------------------------------------------------------------------------
# Per-slot avatars (room tracker)
# ---------------------------------------------------------------------------

def _trusted_avatar_hosts() -> set:
    """Hosts whose avatar URLs we'll render, mirroring the client allowlist."""
    hosts = {host.lower() for host in app.config.get("AVATAR_TRUSTED_HOSTS", ())}
    base = (app.config.get("SHARE_BASE_HOST") or "").strip().lower()
    if base:
        # SHARE_BASE_HOST may or may not carry a scheme; urlparse needs one.
        host = urlparse(base if "://" in base else f"//{base}").hostname
        if host:
            hosts.add(host)
    return hosts


def _safe_avatar_url(value) -> "str | None":
    """Return a client-set profile_data avatar only if HTTPS on a trusted host.

    Mirrors the desktop client's ``safe_avatar_source`` (mwgg_gui) so the web
    shows exactly the avatars a client would - the uploader only ever hands out
    trusted-host URLs, and manually-edited/hostile values collapse to nothing.
    """
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    if parsed.scheme != "https":
        return None
    if (parsed.hostname or "").lower() not in _trusted_avatar_hosts():
        return None
    return value


def compute_slot_avatars(tracker_data) -> dict:
    """Map ``(team, slot) -> same-origin avatar URL`` for every slot in a room.

    Resolution per slot, first hit wins:
      1. an explicit per-slot avatar set on the website (``SlotAvatar``);
      2. the client-set avatar persisted in ``profile_data`` (survives sleep),
         honoured only when HTTPS on the trusted-host allowlist (same gate as
         the desktop client);
      3. the portable session avatar of the slot's lobby player (lobby rooms).
    """
    room = tracker_data.room
    explicit = {
        (row.team, row.slot): row.avatar_id
        for row in db.session.scalars(
            select(SlotAvatar).where(SlotAvatar.room_id == room.id)
        ).all()
    }
    stored = tracker_data._multisave.get("stored_data", {}) or {}

    lobby = Lobby.get(room_id=room.id)
    lobby_sessions: dict = {}
    if lobby is not None:
        for player in db.session.scalars(
            select(LobbyPlayer).where(LobbyPlayer.lobby_id == lobby.id)
        ).all():
            lobby_sessions.setdefault(player.player_name, player.session_id)

    avatars: dict = {}
    for team, players in tracker_data.get_all_players().items():
        for slot in players:
            avatar_id = explicit.get((team, slot))
            if avatar_id is not None:
                avatars[(team, slot)] = url_for("avatar_serve", avatar_url_id=f"{avatar_id.hex}.png")
                continue
            profile = stored.get(f"profile_data_{team}_{slot}")
            trusted = _safe_avatar_url(profile.get("avatar") if isinstance(profile, dict) else None)
            if trusted:
                avatars[(team, slot)] = trusted
                continue
            session_id = lobby_sessions.get(tracker_data.get_player_name(slot))
            if session_id is not None:
                url = session_avatar_url(session_id)
                if url:
                    avatars[(team, slot)] = url
    return avatars


def resolve_slot_avatar(tracker_data, team: int, slot: int) -> "str | None":
    """Same-origin avatar URL for a single slot (see compute_slot_avatars)."""
    return compute_slot_avatars(tracker_data).get((team, slot))


@app.route("/tracker/<suuid:tracker>/avatar", methods=["POST"])
@limiter.limit("20 per hour")
@limiter.limit("60 per hour", key_func=get_remote_address)
def set_slot_avatar(tracker):
    """Set a slot's avatar from the web. Open to anyone, rate-limited + screened.

    Image source is the uploaded file, or - when no file is sent - the caller's
    own session avatar. Overwrites any existing slot avatar; never locks it.
    """
    from WebHostLib.tracker import TrackerData

    room = Room.get(tracker=tracker)
    if room is None:
        abort(404)
    try:
        team = int(request.form["team"])
        slot = int(request.form["slot"])
    except (KeyError, ValueError):
        abort(400)

    back = redirect(url_for("get_player_tracker", tracker=tracker, tracked_team=team, tracked_player=slot))

    tracker_data = TrackerData(room)
    if slot not in tracker_data.get_all_players().get(team, []):
        abort(404)

    uploaded = request.files.get("image")
    if uploaded is not None and uploaded.filename:
        try:
            raw = read_avatar_upload(request)
            avatar = store_avatar(raw, _session_token(session["_id"]))
        except AvatarUploadError as exc:
            flash(exc.message)
            return back
    else:
        record = SessionAvatar.get(session_id=session["_id"])
        if record is None:
            flash("Choose an image, or set your own avatar first to reuse it here.")
            return back
        avatar = record.avatar

    avatar_url = avatar_public_url(avatar.id)
    existing = SlotAvatar.get(room_id=room.id, team=team, slot=slot)
    if existing is None:
        SlotAvatar(room_id=room.id, team=team, slot=slot, avatar=avatar,
                   avatar_url=avatar_url, set_by_session=session["_id"])
    else:
        existing.avatar = avatar
        existing.avatar_url = avatar_url
        existing.set_by_session = session["_id"]
        existing.updated_at = utcnow()
    commit()
    flash("Avatar set for this slot.")
    return back


def apply_slot_avatars_to_stored_data(session, room_id, stored_data: dict) -> None:
    """Inject web-set slot avatars into a room's ``stored_data`` profile_data.

    Called by the live room process at boot (customserver) so connected desktop
    clients render web-set avatars. Takes an explicit SQLAlchemy session because
    the room process isn't in a Flask request context, and mutates ``stored_data``
    in place. Only explicit ``SlotAvatar`` rows are seeded - lobby-derived session
    avatars stay web-only (the client carries its own via persistent storage).
    """
    rows = session.scalars(select(SlotAvatar).where(SlotAvatar.room_id == room_id)).all()
    for row in rows:
        if not row.avatar_url:
            continue
        key = f"profile_data_{row.team}_{row.slot}"
        profile = stored_data.get(key)
        profile = profile if isinstance(profile, dict) else {}
        profile["avatar"] = row.avatar_url
        stored_data[key] = profile
