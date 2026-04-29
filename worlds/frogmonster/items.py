from typing import NamedTuple, Dict, Optional

from BaseClasses import Item, ItemClassification
from .names import item_names as i

BASE_ID = 1  # Starting ID for both Frogmonster items and locations, moved out of __init__ to avoid circular imports

class FrogmonsterItem(Item):
    game = "Frogmonster"

class FrogmonsterItemData(NamedTuple):
    id: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    category: Optional[(str)] = None
    qty: int = 1

item_data_table: Dict[str, FrogmonsterItemData] = {

    # Items
    i.dash: FrogmonsterItemData(
        id=BASE_ID + 0,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Movement")
    ),
    i.sticky_hands: FrogmonsterItemData(
        id=BASE_ID + 1,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Movement")
    ),
    i.tongue_swing: FrogmonsterItemData(
        id=BASE_ID + 2,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Movement")
    ),
    i.runi_key: FrogmonsterItemData(
        id=BASE_ID + 3,
        type=ItemClassification.progression,
    ),
    i.glowbug: FrogmonsterItemData(
        id=BASE_ID + 4,
        type=ItemClassification.progression,
        category=("Bug")
    ),
    i.frog: FrogmonsterItemData(
        id=BASE_ID + 5,
        type=ItemClassification.progression,
        category=("Bug")
    ),
    i.fly: FrogmonsterItemData(
        id=BASE_ID + 6,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.dragonfly: FrogmonsterItemData(
        id=BASE_ID + 7,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.eel: FrogmonsterItemData(
        id=BASE_ID + 8,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.bass: FrogmonsterItemData(
        id=BASE_ID + 9,
        type=ItemClassification.progression,
        category=("Bug")
    ),
    i.blue_snack: FrogmonsterItemData(
        id=BASE_ID + 10,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.purple_snack: FrogmonsterItemData(
        id=BASE_ID + 11,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.magnet_roach: FrogmonsterItemData(
        id=BASE_ID + 12,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.mushroll: FrogmonsterItemData(
        id=BASE_ID + 13,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.mushfrog: FrogmonsterItemData(
        id=BASE_ID + 14,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.beet: FrogmonsterItemData(
        id=BASE_ID + 15,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.skater: FrogmonsterItemData(
        id=BASE_ID + 16,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.soul_frog: FrogmonsterItemData(
        id=BASE_ID + 17,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.river_fish: FrogmonsterItemData(
        id=BASE_ID + 18,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.bird: FrogmonsterItemData(
        id=BASE_ID + 19,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.leafbug: FrogmonsterItemData(
        id=BASE_ID + 20,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.wormy: FrogmonsterItemData(
        id=BASE_ID + 21,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.minnow: FrogmonsterItemData(
        id=BASE_ID + 22,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.turtle: FrogmonsterItemData(
        id=BASE_ID + 23,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.blue_jelly: FrogmonsterItemData(
        id=BASE_ID + 24,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.roof_snail: FrogmonsterItemData(
        id=BASE_ID + 25,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.crab: FrogmonsterItemData(
        id=BASE_ID + 26,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.bridge_frog: FrogmonsterItemData(
        id=BASE_ID + 27,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.cricket: FrogmonsterItemData(
        id=BASE_ID + 28,
        type=ItemClassification.progression,
        category=("Bug")
    ),
    i.spider: FrogmonsterItemData(
        id=BASE_ID + 29,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.moth: FrogmonsterItemData(
        id=BASE_ID + 30,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.ammofly: FrogmonsterItemData(
        id=BASE_ID + 31,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.pecker: FrogmonsterItemData(
        id=BASE_ID + 32,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.soul_fish: FrogmonsterItemData(
        id=BASE_ID + 33,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.fog_fly: FrogmonsterItemData(
        id=BASE_ID + 34,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.cicada: FrogmonsterItemData(
        id=BASE_ID + 35,
        type=ItemClassification.progression,
        category=("Bug")
    ),
    i.mantis: FrogmonsterItemData(
        id=BASE_ID + 36,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.jungle_snack: FrogmonsterItemData(
        id=BASE_ID + 37,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.gecko: FrogmonsterItemData(
        id=BASE_ID + 38,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.bee: FrogmonsterItemData(
        id=BASE_ID + 39,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.mushroom: FrogmonsterItemData(
        id=BASE_ID + 40,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.tang: FrogmonsterItemData(
        id=BASE_ID + 41,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.axolotyl: FrogmonsterItemData(
        id=BASE_ID + 42,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.mite: FrogmonsterItemData(
        id=BASE_ID + 43,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Bug")
    ),
    i.health: FrogmonsterItemData(
        id=BASE_ID + 44,
        type=ItemClassification.progression_deprioritized,
        category=("Health"),
        qty=6
    ),
#    i.health_2: FrogmonsterItemData(
#        id=BASE_ID + 45,
#        type=ItemClassification.useful,
#        category=("Health")
#    ),
#    i.health_3: FrogmonsterItemData(
#        id=BASE_ID + 46,
#        type=ItemClassification.useful,
#        category=("Health")
#    ),
#    i.health_4: FrogmonsterItemData(
#        id=BASE_ID + 47,
#        type=ItemClassification.useful,
#        category=("Health")
#    ),
#    i.health_5: FrogmonsterItemData(
#        id=BASE_ID + 48,
#        type=ItemClassification.useful,
#        category=("Health")
#    ),
#    i.health_6: FrogmonsterItemData(
#        id=BASE_ID + 49,
#        type=ItemClassification.useful,
#        category=("Health")
#    ),
    i.mana: FrogmonsterItemData(
        id=BASE_ID + 50,
        type=ItemClassification.progression_deprioritized,
        category=("Mana"),
        qty=6
    ),
#    i.mana_2: FrogmonsterItemData(
#        id=BASE_ID + 51,
#        type=ItemClassification.useful,
#        category=("Mana")
#    ),
#    i.mana_3: FrogmonsterItemData(
#        id=BASE_ID + 52,
#        type=ItemClassification.useful,
#        category=("Mana")
#    ),
#    i.mana_4: FrogmonsterItemData(
#        id=BASE_ID + 53,
#        type=ItemClassification.useful,
#        category=("Mana")
#    ),
#    i.mana_5: FrogmonsterItemData(
#        id=BASE_ID + 54,
#        type=ItemClassification.useful,
#        category=("Mana")
#    ),
#    i.mana_6: FrogmonsterItemData(
#        id=BASE_ID + 55,
#        type=ItemClassification.useful,
#        category=("Mana")
#    ),
    i.reeder: FrogmonsterItemData(
        id=BASE_ID + 56,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.machine_gun: FrogmonsterItemData(
        id=BASE_ID + 57,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.weepwood_bow: FrogmonsterItemData(
        id=BASE_ID + 58,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.finisher: FrogmonsterItemData(
        id=BASE_ID + 59,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.fire_fruit_juicer: FrogmonsterItemData(
        id=BASE_ID + 60,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.gatling_gun: FrogmonsterItemData(
        id=BASE_ID + 61,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.wooden_cannon: FrogmonsterItemData(
        id=BASE_ID + 62,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Gun")
    ),
    i.fireball: FrogmonsterItemData(
        id=BASE_ID + 63,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.mushbomb: FrogmonsterItemData(
        id=BASE_ID + 64,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.sharp_shot: FrogmonsterItemData(
        id=BASE_ID + 65,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.beans: FrogmonsterItemData(
        id=BASE_ID + 66,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.zap: FrogmonsterItemData(
        id=BASE_ID + 67,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.slam: FrogmonsterItemData(
        id=BASE_ID + 68,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.hive: FrogmonsterItemData(
        id=BASE_ID + 69,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.puff: FrogmonsterItemData(
        id=BASE_ID + 70,
        type=ItemClassification.progression,
        category=("Spell")
    ),
    i.bug_slot: FrogmonsterItemData(
        id=BASE_ID + 71,
        type=ItemClassification.progression_deprioritized,
        category=("Bug Slot"),
        qty=7
    ),
#    i.bug_slot_2: FrogmonsterItemData(
#        id=BASE_ID + 72,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
#    i.bug_slot_3: FrogmonsterItemData(
#        id=BASE_ID + 73,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
#    i.bug_slot_4: FrogmonsterItemData(
#        id=BASE_ID + 74,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
#    i.bug_slot_5: FrogmonsterItemData(
#        id=BASE_ID + 75,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
#    i.bug_slot_6: FrogmonsterItemData(
#        id=BASE_ID + 76,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
#    i.bug_slot_7: FrogmonsterItemData(
#        id=BASE_ID + 77,
#        type=ItemClassification.useful,
#        category=("Bug Slot")
#    ),
    i.metal_ore: FrogmonsterItemData(
        id=BASE_ID + 78,
        type=ItemClassification.progression_deprioritized_skip_balancing,
        category=("Metal Ore"),
        qty=19
    ),
#    i.metal_ore_2: FrogmonsterItemData(
#        id=BASE_ID + 79,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_3: FrogmonsterItemData(
#        id=BASE_ID + 80,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_4: FrogmonsterItemData(
#        id=BASE_ID + 81,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_5: FrogmonsterItemData(
#        id=BASE_ID + 82,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_6: FrogmonsterItemData(
#        id=BASE_ID + 83,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_7: FrogmonsterItemData(
#        id=BASE_ID + 84,
#        type=ItemClassification.useful,
#       category=("Metal Ore")
#    ),
#    i.metal_ore_8: FrogmonsterItemData(
#        id=BASE_ID + 85,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_9: FrogmonsterItemData(
#        id=BASE_ID + 86,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_10: FrogmonsterItemData(
#        id=BASE_ID + 87,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_11: FrogmonsterItemData(
#        id=BASE_ID + 88,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_12: FrogmonsterItemData(
#        id=BASE_ID + 89,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_13: FrogmonsterItemData(
#        id=BASE_ID + 90,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_14: FrogmonsterItemData(
#        id=BASE_ID + 91,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_15: FrogmonsterItemData(
#        id=BASE_ID + 92,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_16: FrogmonsterItemData(
#        id=BASE_ID + 93,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_17: FrogmonsterItemData(
#        id=BASE_ID + 94,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_18: FrogmonsterItemData(
#        id=BASE_ID + 95,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
#    i.metal_ore_19: FrogmonsterItemData(
#        id=BASE_ID + 96,
#        type=ItemClassification.useful,
#        category=("Metal Ore")
#    ),
    i.eel_trophy: FrogmonsterItemData(
        id=BASE_ID + 97,
        type=ItemClassification.progression,
    ),
    i.eye_fragment: FrogmonsterItemData(
        id=BASE_ID + 98,
        type=ItemClassification.filler,
    ),
    i.key: FrogmonsterItemData(
        id=BASE_ID + 99,
        type=ItemClassification.progression,
        category=("Key"),
        qty=3
    ),
#    i.key_2: FrogmonsterItemData(
#        id=BASE_ID + 100,
#        type=ItemClassification.useful,
#        category=("Key")
#    ),
#    i.key_3: FrogmonsterItemData(
#        id=BASE_ID + 101,
#        type=ItemClassification.useful,
#        category=("Key")
#    ),
    i.workshop_key: FrogmonsterItemData(
        id=BASE_ID + 100,
        type=ItemClassification.progression | ItemClassification.useful,
    ),
    i.orchus_key: FrogmonsterItemData(
        id=BASE_ID + 101,
        type=ItemClassification.progression | ItemClassification.useful,
    ),
    i.smooth_stone: FrogmonsterItemData(
        id=BASE_ID + 102,
        type=ItemClassification.filler,
        category=("Relic"),
        qty=11
    ),
#    i.smooth_stone_2: FrogmonsterItemData(
#        id=BASE_ID + 103,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_3: FrogmonsterItemData(
#        id=BASE_ID + 104,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_4: FrogmonsterItemData(
#        id=BASE_ID + 105,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_5: FrogmonsterItemData(
#        id=BASE_ID + 106,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_6: FrogmonsterItemData(
#        id=BASE_ID + 107,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_7: FrogmonsterItemData(
#        id=BASE_ID + 108,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_8: FrogmonsterItemData(
#        id=BASE_ID + 109,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_9: FrogmonsterItemData(
#        id=BASE_ID + 110,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_10: FrogmonsterItemData(
#        id=BASE_ID + 111,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_11: FrogmonsterItemData(
#        id=BASE_ID + 112,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.smooth_stone_12: FrogmonsterItemData(
#        id=BASE_ID + 113,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
    i.square_rock: FrogmonsterItemData(
        id=BASE_ID + 114,
        type=ItemClassification.filler,
        category=("Relic"),
        qty=10
    ),
#    i.square_rock_2: FrogmonsterItemData(
#        id=BASE_ID + 115,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_3: FrogmonsterItemData(
#        id=BASE_ID + 116,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_4: FrogmonsterItemData(
#        id=BASE_ID + 117,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_5: FrogmonsterItemData(
#        id=BASE_ID + 118,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_6: FrogmonsterItemData(
#        id=BASE_ID + 119,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_7: FrogmonsterItemData(
#        id=BASE_ID + 120,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_8: FrogmonsterItemData(
#        id=BASE_ID + 121,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_9: FrogmonsterItemData(
#        id=BASE_ID + 122,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.square_rock_10: FrogmonsterItemData(
#        id=BASE_ID + 123,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
    i.dark_pebble: FrogmonsterItemData(
        id=BASE_ID + 124,
        type=ItemClassification.filler,
        category=("Relic"),
        qty=8
    ),
#    i.dark_pebble_2: FrogmonsterItemData(
#        id=BASE_ID + 125,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_3: FrogmonsterItemData(
#        id=BASE_ID + 126,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_4: FrogmonsterItemData(
#        id=BASE_ID + 127,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_5: FrogmonsterItemData(
#        id=BASE_ID + 128,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_6: FrogmonsterItemData(
#        id=BASE_ID + 129,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_7: FrogmonsterItemData(
#        id=BASE_ID + 130,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.dark_pebble_8: FrogmonsterItemData(
#        id=BASE_ID + 131,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
    i.sparkling_gem: FrogmonsterItemData(
        id=BASE_ID + 132,
        type=ItemClassification.useful,
        category=("Relic"),
        qty=6
    ),
#    i.sparkling_gem_2: FrogmonsterItemData(
#        id=BASE_ID + 133,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.sparkling_gem_3: FrogmonsterItemData(
#        id=BASE_ID + 134,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.sparkling_gem_4: FrogmonsterItemData(
#        id=BASE_ID + 135,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.sparkling_gem_5: FrogmonsterItemData(
#        id=BASE_ID + 136,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
#    i.sparkling_gem_6: FrogmonsterItemData(
#        id=BASE_ID + 137,
#        type=ItemClassification.useful,
#        category=("Relic")
#    ),
    i.seedling_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 138,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.reeder_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 139,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.machine_gun_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 140,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.weepwood_bow_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 141,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.finisher_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 142,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.fire_fruit_juicer_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 143,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.gatling_gun_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 144,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.wooden_cannon_myzand_upgrade: FrogmonsterItemData(
        id=BASE_ID + 145,
        type=ItemClassification.progression | ItemClassification.useful,
        category=("Upgrade")
    ),
    i.coins: FrogmonsterItemData(
        id=BASE_ID + 146,
        type=ItemClassification.filler,
        qty=6
    ),
    
    # Events
    i.victory: FrogmonsterItemData(
        type=ItemClassification.progression
    ),
}

item_id_table = {name: data.id for name, data in item_data_table.items() if data.id is not None}

item_name_groups = {
    "Bug": {name for name, data in item_data_table.items() if data.category == ("Bug")},
    "Gun": {name for name, data in item_data_table.items() if data.category == ("Gun")},
    "Spell": {name for name, data in item_data_table.items() if data.category == ("Spell")},
    "Gun Upgrade": {name for name, data in item_data_table.items() if data.category == ("Upgrade")},
    # Aliases
    "Shotgun": {i.reeder},
    "Machine Gun": {i.machine_gun},
    "Bow": {i.weepwood_bow},
    "Grenade Launcher": {i.finisher},
    "Flamethrower": {i.fire_fruit_juicer},
    "Cannon": {i.wooden_cannon},
    "Pistol Myzand Upgrade": {i.seedling_myzand_upgrade},
    "Shotgun Myzand Upgrade": {i.reeder_myzand_upgrade},
    "Machine Gun Myzand Upgrade": {i.machine_gun_myzand_upgrade},
    "Bow Myzand Upgrade": {i.weepwood_bow_myzand_upgrade},
    "Grenade Launcher Myzand Upgrade": {i.finisher_myzand_upgrade},
    "Flamethrower Myzand Upgrade": {i.fire_fruit_juicer_myzand_upgrade},
    "Cannon Myzand Upgrade": {i.wooden_cannon_myzand_upgrade},
    "Pistol Upgrade": {i.seedling_myzand_upgrade},
    "Shotgun Upgrade": {i.reeder_myzand_upgrade},
    "Machine Gun Upgrade": {i.machine_gun_myzand_upgrade},
    "Bow Upgrade": {i.weepwood_bow_myzand_upgrade},
    "Grenade Launcher Upgrade": {i.finisher_myzand_upgrade},
    "Flamethrower Upgrade": {i.fire_fruit_juicer_myzand_upgrade},
    "Gatling Gun Upgrade": {i.gatling_gun_myzand_upgrade},
    "Cannon Upgrade": {i.wooden_cannon_myzand_upgrade},
    "Grapple": {i.tongue_swing},
    "Wall Climb": {i.sticky_hands},
    "Myzand Upgrade": {name for name, data in item_data_table.items() if data.category == ("Upgrade")},
}