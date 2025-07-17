import math
from typing import Dict, Any, ClassVar, List, Set
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType, Tutorial
from .Items import raw_items, PowerwashSimulatorItem, item_table, create_items, unlock_items, filler_items
from .Locations import location_dict, raw_location_dict, locations_percentages, land_vehicles, objectsanity_dict
from .Options import PowerwashSimulatorOptions, PowerwashSimulatorSettings, check_options
from .Constants import GAME_NAME, AUTHOR, IGDB_ID

uuid_offset = 0x3AF4F1BC

class PowerwashSimulatorWebWorld(WebWorld):
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Powerwash Simulator in MultiworldGG.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["SW_CreeperKing"]
    )

    tutorials = [setup_en]

class PowerwashSimulator(World):
    """
    Powerwash Simulator
    """
    game = GAME_NAME
    author: str = AUTHOR
    igdb_id = IGDB_ID
    web = PowerwashSimulatorWebWorld()
    options_dataclass = PowerwashSimulatorOptions
    options: PowerwashSimulatorOptions
    settings: ClassVar[PowerwashSimulatorSettings]
    location_name_to_id = {value: location_dict.index(value) + uuid_offset for value in location_dict}
    item_name_to_id = {value: raw_items.index(value) + uuid_offset for value in raw_items}
    player_item_steps: Dict[str, Dict[str, int]] = {}
    player_filler_locations: Dict[str, List[str]] = {}
    player_goal_levels: Dict[str, List[str]] = {}
    player_starting_location: Dict[str, str] = {}
    item_name_groups = {
        "unlocks": unlock_items
    }

    def generate_early(self) -> None:
        item_steps: Dict[str, int] = {}
        self.player_starting_location[self.player_name] = land_vehicles[0]
        option_locations = self.options.get_locations()
        check_options(self)

        option_location_count = len(option_locations)
        percentsanity = self.options.percentsanity

        item_steps["total"] = 0
        item_steps["percentsanity"] = (len(range(percentsanity, 100, percentsanity)) + 1) * option_location_count
        item_steps["objectsanity"] = sum(len(objectsanity_dict[loc]) for loc in option_locations)

        if self.options.has_percentsanity():
            item_steps["total"] += item_steps["percentsanity"]

        if self.options.has_objectsanity():
            item_steps["total"] += item_steps["objectsanity"]

        item_steps["unlocks"] = option_location_count - 1
        item_steps["raw mcguffins"] = option_location_count if self.options.goal_type == 0 else 0
        item_steps["progression before added"] = item_steps["unlocks"] + item_steps["raw mcguffins"]

        item_steps["added mcguffins"] = math.floor(
            (item_steps["total"] - item_steps[
                "progression before added"]) * .1) if self.options.goal_type == 0 else 0

        item_steps["total mcguffins"] = item_steps["raw mcguffins"] + item_steps["added mcguffins"]

        item_steps["total progression"] = item_steps["progression before added"] + item_steps[
            "added mcguffins"]

        item_steps["filler"] = math.floor(
            (item_steps["total"] - item_steps["total progression"]) * self.options.local_fill / 100.0)

        if self.options.goal_type == 1:
            levels = [loc for loc in self.options.levels_to_goal.value]
            amount_to_goal = self.options.amount_of_levels_to_goal.value

            self.player_goal_levels[self.player_name] = levels
            item_steps["goal level count"] = amount_to_goal
        else:
            item_steps["goal level count"] = -1
            self.player_goal_levels[self.player_name] = ["None"]

        self.player_item_steps[self.player_name] = item_steps


    def create_regions(self) -> None:
        self.player_filler_locations[self.player_name] = []
        option_locations = self.options.get_locations()
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        option_location_count = len(option_locations)
        percentsanity = self.options.percentsanity
        starting_location = self.player_starting_location[self.player_name]

        planned_placement = {}
        if self.options.goal_type == 0:
            placement_queue = [starting_location]
            unlock_queue = [loc for loc in option_locations if loc != starting_location]
            self.random.shuffle(unlock_queue)

            while len(placement_queue) > 0 and len(unlock_queue) > 0:
                place_next = placement_queue.pop()
                place_random_queue = min(3, len(unlock_queue))
                place_next_queue = self.random.sample(unlock_queue, self.random.randint(1, place_random_queue))
                unlock_queue = [loc for loc in unlock_queue if loc not in place_next_queue]
                placement_queue += place_next_queue
                planned_placement[place_next] = place_next_queue

        for location in option_locations:
            location_list: List[str] = []
            next_region = Region(f"Clean the {location}", self.player, self.multiworld)
            self.multiworld.regions.append(next_region)

            if self.options.has_percentsanity():
                for i in range(percentsanity, 100, percentsanity):
                    location_list.append(self.make_location(f"{location} {i}%", next_region).name)

                location_list.append(self.make_location(f"{location} 100%", next_region).name)

            if self.options.has_objectsanity():
                for part in objectsanity_dict[location]:
                    location_list.append(self.make_location(part, next_region).name)

            if location in self.options.levels_to_goal:
                level_completion_loc = Location(self.player, f"Urge to clean the {location}", None, next_region)
                level_completion_loc.place_locked_item(
                    Item("Satisfied the Urge", ItemClassification.progression, None, self.player))
                next_region.locations.append(level_completion_loc)

            if location == starting_location:
                menu_region.connect(next_region)
            else:
                menu_region.connect(next_region,
                                    rule=lambda state, location_lock=location: state.has(f"{location_lock} Unlock",
                                                                                         self.player))

            next_region.connect(menu_region)
            self.random.shuffle(location_list)

            if self.options.goal_type == 0 and location in planned_placement:
                for loc in planned_placement[location]:
                    self.multiworld.get_location(location_list.pop(), self.player).place_locked_item(self.create_item(f"{loc} Unlock"))
            elif self.options.goal_type == 1:
                location_list.pop()
                self.multiworld.get_location(location_list.pop(), self.player).progress_type = ItemClassification.progression

            self.player_filler_locations[self.player_name] += location_list

        item_steps = self.player_item_steps[self.player_name]
        item_steps["mcguffin requirement"] = max(
            min(math.floor(item_steps["total"] * .05), item_steps["total"] - option_location_count * 2),
            len(option_locations))
        item_steps["added filler"] = item_steps["filler"] - len(self.player_filler_locations[self.player_name])
        self.player_item_steps[self.player_name] = item_steps


    def create_item(self, name: str) -> PowerwashSimulatorItem:
        return PowerwashSimulatorItem(name, item_table[name], self.item_name_to_id[name], self.player)


    def create_items(self) -> None:
        create_items(self)


    def set_rules(self) -> None:
        if self.options.goal_type == 0:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("A Job Well Done", self.player,
                                                                                        self.player_item_steps[self.player_name]["mcguffin requirement"])
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Satisfied the Urge", self.player, self.player_item_steps[self.player_name]["goal level count"])


    def pre_fill(self) -> None:
        location_map: List[Location] = [self.multiworld.get_location(loc, self.player) for loc in self.player_filler_locations[self.player_name]]
        filler = self.player_item_steps[self.player_name]["filler"]
        filler_size = min(filler, len(location_map))

        for i in range(filler_size):
            location_map[i].place_locked_item(self.create_item(self.random.choice(filler_items)))


    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "starting_location": str(self.player_starting_location[self.player_name]),
            "jobs_done": int(self.player_item_steps[self.player_name]["mcguffin requirement"]),
            "objectsanity": bool("Objectsanity" in self.options.sanities),
            "percentsanity": bool("Percentsanity" in self.options.sanities),
            "goal_levels": str(self.player_goal_levels[self.player_name]),
            "goal_level_amount": int(self.player_item_steps[self.player_name]["goal level count"])
        }

        return slot_data


    def make_location(self, location_name, region) -> Location:
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)
        return location
