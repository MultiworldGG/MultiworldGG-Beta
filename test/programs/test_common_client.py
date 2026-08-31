import importlib.metadata
import sys
import types
import unittest
from contextlib import ExitStack
from unittest import mock

import NetUtils
from CommonClient import CommonContext


class TestCommonContext(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.ctx = CommonContext()
        self.ctx.slot = 1  # Pretend we're player 1 for this.
        self.ctx.slot_info.update({
            1: NetUtils.NetworkSlot("Player 1", "__TestGame1", NetUtils.SlotType.player),
            2: NetUtils.NetworkSlot("Player 2", "__TestGame1", NetUtils.SlotType.player),
            3: NetUtils.NetworkSlot("Player 3", "__TestGame2", NetUtils.SlotType.player),
        })
        self.ctx.consume_players_package([
            NetUtils.NetworkPlayer(1, 1, "Player 1", "Player 1"),
            NetUtils.NetworkPlayer(1, 2, "Player 2", "Player 2"),
            NetUtils.NetworkPlayer(1, 3, "Player 3", "Player 3"),
        ])
        # Using IDs outside the "safe range" for testing purposes only. If this fails unit tests, it's because
        # another world is not following the spec for allowed ID ranges.
        self.ctx.update_data_package({
            "games": {
                "__TestGame1": {
                    "location_name_to_id": {
                        "Test Location 1 - Safe": 2**54 + 1,
                        "Test Location 2 - Duplicate": 2**54 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 1 - Safe": 2**54 + 1,
                        "Test Item 2 - Duplicate": 2**54 + 2,
                    },
                },
                "__TestGame2": {
                    "location_name_to_id": {
                        "Test Location 3 - Duplicate": 2**54 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 3 - Duplicate": 2**54 + 2,
                    },
                },
            },
        })

    async def test_archipelago_datapackage_lookups_exist(self):
        assert "Archipelago" in self.ctx.item_names, "Archipelago item names entry does not exist"
        assert "Archipelago" in self.ctx.location_names, "Archipelago location names entry does not exist"

    async def test_explicit_name_lookups(self):
        # Items
        assert self.ctx.item_names["__TestGame1"][2**54+1] == "Test Item 1 - Safe"
        assert self.ctx.item_names["__TestGame1"][2**54+2] == "Test Item 2 - Duplicate"
        assert self.ctx.item_names["__TestGame1"][2**54+3] == f"Unknown item (ID: {2**54+3})"
        assert self.ctx.item_names["__TestGame1"][-1] == "Nothing"
        assert self.ctx.item_names["__TestGame2"][2**54+1] == f"Unknown item (ID: {2**54+1})"
        assert self.ctx.item_names["__TestGame2"][2**54+2] == "Test Item 3 - Duplicate"
        assert self.ctx.item_names["__TestGame2"][2**54+3] == f"Unknown item (ID: {2**54+3})"
        assert self.ctx.item_names["__TestGame2"][-1] == "Nothing"

        # Locations
        assert self.ctx.location_names["__TestGame1"][2**54+1] == "Test Location 1 - Safe"
        assert self.ctx.location_names["__TestGame1"][2**54+2] == "Test Location 2 - Duplicate"
        assert self.ctx.location_names["__TestGame1"][2**54+3] == f"Unknown location (ID: {2**54+3})"
        assert self.ctx.location_names["__TestGame1"][-1] == "Cheat Console"
        assert self.ctx.location_names["__TestGame2"][2**54+1] == f"Unknown location (ID: {2**54+1})"
        assert self.ctx.location_names["__TestGame2"][2**54+2] == "Test Location 3 - Duplicate"
        assert self.ctx.location_names["__TestGame2"][2**54+3] == f"Unknown location (ID: {2**54+3})"
        assert self.ctx.location_names["__TestGame2"][-1] == "Cheat Console"

    async def test_lookup_helper_functions(self):
        # Checking own slot.
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1) == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2) == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 3) == f"Unknown item (ID: {2 ** 54 + 3})"
        assert self.ctx.item_names.lookup_in_slot(-1) == f"Nothing"

        # Checking others' slots.
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1, 2) == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2, 2) == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1, 3) == f"Unknown item (ID: {2 ** 54 + 1})"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2, 3) == "Test Item 3 - Duplicate"

        # Checking by game.
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 1, "__TestGame1") == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 2, "__TestGame1") == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 3, "__TestGame1") == f"Unknown item (ID: {2 ** 54 + 3})"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 1, "__TestGame2") == f"Unknown item (ID: {2 ** 54 + 1})"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 2, "__TestGame2") == "Test Item 3 - Duplicate"

        # Checking with MultiworldGG ids are valid in any game package.
        assert self.ctx.item_names.lookup_in_slot(-1, 2) == "Nothing"
        assert self.ctx.item_names.lookup_in_slot(-1, 3) == "Nothing"
        assert self.ctx.item_names.lookup_in_game(-1, "__TestGame1") == "Nothing"
        assert self.ctx.item_names.lookup_in_game(-1, "__TestGame2") == "Nothing"


PIN_TAG = "sixteen-2026.05.16"


def _pin_ctx(game="Some Game", version=(1, 2, 3), custom=False, tag=PIN_TAG):
    return types.SimpleNamespace(
        game=game,
        world_versions={game: {"version": version, "custom": custom}} if game else {},
        igdb_tag=tag,
        ui=None,
    )


def _pin_settings(auto: bool):
    return lambda: types.SimpleNamespace(
        general_options=types.SimpleNamespace(auto_install_pinned_worlds=auto))


class TestWorldVersionPinDecision(unittest.TestCase):
    """CommonClient._check_world_version_pin decision logic.

    Managed worlds are resolved via the room's igdb tag: install the gen-time version from
    the tagged index snapshot (never overwriting the active mwgg_igdb) and relaunch. Custom
    worlds are report-only. Covers the one-shot loop guard, the missing-tag and failed-install
    degrade paths, and the auto_install_pinned_worlds setting.
    """

    def setUp(self):
        import CommonClient
        import ModuleUpdate
        import Utils
        import settings
        from mwgg_igdb import GameIndex

        self.from_tag_calls: list = []
        self.restarts: list = []
        self._failed: list = []  # what install_worlds_from_tag should report as failed
        self._stack = ExitStack()
        # installed world resolves to slug "some_game" at 1.0.0 (mismatch vs the 1.2.3 pin)
        self._stack.enter_context(mock.patch.object(
            GameIndex, "get_module_for_game", lambda game_name, worlds=False: "some_game"))
        self._stack.enter_context(mock.patch.object(
            importlib.metadata, "distribution",
            lambda name: types.SimpleNamespace(version="1.0.0")))
        self._stack.enter_context(mock.patch.object(settings, "get_settings", _pin_settings(True)))
        self._stack.enter_context(mock.patch.object(
            ModuleUpdate, "install_worlds_from_tag",
            lambda slugs, tag, **kw: (self.from_tag_calls.append((slugs, tag)), list(self._failed))[1]))
        self._stack.enter_context(mock.patch.object(
            Utils, "_restart_client_with_args", lambda: self.restarts.append(True)))
        self.check = CommonClient._check_world_version_pin
        self.settings_module = settings

    def tearDown(self):
        self._stack.close()

    def test_managed_mismatch_installs_from_tag_and_restarts(self):
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx())
        self.assertEqual(self.from_tag_calls, [(["some_game"], PIN_TAG)])
        self.assertEqual(self.restarts, [True])

    def test_no_tag_does_not_install_or_restart(self):
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx(tag=None))
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])

    def test_failed_install_does_not_restart(self):
        self._failed = ["some_game"]
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx())
        self.assertEqual(self.from_tag_calls, [(["some_game"], PIN_TAG)])
        self.assertEqual(self.restarts, [])  # install failed -> no relaunch

    def test_loop_guard_skips_after_relaunch(self):
        # Already relaunched once (--no-restart present) and still mismatched:
        # must NOT install or relaunch again.
        with mock.patch.object(sys, "argv", ["client", "--no-restart"]):
            self.check(_pin_ctx())
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])

    def test_disabled_setting_does_not_install(self):
        with mock.patch.object(self.settings_module, "get_settings", _pin_settings(False)), \
                mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx())
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])

    def test_custom_mismatch_is_report_only(self):
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx(custom=True))
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])

    def test_no_game_is_noop(self):
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx(game=None))
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])

    def test_matching_version_is_noop(self):
        with mock.patch.object(sys, "argv", ["client"]):
            self.check(_pin_ctx(version=(1, 0, 0)))  # == installed 1.0.0
        self.assertEqual(self.from_tag_calls, [])
        self.assertEqual(self.restarts, [])
