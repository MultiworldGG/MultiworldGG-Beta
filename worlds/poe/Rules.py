import logging

from worlds.poe.Options import PathOfExileOptions
from .Locations import PathOfExileLocation, base_item_type_locations, level_locations, acts, LocationDict
from BaseClasses import CollectionState, Region
from . import Items
import typing
if typing.TYPE_CHECKING:
    from . import PathOfExileWorld

logger = logging.getLogger("poe.Rules")
logger.setLevel(logging.DEBUG)

MAX_GUCCI_GEAR_UPGRADES = 20
MAX_GEAR_UPGRADES       = 50
MAX_FLASK_SLOTS         = 10
MAX_LINK_UPGRADES       = 22
MAX_SKILL_GEMS          = 30 # you will get more, but this is the max required for "logic"

ACT_0_USABLE_GEMS = 4
ACT_0_FLASK_SLOTS = 3
ACT_0_NORMAL_WEAPONS = 2
ACT_0_NORMAL_ARMOUR = 2
ACT_0_ADDITIONAL_LOCATIONS = 8
_debug = False
_very_debug = False


req_to_use_weapon_types = ["Axe","Bow","Claw","Dagger","Mace","Sceptre","Staff","Sword","Wand",
                            #"Fishing Rod", # yeahhhh no
                            #"Unarmed" # every character can use unarmed, so no need to check this
                            ]

#passives_gained_in_each_act = {
#    1: 16,
#    2: 16,
#    3: 12,
#    4: 10,
#    5: 10,
#    6: 10,
#    7: 10,
#    8: 10,
#    9: 9,
#    10: 9,
#    11: 16,
#}

passives_required_for_act = {
    1: 6,
    2: 16,
    3: 32,
    4: 44,
    5: 54,
    6: 64,
    7: 74,
    8: 84,
    9: 94,
    10: 103,
    11: 112,
    12: 128,  # max ammount of passives in the game
}

def get_ascendancy_amount_for_act(act, opt):
    return (
        min(
            opt.ascendancies_available_per_class.value,
            3 if opt.starting_character.value != opt.starting_character.option_scion else 1
        )
    ) if act == 3 else 0

def get_gear_amount_for_act(act, opt): return min(opt.gear_upgrades_per_act.value * (act - 1), MAX_GEAR_UPGRADES if opt.gucci_hobo_mode.value == opt.gucci_hobo_mode.option_disabled else MAX_GUCCI_GEAR_UPGRADES)
def get_flask_amount_for_act(act, opt): return 0 if not opt.add_flask_slots_to_item_pool else min(opt.flask_slots_per_act.value * (act - 1), MAX_FLASK_SLOTS)
def get_gem_amount_for_act(act, opt): return 0 if not opt.add_max_links_to_item_pool else min(opt.max_links_per_act.value * (act - 1), MAX_LINK_UPGRADES)
def get_skill_gem_amount_for_act(act, opt): return min(opt.skill_gems_per_act.value * (act - 1), MAX_SKILL_GEMS)
def get_passives_amount_for_act(act, opt): return passives_required_for_act.get(act, 0) if opt.add_passive_skill_points_to_item_pool.value else 0

def completion_condition(world: "PathOfExileWorld",  state: CollectionState) -> bool:
    if len(world.bosses_for_goal) > 0:
        # if we can reach act 11, we can assume we have completed the goal
        return can_reach(11, world, state)
    #    # if there are bosses for the goal, we need to check if they are all completed
    #    for boss in world.bosses_for_goal:
    #        if not state.has(f"complete {boss}", world.player):
    #            return False
    #    return True

    else: # reach act for goal
        return can_reach(world.goal_act, world, state)

def can_reach(act: int, world , state: CollectionState) -> bool:
    opt : PathOfExileOptions = world.options

    reachable = True
    if act < 1:
        return True

    ascedancy_amount = get_ascendancy_amount_for_act(act, opt)
    gear_amount = get_gear_amount_for_act(act, opt)
    flask_amount = get_flask_amount_for_act(act, opt)
    gem_slot_amount = get_gem_amount_for_act(act, opt)
    skill_gem_amount = get_skill_gem_amount_for_act(act, opt)
    passive_amount = get_passives_amount_for_act(act,opt)

    # make a list of valid weapon types, based on the state

    valid_weapon_types = {
        item for item in req_to_use_weapon_types
        if state.has_from_list([i["name"] for i in Items.get_by_category(item)], world.player, 1)
    }
    valid_weapon_types.add("Unarmed")  # every character can use unarmed, so we always add it
    
    ascedancy_count = state.count_from_list([item['name'] for item in Items.get_ascendancy_class_items(opt.starting_character.current_option_name)], world.player)
    gear_count = state.count_from_list([item['name'] for item in Items.get_gear_items()], world.player)
    flask_count = state.count_from_list([item['name'] for item in Items.get_flask_items() if 'Unique' not in item['category']], world.player) # unique flasks are not logically required
    gem_slot_count = state.count_from_list([item['name'] for item in Items.get_max_links_items()], world.player)
    passive_count = state.count("Progressive passive point", world.player)

    gems_for_our_weapons = [item['name'] for item in Items.get_main_skill_gems_by_required_level_and_useable_weapon(
            available_weapons= valid_weapon_types, level_minimum=1, level_maximum=acts[act].get("maxMonsterLevel", 0) )]
    usable_skill_gem_count = (state.count_from_list(gems_for_our_weapons, world.player))


    
    if act == 1:
        normal_weapons = state.count_from_list([item['name'] for item in Items.get_by_has_every_category({"Weapon","Normal"})], world.player)
        normal_armour = state.count_from_list([item['name'] for item in Items.get_by_has_every_category({"Armour", "Normal"})], world.player)
        reachable &= usable_skill_gem_count >= ACT_0_USABLE_GEMS
        reachable &= normal_weapons >= ACT_0_NORMAL_WEAPONS
        reachable &= normal_armour >= ACT_0_NORMAL_ARMOUR
        reachable &= flask_count >= ACT_0_FLASK_SLOTS


    reachable &= ascedancy_count >= ascedancy_amount and \
           gear_count >= gear_amount and \
           flask_count >= flask_amount and \
           gem_slot_count >= gem_slot_amount and \
           usable_skill_gem_count >= skill_gem_amount and \
           passive_count >= passive_amount

    if not reachable:
        if _debug:
            log = f"Act {act} not reachable with gear:"
            if gear_count < gear_amount:
                log += f"gear: {gear_count}/{gear_amount},"
            if flask_count < flask_amount:
                log += f" flask: {flask_count}/{flask_amount},"
            if gem_slot_count < gem_slot_amount:
                log += f" gem slots: {gem_slot_count}/{gem_slot_amount},"
            if usable_skill_gem_count < skill_gem_amount:
                log += f" skill gems: {usable_skill_gem_count}/{skill_gem_amount},"
            if ascedancy_count < ascedancy_amount:
                log += f" ascendancies: {ascedancy_count}/{ascedancy_amount},"
            if passive_count < passive_amount:
                log += f" levels:{passive_count}/{passive_amount}"
            log += f" for {opt.starting_character.current_option_name}"

            #print (log)

            logger.debug(log)
        if _very_debug:
            logger.debug(f"[DEBUG] expecting Act {act} - Gear: {gear_amount}, Flask: {flask_amount}, Gem Slots: {gem_slot_amount}, Skill Gems: {skill_gem_amount}, Ascendancies: {ascedancy_amount}")
            logger.debug(f"[DEBUG] we have   Act {act} - Gear: {gear_count}, Flask: {flask_count}, Gem Slots: {gem_slot_count}, Skill Gems: {usable_skill_gem_count}, Ascendancies: {ascedancy_count}")
            #add up all the prog items


            total_items = state.count_from_list([item["name"] for item in Items.get_gear_items()], world.player) + \
                          state.count_from_list([item["name"] for item in Items.get_flask_items()], world.player) + \
                          state.count_from_list([item["name"] for item in Items.get_max_links_items()], world.player) + \
                          state.count_from_list([item["name"] for item in Items.get_main_skill_gem_items()], world.player) + \
                          state.count_from_list([item["name"] for item in Items.get_ascendancy_class_items(opt.starting_character.current_option_name)], world.player)
            logger.debug(f"[DEBUG] total items {total_items}, ")
            logger.debug(f"[DEBUG] expecting   {gear_amount + flask_amount + gem_slot_amount + skill_gem_amount} items")
            logger.debug(f"\n\n")
    
    
    return reachable





def SelectLocationsToAdd (world: "PathOfExileWorld", target_amount):
    opt:PathOfExileOptions = world.options

    total_available_locations: list[LocationDict] = list()
    selected_locations_result: list[LocationDict] = list()
    goal_act = world.goal_act

    max_level = acts[goal_act]["maxMonsterLevel"]

    # Add base item locations
    base_item_locs = [loc for loc in base_item_type_locations.values() if loc["act"] <= goal_act]
    total_available_locations.extend(base_item_locs)
    
    if opt.add_leveling_up_to_location_pool:
        #    {"name": "Reach Level 100", "level": 100, "act": 11},
        lvl_locs = [loc for loc in level_locations.values() if loc["level"] is not None and loc["level"] <= max_level]
        total_available_locations.extend(lvl_locs)

    def total_needed_by_act(act: int, opt: PathOfExileOptions) -> int:
        if act < 1:
            return 0
        needed_locations_for_act = 0
        needed_locations_for_act += ACT_0_USABLE_GEMS + ACT_0_NORMAL_WEAPONS + ACT_0_NORMAL_ARMOUR + ACT_0_FLASK_SLOTS + ACT_0_ADDITIONAL_LOCATIONS
        needed_locations_for_act += get_ascendancy_amount_for_act(act, opt)
        needed_locations_for_act += get_gear_amount_for_act(act, opt)
        needed_locations_for_act += get_flask_amount_for_act(act, opt)
        needed_locations_for_act += get_gem_amount_for_act(act, opt)
        needed_locations_for_act += get_skill_gem_amount_for_act(act, opt)
        needed_locations_for_act += get_passives_amount_for_act(act, opt)
        return needed_locations_for_act


    for act in range(1, goal_act + 1):
        needed_locations_for_act = total_needed_by_act(act, opt) - total_needed_by_act(act - 1, opt)
        locations_in_act = [loc for loc in total_available_locations if loc["act"] == act]
    
        if not locations_in_act:
            break

        if needed_locations_for_act > len(locations_in_act):
            logger.error(f"[ERROR] Not enough locations for Act {act}. Needed: {needed_locations_for_act}, Available: {len(locations_in_act)}, going to try to generate anyway...")

        selected_locations = world.random.sample(locations_in_act, k=min(needed_locations_for_act, len(locations_in_act)))
        for loc in selected_locations:
            total_available_locations.remove(loc)
        selected_locations_result.extend(selected_locations)
    
    
    world.random.shuffle(total_available_locations)
    selected_locations_result.extend(total_available_locations)
    return selected_locations_result[:target_amount]




