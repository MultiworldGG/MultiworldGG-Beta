from dataclasses import dataclass

from Options import (
    Choice,
    NamedRange,
    PerGameCommonOptions,
    Toggle,
    OptionDict,
    StartInventoryPool,
    DeathLink,
)


class SkillLevel(Choice):
    """In-Game difficulty.
    Primarily affects number of Enemies spawned"""

    display_name = "Skill Level"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_nightmare = 3
    default = 1


class Difficulty(Choice):
    """Randomizer difficulty.
    Higher levels offer less resources and worse items in the pool"""

    display_name = "Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_extreme = 3
    default = 1


class LogicDifficulty(Choice):
    """Trick difficulty for logic.
    Higher levels require harder tricks such precise Rocket/Grenade Jumps and airstrafes
    """

    display_name = "Logic Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_extreme = 3
    default = 1


class BaseGame(Choice):
    """Pick which game/expansion to play"""

    display_name = "Pick Q1/Expansion"
    option_quake = 0
    option_hipnotic = 1
    option_rogue = 2
    option_mg1 = 3
    option_dopa = 4


class UnlockAbilities(Toggle):
    """Unlock Jumping, Diving, Running, Rocket/Grenade Jumps as items"""

    display_name = "Unlock Abilities"
    default = True


class DamageRemoverAbilities(Toggle):
    """Unlock the ability to not get hurt when doing rocket/grenade jumps"""

    display_name = "Unlock Damage Removal"
    default = True


class UnlockInteract(Toggle):
    """Unlock using buttons, shooting switches and opening doors as items"""

    display_name = "Unlock Interaction"
    default = True


# class AllowSaving(Toggle):
#    """Enables saving to store mid level progress. If disabled, levels always have to be played from the start"""
#
#    display_name = "Allow Saving"
#    default = True


class AreaMaps(Choice):
    """Select if full game maps are available in the in-game map view"""

    display_name = "Area Maps"
    option_none = 0
    option_unlockable = 1
    option_start_with = 2
    default = 2


class Goal(Choice):
    """Choose the goal of the game"""

    display_name = "Goal"
    option_beat_all_bosses = 0
    option_beat_all_levels = 1
    option_collect_all_secrets = 2
    option_all = 3
    default = 3


class GoalPercentage(NamedRange):
    """Percentage of chosen goals that need to be reached to win the game"""

    display_name = "Percentage of Goals required"
    range_start = 25
    range_end = 100
    default = 100


class IncludeSecrets(Toggle):
    """Include secret areas into the location pool.
    This only has an effect if they are not already included as goal locations"""

    display_name = "Include Secrets as Locations"
    default = False


class IncludeAllKills(Toggle):
    """Includes all kills per level in the location pool."""

    display_name = "Include All-Kills as Locations"
    default = False


class IncludedLocations(Choice):
    """Presets for included locations.
    Iconic includes all keys, weapons, sigils, armor and powerups.
    Balanced adds 25 % ammo + health.
    Dense adds 50% ammo + health.
    All adds 100% ammo + health.
    Use the custom option if you want to make use of CustomIncludedLocations.
    """

    display_name = "Included Locations"
    option_iconic = 0
    option_balanced = 1
    option_dense = 2
    option_all = 3
    option_custom = 4
    default = 1


class IncludeMPItems(Toggle):
    """Set if included locations should also contain multiplayer item spawns."""

    display_name = "Include multiplayer items as locations"
    default = False


class CustomIncludedLocations(OptionDict):
    """A list of itemnames that will be replaced with AP locations.
    The number after the itemname is the percentage of items of that type, which will get turned into AP locations.
    Quake 1 Items: ["item_armor1", "item_armor2", "item_armorInv", "weapon_lightning", "weapon_nailgun", "weapon_supernailgun", "weapon_supershotgun", "weapon_grenadelauncher",
        "weapon_rocketlauncher", "item_health (Small Medkit)", "item_health (Large Medkit)", "item_health (Megahealth)", "item_cells", "item_rockets", "item_shells", "item_spikes",
        "item_artifact_envirosuit", "item_artifact_invisibility", "item_artifact_invulnerability", "item_artifact_super_damage", "item_key1", "item_key2", "item_sigil"]
    Hipnotic Items: ["item_artifact_empathy_shields", "item_hornofconjuring", "item_artifact_wetsuit", "weapon_laser_gun", "weapon_mjolnir", "weapon_proximity_gun"]
    Rogue Items: ["item_sphere", "item_random_powerup", "item_powerup_belt", "item_powerup_shield", "item_flag", "item_flag_team1", "item_flag_team2", "item_lava_spikes", "item_multi_rockets", "item_plasma"]
    """

    default = {
        "item_armor1": 100,
        "item_armor2": 100,
        "item_armorInv": 100,
        "weapon_lightning": 100,
        "weapon_nailgun": 100,
        "weapon_supernailgun": 100,
        "weapon_supershotgun": 100,
        "weapon_grenadelauncher": 100,
        "weapon_rocketlauncher": 100,
        "item_health (Small Medkit)": 100,
        "item_health (Large Medkit)": 100,
        "item_health (Megahealth)": 100,
        "item_cells": 100,
        "item_rockets": 100,
        "item_shells": 100,
        "item_spikes": 100,
        "item_artifact_envirosuit": 100,
        "item_artifact_invisibility": 100,
        "item_artifact_invulnerability": 100,
        "item_artifact_super_damage": 100,
        "item_key1": 100,
        "item_key2": 100,
        "item_sigil": 100,
        "item_weapon": 100,
        # hipnotic
        "item_artifact_empathy_shields": 100,
        "item_hornofconjuring": 100,
        "item_artifact_wetsuit": 100,
        "weapon_laser_gun": 100,
        "weapon_mjolnir": 100,
        "weapon_proximity_gun": 100,
        # rogue
        "item_sphere": 100,
        "item_random_powerup": 100,
        "item_powerup_belt": 100,
        "item_powerup_shield": 100,
        "item_flag": 100,
        "item_flag_team1": 100,
        "item_flag_team2": 100,
        "item_lava_spikes": 100,
        "item_multi_rockets": 100,
        "item_plasma": 100,
    }
    valid_keys = [
        # quake 1
        "item_armor1",
        "item_armor2",
        "item_armorInv",
        "weapon_lightning",
        "weapon_nailgun",
        "weapon_supernailgun",
        "weapon_supershotgun",
        "weapon_grenadelauncher",
        "weapon_rocketlauncher",
        "item_health (Small Medkit)",
        "item_health (Large Medkit)",
        "item_health (Megahealth)",
        "item_cells",
        "item_rockets",
        "item_shells",
        "item_spikes",
        "item_artifact_envirosuit",
        "item_artifact_invisibility",
        "item_artifact_invulnerability",
        "item_artifact_super_damage",
        "item_key1",
        "item_key2",
        "item_sigil",
        "item_weapon",
        # hipnotic
        "item_artifact_empathy_shields",
        "item_hornofconjuring",
        "item_artifact_wetsuit",
        "weapon_laser_gun",
        "weapon_mjolnir",
        "weapon_proximity_gun",
        "item_sphere",
        "item_random_powerup",
        "item_powerup_belt",
        "item_powerup_shield",
        "item_flag",
        "item_flag_team1",
        "item_flag_team2",
        "item_lava_spikes",
        "item_multi_rockets",
        "item_plasma",
    ]


class Episode1(Toggle):
    """Include Episode 1 in the randomizer"""

    display_name = "Use Episode 1"
    default = True


class Episode2(Toggle):
    """Include Episode 2 in the randomizer"""

    display_name = "Use Episode 2"
    default = True


class Episode3(Toggle):
    """Include Episode 3 in the randomizer"""

    display_name = "Use Episode 3"
    default = True


class Episode4(Toggle):
    """Include Episode 4 in the randomizer"""

    display_name = "Use Episode 4"
    default = True


class Episode5(Toggle):
    """Include Episode 5 in the randomizer"""

    display_name = "Use Episode 5"
    default = True


class IncludeHub(Toggle):
    """Include the Hub Level in the randomizer"""

    display_name = "Use Hub Level"
    default = False


class IncludeEnd(Toggle):
    """Include the End Level in the randomizer"""

    display_name = "Use End Level"
    default = True


class LevelCount(NamedRange):
    """
    Number of maps that should be included in the shuffle. Maps are picked from the enabled episodes. If this count
    exceeds the maximum number of levels in those episodes, all of them will be included.
    """

    display_name = "Level Count"
    range_start = 3
    range_end = 32
    default = 9


class StartingLevelCount(NamedRange):
    """
    The number of levels that are unlocked from the start.
    """

    display_name = "Starting Level Count"
    range_start = 1
    range_end = 32
    default = 1


class ShuffleStartingLevels(Toggle):
    """If enabled will pick levels unlocked by default at random instead of the first of each episode"""

    display_name = "Shuffle Starting Levels"
    default = True


class ProgressiveWeapons(Toggle):
    """
    Replace weapon unlocks and ammunition capacity upgrades with progressive versions.
    This greatly increases access to weapons to your world.
    """

    display_name = "Progressive Weapons"
    default = True


class ProgressiveInventories(Toggle):
    """
    Replace Inventory unlocks and their capacity upgrades with progressive versions.
    This increases access to their abilities in your world.
    """

    display_name = "Progressive Inventory"
    default = True


class ShellRecharge(Toggle):
    """
    Recharges 1 shell (ammo) every second.
    QoL to make the early game less painful on harder difficulties.
    """

    display_name = "Recharge Shells"
    default = False


class PowerupRecharge(Toggle):
    """
    Recharges 1 of each powerup every 60 seconds.
    This is incredibly overpowered, only use it if you struggle with the game.
    """

    display_name = "Recharge Powerups"
    default = False


class TrapPercentage(NamedRange):
    """Percentage of filler items that should be traps"""

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 90
    default = 10


class ShowTrapsAsProgressive(Toggle):
    """Traps show up as progressive items in-game."""

    display_name = "Traps as Progression"
    default = True


@dataclass
class Q1Options(PerGameCommonOptions):
    difficulty: Difficulty
    logic_difficulty: LogicDifficulty
    skill_level: SkillLevel
    basegame: BaseGame
    unlock_abilities: UnlockAbilities
    damage_remover_abilities: DamageRemoverAbilities
    unlock_interact: UnlockInteract
    # allow_saving: AllowSaving
    area_maps: AreaMaps
    goal: Goal
    goal_percentage: GoalPercentage
    # location_density: LocationDensity
    included_locations_preset: IncludedLocations
    include_mp_items: IncludeMPItems
    custom_included_locations: CustomIncludedLocations
    include_secrets: IncludeSecrets
    include_allkills: IncludeAllKills
    episode1: Episode1
    episode2: Episode2
    episode3: Episode3
    episode4: Episode4
    episode5: Episode5
    include_hub: IncludeHub
    include_end: IncludeEnd
    level_count: LevelCount
    shuffle_starting_levels: ShuffleStartingLevels
    starting_level_count: StartingLevelCount
    progressive_weapons: ProgressiveWeapons
    progressive_inventories: ProgressiveInventories
    trap_percentage: TrapPercentage
    traps_as_progressive: ShowTrapsAsProgressive
    shell_recharge: ShellRecharge
    powerup_recharge: PowerupRecharge
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
