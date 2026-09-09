"""Overlay wrap glue tests (local-item scouting, refresh feed, tooltip sweep); add new overlay tests here."""

import asyncio
import sys
import types
import unittest
from types import SimpleNamespace
from unittest import mock

from NetUtils import NetworkItem
from worlds.tracker import gui, wrap


def _ctx(**kwargs) -> SimpleNamespace:
    defaults = dict(
        items_handling=0b001,
        slot=3,
        checked_locations=set(),
        locations_info={},
        items_received=[],
        missing_locations=set(),
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class TestLocalItems(unittest.TestCase):
    def test_only_own_scouted_items_merge(self):
        own = NetworkItem(101, 11, 3, 1)
        ctx = _ctx(
            checked_locations={11, 12, 13},
            locations_info={11: own, 12: NetworkItem(102, 12, 4, 0)},
        )
        self.assertEqual(wrap._local_items(ctx), [own])

    def test_empty_when_connection_receives_own_items(self):
        ctx = _ctx(
            items_handling=0b111,
            checked_locations={11},
            locations_info={11: NetworkItem(101, 11, 3, 1)},
        )
        self.assertEqual(wrap._local_items(ctx), [])
        ctx.items_handling = None
        self.assertEqual(wrap._local_items(ctx), [])


class TestScoutCheckedLocations(unittest.TestCase):
    def _run_scout(self, ctx) -> list:
        sent = []

        async def send_msgs(msgs):
            sent.append(msgs)

        ctx.send_msgs = send_msgs

        async def run():
            wrap._scout_checked_locations(ctx)
            await asyncio.sleep(0)

        asyncio.run(run())
        return sent

    def test_scouts_only_unknown_checked(self):
        ctx = _ctx(
            checked_locations={11, 13},
            locations_info={11: NetworkItem(101, 11, 3, 1)},
        )
        sent = self._run_scout(ctx)
        self.assertEqual(sent, [[{"cmd": "LocationScouts", "locations": [13], "create_as_hint": 0}]])

    def test_no_scout_when_connection_receives_own_items(self):
        ctx = _ctx(items_handling=0b111, checked_locations={11})
        self.assertEqual(self._run_scout(ctx), [])

    def test_no_scout_when_nothing_unknown(self):
        ctx = _ctx(
            checked_locations={11},
            locations_info={11: NetworkItem(101, 11, 3, 1)},
        )
        self.assertEqual(self._run_scout(ctx), [])


class TestRefreshFeed(unittest.TestCase):
    def test_refresh_feeds_received_plus_local_items(self):
        received = NetworkItem(100, -1, 3, 1)
        local = NetworkItem(103, 7, 3, 1)
        recorded = {}
        core = SimpleNamespace(
            multiworld=object(),
            player_id=1,
            set_missing_locations=lambda v: recorded.__setitem__("missing", v),
            set_items_received=lambda v: recorded.__setitem__("items", v),
            set_hints=lambda v: None,
            updateTracker=lambda: None,
        )
        ctx = _ctx(
            tracker_core=core,
            items_received=[received],
            missing_locations={5},
            checked_locations={7, 8},
            locations_info={7: local, 8: NetworkItem(104, 8, 4, 0)},
        )
        wrap._refresh(ctx, None)
        self.assertEqual(recorded["items"], [received, local])
        self.assertEqual(recorded["missing"], {5})

    def test_refresh_rebuilds_hint_table(self):
        core = SimpleNamespace(
            multiworld=object(), player_id=1,
            set_missing_locations=lambda v: None, set_items_received=lambda v: None,
            set_hints=lambda v: None, updateTracker=lambda: None,
        )
        ctx = _ctx(tracker_core=core, items_received=[], missing_locations=set(),
                   checked_locations=set(), locations_info={})
        calls = []
        app = SimpleNamespace(console_screen=None, update_hints=lambda: calls.append("hints"))
        with mock.patch("worlds.tracker.gui.clear_stray_tooltips", lambda: None):
            wrap._refresh(ctx, app)
        self.assertEqual(calls, ["hints"])


class TestWrappedOnPackage(unittest.TestCase):
    def test_room_update_scouts_and_location_info_pokes(self):
        sent = []
        pokes = []

        async def send_msgs(msgs):
            sent.append(msgs)

        ctx = _ctx(
            tracker_core=None,
            feature_registry=None,
            on_package=lambda cmd, args: None,
            send_msgs=send_msgs,
            checked_locations={21},
        )
        wrap.attach_tracker_overlay(ctx)
        ctx.tracker_overlay_poke = lambda: pokes.append(True)

        async def run():
            ctx.on_package("RoomUpdate", {})
            await asyncio.sleep(0)

        asyncio.run(run())
        self.assertEqual(sent, [[{"cmd": "LocationScouts", "locations": [21], "create_as_hint": 0}]])
        self.assertEqual(len(pokes), 1)

        ctx.on_package("LocationInfo", {})
        self.assertEqual(len(pokes), 2)


class TestRegisterTrackerPageTab(unittest.TestCase):
    def test_page_tab_wires_real_palette(self):
        from worlds.tracker import overlay_features
        from worlds.tracker.TrackerClient import get_ut_color

        ctx = _ctx(tracker_core=None, feature_registry=None, on_package=lambda cmd, args: None)
        wrap.attach_tracker_overlay(ctx)
        self.assertEqual(ctx.tracker_core.get_ut_color("in_logic"), "DD00FF")

        def fake_build(c):
            c.tracker_page = SimpleNamespace(data=[], addLine=lambda *a: None, resetData=lambda: None)
            return object()

        app = SimpleNamespace(add_client_tab=lambda name, widget: object())
        with mock.patch.object(gui, "build_tracker_view", fake_build), \
                mock.patch.object(gui, "install_app_surface", lambda c, a: None):
            overlay_features.register_tracker_page_tab(ctx, app)
        self.assertIs(ctx.tracker_core._get_ut_color, get_ut_color)


class TestClearStrayTooltips(unittest.TestCase):
    def test_sweep_keeps_live_hover_removes_orphans(self):
        class FakePlain:
            pass

        orphan = FakePlain()  # no owner back-ref (e.g. console tooltip)
        live = FakePlain()
        live._tooltip = SimpleNamespace(get_root_window=lambda: object(), hovered=True)
        detached = FakePlain()  # owner recycled out of the tree
        detached._tooltip = SimpleNamespace(get_root_window=lambda: None, hovered=True)
        unhovered = FakePlain()
        unhovered._tooltip = SimpleNamespace(
            get_root_window=lambda: object(), hovered=False, hovering=False)
        kivymd_live = FakePlain()  # kivymd HoverBehavior spells it "hovering"
        kivymd_live._tooltip = SimpleNamespace(get_root_window=lambda: object(), hovering=True)
        not_a_tooltip = object()

        removed = []
        window = SimpleNamespace(
            children=[orphan, live, detached, unhovered, kivymd_live, not_a_tooltip],
            remove_widget=removed.append,
        )
        kivy_mod = types.ModuleType("kivy.core.window")
        kivy_mod.Window = window
        kivymd_mod = types.ModuleType("kivymd.uix.tooltip")
        kivymd_mod.MDTooltipPlain = FakePlain
        with mock.patch.dict(sys.modules, {
            "kivy.core.window": kivy_mod,
            "kivymd.uix.tooltip": kivymd_mod,
        }):
            gui.clear_stray_tooltips()

        self.assertEqual(removed, [orphan, detached, unhovered])


class TestAttachGuard(unittest.TestCase):
    def test_context_owning_its_core_is_left_alone(self):
        class OwnsCore:
            owns_tracker_core = True

            def on_package(self, cmd, args):
                pass

        ctx = OwnsCore()
        wrap.attach_tracker_overlay(ctx)
        self.assertFalse(hasattr(ctx, "tracker_core"))
        self.assertIs(ctx.on_package.__func__, OwnsCore.on_package)


class TestConnectedGeneration(unittest.TestCase):
    def _connect(self, world_cls) -> list:
        calls = []
        core = SimpleNamespace(
            launch_multiworld=None,
            tracker_disabled=True,
            set_slot_params=lambda *a: None,
            run_generator=lambda *a: calls.append("run_generator"),
            initalize_tracker_core=lambda *a: calls.append("initalize_tracker_core"),
        )
        ctx = _ctx(team=0, tracker_core=core)
        args = {"slot": 3, "slot_info": {"3": ("me", "FakeGame")}, "slot_data": {}}
        from worlds import AutoWorld
        with mock.patch.dict(AutoWorld.AutoWorldRegister.world_types, {"FakeGame": world_cls}):
            wrap._handle_connected(ctx, args)
        return calls

    def test_yamlless_world_skips_the_yaml_generation(self):
        class YamlLess:
            ut_can_gen_without_yaml = True

        self.assertEqual(self._connect(YamlLess), ["initalize_tracker_core"])

    def test_world_needing_a_yaml_generates_first(self):
        class NeedsYaml:
            pass

        self.assertEqual(self._connect(NeedsYaml), ["run_generator", "initalize_tracker_core"])


if __name__ == "__main__":
    unittest.main()
