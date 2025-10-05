from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Regions import create_regions

from .Locations import create_locations, location_table
from .Items import create_items, item_table

class ChainedEchoesWeb(WebWorld):
    rich_text_options_doc = True
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Chained Echoes on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SergioAlonso"]
    )

    tutorials = [setup_en]

class ChainedEchoesWorld(World):
    """
    Chained Echoes world integration for MultiworldGG.
    Regions and locations are created in `create_regions` (including a call to `create_locations`).
    Items are created in `create_items`.
    """

    from BaseUtils import get_archipelago_json
    GAME_NAME, AUTHOR, AP_VERSION, WORLD_VERSION = get_archipelago_json("chainedechoes")

    game = GAME_NAME
    author: str = AUTHOR
    
    location_name_to_id = location_table
    item_name_to_id = item_table
    topology_present = True

    web = ChainedEchoesWeb()
    
    def create_regions(self):
        """
        Creates regions and locations for the world.
        `create_regions` internally calls `create_locations`.
        """
        create_regions(self)
        create_locations(self)

    def create_items(self):
        """
        Populates the item pool with items for the world.
        """
        create_items(self)