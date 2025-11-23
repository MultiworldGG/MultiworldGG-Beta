from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld


from BaseClasses import Item, ItemClassification
from .constants import *


class SonicHeroesItem(Item):
    game: str = SONICHEROES


def create_item(world: SonicHeroesWorld, name: str, classification: ItemClassification, amount: int = 1):
    for i in range(amount):
        world.multiworld.itempool.append(SonicHeroesItem(name, classification, world.item_name_to_id[name], world.player))

def create_filler_items(world: SonicHeroesWorld, amount: int):
    filler_list = world.multiworld.random.choices(list(filler_items_to_weights.keys()), weights=list(filler_items_to_weights.values()), k=amount)

    for name in filler_list:
        create_item(world, name, ItemClassification.filler)

def create_trap_items(world: SonicHeroesWorld, amount: int):
    trap_list = world.multiworld.random.choices(list(trap_items_to_weights.keys()), weights=list(trap_items_to_weights.values()), k=amount)

    for name in trap_list:
        create_item(world, name, ItemClassification.trap)


def create_items(world: SonicHeroesWorld):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))

    #create_item(world, EMBLEM, ItemClassification.progression)
    #total_location_count -= 1

    if world.options.sonic_story_starting_character != 0:
        create_item(world, get_playable_char_item_name(CHARSONIC), ItemClassification.progression)
        total_location_count -= 1

    if world.options.sonic_story_starting_character != 1:
        create_item(world, get_playable_char_item_name(CHARTAILS), ItemClassification.progression)
        total_location_count -= 1

    if world.options.sonic_story_starting_character != 2:
        create_item(world, get_playable_char_item_name(CHARKNUCKLES), ItemClassification.progression)
        total_location_count -= 1


    if world.options.ability_unlocks == 0:
        for region in world.regular_regions:
            for team in world.enabled_teams:
                for ability in get_all_abilities_for_team(team):
                    create_item(world, get_ability_item_name_without_world(team, region, ability), ItemClassification.progression)
                    total_location_count -= 1


    elif world.options.ability_unlocks == 1:
        for team in world.enabled_teams:
            for ability in get_all_abilities_for_team(team):
                create_item(world, get_ability_item_name_without_world(team, ALLREGIONS, ability), ItemClassification.progression)
                total_location_count -= 1


    if world.options.goal_unlock_condition >= 1:
        create_item(world, GREENCHAOSEMERALD, ItemClassification.progression)
        create_item(world, BLUECHAOSEMERALD, ItemClassification.progression)
        create_item(world, YELLOWCHAOSEMERALD, ItemClassification.progression)
        create_item(world, WHITECHAOSEMERALD, ItemClassification.progression)
        create_item(world, CYANCHAOSEMERALD, ItemClassification.progression)
        create_item(world, PURPLECHAOSEMERALD, ItemClassification.progression)
        create_item(world, REDCHAOSEMERALD, ItemClassification.progression)
        total_location_count -= 7



    world.extra_items = total_location_count

    #print(f"Extra Items count: {total_location_count}")

    create_filler_items(world, world.extra_items)
        #create_item(world, EXTRALIFE, ItemClassification.filler)


itemList: list[ItemData] = \
[
    ItemData(0x93930000, EMBLEM, ItemClassification.progression),
    ItemData(0x93930001, GREENCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930002, BLUECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930003, YELLOWCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930004, WHITECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930005, CYANCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930006, PURPLECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930007, REDCHAOSEMERALD, ItemClassification.progression),

    ItemData(0x93930008, get_playable_char_item_name(CHARSONIC), ItemClassification.progression),
    ItemData(0x93930009, get_playable_char_item_name(CHARTAILS), ItemClassification.progression),
    ItemData(0x9393000A, get_playable_char_item_name(CHARKNUCKLES), ItemClassification.progression),
    ItemData(0x9393000B, get_playable_char_item_name(CHARSHADOW), ItemClassification.progression),
    ItemData(0x9393000C, get_playable_char_item_name(CHARROUGE), ItemClassification.progression),
    ItemData(0x9393000D, get_playable_char_item_name(CHAROMEGA), ItemClassification.progression),
    ItemData(0x9393000E, get_playable_char_item_name(CHARAMY), ItemClassification.progression),
    ItemData(0x9393000F, get_playable_char_item_name(CHARCREAM), ItemClassification.progression),
    ItemData(0x93930010, get_playable_char_item_name(CHARBIG), ItemClassification.progression),
    ItemData(0x93930011, get_playable_char_item_name(CHARESPIO), ItemClassification.progression),
    ItemData(0x93930012, get_playable_char_item_name(CHARCHARMY), ItemClassification.progression),
    ItemData(0x93930013, get_playable_char_item_name(CHARVECTOR), ItemClassification.progression),
    ItemData(0x93930014, get_playable_char_item_name(CHARSUPERHARDSONIC), ItemClassification.progression),
    ItemData(0x93930015, get_playable_char_item_name(CHARSUPERHARDTAILS), ItemClassification.progression),
    ItemData(0x93930016, get_playable_char_item_name(CHARSUPERHARDKNUCKLES), ItemClassification.progression),


    #ItemData(0x93930200, get_ability_item_name_without_world(ANYTEAM, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930400, get_ability_item_name_without_world(SONIC, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930600, get_ability_item_name_without_world(DARK, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930800, get_ability_item_name_without_world(ROSE, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930A00, get_ability_item_name_without_world(CHAOTIX, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930C00, get_ability_item_name_without_world(SUPERHARD, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),

    #to 0xE00


    #StageOBJS
    #start at 0x1000
    #go to 0x1C00-ish


    ItemData(0x93931000, get_stage_obj_item_name_without_world(ANYTEAM, ALLREGIONS, ALLSTAGEOBJS), ItemClassification.progression),




    #ItemData(0x93930F00, char_levelup_to_item_name[SONIC][SPEED], ItemClassification.progression),
    #ItemData(0x93930F01, char_levelup_to_item_name[SONIC][FLYING], ItemClassification.progression),
    #ItemData(0x93930F02, char_levelup_to_item_name[SONIC][POWER], ItemClassification.progression),


    ItemData(0x93938000, EXTRALIFE, ItemClassification.filler),
    ItemData(0x93938001, RINGS5, ItemClassification.filler),
    ItemData(0x93938002, RINGS10, ItemClassification.filler),
    ItemData(0x93938003, RINGS20, ItemClassification.filler),
    ItemData(0x93938004, SHIELD, ItemClassification.filler),
    ItemData(0x93938005, INVINCIBILITY, ItemClassification.filler, fillerweight=0),
    #ItemData(0x93938006, SPEEDLEVELUP, ItemClassification.filler),
    #ItemData(0x93938007, FLYINGLEVELUP, ItemClassification.filler),
    #ItemData(0x93938008, POWERLEVELUP, ItemClassification.filler),
    #ItemData(0x93938009, TEAMLEVELUP, ItemClassification.filler, fillerweight=25),
    ItemData(0x9393800A, TEAMBLASTREFILL, ItemClassification.filler),
    ItemData(0x93938100, STEALTHTRAP, ItemClassification.trap),
    ItemData(0x93938101, FREEZETRAP, ItemClassification.trap),
    ItemData(0x93938102, NOSWAPTRAP, ItemClassification.trap),
    ItemData(0x93938103, RINGTRAP, ItemClassification.trap),
    ItemData(0x93938104, CHARMYTRAP, ItemClassification.trap),
]


filler_items_to_weights = \
    {item.name: item.fillerweight for item in itemList if item.classification == ItemClassification.filler}

trap_items_to_weights = \
    {item.name: item.fillerweight for item in itemList if item.classification == ItemClassification.trap}



item_id = 0x939301F0

for item_team in item_teams:
    hex_mod = item_id % 512
    item_id += (512 - hex_mod)

    for item_region in item_regions:
        for item_ability in item_abilities:
            #team_name = [k for k, v in locals().items() if v == team][0]
            #region_name = [k for k, v in locals().items() if v == region][0]
            #ability_name = [k for k, v in locals().items() if v == ability][0]
            #data.append(
            #    {
            #        "Entry": f"ItemData({hex(item_id).upper().replace("X", "x")}, get_ability_item_name_without_world({team_name}, {region_name}, {ability_name}), ItemClassification.progression),"
            #    })

            itemList.append(ItemData(item_id, get_ability_item_name_without_world(item_team, item_region, item_ability), ItemClassification.progression))
            item_id += 1

        hex_mod = item_id % 16
        item_id += (16 - hex_mod)


"""
item_id = 0x93930FFF

for item_team in item_teams:
    hex_mod = item_id % 4096
    item_id += (4096 - hex_mod)

    for item_region in item_regions:
        for stage_obj in stage_objs:
            #team_name = [k for k, v in locals().items() if v == team][0]
            #region_name = [k for k, v in locals().items() if v == region][0]
            #ability_name = [k for k, v in locals().items() if v == ability][0]
            #data.append(
            #    {
            #        "Entry": f"ItemData({hex(item_id).upper().replace("X", "x")}, get_ability_item_name_without_world({team_name}, {region_name}, {ability_name}), ItemClassification.progression),"
            #    })

            itemList.append(ItemData(item_id, get_stage_obj_item_name_without_world(item_team, item_region, stage_obj), ItemClassification.progression))
            item_id += 1

        hex_mod = item_id % 256
        item_id += (256 - hex_mod)
"""
