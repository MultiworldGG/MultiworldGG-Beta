"""Age-based auto-deletion in WebHostLib.autolauncher.cleanup().

``cleanup(config)`` reads ``ROOM_AUTO_DELETE`` (minimum age in days, 0 to
disable). When enabled it deletes, in addition to the unowned content covered
by test_autolauncher_invariants.py, Rooms whose ``last_activity`` and Seeds
whose ``creation_time`` are older than the cutoff. Seeds are still only
deletable once no Room references them, so an old Seed with a recent Room
survives, while an old Seed whose only Room was deleted in the same pass goes
with it. Slots of a deleted Seed are cascade-deleted.

Same harness as test_autolauncher_invariants.py: drive the real ``cleanup()``
against the in-memory test database by monkeypatching the module-level
``_engine`` it reads through ``_get_engine()``, then assert the observable
database state afterwards.
"""
from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select

from Utils import utcnow

AUTO_DELETE_DAYS = 5
ENABLED = {"ROOM_AUTO_DELETE": AUTO_DELETE_DAYS}
DISABLED = {"ROOM_AUTO_DELETE": 0}


@pytest.fixture
def cleanup_on_test_db(app):
    """Point autolauncher.cleanup()'s engine at the test app's DB engine.

    Yields the ``cleanup`` callable; restores the previous ``_engine`` and
    deletes any Room/Seed/Slot rows the test created, so nothing leaks into the
    session-scoped test DB.
    """
    import WebHostLib.autolauncher as autolauncher
    from WebHostLib.models import db, commit, Room, Seed, Slot

    models = (Slot, Room, Seed)  # children before parents on teardown delete
    with app.app_context():
        engine = db.engine
        before = {M: {row.id for row in db.session.scalars(select(M)).all()} for M in models}
    previous = autolauncher._engine
    autolauncher._engine = engine
    try:
        yield autolauncher.cleanup
    finally:
        autolauncher._engine = previous
        with app.app_context():
            for M in models:
                for row in db.session.scalars(select(M)).all():
                    if row.id not in before[M]:
                        db.session.delete(row)
            commit()


def _make_seed(db, owner, creation_time):
    from WebHostLib.models import Seed

    seed = Seed(multidata=b"", owner=owner, creation_time=creation_time)
    db.session.flush()
    return seed


def _make_room(db, seed, owner, last_activity):
    from WebHostLib.models import Room

    room = Room(seed_id=seed.id, owner=owner, tracker=uuid4(), last_activity=last_activity)
    db.session.flush()
    return room


def test_cleanup_auto_delete(app, cleanup_on_test_db):
    """With ROOM_AUTO_DELETE set, old owned content is deleted, recent kept.

    Rooms age out on ``last_activity``, Seeds on ``creation_time`` — but a
    Seed only goes once no Room references it. The interesting case is s1: its
    only Room aged out in the same pass, so the (old) Seed must follow it.
    """
    from WebHostLib.models import db, commit, Room, Seed

    now = utcnow()
    old_time = now - timedelta(days=AUTO_DELETE_DAYS * 2)
    recent_time = now - timedelta(days=AUTO_DELETE_DAYS - 3)

    with app.app_context():
        s1 = _make_seed(db, uuid4(), old_time)  # old seed, old room: both deleted
        r1 = _make_room(db, s1, uuid4(), old_time)
        s2 = _make_seed(db, uuid4(), old_time)  # old seed, recent room: both kept
        r2 = _make_room(db, s2, uuid4(), recent_time)
        s3 = _make_seed(db, uuid4(), old_time)  # old seed, no rooms: deleted
        s4 = _make_seed(db, uuid4(), recent_time)  # recent seed, no rooms: kept
        ids = {name: obj.id for name, obj in
               (("s1", s1), ("r1", r1), ("s2", s2), ("r2", r2), ("s3", s3), ("s4", s4))}
        commit()

    cleanup_on_test_db(ENABLED)

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Room, ids["r1"]) is None, "old Room was not deleted"
        assert db.session.get(Seed, ids["s1"]) is None, \
            "old Seed whose only Room aged out was not deleted"
        assert db.session.get(Room, ids["r2"]) is not None, "recent Room was wrongly deleted"
        assert db.session.get(Seed, ids["s2"]) is not None, \
            "old Seed with a recent Room was wrongly deleted"
        assert db.session.get(Seed, ids["s3"]) is None, "old room-less Seed was not deleted"
        assert db.session.get(Seed, ids["s4"]) is not None, "recent Seed was wrongly deleted"


def test_cleanup_disabled(app, cleanup_on_test_db):
    """ROOM_AUTO_DELETE=0 (and no config at all) leaves old owned content alone."""
    from WebHostLib.models import db, commit, Room, Seed

    old_time = utcnow() - timedelta(days=AUTO_DELETE_DAYS * 2)
    with app.app_context():
        seed = _make_seed(db, uuid4(), old_time)
        room = _make_room(db, seed, uuid4(), old_time)
        room_id, seed_id = room.id, seed.id
        commit()

    cleanup_on_test_db(DISABLED)
    cleanup_on_test_db()  # config defaults to disabled

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Room, room_id) is not None, \
            "Room was deleted despite auto-delete being disabled"
        assert db.session.get(Seed, seed_id) is not None, \
            "Seed was deleted despite auto-delete being disabled"


def test_cleanup_slots(app, cleanup_on_test_db):
    """Slots follow their Seed: cascade-deleted with an old Seed, kept with a recent one."""
    from WebHostLib.models import db, commit, Seed, Slot

    now = utcnow()
    old_time = now - timedelta(days=AUTO_DELETE_DAYS * 2)

    with app.app_context():
        old_seed = _make_seed(db, uuid4(), old_time)
        old_slot = Slot(player_id=1, player_name="P1", game="Clique", seed_id=old_seed.id)
        recent_seed = _make_seed(db, uuid4(), now)
        recent_slot = Slot(player_id=2, player_name="P2", game="Clique", seed_id=recent_seed.id)
        db.session.flush()
        ids = {"old_seed": old_seed.id, "old_slot": old_slot.id,
               "recent_seed": recent_seed.id, "recent_slot": recent_slot.id}
        commit()

    cleanup_on_test_db(ENABLED)

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Seed, ids["old_seed"]) is None, "old Seed was not deleted"
        assert db.session.get(Slot, ids["old_slot"]) is None, \
            "Slot of deleted Seed was not cascade-deleted"
        assert db.session.get(Seed, ids["recent_seed"]) is not None, \
            "recent Seed was wrongly deleted"
        assert db.session.get(Slot, ids["recent_slot"]) is not None, \
            "Slot of kept Seed was wrongly deleted"
