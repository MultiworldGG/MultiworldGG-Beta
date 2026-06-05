"""Behavioral invariants for WebHostLib/sharing.py.

Pins non-obvious response/state shapes that prose comments used to describe:

* The co-owner DELETE endpoint is idempotent (200, not 404, for a missing row).
* Accepting a transfer as an existing co-owner drops the now-redundant
  co-owner row, leaving the accepter as primary owner only.
"""
from __future__ import annotations

from uuid import UUID, uuid4


def _login(client, session_id: UUID):
    with client.session_transaction() as sess:
        sess["_id"] = session_id


def _suuid(uid: UUID) -> str:
    from WebHostLib import to_url
    return to_url(uid)


# ---------------------------------------------------------------------------
# DELETE co-owner is idempotent: a missing row still returns 200 {"ok": True}
# ---------------------------------------------------------------------------

def test_remove_nonexistent_co_owner_returns_ok_not_404(client, app, room_factory):
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
# Transfer accepted by an existing co-owner drops the redundant co-owner row
# ---------------------------------------------------------------------------

def test_transfer_accept_by_existing_co_owner_drops_co_owner_row(client, app, room_factory):
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
