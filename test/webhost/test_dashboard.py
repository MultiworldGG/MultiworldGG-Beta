"""Tests for the /me dashboard data aggregation."""
from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest

from Utils import utcnow
from WebHostLib.dashboard import (
    DashboardData,
    DashboardStats,
    RoomStatus,
    classify_room,
    get_dashboard_data,
)


# ---------------------------------------------------------------------------
# classify_room — pure function, no DB needed
# ---------------------------------------------------------------------------

class TestClassifyRoom:
    def test_recent_activity_within_timeout_is_running(self):
        room = SimpleNamespace(
            last_activity=utcnow() - timedelta(minutes=5),
            timeout=4 * 60 * 60,  # 4 hours, default
        )
        status = classify_room(room)
        assert status.label == "Running"
        assert status.pill_class == "running"

    def test_old_activity_past_timeout_is_paused(self):
        room = SimpleNamespace(
            last_activity=utcnow() - timedelta(hours=5),
            timeout=4 * 60 * 60,
        )
        status = classify_room(room)
        assert status.label == "Paused"
        assert status.pill_class == "paused"

    def test_uses_per_room_timeout_not_a_global_threshold(self):
        # Short-timeout room: 5 min activity is past its 60 s window → Paused.
        room = SimpleNamespace(
            last_activity=utcnow() - timedelta(minutes=5),
            timeout=60,
        )
        assert classify_room(room).label == "Paused"

    def test_missing_last_activity_is_paused(self):
        room = SimpleNamespace(last_activity=None, timeout=4 * 60 * 60)
        assert classify_room(room).label == "Paused"


# ---------------------------------------------------------------------------
# get_dashboard_data — uses real DB via the conftest factories
# ---------------------------------------------------------------------------

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


class TestGetDashboardData:
    def test_empty_for_unknown_session(self, app):
        unknown_session = uuid4()
        with app.app_context():
            data = get_dashboard_data(unknown_session)
        assert data.is_empty is True
        assert data.stats.active_rooms == 0
        assert data.stats.open_lobbies == 0
        assert data.stats.saved_seeds == 0

    def test_populated_with_owned_content(
        self, app, room_factory, lobby_factory, seed_factory
    ):
        session = uuid4()
        # room_factory creates a Room AND its Seed under the given owner.
        room_factory(owner=session)
        lobby_factory(owner=session, state=0)
        seed_factory(owner=session)

        with app.app_context():
            data = get_dashboard_data(session)

        assert data.is_empty is False
        # 1 active room (default last_activity is now → within timeout → Running)
        assert data.stats.active_rooms == 1
        # 1 open lobby
        assert data.stats.open_lobbies == 1
        # 2 seeds: one from room_factory + one from seed_factory
        assert data.stats.saved_seeds == 2
        # Cards populated
        assert len(data.active_rooms) == 1
        assert len(data.my_lobbies) == 1
        assert len(data.recent_seeds) == 2

    def test_limits_items_per_section(self, app, room_factory):
        session = uuid4()
        for _ in range(10):
            room_factory(owner=session)

        with app.app_context():
            data = get_dashboard_data(session, max_per_section=3)

        assert len(data.active_rooms) == 3
        assert data.total_active_rooms == 10  # total preserved for "View all" link

    def test_closed_lobbies_excluded_from_count(self, app):
        # lobby_factory hard-codes state from with_finished_room, so create the
        # rows directly to exercise the state filter.
        from WebHostLib.models import Lobby, LOBBY_CLOSED, LOBBY_OPEN, db, commit

        session = uuid4()
        with app.app_context():
            Lobby(title="open", owner=session, state=LOBBY_OPEN, meta="{}")
            Lobby(title="closed", owner=session, state=LOBBY_CLOSED, meta="{}")
            commit()
            data = get_dashboard_data(session)

        # Only the OPEN lobby counts — CLOSED ones are stripped.
        assert data.stats.open_lobbies == 1

    def test_all_active_lobby_states_counted(self, app):
        # OPEN, GENERATING, DONE, and LOCKED are all "active" (only CLOSED is
        # excluded), and the sub-string lists them in the order the source builds.
        from WebHostLib.models import (
            Lobby, LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_LOCKED, db, commit,
        )

        session = uuid4()
        with app.app_context():
            Lobby(title="open", owner=session, state=LOBBY_OPEN, meta="{}")
            Lobby(title="generating", owner=session, state=LOBBY_GENERATING, meta="{}")
            Lobby(title="done", owner=session, state=LOBBY_DONE, meta="{}")
            Lobby(title="locked", owner=session, state=LOBBY_LOCKED, meta="{}")
            commit()
            data = get_dashboard_data(session)

        assert data.stats.open_lobbies == 4
        assert data.stats.open_lobbies_sub == "1 open · 1 generating · 1 locked · 1 done"

    def test_returns_dashboard_data_dataclass(
        self, app, room_factory, lobby_factory, seed_factory
    ):
        # Drive the *populated* path so the assertions pin the aggregation
        # output, not the empty-session early return (which trivially yields
        # default-constructed dataclasses regardless of the function body).
        session = uuid4()
        room_factory(owner=session)            # default last_activity=now → Running
        lobby_factory(owner=session, state=0)  # LOBBY_OPEN
        seed_factory(owner=session)            # 2nd seed (room_factory made one too)

        with app.app_context():
            data = get_dashboard_data(session)

        assert isinstance(data, DashboardData)
        assert isinstance(data.stats, DashboardStats)

        # Headline sub-strings are computed from the live rows.
        assert data.stats.active_rooms_sub == "1 running"
        assert data.stats.open_lobbies_sub == "1 open"
        assert data.stats.saved_seeds_sub == "0 with spoilers"

        # The active-rooms cards are (Room, RoomStatus) pairs, and the status
        # is the one classify_room produced for a fresh (Running) room.
        assert len(data.active_rooms) == 1
        room, status = data.active_rooms[0]
        assert isinstance(status, RoomStatus)
        assert status.label == "Running"
        assert status.pill_class == "running"
        assert room.owner == session

        # total_* mirror the full counts the "View all" links use.
        assert data.total_active_rooms == 1
        assert data.total_lobbies == 1
        assert data.total_seeds == 2
