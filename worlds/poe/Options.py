from dataclasses import dataclass, fields, Field
from typing import FrozenSet, Union, Set

from Options import Choice, Toggle, DefaultOnToggle, ItemSet, OptionSet, Range, PerGameCommonOptions, DeathLinkMixin
from worlds.AutoWorld import World
from worlds.poe import Locations


class Goal(Choice):
    """
    Specifies the goal of the world.
    if your goal is act 5, you need to get to the 3rd area in act 6, kauri fortress, because of zone names.
    """
    display_name = "Goal"
    option_complete_the_campaign = 0
    option_complete_act_1 = 1
    option_complete_act_2 = 2
    option_complete_act_3 = 3
    option_complete_act_4 = 4
    option_kauri_fortress_act_6 = 5
    option_complete_act_6 = 6
    option_complete_act_7 = 7
    option_complete_act_8 = 8
    option_complete_act_9 = 9
    alias_complete_act_10 = 0
    option_defeat_bosses = 10
    default = 0

class NumberOfBosses(Range):
    """
    This is ignored if Goal isn't set to defeat_bosses. This specifies the number of bosses that need to be defeated
    (and for you to pick up their drops) in order for you to goal. This will max out at the number of bosses available in the world.
    """
    display_name = "Bosses to kill (ignored if Goal is not set to defeat_bosses)"
    range_start = 0
    range_end = len(Locations.bosses.values())
    default = 1

class BossesAvailable(OptionSet):
    """
    This is also ignored if Goal isn't set to defeat_bosses. Specifies the availability of the bosses in the world.
    This will NOT determine how many bosses are available in the world, but rather which bosses can be randomized.
    This will choose any (including _very_ difficult bosses if none are selected.)

    valid choices: [ "hydra", "phoenix", "chimera", "minotaur", "shaper", "uber_shaper", "elder", "uber_elder",
     "uber_uber_elder", "atziri", "al-hezmin", "baran", "drox", "veritania", "sirus", "uber_sirus", "maven",
     "uber_maven", "exarch", "uber_exarch", "eater", "uber_eater", "incarnation_of_neglect", "incarnation_of_fear",
     "incarnation_of_dread", "cortex", "uber_cortex"]
    """
    display_name = "Bosses Available"
    valid_keys = Locations.bosses.keys()
    default = [
        key for key in valid_keys
        if Locations.bosses[key].get('difficulty', 'Guardian') not in {'Uber', 'Pinnacle'}
    ]


class GearUpgrades(Choice):
    """
    Specifies if gear rarity should be restricted to a certain rarity, unlockable through items found in the multiworld.
    """
    display_name = "Gear Unlocks"
    option_all_gear_unlocked_at_start = 0
    option_all_normal_and_unique_gear_unlocked = 1
    option_all_normal_gear_unlocked = 2
    option_all_uniques_unlocked = 3
    option_no_gear_unlocked = 4
    default = 2

class UsableStartingGear(Choice):
    """
    Specifies if you should start with the gear that you find in the tutorial, for your starting character.
    use this option if you don't want to punch hillock to death.
    """
    display_name = "Usable Starting Gear"
    option_no_starting_gear = 0
    option_starting_weapon = 1
    option_starting_weapon_and_flask_slots = 2
    option_starting_weapon_and_gems = 3
    option_starting_weapon_flask_and_gems = 4
    default = 3

class AddPassiveSkillPointsToItemPool(Toggle):
    """
    Specifies if passive skill points should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Randomized Passive Skill Points"
    default = True

class AddLevelingUpToLocationPool(Toggle):
    """
    Specifies if leveling up be considered "locations".
    """
    display_name = "Leveling Up locations"
    default = True

class GearUpgradesPerAct(Range):
    """
    Specifies a minimum number of rarity of gear upgrades available per act. (there are 38 total)
    This will be ignored if the "Gear Upgrades" option is turned off.
    """
    display_name = "Gear Upgrades Per Act"
    range_start = 0
    range_end = 38
    default = 5
    
class AddFlaskSlotsToItemPool(Toggle):
    """
    Specifies if flasks should be restricted, unlockable through items found in the multiworld.
    You may equip up to 5 flasks of a given rarity, and can unlock more flasks of a rarity through items.
    """
    display_name = "Flask Slot Upgrades"
    default = False

class FlaskSlotsPerAct(Range):
    """
    Specifies a minimum number of available flask slots per act. (there are 5 total)
    This will be ignored if the "Flask Slots" option is turned off.
    """
    display_name = "Flask Slots Per Act"
    range_start = 0
    range_end = 5
    default = 1

class AddMaxLinksToItemPool(Toggle):
    """
    Specifies if the number of linked support gem slots you can use in gear should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Support Gem Slot Upgrades"
    default = True

class MaxLinksPerAct(Range):
    """
    Specifies a minimum number of available linked support gem slots per act. (there are 22 total)
    This will be ignored if the "Support Gem Slot Upgrades" option is turned off.
    """
    display_name = "Support Gem Slots Per Act"
    range_start = 0
    range_end = 22
    default = 2


class SkillGemsPerAct(Range):
    """
    Specifies the minimum number of usable skill gems placed by the generator per act.
    Higher values will place more relevant skill gems early on
    """
    display_name = "Skill Gem Slots Per Act"
    range_start = 0
    range_end = 20
    default = 2

class StartingCharacter(Choice):
    """
    The starting character for the world. This will determine the class available at the start.
    """
    display_name = "Starting Character"
    option_marauder    = 1
    option_ranger      = 2
    option_witch       = 3
    option_duelist     = 4
    option_templar     = 5
    option_shadow      = 6
    option_scion       = 7
    default = "random"
    
class AscendanciesAvailablePerClass(Range):
    """
    Specifies the maximum number of available ascendancies per class.
    """
    display_name = "Ascendancies Available Per Class"
    range_start = 0
    range_end = 3
    default = 1

class AllowUnlockOfOtherCharacters(Toggle):
    """
    Allows unlocking of other characters.
    """
    display_name = "Allow Unlock of Other Characters"
    default = False

class GucciHoboMode(Choice):
    """
    Specifies if the world should be in Gucci Hobo Mode, this restricts use of any non-unique equipment to only 1 slot.
    This is an extremely difficult challenge intended for experienced players, and will greatly increase the length of your run.
    Expect a very slow start, involving farming early act 1 zones.
    """
    display_name = "Gucci Hobo Mode"
    option_disabled = 4
    option_allow_one_slot_of_any_rarity = 1
    option_allow_one_slot_of_normal_rarity = 2
    option_no_non_unique_items = 3
    default = 4

class EnableTTS(Choice):
    """
    Settings for the Text-to-Speech (TTS) feature.
    """
    display_name = "Text-to-Speech"
    option_no_tts     = 0
    option_enabled_AP_Item = 1
    option_enabled_Base_Item = 2
    default = 1

class TTSSpeed(Range):
    """
    Speed of the Text-to-Speech (TTS) feature.
    """
    display_name = "TTS Speed"
    range_start = 50
    range_end = 500
    default = 250


@dataclass
class PathOfExileOptions(DeathLinkMixin, PerGameCommonOptions):
    """
    Common options for Path of Exile.
    """
    goal: Goal
    number_of_bosses: NumberOfBosses
    bosses_available: BossesAvailable
    gear_upgrades: GearUpgrades
    usable_starting_gear: UsableStartingGear
    add_passive_skill_points_to_item_pool: AddPassiveSkillPointsToItemPool
    add_leveling_up_to_location_pool: AddLevelingUpToLocationPool
    gear_upgrades_per_act: GearUpgradesPerAct
    add_flask_slots_to_item_pool: AddFlaskSlotsToItemPool
    flask_slots_per_act: FlaskSlotsPerAct
    add_max_links_to_item_pool: AddMaxLinksToItemPool
    max_links_per_act: MaxLinksPerAct
    skill_gems_per_act: SkillGemsPerAct
    starting_character: StartingCharacter
    ascendancies_available_per_class: AscendanciesAvailablePerClass
    allow_unlock_of_other_characters: AllowUnlockOfOtherCharacters
    gucci_hobo_mode: GucciHoboMode
    enable_tts: EnableTTS
    tts_speed: TTSSpeed



def option_starting_character_to_class_name(option_id: int) -> str:
    mapping = {
        1: "Marauder",
        2: "Ranger",
        3: "Witch",
        4: "Duelist",
        5: "Templar",
        6: "Shadow",
        7: "Scion",
    }
    return mapping.get(option_id, "Unknown")
