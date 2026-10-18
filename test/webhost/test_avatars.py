"""Webhost avatar tests; add new avatar tests here.

PR1 of the persistent-avatar feature (website/session avatars): the
/me/avatar upload/replace/remove flow, the nav context processor, and the
refactored Bearer-token API in ``api/avatar.py``.

PR2 (per-slot avatars on room trackers): the resolution precedence (explicit
SlotAvatar > our-store profile_data > lobby-player session avatar), the
room-prune cascade, and the set endpoint's guards. Resolution is unit-tested
against a lightweight TrackerData stand-in so the tests don't need a fully
decodable seed.
"""
from __future__ import annotations

import io
import os
from uuid import uuid4

import pytest
from flask import url_for
from PIL import Image


def _png_bytes(color=(10, 120, 200, 255), size=(64, 64)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGBA", size, color).save(buf, format="PNG")
    return buf.getvalue()


def _upload(client, png: bytes, filename: str = "a.png"):
    return client.post(
        "/me/avatar",
        data={"image": (io.BytesIO(png), filename)},
        content_type="multipart/form-data",
    )


def _pin_session(client):
    sid = uuid4()
    with client.session_transaction() as sess:
        sess["_id"] = sid
    return sid


def _session_avatar_hex(app, sid):
    from WebHostLib.models import SessionAvatar
    with app.app_context():
        record = SessionAvatar.get(session_id=sid)
        return record.avatar_id.hex if record else None


@pytest.fixture(autouse=True)
def _isolated_avatar_dir(app, tmp_path):
    """Point avatar storage at a per-test temp dir so uploads don't litter the repo."""
    original = app.config["AVATAR_UPLOAD_FOLDER"]
    app.config["AVATAR_UPLOAD_FOLDER"] = str(tmp_path)
    yield
    app.config["AVATAR_UPLOAD_FOLDER"] = original


# ---------------------------------------------------------------------------
# Session avatars: page + happy path
# ---------------------------------------------------------------------------

def test_me_avatar_page_renders_default(client):
    resp = client.get("/me/avatar")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Your avatar" in body
    # No avatar yet -> falls back to the controller icon.
    assert "controller-icon.png" in body


def test_upload_sets_session_avatar(client, app):
    sid = _pin_session(client)

    resp = _upload(client, _png_bytes())
    assert resp.status_code == 302  # redirect back to /me/avatar

    hex_id = _session_avatar_hex(app, sid)
    assert hex_id is not None
    assert os.path.isfile(os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], f"{hex_id}.png"))

    body = client.get("/me/avatar").get_data(as_text=True)
    assert f"/avatar/{hex_id}.png" in body
    # A 404 on the avatar URL swaps in the controller icon client-side.
    assert "onerror=" in body and "controller-icon.png" in body


def test_nav_avatar_uses_session_avatar(client, app):
    """The baseHeader nav <img> (present on every page) shows the session avatar."""
    sid = _pin_session(client)
    _upload(client, _png_bytes())
    hex_id = _session_avatar_hex(app, sid)

    body = client.get("/me/seeds").get_data(as_text=True)
    assert f"/avatar/{hex_id}.png" in body


# ---------------------------------------------------------------------------
# Session avatars: replace + remove lifecycle
# ---------------------------------------------------------------------------

def test_upload_replaces_previous(client, app):
    from sqlalchemy import func, select
    from WebHostLib.models import SessionAvatar, db

    sid = _pin_session(client)
    _upload(client, _png_bytes(color=(255, 0, 0, 255)))
    first = _session_avatar_hex(app, sid)
    _upload(client, _png_bytes(color=(0, 255, 0, 255)))
    second = _session_avatar_hex(app, sid)

    assert second != first
    avatars_dir = app.config["AVATAR_UPLOAD_FOLDER"]
    assert os.path.isfile(os.path.join(avatars_dir, f"{second}.png"))
    # The old file stays: its URL may be pinned to a slot or persisted by a client.
    assert os.path.isfile(os.path.join(avatars_dir, f"{first}.png"))

    with app.app_context():
        count = db.session.scalar(
            select(func.count()).select_from(SessionAvatar).where(SessionAvatar.session_id == sid)
        )
    assert count == 1  # exactly one row per session


def test_remove_clears_avatar(client, app):
    sid = _pin_session(client)
    _upload(client, _png_bytes())
    hex_id = _session_avatar_hex(app, sid)
    avatars_dir = app.config["AVATAR_UPLOAD_FOLDER"]

    resp = client.post("/me/avatar/remove")
    assert resp.status_code == 302
    assert _session_avatar_hex(app, sid) is None
    assert os.path.isfile(os.path.join(avatars_dir, f"{hex_id}.png"))
    body = client.get("/me/avatar").get_data(as_text=True)
    assert f"/avatar/{hex_id}.png" not in body
    assert "controller-icon.png" in body


# ---------------------------------------------------------------------------
# Session avatars: rejections + API regression guard
# ---------------------------------------------------------------------------

def test_reject_non_image(client, app):
    sid = _pin_session(client)
    resp = _upload(client, b"this is not an image", filename="x.png")
    assert resp.status_code == 302  # error flashed, redirected
    assert _session_avatar_hex(app, sid) is None


def test_mwgg_viewer_avatar_url(app):
    """The Jinja global feeding mwgg:// &avatar= returns the session's absolute
    avatar URL, or '' when the session has none."""
    from flask import session as flask_session
    from WebHostLib.avatars import mwgg_viewer_avatar_url
    from WebHostLib.models import Avatar, AvatarToken, SessionAvatar, commit, db

    sid = uuid4()
    with app.app_context():
        token = AvatarToken()
        db.session.flush()
        avatar = Avatar(id=uuid4(), owner_token=token, mime_type="image/png",
                        file_size=1, original_sha256="0" * 64)
        db.session.flush()
        SessionAvatar(session_id=sid, avatar_id=avatar.id)
        avatar_hex = avatar.id.hex
        commit()

    with app.test_request_context():
        flask_session["_id"] = sid
        assert mwgg_viewer_avatar_url().endswith(f"/avatar/{avatar_hex}.png")

    with app.test_request_context():
        flask_session["_id"] = uuid4()  # different session, no avatar
        assert mwgg_viewer_avatar_url() == ""


def test_bearer_api_upload_still_works(client):
    """Guards the avatar.py refactor: the desktop-client Bearer flow is intact."""
    mint = client.post("/api/avatar/token")
    assert mint.status_code == 200
    token = mint.get_json()["token"]

    resp = client.post(
        "/api/avatar/upload",
        data={"image": (io.BytesIO(_png_bytes()), "a.png")},
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert "/avatar/" in resp.get_json()["url"]


# ---------------------------------------------------------------------------
# Slot avatars: helpers
# ---------------------------------------------------------------------------

class _FakeTrackerData:
    """Minimal stand-in exposing only what ``compute_slot_avatars`` reads."""

    def __init__(self, room, multisave, players, names):
        self.room = room
        self._multisave = multisave
        self._players = players  # {team: [slot, ...]}
        self._names = names      # {slot: player_name}

    def get_all_players(self):
        return self._players

    def get_player_name(self, slot):
        return self._names[slot]


def _make_avatar(app):
    """Create a bare Avatar row (no file needed for URL resolution); return its id."""
    from WebHostLib.models import Avatar, AvatarToken, commit, db
    with app.app_context():
        token = AvatarToken()
        db.session.flush()
        avatar = Avatar(id=uuid4(), owner_token=token, mime_type="image/png",
                        file_size=1, original_sha256="0" * 64)
        db.session.flush()
        avatar_id = avatar.id
        commit()
    return avatar_id


# ---------------------------------------------------------------------------
# Slot avatars: model + cascade
# ---------------------------------------------------------------------------

def test_slot_avatar_cascades_with_room(app, room_factory):
    from WebHostLib.models import Room, SlotAvatar, commit, db
    room = room_factory()
    avatar_id = _make_avatar(app)

    with app.app_context():
        SlotAvatar(room_id=room.id, team=0, slot=1, avatar_id=avatar_id, set_by_session=uuid4())
        commit()
        assert SlotAvatar.get(room_id=room.id, team=0, slot=1) is not None

    with app.app_context():
        db.session.delete(Room.get(id=room.id))
        commit()

    with app.app_context():
        assert SlotAvatar.get(room_id=room.id, team=0, slot=1) is None


# ---------------------------------------------------------------------------
# Slot avatars: resolution precedence
# ---------------------------------------------------------------------------

def test_resolve_prefers_explicit_slot_avatar(app, room_factory):
    from WebHostLib.avatars import compute_slot_avatars
    from WebHostLib.models import SlotAvatar, commit
    room = room_factory()
    avatar_id = _make_avatar(app)
    with app.app_context():
        SlotAvatar(room_id=room.id, team=0, slot=1, avatar_id=avatar_id, set_by_session=uuid4())
        commit()

    # profile_data also present, but the explicit assignment wins.
    td = _FakeTrackerData(
        room,
        {"stored_data": {"profile_data_0_1": {"avatar": "https://multiworld.gg/avatar/" + "a" * 32 + ".png"}}},
        {0: [1]}, {1: "Alice"},
    )
    with app.test_request_context():
        avatars = compute_slot_avatars(td)
    assert avatars[(0, 1)] == f"/avatar/{avatar_id.hex}.png"


def test_resolve_renders_trusted_profile_data_avatar(app, room_factory):
    from WebHostLib.avatars import compute_slot_avatars
    room = room_factory()
    avatar_url = "https://multiworld.gg/avatar/" + "ab" * 16 + ".png"
    td = _FakeTrackerData(
        room,
        {"stored_data": {"profile_data_0_1": {"avatar": avatar_url}}},
        {0: [1]}, {1: "Alice"},
    )
    with app.test_request_context():
        avatars = compute_slot_avatars(td)
    assert avatars[(0, 1)] == avatar_url  # trusted-host URL rendered as-is


def test_resolve_ignores_untrusted_profile_avatar(app, room_factory):
    from WebHostLib.avatars import compute_slot_avatars
    room = room_factory()
    # Off-allowlist host, and a non-HTTPS trusted host: both rejected, matching
    # the desktop client's safe_avatar_source gate.
    for bad in ("https://evil.example/pixel.png",
                "http://multiworld.gg/avatar/" + "ab" * 16 + ".png"):
        td = _FakeTrackerData(
            room,
            {"stored_data": {"profile_data_0_1": {"avatar": bad}}},
            {0: [1]}, {1: "Alice"},
        )
        with app.test_request_context():
            avatars = compute_slot_avatars(td)
        assert (0, 1) not in avatars, bad


def test_resolve_uses_lobby_player_session_avatar(app, room_factory):
    from WebHostLib.avatars import compute_slot_avatars
    from WebHostLib.models import Lobby, LobbyPlayer, SessionAvatar, commit, db
    room = room_factory()
    avatar_id = _make_avatar(app)
    sid = uuid4()
    with app.app_context():
        SessionAvatar(session_id=sid, avatar_id=avatar_id)
        lobby = Lobby(title="t", owner=uuid4(), password_hash="", timeout_minutes=60,
                      max_yamls_per_player=1, race=False, meta="{}", state=0, max_players=0,
                      allow_custom_apworlds=True)
        db.session.flush()
        lobby.room_id = room.id
        LobbyPlayer(lobby_id=lobby.id, session_id=sid, player_name="Alice")
        commit()

    td = _FakeTrackerData(room, {"stored_data": {}}, {0: [1]}, {1: "Alice"})
    with app.test_request_context():
        avatars = compute_slot_avatars(td)
    assert avatars[(0, 1)] == f"/avatar/{avatar_id.hex}.png"


# ---------------------------------------------------------------------------
# Slot avatars: set endpoint guards
# ---------------------------------------------------------------------------

def test_set_slot_avatar_unknown_tracker_404(client, app):
    with app.test_request_context():
        path = url_for("set_slot_avatar", tracker=uuid4())
    resp = client.post(path, data={"team": "0", "slot": "1"})
    assert resp.status_code == 404


def test_set_slot_avatar_missing_form_400(client, app, room_factory):
    from WebHostLib.models import Room
    room = room_factory()
    with app.app_context():
        tracker = Room.get(id=room.id).tracker
    with app.test_request_context():
        path = url_for("set_slot_avatar", tracker=tracker)
    resp = client.post(path, data={})  # no team/slot
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Slot avatars: live-server boot seeding (apply_slot_avatars_to_stored_data)
# ---------------------------------------------------------------------------

def test_apply_seeds_profile_data_avatar(app, room_factory):
    from WebHostLib.avatars import apply_slot_avatars_to_stored_data
    from WebHostLib.models import SlotAvatar, commit, db
    room = room_factory()
    avatar_id = _make_avatar(app)
    url = f"https://mw.prismativerse.com/avatar/{avatar_id.hex}.png"
    with app.app_context():
        SlotAvatar(room_id=room.id, team=0, slot=1, avatar_id=avatar_id,
                   avatar_url=url, set_by_session=uuid4())
        commit()

    stored = {"profile_data_0_1": {"pronouns": "she/her"}}
    with app.app_context():
        apply_slot_avatars_to_stored_data(db.session, room.id, stored)

    assert stored["profile_data_0_1"]["avatar"] == url
    assert stored["profile_data_0_1"]["pronouns"] == "she/her"  # existing fields preserved


def test_apply_skips_rows_without_url(app, room_factory):
    from WebHostLib.avatars import apply_slot_avatars_to_stored_data
    from WebHostLib.models import SlotAvatar, commit, db
    room = room_factory()
    avatar_id = _make_avatar(app)
    with app.app_context():
        SlotAvatar(room_id=room.id, team=0, slot=1, avatar_id=avatar_id,
                   avatar_url=None, set_by_session=uuid4())
        commit()

    stored = {}
    with app.app_context():
        apply_slot_avatars_to_stored_data(db.session, room.id, stored)
    assert stored == {}  # nothing seeded without a URL


# ---------------------------------------------------------------------------
# Retention sweep (autohost prune_avatars)
# ---------------------------------------------------------------------------

def _token(app, note=None):
    from WebHostLib.models import AvatarToken, commit, db
    with app.app_context():
        token = AvatarToken(note=note)
        db.session.flush()
        token_id = token.token
        commit()
    return token_id


def _aged_avatar(app, token_id, days: int):
    """Avatar row plus file, owned by ``token_id`` and created ``days`` ago."""
    from datetime import timedelta
    from Utils import utcnow
    from WebHostLib.models import Avatar, commit
    avatar_id = uuid4()
    with app.app_context():
        Avatar(id=avatar_id, owner_token_id=token_id, mime_type="image/png", file_size=1,
               original_sha256="0" * 64, created_at=utcnow() - timedelta(days=days))
        commit()
    with open(os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], f"{avatar_id.hex}.png"), "wb") as f:
        f.write(b"png")
    return avatar_id


def test_prune_removes_only_old_unreferenced_avatars(app, room_factory, monkeypatch):
    from sqlalchemy import select
    from WebHostLib import autolauncher
    from WebHostLib.models import Avatar, SessionAvatar, SlotAvatar, commit, db
    avatars_dir = app.config["AVATAR_UPLOAD_FOLDER"]

    client_token = _token(app)
    session_token = _token(app, note="session-avatar:test")
    old_client = _aged_avatar(app, client_token, 400)
    newest_client = _aged_avatar(app, client_token, 300)  # the client's live avatar
    recent_client = _aged_avatar(app, _token(app), 10)
    session_current = _aged_avatar(app, session_token, 400)
    slot_pinned = _aged_avatar(app, session_token, 400)
    session_stale = _aged_avatar(app, session_token, 200)  # newest, but session tokens keep none
    room = room_factory()
    with app.app_context():
        SessionAvatar(session_id=uuid4(), avatar_id=session_current)
        SlotAvatar(room_id=room.id, team=0, slot=1, avatar_id=slot_pinned, set_by_session=uuid4())
        commit()

    with app.app_context():
        monkeypatch.setattr(autolauncher, "_engine", db.engine)
        assert autolauncher.prune_avatars({"AVATAR_RETENTION_DAYS": 0, "AVATAR_UPLOAD_FOLDER": avatars_dir}) == 0
        removed = autolauncher.prune_avatars({"AVATAR_RETENTION_DAYS": 180, "AVATAR_UPLOAD_FOLDER": avatars_dir})
        remaining = set(db.session.scalars(select(Avatar.id)).all())
    assert removed == 2

    for kept in (newest_client, recent_client, session_current, slot_pinned):
        assert kept in remaining
        assert os.path.isfile(os.path.join(avatars_dir, f"{kept.hex}.png"))
    for gone in (old_client, session_stale):
        assert gone not in remaining
        assert not os.path.isfile(os.path.join(avatars_dir, f"{gone.hex}.png"))
