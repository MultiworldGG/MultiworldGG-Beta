import math
from typing import Dict, Any, Union, ClassVar, Final
from .Locations import locations, columns
from .Items import PPDSItem, item_table, create_items
()
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Location, Region, LocationProgressType, Tutorial
from settings import Group, Bool

uuid_offset = 0x0BF6E0BB

class PPDSWebWorld(WebWorld):
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Placid Plastic Duck Simulator in MultiworldGG.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["SW_CreeperKing"]
    )

    tutorials = [setup_en]


class PlacidPlasticDuckSimulator(World):
    """A game about funny ducks in a pool"""
    game = GAME_NAME
    
    author: str = AUTHOR
    web = PPDSWebWorld()
    location_name_to_id = {name: uuid_offset + id_offset for name, id_offset in locations.items()}
    item_name_to_id = {name: uuid_offset + data.id_offset for name, data in item_table.items()}
    locations_to_fill = 0

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        last_region = menu_region

        for column in range(len(columns)):
            next_region = Region(f"Duck Column {column}", self.player, self.multiworld)
            self.multiworld.regions.append(next_region)

            if column > 0:
                last_region.connect(next_region, rule=lambda state, progression_req=column: \
                    state.has("Progressive Column Unlock", self.player, progression_req))
            else:
                last_region.connect(next_region)
            last_region = next_region

            for duck in columns[column]:
                self.locations_to_fill += 1
                location = Location(self.player, duck, self.location_name_to_id[duck], last_region)
                last_region.locations.append(location)

        self.multiworld.regions.append(menu_region)

    def create_item(self, name: str) -> PPDSItem:
        item = item_table[name]
        return PPDSItem(name, item.type, item.id_offset + uuid_offset, self.player)

    def create_items(self) -> None:
        create_items(self)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Progressive Column Unlock", self.player, 9)
