import typing

if typing.TYPE_CHECKING:
    from worlds.poe import PathOfExileWorld
    from worlds.poe.Options import PathOfExileOptions

from BaseClasses import Item, ItemClassification
from typing import TypedDict, Dict, Set

from worlds.poe.data import ItemTable
from worlds.poe import Locations

import logging
logger = logging.getLogger("poe.Items")
logger.setLevel(logging.DEBUG)
_verbose_debug = False  # Set to True to enable verbose debug logging

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



#def get_items():
#    """
#    Returns a list of all items available in the Path of Exile world.
#    This function can be extended to include specific item definitions.
#    """
#    return items



item_table: Dict[int, ItemDict] = ItemTable.item_table
if _verbose_debug:
    logger.debug(f"Loaded {len(item_table)} items from ItemTable.")
memoize_cache: Dict[str, list[ItemDict]] = {}

def deprioritize_non_logic_gems(world: "PathOfExileWorld", table: Dict[int, ItemDict]) -> Dict[int, ItemDict]:
    opt: PathOfExileOptions = world.options
    
    still_required_gem_ids = set()
    
    for act in range(1, world.goal_act + 1):
        main_gems_for_act = [item for item in get_main_skill_gem_items(table) if item["reqLevel"] <= Locations.acts[act]["maxMonsterLevel"]]
        support_gems_for_act = [item for item in get_support_gem_items(table) if item["reqLevel"] <= Locations.acts[act]["maxMonsterLevel"]]
        utility_gems_for_act = [item for item in get_utility_skill_gem_items(table) if item["reqLevel"] <= Locations.acts[act]["maxMonsterLevel"]]
        
        if main_gems_for_act:  
            selected_gems = world.random.sample(main_gems_for_act, k=min(opt.skill_gems_per_act.value + 1, len(main_gems_for_act))) #need at _least_ one main skill gem per act
            selected_gems.extend(world.random.sample(support_gems_for_act, k=min(opt.skill_gems_per_act.value, len(support_gems_for_act))))
            selected_gems.extend(world.random.sample(utility_gems_for_act, k=min(opt.skill_gems_per_act.value, len(utility_gems_for_act))))


            still_required_gem_ids.update(item["id"] for item in selected_gems)
    
    for item in table.values():
        if "MainSkillGem" in item["category"]\
            or "SupportGem" in item["category"] \
            or "UtilSkillGem" in item["category"] \
                :
            if item["id"] in still_required_gem_ids:
                item["classification"] = ItemClassification.progression
            else:
                if item["classification"] == ItemClassification.progression:
                    item["classification"] = ItemClassification.useful
                elif item["classification"] == ItemClassification.useful:
                    item["classification"] = ItemClassification.filler
    return table

GUARANTEED_WEAPON_COUNT = 2  # The number of guaranteed weapons to keep in the world
def deprioritize_non_logic_gear(world: "PathOfExileWorld", table: Dict[int, ItemDict]) -> Dict[int, ItemDict]:
    opt: PathOfExileOptions = world.options

    required_weps = list()
    progression_main_gems = [gem for gem in get_main_skill_gem_items(table) if gem["classification"] == ItemClassification.progression]
    for gem in progression_main_gems:
        for wep in gem.get("reqToUse", []):
            required_weps.append(wep)
    
    required_weps = world.random.sample(required_weps, k=min(GUARANTEED_WEAPON_COUNT, len(required_weps)))
    if "Unarmed" in required_weps: required_weps.remove("Unarmed")
    required_weps.extend(["Wand", "Bow", "Sword"])
    required_weps = required_weps[:GUARANTEED_WEAPON_COUNT]  # Ensure we only keep the guaranteed number of weapons


    gear_ids = [item["id"] for item in get_gear_items(table)]
    progression_sample_size = min(opt.gear_upgrades_per_act.value * world.goal_act, len(gear_ids))
    progression_gear_ids = world.random.sample(gear_ids, progression_sample_size)

    for item in [ item for item in get_gear_items(table)]:
        if item["name"] in required_weps or item["id"] in progression_gear_ids:
            item["classification"] = ItemClassification.progression
        else:
            if item["classification"] == ItemClassification.progression:
                item["classification"] = ItemClassification.useful
            elif item["classification"] == ItemClassification.useful:
                item["classification"] = ItemClassification.filler
    
    return table

def cull_items_to_place(world: "PathOfExileWorld", items: Dict[int, ItemDict], locations: Dict[int, ItemDict]) -> Dict[int, ItemDict]:
    total_locations_count = len(locations)

    # Keep culling until we match the location count
    while True:
        total_items_count = sum(item.get("count", 1) for item in items.values())
        amount_to_cull = total_items_count - total_locations_count
        
        if amount_to_cull <= 0:
            break

        filler_items = [(item_id, item) for item_id, item in items.items() 
                       if item.get("classification") == ItemClassification.filler]

        useful_items = [(item_id, item) for item_id, item in items.items()
                       if item.get("classification") == ItemClassification.useful]
        
        
        if not filler_items and not useful_items:
            logger.error("[ERROR] No items available to remove. Cannot match location count.")
            break

        filler_items = world.random.sample(filler_items, k=min(len(filler_items), amount_to_cull))
        useful_items = world.random.sample(useful_items, k=min(len(useful_items), amount_to_cull))

        culled_count = 0
        def cull_item_func(cull_items, culled_count=0, amount_to_cull=amount_to_cull):
            starting_culled_count = culled_count
            items_to_remove = []

            for item_id, item in cull_items:
                if culled_count >= amount_to_cull:
                    break

                item_count = item.get("count", 1)

                if item_count <= (amount_to_cull - culled_count):
                    # Remove entire item
                    items_to_remove.append(item_id)
                    culled_count += item_count
                else:
                    # Reduce item count
                    reduction = amount_to_cull - culled_count
                    item["count"] = item_count - reduction
                    culled_count += reduction

            # Remove items marked for removal
            for item_id in items_to_remove:
                items.pop(item_id, None)
            return culled_count - starting_culled_count

        culled_count += cull_item_func(filler_items, culled_count, amount_to_cull)
        culled_count += cull_item_func(useful_items, culled_count, amount_to_cull)

        logger.info(f"[INFO] Culled {culled_count} items.")

    # Final verification
    final_count = sum(item.get("count", 1) for item in items.values())
    if final_count != total_locations_count:
        logger.warning(f"Final item count ({final_count}) doesn't match location count ({total_locations_count})")

    return items


def get_item_name_groups() -> Dict[str, Set[str]]:
        categories: Dict[str, Set[str]] = {}
        for item in item_table.values():
            category = item.get("category", [])
            main_category = category[0]
            if main_category:
                if main_category not in categories:
                    categories[main_category] = set()
                categories[main_category].add(item["name"])

        return categories

def get_flask_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Flask" in memoize_cache:
        return memoize_cache["Flask"]
    result = [item for item in table.values() if "Flask" in item["category"]]
    if table is item_table: memoize_cache["Flask"] = result
    return result

def get_character_class_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Character Class" in memoize_cache:
        return memoize_cache["Character Class"]
    result = [item for item in table.values() if "Character Class" in item["category"]]
    if table is item_table: memoize_cache["Character Class"] = result
    return result

def get_base_class_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Base Class" in memoize_cache:
        return memoize_cache["Base Class"]
    result = [item for item in table.values() if "Base Class" in item["category"]]
    if table is item_table: memoize_cache["Base Class"] = result
    return result

def get_ascendancy_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Ascendancy" in memoize_cache:
        return memoize_cache["Ascendancy"]
    result = [item for item in table.values() if "Ascendancy" in item["category"]]
    if table is item_table: memoize_cache["Ascendancy"] = result
    return result

def get_ascendancy_class_items(class_name: str, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and f"{class_name} Ascendancy Class" in memoize_cache:
        return memoize_cache[f"{class_name} Ascendancy Class"]
    result = [item for item in table.values() if "Ascendancy" in item["category"] and f"{class_name} Class" in item["category"]]
    if table is item_table: memoize_cache[f"{class_name} Ascendancy Class"] = result
    return result

def get_main_skill_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "MainSkillGem" in memoize_cache:
        return memoize_cache["MainSkillGem"]
    result = [item for item in table.values() if "MainSkillGem" in item["category"]]
    if table is item_table: memoize_cache["MainSkillGem"] = result
    return result

def get_main_skill_gem_items_table(table: Dict[int, ItemDict] = item_table) -> dict[int, ItemDict]:
    result = {item["id"]: item for item in table.values() if "MainSkillGem" in item["category"]}
    return result

def get_support_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "SupportGem" in memoize_cache:
        return memoize_cache["SupportGem"]
    result = [item for item in table.values() if "SupportGem" in item["category"]]
    if table is item_table: memoize_cache["SupportGem"] = result
    return result

def get_utility_skill_gem_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "UtilSkillGem" in memoize_cache:
        return memoize_cache["UtilSkillGem"]
    result = [item for item in table.values() if "UtilSkillGem" in item["category"]]
    if table is item_table: memoize_cache["UtilSkillGem"] = result
    return result

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
    return [item for item in table.values() if "MainSkillGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))
            and (any(weapon in available_weapons for weapon in item.get("reqToUse", [])) or not item.get("reqToUse", []))] # we have the weapon, or there are no reqToUse

def get_support_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    key = f"SupportGems_{level_minimum}_{level_maximum}"
    if table is item_table and key in memoize_cache:
        return memoize_cache[key]
    result = [item for item in table.values() if "SupportGem" in item["category"] and (item["reqLevel"] is not None and (level_minimum <= item["reqLevel"] <= level_maximum))]
    if table is item_table: memoize_cache[key] = result
    return result

def get_utility_skill_gems_by_required_level(level_minimum:int=0, level_maximum:int=100, table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
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

def get_gear_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Gear" in memoize_cache:
        return memoize_cache["Gear"]
    result = [item for item in table.values() if "Gear" in item["category"]]
    if table is item_table: memoize_cache["Gear"] = result
    return result

def get_armor_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Armor" in memoize_cache:
        return memoize_cache["Armor"]
    result = [item for item in table.values() if "Armor" in item["category"]]
    if table is item_table: memoize_cache["Armor"] = result
    return result

def get_weapon_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "Weapon" in memoize_cache:
        return memoize_cache["Weapon"]
    result = [item for item in table.values() if "Weapon" in item["category"]]
    if table is item_table: memoize_cache["Weapon"] = result
    return result

def get_max_links_items(table: Dict[int, ItemDict] = item_table) -> list[ItemDict]:
    if table is item_table and "max links" in memoize_cache:
        return memoize_cache["max links"]
    result = [item for item in table.values() if "max links" in item["category"]]
    if table is item_table: memoize_cache["max links"] = result
    return result

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