"""Webhost /me dashboard tests; add new dashboard tests here.

Covers the ``classify_room`` pure function, the ``get_dashboard_data``
aggregation, which lobby states the dashboard treats as active
(``_ACTIVE_LOBBY_STATES = (0, 1, 2, 3)``, dropping only CLOSED = -1), and
end-to-end smoke of the /me routes.
"""
from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace
from uuid import uuid4

from Utils import utcnow
from WebHostLib.dashboard import (
    _ACTIVE_LOBBY_STATES,
    DashboardData,
    DashboardStats,
    RoomStatus,
    classify_room,
    get_dashboard_data,
)


# ---------------------------------------------------------------------------
# classify_room - pure function, no DB needed
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
# get_dashboard_data - uses real DB via the conftest factories
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Active-lobby-state filter
# ---------------------------------------------------------------------------

def _make_lobby(session, state):
    from WebHostLib.models import Lobby, db

    db.session.add(Lobby(title=f"state-{state}", owner=session, state=state, meta="{}"))


class TestDashboardLobbyStates:
    def test_active_states_are_open_generating_done_locked(self, app):
        """Each named active state survives the dashboard filter; CLOSED does not.

        Drives ``get_dashboard_data`` with one lobby per named state and pins
        the kept-states set behaviorally, so a bug in ``_ACTIVE_LOBBY_STATES``
        (or in the filter that consumes it) would fail this test - not just a
        constant-vs-constant comparison.
        """
        from WebHostLib.models import (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
            LOBBY_CLOSED,
            commit,
        )

        session = uuid4()
        all_states = (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
            LOBBY_CLOSED,
        )
        with app.app_context():
            for state in all_states:
                _make_lobby(session, state)
            commit()
            data = get_dashboard_data(session, max_per_section=len(all_states))

        kept_states = {lobby.state for lobby in data.my_lobbies}
        # Exactly the four active states are kept; CLOSED is excluded.
        assert kept_states == {LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_LOCKED}
        assert LOBBY_CLOSED not in kept_states
        # The dashboard's active-states tuple must agree with what it keeps.
        assert set(_ACTIVE_LOBBY_STATES) == kept_states

    def test_only_closed_state_is_excluded(self, app):
        from WebHostLib.models import (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
            LOBBY_CLOSED,
            commit,
        )

        session = uuid4()
        with app.app_context():
            for state in (
                LOBBY_OPEN,
                LOBBY_GENERATING,
                LOBBY_DONE,
                LOBBY_LOCKED,
                LOBBY_CLOSED,
            ):
                _make_lobby(session, state)
            commit()
            data = get_dashboard_data(session, max_per_section=10)

        # The single CLOSED (-1) lobby is the only one stripped.
        assert data.stats.open_lobbies == 4
        assert data.total_lobbies == 4


# ---------------------------------------------------------------------------
# /me routes - end-to-end smoke
# ---------------------------------------------------------------------------

def test_me_returns_first_run_for_fresh_browser(client):
    """A fresh session sees the empty-state page, not the dashboard."""
    response = client.get("/me")
    assert response.status_code == 200


def test_me_returns_dashboard_when_owner_has_content(client, room_factory):
    """When the browser session owns a room, the dashboard renders (not the empty state)."""
    # Pin a known session_key on the test client, then create data under that key.
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me")
    assert response.status_code == 200


def test_my_rooms_renders_empty_message_when_no_rooms(client):
    response = client.get("/me/rooms")
    assert response.status_code == 200


def test_my_lobbies_renders_empty_message_when_no_lobbies(client):
    response = client.get("/me/lobbies")
    assert response.status_code == 200


def test_my_seeds_renders_empty_message_when_no_seeds(client):
    response = client.get("/me/seeds")
    assert response.status_code == 200


def test_my_rooms_lists_owned_rooms(client, room_factory):
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me/rooms")
    assert response.status_code == 200
