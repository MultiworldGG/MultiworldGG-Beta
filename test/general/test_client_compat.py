"""Client compatibility shims (websockets legacy attrs, kvui TUI stand-ins, legacy make_gui() resolution); add new client-compat tests here."""

import asyncio
import contextlib
import os
import subprocess
import sys
import unittest
from types import SimpleNamespace
from unittest import mock

import websockets

from websockets.asyncio.client import ClientConnection
from websockets.asyncio.connection import Connection
from websockets.protocol import State

import ClientBuilder
import CommonClient  # noqa: F401  importing it installs the compat properties

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# --------------------------------------------------------------------------- #
# World clients written against websockets 13.x (shipped MWGG) check
# server liveness via the legacy `ctx.server.socket.closed` / `.open`
# attributes (e.g. kh3's _is_ap_connected). The websockets 14+ asyncio
# Connection removed both, so CommonClient restores them as State-backed
# properties; these pin that compat surface and its legacy semantics (both
# False while opening/closing).
# --------------------------------------------------------------------------- #

class TestWebsocketsLegacyCompat(unittest.TestCase):
    def test_compat_properties_installed(self) -> None:
        for name in ("closed", "open"):
            with self.subTest(name=name):
                self.assertIsInstance(getattr(Connection, name, None), property)

    def test_client_connection_inherits_compat(self) -> None:
        # The object world clients actually touch is ctx.server.socket, a
        # ClientConnection returned by websockets.connect in server_loop.
        for name in ("closed", "open"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(ClientConnection, name))

    def test_closed_matches_legacy_semantics(self) -> None:
        # legacy: closed is True only once fully CLOSED
        for state, expected in ((State.CONNECTING, False), (State.OPEN, False),
                                (State.CLOSING, False), (State.CLOSED, True)):
            # subTest param must be a plain string: pytest-xdist ships subtest
            # reports over execnet, which cannot serialize the State enum
            with self.subTest(state=state.name):
                stub = SimpleNamespace(state=state)
                self.assertIs(Connection.closed.fget(stub), expected)

    def test_open_matches_legacy_semantics(self) -> None:
        # legacy: open is True only while fully OPEN
        for state, expected in ((State.CONNECTING, False), (State.OPEN, True),
                                (State.CLOSING, False), (State.CLOSED, False)):
            with self.subTest(state=state.name):
                stub = SimpleNamespace(state=state)
                self.assertIs(Connection.open.fget(stub), expected)

    def test_world_client_liveness_check_pattern(self) -> None:
        # The exact expression kh3 uses: bool(server and socket and not socket.closed)
        server = SimpleNamespace(socket=SimpleNamespace(state=State.OPEN))
        server.socket.closed = Connection.closed.fget(server.socket)
        self.assertTrue(bool(server and server.socket and not server.socket.closed))

    def test_deprecation_warning_once_per_call_site(self) -> None:
        # Accessing a legacy attribute surfaces a warning in the client log,
        # but only once per call site -- these checks sit in per-package loops.
        stub = SimpleNamespace(state=State.OPEN)
        with self.assertLogs("Client", level="WARNING") as logs:
            for _ in range(3):
                Connection.closed.fget(stub)  # one call site, three accesses
        records = [r for r in logs.output if "socket.closed" in r]
        self.assertEqual(len(records), 1)
        self.assertIn("Deprecated websockets API", records[0])
        # Windows drive-letter casing can differ between __file__ and the frame
        # filename inspect/traceback report, so compare case-insensitively.
        self.assertIn(__file__.lower(), records[0].lower())  # points at the offending call site


# --------------------------------------------------------------------------- #
# kvui TUI branch: world clients that route all Kivy access through kvui
# must be able to `from kvui import <kivy names>` under MWGG_FRONTEND=tui
# WITHOUT importing Kivy (importing kivy.core.window would open a rogue
# window over the Textual TUI). These run in a clean subprocess because
# (a) the parent test process has no MWGG_FRONTEND set, so importing kvui
# here would take the GUI branch and pull in kivymd, and (b) a fresh
# interpreter is the only rigorous way to assert that importing kvui did
# not drag Kivy into sys.modules.
# --------------------------------------------------------------------------- #

# Mirrors the unconditional first line of a kh3/kh2/albw-style run_gui() override.
WORLD_CLIENT_IMPORT = (
    "from kvui import (Clock, GameManager, HoverBehavior, MDBoxLayout, MDButton, "
    "MDButtonText, MDGridLayout, MDIconButton, MDLabel, MDTextField, Window, dp)"
)


def _run_tui(script: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "MWGG_FRONTEND": "tui"}
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True,
    )


class TestKvuiTuiStandins(unittest.TestCase):
    def _assert_ok(self, script: str) -> None:
        result = _run_tui(script + "\nprint('KVUI_TUI_OK')")
        self.assertEqual(
            result.returncode, 0,
            msg=f"subprocess failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )
        self.assertIn("KVUI_TUI_OK", result.stdout)

    def test_world_client_import_succeeds_without_kivy(self) -> None:
        """The import that crashes today must succeed and pull in no Kivy."""
        self._assert_ok(
            WORLD_CLIENT_IMPORT + "\n"
            "import sys; assert 'kivy' not in sys.modules, 'Kivy was imported'"
        )

    def test_dp_returns_its_argument(self) -> None:
        self._assert_ok("from kvui import dp, sp\nassert dp(30) == 30 and sp(12) == 12")

    def test_standins_support_inheritance_and_instantiation(self) -> None:
        """Stand-ins are usable as base classes (incl. multiple inheritance) and
        instantiable, with dp()/factory calls in the class body."""
        self._assert_ok(
            WORLD_CLIENT_IMPORT + "\n"
            "from kvui import StringProperty\n"
            "class Panel(MDBoxLayout): pass\n"
            "class Hoverable(HoverBehavior, MDLabel):\n"
            "    height = dp(30)\n"
            "    color = StringProperty('')\n"
            "assert Hoverable.height == 30\n"
            "assert MDBoxLayout in Panel.__mro__\n"
            "assert MDButton().anything is not None  # instance attr is inert, not error\n"
        )

    def test_game_manager_is_real_takeover_class(self) -> None:
        """GameManager must stay a real class whose async_run drives the takeover
        and then hands its declared base_title to the live app (worlds building the
        manager in run_gui skip build_for_live_app); its inert __getattr__ must not
        shadow that, and __init__ accepts extra args."""
        self._assert_ok(
            "import asyncio\n"
            "from kvui import GameManager\n"
            "class M(GameManager):\n"
            "    base_title = 'M Client'\n"
            "    def __init__(self, ctx): super().__init__(ctx, app=None)\n"
            "class LiveApp:\n"
            "    base_title = 'MultiworldGG'\n"
            "class Ctx:\n"
            "    took_over = False\n"
            "    def _can_takeover_existing_ui(self): return True\n"
            "    async def _takeover_existing_ui(self):\n"
            "        self.took_over = True\n"
            "        self.ui = LiveApp()\n"
            "ctx = Ctx()\n"
            "m = M(ctx)\n"
            "assert m.run() is None\n"
            "asyncio.run(m.async_run())\n"
            "assert ctx.took_over, 'async_run did not reach the takeover handshake'\n"
            "assert ctx.ui.base_title == 'M Client', 'manager base_title not applied to the live app'\n"
        )

    def test_tracker_hint_patch_import_and_classic_screen(self) -> None:
        """The tracker's hint-patch import line (worlds/tracker/gui.py) and the
        classic hint screen must resolve to inert stand-ins without Kivy."""
        self._assert_ok(
            "from kvui import HintLog, HintLabel, TooltipLabel\n"
            "from kvui import ClassicHintScreen\n"
            "import sys; assert 'kivy' not in sys.modules, 'Kivy was imported'"
        )

    def test_catch_all_handles_unenumerated_names_but_not_dunders(self) -> None:
        """Any non-dunder name resolves to a stable inert class; dunders still raise."""
        self._assert_ok(
            "import kvui\n"
            "from kvui import SomeFutureCustomWidget as a\n"
            "assert kvui.SomeFutureCustomWidget is a, 'stub identity not stable'\n"
            "assert isinstance(a(), a)\n"
            "raised = False\n"
            "try:\n"
            "    kvui.__not_a_real_dunder__\n"
            "except AttributeError:\n"
            "    raised = True\n"
            "assert raised, 'catch-all manufactured a dunder'\n"
        )


# --------------------------------------------------------------------------- #
# Takeover path: LegacyKvuiClientBuilder resolves the per-world UI class from
# ctx.make_gui(). Upstream world clients (e.g. SMS) return a subclass of the
# frontend App class with a build() override; that shape must reach the live
# app via build_legacy_kvui, while the bare frontend class and unrelated
# classes must not.
# --------------------------------------------------------------------------- #

class _Frontend:
    """Stand-in for the running frontend App class (mwgg_gui.app.MultiMDApp)."""

    def __init__(self):
        self.built = []

    def build_legacy_kvui(self, ctx, manager_cls):
        self.built.append(manager_cls)
        return manager_cls


class _GameManager:
    """kvui.GameManager stand-in; importing the real one takes the Kivy branch."""


class _Ctx:
    def __init__(self, manager_cls, explicit_gui: bool = False):
        self.make_gui = lambda: manager_cls
        self.explicit_built = []
        if explicit_gui:
            self.build_gui = self.explicit_built.append


def _patched_frontend() -> contextlib.ExitStack:
    """Pin the frontend class, keep the kvui import Kivy-free, force the GUI branch."""
    stack = contextlib.ExitStack()
    stack.enter_context(mock.patch.object(ClientBuilder, "resolve_frontend_class", lambda: _Frontend))
    stack.enter_context(mock.patch.dict(sys.modules, {"kvui": SimpleNamespace(GameManager=_GameManager)}))
    stack.enter_context(mock.patch.dict(os.environ, {"MWGG_FRONTEND": "gui"}))
    return stack


class TestLegacyManagerClassResolution(unittest.TestCase):
    def _resolve(self, manager_cls):
        ctx = _Ctx(manager_cls)  # the builder only weak-refs it
        builder = ClientBuilder.LegacyKvuiClientBuilder(ctx)
        with _patched_frontend():
            return builder._legacy_manager_class(_Frontend())

    def test_frontend_class_itself_is_ignored(self) -> None:
        self.assertIsNone(self._resolve(_Frontend))

    def test_frontend_subclass_is_returned(self) -> None:
        class Wrapper(_Frontend):
            def build(self):
                return None

        self.assertIs(self._resolve(Wrapper), Wrapper)

    def test_game_manager_subclass_is_returned(self) -> None:
        class Manager(_GameManager):
            pass

        self.assertIs(self._resolve(Manager), Manager)

    def test_unrelated_class_is_ignored(self) -> None:
        class Unrelated:
            pass

        self.assertIsNone(self._resolve(Unrelated))

    def test_build_hands_frontend_subclass_to_live_app(self) -> None:
        class Wrapper(_Frontend):
            def build(self):
                return None

        app = _Frontend()
        ctx = _Ctx(Wrapper)
        builder = ClientBuilder.LegacyKvuiClientBuilder(ctx, app)
        with _patched_frontend():
            result = asyncio.run(builder.build())
        self.assertEqual(app.built, [Wrapper])
        self.assertEqual(result, {"builders": ["legacy_kvui"], "manager": Wrapper})

    def test_build_runs_explicit_hook_and_frontend_subclass(self) -> None:
        """TrackerGameContext worlds (e.g. SMS) declare build_gui via the tracker
        and still return their own make_gui() subclass; both must build."""
        class Wrapper(_Frontend):
            def build(self):
                return None

        app = _Frontend()
        ctx = _Ctx(Wrapper, explicit_gui=True)
        builder = ClientBuilder.LegacyKvuiClientBuilder(ctx, app)
        with _patched_frontend():
            result = asyncio.run(builder.build())
        self.assertEqual(ctx.explicit_built, [app])
        self.assertEqual(app.built, [Wrapper])
        self.assertEqual(result, {"builders": ["build_gui", "legacy_kvui"], "manager": Wrapper})

    def test_build_explicit_hook_only_when_make_gui_is_frontend(self) -> None:
        app = _Frontend()
        ctx = _Ctx(_Frontend, explicit_gui=True)
        builder = ClientBuilder.LegacyKvuiClientBuilder(ctx, app)
        with _patched_frontend():
            result = asyncio.run(builder.build())
        self.assertEqual(ctx.explicit_built, [app])
        self.assertEqual(app.built, [])
        self.assertEqual(result, {"builders": ["build_gui"]})

    def test_failing_explicit_hook_does_not_skip_frontend_subclass(self) -> None:
        class Wrapper(_Frontend):
            def build(self):
                return None

        def broken(app):
            raise RuntimeError("tracker view failed")

        app = _Frontend()
        ctx = _Ctx(Wrapper)
        ctx.build_gui = broken
        builder = ClientBuilder.LegacyKvuiClientBuilder(ctx, app)
        with _patched_frontend(), self.assertLogs("Client", level="ERROR"):
            result = asyncio.run(builder.build())
        self.assertEqual(app.built, [Wrapper])
        self.assertEqual(result, {"builders": ["legacy_kvui"], "manager": Wrapper})


# --------------------------------------------------------------------------- #
# server_loop retries ws:// as wss:// by recursing, so two finally blocks run
# per connection attempt; only the innermost may close the connection and
# schedule the auto-reconnect. Nothing is scheduled once the exit event is
# set: asyncio.run cancels the loop during shutdown before ctx.shutdown()
# has cleared server_address.
# --------------------------------------------------------------------------- #
def _loop_ctx(exit_set: bool = False) -> SimpleNamespace:
    ctx = SimpleNamespace(
        takeover_complete=asyncio.Event(), exit_event=asyncio.Event(), server=None,
        server_address="ws://localhost:38281", username="Player1", max_size=None,
        disconnected_intentionally=False, autoreconnect_task=None, current_reconnect_delay=5,
        _messagebox_connection_loss=None, ui=None, closed=0, losses=[],
        cancel_autoreconnect=lambda: False,
    )
    ctx.takeover_complete.set()
    if exit_set:
        ctx.exit_event.set()

    async def connection_closed():
        ctx.closed += 1

    ctx.connection_closed = connection_closed
    ctx.handle_connection_loss = lambda msg: ctx.losses.append(msg)
    return ctx


class TestServerLoopReconnect(unittest.TestCase):
    def _run(self, ctx) -> list:
        attempts = []

        async def connect(address, **kwargs):
            attempts.append(address)
            if address.startswith("ws://"):
                raise websockets.InvalidMessage("not a websocket upgrade")
            raise ConnectionRefusedError()

        with mock.patch.object(CommonClient.websockets, "connect", connect):
            asyncio.run(CommonClient.server_loop(ctx, ctx.server_address))
        return attempts

    def test_wss_retry_schedules_one_reconnect(self):
        ctx = _loop_ctx()
        attempts = self._run(ctx)
        self.assertEqual(attempts, ["ws://localhost:38281", "wss://localhost:38281"])
        self.assertEqual(ctx.closed, 1)
        self.assertEqual(len(ctx.losses), 1)
        self.assertIsNotNone(ctx.autoreconnect_task)
        self.assertEqual(ctx.current_reconnect_delay, 10)

    def test_no_reconnect_after_exit_event(self):
        ctx = _loop_ctx(exit_set=True)
        self._run(ctx)
        self.assertEqual(ctx.closed, 1)
        self.assertIsNone(ctx.autoreconnect_task)


class TestUpdateMwggHints(unittest.TestCase):
    def test_update_merges_instead_of_replacing(self):
        sent = []

        async def send_msgs(msgs):
            sent.extend(msgs)

        ctx = SimpleNamespace(team=0, slot=3, send_msgs=send_msgs)
        ctx.update_mwgg_hints = lambda statuses: CommonClient.CommonContext.update_mwgg_hints(ctx, statuses)

        async def run():
            CommonClient.CommonContext.update_mwgg_hints(ctx, {"2_10": 9})
            CommonClient.CommonContext.update_mwgg_hint(ctx, 11, 2, CommonClient.MWGGUIHintStatus.HINT_GOAL)
            await asyncio.sleep(0)

        asyncio.run(run())
        self.assertEqual([msg["key"] for msg in sent], ["hints_0_3_mwgg"] * 2)
        self.assertEqual([msg["operations"] for msg in sent],
                         [[{"operation": "update", "value": {"2_10": 9}}],
                          [{"operation": "update", "value": {"2_11": 2}}]])

