"""kvui TUI branch: world clients that route all Kivy access through kvui must be
able to `from kvui import <kivy names>` under MWGG_FRONTEND=tui WITHOUT importing
Kivy (importing kivy.core.window would open a rogue window over the Textual TUI).

These run in a clean subprocess because (a) the parent test process has no
MWGG_FRONTEND set, so importing kvui here would take the GUI branch and pull in
kivymd, and (b) a fresh interpreter is the only rigorous way to assert that
importing kvui did not drag Kivy into sys.modules.
"""
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        """GameManager must stay a real class whose async_run drives the takeover;
        its inert __getattr__ must not shadow that, and __init__ accepts extra args."""
        self._assert_ok(
            "import asyncio\n"
            "from kvui import GameManager\n"
            "class M(GameManager):\n"
            "    def __init__(self, ctx): super().__init__(ctx, app=None)\n"
            "class Ctx:\n"
            "    took_over = False\n"
            "    def _can_takeover_existing_ui(self): return True\n"
            "    async def _takeover_existing_ui(self): self.took_over = True\n"
            "ctx = Ctx()\n"
            "m = M(ctx)\n"
            "assert m.run() is None\n"
            "asyncio.run(m.async_run())\n"
            "assert ctx.took_over, 'async_run did not reach the takeover handshake'\n"
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


if __name__ == "__main__":
    unittest.main()
