"""settings_ui._ctx: which live context the tracker settings panel's runtime
toggles act on.

Stubs kivy/kivymd/mwgg_gui.settings in sys.modules so the module imports
without a window (same pattern as test_hint_log_column.py).
"""

import sys
import types
import unittest
from types import SimpleNamespace
from unittest import mock

_App = type("App", (), {"get_running_app": staticmethod(lambda: None)})

_STUBS = {
    "kivy": {}, "kivy.metrics": {"dp": lambda v: v}, "kivy.app": {"App": _App},
    "kivymd": {}, "kivymd.uix": {}, "kivymd.uix.boxlayout": {"MDBoxLayout": object},
    "kivymd.uix.button": {"MDButton": object, "MDButtonText": object},
    "kivymd.uix.label": {"MDLabel": object},
    "mwgg_gui": {}, "mwgg_gui.settings": {
        "SettingsScrollBox": object, "SettingsSection": object,
        "LabeledSwitch": object, "LabeledDropdown": object,
    },
}


def _import_settings_ui():
    saved = {name: sys.modules.get(name) for name in _STUBS}
    for name, attrs in _STUBS.items():
        module = types.ModuleType(name)
        for attr, value in attrs.items():
            setattr(module, attr, value)
        sys.modules[name] = module
    sys.modules.pop("worlds.tracker.settings_ui", None)
    try:
        from worlds.tracker import settings_ui
        return settings_ui
    finally:
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


class TestLiveContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings_ui = _import_settings_ui()

    def _ctx_with_app(self, ctx):
        app = SimpleNamespace(ctx=ctx)
        with mock.patch.object(self.settings_ui.App, "get_running_app", lambda: app, create=True):
            return self.settings_ui._ctx()

    def test_overlay_context_is_live(self):
        """A game client with the tracker overlay attached carries the map
        controller too, so Show Map and Reset Pack Path must reach it."""
        ctx = SimpleNamespace(_map_controller=object(), set_map_visible=lambda v: None)
        self.assertIs(self._ctx_with_app(ctx), ctx)

    def test_standalone_context_is_live(self):
        ctx = SimpleNamespace(_map_controller=object())
        self.assertIs(self._ctx_with_app(ctx), ctx)

    def test_launcher_init_context_is_not(self):
        self.assertIsNone(self._ctx_with_app(SimpleNamespace(slot=None)))
        self.assertIsNone(self._ctx_with_app(None))

    def test_no_running_app(self):
        with mock.patch.object(self.settings_ui.App, "get_running_app", lambda: None, create=True):
            self.assertIsNone(self.settings_ui._ctx())


if __name__ == "__main__":
    unittest.main()
