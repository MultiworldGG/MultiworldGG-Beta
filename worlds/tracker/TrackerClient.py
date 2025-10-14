import asyncio
import logging
import traceback
from collections.abc import Callable
from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop, ClientCommandProcessor, handle_url_arg
import os
import time
import sys
from typing import Union, Any, TYPE_CHECKING


from BaseClasses import CollectionState, MultiWorld, LocationProgressType, ItemClassification, Location
from worlds.generic.Rules import exclusion_rules
from Utils import __version__, output_path, open_filename,async_start
import Utils

apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from . import TrackerWorld, UTMapTabData, CurrentTrackerState,UT_VERSION
from .TrackerCore import TrackerCore
from collections import Counter, defaultdict
from MultiServer import mark_raw
from NetUtils import NetworkItem

from . import TrackerCore

from gui import get_ut_color

if not sys.stdout:  # to make sure sm varia's "i'm working" dots don't break UT in frozen
    sys.stdout = open(os.devnull, 'w', encoding="utf-8")  # from https://stackoverflow.com/a/6735958

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111
UT_MAP_TAB_KEY = "UT_MAP"
   
    
class TrackerCommandProcessor(ClientCommandProcessor):
    ctx: "TrackerGameContext"

    @mark_raw
    def _cmd_inventory(self, filter_text: str = ""):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for item, count in sorted(currentState.all_items.items()):
            if filter_text in item:
                logger.info(str(count) + "x: " + item)

    @mark_raw
    def _cmd_prog_inventory(self, filter_text: str = ""):
        """Print the list of current progression items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for item, count in sorted(currentState.prog_items.items()):
            if filter_text in item:
                logger.info(str(count) + "x: " + item)

    @mark_raw
    def _cmd_event_inventory(self, filter_text: str = ""):
        """Print the list of current event items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for event in sorted(currentState.events):
            if filter_text in event:
                logger.info(event)

    @mark_raw
    def _cmd_manually_collect(self, item_name: str = ""):
        """Manually adds an item name to the CollectionState to test"""
        self.ctx.tracker_core.manual_items.append(item_name)
        self.ctx.updateTracker()
        logger.info(f"Added {item_name} to manually collect.")

    def _cmd_reset_manually_collect(self):
        """Resets the list of items manually collected by /manually_collect"""
        self.ctx.tracker_core.manual_items = []
        self.ctx.updateTracker()
        logger.info("Reset manually collect.")

    @mark_raw
    def _cmd_ignore(self, location_name: str = ""):
        """Ignore a location so it doesn't appear in the tracker list"""
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        location_name_to_id = self.ctx.location_names[self.ctx.game]
        if location_name not in location_name_to_id:
            logger.info(f"Unrecognized location {location_name}")
            return

        self.ctx.tracker_core.ignored_locations.add(location_name_to_id[location_name])
        self.ctx.updateTracker()
        logger.info(f"Added {location_name} to ignore list.")

    @mark_raw
    def _cmd_unignore(self, location_name: str = ""):
        """Stop ignoring a location so it appears in the tracker list again"""
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        location_name_to_id = self.ctx.location_names[self.ctx.game]
        if location_name not in location_name_to_id:
            logger.info(f"Unrecognized location {location_name}")
            return

        location = location_name_to_id[location_name]
        if location not in self.ctx.tracker_core.ignored_locations:
            logger.info(f"{location_name} is not on ignore list.")
            return

        self.ctx.tracker_core.ignored_locations.remove(location)
        self.ctx.updateTracker()
        logger.info(f"Removed {location_name} from ignore list.")

    def _cmd_list_ignored(self):
        """List the ignored locations"""
        if len(self.ctx.tracker_core.ignored_locations) == 0:
            logger.info("No ignored locations")
            return
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        logger.info("Ignored locations:")
        location_names = [self.ctx.location_names.lookup_in_game(location) for location in self.ctx.tracker_core.ignored_locations]
        for location_name in sorted(location_names):
            logger.info(location_name)

    def _cmd_reset_ignored(self):
        """Reset the list of ignored locations"""
        self.ctx.tracker_core.ignored_locations.clear()
        self.ctx.updateTracker()
        logger.info("Reset ignored locations.")

    def _cmd_next_progression(self):
        """Finds all items that will unlock a check immediately when collected, and a best guess of how many new checks they will unlock."""
        updateTracker(self.ctx)
        baseLocs = len(self.ctx.tracker_core.locations_available)
        counter = Counter()
        goal_items = []
        items_to_check = {item.name for item in self.ctx.tracker_core.multiworld.get_items() if item.player == self.ctx.tracker_core.player_id and item.advancement}
        for item in items_to_check:
            self.ctx.tracker_core.manual_items.append(item)
            update_ret = updateTracker(self.ctx)
            newlocs = len(self.ctx.tracker_core.locations_available) - baseLocs
            if newlocs:
                counter[item] = newlocs
            if self.ctx.tracker_core.multiworld.completion_condition[self.ctx.tracker_core.player_id](update_ret.state):
                goal_items.append(item)
            self.ctx.tracker_core.manual_items.pop()
        if not counter:
            logger.info("No item will unlock any checks right now.")
        for (item, count) in counter.most_common():
            logger.info(f"{item} unlocks {count} check{'s' if count > 1 else ''}{' (and goal)' if item in goal_items else ''}.")
        updateTracker(self.ctx)

    def _cmd_toggle_auto_tab(self):
        """Toggle the auto map tabbing function"""
        self.ctx.auto_tab = not self.ctx.auto_tab
        logger.info(f"Auto tracking currently {'Enabled' if self.ctx.auto_tab else 'Disabled'}")

    @mark_raw
    def _cmd_get_logical_path(self, dest_name: str = ""):
        """Finds a logical expected path to a particular location or region by name"""
        if not self.ctx.game:
            logger.info("Not yet loaded into a game")
            return
        if self.ctx.stored_data and "_read_race_mode" in self.ctx.stored_data and self.ctx.stored_data["_read_race_mode"]:
            logger.info("Logical Path is disabled during Race Mode")
            return
        get_logical_path(self.ctx, dest_name)
    
    @mark_raw
    def _cmd_explain(self,lookup_name:str=""):
        """Explains the rule for a location, if the world supports it"""
        if not self.ctx.game:
            logger.info("Not yet loaded into a game")
        if self.ctx.stored_data and "_read_race_mode" in self.ctx.stored_data and self.ctx.stored_data["_read_race_mode"]:
            logger.info("Explain is disabled during Race Mode")
            return
        explain(self.ctx, lookup_name)

    def _cmd_faris_asked(self):
        """Print out the error message and any other information we think might be useful"""
        print("We're in commands")
        if self.ctx.tracker_core is not None:
            logger.error(self.ctx.tracker_core.gen_error)
            if self.ctx.tracker_core.launch_multiworld is not None:
                known_slots = [f"{slot_name} ({self.ctx.tracker_core.launch_multiworld.worlds[slot_id].game})" for slot_name, slot_id in self.ctx.tracker_core.launch_multiworld.world_name_lookup.items() if self.ctx.tracker_core.launch_multiworld.worlds[slot_id].game != "Archipelago"]
                logger.error(f"Known slots = [{', '.join(known_slots)}]")
        from worlds import failed_world_loads
        if failed_world_loads:
            logger.error(f"Worlds that failed to load [{', '.join(failed_world_loads)}]")

def cmd_load_map(self: TrackerCommandProcessor, map_id: str = "0"):
    """Force a poptracker map id to be loaded"""
    if self.ctx.tracker_world is not None:
        self.ctx.load_map(map_id)
        self.ctx.updateTracker()
    else:
        logger.info("No world with internal map loaded")


def cmd_list_maps(self: TrackerCommandProcessor):
    """List the available maps to load with /load_map"""
    if self.ctx.tracker_world is not None:
        for i, map in enumerate(self.ctx.maps):
            logger.info("Map["+str(i)+"] = '"+map["name"]+"'")
    else:
        logger.info("No world with internal map loaded")


class TrackerGameContext(CommonContext):
    game = ""
    tags = CommonContext.tags | {"Tracker"}
    command_processor = TrackerCommandProcessor
    tracker_page = None
    map_page = None
    tracker_world: UTMapTabData | None = None
    coord_dict: dict[int, list] = {}
    deferred_dict: dict[str, list] = {}
    ldeferred_dict: dict[str,list] = {}
    map_page_coords_func = lambda *args: {}
    watcher_task = None
    auto_tab = True
    update_callback: Callable[[list[str]], bool] | None = None
    region_callback: Callable[[list[str]], bool] | None = None
    events_callback: Callable[[list[str]], bool] | None = None
    glitches_callback: Callable[[list[str]], bool] | None = None
    gen_error = None
    output_format = "Both"
    hide_excluded = False
    use_split = True
    re_gen_passthrough = None
    local_items: list[NetworkItem] = []

    @property
    def tracker_items_received(self):
        if not (self.items_handling & 0b010):
            return self.items_received + self.local_items
        else:
            return self.items_received

    def update_tracker_items(self):
        self.local_items = [self.locations_info[location] for location in self.checked_locations
                            if location in self.locations_info and
                            self.locations_info[location].player == self.slot]

    def scout_checked_locations(self):
        unknown_locations = [location for location in self.checked_locations
                             if location not in self.locations_info]
        if unknown_locations:
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts",
                                                 "locations": unknown_locations,
                                                 "create_as_hint": 0}]))

    def __init__(self, server_address, slot_name, password, no_connection: bool = False, print_list: bool = False, print_count: bool = False, ready_callback=None, error_callback=None):
        if no_connection:
            from worlds import network_data_package
            self.item_names = self.NameLookupDict(self, "item")
            self.location_names = self.NameLookupDict(self, "location")
            self.update_data_package(network_data_package)
        else:
            super().__init__(server_address, password)
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        self.username = slot_name
        self.items_handling = ITEMS_HANDLING
        self.quit_after_update = print_list or print_count
        self.print_list = print_list
        self.print_count = print_count
        self.location_icon = None
        self.root_pack_path = None
        self.map_id = None
        self.defered_entrance_datastorage_keys = []
        self.defered_entrance_callback = None
        self.tracker_core = TrackerCore.TrackerCore(logger,print_list,print_count)
        self.tracker_core.set_set_page(self.set_page)
        self.tracker_core.set_log_to_tab(self.log_to_tab)
        self.tracker_core.set_clear_page(self.clear_page)
        self.tracker_core.set_get_ut_color(get_ut_color)
        if self.ready_callback:
            from kivy.clock import Clock
            Clock.schedule_once(self.ready_callback, 0.1)

    def updateTracker(self) -> CurrentTrackerState:
        if self.disconnected_intentionally: return CurrentTrackerState.init_empty_state()
        self.tracker_core.set_missing_locations(self.missing_locations)
        self.tracker_core.set_items_received(self.tracker_items_received)
        hints = {}
        if f"_read_hints_{self.team}_{self.slot}" in self.stored_data:
            from NetUtils import HintStatus
            hints = { hint["location"]:hint["status"] for hint in self.stored_data[f"_read_hints_{self.team}_{self.slot}"] if hint["status"] not in [HintStatus.HINT_FOUND, HintStatus.HINT_AVOID ]and self.slot_concerns_self(hint["finding_player"]) }
        self.tracker_core.set_hints( hints)
        try:
            updateTracker_ret = self.tracker_core.updateTracker()
        except Exception as e:
            self.disconnected_intentionally = True
            async_start(self.disconnect(False), name="disconnecting")
            raise e
        if self.tracker_page:
            self.tracker_page.refresh_from_data()
        if self.update_callback is not None:
            self.update_callback(updateTracker_ret.in_logic_locations)
        if self.region_callback is not None:
            self.region_callback(updateTracker_ret.in_logic_regions)
        if self.events_callback is not None:
            self.events_callback(updateTracker_ret.events)
        if self.glitches_callback is not None:
            self.glitches_callback(updateTracker_ret.glitched_locations)
        if len(self.tracker_core.ignored_locations) > 0:
            self.log_to_tab(f"{len(self.tracker_core.ignored_locations)} ignored locations")
        if len(updateTracker_ret.in_logic_locations) == 0:
            self.log_to_tab("All " + str(len(self.checked_locations)) + " accessible locations have been checked! Congrats!")
        if self.tracker_world is not None and self.ui is not None:
            # ctx.load_map()
            for location in self.server_locations:
                relevent_coords = self.coord_dict.get(location, [])
                if not relevent_coords:
                    continue
                
                if location in self.checked_locations or location in self.tracker_core.ignored_locations:
                    status = "collected"
                elif location in self.tracker_core.locations_available:
                    status = "in_logic"
                elif location in self.tracker_core.glitched_locations:
                    status = "glitched"
                else:
                    status = "out_of_logic"
                if location in hints:
                    status = "hinted_"+status
                for coord in relevent_coords:
                    coord.update_status(location, status)
            entrance_cache = list(self.tracker_core.multiworld.regions.entrance_cache[self.tracker_core.player_id].keys())
            for entrance_name in entrance_cache:
                relevent_coords = self.deferred_dict.get(entrance_name,[])
                if not relevent_coords:
                    continue
                temp_entrance = self.tracker_core.get_current_world().get_entrance(entrance_name)
                if temp_entrance.can_reach(updateTracker_ret.state):
                    if temp_entrance.connected_region:
                        status = "passed"
                    else:
                        status = "passable"
                else:
                    status = "impassable"
                for coord in relevent_coords:
                    coord.update_status(entrance_name, status)
            event_loc_cache = [loc for loc in self.tracker_core.get_current_world().get_locations() if loc.address is None and loc.parent_region is not None]
            for loc in event_loc_cache:
                relevent_coords = self.ldeferred_dict.get(loc.name,[])
                if not relevent_coords:
                    continue
                if loc.parent_region.can_reach(updateTracker_ret.state):
                    if loc.can_reach(updateTracker_ret.state):
                        status = "passed"
                    else:
                        status = "passable"
                else:
                    status = "impassable"
                for coord in relevent_coords:
                    coord.update_status(loc.name, status)
        for entrance in updateTracker_ret.unconnected_entrances:
            self.log_to_tab("[color="+get_ut_color("unconnected")+"]"+entrance.name+"[/color]",False) #keep these at the bottom
        if self.quit_after_update:
            name = self.player_names[self.slot]
            if self.print_count:
                logger.error(f"Game: {self.game} | Slot Name : {name} | In logic locations : {len(updateTracker_ret.in_logic_locations)}")
            if self.print_list:
                for i in updateTracker_ret.readable_locations:
                    logger.error(i)
            self.exit_event.set()

        if hasattr(self, "tracker_total_locs_label"):
            self.tracker_total_locs_label.text = f"Locations: {len(self.checked_locations)}/{self.total_locations}"
        if hasattr(self, "tracker_logic_locs_label"):
            self.tracker_logic_locs_label.text = f"In Logic: {len(updateTracker_ret.in_logic_locations)}"
        if hasattr(self, "tracker_glitched_locs_label"):
            self.tracker_glitched_locs_label.text = f"Glitched: [color={get_ut_color('glitched')}]{len(updateTracker_ret.glitched_locations)}[/color]"
        if hasattr(self, "tracker_hinted_locs_label"):
            self.tracker_hinted_locs_label.text = f"Hinted: [color={get_ut_color('hinted_in_logic')}]{len(updateTracker_ret.hinted_locations)}[/color]"

        return updateTracker_ret

    def load_pack(self):
        assert self.tracker_core.player_id is not None
        assert self.tracker_world is not None
        current_world = self.tracker_core.get_current_world()
        assert current_world
        self.maps = []
        self.locs = []
        if self.tracker_world.external_pack_key:
            assert current_world.settings
            try:
                from zipfile import is_zipfile
                packRef = current_world.settings[self.tracker_world.external_pack_key]
                if packRef == "":
                    packRef = open_filename("Select Poptracker pack", filetypes=[("Poptracker Pack", [".zip"])])
                    current_world.settings[self.tracker_world.external_pack_key] = packRef
                    current_world.settings._changed = True
                if packRef:
                    if is_zipfile(packRef):
                        current_world.settings.update({self.tracker_world.external_pack_key: packRef})
                        current_world.settings._changed = True
                        for map_page in self.tracker_world.map_page_maps:
                            self.maps += load_json_zip(packRef, f"{map_page}")
                        for loc_page in self.tracker_world.map_page_locations:
                            self.locs += load_json_zip(packRef, f"{loc_page}")
                    else:
                        current_world.settings.update({self.tracker_world.external_pack_key: ""}) #failed to find a pack, prompt next launch
                        current_world.settings._changed = True
                        self.tracker_world = None
                        return
                else:
                    current_world.settings[self.tracker_world.external_pack_key] = None
                    self.tracker_world = None
                    return
            except Exception as e:
                logger.error("Selected poptracker pack was invalid")
                current_world.settings[self.tracker_world.external_pack_key] = ""
                current_world.settings._changed = True
                self.tracker_world = None
                return
        else:
            PACK_NAME = current_world.__class__.__module__
            for map_page in self.tracker_world.map_page_maps:
                self.maps += load_json(PACK_NAME, f"/{self.tracker_world.map_page_folder}/{map_page}")
            for loc_page in self.tracker_world.map_page_locations:
                self.locs += load_json(PACK_NAME, f"/{self.tracker_world.map_page_folder}/{loc_page}")
        self.load_map(None)

    def load_map(self, map_id: Union[int, str, None]):
        """REMEMBER TO RUN UPDATE_TRACKER!"""
        if not self.ui or self.tracker_world is None:
            return
        if map_id is None:
            key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
            map_id = self.tracker_world.map_page_index(self.stored_data.get(key, ""))
            if not self.auto_tab or map_id < 0 or map_id >= len(self.maps):
                return  # special case, don't load a new map
        if self.map_id is not None and self.map_id == map_id:
            return  # map already loaded
        m = None
        if isinstance(map_id, str) and not map_id.isdecimal():
            for map in self.maps:
                if map["name"] == map_id:
                    m = map
                    map_id = self.maps.index(map)
                    break
            else:
                logger.error("Attempted to load a map that doesn't exist")
                return
        else:
            if isinstance(map_id, str):
                map_id = int(map_id)
            if map_id is None or map_id < 0 or map_id >= len(self.maps):
                logger.error("Attempted to load a map that doesn't exist")
                return
            m = self.maps[map_id]
        self.map_id = map_id
        from worlds import AutoWorld
        location_name_to_id = AutoWorld.AutoWorldRegister.world_types[self.game].location_name_to_id
        # m = [m for m in self.maps if m["name"] == map_name]
        if self.tracker_world.external_pack_key:
            from zipfile import is_zipfile
            packRef = self.tracker_core.get_current_world().settings[self.tracker_world.external_pack_key]
            if packRef and is_zipfile(packRef):
                self.root_pack_path = f"ap:zip:{packRef}"
            else:
                logger.error("Player poptracker doesn't seem to exist :< (must be a zip file)")
                return
        else:
            PACK_NAME = self.tracker_core.get_current_world().__class__.__module__
            self.root_pack_path = f"ap:{PACK_NAME}/{self.tracker_world.map_page_folder}"
        self.ui.source = f"{self.root_pack_path}/{m['img']}"
        self.ui.loc_size = m["location_size"] if "location_size" in m else 65  # default location size per poptracker/src/core/map.h
        self.ui.loc_icon_size = m["location_icon_size"] if "location_icon_size" in m else self.ui.loc_size
        self.ui.loc_border = m["location_border_thickness"] if "location_border_thickness" in m else 8  # default location size per poptracker/src/core/map.h
        temp_locs = [location for location in self.locs]
        map_locs = []
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
                [location_name_to_id[section["name"]] for section in location["sections"]
                 if "name" in section and section["name"] in location_name_to_id
                 and location_name_to_id[section["name"]] in self.server_locations]

            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in location_name_to_id
                and location_name_to_id[section["name"]] in self.server_locations for section in location["sections"]
                )
        }
        poptracker_name_mapping = self.tracker_world.poptracker_name_mapping
        if poptracker_name_mapping:
            tempCoords = {  # compat coords
                (map_loc["x"], map_loc["y"]):
                    [poptracker_name_mapping[f'{location["name"]}/{section["name"]}']
                    for section in location["sections"] if "name" in section
                    and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                    and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in self.server_locations]
                for location in map_locs
                for map_loc in location["map_locations"]
                if map_loc["map"] == m["name"]
                and any("name" in section and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                        and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in self.server_locations
                        for section in location["sections"])
            }
            for maploc, seclist in tempCoords.items():
                if maploc in coords:
                    coords[maploc] += seclist
                else:
                    coords[maploc] = seclist
        entrance_cache = list(self.tracker_core.multiworld.regions.entrance_cache[self.tracker_core.player_id].keys())
        dcoords = {
            (map_loc["x"],map_loc["y"]):[section["name"] for section in location["sections"]
                if "name" in section and section["name"] in entrance_cache ]
            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in entrance_cache for section in location["sections"]
            )
        }
        poptracker_entrance_mapping = self.tracker_world.poptracker_entrance_mapping
        if poptracker_entrance_mapping:
            tempCoords = {
                (map_loc["x"],map_loc["y"]):[poptracker_entrance_mapping[section["name"]] for section in location["sections"]
                    if "name" in section and  section["name"] in poptracker_entrance_mapping and poptracker_entrance_mapping[section["name"]] in entrance_cache]
                for location in map_locs
                for map_loc in location["map_locations"]
                if map_loc["map"] == m["name"] and any(
                    "name" in section and  section["name"] in poptracker_entrance_mapping and poptracker_entrance_mapping[section["name"]] in entrance_cache for section in location["sections"]
                )
            }
            for maploc, seclist in tempCoords.items():
                if maploc in dcoords:
                    dcoords[maploc] += seclist
                else:
                    dcoords[maploc] = seclist
        event_loc_cache = [loc.name for loc in self.tracker_core.get_current_world().get_locations() if loc.address is None and loc.parent_region is not None]
        dlcoords = {
            (map_loc["x"],map_loc["y"]):[section["name"] for section in location["sections"]
                if "name" in section and section["name"] in event_loc_cache ]
            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in event_loc_cache for section in location["sections"]
            )
        }
        both_dcoords = set(entrance_cache).intersection(set(event_loc_cache))
        if both_dcoords:
            for _,temp_coord in dcoords.items():
                if both_dcoords.intersection(set(temp_coord)):
                    logger.error("Mixing of entrance and event names, map will refuse to load")
                    return
            for _,temp_coord in dlcoords.items():
                if both_dcoords.intersection(set(temp_coord)):
                    logger.error("Mixing of entrance and event names, map will refuse to load")
                    return
        self.coord_dict,self.deferred_dict,self.ldeferred_dict = self.map_page_coords_func(coords,dcoords,dlcoords,self.use_split)
        if self.tracker_world.location_setting_key:
            self.update_location_icon_coords()

    def clear_page(self):
        if self.tracker_page is not None:
            self.tracker_page.resetData()

    def set_page(self, line: str):
        if self.tracker_page is not None:
            self.tracker_page.data = [{"text": line}]

    def log_to_tab(self, line: str, sort: bool = False):
        if self.tracker_page is not None:
            self.tracker_page.addLine(line, sort)

    def set_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.update_callback = func

    def set_region_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.region_callback = func

    def set_events_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.events_callback = func

    def set_glitches_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.glitches_callback = func

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TrackerGameContext, self).server_auth(password_requested)

        await self.get_username()
        if "Tracker" in self.tags:
            await self.send_connect(game="")
        else:
            await self.send_connect()

    def run_generator(self):
        self.tracker_core.run_generator(None, None)
        self.use_split = self.tracker_core.use_split #fancy hack

    def on_package(self, cmd: str, args: dict):
        try:
            if cmd == 'Connected':
                self.game = args["slot_info"][str(args["slot"])][1]
                slot_name = args["slot_info"][str(args["slot"])][0]
                self.tracker_core.set_slot_params(self.game,self.slot,slot_name,self.team)
                connected_cls = AutoWorld.AutoWorldRegister.world_types.get(self.game)
                if connected_cls is None:
                    self.log_to_tab(f"Connected to World {self.game} but that world is not installed")
                    return
                if self.checksums[self.game] != connected_cls.get_data_package_data()["checksum"]:
                    logger.warning("*****\nWarning: the local datapackage for the connected game does not match the server's datapackage\n*****")
                self.tracker_core.initalize_tracker_core(connected_cls,args["slot_data"])

                if self.ui is not None and hasattr(connected_cls, "tracker_world"):
                    self.tracker_world = UTMapTabData(self.slot, self.team, **connected_cls.tracker_world)
                    self.load_pack()
                    if self.tracker_world:  # don't show the map if loading failed
                        self.ui.show_map = True
                        if self.tracker_world.map_page_index:
                            key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
                            self.set_notify(key)
                        icon_key = self.tracker_world.location_setting_key
                        if icon_key:
                            self.set_notify(icon_key)
                else:
                    self.tracker_world = None
                if self.tracker_world:
                    if "load_map" not in self.command_processor.commands or not self.command_processor.commands["load_map"]:
                        self.command_processor.commands["load_map"] = cmd_load_map
                    if "list_maps" not in self.command_processor.commands or not self.command_processor.commands["list_maps"]:
                        self.command_processor.commands["list_maps"] = cmd_list_maps
                self.defered_entrance_datastorage_keys = getattr(self.tracker_core.get_current_world(),"found_entrances_datastorage_key",None)
                if self.defered_entrance_datastorage_keys:
                    if isinstance(self.defered_entrance_datastorage_keys,str):
                        self.defered_entrance_datastorage_keys = [self.defered_entrance_datastorage_keys]
                    self.defered_entrance_datastorage_keys = [key.format(player=self.slot, team=self.team) for key in self.defered_entrance_datastorage_keys]
                    self.defered_entrance_callback = getattr(self.tracker_core.get_current_world(),"reconnect_found_entrances",None)
                    if not self.defered_entrance_callback or not callable(self.defered_entrance_callback):
                        self.defered_entrance_callback = None
                        self.defered_entrance_datastorage_keys = []
                    else:
                        self.set_notify(*self.defered_entrance_datastorage_keys)
                else:
                    self.defered_entrance_datastorage_keys = []

                if not (self.items_handling & 0b010):
                    self.scout_checked_locations()

                if not self.quit_after_update:
                    self.updateTracker()
                else:
                    asyncio.create_task(wait_for_items(self),name="UT Delay function") #if we don't get new items, delay for a bit first
                self.watcher_task = asyncio.create_task(game_watcher(self), name="GameWatcher") #This shouldn't be needed, but technically 
            elif cmd == 'RoomUpdate':
                if not (self.items_handling & 0b010):
                    self.scout_checked_locations()
                self.updateTracker()
            elif cmd == 'SetReply' or cmd == 'Retrieved':
                from worlds import AutoWorld
                if self.ui is not None and hasattr(AutoWorld.AutoWorldRegister.world_types.get(self.game), "tracker_world") and self.tracker_world:
                    key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
                    icon_key = self.tracker_world.location_setting_key
                    if "key" in args:
                        if args["key"] == key:
                            self.load_map(None)
                            self.updateTracker()
                        elif args["key"] == icon_key:
                            self.update_location_icon_coords()
                    elif "keys" in args:
                        if icon_key in args["keys"]:
                            self.update_location_icon_coords()
                if self.defered_entrance_datastorage_keys:
                    if "key" in args and args["key"] in self.defered_entrance_datastorage_keys:
                            self.update_defered_entrances(args["key"])
                    elif "keys" in args:
                        for key in self.defered_entrance_datastorage_keys:
                            if key in args["keys"]:
                                self.update_defered_entrances(key)
            elif cmd == 'LocationInfo':
                if not (self.items_handling & 0b010):
                    self.update_tracker_items()
                    self.updateTracker()
        except Exception as e:
            e.args = e.args+("This is likely a UT error, make sure you have the correct tracker.apworld version and no duplicates",
                             "Then try to reproduce with the debug launcher and post in the Discord channel")
            self.disconnected_intentionally = True
            raise e
        
    def update_location_icon_coords(self):
        icon_key = self.tracker_world.location_setting_key
        temp_ret = self.tracker_world.location_icon_coords(self.map_id,self.stored_data.get(icon_key, ""))
        if temp_ret:
            (x,y,ref) = temp_ret #should be a 3-tuple
            if x < 0 or y < 0:
                self.location_icon.size = (0,0)
            else:
                self.ui.iconSource = f"{self.root_pack_path}/{ref}"
                self.location_icon.size = (self.ui.loc_icon_size, self.ui.loc_icon_size)
                self.location_icon.pos = (x,y)

    def update_defered_entrances(self,key):
        if self.defered_entrance_callback and key:
            self.defered_entrance_callback(key,self.stored_data.get(key,None))
            self.updateTracker()

    async def disconnect(self, allow_autoreconnect: bool = False):
        if "Tracker" in self.tags:
            self.game = ""
            if self.ui:
                self.ui.show_map = False
            if self.tracker_world:
                if "load_map" in self.command_processor.commands:
                    self.command_processor.commands["load_map"] = None
                if "list_maps" in self.command_processor.commands:
                    self.command_processor.commands["list_maps"] = None
                self.map_id = None
                self.root_pack_path = None
                self.coord_dict.clear()
                self.deferred_dict.clear()
                self.ldeferred_dict.clear()
            self.tracker_world = None
            self.defered_entrance_callback = None
            self.defered_entrance_datastorage_keys = []
            # TODO: persist these per url+slot(+seed)?
            self.tracker_core.ignored_locations.clear()
            self.set_page("Connect to a slot to start tracking!")
            if hasattr(self, "tracker_total_locs_label"):
                self.tracker_total_locs_label.text = f"Locations: 0/0"
            if hasattr(self, "tracker_logic_locs_label"):
                self.tracker_logic_locs_label.text = f"In Logic: 0"
            if hasattr(self, "tracker_glitched_locs_label"):
                self.tracker_glitched_locs_label.text = f"Glitched: [color={get_ut_color('glitched')}]0[/color]"
            if hasattr(self, "tracker_hinted_locs_label"):
                self.tracker_hinted_locs_label.text = f"Hinted: [color={get_ut_color('hinted_in_logic')}]0[/color]"
            self.tracker_core.disconnect()
        self.local_items.clear()

        await super().disconnect(allow_autoreconnect)





def load_json(pack, path):
    import pkgutil
    import json
    return json.loads(pkgutil.get_data(pack, path).decode('utf-8-sig'))


def load_json_zip(pack, path):
    import json
    import zipfile
    with zipfile.ZipFile(pack) as parentFile:
        with parentFile.open(path) as childFile:
            return json.loads(childFile.read().decode('utf-8-sig'))

def explain(ctx: TrackerGameContext, dest_name: str):
    from NetUtils import JSONMessagePart
    if ctx.tracker_core.player_id is None or ctx.tracker_core.multiworld is None:
        logger.error("Player YAML not installed or Generator failed")
        ctx.set_page(f"Check Player YAMLs for error; Tracker {UT_VERSION} for {apname} version {__version__}")
        return
    current_world = ctx.tracker_core.get_current_world()
    assert current_world
    state = ctx.updateTracker().state
    if not state: return

    if hasattr(current_world,"explain_rule"):
        returned_json = current_world.explain_rule(dest_name,state)
        if returned_json:
            ctx.ui.print_json(returned_json)
            return
    parent_region = None
    location = None
    if dest_name in ctx.tracker_core.multiworld.regions.location_cache[ctx.tracker_core.player_id]:
        dest_id = current_world.location_name_to_id[dest_name]
        if dest_id not in ctx.server_locations:
            logger.error("Location not found")
            return
        location = ctx.tracker_core.multiworld.get_location(dest_name, ctx.tracker_core.player_id)
        if hasattr(location.access_rule,"explain_json"):
            ctx.ui.print_json(location.access_rule.explain_json(state))
        elif location.access_rule is Location.access_rule:
            logger.info("Location has a default access rule")
        else:
            logger.info("Location doesn't have a rule that supports explanation")
        parent_region = location.parent_region
    elif dest_name in ctx.tracker_core.multiworld.regions.region_cache[ctx.tracker_core.player_id]:
        parent_region = ctx.tracker_core.multiworld.get_region(dest_name,ctx.tracker_core.player_id)
    else:
        from Utils import get_fuzzy_results
        results = get_fuzzy_results(dest_name,set(ctx.tracker_core.multiworld.regions.location_cache[ctx.tracker_core.player_id].keys()).union(set(ctx.tracker_core.multiworld.regions.region_cache[ctx.tracker_core.player_id].keys())),limit=1)[0]
        logger.error(f"Did you mean '{results[0]}' ({results[1]}% sure)? ")
        return
    if parent_region:
        if location:
            logger.info(f"Parent region ({parent_region.name})")
        for entrance in parent_region.entrances:
            if entrance.parent_region:
                if hasattr(entrance.access_rule,"explain_json"):
                    returned_json:list[JSONMessagePart] = [{"type":"text","text":f"{entrance.parent_region.name} ({entrance.parent_region.can_reach(state)}): {entrance.name} : "}]
                    returned_json.extend(entrance.access_rule.explain_json(state))
                    ctx.ui.print_json(returned_json)
                else:
                    ctx.ui.print_json([{"type":"text","text":f"{entrance.parent_region.name} ({entrance.parent_region.can_reach(state)}): {entrance.name} : {entrance.access_rule(state)}"}])
        

def get_logical_path(ctx: TrackerGameContext, dest_name: str):
    if ctx.tracker_core.player_id is None or ctx.tracker_core.multiworld is None:
        logger.error("Player YAML not installed or Generator failed")
        ctx.set_page(f"Check Player YAMLs for error; Tracker {UT_VERSION} for {apname} version {__version__}")
        return
    relevent_region = None
    state = None
    current_world = ctx.tracker_core.get_current_world()
    assert current_world

    if hasattr(current_world,"get_logical_path"):
        state = ctx.updateTracker().state
        returned_json = current_world.get_logical_path(dest_name,state)
        if returned_json:
            ctx.ui.print_json(returned_json)
            return

    if dest_name in [loc.name for loc in ctx.tracker_core.multiworld.get_locations(ctx.tracker_core.player_id)]:
        location = ctx.tracker_core.multiworld.get_location(dest_name, ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if location.can_reach(state):
            relevent_region = location.parent_region
    elif dest_name in ctx.tracker_core.multiworld.regions.region_cache[ctx.tracker_core.player_id]:
        relevent_region = ctx.tracker_core.multiworld.get_region(dest_name,ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if not relevent_region.can_reach(state):
            relevent_region = None
    elif dest_name in ctx.tracker_core.multiworld.regions.location_cache[ctx.tracker_core.player_id]:
        location = ctx.tracker_core.multiworld.get_location(dest_name,ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if location.can_reach(state):
            relevent_region = location.parent_region
    else:
        logger.info(f"{dest_name} not found in the multiworld")

    if state:
        if relevent_region:
            # stolen from core
            from BaseClasses import Region
            from typing import Tuple, Iterator
            from itertools import zip_longest

            def flist_to_iter(path_value) -> Iterator[str]:
                while path_value:
                    region_or_entrance, path_value = path_value
                    yield region_or_entrance

            def get_path(state: CollectionState, region: Region) -> list[Union[Tuple[str, str], Tuple[str, None]]]:
                reversed_path_as_flist = state.path.get(region, (str(region), None))
                string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
                # Now we combine the flat string list into (region, exit) pairs
                pathsiter = iter(string_path_flat)
                pathpairs = zip_longest(pathsiter, pathsiter)
                return list(pathpairs)

            paths = get_path(state=state, region=relevent_region)
            for k, v in paths:
                if v:
                    logger.info(v)
        else:
            logger.info(f"{dest_name} not in logic")

async def game_watcher(ctx: TrackerGameContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            continue
        ctx.watcher_event.clear()
        try:
            ctx.updateTracker()
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            logger.error("".join(traceback.format_exception_only(sys.exception())))
            raise e

async def wait_for_items(ctx: TrackerGameContext)-> None:
    try:
        await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
    except asyncio.TimeoutError:
        ctx.updateTracker() #if it timed out, we need to manually trigger this
        #if it didn't, then game_watcher will handle it

def launch(server_address: str = None, slot_name: str = None, password: str = None, ready_callback=None, error_callback=None, 
          print_count: bool = False, print_list: bool = False):
    """
    Launch the client
    """
    import logging
    logging.getLogger("TrackerClient")

    async def main():
        ctx = TrackerGameContext(server_address, slot_name, password, print_count=print_count, print_list=print_list, 
                               ready_callback=ready_callback, error_callback=error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | Universal Tracker"
        ctx.auth = slot_name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        await ctx.server_auth()
        
        ctx.run_generator()

        await ctx.exit_event.wait()
        await ctx.shutdown()


def launch(*args):
    parser = get_base_parser(description=f"Gameless {apname} Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--count', default=False, action='store_true', help="just return a count of in logic checks")
        parser.add_argument('--list', default=False, action='store_true', help="just return a list of in logic checks")
    parser.add_argument("url", nargs="?", help=f"{apname} connection url")
    args = handle_url_arg(parser.parse_args(args))


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, 
         slot_name: str = None, print_count: bool = False, print_list: bool = False):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, slot_name, password, ready_callback, error_callback, slot_name, print_count, print_list)


if __name__ == "__main__":
    launch(*sys.argv[1:])
