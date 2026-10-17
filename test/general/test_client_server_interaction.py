import asyncio
import logging
import unittest
from contextlib import ExitStack
from types import SimpleNamespace
from unittest import mock

import Utils
from CommonClient import CommonContext, process_server_cmd
from Utils import get_intended_text, get_input_text_from_response


class TestClient(unittest.TestCase):
    def test_autofill_hint_from_fuzzy_hint(self) -> None:
        tests = (
            ("item", ["item1", "item2"]),  # Multiple close matches
            ("itm", ["item1", "item21"]),  # No close match, multiple option
            ("item", ["item1"]),  # No close match, single option
            ("item", ["\"item\" 'item' (item)"]),  # Testing different special characters
        )

        for input_text, possible_answers in tests:
            item_name, usable, response = get_intended_text(input_text, possible_answers)
            self.assertFalse(usable, "This test must be updated, it seems get_fuzzy_results behavior changed")

            hint_command = get_input_text_from_response(response, "!hint")
            self.assertIsNotNone(hint_command,
                                 "The response to fuzzy hints is no longer recognized by the hint autofill")
            self.assertEqual(hint_command, f"!hint {item_name}",
                             "The hint command autofilled by the response is not correct")


def _fake_frontend(with_dialog=True):
    """Frontend stand-in recording the surfaces a refusal may touch; the TUI has no
    connect dialog, hence the switch."""
    class Frontend:
        def __init__(self):
            self.calls = []

        def show_error_dialog(self, title, message):
            self.calls.append(f"show_error_dialog:{title}")
            return object()

        def hide_loading(self):
            self.calls.append("hide_loading")

        def update_hints(self):
            pass

    if with_dialog:
        Frontend.open_connect_dialog = lambda self: self.calls.append("open_connect_dialog")
    return Frontend()


class _Client(CommonContext):
    """World-client shape: server_auth is the login step RoomInfo triggers."""
    game = "Some Game"
    items_handling = 0b111

    async def server_auth(self, password_requested: bool = False):
        await self.get_username()
        await self.send_connect()


class TestConnectionRefusedRecovery(unittest.IsolatedAsyncioTestCase):
    """InvalidGame/InvalidSlot must leave the user a way to pick the right slot: a
    frontend with a connect dialog gets it, prefilled with the refused server; a
    console-only client is re-prompted and the login is redone on the open socket."""

    def setUp(self):
        self.stored = []
        self._stack = ExitStack()
        self._stack.enter_context(mock.patch.object(
            Utils, "persistent_load", lambda: {"client": {"last_username": "OldName"}}))
        self._stack.enter_context(mock.patch.object(
            Utils, "persistent_store", lambda *args: self.stored.append(args)))
        self.addCleanup(self._stack.close)

    def _refused_ctx(self, ui):
        """A context as server_loop leaves it once the socket to the patch's server opened."""
        ctx = _Client()
        ctx.server_address = "ws://room.example:38281"
        ctx.auth = "OldName"
        ctx.ui = ui
        ctx.console_input = mock.AsyncMock(return_value="NewName")
        ctx.send_msgs = mock.AsyncMock()
        return ctx

    async def test_frontend_dialog_opens_for_refused_game_or_slot(self):
        for error in ("InvalidGame", "InvalidSlot"):
            with self.subTest(error=error):
                ui = _fake_frontend()
                ctx = self._refused_ctx(ui)
                await process_server_cmd(ctx, {"cmd": "ConnectionRefused", "errors": [error]})
                self.assertEqual(ui.calls, ["hide_loading", "open_connect_dialog"])
                ctx.console_input.assert_not_awaited()
                ctx.send_msgs.assert_not_awaited()
                self.assertIsNone(ctx.auth)
                self.assertEqual((ctx.hostname, ctx.port), ("room.example", "38281"))
                self.assertEqual(self.stored, [])
                self.assertTrue(ctx.disconnected_intentionally)

    async def test_dialog_reconnect_runs_from_refused_state(self):
        """The dialog's confirm path (set username, ctx.connect) must not be blocked."""
        import CommonClient
        ctx = self._refused_ctx(_fake_frontend())
        await process_server_cmd(ctx, {"cmd": "ConnectionRefused", "errors": ["InvalidSlot"]})
        loops = []

        async def fake_server_loop(ctx_, address=None):
            loops.append(address)

        with mock.patch.object(CommonClient, "server_loop", fake_server_loop):
            ctx.username = "NewName"
            await ctx.connect("NewName:@room.example:38281")
            await ctx.server_task
        self.assertEqual(loops, ["NewName:@room.example:38281"])
        self.assertEqual(self.stored, [("client", "last_username", "NewName")])

    async def test_console_prompt_without_dialog(self):
        """No frontend (CLI) or one without the dialog hook (TUI): the console prompt
        asks for the name and the login is redone with it."""
        for ui in (None, _fake_frontend(with_dialog=False)):
            with self.subTest(ui=type(ui).__name__ if ui else None):
                ctx = self._refused_ctx(ui)
                await process_server_cmd(ctx, {"cmd": "ConnectionRefused", "errors": ["InvalidSlot"]})
                ctx.console_input.assert_awaited_once()
                self.assertEqual(ctx.auth, "NewName")
                connect = ctx.send_msgs.await_args_list[0].args[0][0]
                self.assertEqual((connect["cmd"], connect["name"]), ("Connect", "NewName"))
                self.assertEqual(self.stored, [])
                self.assertFalse(ctx.disconnected_intentionally)


class TestDeliberateShutdownReason(unittest.IsolatedAsyncioTestCase):
    """A deliberate shutdown names its reason on the GOING_AWAY close frame; that is
    what lets clients skip auto-reconnect and tell the user why."""

    @staticmethod
    def _server_ctx():
        return SimpleNamespace(exit_event=asyncio.Event(), auto_shutdown=0.01, client_activity_timers={},
                               server=mock.Mock(), logger=logging.getLogger("test"))

    async def test_inactivity_shutdown_closes_with_reason(self):
        import MultiServer
        ctx = self._server_ctx()
        await MultiServer.auto_shutdown(ctx)
        ctx.server.close.assert_called_once_with(reason=MultiServer.INACTIVITY_SHUTDOWN_REASON)
        self.assertTrue(ctx.exit_event.is_set())

    async def test_exit_command_closes_with_reason(self):
        import MultiServer
        ctx = self._server_ctx()
        MultiServer.ServerCommandProcessor._cmd_exit(SimpleNamespace(ctx=ctx))
        ctx.server.close.assert_called_once_with(reason=MultiServer.HOST_SHUTDOWN_REASON)
        self.assertTrue(ctx.exit_event.is_set())


class _FakeVerifySocket:
    """Websocket stand-in replaying server frames to the pre-flight verifier."""

    def __init__(self, *messages):
        from NetUtils import encode
        self.frames = [encode([message]) for message in messages]

    async def send(self, data):
        pass

    async def close(self):
        pass

    async def __aiter__(self):
        for frame in self.frames:
            yield frame


class TestVerifySlotWorldPin(unittest.IsolatedAsyncioTestCase):
    """The launcher pre-flight reports the room's world version pin, so the pinned world
    installs before the client imports it."""

    ROOM_INFO = {"cmd": "RoomInfo", "world_versions": {"Some Game": {"version": [1, 2, 3], "custom": False}},
                 "mwgg_index_tag": "sixteen-2026.05.16"}

    async def _verify(self, *messages):
        import websockets
        from frontend_protocol import verify_slot

        async def _connect(*args, **kwargs):
            return _FakeVerifySocket(*messages)

        with mock.patch.object(websockets, "connect", _connect):
            return await verify_slot("localhost:38281", "Player", None, "Some Game")

    def _pin(self, installed):
        import ModuleUpdate
        return ModuleUpdate.WorldPinCheck("Some Game", "1.2.3", installed, "some_game", "sixteen-2026.05.16", False)

    async def test_mismatched_pin_rides_on_the_verdict(self):
        import ModuleUpdate
        pin = self._pin("1.0.0")
        with mock.patch.object(ModuleUpdate, "check_world_pin", return_value=pin) as check:
            result = await self._verify(self.ROOM_INFO, {"cmd": "Connected"})
        self.assertTrue(result.ok)
        self.assertEqual(result.world_pin, pin)
        check.assert_called_once_with("Some Game", {"version": [1, 2, 3], "custom": False}, "sixteen-2026.05.16")

    async def test_matching_or_unresolvable_pin_is_not_reported(self):
        import ModuleUpdate
        checks = {
            "matching": mock.Mock(return_value=self._pin("1.2.3")),
            "no pin": mock.Mock(return_value=None),
            "lookup error": mock.Mock(side_effect=RuntimeError("index unavailable")),
        }
        for label, check in checks.items():
            with self.subTest(label), mock.patch.object(ModuleUpdate, "check_world_pin", check):
                result = await self._verify(self.ROOM_INFO, {"cmd": "Connected"})
                self.assertTrue(result.ok)
                self.assertIsNone(result.world_pin)

    def test_install_pinned_world_reports_success(self):
        import ModuleUpdate
        from frontend_protocol import install_pinned_world
        outcomes = {
            "installed": (mock.Mock(return_value=[]), True),
            "failed": (mock.Mock(return_value=["some_game"]), False),
            "raised": (mock.Mock(side_effect=RuntimeError("uv missing")), False),
        }
        for label, (install, expected) in outcomes.items():
            with self.subTest(label), mock.patch.object(ModuleUpdate, "install_worlds_from_tag", install):
                self.assertEqual(install_pinned_world(self._pin("1.0.0")), expected)
                install.assert_called_once_with(["some_game"], "sixteen-2026.05.16")
