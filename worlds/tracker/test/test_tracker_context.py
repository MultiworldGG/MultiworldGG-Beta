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


if __name__ == "__main__":
    unittest.main()
