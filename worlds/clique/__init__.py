from typing import Callable

from BaseClasses import CollectionState, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from .items import CliqueItem, item_data
from .locations import CliqueLocation, location_table, location_table
from .options import CliqueOptions
()

class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Clique.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Phar"]
    )

    setup_de = Tutorial(
        tutorial_name="Anleitung zum Anfangen",
        description="Eine Anleitung um Clique zu spielen.",
        language="Deutsch",
        file_name="guide_de.md",
        link="guide/de",
        authors=["Held_der_Zeit"]
    )
    
    tutorials = [setup_en, setup_de]
    game_info_languages = ["en", "de"]


class CliqueWorld(World):
    """The greatest game of all time."""

    game = GAME_NAME
    author: str = AUTHOR
    
    web = CliqueWebWorld()
    options: CliqueOptions
    options_dataclass = CliqueOptions
    location_name_to_id = location_table
    item_name_to_id = {name: data.code for name, data in item_data.items()}

    def create_item(self, name: str) -> CliqueItem:
        return CliqueItem(name, item_data[name].type, item_data[name].code, self.player)

    def create_items(self) -> None:
        item_pool: list[CliqueItem] = [self.create_item("Feeling of Satisfaction")]
        if self.options.hard_mode:
            item_pool.append(self.create_item("Button Activation"))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        region = Region("Menu", self.player, self.multiworld)
        region.add_locations({"The Button": 69696969}, CliqueLocation)
        if self.options.hard_mode:
            region.add_locations({"The Free Item": 69696968}, CliqueLocation)

        # Set priority location for the Button!
        if self.options.force_progression:
            self.options.priority_locations.value.add("The Button")

        self.multiworld.regions.append(region)

    def get_filler_item_name(self) -> str:
        return "A Cool Filler Item (No Satisfaction Guaranteed)"

    def set_rules(self) -> None:
        def get_button_rule(world: "CliqueWorld") -> Callable[[CollectionState], bool]:
            if world.options.hard_mode:
                return lambda state: state.has("Button Activation", world.player)

            return lambda state: True

        self.get_location("The Button").access_rule = get_button_rule(self)

        # Completion condition.
        self.multiworld.completion_condition[self.player] = get_button_rule(self)

    def fill_slot_data(self) -> dict:
        return {
            # fmt: off
            "world_version":    1,
            "hard_mode":        bool(self.options.hard_mode),
            "color":            self.options.color.current_key,
            # fmt: on
        }
