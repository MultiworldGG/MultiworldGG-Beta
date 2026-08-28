"""Per-slot avatars on room trackers (PR2 of the persistent-avatar feature).

Covers the resolution precedence (explicit SlotAvatar > our-store profile_data >
lobby-player session avatar), the room-prune cascade, and the set endpoint's
guards. Resolution is unit-tested against a lightweight TrackerData stand-in so
the tests don't need a fully decodable seed.
"""
from __future__ import annotations

from uuid import uuid4

from flask import url_for


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
# Model + cascade
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
# Resolution precedence
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
# Set endpoint guards
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
# Live-server boot seeding (apply_slot_avatars_to_stored_data)
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
