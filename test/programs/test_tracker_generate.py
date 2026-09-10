"""TrackerCore.run_generator through the real Generate: the Players-folder scan stages one yaml."""

import logging
import os
import shutil
import tempfile
import unittest
from unittest import mock


def _write(folder: str, name: str, text: str) -> str:
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TestGenerateFromStagedYaml(unittest.TestCase):
    """The whole run: only the slot's yaml reaches Generate, so a neighbour for an uninstalled game is harmless."""

    def setUp(self):
        import sys
        from worlds.tracker import TrackerCore
        self.mod = TrackerCore
        self.folder = tempfile.mkdtemp()
        self.cache = tempfile.mkdtemp()
        for folder in (self.folder, self.cache):
            self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        argv = sys.argv.copy()
        self.addCleanup(lambda: setattr(sys, "argv", argv))

    def test_uninstalled_neighbour_yaml_does_not_break_generation(self):
        _write(self.folder, "dice.yaml", "name: Deliladice\ngame: Yacht Dice\nYacht Dice: {}\n")
        _write(self.folder, "quest.yaml", "name: Player{NUMBER}\ngame:\n  APQuest: 1\nAPQuest: {}\n")
        core = self.mod.TrackerCore(logging.getLogger("test"), False, False)
        core.set_slot_params("APQuest", 1, "Player7", 0)
        host_settings = core._set_host_settings
        core._set_host_settings = lambda: (self.folder, *host_settings()[1:])
        with mock.patch.object(self.mod, "cache_path", lambda *parts: os.path.join(self.cache, *parts)), \
                mock.patch.object(self.mod, "open_filename", side_effect=AssertionError("prompted")):
            core.run_generator(None, None)
        self.assertEqual(core.gen_error, "")
        self.assertEqual(core.launch_multiworld.players, 1)
        self.assertEqual(core.launch_multiworld.game[1], "APQuest")
        self.assertIn("Player7", core.launch_multiworld.world_name_lookup)
        self.assertEqual(os.listdir(os.path.join(self.cache, "ut_picked_yaml")), ["quest.yaml"])
