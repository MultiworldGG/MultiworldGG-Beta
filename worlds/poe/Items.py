import random
import typing
from collections import defaultdict

if typing.TYPE_CHECKING:
    from worlds.poe import PathOfExileWorld
    from worlds.poe.Options import PathOfExileOptions

from BaseClasses import Item, ItemClassification
from typing import TypedDict, Dict, Set

from worlds.poe.data import ItemTable
from worlds.poe import Locations
from worlds.poe import Items

import logging
logger = logging.getLogger("poe.Items")
logger.setLevel(logging.DEBUG)
_verbose_debug = False  # Set to True to enable verbose debug logging

ACT_0_USABLE_GEMS = 4
ACT_0_FLASK_SLOTS = 3
ACT_0_WEAPON_TYPES = 2
ACT_0_ARMOUR_TYPES = 2
ACT_0_ADDITIONAL_LOCATIONS = 8

ACT_1_MOVEMENT_GEMS = 2

class ItemDict(TypedDict, total=False): 
    classification: ItemClassification 
    count: int | None
    id : int
    name: str 
    category: list[str]
    reqLevel: int | None
    reqToUse: list[str] | None

class PathOfExileItem(Item):
    """
    Represents an item in the Path of Exile world.
    This class can be extended to include specific item properties and methods.
    """
    game = "Path of Exile"
    itemInfo: ItemDict
    category = list[str]()


item_table: Dict[int, ItemDict] = ItemTable.item_table
alternate_gems: Dict[str, Dict] = ItemTable.alternate_gems
if _verbose_debug:
    logger.debug(f"Loaded {len(item_table)} items from ItemTable.")
memoize_cache: Dict[str, list[ItemDict]] = {}

def get_item_name_groups() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = defaultdict(set)
    for item in item_table.values():
        main_category = item.get("category", [None])[0]
        if main_category:
            categories[main_category].add(item["name"])
    return categories

def get_flask_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Flask", table)

def get_character_class_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Character Class", table)

def get_base_class_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Base Class", table)

def get_ascendancy_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Ascendancy", table)

def get_ascendancy_class_items(class_name: str, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_has_every_category({"Ascendancy", f"{class_name} Class"}, table)

def get_main_skill_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("MainSkillGem", table)

def get_main_skill_gem_items_table(table: Dict[int, ItemDict] = item_table) -> dict[int, ItemDict]:
    return {item["id"]: item for item in get_main_skill_gem_items(table)}

def get_support_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("SupportGem", table)

def get_utility_skill_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("UtilSkillGem", table)

def get_gear_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Gear", table)

def get_armor_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Armor", table)

def get_weapon_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("Weapon", table)

def get_max_links_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_by_category("max links", table)

def get_all_gems(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "AllGems" in memoize_cache:
        return memoize_cache["AllGems"]
    result = get_main_skill_gem_items(table) + get_support_gem_items(table) + get_utility_skill_gem_items(table)
    if table is item_table: memoize_cache["AllGems"] = result
    return result

def get_main_skill_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"MainSkillGems_{level_minimum}_{level_maximum}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if "MainSkillGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))]
    if table is item_table: memoize_cache[key] = result
    return result

def get_main_skill_gems_by_required_level_and_useable_weapon(available_weapons: set[str], level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    # Create a sorted, hashable key from the weapons set
    weapons_key = "_".join(sorted(available_weapons))
    key = f"MainSkillGemsUseable_{weapons_key}_{level_minimum}_{level_maximum}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if "MainSkillGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))
            and (any(weapon in available_weapons for weapon in item.get("reqToUse", [])) or not item.get("reqToUse", []))] # we have the weapon, or there are no reqToUse
    if table is item_table: memoize_cache[key] = result
    return result

def get_support_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"SupportGems_{level_minimum}_{level_maximum}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if "SupportGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))]
    if table is item_table: memoize_cache[key] = result
    return result

def get_utility_skill_gems_by_required_level_usable_weapon_and_category(available_weapons: set[str], level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table, required_categories:set[str]=set()) -> list[ItemDict]:
    key = f"UtilitySkillGems_{level_minimum}_{level_maximum}_category_" + "_".join(sorted(required_categories))
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in get_utility_skill_gems_by_required_level(level_minimum, level_maximum, table) if
              any(cat in item["category"] for cat in required_categories) and
              (any(weapon in available_weapons for weapon in item.get("reqToUse", [])) or not item.get("reqToUse", [])) # we have the weapon, or there are no reqToUse]
              ]
    if table is item_table: memoize_cache[key] = result
    return result

def get_utility_skill_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table, additional_categories:list[str] = None) -> list[ItemDict]:
    key = f"UtilitySkillGems_{level_minimum}_{level_maximum}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if "UtilSkillGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))]
    if table is item_table: memoize_cache[key] = result
    return result

def get_all_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    return get_main_skill_gems_by_required_level(level_minimum, level_maximum, table) + \
           get_support_gems_by_required_level(level_minimum, level_maximum, table) + \
           get_utility_skill_gems_by_required_level(level_minimum, level_maximum, table)

def get_by_category(category: str, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"category_{category}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if category in item["category"]]
    if table is item_table: memoize_cache[key] = result
    return result

def get_by_has_every_category(categories: Set[str], table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"has_every_category_{'_'.join(sorted(categories))}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if all(cat in item["category"] for cat in categories)]
    if table is item_table: memoize_cache[key] = result
    return result

def get_by_has_any_category(categories: Set[str], table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"has_any_category_{'_'.join(sorted(categories))}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if any(cat in item["category"] for cat in categories)]
    if table is item_table: memoize_cache[key] = result
    return result

def get_by_name(name: str, table: Dict[int, ItemDict] = item_table) -> ItemDict | None:
    return next((item for item in table.values() if item["name"] == name), None)

# used to check offhands

quiver_base_types = ItemTable.quiver_base_type_array.copy()  # Copy the list to avoid modifying the original data
shield_base_types = ItemTable.shield_base_type_array.copy() 


# used to check weapon base types
held_equipment_types = [
"Axe",
"Bow",
"Claw",
"Dagger",
"Mace",
"Sceptre",
"Staff",
"Sword",
"Wand",
"Shield",
"Quiver",
"Fishing Rod",
]