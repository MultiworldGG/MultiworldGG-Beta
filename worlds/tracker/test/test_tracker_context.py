"""TrackerGameContext startup generation: world clients call ctx.run_generator() before connecting."""

import unittest
from types import SimpleNamespace
from unittest import mock


def _run(game: str):
    from worlds.tracker.TrackerClient import TrackerGameContext
    calls = []
    core = SimpleNamespace(run_generator=lambda *a: calls.append(a), use_split=False)
    ctx = SimpleNamespace(game=game, tracker_core=core, use_split=True)
    TrackerGameContext.run_generator(ctx)
    return calls, ctx


class TestStartupGeneration(unittest.TestCase):
    def _world_types(self, world_cls):
        from worlds import AutoWorld
        return mock.patch.dict(AutoWorld.AutoWorldRegister.world_types, {"FakeGame": world_cls})

    def test_yamlless_world_client_skips_the_yaml_prompt(self):
        class YamlLess:
            ut_can_gen_without_yaml = True

        with self._world_types(YamlLess):
            calls, ctx = _run("FakeGame")
        self.assertEqual(calls, [])
        self.assertTrue(ctx.use_split)

    def test_world_needing_a_yaml_still_generates(self):
        class NeedsYaml:
            pass

        with self._world_types(NeedsYaml):
            calls, ctx = _run("FakeGame")
        self.assertEqual(calls, [(None, None)])
        self.assertFalse(ctx.use_split)

    def test_gameless_standalone_tracker_still_generates(self):
        calls, _ = _run("")
        self.assertEqual(calls, [(None, None)])


class TestPlayersFolderScan(unittest.TestCase):
    """run_generator takes host.yaml's Players folder before prompting for a YAML."""

    def setUp(self):
        import tempfile
        from worlds.tracker.TrackerCore import folder_has_yamls
        self.folder_has_yamls = folder_has_yamls
        self.folder = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, self.folder, ignore_errors=True)

    def test_folder_with_a_yaml_is_used(self):
        import os
        open(os.path.join(self.folder, "Player1.YML"), "w").close()
        self.assertTrue(self.folder_has_yamls(self.folder))

    def test_empty_missing_or_unset_folder_falls_through_to_the_prompt(self):
        import os
        open(os.path.join(self.folder, "notes.txt"), "w").close()
        self.assertFalse(self.folder_has_yamls(self.folder))
        self.assertFalse(self.folder_has_yamls(os.path.join(self.folder, "missing")))
        self.assertFalse(self.folder_has_yamls(""))
        self.assertFalse(self.folder_has_yamls(None))


if __name__ == "__main__":
    unittest.main()
