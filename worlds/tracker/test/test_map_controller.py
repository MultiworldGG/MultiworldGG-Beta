"""Kivy-free tests for UTMapController (worlds/tracker/map_controller.py).

Covers the overlay's map-activation glue: tracker_world detection, command
registration, notify-key subscription, and the SetReply/Retrieved reload
path. Widget construction (build_map_view et al) is mocked out since it
requires a live Kivy app; see gui.py for that surface.
"""

import sys
import unittest
from types import SimpleNamespace
from unittest import mock

from worlds.tracker.map_controller import UTMapController, cmd_load_map, cmd_list_maps


class _Processor:
    """Fresh per-test commands dict; real command processor subclasses get
    their own dict via CommandMeta, this mirrors that isolation."""
    commands: dict = {}


def _ctx(**kwargs) -> SimpleNamespace:
    defaults = dict(slot=1, team=0, game="TestGame", ui=None,
                     set_notify=lambda *keys: None,
                     command_processor=type("Processor", (_Processor,), {"commands": {}}))
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _core(player_id=1, current_world=None):
    return SimpleNamespace(player_id=player_id, get_current_world=lambda: current_world)


class TestBuildTrackerWorld(unittest.TestCase):
    def test_no_tracker_world_attr_anywhere(self):
        ctx = _ctx()
        controller = UTMapController(ctx, _core(current_world=SimpleNamespace()))

        class ConnectedCls:
            pass

        controller.build_tracker_world(ConnectedCls)
        self.assertIsNone(ctx.tracker_world)

    def test_tracker_world_from_connected_class(self):
        ctx = _ctx()
        controller = UTMapController(ctx, _core(current_world=SimpleNamespace()))

        class ConnectedCls:
            tracker_world = {"map_page_folder": "maps", "location_setting_key": "icon"}

        controller.build_tracker_world(ConnectedCls)
        self.assertIsNotNone(ctx.tracker_world)
        self.assertEqual(ctx.tracker_world.map_page_folder, "maps")

    def test_tracker_world_from_current_world_instance(self):
        current_world = SimpleNamespace(tracker_world={"map_page_folder": "maps"})
        ctx = _ctx()
        controller = UTMapController(ctx, _core(current_world=current_world))

        class ConnectedCls:
            pass

        controller.build_tracker_world(ConnectedCls)
        self.assertIsNotNone(ctx.tracker_world)


class TestInit(unittest.TestCase):
    def test_auto_tab_defaults_on_for_plain_contexts(self):
        ctx = _ctx()
        UTMapController(ctx, _core())
        self.assertTrue(ctx.auto_tab)

    def test_auto_tab_left_alone_when_context_defines_it(self):
        ctx = _ctx(auto_tab=False)
        UTMapController(ctx, _core())
        self.assertFalse(ctx.auto_tab)


class TestSetMapVisible(unittest.TestCase):
    def _live(self, ctx):
        tabs = []
        app = SimpleNamespace(add_client_tab=lambda name, content: tabs.append((name, content)) or "handle",
                              remove_client_tab=lambda handle: tabs.append(("removed", handle)))
        stub = SimpleNamespace(MDApp=SimpleNamespace(get_running_app=lambda: app))
        return tabs, mock.patch.dict(sys.modules, {"kivymd": SimpleNamespace(app=stub), "kivymd.app": stub})

    def test_show_reuses_prebuilt_widget(self):
        ctx = _ctx()
        controller = UTMapController(ctx, _core())
        prebuilt = object()
        ctx._map_content = ctx.map_page = prebuilt
        tabs, patcher = self._live(ctx)
        with patcher, mock.patch("worlds.tracker.gui.build_map_view", side_effect=AssertionError("rebuilt")):
            controller.set_map_visible(True)
        self.assertEqual(tabs, [("map", prebuilt)])
        self.assertIs(ctx.map_page, prebuilt)
        self.assertTrue(ctx._show_map)

    def test_hide_drops_widget_so_next_show_rebuilds(self):
        ctx = _ctx()
        controller = UTMapController(ctx, _core())
        ctx._map_content = ctx.map_page = object()
        ctx.map_page_coords_func = lambda *args: None
        tabs, patcher = self._live(ctx)
        with patcher:
            controller.set_map_visible(True)
            controller.set_map_visible(False)
        self.assertEqual(tabs[-1], ("removed", "handle"))
        self.assertIsNone(ctx.map_page)
        self.assertIsNone(ctx._map_content)
        self.assertEqual(ctx.map_page_coords_func(), ({}, {}, {}))


class TestActivate(unittest.TestCase):
    def _stub_controller(self, ctx, core):
        controller = UTMapController(ctx, core)
        controller.prebuild_widget = lambda: None
        controller.load_pack = lambda: None
        controller.set_map_visible = lambda visible: None
        return controller

    def test_noop_without_app(self):
        ctx = _ctx()
        controller = self._stub_controller(ctx, _core())
        controller.activate(None)
        self.assertFalse(ctx._map_activated)

    def test_noop_without_tracker_world(self):
        ctx = _ctx()
        controller = self._stub_controller(ctx, _core())
        controller.activate(object())
        self.assertFalse(ctx._map_activated)

    def test_registers_commands_and_notify_keys(self):
        notified = []
        ctx = _ctx(set_notify=lambda *keys: notified.extend(keys))
        controller = self._stub_controller(ctx, _core())
        ctx.tracker_world = SimpleNamespace(
            map_page_index=lambda _: 0,
            map_page_setting_key=None,
            location_setting_key="icon_key",
        )

        controller.activate(object())

        self.assertIn("1_0_UT_MAP", notified)
        self.assertIn("icon_key", notified)
        self.assertIs(ctx.command_processor.commands["load_map"], cmd_load_map)
        self.assertIs(ctx.command_processor.commands["list_maps"], cmd_list_maps)
        self.assertTrue(ctx._map_activated)

    def test_idempotent(self):
        calls = {"load_pack": 0}
        ctx = _ctx()
        controller = self._stub_controller(ctx, _core())
        controller.load_pack = lambda: calls.__setitem__("load_pack", calls["load_pack"] + 1)
        ctx.tracker_world = SimpleNamespace(
            map_page_index=lambda _: 0, map_page_setting_key=None, location_setting_key=None)

        controller.activate(object())
        controller.activate(object())

        self.assertEqual(calls["load_pack"], 1)

    def test_load_pack_failure_skips_tab_but_keeps_commands(self):
        """Mirrors TrackerGameContext.on_package: commands still register
        even if load_pack invalidates tracker_world (e.g. bad external pack)."""
        ctx = _ctx()
        controller = self._stub_controller(ctx, _core())
        ctx.tracker_world = SimpleNamespace(
            map_page_index=lambda _: 0, map_page_setting_key=None, location_setting_key=None)
        shown = []
        controller.set_map_visible = lambda visible: shown.append(visible)

        def failing_load_pack():
            ctx.tracker_world = None
        controller.load_pack = failing_load_pack

        controller.activate(object())

        self.assertEqual(shown, [])
        self.assertIn("load_map", ctx.command_processor.commands)


class TestHandleStoredData(unittest.TestCase):
    def _ready_ctx(self):
        ctx = _ctx(ui=object())
        controller = UTMapController(ctx, _core())
        ctx.tracker_world = SimpleNamespace(
            map_page_setting_key="mapkey", location_setting_key="iconkey")
        return ctx, controller

    def test_map_key_reloads_and_refreshes(self):
        ctx, controller = self._ready_ctx()
        calls = []
        controller.load_map = lambda mid: calls.append(("load_map", mid))
        ctx.updateTracker = lambda: calls.append(("refresh",))

        controller.handle_stored_data({"key": "mapkey"})

        self.assertEqual(calls, [("load_map", None), ("refresh",)])

    def test_icon_key_updates_icons_only(self):
        ctx, controller = self._ready_ctx()
        calls = []
        controller.load_map = lambda mid: calls.append("load_map")
        controller.update_location_icon_coords = lambda: calls.append("icons")

        controller.handle_stored_data({"key": "iconkey"})

        self.assertEqual(calls, ["icons"])

    def test_bulk_keys_icon_only(self):
        ctx, controller = self._ready_ctx()
        calls = []
        controller.update_location_icon_coords = lambda: calls.append("icons")

        controller.handle_stored_data({"keys": {"iconkey": "v", "other": "v"}})

        self.assertEqual(calls, ["icons"])

    def test_noop_without_ui(self):
        ctx, controller = self._ready_ctx()
        ctx.ui = None
        calls = []
        controller.load_map = lambda mid: calls.append("load_map")

        controller.handle_stored_data({"key": "mapkey"})

        self.assertEqual(calls, [])

    def test_noop_without_tracker_world(self):
        ctx, controller = self._ready_ctx()
        ctx.tracker_world = None
        calls = []
        controller.load_map = lambda mid: calls.append("load_map")

        controller.handle_stored_data({"key": "mapkey"})

        self.assertEqual(calls, [])


class TestDisconnect(unittest.TestCase):
    def test_resets_map_state_and_commands(self):
        ctx = _ctx(ui=object())
        controller = UTMapController(ctx, _core())
        controller.set_map_visible = lambda visible: None
        ctx.tracker_world = SimpleNamespace()
        ctx.command_processor.commands["load_map"] = cmd_load_map
        ctx.command_processor.commands["list_maps"] = cmd_list_maps
        ctx.coord_dict = {1: []}
        ctx._map_activated = True

        controller.disconnect()

        self.assertIsNone(ctx.tracker_world)
        self.assertNotIn("load_map", ctx.command_processor.commands)
        self.assertNotIn("list_maps", ctx.command_processor.commands)
        self.assertFalse(ctx._map_activated)

    def test_safe_without_prior_activation(self):
        ctx = _ctx()
        controller = UTMapController(ctx, _core())
        controller.disconnect()  # should not raise
        self.assertIsNone(ctx.tracker_world)


class TestLoadPack(unittest.TestCase):
    def test_populates_maps_locs_layouts_from_apworld_package(self):
        current_world = SimpleNamespace(settings=None)
        ctx = _ctx(ui=None)  # ui=None -> load_map's tail call bails immediately
        controller = UTMapController(ctx, _core(current_world=current_world))
        ctx.tracker_world = SimpleNamespace(
            external_pack_key="",
            map_page_folder="maps",
            map_page_maps=["map.json"],
            map_page_locations=["locations.json"],
            map_page_layouts=["layout.json"],
            map_page_groups=[("Region", ["map1"])],
        )

        fake_data = {
            "/maps/map.json": [{"name": "map1", "img": "map1.png"}],
            "/maps/locations.json": [],
            "/maps/layout.json": {},
        }
        with mock.patch("worlds.tracker.map_controller.load_json",
                         side_effect=lambda pack, path: fake_data[path]):
            controller.load_pack()

        self.assertEqual(ctx.maps, [{"name": "map1", "img": "map1.png"}])
        self.assertEqual(ctx.locs, [])
        self.assertEqual(ctx.layouts, [{}])
        self.assertEqual(ctx.map_groups, [("Region", ["map1"])])


if __name__ == "__main__":
    unittest.main()
