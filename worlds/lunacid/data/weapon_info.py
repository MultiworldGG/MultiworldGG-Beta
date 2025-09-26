from dataclasses import dataclass
from typing import List

from ..strings.properties import Elements, Types
from ..strings.weapons import Weapon, SpookyWeapon


@dataclass(frozen=True)
class WeaponInfo:
    name: str
    element: str
    style: str

    def __repr__(self):
        return f"{self.name} (Element: {self.element}, Style: {self.style})"


all_weapons: List[WeaponInfo] = []


def weapon_information(name: str, element: str, style: str):
    weapons = WeaponInfo(name, element, style)
    all_weapons.append(weapons)
    return weapons


base_weapons = [
    weapon_information(Weapon.axe_of_harming, Elements.poison, Types.melee),
    weapon_information(Weapon.battle_axe, Elements.normal, Types.melee),
    weapon_information(Weapon.blade_of_jusztina, Elements.dark, Types.melee),
    weapon_information(Weapon.blade_of_ophelia, Elements.normal, Types.melee),
    weapon_information(Weapon.blessed_wind, Elements.normal, Types.melee),
    weapon_information(Weapon.broken_hilt, Elements.normal, Types.melee),
    weapon_information(Weapon.broken_lance, Elements.normal, Types.melee),
    weapon_information(Weapon.corrupted_dagger, Elements.dark, Types.melee),
    weapon_information(Weapon.dark_rapier, Elements.dark, Types.melee),
    weapon_information(Weapon.elfen_bow, Elements.normal, Types.ranged),
    weapon_information(Weapon.elfen_sword, Elements.normal, Types.melee),
    weapon_information(Weapon.fishing_spear, Elements.normal, Types.both),
    weapon_information(Weapon.marauder_black_flail, Elements.normal, Types.melee),
    weapon_information(Weapon.halberd, Elements.normal, Types.melee),
    weapon_information(Weapon.iron_claw, Elements.normal, Types.melee),
    weapon_information(Weapon.moonlight, Elements.light, Types.both),
    weapon_information(Weapon.obsidian_seal, Elements.dark, Types.melee),
    weapon_information(Weapon.replica_sword, Elements.normal, Types.melee),
    weapon_information(Weapon.ritual_dagger, Elements.poison, Types.melee),
    weapon_information(Weapon.serpent_fang, Elements.dark, Types.melee),
    weapon_information(Weapon.shadow_blade, Elements.dark, Types.melee),
    weapon_information(Weapon.steel_spear, Elements.normal, Types.melee),
    weapon_information(Weapon.stone_club, Elements.normal, Types.melee),
    weapon_information(Weapon.torch, Elements.fire, Types.melee),
    weapon_information(Weapon.twisted_staff, Elements.fire, Types.ranged),
    weapon_information(Weapon.vampire_hunter_sword, Elements.light, Types.melee),
    weapon_information(Weapon.wand_of_power, Elements.ignore, Types.ranged),
    weapon_information(Weapon.wolfram_greatsword, Elements.normal, Types.melee),
    weapon_information(Weapon.wooden_shield, Elements.normal, Types.melee),
    weapon_information(Weapon.crossbow, Elements.normal, Types.ranged),
    weapon_information(Weapon.steel_needle, Elements.normal, Types.melee),
    weapon_information(Weapon.lucid_blade, Elements.light, Types.both),
    weapon_information(Weapon.hammer_of_cruelty, Elements.dark_and_light, Types.melee),
    weapon_information(Weapon.thorn, Elements.normal, Types.melee),
    weapon_information(Weapon.ghost_sword, Elements.light, Types.melee),
]

shop_weapons = [
    weapon_information(Weapon.jotunn_slayer, Elements.dark_and_fire, Types.melee),
    weapon_information(Weapon.rapier, Elements.normal, Types.melee),
    weapon_information(Weapon.privateer_musket, Elements.dark, Types.ranged),
]

drop_weapons = [
    weapon_information(Weapon.rusted_sword, Elements.dark_and_fire, Types.melee),
    weapon_information(Weapon.ice_sickle, Elements.ice, Types.melee),
    weapon_information(Weapon.skeleton_axe, Elements.normal, Types.melee),
    weapon_information(Weapon.cursed_blade, Elements.dark, Types.melee),
    weapon_information(Weapon.brittle_arming_sword, Elements.normal, Types.melee),
    weapon_information(Weapon.obsidian_cursebrand, Elements.dark, Types.melee),
    weapon_information(Weapon.obsidian_poisonguard, Elements.dark, Types.melee),
    weapon_information(Weapon.golden_kopesh, Elements.normal, Types.melee),
    weapon_information(Weapon.golden_sickle, Elements.normal, Types.melee),
    weapon_information(Weapon.jailor_candle, Elements.fire, Types.ranged),
    weapon_information(Weapon.sucsarian_dagger, Elements.dark, Types.melee),
    weapon_information(Weapon.sucsarian_spear, Elements.dark, Types.melee),
    weapon_information(Weapon.lyrian_longsword, Elements.normal, Types.melee),
]

forge_weapons = [
    weapon_information(Weapon.lyrian_greatsword, Elements.normal, Types.melee),
    weapon_information(Weapon.dark_greatsword, Elements.dark, Types.melee),
    weapon_information(Weapon.shining_blade, Elements.light, Types.melee),
    weapon_information(Weapon.poison_claw, Elements.poison, Types.melee),
    weapon_information(Weapon.iron_club, Elements.normal, Types.melee),
    weapon_information(Weapon.iron_torch, Elements.fire, Types.melee),
    weapon_information(Weapon.fire_sword, Elements.fire, Types.melee),
    weapon_information(Weapon.steel_lance, Elements.normal, Types.melee),
    weapon_information(Weapon.double_crossbow, Elements.normal, Types.ranged),
    weapon_information(Weapon.death_scythe, Elements.dark_and_light, Types.melee),
    weapon_information(Weapon.elfen_longsword, Elements.normal, Types.melee),
    weapon_information(Weapon.steel_claw, Elements.normal, Types.melee),
    weapon_information(Weapon.steel_club, Elements.normal, Types.melee),
    weapon_information(Weapon.saint_ishii, Elements.dark_and_fire, Types.melee),
    weapon_information(Weapon.silver_rapier, Elements.light, Types.melee),
    weapon_information(Weapon.heritage_sword, Elements.normal, Types.melee),
]

alchemy_weapons = [
    weapon_information(Weapon.limbo, Elements.dark_and_light, Types.melee)
]

spooky_weapons = [
    weapon_information(SpookyWeapon.cavalry_saber, Elements.dark, Types.melee)
]

ranged_weapons = [weapon.name for weapon in all_weapons if weapon.style == Types.ranged or weapon.style == Types.both]
weapons_by_element = {weapon.name: weapon.element for weapon in all_weapons}


all_weapon_info_by_name = {weapon.name: weapon for weapon in all_weapons}
