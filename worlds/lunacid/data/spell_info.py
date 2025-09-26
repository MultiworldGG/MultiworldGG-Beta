from dataclasses import dataclass
from typing import List, Dict

from ..strings.properties import Types, Elements
from ..strings.spells import Spell, MobSpell, SpookySpell, CrimpusSpell


@dataclass(frozen=True)
class SpellInfo:
    name: str
    element: str
    style: str

    def __repr__(self):
        return f"{self.name} (Element: {self.element}, Style: {self.style})"


all_spells: List[SpellInfo] = []


def spell_information(name: str, element: str, style: str):
    spell = SpellInfo(name, element, style)
    all_spells.append(spell)
    return spell


base_spells = [
    spell_information(Spell.barrier, Elements.normal, Types.support),
    spell_information(Spell.bestial_communion, Elements.ignore, Types.support),
    spell_information(Spell.blood_drain, Elements.ignore, Types.melee),
    spell_information(Spell.blood_strike, Elements.poison, Types.ranged),
    spell_information(Spell.blue_flame_arc, Elements.fire, Types.melee),
    spell_information(Spell.coffin, Elements.ignore, Types.support),
    spell_information(Spell.corpse_transformation, Elements.ignore, Types.support),
    spell_information(Spell.earth_strike, Elements.normal, Types.ranged),
    spell_information(Spell.earth_thorn, Elements.normal, Types.melee),
    spell_information(Spell.fire_worm, Elements.fire, Types.melee),
    spell_information(Spell.flame_flare, Elements.fire, Types.melee),
    spell_information(Spell.flame_spear, Elements.fire, Types.ranged),
    spell_information(Spell.ghost_light, Elements.ignore, Types.support),
    spell_information(Spell.holy_warmth, Elements.ignore, Types.support),
    spell_information(Spell.icarian_flight, Elements.normal, Types.support),
    spell_information(Spell.ice_spear, Elements.ice, Types.ranged),
    spell_information(Spell.ice_tear, Elements.ice, Types.melee),
    spell_information(Spell.ignis_calor, Elements.fire, Types.melee),
    spell_information(Spell.lava_chasm, Elements.fire, Types.melee),
    spell_information(Spell.light_reveal, Elements.ignore, Types.support),
    spell_information(Spell.lightning, Elements.light, Types.ranged),
    spell_information(Spell.lithomancy, Elements.ignore, Types.support),
    spell_information(Spell.moon_beam, Elements.light, Types.ranged),
    spell_information(Spell.poison_mist, Elements.poison, Types.melee),
    spell_information(Spell.rock_bridge, Elements.normal, Types.support),
    spell_information(Spell.slime_orb, Elements.poison, Types.ranged),
    spell_information(Spell.spirit_warp, Elements.ignore, Types.support),
    spell_information(Spell.summon_fairy, Elements.ignore, Types.support),
    spell_information(Spell.summon_ice_sword, Elements.ice, Types.support),
    spell_information(Spell.wind_dash, Elements.normal, Types.support),
    spell_information(Spell.wind_slicer, Elements.normal, Types.ranged),
]

drop_spells = [
    spell_information(MobSpell.summon_snail, Elements.normal, Types.support),
    spell_information(MobSpell.dark_skull, Elements.dark, Types.ranged),
    spell_information(MobSpell.summon_kodama, Elements.ignore, Types.support),
    spell_information(MobSpell.tornado, Elements.normal, Types.melee),
    spell_information(MobSpell.quick_stride, Elements.normal, Types.support),
]

spooky_spells = [
    spell_information(SpookySpell.pumpkin_pop, Elements.dark, Types.ranged)
]

crimpus_spells = [
    spell_information(CrimpusSpell.jingle_bells, Elements.fire, Types.ranged)
]

ranged_spells = [spell.name for spell in all_spells if spell.style == Types.ranged]
support_spells = [spell.name for spell in all_spells if spell.style == Types.support]

all_spell_info_by_name: Dict[str, SpellInfo] = {spell.name: spell for spell in all_spells}
spells_by_element = {spell.name: spell.element for spell in all_spells}
