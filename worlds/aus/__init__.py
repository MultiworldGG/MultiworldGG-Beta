from .Regions import link_aus_areas, aus_regions

from BaseClasses import Region, Entrance, Tutorial, Item
from .Options import AUSOptions
from .Items import item_table, AUSItem, item_pool
from .Locations import full_location_table, AUSLocation
from .Rules import AUSRules
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type
from multiprocessing import Process
from .Names import *

class AnUntitledStoryWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the An Untitled Story randomizer for MultiworldGG.",
            "English",
            "setup_en.md",
            "setup/en",
            ["ThatOneGuy27"],
        )
    ]
class AUSWorld(World):
    """
    A freeware metroidvania game created by Maddy Thorson chronicling the travels of an adventurous egg.
    """

    from BaseUtils import get_archipelago_json
    GAME_NAME, AUTHOR, AP_VERSION, WORLD_VERSION = get_archipelago_json("aus")

    game = GAME_NAME
    author: str = AUTHOR
    
    options_dataclass = AUSOptions
    options: AUSOptions
    topology_present = False

    base_id = 72000
    web = AnUntitledStoryWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in full_location_table.items()}

    def _get_aus_data(self):
        return {
            "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
        }

    def create_items(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            for amount in range(item_pool.get(name, 1)):
                if name != VICTORY:
                    item = AUSItem(name, data.classification, data.code, self.player)
                    pool.append(item)

        self.multiworld.itempool += pool

    def create_regions(self):
        def AUSRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [AUSLocation(self.player, loc_name, loc_data.id, ret)
                             for loc_name, loc_data in full_location_table.items()
                             if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [AUSRegion(*r) for r in aus_regions]
        link_aus_areas(self.multiworld, self.player)

        self.multiworld.get_location(VICTORY, self.player).place_locked_item(self.create_item(VICTORY))

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = AUSItem(name, item_data.classification, item_data.code, self.player)
        return item

    def set_rules(self) -> None:
        AUSRules(self).set_aus_rules()

    def get_filler_item_name(self) -> str:
        # I think this might crash? There's no item named this. -Bunne
        return "A cool rock"