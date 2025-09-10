from .items import RoR1Item, item_table, map_offset
from .Constants import GAME_NAME, AUTHOR, IGDB_ID
from .locations import RoR1Location, item_pickups, get_locations, map_orderedstages_table, map_table, shift_by_offset
from .options import ROROptions
from .rules import set_rules
from .regions import create_universal_regions, create_grouped_regions

from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, ItemClassification, Tutorial
from typing import List, Dict, Any

class RiskOfWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Risk of Rain 1 integration for MultiworldGG multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["studkid"]
    )]

class RoR1World(World):
    """
    Risk of Rain is a 2013 roguelike platform game developed by Hopoo Games. Players control the survivor of a space freighter crash on a strange planet. 
    They attempt to survive by killing monsters and collecting items that can boost their offensive and defensive abilities. 
    """
    game = GAME_NAME
    igdb_id = IGDB_ID
    author: str = AUTHOR
    options_dataclass = ROROptions
    options: ROROptions
    web = RiskOfWeb()
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    item_name_groups = {
        "Stages": {name for name, data in item_table.items() if data.category == "Stage"},
        "Maps": {name for name, data in item_table.items() if data.category == "Maps"},
        "Upgrades": {name for name, data in item_table.items() if data.category == "Upgrade"},
        "Fillers": {name for name, data in item_table.items() if data.category == "Filler"},
        "Traps": {name for name, data in item_table.items() if data.category == "Trap"},
    }
    location_name_to_id = item_pickups

    data_version = 8
    required_client_version = (0, 5, 0)

    fragAmount = 0
    requiredFragAmount = 0

    def create_regions(self) -> None:
        if self.options.grouping == "universal":
            create_universal_regions(self)
        else:
            create_grouped_regions(self)

        self.create_events()

    def create_items(self) -> None:
        maps_pool = {}

        if self.options.grouping == "map":
            maps_pool = shift_by_offset(map_table, map_offset)
            unlock = self.random.choices(list(map_orderedstages_table[0].keys()), k=1)
            self.multiworld.push_precollected(self.create_item(unlock[0]))
            self.multiworld.push_precollected(self.create_item("Stage 1"))
            maps_pool.pop(unlock[0])
            if not self.options.require_stage:
                self.multiworld.push_precollected(self.create_item("Stage 2"))
                self.multiworld.push_precollected(self.create_item("Stage 3"))
                self.multiworld.push_precollected(self.create_item("Stage 4"))
                self.multiworld.push_precollected(self.create_item("Stage 5"))
        # elif self.options.grouping == "stage":
        #     self.multiworld.push_precollected(self.create_item("Stage 1"))
        
        itempool: List[str] = []

        for map_name, _ in maps_pool.items():
            itempool += [map_name]
        
        if self.options.grouping == "universal":
            total_locations = self.options.total_locations.value
        else:
            if self.options.require_stage:
                if not self.options.progressive_stages:
                    itempool += ["Stage 2", "Stage 3", "Stage 4", "Stage 5"]
                else:
                    itempool += ["Progressive Stage"] * 4

                
            total_locations = len(
                get_locations(
                    chests=self.options.total_locations.value,
                )
            )

        if self.options.required_frags.value > 0 and self.options.available_frags.value > 0:
            fillerSize = total_locations - len(itempool)
            self.fragAmount = round(fillerSize * (self.options.available_frags / 100))
            self.requiredFragAmount = round(self.fragAmount * (self.options.required_frags / 100))
            itempool += ["Teleporter Fragment"] * self.fragAmount
            
        junk_pool = self.create_junk_pool()
        filler = self.random.choices(*zip(*junk_pool.items()), k = total_locations - len(itempool))
        itempool.extend(filler)

        self.multiworld.itempool += map(self.create_item, itempool)

    def create_junk_pool(self) -> Dict[str, int]:
        # if presets are enabled generate junk_pool from the selected preset
        junk_pool: Dict[str, int] = {}
        junk_pool = {
            "Common Item": self.options.common_item.value,
            "Uncommon Item": self.options.uncommon_item.value,
            "Legendary Item": self.options.legendary_item.value,
            "Boss Item": self.options.boss_item.value,
            "Equipment": self.options.equipment.value,
            "Money": self.options.money.value,
            "1000 Exp": self.options.experience.value,
            "Time Warp Trap": self.options.time_warp_trap.value,
            "Combat Trap": self.options.combat_trap.value,
            "Meteor Trap": self.options.meteor_trap.value,
        }

        if not self.options.enable_trap:
            junk_pool.pop("Time Warp Trap")
            junk_pool.pop("Combat Trap")
            junk_pool.pop("Meteor Trap")

        return junk_pool

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return RoR1Item(name, data.item_type, data.code, self.player)
    
    def set_rules(self) -> None:
        set_rules(self)
    
    def fill_slot_data(self) -> Dict[str, Any]:
        options_dict = self.options.as_dict("grouping", "total_locations", "item_pickup_step",
                                            "stage_five_tp", "strict_stage_prog", "progressive_stages", casing="camel")
        options_dict["requiredFrags"] = self.requiredFragAmount
        return {
            **options_dict,
        }
    
    def create_events(self) -> None:
        total_locations = self.options.total_locations.value
        num_of_events = total_locations // 25
        if total_locations / 25 == num_of_events:
            num_of_events -= 1
        world_region = self.multiworld.get_region("Contact Light", self.player)
        if self.options.grouping == "universal":
            # universal pickups
            for i in range(num_of_events):
                event_loc = RoR1Location(self.player, f"Pickup{(i + 1) * 25}", None, world_region)
                event_loc.place_locked_item(
                    RoR1Item(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None,
                                   self.player))
                event_loc.access_rule = \
                    lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", "Location", self.player)
                world_region.locations.append(event_loc)
        else:
            # stage and map pickups
            event_region = self.multiworld.get_region("OrderedStage_6", self.player)
            event_loc = RoR1Location(self.player, "OrderedStage_6", None, event_region)
            event_loc.place_locked_item(RoR1Item("OrderedStage_6", ItemClassification.progression, None, self.player))
            event_loc.show_in_spoiler = False
            event_region.locations.append(event_loc)
            event_loc.access_rule = lambda state: state.has("Temple of the Elders", self.player)

        victory_region = self.multiworld.get_region("Victory", self.player)
        victory_event = RoR1Location(self.player, "Victory", None, victory_region)
        victory_event.place_locked_item(RoR1Item("Victory", ItemClassification.progression, None, self.player))
        victory_region.locations.append(victory_event)