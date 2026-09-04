"""Poptracker map/pack plumbing shared by the standalone Universal Tracker
context and the game-client overlay (wrap.py).

``UTMapController`` binds its state onto ``ctx`` under the attribute names
``TrackerGameContext`` has always used (``tracker_world``, ``maps``,
``map_page``, ``load_map``, ...) since ``worlds/tracker/gui.py``, Tracker.kv
(via ``app.ctx.*``) and the connected World's own code all read/write those
names directly on the context, whether that context is a ``TrackerGameContext``
or an arbitrary game client with the tracker overlay attached.
"""
from __future__ import annotations

import logging
import traceback
from typing import Any, Union

from Utils import open_filename
from worlds import AutoWorld

from . import UTMapTabData

logger = logging.getLogger("Client")

UT_MAP_TAB_KEY = "UT_MAP"


def _noop_coords(*_args) -> tuple[dict, dict, dict]:
    """Placeholder for ``ctx.map_page_coords_func`` before a map widget
    exists; matches ``VisualTracker.load_coords``'s 3-tuple return shape so
    an early ``load_map`` call (e.g. from ``load_pack``) can't crash on
    unpack."""
    return {}, {}, {}


def load_json(pack, path):
    """Read a JSON resource from inside an installed apworld package;
    importlib.resources so zipimport (.apworld) installs work too."""
    import importlib.resources
    import json
    ref = importlib.resources.files(pack)
    for part in path.lstrip("/").split("/"):
        ref = ref.joinpath(part)
    return json.loads(ref.read_bytes().decode("utf-8-sig"))


def load_json_zip(pack, path):
    import json
    import zipfile
    with zipfile.ZipFile(pack) as parentFile:
        with parentFile.open(path) as childFile:
            return json.loads(childFile.read().decode('utf-8-sig'))


def _refresh_ctx(ctx) -> None:
    """Best-effort tracker refresh after a map/setting change.

    Standalone contexts expose ``updateTracker`` directly; the overlay
    exposes ``tracker_overlay_refresh`` once ``wrap.start_overlay_ui_refresh``
    (Phase 2) has run.
    """
    update = getattr(ctx, "updateTracker", None)
    if update is not None:
        update()
        return
    refresh = getattr(ctx, "tracker_overlay_refresh", None)
    if refresh is not None:
        refresh()


def cmd_load_map(self, map_id: str = "0") -> None:
    """Force a poptracker map id to be loaded"""
    if self.ctx.tracker_world is not None:
        self.ctx.load_map(map_id)
        _refresh_ctx(self.ctx)
    else:
        logger.info("No world with internal map loaded")


def cmd_list_maps(self) -> None:
    """List the available maps to load with /load_map"""
    if self.ctx.tracker_world is not None:
        for i, map in enumerate(self.ctx.maps):
            logger.info("Map[" + str(i) + "] = '" + map["name"] + "'")
    else:
        logger.info("No world with internal map loaded")


class UTMapController:
    """Owns Poptracker pack/map state for one connected tracker context.

    Binds its state onto ``ctx`` (``tracker_world``, ``maps``, ``map_page``,
    ``coord_dict``, ...) and also binds ``load_map``/``set_map_visible``/
    ``update_location_icon_coords`` as callables on ``ctx`` itself, so
    ``gui.py``, Tracker.kv, ``settings_ui.py`` and the ``/load_map``/
    ``/list_maps`` commands can call ``ctx.load_map(...)`` etc regardless of
    whether ``ctx`` is a ``TrackerGameContext`` or a game client with the
    overlay attached.
    """

    def __init__(self, ctx, tracker_core) -> None:
        self.ctx = ctx
        self.tracker_core = tracker_core

        ctx.tracker_world = None
        ctx.maps = []
        ctx.locs = []
        ctx.layouts = []
        ctx.map_to_name = None
        ctx.map_groups = None
        ctx.coord_dict = {}
        ctx.deferred_dict = {}
        ctx.ldeferred_dict = {}
        ctx.map_page_coords_func = _noop_coords
        ctx.location_icons = []
        ctx.root_pack_path = None
        ctx.map_id = None
        ctx.use_split = True
        ctx.map_page = None
        ctx._map_tab_handle = None
        ctx._map_content = None
        ctx._show_map = False
        ctx._map_activated = False
        if not hasattr(ctx, "auto_tab"):
            ctx.auto_tab = True

        ctx._map_controller = self
        ctx.load_map = self.load_map
        ctx.set_map_visible = self.set_map_visible
        ctx.update_location_icon_coords = self.update_location_icon_coords

    # ---------- pack/layout parsing ----------

    def parse_layout_node(self, node, curr_path, is_tab=False):
        ctx = self.ctx
        if is_tab:
            name = node["title"]
            curr_path = name if curr_path is None else f"{curr_path}/{name}"
        else:
            name = None
        maps = []

        if "type" in node and node["type"] == "map":
            maps = node["maps"]
            if curr_path is not None:
                if len(maps) == 1:
                    ctx.map_to_name[maps[0]] = curr_path
                else:
                    for m in maps:
                        ctx.map_to_name[m] = f"{curr_path}/{m}"
        elif "content" in node:
            if isinstance(node["content"], list):
                for item in node["content"]:
                    result = self.parse_layout_node(item, curr_path)
                    if isinstance(result, list):
                        maps.extend(result)
                    elif result:
                        maps.append(result)
            else:
                result = self.parse_layout_node(node["content"], curr_path)
                if result:
                    maps = result
        elif "tabs" in node:
            if isinstance(node["tabs"], list):
                for item in node["tabs"]:
                    result = self.parse_layout_node(item, curr_path, True)
                    if isinstance(result, list):
                        maps.extend(result)
                    elif result:
                        maps.append(result)
            else:
                result = self.parse_layout_node(node["tabs"], curr_path, True)
                if result:
                    maps = result

        return (name, maps) if name is not None else maps

    def parse_map_group_node_names(self, node: str | tuple, curr_path: str, has_siblings: bool):
        ctx = self.ctx
        if isinstance(node, str):
            if has_siblings:
                curr_path = node if curr_path is None else f"{curr_path}/{node}"
            ctx.map_to_name[node] = curr_path
        else:
            name = node[0]
            curr_path = name if curr_path is None else f"{curr_path}/{name}"
            if isinstance(node[1], list):
                for x in node[1]:
                    self.parse_map_group_node_names(x, curr_path, len(node[1]) > 1)
            else:
                self.parse_map_group_node_names(node[1], curr_path, False)

    def parse_map_groups(self) -> None:
        ctx = self.ctx
        ctx.map_to_name = {}
        if ctx.tracker_world.map_page_groups is not None:
            ctx.map_groups = ctx.tracker_world.map_page_groups
            for x in ctx.map_groups:
                self.parse_map_group_node_names(x, None, True)
            return
        all_layouts = []
        for layout in ctx.layouts:
            maps = []
            for key, node in layout.items():
                result = self.parse_layout_node(node, None)
                if result:
                    maps.extend(result)
            if maps:
                all_layouts.extend(maps)
        ctx.map_groups = all_layouts

    # ---------- pack loading ----------

    def load_pack(self) -> None:
        ctx = self.ctx
        assert self.tracker_core.player_id is not None
        assert ctx.tracker_world is not None
        current_world = self.tracker_core.get_current_world()
        assert current_world
        ctx.maps = []
        ctx.locs = []
        ctx.layouts = []
        if ctx.tracker_world.external_pack_key:
            assert current_world.settings
            try:
                from zipfile import is_zipfile
                packRef = current_world.settings[ctx.tracker_world.external_pack_key]
                if not packRef or str(packRef) in ("", ".") or not is_zipfile(packRef):
                    prompt_desc = getattr(current_world.settings[ctx.tracker_world.external_pack_key], "ut_dialog_name", "Select Poptracker pack")
                    packRef = open_filename(prompt_desc, filetypes=[("Poptracker Pack", [".zip"])])
                    current_world.settings[ctx.tracker_world.external_pack_key] = packRef or ""
                    current_world.settings._changed = True
                if packRef:
                    if is_zipfile(packRef):
                        current_world.settings.update({ctx.tracker_world.external_pack_key: packRef})
                        current_world.settings._changed = True
                        # Pack version skew is normal
                        def _try_load_zip(label, path):
                            try:
                                return load_json_zip(packRef, path)
                            except KeyError:
                                logger.warning(f"Poptracker pack is missing {label} {path!r}; skipping.")
                                return None
                        def _try_load_pkg(label, path):
                            try:
                                return load_json(PACK_NAME, path)
                            except (FileNotFoundError, KeyError):
                                logger.warning(f"Apworld pack is missing {label} {path!r}; skipping.")
                                return None
                        if ctx.tracker_world.map_page_folder:
                            PACK_NAME = current_world.__class__.__module__
                            for map_page in ctx.tracker_world.map_page_maps:
                                data = _try_load_pkg("map page", f"/{ctx.tracker_world.map_page_folder}/{map_page}")
                                if data: ctx.maps += data
                            for loc_page in ctx.tracker_world.map_page_locations:
                                data = _try_load_pkg("locations page", f"/{ctx.tracker_world.map_page_folder}/{loc_page}")
                                if data: ctx.locs += data
                            for layout_page in ctx.tracker_world.map_page_layouts:
                                data = _try_load_pkg("layout page", f"/{ctx.tracker_world.map_page_folder}/{layout_page}")
                                if data: ctx.layouts.append(data)
                        else:
                            for map_page in ctx.tracker_world.map_page_maps:
                                data = _try_load_zip("map page", f"{map_page}")
                                if data: ctx.maps += data
                            for loc_page in ctx.tracker_world.map_page_locations:
                                data = _try_load_zip("locations page", f"{loc_page}")
                                if data: ctx.locs += data
                            for layout_page in ctx.tracker_world.map_page_layouts:
                                data = _try_load_zip("layout page", f"{layout_page}")
                                if data: ctx.layouts.append(data)
                    else:
                        current_world.settings.update({ctx.tracker_world.external_pack_key: ""})  # failed to find a pack, prompt next launch
                        current_world.settings._changed = True
                        ctx.tracker_world = None
                        return
                else:
                    current_world.settings[ctx.tracker_world.external_pack_key] = None
                    ctx.tracker_world = None
                    return
            except Exception:
                logger.error("Selected poptracker pack was invalid")
                current_world.settings[ctx.tracker_world.external_pack_key] = ""
                current_world.settings._changed = True
                ctx.tracker_world = None
                return
        else:
            PACK_NAME = current_world.__class__.__module__
            for map_page in ctx.tracker_world.map_page_maps:
                ctx.maps += load_json(PACK_NAME, f"/{ctx.tracker_world.map_page_folder}/{map_page}")
            for loc_page in ctx.tracker_world.map_page_locations:
                ctx.locs += load_json(PACK_NAME, f"/{ctx.tracker_world.map_page_folder}/{loc_page}")
            for layout_page in ctx.tracker_world.map_page_layouts:
                ctx.layouts.append(load_json(PACK_NAME, f"/{ctx.tracker_world.map_page_folder}/{layout_page}"))
        self.parse_map_groups()
        self.load_map(None)

    def load_map(self, map_id: Union[int, str, None]) -> None:
        """REMEMBER TO RUN UPDATE_TRACKER!"""
        ctx = self.ctx
        if not ctx.ui or ctx.tracker_world is None:
            return
        if map_id is None:
            key = ctx.tracker_world.map_page_setting_key or f"{ctx.slot}_{ctx.team}_{UT_MAP_TAB_KEY}"
            map_id = ctx.tracker_world.map_page_index(ctx.stored_data.get(key, ""))
            if not ctx.auto_tab or map_id < 0 or map_id >= len(ctx.maps):
                return  # special case, don't load a new map
        if ctx.map_id is not None and ctx.map_id == map_id:
            return  # map already loaded
        m = None
        if isinstance(map_id, str) and not map_id.isdecimal():
            for map in ctx.maps:
                if map["name"] == map_id:
                    m = map
                    map_id = ctx.maps.index(map)
                    break
            else:
                logger.error("Attempted to load a map that doesn't exist")
                return
        else:
            if isinstance(map_id, str):
                map_id = int(map_id)
            if map_id is None or map_id < 0 or map_id >= len(ctx.maps):
                logger.error("Attempted to load a map that doesn't exist")
                return
            m = ctx.maps[map_id]
        ctx.map_id = map_id
        if ctx.map_to_name is not None:
            ctx.ui.current_map = ctx.map_to_name.get(m["name"], m["name"])
        else:
            ctx.ui.current_map = m["name"]
        location_name_to_id = AutoWorld.AutoWorldRegister.world_types[ctx.game].location_name_to_id
        if ctx.tracker_world.external_pack_key:
            from zipfile import is_zipfile
            packRef = self.tracker_core.get_current_world().settings[ctx.tracker_world.external_pack_key]
            if packRef and is_zipfile(packRef):
                ctx.root_pack_path = f"ap:zip:{packRef}"
            else:
                logger.error("Player poptracker doesn't seem to exist :< (must be a zip file)")
                return
        else:
            PACK_NAME = self.tracker_core.get_current_world().__class__.__module__
            ctx.root_pack_path = f"ap:{PACK_NAME}/{ctx.tracker_world.map_page_folder}"
        ctx.ui.source = f"{ctx.root_pack_path}/{m['img']}"
        ctx.ui.loc_size = m["location_size"] if "location_size" in m else 65  # default location size per poptracker/src/core/map.h
        ctx.ui.loc_icon_size = m["location_icon_size"] if "location_icon_size" in m else ctx.ui.loc_size
        ctx.ui.loc_border = m["location_border_thickness"] if "location_border_thickness" in m else 8  # default location size per poptracker/src/core/map.h
        temp_locs = [location for location in ctx.locs]
        map_locs = []
        hidden_locations = getattr(self.tracker_core.get_current_world(), "ut_map_page_hidden_locations", {})
        current_hidden_locs = hidden_locations.get(m["name"], [])
        while temp_locs:
            temp_loc = temp_locs.pop()
            if "map_locations" in temp_loc:
                if "name" not in temp_loc:
                    temp_loc["name"] = ""
                map_locs.append(temp_loc)
            elif "children" in temp_loc:
                temp_locs.extend(temp_loc["children"])
        coords = {
            (map_loc["x"], map_loc["y"]):
                ([location_name_to_id[section["name"]] for section in location["sections"]
                  if "name" in section and section["name"] in location_name_to_id
                  and location_name_to_id[section["name"]] in ctx.server_locations
                  and not location_name_to_id[section["name"]] in current_hidden_locs],
                 map_loc.get("size"))
            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in location_name_to_id
                and location_name_to_id[section["name"]] in ctx.server_locations
                and location_name_to_id[section["name"]] not in current_hidden_locs
                for section in location["sections"]
            )
        }
        poptracker_name_mapping = ctx.tracker_world.poptracker_name_mapping
        if poptracker_name_mapping:
            tempCoords = {  # compat coords
                (map_loc["x"], map_loc["y"]):
                    ([poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] for section in location["sections"]
                      if "name" in section and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                      and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in ctx.server_locations
                      and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] not in current_hidden_locs],
                     map_loc.get("size"))
                for location in map_locs
                for map_loc in location["map_locations"]
                if map_loc["map"] == m["name"]
                   and any("name" in section and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                           and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in ctx.server_locations
                           and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] not in current_hidden_locs
                           for section in location["sections"])
            }
            for maploc, (seclist, size) in tempCoords.items():
                if maploc in coords:
                    coords[maploc] = (coords[maploc][0] + seclist, coords[maploc][1] or size)
                else:
                    coords[maploc] = (seclist, size)
        entrance_cache = list(self.tracker_core.multiworld.regions.entrance_cache[self.tracker_core.player_id].keys())
        hidden_entrances = getattr(self.tracker_core.get_current_world(), "ut_map_page_hidden_entrances", {})
        current_hidden_entrances = hidden_entrances.get(m["name"], [])
        dcoords = {
            (map_loc["x"], map_loc["y"]): ([section["name"] for section in location["sections"]
                                            if "name" in section and section["name"] in entrance_cache
                                            and section["name"] not in current_hidden_entrances],
                                           map_loc.get("size"))
            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in entrance_cache
                and section["name"] not in current_hidden_entrances for section in location["sections"]
            )
        }
        poptracker_entrance_mapping = ctx.tracker_world.poptracker_entrance_mapping
        if poptracker_entrance_mapping:
            tempCoords = {
                (map_loc["x"], map_loc["y"]): ([poptracker_entrance_mapping[section["name"]] for section in location["sections"]
                                                if "name" in section and section["name"] in poptracker_entrance_mapping
                                                and poptracker_entrance_mapping[section["name"]] in entrance_cache
                                                and poptracker_entrance_mapping[section["name"]] not in current_hidden_entrances],
                                               map_loc.get("size"))
                for location in map_locs
                for map_loc in location["map_locations"]
                if map_loc["map"] == m["name"] and any(
                    "name" in section and section["name"] in poptracker_entrance_mapping
                    and poptracker_entrance_mapping[section["name"]] in entrance_cache
                    and poptracker_entrance_mapping[section["name"]] not in current_hidden_entrances
                    for section in location["sections"]
                )
            }
            for maploc, (seclist, size) in tempCoords.items():
                if maploc in dcoords:
                    dcoords[maploc] = (dcoords[maploc][0] + seclist, dcoords[maploc][1] or size)
                else:
                    dcoords[maploc] = (seclist, size)
        event_loc_cache = [loc.name for loc in self.tracker_core.get_current_world().get_locations() if loc.address is None and loc.parent_region is not None]
        hidden_events = getattr(self.tracker_core.get_current_world(), "ut_map_page_hidden_events", {})
        current_hidden_events = hidden_events.get(m["name"], [])
        dlcoords = {
            (map_loc["x"], map_loc["y"]): ([section["name"] for section in location["sections"] if
                                            "name" in section and section["name"] in event_loc_cache and section["name"] not in current_hidden_events],
                                           map_loc.get("size"))
            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in event_loc_cache
                and section["name"] not in current_hidden_events
                for section in location["sections"]
            )
        }
        both_dcoords = set(entrance_cache).intersection(set(event_loc_cache))
        if both_dcoords:
            for _, (temp_names, _) in dcoords.items():
                if both_dcoords.intersection(temp_names):
                    logger.error("Mixing of entrance and event names, map will refuse to load")
                    return
            for _, (temp_names, _) in dlcoords.items():
                if both_dcoords.intersection(temp_names):
                    logger.error("Mixing of entrance and event names, map will refuse to load")
                    return
        ctx.coord_dict, ctx.deferred_dict, ctx.ldeferred_dict = ctx.map_page_coords_func(
            coords, dcoords, dlcoords, ctx.use_split, ctx.ui.loc_size)
        if ctx.tracker_world.location_setting_key:
            self.update_location_icon_coords()

    def update_location_icon_coords(self) -> None:
        ctx = self.ctx
        icon_key = ctx.tracker_world.location_setting_key
        temp_rets = ctx.tracker_world.location_icon_coords(ctx.map_id, ctx.stored_data.get(icon_key, ""))

        ctx.location_icons.clear()
        if temp_rets:
            if type(temp_rets) != list:  # old callback returning a single tuple
                temp_rets = [temp_rets]
            for temp_ret in temp_rets:
                (x, y, ref) = temp_ret  # should be a 3-tuple
                if x >= 0 and y >= 0:
                    ctx.location_icons.append((x, y, ref))
        if ctx.map_page:
            ctx.map_page.update_location_icon_widgets(ctx, ctx.location_icons)

    # ---------- tab visibility ----------

    def set_map_visible(self, visible: bool) -> None:
        """Toggle the Map Page tab on the live UI."""
        ctx = self.ctx
        if visible == ctx._show_map:
            return
        from kivymd.app import MDApp
        ui = MDApp.get_running_app()
        if ui is None:
            return  # no live UI yet; caller will retry once attached
        if visible:
            if ctx._map_tab_handle is not None:
                ctx._show_map = True
                return
            # Reuse the prebuilt widget: load_pack already loaded its coords, and
            # load_map skips a map id that is already current.
            if ctx._map_content is None:
                from .gui import build_map_view
                try:
                    ctx._map_content = build_map_view(ctx)
                except Exception:
                    traceback.print_exc()
                    return
            # Single-word lowercase to match the launcher's screen menu convention.
            ctx._map_tab_handle = ui.add_client_tab("map", ctx._map_content)
            ctx._show_map = True
        else:
            if ctx._map_tab_handle is not None:
                ui.remove_client_tab(ctx._map_tab_handle)
                ctx._map_tab_handle = None
                ctx._map_content = None
                ctx.map_page = None
                ctx.map_page_coords_func = _noop_coords
            ctx._show_map = False

    def prebuild_widget(self) -> None:
        """Eagerly build the Map Page widget so ``map_page_coords_func`` is
        wired before ``load_pack``'s tail ``load_map(None)`` call runs.
        Idempotent; mirrors the standalone ``build_gui``'s eager
        ``build_map_view`` call."""
        if self.ctx.map_page is not None:
            return
        from .gui import build_map_view
        try:
            self.ctx._map_content = build_map_view(self.ctx)
        except Exception:
            logger.exception("Tracker map: eager widget prebuild failed")

    # ---------- Connected / activation ----------

    def build_tracker_world(self, connected_cls: type) -> None:
        """Construct ``ctx.tracker_world`` from the connected World class (or
        its current instance) if it advertises one. Mirrors
        TrackerGameContext.on_package's Connected branch. Cheap/side-effect
        free: does not touch the pack or the UI, so it is safe to call
        regardless of whether a live app exists yet."""
        ctx = self.ctx
        current_world = self.tracker_core.get_current_world()
        if hasattr(connected_cls, "tracker_world"):
            source = connected_cls
        elif current_world is not None and hasattr(current_world, "tracker_world"):
            source = current_world
        else:
            ctx.tracker_world = None
            return
        ctx.tracker_world = UTMapTabData(ctx.slot, ctx.team, **getattr(source, "tracker_world", {}))

    def activate(self, app) -> None:
        """Finish wiring the map: load the pack, show the tab, subscribe to
        the map/icon data storage keys, and register the load_map/list_maps
        commands. Mirrors TrackerGameContext.on_package's Connected map
        block. Idempotent and a no-op without a live app or a known
        ``tracker_world`` -- safe to call from both the Connected handler
        (if the app is already live) and the Phase-2 overlay feature (if
        Connected already ran)."""
        ctx = self.ctx
        if app is None or ctx.tracker_world is None or ctx._map_activated:
            return
        if getattr(ctx, "ui", None) is None:
            ctx.ui = app
        self.prebuild_widget()
        self.load_pack()
        if ctx.tracker_world:  # don't show the map if loading failed
            self.set_map_visible(True)
            if ctx.tracker_world.map_page_index:
                key = ctx.tracker_world.map_page_setting_key or f"{ctx.slot}_{ctx.team}_{UT_MAP_TAB_KEY}"
                ctx.set_notify(key)
            icon_key = ctx.tracker_world.location_setting_key
            if icon_key:
                ctx.set_notify(icon_key)
        processor = ctx.command_processor
        if "load_map" not in processor.commands or not processor.commands["load_map"]:
            processor.commands["load_map"] = cmd_load_map
        if "list_maps" not in processor.commands or not processor.commands["list_maps"]:
            processor.commands["list_maps"] = cmd_list_maps
        ctx._map_activated = True

    def handle_stored_data(self, args: dict) -> None:
        """Reload the map / icon overlay when SetReply or Retrieved touches
        the map-choice or location-icon data storage keys."""
        ctx = self.ctx
        if getattr(ctx, "ui", None) is None or not ctx.tracker_world:
            return
        key = ctx.tracker_world.map_page_setting_key or f"{ctx.slot}_{ctx.team}_{UT_MAP_TAB_KEY}"
        icon_key = ctx.tracker_world.location_setting_key
        if "key" in args:
            if args["key"] == key:
                self.load_map(None)
                _refresh_ctx(ctx)
            if args["key"] == icon_key:
                self.update_location_icon_coords()
        elif "keys" in args:
            if icon_key in args["keys"]:
                self.update_location_icon_coords()

    def disconnect(self) -> None:
        """Tear down map state on disconnect; mirrors
        TrackerGameContext.disconnect's map block. Safe to call even if the
        map was never activated."""
        ctx = self.ctx
        if getattr(ctx, "ui", None):
            self.set_map_visible(False)
        if ctx.tracker_world:
            ctx.command_processor.commands.pop("load_map", None)
            ctx.command_processor.commands.pop("list_maps", None)
            ctx.map_id = None
            ctx.root_pack_path = None
            ctx.coord_dict.clear()
            ctx.deferred_dict.clear()
            ctx.ldeferred_dict.clear()
        ctx.tracker_world = None
        ctx._map_activated = False
