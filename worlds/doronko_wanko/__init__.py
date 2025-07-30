import settings
import typing
from .options import DoronkoWankoOptions  # the options we defined earlier
from .Constants import GAME_NAME, AUTHOR, IGDB_ID
from .items import doronko_wanko_items  # data used below to add items to the World
from .items import base_id as items_base_id
from .items import group_table as items_groups
from .locations import doronko_wanko_locations  # same as above
from .locations import base_id as loc_base_id
from .locations import group_table as loc_groups
from .rules import create_rules, can_get_all_badges, can_get_all_paintings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification


class DoronkoWankoWeb(WebWorld):
    theme = "dirt"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the DORONKO WANKO randomizer connected to a MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Vendily"]
    )]


class DoronkoWankoItem(Item):  # or from Items import MyGameItem
    game = GAME_NAME  # name of the game/world this item is from


class DoronkoWankoLocation(Location):  # or from Locations import MyGameLocation
    game = GAME_NAME  # name of the game/world this location is in



class DoronkoWankoWorld(World):
    """
    DORONKO WANKO is a DORONKO Action Game. In this game, you can become a cute, innocent Pomeranian, make your master's home messy and dirty.
    """
    game = GAME_NAME  # name of the game/world
    author: str = AUTHOR
    igdb_id = IGDB_ID
    options_dataclass = DoronkoWankoOptions  # options the player can set
    options: DoronkoWankoOptions  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler
    web = DoronkoWankoWeb()
    item_name_to_id = {item["name"]: item["id"] for item in doronko_wanko_items}
    location_name_to_id = {loc["name"]: loc["id"] for loc in doronko_wanko_locations}
    item_name_groups = items_groups
    location_name_groups = loc_groups

    def get_filler_item_name(self) -> str:
        return ["P$10 Damage","P$100 Damage","P$250 Damage","P$500 Damage"][self.options.filler_damage_amount.value]

    def create_regions(self) -> None:
        # Add regions to the multiworld. One of them must use the origin_region_name as its name ("Menu" by default).
        # Arguments to Region() are name, player, multiworld, and optionally hint_text
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        regions = {
            "House": Region("House", self.player, self.multiworld),
            "Train": Region("Train", self.player, self.multiworld),
            "Mom": Region("Mom", self.player, self.multiworld),
            "Fixed Train":Region("Fixed Train", self.player, self.multiworld),
            "Gold Statue":Region("Gold Statue", self.player, self.multiworld),
            "12 Paintings":Region("12 Paintings", self.player, self.multiworld)

        }
        # add main area's locations to main area (all but goal room)
        for loc in self.location_name_to_id.keys():
            loc_id: int = self.location_name_to_id[loc]
            id = loc_id - loc_base_id - 1
            region = regions[doronko_wanko_locations[id].get("region","House")]
            location = DoronkoWankoLocation(self.player, loc, self.location_name_to_id[loc], region)
            region.locations.append(location)
        regions["House"].locations.append(DoronkoWankoLocation(self.player, "12/12 Paintings", None, regions["House"]))
        for region in regions.values():
            self.multiworld.regions.append(region)

        # have to place here or generation fails w/ too many junk items
        self.multiworld.get_location("12/12 Paintings", self.player).place_locked_item(self.create_event("12/12 Paintings"))

        # create Entrances and connect the Regions
        menu_region.connect(regions["House"])
        regions["House"].connect(regions["Mom"], rule=lambda state: state.has("Mom Unlock", self.player))
        regions["House"].connect(regions["Train"], rule=lambda state: state.has("Train Unlock",self.player))
        regions["Train"].connect(regions["Fixed Train"], rule=lambda state: state.has("Train Wheel",self.player))
        regions["House"].connect(regions["Gold Statue"], rule=lambda state: state.has("Giant Gold Statue",self.player))
        regions["House"].connect(regions["12 Paintings"], rule=lambda state: state.has("12/12 Paintings",self.player))

        if self.options.goal == "cake":
            # Cake
            self.multiworld.completion_condition[self.player] = lambda state: state.has("12/12 Paintings",self.player)
        elif self.options.goal == "badge":
            # Badge
            self.multiworld.completion_condition[self.player] = lambda state: can_get_all_badges(state,self.player)

    def create_item(self, name: str) -> "DoronkoWankoItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - items_base_id - 1

        classification = doronko_wanko_items[id]["classification"]
        if name == "Turret Gun" and self.options.logic == "glitched":
            classification = ItemClassification.progression
        return DoronkoWankoItem(name, classification, item_id, player=self.player)

    def create_event(self,name: str) -> "DoronkoWankoItem":
        return DoronkoWankoItem(name,ItemClassification.progression, None, player=self.player)

    def create_items(self) -> None:
        itempool = []
        for item in doronko_wanko_items:
            if "Damage" in item["name"]:
                continue
            itempool.append(self.create_item(item["name"]))

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]

        self.multiworld.itempool += itempool

    def set_rules(self):
        create_rules(self)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        options = self.options

        settings = {
            "goal": int(options.goal)
        }

        slot_data = {
            "settings": settings,
        }

        return slot_data
