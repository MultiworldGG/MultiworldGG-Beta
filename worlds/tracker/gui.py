"""UI surface for the Universal Tracker.

Widgets and helpers live here so that TrackerClient.py is logic-only. Everything
in this module assumes a live Kivy frontend (MultiMDApp). The module-level
imports of kivy/kvui are deferred to first call so that --nogui clients never
pull Kivy in.
"""
import logging
import os
import traceback
from collections import Counter, defaultdict

logger = logging.getLogger("Client")


_hint_column_installed = False


def clear_stray_tooltips() -> None:
    """Remove orphaned hover tooltips from Window.

    Tooltips are parented to Window, so they outlive their owner row when a
    repaint recycles it (a detached row never dispatches the on_leave that
    removes its tooltip). A tooltip whose owner is still attached and hovered
    is kept; everything else plain-tooltip-shaped is swept. Safe without kivy.
    """
    try:
        from kivy.core.window import Window
        from kivymd.uix.tooltip import MDTooltipPlain
    except Exception:
        return
    if Window is None:
        return
    for child in tuple(Window.children):
        if not isinstance(child, MDTooltipPlain):
            continue
        # kivymd convention: the tip and its host cross-reference via _tooltip.
        owner = getattr(child, "_tooltip", None)
        if owner is not None and owner.get_root_window() is not None and (
                getattr(owner, "hovered", False) or getattr(owner, "hovering", False)):
            continue
        Window.remove_widget(child)


def install_hint_log_column():
    """Register the tracker's "In Logic" column on kvui.HintLog once.

    Uses HintLog.register_extra_column (the mixin table's data-driven hook)
    instead of patching on_kv_post, so the column sorts/filters like any
    other. Must run before the hint screen is built. Safe to call repeatedly.
    """
    global _hint_column_installed
    if _hint_column_installed:
        return

    from kvui import HintLog, ColumnSorter, ColumnFilter, ExtraColumn, remove_between_brackets
    from NetUtils import HintStatus
    from worlds.tracker.TrackerClient import get_ut_color

    def build_in_logic(hint: dict, row: dict) -> None:
        from kivy.app import App
        ctx = App.get_running_app().ctx
        if hint["status"] == HintStatus.HINT_FOUND:
            state, color_key, text = "found", "collected", "Found"
        elif hint["location"] in ctx.tracker_core.locations_available:
            state, color_key, text = "in_logic", "in_logic", "In Logic"
        else:
            state, color_key, text = "not_found", "out_of_logic", "Not Found"
        row["in_logic"] = {"text": f"[color={get_ut_color(color_key)}]{text}[/color]", "state": state}

    weights = {"in_logic": 0, "not_found": 1, "found": 2}
    sorter = ColumnSorter("in_logic", lambda row: weights[row["in_logic"]["state"]])
    filt = ColumnFilter("in_logic", lambda row: remove_between_brackets.sub("", row["in_logic"]["text"]))
    filt.option_list.update(("Found", "In Logic", "Not Found"))

    HintLog.register_extra_column(ExtraColumn(
        key="in_logic",
        header_text="In Logic",
        build_value=build_in_logic,
        sorter=sorter,
        filter=filt,
    ))
    _hint_column_installed = True


_kv_loaded = False


def load_tracker_kv():
    """Load Tracker.kv into the kivy Builder. Idempotent."""
    global _kv_loaded
    if _kv_loaded:
        return
    from kivy.lang import Builder
    import importlib.resources
    from Utils import user_path
    from . import TrackerWorld

    data = importlib.resources.files(TrackerWorld.__module__).joinpath("Tracker.kv").read_bytes().decode()
    Builder.load_string(data)
    user_file = user_path("data", "user.kv")
    if os.path.exists(user_file):
        logger.info("loading user.kv into builder.")
        Builder.load_file(user_file)
    _kv_loaded = True


def build_tracker_view(ctx):
    """Build the Tracker Page widget tree and bind tracker state labels onto ctx.

    Returns the root widget for the tab. The header labels (Locations / In Logic /
    Glitched / Hinted / Go Mode) are stashed back on the context so updateTracker
    can refresh them.
    """
    # Widget classes must exist before the kv string loads so its rules resolve.
    _ensure_widgets()
    load_tracker_kv()
    install_hint_log_column()

    # Local imports keep the no-GUI path from pulling Kivy.
    from kivy.uix.boxlayout import BoxLayout
    from kvui import MDLabel, MDDivider
    from kivy.metrics import dp
    from worlds.tracker.TrackerClient import get_ut_color

    tracker_view = _TrackerView_cls()
    # CustomLayout parents by pos/size; fill explicitly or the tracker
    # ends up 100x100 in the bottom-left corner.
    tracker = _TrackerLayout(orientation="vertical", size_hint=(1, 1),
                             pos_hint={"x": 0, "y": 0})

    tracker_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(36))
    tracker_divider = MDDivider(size_hint_y=None, height=dp(1))
    ctx.tracker_total_locs_label = MDLabel(text="Locations: 0/0", halign="center")
    ctx.tracker_logic_locs_label = MDLabel(text="In Logic: 0", halign="center")
    ctx.tracker_glitched_locs_label = MDLabel(
        text=f"Glitched: [color={get_ut_color('glitched')}]0[/color]", halign="center")
    ctx.tracker_hinted_locs_label = MDLabel(
        text=f"Hinted: [color={get_ut_color('hinted_in_logic')}]0[/color]", halign="center")
    ctx.tracker_go_mode_label = MDLabel(
        text=f"Go Mode: [color={get_ut_color('out_of_logic')}]No[/color]", halign="center")
    ctx.tracker_glitched_locs_label.markup = True
    ctx.tracker_hinted_locs_label.markup = True
    ctx.tracker_go_mode_label.markup = True
    tracker_header.add_widget(ctx.tracker_total_locs_label)
    tracker_header.add_widget(ctx.tracker_logic_locs_label)
    tracker_header.add_widget(ctx.tracker_glitched_locs_label)
    tracker_header.add_widget(ctx.tracker_hinted_locs_label)
    tracker_header.add_widget(ctx.tracker_go_mode_label)

    tracker.add_widget(tracker_header)
    tracker.add_widget(tracker_divider)
    tracker.add_widget(tracker_view)

    ctx.tracker_page = tracker_view

    if ctx.gen_error is not None:
        for line in ctx.gen_error.split("\n"):
            ctx.log_to_tab(line, False)

    return tracker


def build_map_view(ctx):
    """Build the Map Page widget (VisualTracker) and wire it into the context.

    Sets ctx.map_page and ctx.map_page_coords_func so load_map() and
    update_location_icon_coords() can drive the new map widget.
    """
    _ensure_widgets()
    load_tracker_kv()

    map_widget = _VisualTracker()
    ctx.map_page = map_widget
    ctx.map_page_coords_func = map_widget.load_coords
    return map_widget


# ---------- widget classes (lazy module-level singletons) ----------


_widgets_built = False
_TrackerLayout = None
_TrackerTooltip = None
_TrackerView_cls = None
_CheckItem = None
_ApLocationIcon = None
_ApLocation = None
_ApLocationDeferred = None
_APLocationMixed = None
_APLocationSplit = None
_VisualTracker = None


def _ensure_widgets():
    """Define widget classes on first use, after kivy is available."""
    global _widgets_built
    global _TrackerLayout, _TrackerTooltip, _TrackerView_cls, _CheckItem
    global _ApLocationIcon, _ApLocation, _ApLocationDeferred
    global _APLocationMixed, _APLocationSplit, _VisualTracker
    if _widgets_built:
        return

    from kivy.uix.boxlayout import BoxLayout
    from kvui import MDRecycleView, HoverBehavior
    from kivymd.uix.tooltip import MDTooltip
    from kivy.uix.widget import Widget
    from kivy.properties import StringProperty, BooleanProperty, DictProperty, ColorProperty, ObjectProperty
    # Local subclass keeps Tracker.kv's `<ApAsyncImage>:` rule off every
    # other AsyncImage in the app.
    from kivy.uix.image import AsyncImage as _KivyAsyncImage
    from kvui import MarkupToolTip
    # Importing registers them with the kivy Factory so Tracker.kv's rules resolve.
    from mwgg_gui.legacy import SelectableLabel, SelectableRecycleBoxLayout  # noqa: F401

    class ApAsyncImage(_KivyAsyncImage):
        pass

    from worlds.tracker import UT_VERSION
    from worlds.tracker.TrackerClient import get_ut_color
    from Utils import __version__, instance_name
    from worlds import AutoWorld

    apname = instance_name if instance_name else "AP"

    class CheckItem(BoxLayout):
        text = StringProperty()
        active = BooleanProperty()

    class TrackerLayout(BoxLayout):
        pass

    class TrackerTooltip(MarkupToolTip):
        pass

    class TrackerView(MDRecycleView):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.data = []
            self.theme_bg_color = "Custom"
            self.mw_bg_color = self.theme_cls.surfaceContainerLowestColor
            self.data.append({"text": f"Tracker {UT_VERSION} Initializing for {apname} version {__version__}"})

        def resetData(self):
            self.data.clear()
            clear_stray_tooltips()

        def addLine(self, line: str, sort: bool = False):
            self.data.append({"text": line})
            if sort:
                logger.warning("Sorting in TrackerClient is deprecated.")

    class ApLocationIcon(ApAsyncImage):
        pass

    class ApLocation(HoverBehavior, Widget, MDTooltip):
        locationDict = DictProperty()
        # kivymd's HoverBehavior dropped kvui's border_point; re-declare it as a
        # kivy ObjectProperty (to_window reads it, external code may bind to it).
        border_point = ObjectProperty(None)

        def __init__(self, sections, parent, **kwargs):
            for location_id in sections:
                self.locationDict[location_id] = "none"
                self.tracker_page = parent
            self.bind(locationDict=self.update_color)
            super().__init__(**kwargs)
            self._tooltip = TrackerTooltip(text="Test")
            self._tooltip.markup = True
            # Back-ref so clear_stray_tooltips can tell a live hover from an orphan.
            self._tooltip._tooltip = self

        def on_enter(self):
            self._tooltip.text = self.get_text()
            self.display_tooltip()

        def on_leave(self):
            self.animation_tooltip_dismiss()

        def transform_to_pop_coords(self, x, y):
            x2 = x
            y2 = self.tracker_page.height - y
            x3 = x2 - (self.tracker_page.x + (self.tracker_page.width - self.tracker_page.norm_image_size[0]) / 2)
            y3 = y2 + (self.tracker_page.y - (self.tracker_page.height - self.tracker_page.norm_image_size[1]) / 2)
            x4 = x3 / ((self.tracker_page.norm_image_size[0] / self.tracker_page.texture_size[0]) if self.tracker_page.texture_size[0] > 0 else 1)
            y4 = y3 / ((self.tracker_page.norm_image_size[1] / self.tracker_page.texture_size[1]) if self.tracker_page.texture_size[0] > 0 else 1)
            x5 = x4 + self.width / 2
            y5 = y4 + self.width / 2
            return (x5, y5)

        def on_mouse_pos(self, window, pos):
            return super().on_mouse_pos(window, pos)

        def to_window(self, x, y):
            if self.border_point:
                return self.border_point
            return self.tracker_page.to_window(x, y)

        def to_widget(self, x, y):
            return self.transform_to_pop_coords(*self.tracker_page.to_widget(x, y))

        def update_status(self, location, status):
            if location in self.locationDict:
                if self.locationDict[location] != status:
                    self.locationDict[location] = status

        def get_text(self):
            from kivy.app import App
            ctx = App.get_running_app().ctx
            location_id_to_name = AutoWorld.AutoWorldRegister.world_types[ctx.game].location_id_to_name
            lines = []
            for loc, status in self.locationDict.items():
                color = get_ut_color("collected_light")
                if status in ("in_logic", "out_of_logic", "glitched",
                              "hinted_in_logic", "hinted_out_of_logic", "hinted_glitched"):
                    color = get_ut_color(status)
                lines.append(f"{location_id_to_name[loc]} : [color={color}]{status}[/color]")
            return "\n".join(lines)

        def update_color(self, locationDict):
            return

    class ApLocationDeferred(ApLocation):
        color = ColorProperty("#" + get_ut_color("error"))

        def __init__(self, sections, parent, entrance, **kwargs):
            super().__init__(sections, parent, **kwargs)
            self.entrance = entrance

        @staticmethod
        def update_color(self, entranceDict):
            passable = any(status == "passable" for status in entranceDict.values())
            impassable = any(status == "impassable" for status in entranceDict.values())
            if passable:
                self.color = "#" + get_ut_color("in_logic")
            elif impassable:
                self.color = "#" + get_ut_color("out_of_logic")
            else:
                self.color = "#" + get_ut_color("collected")

        def get_text(self):
            from kivy.app import App
            ctx = App.get_running_app().ctx
            host_world = ctx.tracker_core.get_current_world()
            lines = []
            for entrance, status in self.locationDict.items():
                color = get_ut_color("out_of_logic")
                if status == "passed":
                    color = get_ut_color("collected_light")
                elif status == "passable":
                    color = get_ut_color("in_logic")
                poptracker_entrance_mapping = ctx.tracker_world.poptracker_entrance_mapping
                if poptracker_entrance_mapping:
                    try:
                        entrance_name = next(key for key in poptracker_entrance_mapping
                                             if poptracker_entrance_mapping[key] == entrance)
                    except StopIteration:
                        entrance_name = entrance
                else:
                    entrance_name = entrance
                lines.append(f"{entrance_name} : [color={color}]{status}[/color]")
                if host_world and self.entrance:
                    real_entrance = host_world.get_entrance(entrance)
                    if real_entrance.connected_region:
                        lines.append(f" - connects to ({real_entrance.connected_region.name})")
            return "\n".join(lines)

    class APLocationMixed(ApLocation):
        color = ColorProperty("#" + get_ut_color("error"))

        def __init__(self, sections, parent, **kwargs):
            super().__init__(sections, parent, **kwargs)

        @staticmethod
        def update_color(self, locationDict):
            glitches = any(status.endswith("glitched") for status in locationDict.values())
            in_logic = any(status.endswith("in_logic") for status in locationDict.values())
            out_of_logic = any(status.endswith("out_of_logic") for status in locationDict.values())
            hinted = any(status.startswith("hinted") for status in locationDict.values())

            if in_logic and (out_of_logic or (glitches and hinted)):
                self.color = "#" + get_ut_color("mixed_logic")
            elif glitches and hinted:
                self.color = "#" + get_ut_color("hinted_glitched")
            elif hinted and out_of_logic:
                self.color = "#" + get_ut_color("hinted_out_of_logic")
            elif hinted:
                self.color = "#" + get_ut_color("hinted")
            elif glitches and in_logic:
                self.color = "#" + get_ut_color("in_logic_glitched")
            elif glitches and out_of_logic:
                self.color = "#" + get_ut_color("out_of_logic_glitched")
            elif in_logic:
                self.color = "#" + get_ut_color("in_logic")
            elif out_of_logic:
                self.color = "#" + get_ut_color("out_of_logic")
            elif glitches:
                self.color = "#" + get_ut_color("glitched")
            else:
                self.color = "#" + get_ut_color("collected")

    class APLocationSplit(ApLocation):
        color_1 = ColorProperty("#" + get_ut_color("error"))
        color_2 = ColorProperty("#" + get_ut_color("error"))
        color_3 = ColorProperty("#" + get_ut_color("error"))
        color_4 = ColorProperty("#" + get_ut_color("error"))

        def __init__(self, sections, parent, **kwargs):
            super().__init__(sections, parent, **kwargs)

        @staticmethod
        def update_color(self, locationDict):
            color_list = Counter()

            def sort_status(pair) -> float:
                if pair[0] == "out_of_logic":
                    return 0
                if pair[0] == "in_logic":
                    return 999999999
                if pair[0] == "hinted_in_logic":
                    return 8888888
                return pair[1] + (ord(pair[0][0]) / 10)

            for status in locationDict.values():
                if status == "collected":
                    continue
                color_list[status] += 1

            color_list = [k for k, _ in sorted(color_list.items(), key=sort_status, reverse=True)]
            if color_list:
                color_list = (color_list * max(2, (4 // len(color_list))))[:4]
                self.color_1 = "#" + get_ut_color(color_list[0])
                self.color_2 = "#" + get_ut_color(color_list[1])
                self.color_3 = "#" + get_ut_color(color_list[2])
                self.color_4 = "#" + get_ut_color(color_list[3])
            else:
                self.color_1 = "#" + get_ut_color("collected")
                self.color_2 = "#" + get_ut_color("collected")
                self.color_3 = "#" + get_ut_color("collected")
                self.color_4 = "#" + get_ut_color("collected")

    class VisualTracker(BoxLayout):
        location_icons: list  # pooled ApLocationIcon widgets, see update_location_icon_widgets

        def load_coords(self, coords, defered_coords, ldefered_coords, use_split, default_loc_size: int = 65):
            self.ids.location_canvas.clear_widgets()
            returnDict = defaultdict(list)
            deferredDict = defaultdict(list)
            ldeferredDict = defaultdict(list)
            for coord, (sections, size) in coords.items():
                ap_location_class = APLocationSplit if use_split else APLocationMixed
                loc_size = size if size is not None else default_loc_size
                temp_loc = ap_location_class(sections, self.ids.tracker_map, pos=coord, size=(loc_size, loc_size))
                self.ids.location_canvas.add_widget(temp_loc)
                for location_id in sections:
                    returnDict[location_id].append(temp_loc)
            for coord, (sections, size) in defered_coords.items():
                loc_size = size if size is not None else default_loc_size
                temp_loc = ApLocationDeferred(sections, self.ids.tracker_map, True, pos=coord, size=(loc_size, loc_size))
                self.ids.location_canvas.add_widget(temp_loc)
                for entrance_name in sections:
                    deferredDict[entrance_name].append(temp_loc)
            for coord, (sections, size) in ldefered_coords.items():
                loc_size = size if size is not None else default_loc_size
                temp_loc = ApLocationDeferred(sections, self.ids.tracker_map, False, pos=coord, size=(loc_size, loc_size))
                self.ids.location_canvas.add_widget(temp_loc)
                for event_name in sections:
                    ldeferredDict[event_name].append(temp_loc)
            # Canvas was just cleared, so reset the icon pool; load_map() calls
            # update_location_icon_widgets right after.
            self.location_icons = []
            return returnDict, deferredDict, ldeferredDict

        def update_location_icon_widgets(self, ctx, location_icons):
            # Reuse existing pooled widgets where possible, only adding/removing
            # when the number of simultaneous icons actually changes.
            for i, (x, y, ref) in enumerate(location_icons):
                if i < len(self.location_icons):
                    self.location_icons[i].source = f"{ctx.root_pack_path}/{ref}"
                    self.location_icons[i].pos = (x, y)
                else:
                    location_icon = ApLocationIcon(source=f"{ctx.root_pack_path}/{ref}", pos=(x, y),
                                                    size=(ctx.ui.loc_icon_size, ctx.ui.loc_icon_size))
                    self.ids.location_canvas.add_widget(location_icon)
                    self.location_icons.append(location_icon)

            if len(self.location_icons) > len(location_icons):
                for icon in self.location_icons[len(location_icons):]:
                    self.ids.location_canvas.remove_widget(icon)
                del self.location_icons[len(location_icons):]

    _CheckItem = CheckItem
    _TrackerLayout = TrackerLayout
    _TrackerTooltip = TrackerTooltip
    _TrackerView_cls = TrackerView
    _ApLocationIcon = ApLocationIcon
    _ApLocation = ApLocation
    _ApLocationDeferred = ApLocationDeferred
    _APLocationMixed = APLocationMixed
    _APLocationSplit = APLocationSplit
    _VisualTracker = VisualTracker
    _widgets_built = True


# ---------- live-app helpers (kv references `app.<thing>`) ----------


def install_app_surface(ctx, app):
    """Inject the tracker-specific kivy properties and dropdown methods onto
    the LIVE launcher app, so the Tracker.kv file's `app.source`,
    `app.open_map_dropdown`, etc. resolve correctly. Idempotent."""
    if getattr(app, "_tracker_surface_installed", False):
        return

    from kivy.properties import StringProperty, NumericProperty, BooleanProperty
    import types

    # Kivy properties referenced from Tracker.kv; apply_property only takes
    # effect if the attribute isn't already a property on the class.
    try:
        app.apply_property(
            source=StringProperty(""),
            loc_size=NumericProperty(20),
            loc_icon_size=NumericProperty(20),
            loc_border=NumericProperty(5),
            enable_map=BooleanProperty(False),
            iconSource=StringProperty(""),
            current_map=StringProperty(""),
            auto_tab=BooleanProperty(True),
        )
    except Exception:
        # Relaunch in the same process: existing properties are reusable.
        traceback.print_exc()

    app.open_map_dropdown = types.MethodType(_open_map_dropdown, app)
    app.set_dropdown_items = types.MethodType(_set_dropdown_items, app)
    app.create_dropdown_menu_items = types.MethodType(_create_dropdown_menu_items, app)
    app.map_dropdown_callback = types.MethodType(_map_dropdown_callback, app)
    app.on_auto_tab_active = types.MethodType(_on_auto_tab_active, app)
    app._tracker_surface_installed = True

    # Contribute the Tracker section to the launcher's SettingsScreen;
    # register_settings_section handles both not-yet-built and already-live cases.
    try:
        from mwgg_gui.settings import register_settings_section
        from worlds.tracker.settings_ui import TrackerSettings
        register_settings_section(
            name="tracker",
            title="Tracker",
            factory=TrackerSettings,
            items=[
                {"name": "Runtime", "icon": "play-circle"},
                {"name": "Display", "icon": "format-list-bulleted"},
                {"name": "Behavior", "icon": "tune"},
            ],
        )
    except Exception:
        traceback.print_exc()


def _open_map_dropdown(self, item):
    from kivymd.uix.menu import MDDropdownMenu
    dropdown_menu = MDDropdownMenu(caller=item, hor_growth="right", ver_growth="down")
    if self.ctx.map_groups:
        menu_items = self.create_dropdown_menu_items(dropdown_menu, self.ctx.map_groups)
    else:
        menu_items = [
            {"text": m["name"],
             "on_release": lambda i=i: self.map_dropdown_callback(dropdown_menu, i)}
            for i, m in enumerate(self.ctx.maps)
        ]
    dropdown_menu.items = menu_items
    dropdown_menu.open()


def _set_dropdown_items(self, menu, menu_items):
    from kivy.metrics import dp
    from kivy.animation import Animation
    menu.items = menu_items
    menu.set_menu_properties()
    menu.position = menu.adjust_position()
    if menu.width <= 100:
        menu.width = dp(240)
    menu._tar_x, menu._tar_y = menu.get_target_pos()
    anim = Animation(
        height=menu.target_height,
        x=menu._tar_x,
        y=menu._tar_y - menu.target_height,
        scale_value_center=menu.caller.center,
        duration=menu.hide_duration * 2,
        transition=menu.hide_transition,
    )
    anim.start(menu)


def _create_dropdown_menu_items(self, menu, groups):
    menu_items = []
    for group in groups:
        if isinstance(group, str):
            name = group
            x = group
            trailing_icon = ""
        else:
            name = group[0]
            x = group[1]
            if (isinstance(x, list) and len(x) == 1 and isinstance(x[0], str)) or isinstance(x, str):
                trailing_icon = ""
            else:
                trailing_icon = "menu-right"
        menu_items.append({
            "text": name,
            "trailing_icon": trailing_icon,
            "on_release": lambda menu=menu, x=x: self.map_dropdown_callback(menu, x),
        })
    return menu_items


def _map_dropdown_callback(self, menu, group_item):
    if not isinstance(group_item, list):
        self.ctx.load_map(group_item)
        self.ctx.updateTracker()
    elif isinstance(group_item, list) and len(group_item) == 1 and isinstance(group_item[0], str):
        self.ctx.load_map(group_item[0])
        self.ctx.updateTracker()
    else:
        menu_items = [{
            "text": "Return", "leading_icon": "menu-left",
            "on_release": lambda menu=menu, items=menu.items: self.set_dropdown_items(menu, items),
        }]
        menu_items.extend(self.create_dropdown_menu_items(menu, group_item))
        self.set_dropdown_items(menu, menu_items)


def _on_auto_tab_active(self, checkitem, value):
    self.ctx.auto_tab = value
