import copy
import io
import json
import os
import tempfile
import unittest
import zipfile
from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4

from pony.orm import db_session, flush

from WebHostLib import to_url
from WebHostLib.models import (Generation, Lobby, LobbyApworld, LobbyAuxiliaryApworld, LobbyMetaYaml, LobbyPlayer,
                               LobbyYaml, LOBBY_CLOSED, LOBBY_DONE, LOBBY_GENERATING, LOBBY_LOCKED, LOBBY_OPEN)
from . import TestBase


GAME = "A Link to the Past"
META = b"# Keep this comment\nmeta_description: Lobby overrides\nnull:\n  progression_balancing: 73\n"


def auxiliary_bytes():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        # Auxiliary archives do not need a game manifest, and their code must never execute on upload.
        archive.writestr(zipfile.ZipInfo("plugin/__init__.py"), "raise RuntimeError('do not import uploads')")
    return buffer.getvalue()


class TestLobbyFiles(TestBase):
    @classmethod
    def setUpClass(cls):
        from WebHostLib import app
        app.config["HOST_ADDRESS"] = "localhost"
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.host = uuid4()
        self.member = uuid4()
        self.other = self.app.test_client()
        self.outsider = self.app.test_client()
        for client, user in ((self.client, self.host), (self.other, self.member), (self.outsider, uuid4())):
            with client.session_transaction() as session:
                session["_id"] = user
        directory = tempfile.TemporaryDirectory(prefix="lobby-files-test-")
        self.addCleanup(directory.cleanup)
        config = patch.dict(self.app.config, {"LOBBY_APWORLD_PATH": directory.name,
                                             "LOBBY_AUXILIARY_APWORLD_GAMES": [GAME]})
        config.start()
        self.addCleanup(config.stop)
        with db_session:
            lobby = Lobby(title="Files", owner=self.host, allow_custom_apworlds=True,
                          meta=json.dumps({"plando_options": []}))
            host = LobbyPlayer(lobby=lobby, session_id=self.host, player_name="Host", is_ready=True)
            member = LobbyPlayer(lobby=lobby, session_id=self.member, player_name="Member", is_ready=True)
            self.original = f"name: HostSlot\ngame: {GAME}\n{GAME}:\n  progression_balancing: 12\n".encode()
            first = LobbyYaml(lobby=lobby, player=host, filename="host.yaml", yaml_player_name="HostSlot",
                              yaml_game=GAME, content=self.original)
            second = LobbyYaml(lobby=lobby, player=member, filename="member.yaml", yaml_player_name="MemberSlot",
                               yaml_game=GAME, content=self.original.replace(b"HostSlot", b"MemberSlot"))
            flush()
            self.lobby_id = lobby.id
            self.host_yaml_id, self.member_yaml_id = first.id, second.id
        self.url = f"/api/lobby/{to_url(self.lobby_id)}"

    def upload_meta(self, content=META, client=None):
        return (client or self.client).post(self.url + "/meta-yaml",
                                           data={"file": (io.BytesIO(content), "meta.yaml")})

    def upload_auxiliary(self, name="plugin.apworld", client=None, yaml_id=None, content=None):
        return (client or self.client).post(self.url + f"/auxiliary-apworld/{yaml_id or self.host_yaml_id}",
                                           data={"file": (io.BytesIO(content if content is not None else auxiliary_bytes()), name)})

    def test_meta_absent_until_uploaded_and_excluded_from_player_counts(self):
        self.assertEqual(self.client.get(self.url + "/meta-yaml").status_code, 404)
        with zipfile.ZipFile(io.BytesIO(self.client.get(self.url + "/download-package").data)) as archive:
            self.assertNotIn("Players/meta.yaml", archive.namelist())
        self.assertEqual(self.upload_meta().status_code, 200)
        status = self.other.get(self.url + "/status").get_json()
        self.assertEqual(status["total_yamls"], 2)
        self.assertEqual(status["meta_yaml"]["filename"], "meta.yaml")
        self.assertEqual(status["ready_count"], 0)
        for suffix in ("", "?view=1"):
            response = self.other.get(self.url + "/meta-yaml" + suffix)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, META)
        with zipfile.ZipFile(io.BytesIO(self.other.get(self.url + "/download-package").data)) as archive:
            self.assertEqual(archive.read("Players/meta.yaml"), META)
        self.assertEqual(self.client.delete(self.url + "/meta-yaml").status_code, 200)
        self.assertIsNone(self.client.get(self.url + "/status").get_json()["meta_yaml"])

    def test_meta_permissions_and_generation_states(self):
        self.assertEqual(self.upload_meta(client=self.other).status_code, 403)
        self.assertEqual(self.upload_meta(client=self.outsider).status_code, 403)
        self.assertEqual(self.upload_meta().status_code, 200)
        self.assertEqual(self.outsider.get(self.url + "/meta-yaml").status_code, 403)
        self.assertEqual(self.other.delete(self.url + "/meta-yaml").status_code, 403)
        with db_session:
            Lobby[self.lobby_id].state = LOBBY_LOCKED
        replacement = META.replace(b"73", b"81")
        self.assertEqual(self.upload_meta(replacement).status_code, 200)
        for state in (LOBBY_GENERATING, LOBBY_DONE):
            with db_session:
                Lobby[self.lobby_id].state = state
            self.assertEqual(self.upload_meta().status_code, 400)
            self.assertEqual(self.client.delete(self.url + "/meta-yaml").status_code, 400)
        self.assertEqual(self.other.get(self.url + "/meta-yaml").data, replacement)

    def test_invalid_meta_does_not_replace_existing_file(self):
        self.upload_meta()
        for content in (b"game: Something", b"[]", b"meta_description: x\n---\n{}", b"meta_description: x\nnull: []",
                        b"meta_description: x\nnull:\n  nope: 1", b"meta_description: x\nnull:\n  progression_balancing: {1: 0}",
                        b"!!python/object:object {}"):
            with self.subTest(content=content):
                self.assertEqual(self.upload_meta(content).status_code, 400)
        with patch("WebHostLib.api.lobby.META_YAML_MAX_SIZE", 10):
            self.assertEqual(self.upload_meta().status_code, 400)
        self.assertEqual(self.client.get(self.url + "/meta-yaml").data, META)

    def test_custom_meta_options_can_be_stored_for_local_generation(self):
        content = b"meta_description: custom\nUnlisted Game:\n  custom_option: {yes: 1, no: 1}\n"
        self.assertEqual(self.upload_meta(content).status_code, 200)
        with zipfile.ZipFile(io.BytesIO(self.client.get(self.url + "/download-package").data)) as archive:
            self.assertEqual(archive.read("Players/meta.yaml"), content)

    def test_server_generation_applies_meta_and_preserves_player_uploads(self):
        from Utils import restricted_loads
        self.upload_meta()
        response = self.client.post(self.url + "/generate")
        self.assertEqual(response.status_code, 202, response.get_json())
        with db_session:
            generation = Generation[Lobby[self.lobby_id].generation_id]
            options = restricted_loads(generation.options)
            self.assertEqual(len(options), 2)
            self.assertEqual({slot["progression_balancing"].value for slot in options.values()}, {73})
            self.assertEqual(LobbyYaml[self.host_yaml_id].content, self.original)

    def test_invalid_meta_application_does_not_queue_generation(self):
        self.upload_meta(META.replace(b"73", b"not_a_valid_value"))
        response = self.client.post(self.url + "/generate")
        self.assertEqual(response.status_code, 400, response.get_json())
        with db_session:
            self.assertEqual(Lobby[self.lobby_id].state, LOBBY_OPEN)
            self.assertEqual(Generation.select().count(), 0)

    def test_auxiliary_limit_is_shared_per_world_not_per_yaml(self):
        main_data = io.BytesIO()
        with zipfile.ZipFile(main_data, "w") as archive:
            archive.writestr("alttp/__init__.py", "")
        main_path = os.path.join(self.app.config["LOBBY_APWORLD_PATH"], "main.apworld")
        with open(main_path, "wb") as main_file:
            main_file.write(main_data.getvalue())
        with db_session:
            LobbyApworld(lobby=Lobby[self.lobby_id], yaml=LobbyYaml[self.host_yaml_id], game_name=GAME,
                         original_filename="uploaded_name.apworld", storage_path=main_path)
        # Conflicts are checked against the main world's package filename, not its uploaded name.
        self.assertEqual(self.upload_auxiliary("alttp.apworld").status_code, 409)
        for index in range(5):
            response = self.upload_auxiliary(f"plugin_{index}.apworld", client=self.other if index % 2 else self.client,
                                             yaml_id=self.member_yaml_id if index % 2 else self.host_yaml_id)
            self.assertEqual(response.status_code, 201, response.get_json())
        self.assertEqual(self.upload_auxiliary("sixth.apworld").status_code, 400)
        self.assertEqual(self.upload_auxiliary("sixth.apworld", self.other, self.member_yaml_id).status_code, 400)
        status = self.other.get(self.url + "/status").get_json()
        self.assertEqual(len(status["auxiliary_apworlds"]), 5)
        self.assertEqual(status["ready_count"], 0)
        self.assertTrue(status["force_local_generation"])
        self.assertEqual(self.client.post(self.url + "/generate").status_code, 400)
        with zipfile.ZipFile(io.BytesIO(self.client.get(self.url + "/download-package").data)) as archive:
            self.assertIn("custom_worlds/alttp.apworld", archive.namelist())
            for index in range(5):
                self.assertEqual(archive.read(f"custom_worlds/plugin_{index}.apworld"), auxiliary_bytes())

    def test_auxiliary_limit_is_independent_for_other_worlds(self):
        for index in range(5):
            self.assertEqual(self.upload_auxiliary(f"plugin_{index}.apworld").status_code, 201)
        with db_session:
            lobby = Lobby[self.lobby_id]
            other_world = LobbyYaml(lobby=lobby, player=LobbyYaml[self.host_yaml_id].player, filename="custom.yaml",
                                   yaml_game="Custom Game", is_custom=True, content=b"name: Custom\ngame: Custom Game\n")
            flush()
            yaml_id = other_world.id
        with patch.dict(self.app.config, {"LOBBY_AUXILIARY_APWORLD_GAMES": [GAME, "Custom Game"]}):
            self.assertEqual(self.upload_auxiliary("custom_plugin.apworld", yaml_id=yaml_id).status_code, 201)
        self.assertEqual(len(self.client.get(self.url + "/status").get_json()["auxiliary_apworlds"]), 6)

    def test_auxiliary_allowlist_matches_case_sensitive_world_name_prefixes(self):
        with patch.dict(self.app.config, {"LOBBY_AUXILIARY_APWORLD_GAMES": ["UZDoom"]}):
            for game, expected in (("UZDoom - Doom II", 201), ("My UZDoom World", 400), ("uzdoom - Doom II", 400)):
                with self.subTest(game=game):
                    with db_session:
                        LobbyYaml[self.host_yaml_id].yaml_game = game
                    response = self.upload_auxiliary()
                    self.assertEqual(response.status_code, expected, response.get_json())
        with patch.dict(self.app.config, {"LOBBY_AUXILIARY_APWORLD_GAMES": ["", None]}):
            self.assertEqual(self.upload_auxiliary("another.apworld").status_code, 400)

    def test_auxiliary_permissions_allowlist_and_validation(self):
        self.assertEqual(self.upload_auxiliary(client=self.outsider).status_code, 403)
        self.assertEqual(self.upload_auxiliary(client=self.other).status_code, 403)
        with patch.dict(self.app.config, {"LOBBY_AUXILIARY_APWORLD_GAMES": ["alttp"]}):
            self.assertEqual(self.upload_auxiliary().status_code, 400)
        with db_session:
            Lobby[self.lobby_id].allow_custom_apworlds = False
        self.assertEqual(self.upload_auxiliary().status_code, 400)
        with db_session:
            Lobby[self.lobby_id].allow_custom_apworlds = True
        self.assertEqual(self.upload_auxiliary("plugin.zip").status_code, 400)
        self.assertEqual(self.upload_auxiliary(content=b"not a zip").status_code, 400)
        with patch("WebHostLib.api.lobby.APWORLD_MAX_SIZE", 10):
            self.assertEqual(self.upload_auxiliary().status_code, 400)
        response = self.upload_auxiliary(client=self.other, yaml_id=self.member_yaml_id)
        self.assertEqual(response.status_code, 201, response.get_json())
        file_url = self.url + f"/auxiliary-apworld/{response.get_json()['id']}"
        self.assertEqual(self.outsider.get(file_url).status_code, 403)
        downloaded = self.client.get(file_url)
        self.assertEqual(downloaded.data, auxiliary_bytes())
        downloaded.close()
        with db_session:
            Lobby[self.lobby_id].state = LOBBY_GENERATING
        self.assertEqual(self.upload_auxiliary("another.apworld").status_code, 400)
        self.assertEqual(self.client.delete(file_url).status_code, 400)
        with db_session:
            Lobby[self.lobby_id].state = LOBBY_LOCKED
        self.assertEqual(self.client.delete(file_url).status_code, 200)

    def test_auxiliary_filename_conflicts_and_removal(self):
        response = self.upload_auxiliary()
        auxiliary_id = response.get_json()["id"]
        self.assertEqual(self.upload_auxiliary("PLUGIN.apworld").status_code, 409)
        file_url = self.url + f"/auxiliary-apworld/{auxiliary_id}"
        self.assertEqual(self.other.delete(file_url).status_code, 403)
        with db_session:
            path = LobbyAuxiliaryApworld[auxiliary_id].storage_path
        self.assertEqual(self.client.delete(file_url).status_code, 200)
        self.assertFalse(os.path.exists(path))
        self.assertEqual(self.upload_auxiliary().status_code, 201)

    def test_auxiliaries_removed_only_when_last_yaml_for_game_is_removed(self):
        response = self.upload_auxiliary()
        with db_session:
            path = LobbyAuxiliaryApworld[response.get_json()["id"]].storage_path
        self.client.delete(self.url + f"/yaml/{self.host_yaml_id}")
        self.assertTrue(os.path.exists(path))
        self.other.delete(self.url + f"/yaml/{self.member_yaml_id}")
        self.assertFalse(os.path.exists(path))
        with db_session:
            self.assertEqual(LobbyAuxiliaryApworld.select().count(), 0)

    def test_file_access_is_scoped_to_lobby(self):
        response = self.upload_auxiliary()
        with db_session:
            another = Lobby(title="Another", owner=self.host, allow_custom_apworlds=True)
            LobbyPlayer(lobby=another, session_id=self.host, player_name="Host")
            flush()
            another_url = f"/api/lobby/{to_url(another.id)}"
        self.assertEqual(self.client.get(another_url + f"/auxiliary-apworld/{response.get_json()['id']}").status_code, 404)
        self.assertEqual(self.client.post(another_url + f"/auxiliary-apworld/{self.host_yaml_id}",
                                         data={"file": (io.BytesIO(auxiliary_bytes()), "test.apworld")}).status_code, 404)

    def test_stale_lobby_cleanup_removes_meta_and_auxiliary_files(self):
        from Utils import utcnow
        from WebHostLib.autolauncher import cleanup
        self.upload_meta()
        response = self.upload_auxiliary()
        with db_session:
            path = LobbyAuxiliaryApworld[response.get_json()["id"]].storage_path
            lobby = Lobby[self.lobby_id]
            lobby.state = LOBBY_CLOSED
            lobby.last_activity = utcnow() - timedelta(hours=2)
        cleanup({"ROOM_AUTO_DELETE": 0})
        self.assertFalse(os.path.exists(path))
        with db_session:
            self.assertIsNone(Lobby.get(id=self.lobby_id))
            self.assertEqual(LobbyMetaYaml.select().count(), 0)
            self.assertEqual(LobbyAuxiliaryApworld.select().count(), 0)

    def test_participant_page_contains_compact_meta_control_only(self):
        response = self.other.get(f"/lobby/{to_url(self.lobby_id)}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="lobby-meta-yaml"', response.text)
        self.assertNotIn('id="lobby-auxiliary-apworlds"', response.text)


class TestMetaApplication(unittest.TestCase):
    def test_shared_roll_null_and_trigger_append_without_mutating_inputs(self):
        from Generate import apply_meta_weights, roll_meta_option
        from worlds import ensure_worlds_loaded
        ensure_worlds_loaded()
        trigger = {"option_name": "progression_balancing", "option_result": 99, "options": {}}
        players = {name: ({"game": GAME, GAME: {"progression_balancing": initial, "triggers": []}},)
                   for name, initial in (("one", 10), ("two", 20))}
        meta = {None: {"progression_balancing": {73: 1, 81: 1}}, GAME: {"triggers": [trigger]}}
        original_meta = copy.deepcopy(meta)
        with patch("Generate.roll_meta_option", wraps=roll_meta_option) as roll:
            apply_meta_weights(players, meta)
            self.assertEqual(roll.call_count, 2)
        self.assertEqual(players["one"][0][GAME]["progression_balancing"], players["two"][0][GAME]["progression_balancing"])
        self.assertEqual(meta, original_meta)
        self.assertEqual(players["two"][0][GAME]["triggers"], [trigger])
        players["one"][0][GAME]["triggers"].append({})
        self.assertEqual(players["two"][0][GAME]["triggers"], [trigger])
        before = copy.deepcopy(players)
        apply_meta_weights(players, {None: {"progression_balancing": {None: 1}}})
        self.assertEqual(players, before)
