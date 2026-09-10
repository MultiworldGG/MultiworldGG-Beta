"""TrackerGameContext generation timing and the Players-folder yaml scan."""

import logging
import os
import shutil
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock


def _world_types(world_cls):
    from worlds import AutoWorld
    return mock.patch.dict(AutoWorld.AutoWorldRegister.world_types, {"FakeGame": world_cls})


def _write(folder: str, name: str, text: str) -> str:
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TestStartupGeneration(unittest.TestCase):
    def test_world_client_startup_call_never_generates(self):
        from worlds.tracker.TrackerClient import TrackerGameContext
        calls = []
        ctx = SimpleNamespace(game="FakeGame", tracker_core=SimpleNamespace(run_generator=lambda *a: calls.append(a)))
        TrackerGameContext.run_generator(ctx)
        self.assertEqual(calls, [])


class TestConnectedGeneration(unittest.TestCase):
    def _connect(self, world_cls) -> list:
        from worlds.tracker.TrackerClient import TrackerGameContext
        calls = []
        core = SimpleNamespace(
            launch_multiworld=None,
            tracker_disabled=True,
            set_slot_params=lambda *a: None,
            run_generator=lambda *a: calls.append("run_generator"),
            initalize_tracker_core=lambda *a: calls.append("initalize_tracker_core"),
        )
        ctx = SimpleNamespace(game=None, slot=3, team=0, checksums={"FakeGame": "sum"},
                              tracker_core=core, log_to_tab=lambda *a: None)
        args = {"slot": 3, "slot_info": {"3": ("me", "FakeGame")}, "slot_data": {}}
        with _world_types(world_cls):
            TrackerGameContext.on_package(ctx, "Connected", args)
        return calls

    def test_yamlless_world_skips_the_yaml_generation(self):
        class YamlLess:
            ut_can_gen_without_yaml = True

            @staticmethod
            def get_data_package_data():
                return {"checksum": "sum"}

        self.assertEqual(self._connect(YamlLess), ["initalize_tracker_core"])

    def test_world_needing_a_yaml_generates_first(self):
        class NeedsYaml:
            @staticmethod
            def get_data_package_data():
                return {"checksum": "sum"}

        self.assertEqual(self._connect(NeedsYaml), ["run_generator", "initalize_tracker_core"])


class TestPlayerYamlScan(unittest.TestCase):
    def setUp(self):
        from worlds.tracker import TrackerCore
        self.find = TrackerCore.find_player_yaml
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder, ignore_errors=True)

    def test_only_the_slots_document_is_picked_from_a_mixed_folder(self):
        _write(self.folder, "Deliladice.yaml", "name: Deliladice\ngame: Yacht Dice\n")
        _write(self.folder, "DelilahTTPR.yaml", "name: DelilahTTPR\ngame: A Link to the Past\n")
        _write(self.folder, "FoxyDelilah.yml", "name: FoxyDelilah\ngame: TUNIC\n")
        found = self.find(self.folder, "DelilahTTPR", "A Link to the Past")
        self.assertEqual(found.path.name, "DelilahTTPR.yaml")
        self.assertEqual(found.doc["game"], "A Link to the Past")
        self.assertIsNone(self.find(self.folder, "DelilahTTPR", "TUNIC"))

    def test_unreadable_yaml_does_not_abort_the_scan(self):
        _write(self.folder, "broken.yaml", "name: [unterminated\n")
        _write(self.folder, "me.yaml", "name: me\ngame: G\n")
        self.assertEqual(self.find(self.folder, "me", "G").path.name, "me.yaml")

    def test_placeholder_names_unnamed_docs_weighted_games_and_truncation_match(self):
        _write(self.folder, "bulk.yaml", "name: Player{number}\ngame:\n  G: 1\n  H: 1\nquantity: 4\n")
        _write(self.folder, "stem.yaml", "game: G\n")
        _write(self.folder, "long.yaml", "name: DelilahTTPRVeryLongName\ngame: G\n")
        self.assertEqual(self.find(self.folder, "Player3", "G").path.name, "bulk.yaml")
        self.assertEqual(self.find(self.folder, "Player3", "H").path.name, "bulk.yaml")
        self.assertEqual(self.find(self.folder, "stem", "G").path.name, "stem.yaml")
        self.assertEqual(self.find(self.folder, "DelilahTTPRVeryL", "G").path.name, "long.yaml")
        self.assertIsNone(self.find(self.folder, "Player3", "Other"))
        self.assertIsNone(self.find(self.folder, "Nobody", "G"))

    def test_multi_document_file_yields_the_matching_document(self):
        _write(self.folder, "pair.yaml", "name: first\ngame: G\n---\nname: second\ngame: G\n")
        self.assertEqual(self.find(self.folder, "second", "G").doc["name"], "second")

    def test_missing_empty_or_unset_folder_finds_nothing(self):
        _write(self.folder, "notes.txt", "")
        self.assertIsNone(self.find(self.folder, "me", "G"))
        self.assertIsNone(self.find(os.path.join(self.folder, "missing"), "me", "G"))
        self.assertIsNone(self.find("", "me", "G"))
        self.assertIsNone(self.find(None, "me", "G"))


class TestStagePlayerYaml(unittest.TestCase):
    def setUp(self):
        from worlds.tracker import TrackerCore
        self.mod = TrackerCore
        self.folder = tempfile.mkdtemp()
        self.cache = tempfile.mkdtemp()
        for folder in (self.folder, self.cache):
            self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        self.core = TrackerCore.TrackerCore(logging.getLogger("test"), False, False)
        self.core.set_slot_params("G", 1, "me", 0)
        patcher = mock.patch.object(TrackerCore, "cache_path", lambda *parts: os.path.join(self.cache, *parts))
        patcher.start()
        self.addCleanup(patcher.stop)

    def _staged(self, staged_dir: str) -> tuple[str, dict]:
        from Utils import parse_yaml
        files = os.listdir(staged_dir)
        self.assertEqual(len(files), 1)
        with open(os.path.join(staged_dir, files[0]), encoding="utf-8") as f:
            return files[0], parse_yaml(f)

    def _log_labels(self) -> list[str]:
        return [line.location_label for lines in self.core.log_lines.values() for line in lines]

    def test_matching_folder_yaml_is_staged_alone_without_a_prompt(self):
        _write(self.folder, "other.yaml", "name: other\ngame: G\n")
        _write(self.folder, "me.yaml", "name: Me{NUMBER}\ngame:\n  G: 1\n  H: 1\nquantity: 2\nG:\n  opt: 1\n")
        with mock.patch.object(self.mod, "open_filename", side_effect=AssertionError("prompted")):
            staged = self.core._stage_player_yaml(self.folder)
        name, doc = self._staged(staged)
        self.assertEqual(name, "me.yaml")
        self.assertEqual(doc, {"name": "me", "game": "G", "G": {"opt": 1}})

    def test_no_match_prompts_for_a_file_and_pins_the_slot(self):
        picked = _write(self.cache, "Someone.yaml", "name: Someone\ngame: G\nG:\n  opt: 2\n")
        with mock.patch.object(self.mod, "open_filename", return_value=picked) as prompt:
            staged = self.core._stage_player_yaml(os.path.join(self.folder, "missing"))
        prompt.assert_called_once()
        name, doc = self._staged(staged)
        self.assertEqual(name, "Someone.yaml")
        self.assertEqual(doc, {"name": "me", "game": "G", "G": {"opt": 2}})

    def test_cancelled_prompt_stops_generation(self):
        with mock.patch.object(self.mod, "open_filename", return_value=""):
            self.assertIsNone(self.core._stage_player_yaml(self.folder))
        self.assertTrue(any("No YAML selected" in label for label in self._log_labels()))

    def test_picked_multi_document_file_without_the_slot_stops_generation(self):
        picked = _write(self.cache, "pair.yaml", "name: a\ngame: G\n---\nname: b\ngame: G\n")
        with mock.patch.object(self.mod, "open_filename", return_value=picked):
            self.assertIsNone(self.core._stage_player_yaml(self.folder))
        self.assertTrue(any("No document in pair.yaml" in label for label in self._log_labels()))

    def test_restaging_replaces_the_previous_pick(self):
        _write(self.folder, "me.yaml", "name: me\ngame: G\n")
        first = self.core._stage_player_yaml(self.folder)
        self.core.set_slot_params("G", 2, "you", 0)
        _write(self.folder, "you.yaml", "name: you\ngame: G\n")
        second = self.core._stage_player_yaml(self.folder)
        self.assertEqual(first, second)
        self.assertEqual(self._staged(second)[0], "you.yaml")


if __name__ == "__main__":
    unittest.main()
