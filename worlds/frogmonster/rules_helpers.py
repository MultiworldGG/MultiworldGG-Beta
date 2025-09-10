from typing import Iterable

from BaseClasses import CollectionState
from .combat import combat_data, Difficulty, tanky_bugs, mana_bugs
from .names import item_names as i
from .names import combat_names as c
from .names import region_names as r

myzand_gun_library = {
        i.seedling: i.seedling_myzand_upgrade,
        i.reeder: i.reeder_myzand_upgrade,
        i.machine_gun: i.machine_gun_myzand_upgrade,
        i.weepwood_bow: i.weepwood_bow_myzand_upgrade,
        i.finisher: i.finisher_myzand_upgrade,
        i.fire_fruit_juicer: i.fire_fruit_juicer_myzand_upgrade,
        i.gatling_gun: i.gatling_gun_myzand_upgrade,
        i.wooden_cannon: i.wooden_cannon_myzand_upgrade
    }

def can_fight(name: str, player: int, difficulty: Difficulty, state: CollectionState) -> bool:

    # First, handle some fights that really can't rely on the default calculations.
    weird_fights = {
        c.barge: can_fight_barge,
        c.chroma: can_fight_chroma
    }
    if name in weird_fights:
        return weird_fights[name](difficulty, state, player)
    
    score, need, want, tags = get_combat_data(name, difficulty)
    for item in need:
        if not state.has(item, player):
            return False
    if score <= 0:
        return True
    elif score == 1:
        return nice_to_haves(state, player, 0, 0) >= 1
    elif score == 2:
        return  (
                state.has_group_unique("Gun", player, 1) and
                nice_to_haves(state, player, 1, 0) >= 2
                )
    elif score == 3:
        return (
                state.has_group_unique("Gun", player, 1) and
                nice_to_haves(state, player, 1, 0) >= 4
               )
    elif score == 4:
        return (
                state.has_group_unique("Gun", player, 2) and
                nice_to_haves(state, player, 2, 0) >= 5
               )
    elif score == 5:
        return (
                state.has_group_unique("Gun", player, 2) and
                state.has(i.metal_ore, player, 3) and
                can_upgrade(state, player) and
                state.has_group_unique("Spell", player, 1) and
                nice_to_haves(state, player, 2, 0) >= 5
               )
    elif score == 6:
        return (
                state.has_group_unique("Gun", player, 3) and
                matching_myzands(state, player) >= 1 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 5) and
                state.has_group_unique("Spell", player, 1) and
                nice_to_haves(state, player, 3, 1) >= 6
               )
    elif score == 7:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 3) and
                matching_myzands(state, player) >= 1 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 5) and
                state.has_group_unique("Spell", player, 1) and
                nice_to_haves(state, player, 3, 1) >= 8
               )
    elif score == 8:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 4) and
                matching_myzands(state, player) >= 2 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 6) and
                state.has_group_unique("Spell", player, 1) and
                nice_to_haves(state, player, 4, 2) >= 8
               )
    elif score == 9:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 4) and
                matching_myzands(state, player) >= 2 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 6) and
                state.has_group_unique("Spell", player, 1) and
                nice_to_haves(state, player, 4, 2) >= 9
               )
    elif score == 10:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 5) and
                matching_myzands(state, player) >= 3 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 8) and
                state.has_group_unique("Spell", player, 2) and
                nice_to_haves(state, player, 5, 3) >= 9
               )
    elif score == 11:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 5) and
                matching_myzands(state, player) >= 3 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 8) and
                state.has_group_unique("Spell", player, 2) and
                nice_to_haves(state, player, 5, 3) >= 10
               )
    elif score == 12:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 6) and
                matching_myzands(state, player) >= 4 and 
                can_upgrade(state, player) and
                state.has(i.metal_ore, player, 8) and
                state.has_group_unique("Spell", player, 2) and
                nice_to_haves(state, player, 6, 4) >= 10
               )
    elif score == 13:
        return (
                can_dash(tags, difficulty, state, player) and
                state.has_group_unique("Gun", player, 6) and
                matching_myzands(state, player) >= 4 and 
                state.has(i.metal_ore, player, 8) and
                state.has_group_unique("Spell", player, 2) and
                nice_to_haves(state, player, 6, 4) >= 12
               )
    else:
        raise ValueError(f"Score {score} is not a valid score. Something is wrong with the Frogmonster world.")
    
def nice_to_haves(state: CollectionState, player: int, req_gun: int, req_myz: int) -> int:
    count = 0

    if state.has(i.dash, player):
        count += 3

    count += health_count(state, player)

    bug_slot_value = [0, 0, 1, 1, 1, 2, 2, 2]
    count += bug_slot_value[min(state.count(i.bug_slot, player), 6)]

    if state.has_group("Spell", player, 1):
        count += 3
        count += mana_count(state, player)

    if state.has_any([i.beans, i.fireball], player):
        count += 1

    gun_count = state.count_group_unique("Gun", player)
    if req_gun < gun_count:
        count += gun_count - req_gun

    ore_value = [0, 1, 1, 2, 2, 2, 3, 3]
    if req_myz == 0 and can_upgrade(state, player):
        upgradables = min(gun_count, state.count(i.metal_ore, player))
        count += ore_value[upgradables]

    myz_count = state.count_group_unique("Gun Upgrade", player)
    if can_upgrade(state, player) and (req_myz < myz_count):
        count += myz_count - req_myz

    return count


def can_fight_all(names: Iterable[str], player: int, difficulty: Difficulty, state: CollectionState) -> bool:
    for name in names:
        if not can_fight(name, player, difficulty, state):
            return False
    return True

def can_fight_barge(difficulty: Difficulty, state: CollectionState, player: int):
    if difficulty == Difficulty.EASY:
        return (
            state.has_all([i.dash, i.fire_fruit_juicer], player) and 
            state.has_group_unique("Gun", player, 2) and
            health_count(state, player) >= 1
        )
    elif difficulty == Difficulty.NORMAL:
        return (
            state.has_all([i.dash, i.fire_fruit_juicer], player) and 
            state.has_group_unique("Gun", player, 2) and
            health_count(state, player) >= 1
        )
    elif difficulty == Difficulty.HARD:
        return (
            state.has(i.dash, player) and
            (state.has(i.fire_fruit_juicer, player) or has_level_2_gun(i.gatling_gun, state, player))
        )
    elif difficulty == Difficulty.VERY_HARD:
        return (
            state.has(i.fire_fruit_juicer, player) or has_level_2_gun(i.gatling_gun, state, player)
        )
    else:
        raise ValueError(f"Difficulty {difficulty} is not a valid type. Something is wrong with the Frogmonster world.")

def can_fight_chroma(difficulty: Difficulty, state: CollectionState, player: int):
    if difficulty == Difficulty.EASY:
        return state.has_any([i.machine_gun, i.reeder, i.gatling_gun], player) and state.has(i.dash, player) and state.has_group("Spell", player, 1) and state.has_group_unique("Gun", player, 3) and nice_to_haves(state, player, 3, 0) >= 6
    elif difficulty == Difficulty.NORMAL:
        return state.has_any([i.machine_gun, i.reeder, i.gatling_gun], player) and state.has(i.dash, player) and state.has_group("Spell", player, 1) and state.has_group_unique("Gun", player, 3)
    elif difficulty == Difficulty.HARD:
        return state.has_any([i.machine_gun, i.reeder, i.gatling_gun], player) and state.has(i.dash, player) and ((health_count(state, player) >= 1 or state.has_group("Spell", player, 1)))
    elif difficulty == Difficulty.VERY_HARD:
        return state.has_any([i.machine_gun, i.reeder, i.gatling_gun], player) and (state.has(i.dash, player) or (health_count(state, player) >= 1 and state.has_group("Spell", player, 1)))
    else:
        raise ValueError(f"Difficulty {difficulty} is not a valid type. Something is wrong with the Frogmonster world.")
    
def get_combat_data(name: str, difficulty: Difficulty) -> tuple[int, list[str], list[str], list[str]]:
    for combat in combat_data:
        if combat.name == name:
            if difficulty == Difficulty.EASY:
                return combat.score_easy, combat.need, combat.want, combat.tags
            elif difficulty == Difficulty.NORMAL:
                return combat.score_hard + 3, combat.need, combat.want, combat.tags
            elif difficulty == Difficulty.HARD:
                return combat.score_hard, combat.need, combat.want, combat.tags
            elif difficulty == Difficulty.VERY_HARD:
                return combat.score_very_hard, combat.need, combat.want, combat.tags
            else:
                raise ValueError(f"Difficulty {difficulty} not found in Difficulty enum. Something is wrong with the Frogmonster world.")
    raise ValueError(f"Combat {name} not found in data.py. Something is wrong with the Frogmonster world.")

def can_burn(state: CollectionState, player: int) -> bool:
    return (state.has(i.fire_fruit_juicer, player) or 
            state.has_all([i.fireball, i.cicada], player) or 
            (state.has_all([i.gatling_gun, i.gatling_gun_myzand_upgrade], player) and state.has(i.metal_ore, player, 14))
    )       # 14 ore here since if we're testing this, you don't have fire fruit, and thus can't waste ore on it

def can_burn_underwater(state: CollectionState, player: int) -> bool:
    return (state.has_all([i.fireball, i.cicada], player) or
            (state.has(i.fire_fruit_juicer, player) and can_upgrade(state, player) and state.has(i.metal_ore, player, 16)) or
            (state.has_all([i.gatling_gun, i.gatling_gun_myzand_upgrade], player) and can_upgrade(state, player) and state.has(i.metal_ore, player, 14))
    )
    
def can_dash(tags: list[str], dif: Difficulty, state: CollectionState, player: int) -> bool:
    if "underwater" in tags and dif >= Difficulty.HARD:
        return state.has_any([i.bass, i.dash], player)
    else:
        return state.has(i.dash, player)


def has_level_2_gun(gun: str, state: CollectionState, player: int) -> bool:
    return state.has(gun, player) and state.has(get_gun_upgrade_from_gun(gun), player) and state.has(i.metal_ore, player, 16) and can_upgrade(state, player)

def matching_myzands(state: CollectionState, player: int) -> int:
    count = 0
    for gun in myzand_gun_library:
        if gun is not i.seedling:
            if state.has(gun, player) and state.has(myzand_gun_library[gun], player):
                count += 1
        elif gun is i.seedling:
            if state.has(i.seedling_myzand_upgrade, player):
                count += 1
    return count

def health_count(state: CollectionState, player: int) -> int:
    count = 0
    if state.has(i.health, player, 3):
        if state.has(i.health, player, 6):
            count += 1
        count += 1
    if state.has_any(tanky_bugs, player):
        count += 1
    return count

def mana_count(state: CollectionState, player: int) -> int:
    count = 0
    if state.has(i.mana, player, 3):
        if state.has(i.mana, player, 6):
            count += 1
        count += 1
    if state.has_any(mana_bugs, player) and state.has(i.bug_slot, player, 1):
        count += 1
    return count

def can_upgrade(state: CollectionState, player: int) -> bool:
    return state.has(i.workshop_key, player) and state.can_reach(r.city, "Region", player)

def get_gun_upgrade_from_gun(gun: str) -> str:
    return myzand_gun_library[gun]
