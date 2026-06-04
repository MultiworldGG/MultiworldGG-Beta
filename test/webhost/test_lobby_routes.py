"""HTTP-level tests for the lobby page routes (WebHostLib/lobby.py) and the
lobby state-machine API endpoints (WebHostLib/api/lobby.py).

Everything is driven through the Flask test client with anonymous session
cookies (``session["_id"]``), mirroring the style of
``test_lobby_apworld_queue.py``. Assertions check both the HTTP status code
and the resulting Lobby / LobbyPlayer / LobbyMessage database state.
"""
import json
from uuid import uuid4

from sqlalchemy import select, func
from werkzeug.security import generate_password_hash

from WebHostLib import to_url
from WebHostLib.models import (
    db, commit,
    Lobby, LobbyPlayer, LobbyMessage, LobbyYaml,
    LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_CLOSED, LOBBY_LOCKED,
)

from . import TestBase


class TestLobbyRoutes(TestBase):
    def setUp(self) -> None:
        super().setUp()
        # Owner drives create/manage; viewer is an unrelated anonymous session.
        self.owner_client = self.client
        self.viewer_client = self.app.test_client()

        self.owner_session = uuid4()
        self.viewer_session = uuid4()

        with self.owner_client.session_transaction() as s:
            s["_id"] = self.owner_session
        with self.viewer_client.session_transaction() as s:
            s["_id"] = self.viewer_session

    # ------------------------------------------------------------------ helpers
    def _make_lobby(
        self,
        *,
        owner=None,
        state=LOBBY_OPEN,
        title="Direct Lobby",
        password="",
        max_players=0,
        max_yamls_per_player=3,
        allow_custom_apworlds=True,
        with_owner_player=True,
    ):
        """Insert a Lobby (and optionally its owner LobbyPlayer) directly.

        Returns the lobby id (UUID). Used to set up state the create route
        cannot produce on its own (CLOSED/DONE/GENERATING, passwords, capacity).
        """
        owner = owner if owner is not None else self.owner_session
        with self.app.app_context():
            lobby = Lobby(
                title=title,
                owner=owner,
                password_hash=generate_password_hash(password) if password else "",
                timeout_minutes=60,
                max_yamls_per_player=max_yamls_per_player,
                race=False,
                meta=json.dumps({"server_options": {"hint_cost": 4}, "generator_options": {"spoiler": 1}}),
                state=state,
                max_players=max_players,
                allow_custom_apworlds=allow_custom_apworlds,
            )
            db.session.flush()
            if with_owner_player:
                LobbyPlayer(lobby_id=lobby.id, session_id=owner, player_name="Owner")
            lobby_id = lobby.id
            commit()
        return lobby_id

    def _add_player(self, lobby_id, session_id, name, *, is_ready=False):
        with self.app.app_context():
            player = LobbyPlayer(
                lobby_id=lobby_id, session_id=session_id, player_name=name, is_ready=is_ready
            )
            db.session.flush()
            pid = player.id
            commit()
        return pid

    def _add_yaml(self, lobby_id, player_id, *, filename, game="", is_custom=False):
        with self.app.app_context():
            y = LobbyYaml(
                lobby_id=lobby_id,
                player_id=player_id,
                filename=filename,
                yaml_player_name=filename.rsplit(".", 1)[0],
                yaml_game=game,
                is_custom=is_custom,
                requires_game_version=None,
                content=b"game: " + game.encode() + b"\n",
            )
            db.session.flush()
            yid = y.id
            commit()
        return yid

    def _player_count(self, lobby_id) -> int:
        with self.app.app_context():
            return db.session.scalar(
                select(func.count()).select_from(LobbyPlayer).where(LobbyPlayer.lobby_id == lobby_id)
            ) or 0

    def _lobby_state(self, lobby_id) -> int:
        with self.app.app_context():
            return Lobby.get(id=lobby_id).state

    # ------------------------------------------------------------------ tests
    def test_create_lobby_redirects_and_persists(self) -> None:
        resp = self.owner_client.post(
            "/lobby/create",
            data={
                "title": "My Created Lobby",
                "player_name": "HostName",
                "max_yamls_per_player": "5",
                "max_players": "8",
                "timeout_minutes": "120",
                "allow_custom_apworlds": "on",
            },
        )
        self.assertEqual(resp.status_code, 302, resp.get_data(as_text=True))

        with self.app.app_context():
            lobby = db.session.scalars(
                select(Lobby).where(Lobby.title == "My Created Lobby").limit(1)
            ).first()
            self.assertIsNotNone(lobby)
            # Redirect target is the canonical view URL for the new lobby.
            self.assertTrue(
                resp.headers["Location"].endswith(f"/play/lobby/{to_url(lobby.id)}"),
                resp.headers["Location"],
            )
            self.assertEqual(lobby.owner, self.owner_session)
            self.assertEqual(lobby.state, LOBBY_OPEN)
            self.assertEqual(lobby.max_yamls_per_player, 5)
            self.assertEqual(lobby.max_players, 8)
            self.assertEqual(lobby.timeout_minutes, 120)
            self.assertTrue(lobby.allow_custom_apworlds)

            # Owner is auto-added as a player with the supplied display name.
            owner_player = db.session.scalars(
                select(LobbyPlayer).where(
                    LobbyPlayer.lobby_id == lobby.id,
                    LobbyPlayer.session_id == self.owner_session,
                ).limit(1)
            ).first()
            self.assertIsNotNone(owner_player)
            self.assertEqual(owner_player.player_name, "HostName")

            # A "created the lobby" system message is recorded.
            system_contents = db.session.scalars(
                select(LobbyMessage.content).where(
                    LobbyMessage.lobby_id == lobby.id,
                    LobbyMessage.player_id.is_(None),
                )
            ).all()
            self.assertTrue(any("HostName created the lobby." in c for c in system_contents))

    def test_create_lobby_rejects_blank_title(self) -> None:
        before = self._count_all_lobbies()
        resp = self.owner_client.post("/lobby/create", data={"title": "   "})
        # Validation failure redirects back to the create form, creates nothing.
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith("/lobby/create"))
        self.assertEqual(self._count_all_lobbies(), before)

    def _count_all_lobbies(self) -> int:
        with self.app.app_context():
            return db.session.scalar(select(func.count()).select_from(Lobby)) or 0

    def test_owner_can_view_lobby_page(self) -> None:
        lobby_id = self._make_lobby(title="Owner Viewable Lobby")
        resp = self.owner_client.get(f"/play/lobby/{to_url(lobby_id)}")
        self.assertEqual(resp.status_code, 200, resp.get_data(as_text=True))
        body = resp.get_data(as_text=True)
        # The owner's player_name renders as the host badge and the title appears.
        self.assertIn("Owner Viewable Lobby", body)
        self.assertIn("Owner", body)

    def test_view_closed_lobby_redirects_to_list(self) -> None:
        lobby_id = self._make_lobby(state=LOBBY_CLOSED, title="Gone")
        resp = self.owner_client.get(f"/play/lobby/{to_url(lobby_id)}")
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith("/play/lobbies"))

    def test_join_wrong_password_rejected_correct_password_joins(self) -> None:
        lobby_id = self._make_lobby(password="hunter2", title="PW Lobby")

        # Wrong password: redirected back, no player added for the viewer.
        bad = self.viewer_client.post(
            f"/lobby/{to_url(lobby_id)}/join",
            data={"player_name": "Intruder", "password": "wrong"},
        )
        self.assertEqual(bad.status_code, 302)
        with self.app.app_context():
            self.assertIsNone(
                db.session.scalars(
                    select(LobbyPlayer).where(
                        LobbyPlayer.lobby_id == lobby_id,
                        LobbyPlayer.session_id == self.viewer_session,
                    ).limit(1)
                ).first()
            )

        # Correct password: player row created with the chosen name.
        good = self.viewer_client.post(
            f"/lobby/{to_url(lobby_id)}/join",
            data={"player_name": "Guest", "password": "hunter2"},
        )
        self.assertEqual(good.status_code, 302)
        with self.app.app_context():
            joined = db.session.scalars(
                select(LobbyPlayer).where(
                    LobbyPlayer.lobby_id == lobby_id,
                    LobbyPlayer.session_id == self.viewer_session,
                ).limit(1)
            ).first()
            self.assertIsNotNone(joined)
            self.assertEqual(joined.player_name, "Guest")

    def test_join_rejected_when_lobby_full(self) -> None:
        # Owner player already occupies the single slot.
        lobby_id = self._make_lobby(max_players=1, title="Full Lobby")
        self.assertEqual(self._player_count(lobby_id), 1)

        resp = self.viewer_client.post(
            f"/lobby/{to_url(lobby_id)}/join",
            data={"player_name": "LateComer"},
        )
        self.assertEqual(resp.status_code, 302)
        # No new player was added; still exactly one.
        self.assertEqual(self._player_count(lobby_id), 1)
        with self.app.app_context():
            self.assertIsNone(
                db.session.scalars(
                    select(LobbyPlayer).where(
                        LobbyPlayer.lobby_id == lobby_id,
                        LobbyPlayer.session_id == self.viewer_session,
                    ).limit(1)
                ).first()
            )

    def test_lobby_list_excludes_closed_and_done(self) -> None:
        # Owned by unrelated sessions so they stay in the public list (not "my lobbies").
        open_id = self._make_lobby(owner=uuid4(), state=LOBBY_OPEN, title="OPEN_LISTED_LOBBY")
        closed_id = self._make_lobby(owner=uuid4(), state=LOBBY_CLOSED, title="CLOSED_HIDDEN_LOBBY")
        done_id = self._make_lobby(owner=uuid4(), state=LOBBY_DONE, title="DONE_HIDDEN_LOBBY")

        resp = self.viewer_client.get("/play/lobbies")
        self.assertEqual(resp.status_code, 200, resp.get_data(as_text=True))
        body = resp.get_data(as_text=True)
        self.assertIn("OPEN_LISTED_LOBBY", body)
        self.assertNotIn("CLOSED_HIDDEN_LOBBY", body)
        self.assertNotIn("DONE_HIDDEN_LOBBY", body)

    def test_generate_rejects_non_owner(self) -> None:
        lobby_id = self._make_lobby(title="Gen Auth Lobby")
        owner_pid = self._owner_player_id(lobby_id)
        self._add_yaml(lobby_id, owner_pid, filename="p1.yaml", game="Clique")

        resp = self.viewer_client.post(f"/api/lobby/{to_url(lobby_id)}/generate")
        self.assertEqual(resp.status_code, 403, resp.get_data(as_text=True))
        self.assertEqual(self._lobby_state(lobby_id), LOBBY_OPEN)

    def test_generate_blocks_custom_apworld_yaml(self) -> None:
        lobby_id = self._make_lobby(title="Gen Custom Lobby")
        owner_pid = self._owner_player_id(lobby_id)
        self._add_yaml(lobby_id, owner_pid, filename="custom.yaml", game="MadeUpGame", is_custom=True)

        resp = self.owner_client.post(f"/api/lobby/{to_url(lobby_id)}/generate")
        self.assertEqual(resp.status_code, 400, resp.get_data(as_text=True))
        self.assertIn("Download Package", resp.get_json()["error"])
        # State must not advance to GENERATING on a rejected request.
        self.assertEqual(self._lobby_state(lobby_id), LOBBY_OPEN)

    def test_generate_blocks_over_local_generation_limit(self) -> None:
        lobby_id = self._make_lobby(title="Gen Limit Lobby", max_yamls_per_player=100)
        owner_pid = self._owner_player_id(lobby_id)
        # 26 standard YAMLs exceeds LOBBY_LOCAL_GENERATION_YAML_LIMIT (25); the count
        # check runs before any roll_options validation, so plain content is fine.
        for i in range(26):
            self._add_yaml(lobby_id, owner_pid, filename=f"p{i}.yaml", game="Clique")

        resp = self.owner_client.post(f"/api/lobby/{to_url(lobby_id)}/generate")
        self.assertEqual(resp.status_code, 400, resp.get_data(as_text=True))
        self.assertIn("generated locally", resp.get_json()["error"])
        self.assertEqual(self._lobby_state(lobby_id), LOBBY_OPEN)

    def _owner_player_id(self, lobby_id) -> int:
        with self.app.app_context():
            return db.session.scalars(
                select(LobbyPlayer).where(
                    LobbyPlayer.lobby_id == lobby_id,
                    LobbyPlayer.session_id == self.owner_session,
                ).limit(1)
            ).first().id

    def test_update_settings_rejected_after_generating(self) -> None:
        lobby_id = self._make_lobby(state=LOBBY_GENERATING, title="Generating Lobby")

        resp = self.owner_client.patch(
            f"/api/lobby/{to_url(lobby_id)}/settings",
            json={"title": "Renamed While Generating"},
        )
        self.assertEqual(resp.status_code, 400, resp.get_data(as_text=True))
        self.assertIn("after generation", resp.get_json()["error"])
        # Title is unchanged in the database.
        with self.app.app_context():
            self.assertEqual(Lobby.get(id=lobby_id).title, "Generating Lobby")

    def test_update_settings_owner_changes_persist(self) -> None:
        lobby_id = self._make_lobby(title="Settings Lobby")
        resp = self.owner_client.patch(
            f"/api/lobby/{to_url(lobby_id)}/settings",
            json={"title": "New Title", "hint_cost": 42},
        )
        self.assertEqual(resp.status_code, 200, resp.get_data(as_text=True))
        with self.app.app_context():
            lobby = Lobby.get(id=lobby_id)
            self.assertEqual(lobby.title, "New Title")
            self.assertEqual(json.loads(lobby.meta)["server_options"]["hint_cost"], 42)

    def test_lock_toggles_state(self) -> None:
        lobby_id = self._make_lobby(title="Lockable Lobby")

        locked = self.owner_client.post(f"/api/lobby/{to_url(lobby_id)}/lock")
        self.assertEqual(locked.status_code, 200, locked.get_data(as_text=True))
        self.assertEqual(locked.get_json()["state"], LOBBY_LOCKED)
        self.assertEqual(self._lobby_state(lobby_id), LOBBY_LOCKED)

        unlocked = self.owner_client.post(f"/api/lobby/{to_url(lobby_id)}/lock")
        self.assertEqual(unlocked.status_code, 200, unlocked.get_data(as_text=True))
        self.assertEqual(unlocked.get_json()["state"], LOBBY_OPEN)
        self.assertEqual(self._lobby_state(lobby_id), LOBBY_OPEN)

    def test_kick_by_non_owner_forbidden(self) -> None:
        lobby_id = self._make_lobby(title="Kick Lobby")
        victim_pid = self._add_player(lobby_id, uuid4(), "Victim")

        # viewer_session is not the owner and not a co-owner.
        resp = self.viewer_client.post(f"/api/lobby/{to_url(lobby_id)}/kick/{victim_pid}")
        self.assertEqual(resp.status_code, 403, resp.get_data(as_text=True))
        # Victim is still present.
        with self.app.app_context():
            self.assertIsNotNone(LobbyPlayer.get(id=victim_pid))
