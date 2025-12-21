from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule
from worlds.AutoWorld import World
from .Locations import food_locations, shop_locations, gleeok_locations, gohma_locations
from .ItemPool import dangerous_weapon_locations
from .Options import StartingPosition, CombatDifficulty
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import TLoZWorld

def can_use_bow(state: CollectionState, player: int, options: World):
    return (state.has("Bow", player) and (state.has("Arrow", player) or state.has("Silver Arrow", player)))

def has_sword(state: CollectionState, player: int, options: World):
    return (state.has("Sword", player) or state.has("White Sword", player) or state.has("Magical Sword", player))

def has_weapon(state: CollectionState, player: int, options: World):
    return (has_sword(state, player, options) or state.has("Magical Rod", player))

def can_farm(state: CollectionState, player: int, options: World):
    return (has_weapon(state, player, options) or state.has("Red Candle", player) or (options.BlueCandleFighting and state.has("Candle", player)))

def can_unlock(state: CollectionState, player: int, options: World):
    return (can_farm(state, player, options) or state.has("Magical Key", player))

def can_burn(state: CollectionState, player: int, options: World):
    return (state.has("Blue Candle", player) or state.has("Red Candle", player))

def can_light(state: CollectionState, player: int, options: World):
    return (can_burn(state, player, options) or (state.has("Magical Rod", player) and state.has("Book of Magic", player)) or options.LogicTrickBlindDarkRooms)

def can_kill_0_HP(state: CollectionState, player: int, options: World):
    return (can_farm(state, player, options) or state.has("Boomerang", player) or state.has("Magical Boomerang", player))

def can_kill_digdogger(state: CollectionState, player: int, options: World):
    return (can_farm(state, player, options) and state.has("Recorder", player))

def combat_help_points(state: CollectionState, player: int, options: World):
    defense_rating = 0
    offense_rating = 0
    if state.has("Red Ring", player):
        defense_rating = 2
    elif state.has("Blue Ring", player):
        defense_rating = 1
    if state.has("Magical Sword", player):
        offense_rating = 2
    elif (state.has("White Sword", player) or state.has("Magical Rod", player)):
        offense_rating = 1
    return (defense_rating + offense_rating)

def combat_help_points_wizzrobe(state: CollectionState, player: int, options: World):
    defense_rating = 0
    offense_rating = 0
    if state.has("Red Ring", player):
        defense_rating = 2
    elif state.has("Blue Ring", player):
        defense_rating = 1
    if state.has("Magical Sword", player):
        offense_rating = 2
    elif state.has("White Sword", player):
        offense_rating = 1
    return (defense_rating + offense_rating)

def easy_enemy_reqs(state: CollectionState, player: int, options: World):
    if options.CombatDifficulty == CombatDifficulty.option_veryeasy:
        return 1
    elif options.CombatDifficulty == CombatDifficulty.option_custom:
        return options.EasyEnemyCombatHelp
    else:
        return 0

def medium_enemy_reqs(state: CollectionState, player: int, options: World):
    if options.CombatDifficulty == CombatDifficulty.option_veryeasy:
        return 3
    elif options.CombatDifficulty == CombatDifficulty.option_easy:
        return 2
    elif options.CombatDifficulty == CombatDifficulty.option_normal:
        return 1
    elif options.CombatDifficulty == CombatDifficulty.option_custom:
        return options.MediumEnemyCombatHelp
    else:
        return 0

def hard_enemy_reqs(state: CollectionState, player: int, options: World):
    if options.CombatDifficulty == CombatDifficulty.option_veryeasy:
        return 4
    elif options.CombatDifficulty == CombatDifficulty.option_easy:
        return 4
    elif options.CombatDifficulty == CombatDifficulty.option_normal:
        return 3
    elif options.CombatDifficulty == CombatDifficulty.option_hard:
        return 2
    elif options.CombatDifficulty == CombatDifficulty.option_veryhard:
        return 1
    elif options.CombatDifficulty == CombatDifficulty.option_custom:
        return options.HardEnemyCombatHelp
    else:
        return 0

def pols_enemy_reqs(state: CollectionState, player: int, options: World):
    if options.CombatDifficulty == CombatDifficulty.option_veryeasy:
        return 4
    elif options.CombatDifficulty == CombatDifficulty.option_easy:
        return 3
    elif options.CombatDifficulty == CombatDifficulty.option_normal:
        return 2
    elif options.CombatDifficulty == CombatDifficulty.option_hard:
        return 1
    elif options.CombatDifficulty == CombatDifficulty.option_custom:
        return options.PolsVoiceCombatHelp
    else:
        return 0

def easy_fight(state: CollectionState, player: int, options: World):
    return (easy_enemy_reqs(state, player, options) <= combat_help_points(state, player, options))

def medium_fight(state: CollectionState, player: int, options: World):
    return (medium_enemy_reqs(state, player, options) <= combat_help_points(state, player, options))

def hard_fight(state: CollectionState, player: int, options: World):
    return (hard_enemy_reqs(state, player, options) <= combat_help_points(state, player, options))

def medium_fight_wizzrobe(state: CollectionState, player: int, options: World):
    return (medium_enemy_reqs(state, player, options) <= combat_help_points_wizzrobe(state, player, options))

def hard_fight_wizzrobe(state: CollectionState, player: int, options: World):
    return (hard_enemy_reqs(state, player, options) <= combat_help_points_wizzrobe(state, player, options))

def pols_fight(state: CollectionState, player: int, options: World):
    return (can_use_bow(state, player, options) or (has_weapon(state, player, options) and (pols_enemy_reqs(state, player, options) <= combat_help_points(state, player, options))))

def blue_wizzrobe_fight(state: CollectionState, player: int, options: World):
    return (((can_farm(state, player, options) and options.BlueWizzrobeBombs) or has_sword(state, player, options)) and hard_fight_wizzrobe(state, player, options))

def first_9_start(state: CollectionState, player: int, options: World):
    return (state.has("Triforce Fragment", player, 8) and (can_light(state, player, options) or state.has("Stepladder", player)))

def first_9_main(state: CollectionState, player: int, options: World):
    return (state.has("Triforce Fragment", player, 8) and can_light(state, player, options))

def set_rules(tloz_world: "TLoZWorld"):
    player = tloz_world.player
    options = tloz_world.options

    # Boss events for a nicer spoiler log play through
    for level in range(1, 9):
        boss = tloz_world.get_location(f"Level {level} Boss")
        boss_event = tloz_world.get_location(f"Level {level} Boss Status")
        status = tloz_world.create_event(f"Boss {level} Defeated")
        boss_event.place_locked_item(status)
        add_rule(boss_event, lambda state, b=boss: state.can_reach(b, "Location", player))

    # First Quest Overworld item requirements.
    # Since entrance requirements are handled elsewhere, most locations on the overworld
    # have no requirements at all.

    add_rule(tloz_world.get_location("White Sword Pond"),
             lambda state: state.has("Heart Container", player, 2))
    add_rule(tloz_world.get_location("Magical Sword Grave"),
             lambda state: state.has("Heart Container", player, 9))
    add_rule(tloz_world.get_location("Ocean Heart Container"),
             lambda state: state.has("Stepladder", player))

    # 1st-1 item requirements.
    # Note that the two Stalfos holding keys don't require combat, simply walking into them.

    add_rule(tloz_world.get_location("Level 1 Key Drop (Keese Entrance)"),
             lambda state: (can_kill_0_HP(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 1 Key Drop (Stalfos Middle)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 1 Compass"),
             lambda state: (can_unlock(state, player, options) or options.LogicTrickq1d1KeyDoor))
    add_rule(tloz_world.get_location("Level 1 Map"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 1 Key Drop (Stalfos Water)"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 1 Key Drop (Moblins)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 1 Item (Bow)"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 1 Item (Boomerang)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 1 Key Drop (Wallmasters)"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 1 Boss"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 1 Triforce"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))

    # 1st-2 item requirements.
    #Despite how deep it is, the Keese bomb drop is actually 100% free.

    add_rule(tloz_world.get_location("Level 2 Key Drop (Ropes West)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Key Drop (Ropes Entrance)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Compass"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 2 Map"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 2 Key Drop (Ropes Middle)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Item (Magical Boomerang)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Key Drop (Moldorms)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Rupee Drop (Gels)"),
             lambda state: (can_unlock(state, player, options) and can_kill_0_HP(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Bomb Drop (Moblins)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Boss"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 2 Triforce"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))

    # 1st-3 item requirements.

    add_rule(tloz_world.get_location("Level 3 Key Drop (Zols South)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Bomb Drop (Darknuts Central)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Key Drop (Zols Central)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Map"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 3 Bomb Drop (Keese Corridor)"),
             lambda state: (can_unlock(state, player, options) and can_kill_0_HP(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Key Drop (Zols and Keese West)"),
             lambda state: can_unlock(state, player, options))
    add_rule(tloz_world.get_location("Level 3 Bomb Drop (Darknuts West)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Item (Raft)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Key Drop (Keese North)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Rupee Drop (Zols and Keese East)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Boss"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 3 Triforce"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))

    # 1st-4 item requirements.

    add_rule(tloz_world.get_location("Level 4 Key Drop (Keese Entrance)"),
             lambda state: (can_kill_0_HP(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 4 Compass"),
             lambda state: (can_unlock(state, player, options) and can_light(state, player, options)))
    add_rule(tloz_world.get_location("Level 4 Key Drop (Zols)"),
             lambda state: can_light(state, player, options))
    add_rule(tloz_world.get_location("Level 4 Item (Stepladder)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 4 Map"),
             lambda state: (can_unlock(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 4 Key Drop (Keese North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 4 Boss"),
             lambda state: (has_weapon(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 4 Triforce"),
             lambda state: (has_weapon(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and hard_fight(state, player, options)))

    # 1st-5 item requirements.
    # Walking into Gibdos is scary but survivable even at 3 hearts with no ring.

    add_rule(tloz_world.get_location("Level 5 Key Drop (Pols Voice Entrance)"),
             lambda state: pols_fight(state, player, options))
    add_rule(tloz_world.get_location("Level 5 Key Drop (Gibdos Entrance)"),
             lambda state: can_light(state, player, options))
    add_rule(tloz_world.get_location("Level 5 Bomb Drop (Gibdos)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Item (Recorder)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Key Drop (Keese North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and hard_fight(state, player, options)))
    # Currently, bomb upgrades are not in the item pool, but if they were, the 1st-5 bomb upgrade would share requirements with the above.
    add_rule(tloz_world.get_location("Level 5 Key Drop (Zols)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Bomb Drop (Dodongos)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Map"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Rupee Drop (Zols)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Key Drop (Gibdos Central)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Compass"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Key Drop (Gibdos, Keese, and Pols Voice)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Key Drop (Gibdos North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Boss"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 5 Triforce"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))

    # 1st-6 item requirements.

    add_rule(tloz_world.get_location("Level 6 Key Drop (Wizzrobes Entrance)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and medium_fight_wizzrobe(state, player, options)))
    add_rule(tloz_world.get_location("Level 6 Compass"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 6 Key Drop (Keese)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 6 Rupee Drop (Wizzrobes)"),
             lambda state: blue_wizzrobe_fight(state, player, options))
    # Doing the next two checks without a dark room involves fighting an extra Gleeok which no one will actually do, but it's logical.
    add_rule(tloz_world.get_location("Level 6 Map"),
             lambda state: blue_wizzrobe_fight(state, player, options))
    add_rule(tloz_world.get_location("Level 6 Item (Magical Rod)"),
             lambda state: blue_wizzrobe_fight(state, player, options))
    add_rule(tloz_world.get_location("Level 6 Key Drop (Wizzrobes North Stream)"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 6 Key Drop (Wizzrobes North Island)"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 6 Key Drop (Vires)"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 6 Bomb Drop (Wizzrobes)"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 6 Boss"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and can_use_bow(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 6 Triforce"),
             lambda state: (blue_wizzrobe_fight(state, player, options) and can_light(state, player, options) and can_use_bow(state, player, options) and state.has("Stepladder", player)))

    # 1st-7 item requirements.
    # Because first quest has only one hungry Goriya, food can be checked for as a normal progression item without caring if it is from a shop.

    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Moldorms South)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Rupee Drop (Dodongos)"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Key Drop (Stalfos)"),
             lambda state: can_light(state, player, options))
    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Goriyas South)"),
             lambda state: (can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Key Drop (Ropes)"),
             lambda state: can_farm(state, player, options))
    # Currently, bomb upgrades are not in the item pool, but if they were, the 1st-7 bomb upgrade would share requirements with the above.
    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Keese and Spikes)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Rupee Drop (Dodongos)"),
             lambda state: (can_farm(state, player, options) and easy_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Compass"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and (medium_fight(state, player, options) or state.has("Stepladder", player))))
    add_rule(tloz_world.get_location("Level 7 Key Drop (Moldorms)"),
             lambda state: (can_farm(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Rupee Drop (Goriyas Central)"),
             lambda state: (can_farm(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Rupee Drop (Goriyas Central)"),
             lambda state: (can_farm(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Map"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Rupee Drop (Goriyas North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Key Drop (Goriyas)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Item (Red Candle)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Goriyas North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Moldorms North)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Bomb Drop (Dodongos)"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Boss"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 7 Triforce"),
             lambda state: (can_kill_digdogger(state, player, options) and can_light(state, player, options) and state.has("Stepladder", player) and state.has("Food", player) and medium_fight(state, player, options)))

    # 1st-8 item requirements.

    add_rule(tloz_world.get_location("Level 8 Key Drop (Keese and Zols Entrance)"),
             lambda state: (can_light(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 8 Rupee Drop (Manhandla Entrance West)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Item (Book of Magic)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Rupee Drop (Manhandla Entrance North)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Key Drop (Darknuts Central)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Compass"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Key Drop (Pols Voice and Keese)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Key Drop (Darknuts West)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Rupee Drop (Darknuts and Gibdos)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Map"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Bomb Drop (Pols Voice North)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options) and pols_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Bomb Drop (Darknuts North)"),
             lambda state: (can_farm(state, player, options) and can_use_bow(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Item (Magical Key)"),
             lambda state: (can_farm(state, player, options) and can_use_bow(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Bomb Drop (Darknuts East)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Key Drop (Pols Voice South)"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    # You can avoid clearing the Pols Voice by bombing through the boss room as a connection.
    add_rule(tloz_world.get_location("Level 8 Key Drop (Darknuts Far West)"),
             lambda state: (can_farm(state, player, options) and can_light(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Boss"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 8 Triforce"),
             lambda state: (can_farm(state, player, options) and hard_fight(state, player, options)))

    # 1st-9 item requirements.
    # The big point in here is how early you can pick between a Stepladder or dark room block,
    # then you run into a hard dark room block soon, and you can always avoid the Stepladder to continue forward.
    # Once you grasp that basic structure, most of the actual maze isn't a logical issue.

    add_rule(tloz_world.get_location("Level 9 Key Drop (Like Likes and Zols East)"),
             lambda state: (first_9_start(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Wizzrobes Central)"),
             lambda state: (first_9_start(state, player, options) and can_farm(state, player, options) and medium_fight_wizzrobe(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Keese Central Island)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and state.has("Stepladder", player) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Bomb Drop (Gels Lake)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Red Lanmolas)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Bomb Drop (Blue Lanmolas)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Wizzrobes North Island)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options) and state.has("Stepladder", player)))
    # Doing this next check with the Blue Candle and Bombs as your only weapons would be uniquely awful, but
    # if you seriously checked that box with settings that somehow got you into 9 with that, have fun.
    add_rule(tloz_world.get_location("Level 9 Bomb Drop (Like Likes and Zols Corridor)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Compass"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Bomb Drop (Patra Northeast)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Gels East)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Bomb Drop (Vires)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Key Drop (Wizzrobes and Bubbles East)"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and medium_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Key Drop (Wizzrobes East Island)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Level 9 Map"),
             lambda state: (first_9_main(state, player, options) and can_farm(state, player, options) and hard_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Item (Red Ring)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Keese Southwest)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Key Drop (Patra Southwest)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Item (Silver Arrow)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options)))
    add_rule(tloz_world.get_location("Level 9 Rupee Drop (Wizzrobes West Island)"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options) and state.has("Stepladder", player)))
    add_rule(tloz_world.get_location("Ganon"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options) and has_sword(state, player, options) and can_use_bow(state, player, options) and state.has("Silver Arrow", player)))
    add_rule(tloz_world.get_location("Zelda"),
             lambda state: (first_9_main(state, player, options) and blue_wizzrobe_fight(state, player, options) and has_sword(state, player, options) and can_use_bow(state, player, options) and state.has("Silver Arrow", player)))
    
    # No requiring anything in a shop until we can farm for money
    for location in shop_locations:
        add_rule(tloz_world.get_location(location),
                 lambda state: can_farm(state, player, options))

    # Yes we are looping this range again for Triforce locations. No I can't add it to the boss event loop
    for level in range(1, 9):
        add_rule(tloz_world.get_location(f"Level {level} Triforce"),
                 lambda state, l=level: state.has(f"Boss {l} Defeated", player))

    # Don't allow Take Any Items until we can actually get in one
    # I'm going to comment out some of this stuff that the ER side should be handling just in case it's helpful to have.
    """if options.ExpandedPool:
        add_rule(tloz_world.get_location("Take Any Item Left"),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))
        add_rule(tloz_world.get_location("Take Any Item Middle"),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))
        add_rule(tloz_world.get_location("Take Any Item Right"),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))"""

    add_rule(tloz_world.get_location("Potion Shop Item Left"),
             lambda state: state.has("Letter", player))
    add_rule(tloz_world.get_location("Potion Shop Item Middle"),
             lambda state: state.has("Letter", player))
    add_rule(tloz_world.get_location("Potion Shop Item Right"),
             lambda state: state.has("Letter", player))

    """add_rule(tloz_world.get_location("Shield Shop Item Left"),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))
    add_rule(tloz_world.get_location("Shield Shop Item Middle"),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))
    add_rule(tloz_world.get_location("Shield Shop Item Right"),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))"""

    ganon = tloz_world.get_location("Ganon")
    ganon.place_locked_item(tloz_world.create_event("Triforce of Power"))

    tloz_world.get_location("Zelda").place_locked_item(tloz_world.create_event("Rescued Zelda!"))
    add_rule(tloz_world.get_location("Zelda"),
             lambda state: state.has("Triforce of Power", player))
    tloz_world.multiworld.completion_condition[player] = lambda state: state.has("Rescued Zelda!", player)
