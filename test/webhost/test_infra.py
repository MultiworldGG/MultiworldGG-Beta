"""Webhost infrastructure tests; add new infra tests here.

Covers the pony-style auto-add behaviour of ``WebHostLib.models.Base``, the
behavioral invariants of ``WebHostLib.autolauncher.cleanup()``, and the
``WebHost._pony_config_to_sqlalchemy_uri`` legacy-config mapping.
"""
from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from WebHost import _pony_config_to_sqlalchemy_uri


# ---------------------------------------------------------------------------
# models.Base auto-add: constructing any Base subclass inside a Flask app
# context registers the new instance with db.session as a pending insert via
# the patched __init__ -- no explicit db.session.add() call is required.
# ---------------------------------------------------------------------------

def test_constructing_entity_auto_adds_to_session(app):
    from WebHostLib.models import db, Seed

    with app.app_context():
        before = set(db.session.new)
        seed = Seed(multidata=b"", owner=uuid4())
        # No explicit db.session.add(seed) call happens anywhere above.
        new_objects = set(db.session.new)

    assert seed not in before
    assert seed in new_objects


def test_auto_added_entity_persists_on_commit_without_explicit_add(app):
    from WebHostLib.models import db, commit, Seed

    owner = uuid4()
    with app.app_context():
        seed = Seed(multidata=b"x", owner=owner)
        # Only commit() -- still never an explicit session.add().
        commit()
        seed_id = seed.id

    with app.app_context():
        fetched = Seed.get(id=seed_id)
        assert fetched is not None
        assert fetched.owner == owner


# ---------------------------------------------------------------------------
# autolauncher.cleanup() invariants.
#
# ``cleanup()`` deletes unowned user content: it removes ``Room``/``Seed``
# rows owned by the all-zero "null owner" sentinel (``UUID(int=0)``) and
# orphaned ``Slot`` rows (``seed_id IS NULL``), while leaving real-owner
# content and seed-attached slots alone.
#
# These tests drive the real ``cleanup()`` against the in-memory test database
# by monkeypatching the module-level ``_engine`` it reads through
# ``_get_engine()`` (the same indirection the task notes allows), then assert
# the observable database state afterwards. A plausible mutation to the WHERE
# clauses (e.g. turning ``Room.owner == null_owner`` into a falsiness check,
# or flipping the ``Slot.seed_id == None`` predicate) makes these fail.
# ---------------------------------------------------------------------------

@pytest.fixture
def cleanup_on_test_db(app):
    """Point autolauncher.cleanup()'s engine at the test app's DB engine.

    Yields the ``cleanup`` callable; restores the previous ``_engine`` and
    deletes any Room/Seed/Slot rows the test created, so nothing leaks into the
    session-scoped test DB (e.g. the backfill tests count rooms-without-short-id).
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


def test_cleanup_keeps_real_owner_room_and_seed(app, cleanup_on_test_db):
    """A Room/Seed with a genuine (non-sentinel) owner survives cleanup().

    Guards the equality predicate ``Room.owner == UUID(int=0)``: a falsiness
    guard like ``if not owner`` would (a) never match the truthy sentinel and
    (b) if rewritten the other way, delete every row. Either regression would
    flip one of these assertions.
    """
    from WebHostLib.models import db, commit, Room, Seed

    owner = uuid4()
    with app.app_context():
        seed = Seed(multidata=b"", owner=owner)
        db.session.flush()
        room = Room(seed_id=seed.id, owner=owner, tracker=uuid4())
        db.session.flush()
        room_id, seed_id = room.id, seed.id
        commit()

    cleanup_on_test_db()

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Room, room_id) is not None, "real-owner Room was wrongly deleted"
        assert db.session.get(Seed, seed_id) is not None, "real-owner Seed was wrongly deleted"


def test_cleanup_deletes_sentinel_owned_room_and_seed(app, cleanup_on_test_db):
    """A Room/Seed owned by the UUID(int=0) "null owner" sentinel IS deleted.

    This is the deletion half of cleanup()'s contract. It could not be tested
    until the owner columns moved to sqlalchemy.Uuid: the legacy UUID type stored
    the all-zero sentinel as integer 0 under SQLite and crashed on read-back, so
    cleanup() threw before it could delete anything. A regression of
    ``Room.owner == UUID(int=0)`` to a falsiness guard (which never matches the
    truthy sentinel) would leave these rows behind.
    """
    from WebHostLib.models import db, commit, Room, Seed

    null_owner = UUID(int=0)
    with app.app_context():
        seed = Seed(multidata=b"", owner=null_owner)
        db.session.flush()
        room = Room(seed_id=seed.id, owner=null_owner, tracker=uuid4())
        db.session.flush()
        room_id, seed_id = room.id, seed.id
        commit()

    cleanup_on_test_db()

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Room, room_id) is None, "sentinel-owned Room was not deleted"
        assert db.session.get(Seed, seed_id) is None, "sentinel-owned Seed was not deleted"


def test_cleanup_deletes_orphan_slot_keeps_attached_slot(app, cleanup_on_test_db):
    """cleanup() deletes only Slots with ``seed_id IS NULL``; attached slots stay.

    Guards ``select(Slot).where(Slot.seed_id == None)``. Mutating that to
    ``!= None`` (or dropping the predicate) would delete the seed-attached slot
    and/or spare the orphan, failing these assertions.
    """
    from WebHostLib.models import db, commit, Room, Seed, Slot

    owner = uuid4()
    with app.app_context():
        seed = Seed(multidata=b"", owner=owner)
        db.session.flush()
        # Keep the seed alive past cleanup's "delete unreferenced seeds" pass.
        room = Room(seed_id=seed.id, owner=owner, tracker=uuid4())
        db.session.flush()
        orphan = Slot(player_id=1, player_name="orphan", game="Clique", seed_id=None)
        attached = Slot(player_id=2, player_name="attached", game="Clique", seed_id=seed.id)
        db.session.flush()
        orphan_id, attached_id = orphan.id, attached.id
        room_id, seed_id = room.id, seed.id
        commit()

    cleanup_on_test_db()

    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Slot, orphan_id) is None, "orphan Slot (seed_id NULL) was not deleted"
        assert db.session.get(Slot, attached_id) is not None, "seed-attached Slot was wrongly deleted"
        # The seed is referenced by a room, so it (and its room) must remain.
        assert db.session.get(Seed, seed_id) is not None
        assert db.session.get(Room, room_id) is not None


def test_cleanup_keeps_seed_referenced_by_real_room(app, cleanup_on_test_db):
    """A Seed is only deletable when no Room references it.

    Even an otherwise-orphanable Seed must survive while a Room points at it.
    Guards the ``if not session.scalars(select(Room).where(Room.seed_id == seed.id)...)``
    reference check inside the seed-deletion loop.
    """
    from WebHostLib.models import db, commit, Room, Seed

    owner = uuid4()
    with app.app_context():
        seed = Seed(multidata=b"", owner=owner)
        db.session.flush()
        room = Room(seed_id=seed.id, owner=owner, tracker=uuid4())
        db.session.flush()
        seed_id, room_id = seed.id, room.id
        commit()

    cleanup_on_test_db()

    with app.app_context():
        db.session.expire_all()
        referencing = db.session.scalars(
            select(Room).where(Room.seed_id == seed_id).limit(1)
        ).first()
        assert referencing is not None, "Room reference to Seed disappeared"
        assert db.session.get(Seed, seed_id) is not None, "referenced Seed was wrongly deleted"
        assert db.session.get(Room, room_id) is not None


# ---------------------------------------------------------------------------
# WebHost._pony_config_to_sqlalchemy_uri: the legacy-PONY-config ->
# SQLAlchemy-URI mapping contract - sqlite filename handling (including the
# :memory: special case), postgres/postgresql psycopg2 URIs, and the
# ValueError raised for unsupported providers.
# ---------------------------------------------------------------------------

def test_pony_config_to_sqlalchemy_uri_sqlite_memory_postgres_and_unsupported():
    # sqlite with explicit :memory: filename is special-cased to an in-memory URI
    assert _pony_config_to_sqlalchemy_uri(
        {"provider": "sqlite", "filename": ":memory:"}
    ) == "sqlite:///:memory:"

    # sqlite with a regular filename maps to sqlite:///<filename>
    assert _pony_config_to_sqlalchemy_uri(
        {"provider": "sqlite", "filename": "ap.db3"}
    ) == "sqlite:///ap.db3"

    # provider defaults to sqlite and filename defaults to ap.db3
    assert _pony_config_to_sqlalchemy_uri({}) == "sqlite:///ap.db3"

    # both postgres and postgresql build the same psycopg2 URI
    pg_config = {
        "provider": "postgres",
        "host": "db.example",
        "port": 6543,
        "user": "u",
        "password": "p",
        "database": "mwgg",
    }
    expected = "postgresql+psycopg2://u:p@db.example:6543/mwgg"
    assert _pony_config_to_sqlalchemy_uri(pg_config) == expected
    assert _pony_config_to_sqlalchemy_uri({**pg_config, "provider": "postgresql"}) == expected

    # postgres falls back to localhost:5432 and empty credentials/database
    assert _pony_config_to_sqlalchemy_uri({"provider": "postgres"}) == \
        "postgresql+psycopg2://:@localhost:5432/"

    # an unsupported provider raises ValueError
    with pytest.raises(ValueError, match="Unsupported PONY provider"):
        _pony_config_to_sqlalchemy_uri({"provider": "mysql"})
