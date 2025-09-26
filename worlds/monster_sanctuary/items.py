import math
import re
from enum import IntEnum
from typing import List, Dict, Optional
from BaseClasses import ItemClassification
from BaseClasses import MultiWorld, Item
from worlds.AutoWorld import World


class MonsterSanctuaryItemCategory(IntEnum):
    KEYITEM = 0
    CRAFTINGMATERIAL = 1
    CONSUMABLE = 2
    FOOD = 3
    CATALYST = 4
    WEAPON = 5
    ACCESSORY = 6
    CURRENCY = 7
    EGG = 8
    COSTUME = 9
    RANK = 10,
    ABILITY = 11,


class ItemData:
    id: int
    name: str
    classification: ItemClassification
    category: MonsterSanctuaryItemCategory
    tier: Optional[int]
    unique: bool
    groups: List[str]
    count: int = 1  # how many of this item should be added to the game
    illegal_locations: List[str]

    def __init__(self, item_id, name, classification, category, unique=False, groups=None):
        self.id = item_id
        self.name = name
        self.classification = classification
        self.category = category
        self.unique = unique
        self.illegal_locations = []

        if groups is not None:
            self.groups = groups
        else:
            self.groups = []

    # def __str__(self):
    #     return self.name


class MonsterSanctuaryItem(Item):
    game: str = "Monster Sanctuary"
    quantity: int = 1

    def __init__(self, player: int, id: int, name: str, classification: ItemClassification):
        super(MonsterSanctuaryItem, self).__init__(name, classification, id, player)

    # def __str__(self):
    #     return self.name


# This holds all the item data that is parsed from items.json file
item_data: Dict[str, ItemData] = {}
item_drop_probabilities: List[MonsterSanctuaryItemCategory] = []

# Explore item lists for easy referencing
explore_ability_types = [
    "Spectral Flame",
    "Slime Treats",
    "Insect Pheromones",
    "Monster Treat",
    "Repair Kit",
    "Ancient Encyclopedia",
    "Training Dummy",
    "Spellbook",
    "Goblin Charm",
    "Fishing Lure",
    "Dragon Orb",
    "Power Suit",
    "Spirit Charm",
    "Green Thumb",
    "Bird Seed"
]
explore_ability_progression = [
    ("Progressive Mobility", 5),
    ("Progressive Terrain", 3),
    ("Progressive Mount", 3),
    ("Progressive Walls", 3),
    ("Progressive Boulders", 3),
    ("Progressive Fire Orbs", 2),
    ("Progressive Water Orbs", 2),
    ("Progressive Lightning Orbs", 2),
    ("Progressive Earth Orbs", 3),
    ("Progressive Ice Orbs", 2),
    ("Progressive Light", 2),
    ("Progressive Shroud", 2),
]
explore_ability_combo = [
    ("Combo Flight", 2),
    ("Combo Swimming", 2),
    ("Combo Walls", 3),
    ("Combo Boulders", 2),
    ("Combo Mount", 1),
    ("Combo Light", 1),
    ("Combo Orbs", 3),
    ("Combo Shroud", 2),
    ("Combo Magic", 2),
]


def can_item_be_placed(world: World, item: Item, location: str) -> bool:
    area_name = location.split(' - ')[0]

    # If this item is an area key and keys must be local, then we check to see if
    # the item name starts with the area name (ignoring spaces)
    # This overrides the 'no progression in X' settings
    if item.player == world.player and is_item_in_group(item.name, "Area Key") and world.options.local_area_keys:
        return item.name.startswith(area_name)

    if area_name == "Underworld" and world.options.no_progression_in_underworld:
        if item.classification & ItemClassification.progression:
            return False

    if area_name == "Forgotten World" and world.options.no_progression_in_forgotten_world:
        if item.classification & ItemClassification.progression:
            return False

    # For any item that's not a monster sanctuary item, it can go here
    if item.player != world.player:
        return True

    data = get_item_by_name(item.name)

    # If the item is an egg with an improved movement ability
    # And the settings are to limit placement of those abilities
    # Then we make sure the item can't be placed in the first half of the game
    if is_item_in_group(item.name, "Improved Flying", "Lofty Mount", "Improved Swimming", "Dual Mobility")\
            and world.options.improved_mobility_limit:
        return area_name not in ["Menu", "Mountain Path", "Blue Cave", "Keepers Stronghold", "Keepers Tower",
                            "Stronghold Dungeon", "Snowy Peaks", "Sun Palace", "Ancient Woods"]

    # Go through every illegal location for this item and if the location name starts
    # with an illegal location, then return false
    for illegal_location in data.illegal_locations:
        if location.startswith(illegal_location):
            return False

    return True


def build_item_groups() -> Dict:
    item_groups = {}
    for item, data in item_data.items():
        for group in data.groups:
            item_groups[group] = item_groups.get(group, []) + [item]

    return item_groups


def is_item_in_group(item: str, *groups: str) -> bool:
    """Checks to see fi the item is in any of the given groups"""
    # If there's on groups to check, then we return true
    if len(groups) == 0:
        return True
    return not set(item_data[item].groups).isdisjoint(groups)


def get_item_by_name(item: str) -> Optional[ItemData]:
    if item in item_data:
        return item_data[item]
    return None


def get_item_type(item_name: str) -> Optional[MonsterSanctuaryItemCategory]:
    item = item_data.get(item_name)
    if item is None:
        return None

    return item.category


def get_items_in_group(group: str, include_plus_items: bool = False) -> List[ItemData]:
    return [item for name, item in item_data.items()
            if group in item.groups
            and (include_plus_items or "+" not in name)]


def is_item_type(item_name: str, *item_types: MonsterSanctuaryItemCategory) -> bool:
    # For any item not in the item data dictionary, return false
    # This solves the problem with items from other worlds not having a type
    if item_data.get(item_name) is None:
        return False
    return get_item_type(item_name) in item_types


def build_item_probability_table(probabilities: Dict[MonsterSanctuaryItemCategory, int]) -> None:
    # If the weights don't sum to 100, then we multiply them all by 10 so that the
    # sum is much higher. This solves the issue where at low totals we can't accurately
    # calculate a single percentage for the costumes section
    if sum(probabilities.values()) < 100:
        probabilities = {key: probabilities[key] * 10 for key in probabilities}

    # Costumes are always forced to a 1% drop rate. Maybe a setting to disable this later
    # but for now it's just a flat 1% chance.
    probabilities[MonsterSanctuaryItemCategory.COSTUME] = math.ceil(sum(probabilities.values()) * 0.01)

    item_drop_probabilities.clear()
    for item_type in probabilities:
        for i in range(probabilities[item_type]):
            item_drop_probabilities.append(item_type)


def get_random_item_name(world: World,
                         itempool: List[MonsterSanctuaryItem],
                         group_include: Optional[List[str]] = None,
                         group_exclude: Optional[List[str]] = None) -> Optional[str]:
    """Gets a random item name from the master item list with the following restrictions:
    Unique items already in the item pool will not be added a second time
    Items with groups that intersect with group_exclude will not be added
    Only items whose groups intersect with group_include will be selected from"""
    if group_include is None:
        group_include = []
    if group_exclude is None:
        group_exclude = []

    # We should never return multiple items, those require special randomization
    # that happens down below
    if "Multiple" not in group_exclude:
        group_exclude.append("Multiple")

    item_type = world.random.choice(item_drop_probabilities)
    item_pool_names = {item.name for item in itempool}

    item_name: str
    valid_items = [item_name for item_name, item in item_data.items()
                   if (not item.unique or not item_name in item_pool_names)
                   and item.category == item_type
                   and "+" not in item_name  # Filter out any equipment with a higher level. We handle this below
                   and is_item_in_group(item_name, *group_include)
                   and not is_item_in_group(item_name, *group_exclude)]

    if len(valid_items) == 0:
        return None

    base_item_name = world.random.choice(valid_items)
    base_item = item_data.get(base_item_name)

    # weapons and accessories can gen at a higher tier, so we determine that here
    if (item_type == MonsterSanctuaryItemCategory.WEAPON
            or item_type == MonsterSanctuaryItemCategory.ACCESSORY):
        return roll_random_equipment_level(world, base_item)

    return roll_random_item_quantity(world, base_item)


def roll_random_equipment_level(world: World, base_item: ItemData) -> str:
    # If the options say to automatically level equipment, then we never modify the equipment here
    if world.options.automatically_scale_equipment.value != "disabled":
        return base_item.name

    """Randomly rolls to determine an equipment's level (+0, +1, +2, +3, +4, or +5)"""
    name_append = None
    roll = world.random.randint(1, 100)

    if roll > 95:
        name_append = "+5"
    elif roll > 85:
        name_append = "+4"
    elif roll > 70:
        name_append = "+3"
    elif roll > 50:
        name_append = "+2"
    elif roll > 25:
        name_append = "+1"

    if name_append is not None:
        new_item_name = f"{base_item.name}{name_append}"
        if new_item_name is not None and item_data.get(new_item_name) is not None:
            base_item = item_data[new_item_name]

    return base_item.name


def roll_random_item_quantity(world: World, base_item: ItemData) -> str:
    name_prepend = None
    roll = world.random.randint(1, 10)

    if "Up to 2" in base_item.groups:
        if roll >= 5:
            name_prepend = "2x"
    elif "Up to 3" in base_item.groups:
        if roll >= 8:
            name_prepend = "3x"
        elif roll >= 5:
            name_prepend = "2x"
    elif "Up to 4" in base_item.groups:
        if roll >= 10:
            name_prepend = "4x"
        elif roll >= 8:
            name_prepend = "2x"
        elif roll >= 5:
            name_prepend = "2x"

    if name_prepend is not None:
        new_item_name = f"{name_prepend} {base_item.name}"
        if new_item_name is not None and item_data.get(new_item_name) is not None:
            base_item = item_data[new_item_name]

    return base_item.name


def get_explore_ability_items(explore_ability_option: int) -> List[ItemData]:
    # For options 1, 2, and 3, we simply return a flat list of items
    if explore_ability_option in [1, 2, 3]:
        return [data for name, data in item_data.items()
                if data.category == MonsterSanctuaryItemCategory.ABILITY and
                ((explore_ability_option == 1 and name in explore_ability_types) or
                (explore_ability_option == 2 and "Ability - " in name) or
                (explore_ability_option == 3 and "Ability - " not in name and name not in explore_ability_types)) and
                "Progressive" not in name and
                "Combo" not in name]

    # Progression type
    elif explore_ability_option == 4:
        items = []
        for item in explore_ability_progression:
            for i in range(item[1]):
                items.append(item_data[item[0]])
        return items

    # Combo type
    elif explore_ability_option == 5:
        items = []
        for item in explore_ability_combo:
            for i in range(item[1]):
                items.append(item_data[item[0]])
        return items

    return []
