"""Webhost lobby tests (beta-authored surface); add new lobby tests here.

Covers the pure helpers in WebHostLib/api/lobby.py, the lobby page routes
(WebHostLib/lobby.py) plus the lobby state-machine API endpoints driven
through the Flask test client with anonymous session cookies, and the
backfill_short_ids script. The upstream apworld-queue suite stays in
test_lobby_apworld_queue.py.
"""
import json
from unittest import mock
from uuid import uuid4

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm.exc import StaleDataError
from werkzeug.security import generate_password_hash

from Utils import Version
from WebHostLib import lobby as lobby_module, to_url
from WebHostLib.api.lobby import (
    _extract_game_info,
    _has_name_template,
    _manual_game_segment,
    _safe_zip_name,
    _split_yaml_documents,
    _version_mismatch_direction,
)
from WebHostLib.models import (
    db, commit,
    Lobby, LobbyPlayer, LobbyMessage, LobbyYaml, Room,
    LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_CLOSED, LOBBY_LOCKED,
)
from WebHostLib.scripts.backfill_short_ids import backfill
from WebHostLib.short_id import is_well_formed

from . import TestBase


# ---------------------------------------------------------------------------
# api/lobby.py pure helpers. Each test name documents a non-obvious
# behavioral fact previously carried by an inline comment or docstring in the
# source module.
# ---------------------------------------------------------------------------

def test_safe_zip_name_sanitizes_and_defaults_to_unnamed():
    # Allowed characters (word, whitespace, dot, parens, hyphen) survive.
    assert _safe_zip_name("My_Game (v1.2)-final") == "My_Game (v1.2)-final"
    # Disallowed characters become underscores.
    assert _safe_zip_name("a/b:c*d") == "a_b_c_d"
    # Surrounding whitespace is stripped.
    assert _safe_zip_name("  spaced  ") == "spaced"
    # Empty or whitespace-only input falls back to the literal "unnamed".
    assert _safe_zip_name("") == "unnamed"
    assert _safe_zip_name("   ") == "unnamed"
    # Disallowed chars map to underscores, which are NOT stripped, so an
    # all-invalid (non-whitespace) name stays as underscores, not "unnamed".
    assert _safe_zip_name("///") == "___"


def test_has_name_template_matches_player_and_number_placeholders():
    for token in ("{player}", "{PLAYER}", "{number}", "{NUMBER}"):
        assert _has_name_template(f"Slot{token}") is True
    # No placeholder -> False, and mixed/other casings are not matched.
    assert _has_name_template("PlainName") is False
    assert _has_name_template("{Player}") is False
    assert _has_name_template("{playerX}") is False


def test_manual_game_segment_extracts_first_segment_after_prefix():
    # First underscore-delimited segment after the "Manual_" prefix.
    assert _manual_game_segment("Manual_GameName_Player") == "GameName"
    assert _manual_game_segment("Manual_GameName") == "GameName"
    # Names not starting with "Manual_" yield an empty string.
    assert _manual_game_segment("GameName") == ""
    assert _manual_game_segment("manual_lowercase") == ""


def test_extract_game_info_bare_string_becomes_exact_constraint():
    bare = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    Clique: 1.2.3\n"
    assert _extract_game_info(bare) == ("Bob", "Clique", json.dumps({"exact": "1.2.3"}))

    # A dict constraint is encoded verbatim (min/max preserved).
    as_dict = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    Clique: {min: 1.0.0, max: 2.0.0}\n"
    name, game, requires_json = _extract_game_info(as_dict)
    assert (name, game) == ("Bob", "Clique")
    assert json.loads(requires_json) == {"min": "1.0.0", "max": "2.0.0"}

    # A constraint for a *different* game than the YAML's game is ignored.
    other_game = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    NotClique: 1.2.3\n"
    assert _extract_game_info(other_game) == ("Bob", "Clique", None)

    # str input is accepted and returns the same shape as bytes.
    assert _extract_game_info("name: Bob\ngame: Clique\n") == ("Bob", "Clique", None)

    # No game present, or unparseable content, returns ('', '', None).
    assert _extract_game_info(b"name: Bob\n") == ("Bob", "", None)
    assert _extract_game_info(b": : not yaml [") == ("", "", None)


def test_version_mismatch_direction_exact_min_max_and_malformed():
    exact = lambda v: json.dumps({"exact": v})  # noqa: E731
    # exact: greater than server -> newer, less than -> older, equal -> None.
    assert _version_mismatch_direction(exact("1.2.3"), Version(1, 0, 0)) == "newer"
    assert _version_mismatch_direction(exact("1.0.0"), Version(1, 2, 3)) == "older"
    assert _version_mismatch_direction(exact("1.2.3"), Version(1, 2, 3)) is None

    # min: above server -> newer; satisfied -> None.
    assert _version_mismatch_direction(json.dumps({"min": "2.0.0"}), Version(1, 0, 0)) == "newer"
    assert _version_mismatch_direction(json.dumps({"min": "1.0.0"}), Version(1, 0, 0)) is None

    # max: below server -> older; satisfied -> None.
    assert _version_mismatch_direction(json.dumps({"max": "1.0.0"}), Version(2, 0, 0)) == "older"
    assert _version_mismatch_direction(json.dumps({"max": "3.0.0"}), Version(2, 0, 0)) is None

    # Malformed JSON yields None rather than raising.
    assert _version_mismatch_direction("not json", Version(1, 0, 0)) is None


def test_split_yaml_documents_single_unchanged_multi_indexed_from_one():
    # Single-document content is returned unchanged under its own filename.
    single = b"name: Solo\ngame: Clique\n"
    assert _split_yaml_documents("solo.yaml", single) == {"solo.yaml": single}

    # Multi-document content splits into 1-indexed {base}_N{ext} entries.
    multi = b"name: One\ngame: Clique\n---\nname: Two\ngame: Clique\n"
    out = _split_yaml_documents("party.yaml", multi)
    assert sorted(out.keys()) == ["party_1.yaml", "party_2.yaml"]
    assert b"One" in out["party_1.yaml"]
    assert b"Two" in out["party_2.yaml"]

    # Missing extension defaults to .yaml on the split entries.
    out_noext = _split_yaml_documents("party", multi)
    assert sorted(out_noext.keys()) == ["party_1.yaml", "party_2.yaml"]


# ---------------------------------------------------------------------------
# Lobby page routes + state-machine API. Assertions check both the HTTP
# status code and the resulting Lobby / LobbyPlayer / LobbyMessage database
# state, mirroring the style of test_lobby_apworld_queue.py.
# ---------------------------------------------------------------------------

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

    def _count_all_lobbies(self) -> int:
        with self.app.app_context():
            return db.session.scalar(select(func.count()).select_from(Lobby)) or 0

    def _owner_player_id(self, lobby_id) -> int:
        with self.app.app_context():
            return db.session.scalars(
                select(LobbyPlayer).where(
                    LobbyPlayer.lobby_id == lobby_id,
                    LobbyPlayer.session_id == self.owner_session,
                ).limit(1)
            ).first().id

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

    def test_join_commit_conflict_rolls_back_and_allows_retry(self) -> None:
        lobby_id = self._make_lobby(title="Race Lobby")

        def failing_commit():
            db.session.flush()
            raise StaleDataError("expected to update 1 row(s); 0 were matched")

        with mock.patch.object(lobby_module, "commit", side_effect=failing_commit):
            resp = self.viewer_client.post(
                f"/lobby/{to_url(lobby_id)}/join",
                data={"player_name": "Racer"},
            )
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f"/play/lobby/{to_url(lobby_id)}", resp.headers["Location"])
        # The rollback expunged the flushed player and system message.
        with self.app.app_context():
            self.assertIsNone(
                db.session.scalars(
                    select(LobbyPlayer).where(
                        LobbyPlayer.lobby_id == lobby_id,
                        LobbyPlayer.session_id == self.viewer_session,
                    ).limit(1)
                ).first()
            )
            self.assertEqual(
                db.session.scalar(
                    select(func.count()).select_from(LobbyMessage)
                    .where(LobbyMessage.lobby_id == lobby_id)
                ),
                0,
            )

        # The session recovered; an unmocked retry joins normally.
        retry = self.viewer_client.post(
            f"/lobby/{to_url(lobby_id)}/join",
            data={"player_name": "Racer"},
        )
        self.assertEqual(retry.status_code, 302)
        with self.app.app_context():
            joined = db.session.scalars(
                select(LobbyPlayer).where(
                    LobbyPlayer.lobby_id == lobby_id,
                    LobbyPlayer.session_id == self.viewer_session,
                ).limit(1)
            ).first()
            self.assertIsNotNone(joined)
            self.assertEqual(joined.player_name, "Racer")
            self.assertEqual(
                db.session.scalar(
                    select(func.count()).select_from(LobbyMessage)
                    .where(LobbyMessage.lobby_id == lobby_id)
                ),
                1,
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


# ---------------------------------------------------------------------------
# backfill_short_ids script (Phase 2b). The backfill must assign short_ids
# to rooms where it's NULL, skip rooms that already have one, be idempotent,
# and handle the empty case.
# ---------------------------------------------------------------------------

def _get_room_short_id(db_session, room_id):
    return db_session.get(Room, room_id).short_id


@pytest.mark.usefixtures("_wipe_rooms_after_test")
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

        unassigned = db_session.scalar(
            select(func.count()).select_from(Room).where(Room.short_id.is_(None))
        )
        assert unassigned == 0
