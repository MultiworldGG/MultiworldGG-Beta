"""pytest fixtures for the WebHost test suite.

Mirrors the setup performed by ``test.webhost.TestBase`` (unittest style) so
fixture-based pytest tests have access to a configured Flask app, a test
client, and lightweight Room/Lobby/Seed factories.

Factories return ``SimpleNamespace`` snapshots rather than live ORM objects,
so attribute access keeps working after the database session closes
(``make_lobby`` returns the raw Lobby id instead).
"""
import pytest
from contextlib import nullcontext
from types import SimpleNamespace
from uuid import uuid4

from flask import has_app_context


@pytest.fixture(scope="session")
def app():
    from WebHostLib import app as raw_app
    from WebHost import get_app

    raw_app.config["PONY"] = {
        "provider": "sqlite",
        "filename": ":memory:",
        "create_db": True,
    }
    raw_app.config.update({
        "TESTING": True,
        "DEBUG": True,
    })
    try:
        return get_app()
    except (AssertionError, ValueError) as e:
        # get_app() re-registers blueprints on the import-time WebHostLib.app; a second
        # call raises (AssertionError on older Flask, ValueError on newer). Either way the
        # already-configured raw_app is the app we want.
        message = e.args[0] if e.args else ""
        if "register_blueprint" not in message and "already registered" not in message:
            raise
        return raw_app


@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture
def db_session(app):
    """Yield a SQLAlchemy session bound to an active app context.

    Used by tests that need to drive ``db.session`` directly (e.g.
    calling ``assign_short_id`` outside a request). Reuses the current
    app context if one is already active so it nests cleanly with
    ``room_factory``.
    """
    from WebHostLib.models import db

    ctx_mgr = nullcontext() if has_app_context() else app.app_context()
    with ctx_mgr:
        yield db.session


@pytest.fixture
def room_factory(app):
    from WebHostLib.models import db, commit, Room, Seed

    def _make(**overrides):
        ctx_mgr = nullcontext() if has_app_context() else app.app_context()
        with ctx_mgr:
            owner = overrides.pop("owner", uuid4())
            seed = Seed(multidata=b"", owner=owner)
            db.session.flush()
            room = Room(seed_id=seed.id, owner=owner, tracker=uuid4(), **overrides)
            db.session.flush()
            snapshot = SimpleNamespace(
                id=room.id,
                seed_id=room.seed_id,
                short_id=room.short_id,
            )
            commit()
            return snapshot
    return _make


@pytest.fixture
def seed_factory(app):
    """Create a Seed row owned by a given session UUID."""
    from WebHostLib.models import Seed, db, commit

    def _make(**overrides):
        with app.app_context():
            owner = overrides.pop("owner", uuid4())
            seed = Seed(multidata=b"", owner=owner, **overrides)
            db.session.flush()
            snapshot = SimpleNamespace(id=seed.id, owner=seed.owner)
            commit()
            return snapshot
    return _make


@pytest.fixture
def lobby_factory(app):
    from WebHostLib.models import db, commit, Lobby, Room, Seed, LOBBY_OPEN, LOBBY_DONE

    def _make(with_finished_room=False, **overrides):
        with app.app_context():
            owner = overrides.pop("owner", uuid4())
            state = LOBBY_DONE if with_finished_room else LOBBY_OPEN
            lobby = Lobby(
                title=overrides.pop("title", "Test Lobby"),
                owner=owner,
                password_hash="",
                timeout_minutes=60,
                max_yamls_per_player=3,
                race=False,
                meta="{}",
                state=state,
                max_players=0,
                allow_custom_apworlds=True,
            )
            db.session.flush()

            room_snapshot = None
            if with_finished_room:
                seed = Seed(multidata=b"", owner=owner)
                db.session.flush()
                room = Room(seed_id=seed.id, owner=owner, tracker=uuid4())
                db.session.flush()
                lobby.seed_id = seed.id
                lobby.room_id = room.id
                room_snapshot = SimpleNamespace(id=room.id, seed_id=seed.id)

            snapshot = SimpleNamespace(
                id=lobby.id,
                seed_id=lobby.seed_id,
                room=room_snapshot,
            )
            commit()
            return snapshot
    return _make


@pytest.fixture
def make_lobby(app):
    """Create a Lobby owned by the given session, bypassing lobby_factory
    (which hard-codes state from with_finished_room). Returns the lobby id."""
    from WebHostLib.models import Lobby, commit

    def _make(owner, **overrides):
        with app.app_context():
            kw = dict(title="Test Lobby", owner=owner, password_hash="",
                      timeout_minutes=60, max_yamls_per_player=3, race=False,
                      meta="{}", state=0, max_players=0,
                      allow_custom_apworlds=True)
            kw.update(overrides)
            lobby = Lobby(**kw)
            commit()
            return lobby.id
    return _make


@pytest.fixture
def _wipe_rooms_after_test(app):
    """Wipe Room/Seed/Command/Lobby/LobbyMessage rows around a test.

    The session-scoped ``app`` fixture shares one in-memory DB across the
    whole suite: hardcoded short_ids would trip the UNIQUE constraint across
    tests, and count-based tests (e.g. the backfill script's stats) need a
    known-empty starting state regardless of module ordering. Wipes before the
    test for the clean start and after it so no residue leaks onward. Opt in
    per module or class with
    ``pytest.mark.usefixtures("_wipe_rooms_after_test")``.
    """
    def _wipe():
        from WebHostLib.models import db, Room, Seed, Command, Lobby, LobbyMessage
        with app.app_context():
            db.session.query(LobbyMessage).delete()
            db.session.query(Lobby).delete()
            db.session.query(Command).delete()
            db.session.query(Room).delete()
            db.session.query(Seed).delete()
            db.session.commit()

    _wipe()
    yield
    _wipe()
