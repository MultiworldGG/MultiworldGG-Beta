"""install_worlds must report worlds it could not install to its caller.

A world that fails outright used to be a log line and nothing more, so
tools/mwgg_upgrade.py exited 0 and the compose consumers booted against a venv
missing that world. `.failed` is what makes the failure visible.
"""
import unittest
from unittest import mock

import ModuleUpdate

ABSENT = "world_that_is_in_no_index_and_has_no_apworld"
TARGET = f"worlds.{ABSENT}"


class TestInstallWorldsReportsFailures(unittest.TestCase):
    def setUp(self):
        # Nothing here reaches the network -- the absent slug has no module_location to
        # install from -- but install_worlds also prunes the real venv on the way out.
        patcher = mock.patch.object(ModuleUpdate, "_prune_stale_apworld_extractions")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_uninstallable_world_is_reported(self):
        result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertIn(TARGET, result.failed)
        self.assertNotIn(TARGET, result, "a world with no apworld is not an apworld fallback")

    def test_result_still_behaves_as_the_apworld_list(self):
        # Existing callers use the return value as a plain list of apworld fallbacks.
        result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertIsInstance(result, list)
        self.assertFalse(result)
        self.assertEqual(list(result), [])

    def test_skipped_installs_still_expose_failed(self):
        with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=True):
            result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertEqual(result.failed, [])
        self.assertFalse(result)
