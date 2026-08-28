"""Room/lobby co-ownership: invite tokens, accept flow, co-owner CRUD.

Covers the /api invite + co-owner endpoints, the /me/accept/<token> consumer,
and the /me/sharing/<kind>/<id> management page. Helpers live in ownership.py,
storage in models.py.
"""
from __future__ import annotations

from datetime import timedelta
from uuid import UUID, uuid4

from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import select

from Utils import utcnow
from . import app, to_url
from .api import api_endpoints
from .models import (
    Lobby,
    LobbyCoOwner,
    OwnershipInvite,
    Room,
    RoomCoOwner,
    commit,
    db,
)
from .ownership import is_primary_owner, list_co_owners

_INVITE_TTL = timedelta(days=7)

_VALID_MODES = ("co_owner", "transfer")


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def _absolute_url(path: str) -> str:
    """Build a shareable absolute URL for ``path`` (which already starts with ``/``)."""
    base_host = app.config.get("SHARE_BASE_HOST") or request.host
    return f"{base_host}{path}"


def _get_target(kind: str, target_id: UUID):
    if kind == "room":
        return Room.get(id=target_id)
    if kind == "lobby":
        return Lobby.get(id=target_id)
    return None


def _co_owner_row(kind: str, target_id: UUID, session_id: UUID):
    if kind == "room":
        return db.session.get(RoomCoOwner, (target_id, session_id))
    if kind == "lobby":
        return db.session.get(LobbyCoOwner, (target_id, session_id))
    return None


def _add_co_owner(kind: str, target_id: UUID, session_id: UUID, granted_by: UUID) -> bool:
    """Insert a co-owner row if one doesn't already exist. Returns True if added."""
    if _co_owner_row(kind, target_id, session_id) is not None:
        return False
    if kind == "room":
        RoomCoOwner(room_id=target_id, session_id=session_id, granted_by=granted_by)
    elif kind == "lobby":
        LobbyCoOwner(lobby_id=target_id, session_id=session_id, granted_by=granted_by)
    else:
        return False
    return True


# ---------------------------------------------------------------------------
# Invite create - primary owner only
# ---------------------------------------------------------------------------

def _create_invite(kind: str, target_id: UUID, mode: str):
    """Common logic for both /api/room/.../invite and /api/lobby/.../invite."""
    if mode not in _VALID_MODES:
        abort(400, "invalid mode")
    target = _get_target(kind, target_id)
    if target is None:
        abort(404)
    if not is_primary_owner(target, session["_id"]):
        abort(403, "only the primary owner can mint invites")

    invite = OwnershipInvite(
        token=uuid4(),
        target_kind=kind,
        target_id=target_id,
        mode=mode,
        created_by=session["_id"],
        expires_at=utcnow() + _INVITE_TTL,
    )
    commit()
    return jsonify({
        "url": _absolute_url(url_for("accept_invite", token=invite.token)),
        "expires_at": invite.expires_at.isoformat() + "Z",
        "mode": mode,
    })


@api_endpoints.route("/room/<suuid:room>/invite", methods=["POST"])
def api_room_invite(room: UUID):
    body = request.get_json(silent=True) or request.form.to_dict()
    return _create_invite("room", room, body.get("mode", "co_owner"))


@api_endpoints.route("/lobby/<suuid:lobby>/invite", methods=["POST"])
def api_lobby_invite(lobby: UUID):
    body = request.get_json(silent=True) or request.form.to_dict()
    return _create_invite("lobby", lobby, body.get("mode", "co_owner"))


# ---------------------------------------------------------------------------
# Accept - anyone holding the URL
# ---------------------------------------------------------------------------

@app.route("/me/accept/<suuid:token>")
def accept_invite(token: UUID):
    invite = db.session.get(OwnershipInvite, token)
    if invite is None:
        flash("That invite link is invalid or has been revoked.")
        return redirect(url_for("me"))
    if invite.consumed_at is not None:
        flash("That invite link has already been used.")
        return redirect(url_for("me"))
    if invite.expires_at < utcnow():
        flash("That invite link has expired.")
        return redirect(url_for("me"))

    target = _get_target(invite.target_kind, invite.target_id)
    if target is None:
        flash("The room or lobby this invite was for no longer exists.")
        return redirect(url_for("me"))

    me = session["_id"]
    if me == invite.created_by:
        flash("You can't accept your own invite.")
        return redirect(url_for("me"))

    if invite.mode == "transfer":
        old_primary = target.owner
        target.owner = me
        if old_primary != me:
            _add_co_owner(invite.target_kind, invite.target_id, old_primary, granted_by=me)
        existing = _co_owner_row(invite.target_kind, invite.target_id, me)
        if existing is not None:
            db.session.delete(existing)
        flash(f"You are now the primary owner of this {invite.target_kind}.")
    else:  # co_owner
        if target.owner == me:
            flash("You're already the primary owner.")
        elif _co_owner_row(invite.target_kind, invite.target_id, me) is not None:
            flash("You already have access.")
        else:
            _add_co_owner(invite.target_kind, invite.target_id, me, granted_by=invite.created_by)
            flash(f"You now have shared access to this {invite.target_kind}.")

    invite.consumed_at = utcnow()
    invite.consumed_by = me
    commit()
    return redirect(url_for("me"))


# ---------------------------------------------------------------------------
# Co-owner list + remove - primary owner only
# ---------------------------------------------------------------------------

def _co_owner_listing(kind: str, target_id: UUID):
    target = _get_target(kind, target_id)
    if target is None:
        abort(404)
    if not is_primary_owner(target, session["_id"]):
        abort(403)
    return jsonify({
        "primary_owner": to_url(target.owner),
        "co_owners": [to_url(uid) for uid in list_co_owners(target)],
    })


@api_endpoints.route("/room/<suuid:room>/co_owners", methods=["GET"])
def api_room_co_owners(room: UUID):
    return _co_owner_listing("room", room)


@api_endpoints.route("/lobby/<suuid:lobby>/co_owners", methods=["GET"])
def api_lobby_co_owners(lobby: UUID):
    return _co_owner_listing("lobby", lobby)


def _remove_co_owner(kind: str, target_id: UUID, co_owner: UUID):
    target = _get_target(kind, target_id)
    if target is None:
        abort(404)
    if not is_primary_owner(target, session["_id"]):
        abort(403)
    row = _co_owner_row(kind, target_id, co_owner)
    if row is None:
        return jsonify({"ok": True})
    db.session.delete(row)
    commit()
    return jsonify({"ok": True})


@api_endpoints.route("/room/<suuid:room>/co_owner/<suuid:co_owner>", methods=["DELETE"])
def api_room_remove_co_owner(room: UUID, co_owner: UUID):
    return _remove_co_owner("room", room, co_owner)


@api_endpoints.route("/lobby/<suuid:lobby>/co_owner/<suuid:co_owner>", methods=["DELETE"])
def api_lobby_remove_co_owner(lobby: UUID, co_owner: UUID):
    return _remove_co_owner("lobby", lobby, co_owner)


# ---------------------------------------------------------------------------
# Sharing management page - primary-owner UI
# ---------------------------------------------------------------------------

@app.route("/me/sharing/<string:kind>/<suuid:target_id>")
def share_access(kind: str, target_id: UUID):
    if kind not in ("room", "lobby"):
        abort(404)
    target = _get_target(kind, target_id)
    if target is None:
        abort(404)
    if not is_primary_owner(target, session["_id"]):
        abort(403)

    display_name = (
        getattr(target, "title", None)
        or f"Room {to_url(target.id)[:6]}"
    )
    return render_template(
        "share_access.html",
        kind=kind,
        target=target,
        display_name=display_name,
        co_owners=[to_url(uid) for uid in list_co_owners(target)],
    )
