import importlib.metadata
import asyncio
import os
import types
import unittest
from contextlib import ExitStack
from unittest import mock

import NetUtils
import Utils
from CommonClient import CommonContext, process_server_cmd


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
        mwgg_index_tag=tag,
        ui=None,
    )


class TestWorldVersionPinCheck(unittest.TestCase):
    """CommonClient._check_world_version_pin reports a mismatch and never installs: the
    launcher's pre-flight installs the pinned version before the client imports the world."""

    def setUp(self):
        import CommonClient
        import ModuleUpdate
        from mwgg_igdb import GameIndex

        self._stack = ExitStack()
        # installed world resolves to slug "some_game" at 1.0.0 (mismatch vs the 1.2.3 pin)
        self._stack.enter_context(mock.patch.object(
            GameIndex, "get_module_for_game", lambda game_name, worlds=False: "some_game"))
        self._stack.enter_context(mock.patch.object(
            importlib.metadata, "distribution",
            lambda name: types.SimpleNamespace(version="1.0.0")))
        self.install = self._stack.enter_context(mock.patch.object(ModuleUpdate, "install_worlds_from_tag"))
        self._stack.enter_context(mock.patch.dict(os.environ))
        self.check = CommonClient._check_world_version_pin

    def tearDown(self):
        self._stack.close()

    def test_mismatch_warns_without_installing(self):
        rooms = {
            "managed": _pin_ctx(),
            "managed without tag": _pin_ctx(tag=None),
            "custom": _pin_ctx(custom=True),
        }
        for label, ctx in rooms.items():
            with self.subTest(label), self.assertLogs("Client", "WARNING"):
                self.check(ctx)
        self.install.assert_not_called()

    def test_matching_version_marks_world_room_pinned(self):
        import ModuleUpdate
        self.check(_pin_ctx(version=(1, 0, 0)))
        self.assertEqual(ModuleUpdate._room_pinned_worlds(), {"some_game"})

    def test_new_room_without_a_held_pin_clears_the_previous_rooms_pin(self):
        import ModuleUpdate
        rooms = {
            "mismatch not installed": _pin_ctx(),
            "custom pin": _pin_ctx(custom=True),
            "no tag": _pin_ctx(tag=None),
            "unset pin": _pin_ctx(version=(0, 0, 0)),
            "no game": _pin_ctx(game=None),
        }
        for label, ctx in rooms.items():
            with self.subTest(label):
                os.environ[ModuleUpdate._ROOM_PINNED_WORLDS_ENV] = "some_game"
                self.check(ctx)
                self.assertEqual(ModuleUpdate._room_pinned_worlds(), set())


class TestAdminCommandResultHook(unittest.IsolatedAsyncioTestCase):
    PACKET = {"cmd": "PrintJSON", "type": "AdminCommandResult", "data": [{"text": "name  game"}], "players": []}

    async def test_forwards_full_packet_to_ui_hook(self):
        ctx = CommonContext()
        printed, received = [], []
        ctx.ui = types.SimpleNamespace(print_json=printed.append, on_admin_command_result=received.append)
        await process_server_cmd(ctx, dict(self.PACKET))
        self.assertEqual(received, [self.PACKET])
        # text routing still runs alongside the hook
        self.assertEqual(printed, [self.PACKET["data"]])

    async def test_ui_without_hook_still_routes_text(self):
        ctx = CommonContext()
        printed = []
        ctx.ui = types.SimpleNamespace(print_json=printed.append)
        await process_server_cmd(ctx, dict(self.PACKET))
        self.assertEqual(printed, [self.PACKET["data"]])

    async def test_other_print_json_types_do_not_call_hook(self):
        ctx = CommonContext()
        received = []
        ctx.ui = types.SimpleNamespace(print_json=lambda data: None, on_admin_command_result=received.append)
        await process_server_cmd(ctx, {"cmd": "PrintJSON", "type": "CommandResult", "data": [{"text": "x"}]})
        self.assertEqual(received, [])


class TestShutdownKeepsSavedUsername(unittest.IsolatedAsyncioTestCase):
    """shutdown() clears the in-memory credentials without touching persistent
    storage: the username setter persists, and storing None deletes last_username."""

    async def test_shutdown_does_not_persist(self):
        ctx = CommonContext()
        ctx._username = "Player1"
        ctx._password = "hunter2"
        stored = []
        with mock.patch.object(Utils, "persistent_store", lambda *args: stored.append(args)):
            await ctx.shutdown()
        self.assertEqual(stored, [])
        self.assertIsNone(ctx._username)
        self.assertIsNone(ctx._password)


class TestConnectedPersistsSlotName(unittest.IsolatedAsyncioTestCase):
    """ROM clients log in with a ROM-derived alias in ctx.auth; the name persisted as
    last_username must be the slot name from slot_info, whose keys arrive as strings."""

    async def test_connected_stores_slot_name_not_auth(self):
        ctx = CommonContext()
        ctx.server_address = "ws://room.example:38281"
        ctx.auth = "QVAxMjM0NTY3ODkwMTIzNA=="
        packet = {
            "cmd": "Connected", "team": 0, "slot": 2,
            "players": [NetUtils.NetworkPlayer(0, 1, "Player 1", "Player 1"),
                        NetUtils.NetworkPlayer(0, 2, "Player 2", "Player 2")],
            "missing_locations": [], "checked_locations": [],
            "slot_info": {"1": NetUtils.NetworkSlot("Player 1", "__TestGame1", NetUtils.SlotType.player),
                          "2": NetUtils.NetworkSlot("Player 2", "__TestGame1", NetUtils.SlotType.player)},
        }
        stored = []
        with mock.patch.object(Utils, "persistent_store", lambda *args: stored.append(args)):
            await process_server_cmd(ctx, packet)
        self.assertEqual(ctx.username, "Player 2")
        self.assertEqual(ctx.auth, "QVAxMjM0NTY3ODkwMTIzNA==")
        self.assertIn(("client", "last_username", "Player 2"), stored)
        self.assertNotIn(("client", "last_username", ctx.auth), stored)


class TestBeforePackageHook(unittest.IsolatedAsyncioTestCase):
    """The server loop awaits before_package ahead of on_package; a failure there is logged
    and the packet is still handled."""

    async def test_runs_before_on_package(self):
        calls = []

        class Ctx(CommonContext):
            async def before_package(self, cmd, args):
                await asyncio.sleep(0)
                calls.append(("before", cmd))

            def on_package(self, cmd, args):
                calls.append(("on", cmd))

        await process_server_cmd(Ctx(), {"cmd": "Unknown"})
        self.assertEqual(calls, [("before", "Unknown"), ("on", "Unknown")])

    async def test_failure_is_logged_and_the_packet_still_handled(self):
        calls = []

        class Ctx(CommonContext):
            async def before_package(self, cmd, args):
                raise RuntimeError("boom")

            def on_package(self, cmd, args):
                calls.append(cmd)

        with self.assertLogs("Client", level="ERROR") as logs:
            await process_server_cmd(Ctx(), {"cmd": "Unknown"})
        self.assertEqual(calls, ["Unknown"])
        self.assertIn("before_package failed", logs.output[0])
