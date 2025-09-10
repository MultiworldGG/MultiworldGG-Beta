import random

from BaseClasses import Region, MultiWorld, ItemClassification
from .Locations import LocationDict, PathOfExileLocation, base_item_type_locations, acts, get_lvl_location_name_from_lvl
from .Rules import can_reach
from . import Items
from . import Locations

import typing
if typing.TYPE_CHECKING:
    from worlds.poe import PathOfExileWorld
    from . import PathOfExileOptions

import logging
logger = logging.getLogger("poe.Regions")

def create_and_populate_regions(world: "PathOfExileWorld", multiworld: MultiWorld, player: int, locations: list[LocationDict] = base_item_type_locations, act_regions=acts) -> list[Region]:
    opt: PathOfExileOptions = world.options
    locations: list[LocationDict] = locations.copy()
    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    regions = []
    last_region = menu
    for act in act_regions:
        region_name = ""
        maps_region = False
        if act["act"] == 0.2:
            region_name = "early act 1"
        elif act["act"] == 11:
            region_name = "Maps"
            maps_region = True
        else:
            region_name = f"Act {act['act']}"
        
        region = Region(region_name, player, multiworld)
        entrance_logic = lambda state, act=act["act"]: can_reach(act, world, state)
        last_region.connect(region, rule=entrance_logic)
        region.connect(last_region, rule=entrance_logic)
        multiworld.regions.append(region)
        last_region = region

        if maps_region and len(world.bosses_for_goal) > 0:
            for boss in world.bosses_for_goal:
                location_name = f"Defeat {boss}"
                # Fix: Use 'id' as a string key
                boss_id = Locations.bosses.get(boss, {}).get('id', None)
                locationObj = PathOfExileLocation(player, location_name, parent=region, address=boss_id)
                region.locations.append(locationObj)
                item = Items.PathOfExileItem(f"complete {boss}", ItemClassification.skip_balancing, boss_id, player)
                locationObj.place_locked_item(item)


        for i, loc in enumerate(locations):
            if loc != "used" and (\
            loc.get("dropLevel", 9001) <= act["maxMonsterLevel"] or #9001 is just a big number to default to
            loc.get("level", 9001) <= act["maxMonsterLevel"]):
                #is_level = loc.get("baseItem") is None
                location_name = loc["name"]

                locationObj = PathOfExileLocation(player, location_name, parent=region, address=loc["id"])
                try:
                    region.locations.append(locationObj)
                except:
                    logger.error("[ERROR] Failed to add location to region. Location might already exist.")
                locations[i] = "used"  # Mark the location as used to avoid duplicates
            # act=act["act"] -- this is used to pass the act number to the can_reach function, otherwise it would be the last act number.

    return regions

class PathOfExileRegion(Region):
    def can_reach(self, state):
        return super().can_reach(state) and can_reach(self.act, self, state)
