from typing import Dict, Any

from BaseClasses import CollectionState, Item, MultiWorld, Region
from worlds.AutoWorld import LogicMixin, World
from .items import item_table

class DebugWorld(World):
    """A minimal debug world with only a few items for testing purposes."""
    game = "debug"
    author = "TreZ"
    hidden = True
    location_name_to_id = {}
    item_name_to_id = item_table
    origin_region_name = "TestRegion"
    item_name_groups = {
        "Progression": frozenset({"TestItem1","TestItem3","TestItem6","TestItem9"}),
        "Useful": frozenset({"TestItem2","TestItem4","TestItem10"}),
        "Filler": frozenset({"TestItem5","TestItem8"}),
        "OddsAndEnds": frozenset({"TestItem7"}),
    }
    
    def create_item(self, name: str) -> "DebugItem":
        item = DebugItem(name, self.player)
        return item

    def create_items(self) -> None:
        items_to_create = [
            "TestItem1", "TestItem2", "TestItem3", "TestItem4", "TestItem5",
            "TestItem6", "TestItem7", "TestItem8", "TestItem9", "TestItem10"
        ]
        self.multiworld.itempool += [self.create_item(item) for item in items_to_create]

    def create_regions(self) -> None:
        test_region = Region("TestRegion", self.player, self.multiworld)
        self.multiworld.regions += [test_region]

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"version": "1.0.0"}


class DebugItem(Item):
    game = "debug"


class DebugState(LogicMixin):
    pass
