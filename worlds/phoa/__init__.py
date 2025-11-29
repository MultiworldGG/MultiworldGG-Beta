from typing import List, Dict
from BaseClasses import Tutorial, ItemClassification, Item
from worlds.AutoWorld import WebWorld, World
from .Options import PhoaOptions
from .Locations import PhoaLocation, get_location_data
from .Items import PhoaItem, item_table, get_item_data, PhoaItemData
from .Regions import create_regions_and_locations


class PhoaWebWorld(WebWorld):
    tutorials = [Tutorial(
        tutorial_name="Start Guide",
        description="A guide to start playing Phoenotopia: Awakening in MultiworldGG",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Lenamphy"]
    )]


class PhoaWorld(World):
    """
    Phoenotopia: Awakening is a 2020 action-adventure game, remaking the original flash game, a 2D side-scrolling action adventure in a post-apcalyptic fictional world.
    """
    game = "Phoenotopia: Awakening"
    web = PhoaWebWorld()
    options: PhoaOptions
    options_dataclass = PhoaOptions
    location_name_to_id = {data.region + " - " + name: data.address for name, data in
                           get_location_data(-1, None).items()}
    item_name_to_id = {name: data.code for name, data in get_item_data(None).items()}

    def create_item(self, name: str) -> PhoaItem:
        return PhoaItem(name, item_table[name].type, item_table[name].code, self.player)

    def create_items(self) -> None:
        self.create_and_assign_event_items()
        included_items: Dict[str, PhoaItemData] = get_item_data(self.options)

        item_pool: List[PhoaItem] = []
        for name, item in included_items.items():
            if item.code:
                for _ in range(item.amount):
                    item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        create_regions_and_locations(self.multiworld, self.player, self.options)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "Anuri Temple - Strange Urn", self.player
        )

    def get_filler_item_name(self) -> str:
        return '20 Rin'

    def create_and_assign_event_items(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.address is None:
                location.place_locked_item(Item(location.name, ItemClassification.progression, None, self.player))

    def fill_slot_data(self):
        return {
            "DeathLink": self.options.death_link.value,
        }
