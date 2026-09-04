"""install_hint_log_column: the tracker's In Logic hint-table column hook.

Stubs kvui/kivy.app so this stays Kivy-free (see test_overlay_wrap.py's
tooltip sweep test for the same sys.modules-patching pattern).
"""

import re
import sys
import types
import unittest
from types import SimpleNamespace
from unittest import mock

from NetUtils import HintStatus
from worlds.tracker import gui


class _FakeColumnSorter:
    def __init__(self, key, sort_func, reverse=False):
        self.key = key
        self.sort_func = sort_func
        self.reverse = reverse


class _FakeColumnFilter:
    def __init__(self, key, str_conv_func=None):
        self.key = key
        self.str_conv_func = str_conv_func
        self.option_list = set()


class _FakeExtraColumn:
    def __init__(self, key, header_text, build_value, sorter, filter=None):
        self.key = key
        self.header_text = header_text
        self.build_value = build_value
        self.sorter = sorter
        self.filter = filter


class _FakeHintLog:
    registered = None

    @classmethod
    def register_extra_column(cls, column):
        cls.registered = column


def _fake_kvui_module() -> types.ModuleType:
    module = types.ModuleType("kvui")
    module.HintLog = _FakeHintLog
    module.ColumnSorter = _FakeColumnSorter
    module.ColumnFilter = _FakeColumnFilter
    module.ExtraColumn = _FakeExtraColumn
    module.remove_between_brackets = re.compile(r"\[.*?]")
    return module


class TestInstallHintLogColumn(unittest.TestCase):
    def setUp(self):
        gui._hint_column_installed = False
        _FakeHintLog.registered = None

    def _install(self):
        # Patches stay live for the rest of the test (enterContext), since
        # build_value's own `from kivy.app import App` runs on later calls,
        # not during registration.
        kivy_app_mod = types.ModuleType("kivy.app")
        kivy_app_mod.App = mock.Mock()
        self.enterContext(mock.patch.dict(sys.modules, {"kvui": _fake_kvui_module(), "kivy.app": kivy_app_mod}))
        self.enterContext(mock.patch("worlds.tracker.TrackerClient.get_ut_color", side_effect=lambda name: name.upper()))
        gui.install_hint_log_column()
        return kivy_app_mod.App, _FakeHintLog.registered

    def test_registers_column_metadata(self):
        _, column = self._install()
        self.assertEqual(column.key, "in_logic")
        self.assertEqual(column.header_text, "In Logic")
        self.assertEqual(column.sorter.key, "in_logic")
        self.assertEqual(column.filter.key, "in_logic")
        self.assertEqual(column.filter.option_list, {"Found", "In Logic", "Not Found"})

    def test_build_value_covers_found_in_logic_and_not_found(self):
        app, column = self._install()
        ctx = SimpleNamespace(tracker_core=SimpleNamespace(locations_available={5}))
        app.get_running_app.return_value = SimpleNamespace(ctx=ctx)

        row = {}
        column.build_value({"status": HintStatus.HINT_FOUND, "location": 5}, row)
        self.assertEqual(row["in_logic"], {"text": "[color=COLLECTED]Found[/color]", "state": "found"})

        row = {}
        column.build_value({"status": HintStatus.HINT_UNSPECIFIED, "location": 5}, row)
        self.assertEqual(row["in_logic"], {"text": "[color=IN_LOGIC]In Logic[/color]", "state": "in_logic"})

        row = {}
        column.build_value({"status": HintStatus.HINT_UNSPECIFIED, "location": 999}, row)
        self.assertEqual(row["in_logic"], {"text": "[color=OUT_OF_LOGIC]Not Found[/color]", "state": "not_found"})

    def test_sorter_orders_in_logic_before_not_found_before_found(self):
        _, column = self._install()
        rows = [{"in_logic": {"state": "found"}},
                {"in_logic": {"state": "not_found"}},
                {"in_logic": {"state": "in_logic"}}]
        rows.sort(key=column.sorter.sort_func, reverse=column.sorter.reverse)
        self.assertEqual([r["in_logic"]["state"] for r in rows], ["in_logic", "not_found", "found"])

    def test_filter_strips_markup(self):
        _, column = self._install()
        row = {"in_logic": {"text": "[color=FF0000]Not Found[/color]"}}
        self.assertEqual(column.filter.str_conv_func(row), "Not Found")

    def test_idempotent_second_call_is_a_noop(self):
        _, first = self._install()
        gui.install_hint_log_column()  # _hint_column_installed already True: returns early
        self.assertIs(_FakeHintLog.registered, first)


if __name__ == "__main__":
    unittest.main()
