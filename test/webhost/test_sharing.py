"""Webhost sharing/co-ownership tests; add new sharing tests here.

Covers the is_authorized/is_primary_owner helpers, the invite flow (mint,
accept, single-use, expiry, transfer mode), co-owner removal, dashboard
inclusion of co-owned rooms, and behavioral invariants of
WebHostLib/sharing.py that prose comments used to describe: the co-owner
DELETE endpoint is idempotent (200, not 404, for a missing row), and
accepting a transfer as an existing co-owner drops the now-redundant
co-owner row, leaving the accepter as primary owner only.
"""
from __future__ import annotations

from datetime import timedelta
from uuid import UUID, uuid4

from Utils import utcnow


def _login(client, session_id: UUID):
    with client.session_transaction() as sess:
        sess["_id"] = session_id


def _suuid(uid: UUID) -> str:
    from WebHostLib import to_url
    return to_url(uid)


# ---------------------------------------------------------------------------
# is_authorized helper
# ---------------------------------------------------------------------------

def test_primary_owner_is_authorized(app, room_factory):
    from WebHostLib.models import Room
    from WebHostLib.ownership import is_authorized, is_primary_owner

    owner = uuid4()
    snapshot = room_factory(owner=owner)
    with app.app_context():
        room = Room.get(id=snapshot.id)
        assert is_authorized(room, owner) is True
        assert is_primary_owner(room, owner) is True


def test_stranger_is_not_authorized(app, room_factory):
    from WebHostLib.models import Room
    from WebHostLib.ownership import is_authorized

    snapshot = room_factory(owner=uuid4())
    stranger = uuid4()
    with app.app_context():
        room = Room.get(id=snapshot.id)
        assert is_authorized(room, stranger) is False


def test_co_owner_is_authorized_but_not_primary(app, room_factory):
    from WebHostLib.models import Room, RoomCoOwner, commit
    from WebHostLib.ownership import is_authorized, is_primary_owner

    owner = uuid4()
    co_owner = uuid4()
    snapshot = room_factory(owner=owner)
    with app.app_context():
        RoomCoOwner(room_id=snapshot.id, session_id=co_owner, granted_by=owner)
        commit()
        room = Room.get(id=snapshot.id)
        assert is_authorized(room, co_owner) is True
        assert is_primary_owner(room, co_owner) is False


# ---------------------------------------------------------------------------
# Invite create - primary only
# ---------------------------------------------------------------------------

def test_invite_create_requires_primary_owner(client, app, room_factory):
    """Only the primary owner can mint invites."""
    owner = uuid4()
    snapshot = room_factory(owner=owner)
    short_id = _suuid(snapshot.id)

    # Stranger can't mint
    _login(client, uuid4())
    res = client.post(f"/api/room/{short_id}/invite", json={"mode": "co_owner"})
    assert res.status_code == 403

    # Owner can
    _login(client, owner)
    res = client.post(f"/api/room/{short_id}/invite", json={"mode": "co_owner"})
    assert res.status_code == 200
    body = res.get_json()
    assert "url" in body
    assert "expires_at" in body
    assert body["mode"] == "co_owner"


def test_invite_create_rejects_unknown_mode(client, app, room_factory):
    owner = uuid4()
    snapshot = room_factory(owner=owner)
    _login(client, owner)
    res = client.post(f"/api/room/{_suuid(snapshot.id)}/invite", json={"mode": "evil"})
    assert res.status_code == 400


# ---------------------------------------------------------------------------
# Invite accept - happy path + single-use
# ---------------------------------------------------------------------------

def test_co_owner_accept_grants_access(client, app, room_factory):
    owner = uuid4()
    snapshot = room_factory(owner=owner)

    # Owner mints an invite
    _login(client, owner)
    res = client.post(f"/api/room/{_suuid(snapshot.id)}/invite", json={"mode": "co_owner"})
    invite_url = res.get_json()["url"]
    token_path = invite_url.split("/me/accept/")[-1]

    # New session accepts
    invitee = uuid4()
    _login(client, invitee)
    res = client.get(f"/me/accept/{token_path}", follow_redirects=False)
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/me")

    # Invitee is now a co-owner
    from WebHostLib.models import Room, RoomCoOwner
    from WebHostLib.ownership import is_authorized
    with app.app_context():
        row = client.application.extensions["sqlalchemy"].session.get(
            RoomCoOwner, (snapshot.id, invitee))
        assert row is not None
        room = Room.get(id=snapshot.id)
        assert is_authorized(room, invitee) is True


def test_invite_is_single_use(client, app, room_factory):
    owner = uuid4()
    snapshot = room_factory(owner=owner)

    _login(client, owner)
    res = client.post(f"/api/room/{_suuid(snapshot.id)}/invite", json={"mode": "co_owner"})
    token_path = res.get_json()["url"].split("/me/accept/")[-1]

    # First accept succeeds
    invitee_a = uuid4()
    _login(client, invitee_a)
    client.get(f"/me/accept/{token_path}", follow_redirects=False)

    # Second accept (different session) sees the same link as already-used.
    invitee_b = uuid4()
    _login(client, invitee_b)
    client.get(f"/me/accept/{token_path}", follow_redirects=False)
    # Follow to /me to see the flash
    res = client.get("/me")
    assert b"already been used" in res.data

    # Only invitee_a is a co-owner
    from WebHostLib.models import RoomCoOwner, db
    with app.app_context():
        assert db.session.get(RoomCoOwner, (snapshot.id, invitee_a)) is not None
        assert db.session.get(RoomCoOwner, (snapshot.id, invitee_b)) is None


def test_expired_invite_is_rejected(client, app, room_factory):
    from WebHostLib.models import OwnershipInvite, commit, db

    owner = uuid4()
    snapshot = room_factory(owner=owner)

    # Mint an invite directly with a past expiry
    with app.app_context():
        invite = OwnershipInvite(
            token=uuid4(),
            target_kind="room",
            target_id=snapshot.id,
            mode="co_owner",
            created_by=owner,
            expires_at=utcnow() - timedelta(hours=1),
        )
        commit()
        token = invite.token

    invitee = uuid4()
    _login(client, invitee)
    client.get(f"/me/accept/{_suuid(token)}", follow_redirects=False)
    res = client.get("/me")
    assert b"expired" in res.data

    from WebHostLib.models import RoomCoOwner
    with app.app_context():
        assert db.session.get(RoomCoOwner, (snapshot.id, invitee)) is None


# ---------------------------------------------------------------------------
# Transfer mode
# ---------------------------------------------------------------------------

def test_transfer_swaps_primary_and_demotes_old_owner(client, app, room_factory):
    from WebHostLib.models import Room, RoomCoOwner, db

    old_primary = uuid4()
    new_primary = uuid4()
    snapshot = room_factory(owner=old_primary)

    _login(client, old_primary)
    res = client.post(f"/api/room/{_suuid(snapshot.id)}/invite", json={"mode": "transfer"})
    token_path = res.get_json()["url"].split("/me/accept/")[-1]

    _login(client, new_primary)
    client.get(f"/me/accept/{token_path}", follow_redirects=False)

    with app.app_context():
        room = Room.get(id=snapshot.id)
        assert room.owner == new_primary
        # Old primary should now be a co-owner (kept access)
        assert db.session.get(RoomCoOwner, (snapshot.id, old_primary)) is not None


def test_transfer_accept_by_existing_co_owner_drops_co_owner_row(client, app, room_factory):
    """Accepting a transfer as an existing co-owner drops the now-redundant
    co-owner row, leaving the accepter as primary owner only."""
    from WebHostLib.models import Room, RoomCoOwner, commit, db
    from WebHostLib.ownership import is_primary_owner

    old_primary = uuid4()
    co_then_primary = uuid4()
    snapshot = room_factory(owner=old_primary)

    # The accepting user already holds a co-owner row before the transfer.
    with app.app_context():
        RoomCoOwner(room_id=snapshot.id, session_id=co_then_primary, granted_by=old_primary)
        commit()
        assert db.session.get(RoomCoOwner, (snapshot.id, co_then_primary)) is not None

    _login(client, old_primary)
    res = client.post(f"/api/room/{_suuid(snapshot.id)}/invite", json={"mode": "transfer"})
    token_path = res.get_json()["url"].split("/me/accept/")[-1]

    _login(client, co_then_primary)
    client.get(f"/me/accept/{token_path}", follow_redirects=False)

    with app.app_context():
        room = Room.get(id=snapshot.id)
        # New owner is primary...
        assert room.owner == co_then_primary
        assert is_primary_owner(room, co_then_primary) is True
        # ...and their old, now-redundant co-owner row is gone.
        assert db.session.get(RoomCoOwner, (snapshot.id, co_then_primary)) is None


# ---------------------------------------------------------------------------
# Co-owner remove - primary only
# ---------------------------------------------------------------------------

def test_primary_can_remove_co_owner(client, app, room_factory):
    from WebHostLib.models import RoomCoOwner, commit, db

    owner = uuid4()
    co_owner = uuid4()
    snapshot = room_factory(owner=owner)
    with app.app_context():
        RoomCoOwner(room_id=snapshot.id, session_id=co_owner, granted_by=owner)
        commit()

    _login(client, owner)
    res = client.delete(f"/api/room/{_suuid(snapshot.id)}/co_owner/{_suuid(co_owner)}")
    assert res.status_code == 200
    with app.app_context():
        assert db.session.get(RoomCoOwner, (snapshot.id, co_owner)) is None


def test_co_owner_cannot_remove_other_co_owner(client, app, room_factory):
    from WebHostLib.models import RoomCoOwner, commit, db

    owner = uuid4()
    co_a = uuid4()
    co_b = uuid4()
    snapshot = room_factory(owner=owner)
    with app.app_context():
        RoomCoOwner(room_id=snapshot.id, session_id=co_a, granted_by=owner)
        RoomCoOwner(room_id=snapshot.id, session_id=co_b, granted_by=owner)
        commit()

    _login(client, co_a)
    res = client.delete(f"/api/room/{_suuid(snapshot.id)}/co_owner/{_suuid(co_b)}")
    assert res.status_code == 403
    with app.app_context():
        assert db.session.get(RoomCoOwner, (snapshot.id, co_b)) is not None


def test_remove_nonexistent_co_owner_returns_ok_not_404(client, app, room_factory):
    """The co-owner DELETE endpoint is idempotent: a missing row still
    returns 200 {"ok": True}."""
    from WebHostLib.models import RoomCoOwner, db

    owner = uuid4()
    never_a_co_owner = uuid4()
    snapshot = room_factory(owner=owner)

    # Sanity: the target really has no co-owner row.
    with app.app_context():
        assert db.session.get(RoomCoOwner, (snapshot.id, never_a_co_owner)) is None

    _login(client, owner)
    res = client.delete(
        f"/api/room/{_suuid(snapshot.id)}/co_owner/{_suuid(never_a_co_owner)}")

    assert res.status_code == 200
    assert res.get_json() == {"ok": True}


# ---------------------------------------------------------------------------
# Dashboard inclusion
# ---------------------------------------------------------------------------

def test_dashboard_includes_co_owned_rooms(client, app, room_factory):
    from WebHostLib.models import RoomCoOwner, commit
    from WebHostLib.dashboard import get_dashboard_data

    owner = uuid4()
    co_owner = uuid4()
    snapshot = room_factory(owner=owner)
    with app.app_context():
        RoomCoOwner(room_id=snapshot.id, session_id=co_owner, granted_by=owner)
        commit()
        data = get_dashboard_data(co_owner)

    assert data.is_empty is False
    assert data.stats.active_rooms == 1
