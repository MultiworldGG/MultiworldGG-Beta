"""
Tests for the backfill_short_ids command.

Phase 2b. The backfill script must:
- Assign short_ids to rooms where it's NULL
- Skip rooms that already have one
- Be idempotent (running twice gives the same result as running once)
- Handle the empty case (no rooms to backfill)
"""

import pytest

from WebHostLib.scripts.backfill_short_ids import backfill
from WebHostLib.short_id import is_well_formed


@pytest.fixture(autouse=True)
def _wipe_rooms_after_test(app):
    """The session-scoped ``app`` fixture shares one in-memory DB across
    all tests in this module. Each test relies on a known starting
    count, so wipe room/seed/command/lobby rows after each test.
    """
    yield
    from WebHostLib.models import db, Room, Seed, Command, Lobby, LobbyMessage
    with app.app_context():
        db.session.query(LobbyMessage).delete()
        db.session.query(Lobby).delete()
        db.session.query(Command).delete()
        db.session.query(Room).delete()
        db.session.query(Seed).delete()
        db.session.commit()


def _get_room_short_id(db_session, room_id):
    from WebHostLib.models import Room
    return db_session.get(Room, room_id).short_id


class TestBackfill:
    def test_assigns_short_id_to_rooms_without_one(
        self, db_session, room_factory
    ):
        rooms = [room_factory(short_id=None) for _ in range(5)]

        stats = backfill(batch_size=10)

        for room in rooms:
            short_id = _get_room_short_id(db_session, room.id)
            assert short_id is not None
            assert is_well_formed(short_id)
        assert stats["assigned"] == 5
        assert stats["total"] == 5
        assert stats["failed"] == 0

    def test_skips_rooms_with_existing_short_id(
        self, db_session, room_factory
    ):
        existing = room_factory(short_id="EXIST1")
        without = room_factory(short_id=None)

        backfill(batch_size=10)

        assert _get_room_short_id(db_session, existing.id) == "EXIST1"
        assert _get_room_short_id(db_session, without.id) is not None

    def test_idempotent(self, db_session, room_factory):
        """Running backfill twice gives the same result as running once."""
        rooms = [room_factory(short_id=None) for _ in range(3)]

        backfill(batch_size=10)
        first_run_ids = [_get_room_short_id(db_session, r.id) for r in rooms]
        assert all(sid is not None for sid in first_run_ids)

        stats = backfill(batch_size=10)
        assert stats["total"] == 0
        assert stats["assigned"] == 0

        for room, original in zip(rooms, first_run_ids):
            assert _get_room_short_id(db_session, room.id) == original

    def test_empty_database(self, db_session):
        """Backfill on an empty DB succeeds without error."""
        stats = backfill(batch_size=10)
        assert stats["total"] == 0
        assert stats["assigned"] == 0
        assert stats["failed"] == 0

    def test_dry_run_does_not_persist(self, db_session, room_factory):
        room = room_factory(short_id=None)

        stats = backfill(batch_size=10, dry_run=True)

        assert _get_room_short_id(db_session, room.id) is None
        assert stats["total"] == 1

    def test_no_collisions_among_assigned(self, db_session, room_factory):
        """All assigned short_ids in a single backfill should be unique."""
        for _ in range(20):
            room_factory(short_id=None)

        backfill(batch_size=10)

        from sqlalchemy import select
        from WebHostLib.models import Room
        all_short_ids = [
            r.short_id for r in db_session.scalars(select(Room)).all()
            if r.short_id is not None
        ]
        assert len(all_short_ids) == 20
        assert len(all_short_ids) == len(set(all_short_ids)), (
            "Backfill produced duplicate short_ids"
        )

    def test_batch_commit_works(self, db_session, room_factory):
        """Backfill with batch_size smaller than total should still
        complete and persist everything."""
        for _ in range(15):
            room_factory(short_id=None)

        stats = backfill(batch_size=5)
        assert stats["assigned"] == 15

        from sqlalchemy import select, func
        from WebHostLib.models import Room
        unassigned = db_session.scalar(
            select(func.count()).select_from(Room).where(Room.short_id.is_(None))
        )
        assert unassigned == 0
