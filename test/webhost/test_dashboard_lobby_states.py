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
    def test_active_states_are_open_generating_done_locked(self, app):
        """Each named active state survives the dashboard filter; CLOSED does not.

        Drives ``get_dashboard_data`` with one lobby per named state and pins
        the kept-states set behaviorally, so a bug in ``_ACTIVE_LOBBY_STATES``
        (or in the filter that consumes it) would fail this test — not just a
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
