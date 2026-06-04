"""Pins which lobby states the /me dashboard treats as active.

``get_dashboard_data`` keeps lobbies whose state is in
``_ACTIVE_LOBBY_STATES = (0, 1, 2, 3)`` and drops only CLOSED (-1).
"""
from __future__ import annotations

from uuid import uuid4

from WebHostLib.dashboard import _ACTIVE_LOBBY_STATES, get_dashboard_data


def _make_lobby(session, state):
    from WebHostLib.models import Lobby, db

    db.session.add(Lobby(title=f"state-{state}", owner=session, state=state, meta="{}"))


class TestDashboardLobbyStates:
    def test_active_states_are_open_generating_done_locked(self):
        from WebHostLib.models import (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
        )

        assert _ACTIVE_LOBBY_STATES == (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
        )

    def test_every_non_closed_state_counts_as_open_lobby(self, app):
        from WebHostLib.models import (
            LOBBY_OPEN,
            LOBBY_GENERATING,
            LOBBY_DONE,
            LOBBY_LOCKED,
            commit,
        )

        session = uuid4()
        with app.app_context():
            for state in (LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_LOCKED):
                _make_lobby(session, state)
            commit()
            data = get_dashboard_data(session, max_per_section=10)

        assert data.stats.open_lobbies == 4
        assert len(data.my_lobbies) == 4

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
