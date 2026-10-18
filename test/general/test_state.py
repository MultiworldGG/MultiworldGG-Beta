import unittest

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    world_relevant = True
    gen_steps = (
        "generate_early",
        "create_regions",
    )

    test_steps = (
        "create_items",
        "set_rules",
        "connect_entrances",
        "generate_basic",
        "pre_fill",
    )

    @staticmethod
    def collect_pool_and_pre_fill(multiworld) -> CollectionState:
        """
        Independent oracle for ``get_all_state`` without its sweep: build a fresh CollectionState (which collects
        precollected items in its constructor) and collect the itempool plus every world's ``get_pre_fill_items()``
        through the public ``World.collect`` API, mirroring the documented contract of ``get_all_state``.
        """
        state = CollectionState(multiworld, True)
        for item in multiworld.itempool:
            multiworld.worlds[item.player].collect(state, item)
        for player in multiworld.player_ids:
            subworld = multiworld.worlds[player]
            for item in subworld.get_pre_fill_items():
                subworld.collect(state, item)
        return state

    def test_all_state_is_available(self):
        """Ensure get_all_state collects the itempool + pre_fill items and honors allow_partial_entrances at each step."""
        for game_name, world_type in AutoWorldRegister.testable_worlds.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, self.gen_steps)
                for step in self.test_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, step)

                        # Without the sweep, get_all_state's collected progression items must match an oracle that
                        # collects only the itempool + pre_fill items. This pins the collection contract: dropping the
                        # itempool or pre_fill collection (or collecting the wrong things) would diverge here.
                        unswept = multiworld.get_all_state(allow_partial_entrances=True, perform_sweep=False)
                        self.assertIsInstance(unswept, CollectionState)
                        self.assertIs(unswept.multiworld, multiworld)
                        self.assertTrue(unswept.allow_partial_entrances,
                                        "get_all_state must propagate allow_partial_entrances to the CollectionState")
                        expected = self.collect_pool_and_pre_fill(multiworld)
                        self.assertEqual(unswept.prog_items, expected.prog_items,
                                         f"{game_name} get_all_state collected the wrong items before sweep at {step}")

                        # The real (sweeping) call only adds reachable placed items on top, so every progression item the
                        # oracle collected must still be present, and the result is a usable CollectionState.
                        swept = multiworld.get_all_state(allow_partial_entrances=True)
                        self.assertIsInstance(swept, CollectionState)
                        for player, counter in expected.prog_items.items():
                            for item_name, amount in counter.items():
                                self.assertGreaterEqual(
                                    swept.prog_items[player][item_name], amount,
                                    f"{game_name} sweep dropped collected item {item_name!r} at {step}")
