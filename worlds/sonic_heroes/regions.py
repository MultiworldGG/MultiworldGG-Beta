from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from typing import Optional

from BaseClasses import Entrance, Region, CollectionState
from .constants import *
from .locations import *


class SonicHeroesRegion(Region):
    game = SONICHEROES

def create_single_region_csv_entry(world: SonicHeroesWorld, team: str, level: str, name: str, obj_checks: int):
    reg = RegionCSVData(team, level, name, obj_checks)
    world.region_list.append(reg)
    world.region_to_location[reg.name] = []


def create_special_region_csv_data(world: SonicHeroesWorld):
    create_single_region_csv_entry(world, ANYTEAM, METALMADNESS, METALMADNESS, 0)
    for name in bonus_and_emerald_stages:
        create_single_region_csv_entry(world, ANYTEAM, name, name, 0)
    world.logic_mapping_dict[ANYTEAM] = world.init_logic_mapping_any_team()




def handle_single_emerald_connection(world: SonicHeroesWorld, team: str, name: str):
    index = 1 if world.secret else 0
    target_region_end = EMERALDSTAGE if bonus_emerald_stage_to_level[name] in emerald_levels else BONUSSTAGE

    if bonus_emerald_stage_to_level[name] in world.allowed_levels_per_team[team]:
        emerald_rule = lambda state: state.has_from_list_unique(world.bonus_key_event_items_per_team[team][
            bonus_emerald_stage_to_level[name]], world.player, world.bonus_keys_needed_for_bonus_stage) and state.has(
            f"{team} {bonus_emerald_stage_to_level[name]} {COMPLETIONEVENT}", world.player)

        connect(world, f"{team} {bonus_emerald_stage_to_level[name]} Bonus Key and Goal",
                f"{bonus_emerald_stage_to_level[name]} {team} Goal",
                f"{bonus_emerald_stage_to_level[name]} {target_region_end}", emerald_rule,
                rule_to_str=f"{world.bonus_keys_needed_for_bonus_stage} Bonus Keys and Goal")
    return



def handle_emerald_connections(world: SonicHeroesWorld, team: str):
    for name in bonus_and_emerald_stages:
        handle_single_emerald_connection(world, team, name)









def create_region(world: SonicHeroesWorld, name: str, hint: str = ""):
    region = SonicHeroesRegion(name, world.player, world.multiworld)
    create_locations(world, region)

    if name == METALOVERLORD:
        location = SonicHeroesLocation(world.player, VICTORYLOCATION, None, region)
        region.locations.append(location)

    #Seaside Hill (Team) Goal
    #Seaside Hill (Team) Bonus Key 1
    name_split = name.split(" ")

    if len(name_split) > 3:
        if name_split[-2] == "Key":
            if name_split[-3] == "Bonus":
                for team in world.enabled_teams:
                    last_word_of_team = team.split(" ")[-1]
                    if name_split[-4] == last_word_of_team:
                        level_name = name_split[0] + " " + name_split[1]
                        #this should be a bonus key region
                        #print(f"I think this is a bonus key region: {name}")
                        location = SonicHeroesLocation(world.player, f"{level_name} {team} Bonus Key {int(name_split[-1])} Event", None, region)
                        region.locations.append(location)





    if name_split[-1] == "Goal":
        for team in world.enabled_teams:
            last_word_of_team = team.split(" ")[-1]
            if name_split[-2] == last_word_of_team:
                level_name = name_split[0] + " " + name_split[1]
                if level_name in world.allowed_levels_per_team[team]:
                    location = SonicHeroesLocation(world.player, f"{name} Event Location", None, region)
                    region.locations.append(location)
                    world.team_level_goal_event_locations[team].append(level_name)

    world.multiworld.regions.append(region)


def create_regions(world: SonicHeroesWorld):
    create_region(world, MENU, MENUREGIONHINT)
    create_region(world, METALOVERLORD, METALMADNESSREGIONHINT)

    create_regions_from_region_list(world)
    pass


def create_regions_from_region_list(world: SonicHeroesWorld):
    #world.region_list = []
    for reg in world.region_list:
        create_region(world, reg.name)
    pass


def connect_entrances(world: SonicHeroesWorld):

    goal_rule = lambda state: get_goal_rule(world, state)

    for team in world.enabled_teams:
        handle_emerald_connections(world, team)
        for reg in world.allowed_levels_per_team[team]:
            connect(world,f"{MENU} -> {reg} {team} Start", MENU, f"{reg} {team} Start", None, rule_to_str="None")

    #connect(world, f"{MENU} -> {SEASIDEHILL} {SONIC} Start", MENU, f"{SEASIDEHILL} {SONIC} Start", None, rule_to_str="None")

    connect(world, f"Goal Connection", MENU, METALMADNESS, goal_rule, rule_to_str=f"Goal Rule")

    connect(world, f"Goal Connection 2", METALMADNESS, METALOVERLORD, goal_rule, rule_to_str=f"Goal Rule")

    connect_entrances_from_connection_list(world)
    pass


def connect_entrances_from_connection_list(world: SonicHeroesWorld):
    for connection in world.connection_list:
        connect(world, connection.name, connection.source, connection.target, world.logic_mapping_dict[connection.team][connection.level][connection.rulestr], rule_to_str=connection.rulestr)



def connect(world: SonicHeroesWorld, name: str, source: str, target: str, rule=None, reach: Optional[bool] = False, rule_to_str: Optional[str] = None,) -> Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    #world.spoiler_string += f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n"
    #print(f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n")

    return connection if reach else None


def get_goal_rule(world: SonicHeroesWorld, state: CollectionState):
    goal_rule_dict: dict[str, int] = {}
    level_completion_items_dict: dict[str, list[str]] = {}

    for team in world.enabled_teams:
        level_completion_items_dict[team] = []
        for char_name in team_char_names[team]:
            goal_rule_dict[get_playable_char_item_name(char_name)] = 1

        if world.options.goal_unlock_condition != 1:
            for name in world.team_level_goal_event_locations[team]:
                level_completion_items_dict[team].append(f"{team} {name} {COMPLETIONEVENT}")

    if world.options.goal_unlock_condition != 0:
        for emerald in emeralds:
            goal_rule_dict[emerald] = 1

    goal_rule_levels = {SONIC: True, DARK: True, ROSE: True, CHAOTIX: True, SUPERHARD: True}

    if world.options.goal_unlock_condition != 1:
        teams_list = level_completion_items_dict.keys()
        if SONIC in teams_list:
            goal_rule_levels[SONIC] = goal_rule_levels[SONIC] and state.has_from_list_unique(level_completion_items_dict[SONIC], world.player,world.options.goal_level_completions.value)
        if DARK in teams_list:
            goal_rule_levels[DARK] = goal_rule_levels[DARK] and state.has_from_list_unique(level_completion_items_dict[DARK], world.player,world.options.goal_level_completions.value)
        if ROSE in teams_list:
            goal_rule_levels[ROSE] = goal_rule_levels[ROSE] and state.has_from_list_unique(level_completion_items_dict[ROSE], world.player,world.options.goal_level_completions.value)
        if CHAOTIX in teams_list:
            goal_rule_levels[CHAOTIX] = goal_rule_levels[CHAOTIX] and state.has_from_list_unique(level_completion_items_dict[CHAOTIX], world.player,world.options.goal_level_completions.value)
        if SUPERHARD in teams_list:
            goal_rule_levels[SUPERHARD] = goal_rule_levels[SUPERHARD] and state.has_from_list_unique(level_completion_items_dict[SUPERHARD], world.player,world.options.goal_level_completions.value)

    goal_rule_items = state.has_all_counts(goal_rule_dict, world.player)

    return goal_rule_items and goal_rule_levels[SONIC] and goal_rule_levels[DARK] and goal_rule_levels[ROSE] and goal_rule_levels[CHAOTIX] and goal_rule_levels[SUPERHARD]