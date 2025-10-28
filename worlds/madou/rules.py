from typing import TYPE_CHECKING, Dict, List

from BaseClasses import CollectionState
from .strings.locations import HarpyPath, Spell, ShadyWell, DarkForest, ForestOfLight, LightGarden, MagicTown, \
    SatanVilla, AncientRuins, School, \
    AncientVillage, DragonAreas, Bestiary, LookoutMountain, SageMountain, Bazaar
from .strings.region_entrances import MadouEntrance
from .strings.items import Tool, Custom, Special, Souvenir, EventItem, Gem, SpellItem, FlightUnlocks
from .options import MadouOptions
from worlds.generic.Rules import CollectionRule

if TYPE_CHECKING:
    from . import MadouWorld


class MadouRules:
    world: "MadouWorld"
    region_rules: Dict[str, CollectionRule]
    entrance_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "MadouWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options

        self.region_rules = {

        }

        self.entrance_rules = {
            MadouEntrance.village_to_nw_cave: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.nw_cave_to_village: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.forest_to_frog: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.frog_to_forest: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.ruins_to_ancient_ruins: lambda state: state.has(Tool.magic_bracelet, self.player),
            MadouEntrance.rain_forest_to_ancient_village: lambda state: state.has(Tool.hammer, self.player),
            MadouEntrance.ancient_to_zoh: lambda state: state.has(Special.elephant_head, self.player),
            MadouEntrance.nw_cave_to_smoky: lambda state: state.has(Custom.bomb, self.player),
            MadouEntrance.death_to_bazaar: lambda state: state.has(Special.bazaar_pass, self.player) and state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.smoky_left_to_right: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.magic_village_to_tower: lambda state: self.can_fight_generic_at_level(state, 5, self.world.options) and
                                                                state.has("Final Exam Certificate", self.player),
            MadouEntrance.headmaster_to_school_maze: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            MadouEntrance.smoky_to_graveyard: lambda state: state.has(Special.dark_flower, self.player) and state.has(Special.leaf, self.player),
            MadouEntrance.dark_forest_to_well: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.dark_forest_to_satan: lambda state: state.has(Tool.ribbit_boots, self.player) and state.has(Special.secret_stone, self.player, 3),
            MadouEntrance.dark_forest_to_maze: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.dark_forest_to_dark_orb: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.wolf_to_sage: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.sage_to_wolf: lambda state: state.has(Tool.ribbit_boots, self.player),
            MadouEntrance.sage_to_summit: lambda state: state.has(Tool.ribbit_boots, self.player),
            # TODO: find a way to make the game accept a flight path even if you only have one; this isn't very intuitive.
            MadouEntrance.flight_magic_to_ruins: lambda state: state.has(FlightUnlocks.ruins_town, self.player) and
                                                               self.has_any_flight_path_other_than(FlightUnlocks.ruins_town, state),
            MadouEntrance.flight_magic_to_wolf: lambda state: state.has(FlightUnlocks.wolf_town, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.wolf_town, state),
            MadouEntrance.flight_magic_to_ancient: lambda state: state.has(FlightUnlocks.ancient_village, self.player) and
                                                                 self.has_any_flight_path_other_than(FlightUnlocks.ancient_village, state),
            MadouEntrance.flight_magic_to_sage: lambda state: state.has(FlightUnlocks.sage_mountain, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain, state),
            MadouEntrance.flight_ruins_to_magic: lambda state: state.has(FlightUnlocks.magic_village, self.player) and
                                                               self.has_any_flight_path_other_than(FlightUnlocks.magic_village, state),
            MadouEntrance.flight_ruins_to_ancient: lambda state: state.has(FlightUnlocks.ancient_village, self.player) and
                                                                 self.has_any_flight_path_other_than(FlightUnlocks.ancient_village, state),
            MadouEntrance.flight_ruins_to_wolf: lambda state: state.has(FlightUnlocks.wolf_town, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.wolf_town, state),
            MadouEntrance.flight_ruins_to_sage: lambda state: state.has(FlightUnlocks.sage_mountain, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain, state),
            MadouEntrance.flight_wolf_to_magic: lambda state: state.has(FlightUnlocks.magic_village, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.magic_village, state),
            MadouEntrance.flight_wolf_to_ruins: lambda state: state.has(FlightUnlocks.ruins_town, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.ruins_town, state),
            MadouEntrance.flight_wolf_to_ancient: lambda state: state.has(FlightUnlocks.ancient_village, self.player) and
                                                                self.has_any_flight_path_other_than(FlightUnlocks.ancient_village, state),
            MadouEntrance.flight_wolf_to_sage: lambda state: state.has(FlightUnlocks.sage_mountain, self.player) and
                                                             self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain, state),
            MadouEntrance.flight_ancient_to_magic: lambda state: state.has(FlightUnlocks.magic_village, self.player) and
                                                                 self.has_any_flight_path_other_than(FlightUnlocks.magic_village, state),
            MadouEntrance.flight_ancient_to_ruins: lambda state: state.has(FlightUnlocks.ruins_town, self.player) and
                                                                 self.has_any_flight_path_other_than(FlightUnlocks.ruins_town, state),
            MadouEntrance.flight_ancient_to_wolf: lambda state: state.has(FlightUnlocks.wolf_town, self.player) and
                                                                self.has_any_flight_path_other_than(FlightUnlocks.wolf_town, state),
            MadouEntrance.flight_ancient_to_sage: lambda state: state.has(FlightUnlocks.sage_mountain, self.player) and
                                                                self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain, state),
            MadouEntrance.flight_sage_to_magic: lambda state: state.has(FlightUnlocks.magic_village, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.magic_village, state),
            MadouEntrance.flight_sage_to_ruins: lambda state: state.has(FlightUnlocks.ruins_town, self.player) and
                                                              self.has_any_flight_path_other_than(FlightUnlocks.ruins_town, state),
            MadouEntrance.flight_sage_to_wolf: lambda state: state.has(FlightUnlocks.wolf_town, self.player) and
                                                             self.has_any_flight_path_other_than(FlightUnlocks.wolf_town, state),
            MadouEntrance.flight_sage_to_ancient: lambda state: state.has(FlightUnlocks.ancient_village, self.player) and
                                                                self.has_any_flight_path_other_than(FlightUnlocks.ancient_village, state),
        }

        self.location_rules = {
            MagicTown.magic_bracelet: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            SatanVilla.satan: lambda state: state.has(Special.secret_stone, self.player, 3),
            ForestOfLight.sukiyapodes_2: lambda state: state.has(Special.light_orb, self.player),
            Spell.thunder_dark_forest: lambda state: state.has(Tool.ribbit_boots, self.player),
            Spell.diacute_dark_forest: lambda state: state.has(Tool.ribbit_boots, self.player),
            DarkForest.green_gem: lambda state: state.has(Tool.ribbit_boots, self.player),
            DarkForest.dark_flower: lambda state: state.has(Special.dark_orb, self.player),
            LightGarden.purple_orb: lambda state: state.has(Tool.toy_elephant, self.player),
            LightGarden.bouquet: lambda state: state.has(Special.leaf, self.player) and state.has(Special.dark_flower, self.player) and state.has(EventItem.unpetrify,
                                                                                                                                      self.player),
            ShadyWell.lofu: lambda state: state.has(Tool.toy_elephant, self.player),
            SageMountain.cyan_orb: lambda state: state.has(Tool.toy_elephant, self.player) and state.has(Tool.ribbit_boots, self.player),
            DarkForest.rele: lambda state: state.has(Tool.toy_elephant, self.player),
            MagicTown.white_gem: lambda state: self.has_souvenirs(state, self.world.options),
            LookoutMountain.red_gem: lambda state: state.has(Tool.ribbit_boots, self.player),
            #  Gold Tablets
            Spell.fire_school: lambda state: state.has(Tool.magical_dictionary, self.player),
            Spell.fire_library: lambda state: self.has_gems(state) and state.has(Tool.magical_dictionary, self.player),
            Spell.ice_storm_underground: lambda state: state.has(Tool.magical_dictionary, self.player),
            Spell.ice_storm_library: lambda state: self.has_gems(state) and state.has(Tool.magical_dictionary, self.player),
            Spell.thunder_northwestern: lambda state: state.has(Tool.magic_ribbon, self.player) and state.has(Tool.magical_dictionary, self.player),
            Spell.thunder_library: lambda state: self.has_gems(state) and state.has(Tool.magical_dictionary, self.player),
            Spell.diacute_library: lambda state: self.has_gems(state) and state.has(Tool.magical_dictionary, self.player),
            #  Combat Rules
            ForestOfLight.orb: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options) and state.has(Tool.ribbit_boots, self.player),
            ForestOfLight.ribbit_boots: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            ForestOfLight.sukiyapodes_1: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            AncientRuins.zoh_daimaoh: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            HarpyPath.bag: lambda state: state.has(Tool.panotty_flute, self.player) and self.can_fight_generic_at_level(state, 2, self.world.options),
            ShadyWell.arachne: lambda state: state.has(Special.ripe_cucumber, self.player) and self.can_fight_generic_at_level(state, 2, self.world.options),
            School.magical_dictionary: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            AncientVillage.elder: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_1: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_2: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_3: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_4: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_5: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            AncientVillage.villager_6: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            DragonAreas.firefly_egg: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            DragonAreas.stone: lambda state: self.can_fight_generic_at_level(state, 4, self.world.options) and state.has(Special.firefly_egg, self.player, 2),
            MagicTown.suketoudara: lambda state: state.has(Special.secret_stone, self.player, 7) and self.can_fight_generic_at_level(state, 4, self.world.options),
            Bestiary.flea: lambda state: state.has(Tool.toy_elephant, self.player),
            DarkForest.ribbon: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            # Boss checks require that you can actually defeat them
            Bestiary.owlbear: lambda state: state.has(Special.secret_stone, self.player, 8) and state.has(
                Special.dark_orb, self.player) and self.can_fight_generic_at_level(state, 4, self.world.options),
            Bestiary.sukiyapodes: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Bestiary.mini_zombie: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Bestiary.zoh: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Bestiary.arachne: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            Bestiary.headmaster: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            Bestiary.harpy: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            Bestiary.skeleton_d: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            Bestiary.skeleton_t: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
            Bestiary.nasu_grave: lambda state: self.can_fight_generic_at_level(state, 2, self.world.options),
            Bestiary.leviathan: lambda state: self.can_fight_generic_at_level(state, 4, self.world.options),
            # Shop locations require combat to farm money.
            Souvenir.dragon_nail: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.magic_king_foot: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.magic_king_tusk: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.magic_king_picture: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.magic_king_statue: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.waterfall_vase: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.wolf_tail: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Souvenir.dark_jug: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Bazaar.bazaar_pass: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            Bazaar.elephant: lambda state: self.can_fight_generic_at_level(state, 1, self.world.options),
            # Firefly egg is really expensive, so push it a bit later.
            Bazaar.firefly_egg: lambda state: self.can_fight_generic_at_level(state, 3, self.world.options),
        }

    def has_all(self, items: List[str], state: CollectionState):
        rule = True
        for item in items:
            rule = rule & state.has(item, self.player)
        return rule

    def has_souvenirs(self, state: CollectionState, options: MadouOptions):
        if options.souvenir_hunt:
            return self.has_all(Souvenir.souvenirs, state)
        return self.has_all(EventItem.shops, state)

    def has_gems(self, state: CollectionState):
        return self.has_all(Gem.gems, state)

    def can_fight_generic_at_level(self, state: CollectionState, level: int, options: MadouOptions):
        total_combat_spell_items = state.count_from_list(SpellItem.combat_spells, self.player)
        if total_combat_spell_items == 0:
            return False
        stun_rule = True
        diacute_count = max(0, level - 1)
        starting_spells = options.starting_magic.value
        if "Fire" in starting_spells:
            total_combat_spell_items += 1
        if "Ice Storm" in starting_spells:
            total_combat_spell_items += 1
        if "Thunder" in starting_spells:
            total_combat_spell_items += 1
        average_count = total_combat_spell_items // 3
        if level > 1:
            stun_rule = state.has(SpellItem.bayoen, self.player)
        return (state.has(SpellItem.diacute, self.player, diacute_count) and stun_rule and average_count >= min(4, level)) or state.has(EventItem.glitch, self.player)

    def has_any_flight_path_other_than(self, exception: str, state: CollectionState):
        flights = [FlightUnlocks.magic_village, FlightUnlocks.ancient_village, FlightUnlocks.wolf_town, FlightUnlocks.ruins_town, FlightUnlocks.sage_mountain]
        flights.remove(exception)
        has_path = False
        for flight in flights:
            has_path = has_path or state.has(flight, self.player)
        return has_path

    def set_madou_rules(self) -> None:
        for region in self.world.get_regions():
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
                for location in region.locations:
                    location.access_rule = self.region_rules[region.name]
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    entrance.access_rule = entrance.access_rule and self.entrance_rules[entrance.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = loc.access_rule and self.location_rules[loc.name]
