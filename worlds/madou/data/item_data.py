from dataclasses import dataclass
from typing import List, Dict, Tuple

from BaseClasses import ItemClassification
from ..strings.items import SpellItem, Tool, Special, Custom, Souvenir, Gem, Equip, Consumable, FlightUnlocks


@dataclass(frozen=True)
class MadouHexData:
    hex_address: int
    value: int


@dataclass(frozen=True)
class MadouItemData:
    code: int
    name: str
    group: str
    classification: ItemClassification
    hex_info: List[MadouHexData]

    def __repr__(self):
        return f"{self.code} {self.name} (Classification: {self.classification})"


all_items: List[MadouItemData] = []
hex_data_by_item: Dict[int, Tuple[str, List[MadouHexData]]] = {}
item_by_group: Dict[str, List[MadouItemData]] = {}


def create_item(code: int, name: str, group_name: str, classification: ItemClassification, hex_info: List[MadouHexData]):
    item_data = MadouItemData(code, name, group_name, classification, hex_info)
    hex_data_by_item[code] = (group_name, hex_info)
    all_items.append(item_data)
    if group_name not in item_by_group:
        item_by_group[group_name] = [item_data]
    else:
        item_by_group[group_name].append(item_data)

    return item_data


spell_start_id = 0
spell_items = [
    create_item(spell_start_id + 1, SpellItem.healing, "Spell", ItemClassification.useful, [MadouHexData(0x37, 4),]),
    create_item(spell_start_id + 2, SpellItem.fire, "Spell", ItemClassification.progression | ItemClassification.useful, [MadouHexData(0x39, 4),]),
    create_item(spell_start_id + 3, SpellItem.ice_storm, "Spell", ItemClassification.progression | ItemClassification.useful, [MadouHexData(0x3A, 4),]),
    create_item(spell_start_id + 4, SpellItem.thunder, "Spell", ItemClassification.progression | ItemClassification.useful, [MadouHexData(0x3B, 4),]),
    create_item(spell_start_id + 5, SpellItem.diacute, "Spell", ItemClassification.progression | ItemClassification.useful, [MadouHexData(0x36, 4),]),
    create_item(spell_start_id + 6, SpellItem.bayoen, "Spell", ItemClassification.progression | ItemClassification.useful, [MadouHexData(0x3D, 1),]),
    create_item(spell_start_id + 7, SpellItem.bayohihihi, "Spell", ItemClassification.useful, [MadouHexData(0x42, 1),]),
    create_item(spell_start_id + 8, SpellItem.braindumbed, "Spell", ItemClassification.useful, [MadouHexData(0x41, 1),]),
    create_item(spell_start_id + 9, SpellItem.jugem, "Spell", ItemClassification.useful, [MadouHexData(0x3C, 1),]),
    create_item(spell_start_id + 10, SpellItem.revia, "Spell", ItemClassification.useful, [MadouHexData(0x3F, 1),]),
    create_item(spell_start_id + 11, SpellItem.heedon, "Spell", ItemClassification.useful, [MadouHexData(0x40, 1),]),
]

tool_start_id = 20
tool_items = [
    create_item(tool_start_id + 1, Tool.ribbit_boots, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xb4, 0x03), MadouHexData(0xe0, 0x01),]),
    create_item(tool_start_id + 2, Tool.magic_bracelet, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x02), MadouHexData(0xdd, 0x01),]),
    create_item(tool_start_id + 3, Tool.panotty_flute, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x01), MadouHexData(0xdc, 0x01)]),
    create_item(tool_start_id + 4, Tool.magic_ribbon, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x06), MadouHexData(0xe1, 0x01)]),
    create_item(tool_start_id + 5, Tool.hammer, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x03), MadouHexData(0xde, 0x01)]),
    create_item(tool_start_id + 6, Tool.magical_dictionary, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x04), MadouHexData(0xdf, 0x01), MadouHexData(0x7b, 0x01)]),
    create_item(tool_start_id + 7, Tool.toy_elephant, "Tool", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x07), MadouHexData(0xe2, 0x01)]),
]

special_start_id = 30
special_items = [
    create_item(special_start_id + 1, Special.secret_stone, "Secret Stone", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xe3, 0x01),]),
    create_item(special_start_id + 2, Special.dark_orb, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4a),]),
    create_item(special_start_id + 3, Special.elephant_head, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4b), MadouHexData(0x79, 0x10)]),
    create_item(special_start_id + 4, Special.light_orb, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x49)]),
    create_item(special_start_id + 5, Special.ripe_cucumber, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x37), MadouHexData(0x80, 0x02)]),
    create_item(special_start_id + 6, Special.dark_flower, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4c)]),
    create_item(special_start_id + 7, Special.bazaar_pass, "Special Item", ItemClassification.progression,
                [MadouHexData(0xFF, 0x54), MadouHexData(0x84, 0x10)]),
    create_item(special_start_id + 8, Custom.bomb, "Event Item", ItemClassification.progression,
                [MadouHexData(0x7f, 0x10)]),
    create_item(special_start_id + 9, Special.firefly_egg, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4e)]),
    create_item(special_start_id + 10, Special.leaf, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4f)]),
    create_item(special_start_id + 11, Special.carbuncle, "Event Item", ItemClassification.useful | ItemClassification.trap,
                [MadouHexData(0x86, 0x20)]),
    create_item(special_start_id + 12, Special.squirrel_vip, "Special Item", ItemClassification.useful,
                [MadouHexData(0xFF, 0x55), MadouHexData(0x89, 0x08)]),
    create_item(special_start_id + 13, Special.wanderlust, "Special Item", ItemClassification.useful | ItemClassification.trap,
                [MadouHexData(0xFF, 0x41)]),
    create_item(special_start_id + 14, Special.wallet, "Special Item", ItemClassification.useful | ItemClassification.trap,
                [MadouHexData(0xFF, 0x42)]),
    create_item(special_start_id + 15, Special.bouquet, "Special Item", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x4d), MadouHexData(0x82, 0x40)]),
    create_item(special_start_id + 16, Special.rotted_cucumber, "Nothing", ItemClassification.filler,
                [MadouHexData(0xFF, 0xFF)]),  # Its "nothing".
]

souvenir_start_id = 50
souvenir_items = [
    create_item(souvenir_start_id + 1, Souvenir.magic_king_statue, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x5e)]),
    create_item(souvenir_start_id + 2, Souvenir.magic_king_picture, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x5f)]),
    create_item(souvenir_start_id + 3, Souvenir.magic_king_tusk, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x60)]),
    create_item(souvenir_start_id + 4, Souvenir.magic_king_foot, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x61)]),
    create_item(souvenir_start_id + 5, Souvenir.dragon_nail, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x62)]),
    create_item(souvenir_start_id + 6, Souvenir.waterfall_vase, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x63)]),
    create_item(souvenir_start_id + 7, Souvenir.dark_jug, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x66)]),
    create_item(souvenir_start_id + 8, Souvenir.wolf_tail, "Souvenir", ItemClassification.progression | ItemClassification.useful,
                [MadouHexData(0xFF, 0x67)]),
]

gem_start_id = 60
gem_items = [
    create_item(gem_start_id + 1, Gem.red_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x57), MadouHexData(0x96, 0x01)]),
    create_item(gem_start_id + 2, Gem.purple_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x5b), MadouHexData(0x96, 0x02)]),
    create_item(gem_start_id + 3, Gem.blue_gem,"Gem",  ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x58), MadouHexData(0x96, 0x04)]),
    create_item(gem_start_id + 4, Gem.cyan_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x5c), MadouHexData(0x96, 0x08)]),
    create_item(gem_start_id + 5, Gem.green_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x59), MadouHexData(0x96, 0x10)]),
    create_item(gem_start_id + 6, Gem.white_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x5d), MadouHexData(0x96, 0x20)]),
    create_item(gem_start_id + 7, Gem.yellow_gem, "Gem", ItemClassification.progression_skip_balancing,
                [MadouHexData(0xFF, 0x5a), MadouHexData(0x96, 0x40)]),
]

equip_start_id = 70
equip_items = [
    create_item(equip_start_id + 1, Equip.magic_ring_rala, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x43)]),
    create_item(equip_start_id + 2, Equip.magic_ring_rele, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x46)]),
    create_item(equip_start_id + 3, Equip.magic_ring_rili, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x44)]),
    create_item(equip_start_id + 4, Equip.magic_ring_rolo, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x47)]),
    create_item(equip_start_id + 5, Equip.magic_ring_rulu, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x45)]),
    create_item(equip_start_id + 6, Equip.magic_staff_papo, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x36)]),
    create_item(equip_start_id + 7, Equip.magic_staff_ray, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x32)]),
    create_item(equip_start_id + 8, Equip.magic_staff_miho, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x33)]),
    create_item(equip_start_id + 9, Equip.magic_staff_pici, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x34)]),
    create_item(equip_start_id + 10, Equip.magic_staff_lofu, "Equipment", ItemClassification.useful,
                [MadouHexData(0xFF, 0x35)]),
]

consumable_start_id = 90
consumable_items = [
    create_item(consumable_start_id + 1, Consumable.scallion, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x23)]),
    create_item(consumable_start_id + 2, Consumable.veggies, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x26)]),
    create_item(consumable_start_id + 3, Consumable.curry_rice, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x24)]),
    create_item(consumable_start_id + 4, Consumable.magic_wine, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x25)]),
    create_item(consumable_start_id + 5, Consumable.momomo_wine, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x28)]),
    create_item(consumable_start_id + 6, Consumable.dragon_meat, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x29)]),
    create_item(consumable_start_id + 7, Consumable.magic_crystal, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x2c)]),
    create_item(consumable_start_id + 8, Consumable.turtle_heart, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x3a)]),
    create_item(consumable_start_id + 9, Consumable.crown_grass, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x20)]),
    create_item(consumable_start_id + 10, Consumable.stroll_grass, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x21)]),
    create_item(consumable_start_id + 11, Consumable.cotton_ball_grass, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x22)]),
    create_item(consumable_start_id + 12, Consumable.medicine, "Consumable", ItemClassification.filler,
                [MadouHexData(0xFF, 0x3d)]),
    create_item(consumable_start_id + 13, Consumable.cookies, "Cookies", ItemClassification.filler,
                [MadouHexData(0x07, 0x00)]),
]

flight_start_id = 120
flight_items = [
    create_item(flight_start_id + 1, FlightUnlocks.wolf_town, "Flight Access", ItemClassification.progression,
                [MadouHexData(0x87, 0x01)]),
    create_item(flight_start_id + 2, FlightUnlocks.sage_mountain, "Flight Access", ItemClassification.progression,
                [MadouHexData(0x87, 0x04)]),
    create_item(flight_start_id + 3, FlightUnlocks.ruins_town, "Flight Access", ItemClassification.progression,
                [MadouHexData(0x86, 0x80)]),
    create_item(flight_start_id + 4, FlightUnlocks.ancient_village, "Flight Access", ItemClassification.progression,
                [MadouHexData(0x87, 0x02)]),
    create_item(flight_start_id + 5, FlightUnlocks.magic_village, "Flight Access", ItemClassification.progression,
                [MadouHexData(0x86, 0x40)])
]

filler_weights = {
    Consumable.scallion: 40,
    Consumable.veggies: 25,
    Consumable.momomo_wine: 20,
    Consumable.curry_rice: 20,
    Consumable.magic_wine: 40,
    Consumable.dragon_meat: 10,
    Consumable.magic_crystal: 5,
    Consumable.turtle_heart: 1,
    Consumable.stroll_grass: 1,
    Consumable.cotton_ball_grass: 1,
    Consumable.crown_grass: 1,
    Consumable.medicine: 1,
    Consumable.cookies: 25
}

items_on_flag_value = {}

inventory_items = []
allowed_groups = ["Special Item", "Gem", "Equipment", "Consumable", "Flight Access"]
for group in item_by_group:
    if group not in allowed_groups:
        continue
    for item in item_by_group[group]:
        inventory_items.append(item)
