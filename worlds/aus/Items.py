from BaseClasses import Item, ItemClassification
from typing import Dict, NamedTuple, Optional
from .Names import *

class AUSItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification

class AUSItem(Item):
    game: str = "An Untitled Story"

item_table = {
    I_JUMP_UPGRADE: AUSItemData(72001, ItemClassification.progression),
    I_RED_ENERGY: AUSItemData(72004, ItemClassification.progression),
    I_LUCKY_POTS: AUSItemData(72005, ItemClassification.useful),
    I_DOUBLE_JUMP: AUSItemData(72006, ItemClassification.progression),
    I_DUCKING: AUSItemData(72009, ItemClassification.progression),
    I_STICKING: AUSItemData(72010, ItemClassification.progression),
    # TELEPORT: AUSItemData(72012, ItemClassification.progression), # given automatically
    I_DIVE_BOMB: AUSItemData(72013, ItemClassification.progression),
    I_SHOOT_FIRE: AUSItemData(72014, ItemClassification.progression),
    I_YELLOW_ENERGY: AUSItemData(72016, ItemClassification.progression),
    I_HATCH: AUSItemData(72017, ItemClassification.progression),
    I_AIR_UPGRADE: AUSItemData(72018, ItemClassification.progression_skip_balancing),
    I_MAGNETISM: AUSItemData(72020, ItemClassification.useful),
    I_SHOOT_ICE: AUSItemData(72021, ItemClassification.progression),
    I_TOUGHNESS: AUSItemData(72022, ItemClassification.useful),
    I_HEART: AUSItemData(72100, ItemClassification.filler),
    I_GOLD_ORB: AUSItemData(72200, ItemClassification.progression_skip_balancing),
    I_FLOWER: AUSItemData(72300, ItemClassification.progression_skip_balancing),
    "10 Crystals": AUSItemData(72401, ItemClassification.filler),
    "25 Crystals": AUSItemData(72402, ItemClassification.filler),
    "35 Crystals": AUSItemData(72403, ItemClassification.filler),
    "50 Crystals": AUSItemData(72405, ItemClassification.progression_deprioritized_skip_balancing),
    "75 Crystals": AUSItemData(72406, ItemClassification.progression_deprioritized_skip_balancing),
    "110 Crystals": AUSItemData(72407, ItemClassification.progression_deprioritized_skip_balancing),
    "65 Crystals": AUSItemData(72408, ItemClassification.progression_deprioritized_skip_balancing),
    "125 Crystals": AUSItemData(72409, ItemClassification.progression_deprioritized_skip_balancing),
    "180 Crystals": AUSItemData(72410, ItemClassification.progression_deprioritized_skip_balancing),
    "270 Crystals": AUSItemData(72411, ItemClassification.progression_deprioritized_skip_balancing),
    "150 Crystals": AUSItemData(72412, ItemClassification.progression_deprioritized_skip_balancing),
    "200 Crystals": AUSItemData(72414, ItemClassification.progression_deprioritized_skip_balancing),
    "235 Crystals": AUSItemData(72417, ItemClassification.progression_deprioritized_skip_balancing),
    "245 Crystals": AUSItemData(72418, ItemClassification.progression_deprioritized_skip_balancing),
    "400 Crystals": AUSItemData(72419, ItemClassification.progression_deprioritized_skip_balancing),
    "300 Crystals": AUSItemData(72420, ItemClassification.progression_deprioritized_skip_balancing),
    "100 Crystals": AUSItemData(72421, ItemClassification.progression_deprioritized_skip_balancing),
    VICTORY: AUSItemData(None, ItemClassification.progression)
}

item_pool: Dict[str, int] = {
    I_JUMP_UPGRADE: 3,
    I_DOUBLE_JUMP: 3,
    I_STICKING: 2,
    I_SHOOT_FIRE: 2,
    I_AIR_UPGRADE: 2,
    I_TOUGHNESS: 3,
    I_HEART: 92,
    I_GOLD_ORB: 10,
    I_FLOWER: 20,
    "35 Crystals": 2,
    "150 Crystals": 2,
    "200 Crystals": 3,
}