from dataclasses import dataclass

from Options import Toggle, Choice, Range, DeathLink, PerGameCommonOptions


# TODO: Other potential options
# Randomize starting monster (because right not logic doesn't care about starting monster's ability)
#   Randomize to any monster
# Randomize keeper's monsters

# region Logic Flags
class LogicDifficulty(Choice):
    """Sets the difficulty of movement that is required from the player. Default is casual.

    Casual: Logic will only require of you what the vanilla game expects.
    Advanced: Logic can require difficult jumps and require using abilities in unintended ways.
    Expert: Logic can require frame-perfect (or near frame-perfect) jumps while using abilities in ways they weren't intended."""

    display_name = "Logic Difficulty"
    option_casual = 0
    option_advanced = 1
    option_expert = 2
    default = 0


class TediousChecks(Toggle):
    """When enabled, the logic will expect the player to use the Warp to Start feature to get out of areas that are only accessible in one direction, or to attempt failed jumps multiple times. Default is disabled"""

    display_name = "Include Tedious Logic"
    default = False
# endregion


# region Monster Randomization
class RandomizeMonsters(Choice):
    """Randomize monsters

    Off: Monsters are not randomized. Koi and Bard Egg locations are also not randomized
    Any: All monsters are randomized independently
    By Specie: Monsters of the same specie are all randomized to another monster specie
    By Encounter: Within an encounter, all monsters of the same specie are randomized to another specie. Each encounter is randomized separately"""
    display_name = "Randomize Monsters"
    option_off = 0
    option_any = 1
    option_by_specie = 2
    option_by_encounter = 3
    default = 1


class RandomizeMonsterShifts(Choice):
    """When do shifted monsters start appearing?

    Never: Shifted monsters will never appear in the wild
    After Sun Palace: Shifted monsters will start appearing after completing the Sun Palace storyline
    Any Time: Shifted monsters can appear any time"""
    display_name = "Randomize Shifted Monsters"
    option_never = 0
    option_after_sun_palace = 1
    option_any_time = 2
    default = 1


class ImprovedMobilityLimitation(Toggle):
    """Limit monsters with improved mobility abilities from showing up too early.
    Abilities include: improved flying, lofty mount, improved swimming, and dual mobility

    If enabled, monsters with improved mobility abilities will not show up in the Mountain Path, Blue Caves, Stronghold Dungeon, Snowy Peaks, Sun Palace, or Ancient Woods.
    if disabled, monsters with improved mobility abilities can appear anywhere."""
    display_name = "Limit Improved Mobility Abilities"
    default = True


class IncludeSpectralFamiliarsInMonsterPool(Toggle):
    """If enabled, spectral familiars will be added to the pool of monsters that's randomized"""
    display_name = "Include Spectral Familiars"
    default = False


class IncludeBardInMonsterPool(Toggle):
    """If enabled, Bard will be added to the pool of monsters that's randomized"""
    display_name = "Include Bard"
    default = False


class RandomizeMonsterSkillTrees(Toggle):
    """If enabled, randomizes the 3 or 4 skill trees that every monster has"""
    display_name = "Randomize Monster Skill Trees"
    default = False


class RandomizeMonsterUltimates(Toggle):
    """If enabled, randomizes every monster's three ultimate skills"""
    display_name = "Randomize Monster Ultimates"
    default = False


class RandomizeMonsterShiftSkills(Toggle):
    """If enabled, randomizes the light and dark shift traits for all monsters"""
    display_name = "Randomize Monster Shift Skills"
    default = False


class ExploreAbilitiesMustBeUnlocked(Choice):
    """If enabled, explore abilities cannot be used until a corresponding item has been collected.
    The items required to use explore abilities depends on the selected option:

    Off: Explore Abilities are always available.
    Type: Monsters are grouped into 16 different categories based on monster type. There are 16 unique items to unlock abilities for all monsters of a given type
    Ability: Each explore ability must be unlocked separately. For example, unlocking Flying will allow that ability to be used on any monster with the Flying ability
    Species: Each monster species will require a unique item to unlock its explore ability (excepting evolutions where the ability doesn't change)
    Progression: Monster abilities are grouped by function and unlocked progressively. This helps to keep more advanced abilities from being made available early in the game
    Combo: Similar to Progression, except there are a smaller number of progressive groups, and more advanced abilities require combinations of different progression chains"""
    display_name = "Explore Abilities Must be Unlocked"
    option_off = 0
    option_type = 1
    option_ability = 2
    option_species = 3
    option_progression = 4
    option_combo = 5
    default = 0
# endregion


# region Check Restrictions
class CryomancerPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the four checks given by Lady Stasis in the Snowy Peaks.

    Vanilla: The checks are unchanged from the base game.
    Randomized: The checks are randomized with the rest of the item pool.
    Filler: The checks are guaranteed to be junk items."""
    display_name = "Lady Stasis' (Dodo Egg) Checks"
    option_vanilla = 0
    option_randomized = 1
    option_filler = 2
    default = 1


class KoiEggPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the Caretaker's Koi Egg check in Sun Palace

    Vanilla: The check is unchanged from the base game.
    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Koi Egg Check"
    option_vanilla = 0
    option_randomized = 1
    option_filler = 2
    default = 1


class SkorchEggPlacementRestriction(Choice):
    """Sets what kind of items can be placed at Bex's Skorch Egg check in Magma Caverns

    Vanilla: The check is unchanged from the base game.
    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Skorch Egg Check"
    option_vanilla = 0
    option_randomized = 1
    option_filler = 2
    default = 1


class BardEggPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the 5 Celestial Feathers/Bard Egg check in the Forgotten World

    Vanilla: The check is unchanged from the base game.
    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Bard Egg (Celestial Feathers) Check"
    option_vanilla = 0
    option_randomized = 1
    option_filler = 2
    default = 1


class SpectralFamiliarEggPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the four spectral familiar battle checks in Eternity's End.

        Vanilla: The check is unchanged from the base game (gives Spectral Familiar eggs)
        Randomized: The check is randomized with the rest of the item pool.
        Filler: The check is guaranteed to be a junk item."""
    display_name = "Spectral Familiar Egg (Eternity's End) Checks"
    option_vanilla = 0
    option_randomized = 1
    option_filler = 2
    default = 1


class NoProgressionInUnderworld(Toggle):
    """If enabled, no progression items will be placed in the Underworld"""
    display_name = "No Progression in Underworld"
    default = False


class NoProgressionInForgottenWorld(Toggle):
    """If enabled, no progression items will be placed in the Forgotten World"""
    display_name = "No Progression in the Forgotten World"
    default = False


class OldManPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the Old Man check in Horizon Beach.

    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Old Man (Memorial Ring) Check"
    option_randomized = 0
    option_filler = 1
    default = 0


class FishermanPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the Fisherman check in Horizon Beach.

    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Fisherman (Rare Seashells) Check"
    option_randomized = 0
    option_filler = 1
    default = 0


class WandererGiftPlacementRestriction(Choice):
    """Sets what kind of items can be placed at the Wanderer check that requires defeating Dracomer in the Forgotten World

    Randomized: The check is randomized with the rest of the item pool.
    Filler: The check is guaranteed to be a junk item."""
    display_name = "Wanderer World Tree Check"
    option_randomized = 0
    option_filler = 1
    default = 0
# endregion


# region Item Drop Chance
class CraftingMaterialDropChance(Range):
    """Frequency that a random non-progression item is a crafting material

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Crafting Material Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class ConsumableDropChance(Range):
    """Frequency that a random non-progression item is a consumable

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Consumable Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class FoodDropChance(Range):
    """Frequency that a random non-progression item is a food item

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Food Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class CatalystDropChance(Range):
    """Frequency that a random non-progression item is a catalyst

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Catalyst Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class WeaponDropChance(Range):
    """Frequency that a random non-progression item is a weapon

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Weapon Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class AccessoryDropChance(Range):
    """Frequency that a random non-progression item is an accessory

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Accessory Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class GoldDropChance(Range):
    """Frequency that a random non-progression item is gold

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Gold Drop Chance"
    range_start = 0
    range_end = 100
    default = 50
# endregion


# region Open World Options
class SkipPlot(Toggle):
    """Skip plot related events and open up all areas gated by story progression."""
    display_name = "Skip Plot Requirements"
    default = False


class SkipBattles(Toggle):
    """Skip all keeper battles."""
    display_name = "Skip Keeper Battles"
    default = False


class LocalAreaKeys(Toggle):
    """Localized Area Keys

    If enabled, area keys will only appear in the Monster Sanctuary player's world, and they will only appear in their own area.
    If disabled, keys can appear in any world, and may be found outside their area in which they are used."""
    display_name = "Local Area Keys"
    default = False


class RemoveLockedDoors(Choice):
    """Remove Locked Doors

    Off: Locked doors are not removed
    Minimal: Superfluous locked doors are removed, while ones that gate large numbers of checks remain
    All: All locked doors are removed"""
    display_name = "Remove Locked Doors"
    option_off = 0
    option_minimal = 1
    option_all = 2
    default = 0


class OpenBlueCaves(Toggle):
    """If enabled, the Blue Cave to Mountain path shortcut will be opened"""
    display_name = "Open World - Blue Caves"
    default = False


class OpenStrongholdDungeon(Choice):
    """Opens shortcuts and entrances to Stronghold Dungeon

    Entrances: Opens up entrances to the Dungeon from Blue Caves and Ancient Woods
    Shortcuts: Opens interior gates within the Dungeon
    Full: Opens both Entrances and Shortcuts"""
    display_name = "Open World - Stronghold Dungeon"
    option_off = 0
    option_entrances = 1
    option_shortcuts = 2
    option_full = 3
    default = 0


class OpenAncientWoods(Toggle):
    """If enabled, opens up the alternate routes past the Brutus and Goblin King fights
    NOTE: These shortcuts allow you to bypass the need for Ancient Woods Keys. It is recommended to only use this setting if locked doors are turned off"""
    display_name = "Open World - Ancient Woods"
    default = False


class OpenSnowyPeaks(Toggle):
    """If enabled, opens up shortcuts within Snowy Peaks"""
    display_name = "Open World - Snowy Peaks"
    default = False


class OpenSunPalace(Choice):
    """Opens shortcuts and entrances to Sun Palace

    Entrances: Opens the elemental gates between Blue Caves and Sun Palace, and opens the gate between Snowy Peaks and Sun Palace
    Raise Pillar: Raises the pillar, lowers the water, and opens the east and west shortcuts
    Full: Opens both Entrances and Raises the Pillar"""
    display_name = "Open World - Sun Palace"
    option_off = 0
    option_entrances = 1
    option_raise_pillar = 2
    option_full = 3
    default = 0


class OpenHorizonBeach(Choice):
    """Opens shortcuts and entrances to Horizon Beach

    Entrances: Opens the elemental door locks between Ancient Woods and Horizon Beach, and opens the Magma Chamber to Horizon Beach shortcut
    Shortcuts: Opens the shortcut in central Horizon Beach
    Full: Opens both Entrances and Shortcuts"""
    display_name = "Open World - Horizon Beach"
    option_off = 0
    option_entrances = 1
    option_shortcuts = 2
    option_full = 3
    default = 0


class OpenMagmaChamber(Choice):
    """Opens shortcuts and entrances to Magma Chamber

    Entrances: Opens the rotating gates between Ancient Woods and Magma Chamber, and the breakable wall between Forgotten world and Magma Chamber
    Lower Lava: Removes the runestone shard from the item pool, lowers the lava, and opens all internal shortcuts
    Full: Opens Entrances and Lowers Lava"""
    display_name = "Open World - Magma Chamber"
    option_off = 0
    option_entrances = 1
    option_lower_lava = 2
    option_full = 3
    default = 0


class OpenBlobBurg(Choice):
    """Opens up Blob Burg

    Entrances: Removes blob key from the item pool and makes Blob Burg accessible with no requirements
    Open Walls: Opens up all areas within Blob Burg, removing the need to incrementally open it
    Full: Opens Entrances and all Walls"""
    display_name = "Open World - Blob Burg"
    option_off = 0
    option_entrances = 1
    option_open_walls = 2
    option_full = 3
    default = 0


class OpenForgottenWorld(Choice):
    """Opens shortcuts and entrances to Horizon Beach

    Entrances: Opens alternative entrances to Forgotten World from Horizon Beach and Magma Chamber
    Shortcuts: Opens one-way shortcuts in the Forgotten World
    Full: Opens both Entrances and Shortcuts"""
    display_name = "Open World - Forgotten World"
    option_off = 0
    option_entrances = 1
    option_shortcuts = 2
    option_full = 3
    default = 0


class OpenMysticalWorkshop(Toggle):
    """If enabled, opens up the northern shortcut within the Mystical Workshop
    NOTE: This shortcut allows you to bypass the need for Mystical Workshop Keys. It is recommended to only use this setting if locked doors are turned off"""
    display_name = "Open World - Mystical Workshop"
    default = False


class OpenUnderworld(Choice):
    """Opens up the Underworld

    Entrances: Removes sanctuary tokens from the item pool and opens up the Underworld door in Blue Caves, as well as the back entrance in Sun Palace
    Shortcuts: Opens all shortcuts and enables all grapple points within the Underworld
    Full: Opens Entrances and Shortcuts"""
    display_name = "Open World - Underworld"
    option_off = 0
    option_entrances = 1
    option_shortcuts = 2
    option_full = 3
    default = 0


class OpenAbandonedTower(Choice):
    """Opens up the Abandoned Tower

    Entrances: Opens the large door between Mystical Workshop and Abandoned Tower, as well as removing the Key of Power door. Removes Key of Power from the item pool
    Shortcuts: Opens all shortcuts in Abandoned Tower
    Full: Opens Entrances and Shortcuts"""
    display_name = "Open World - Abandoned Tower"
    option_off = 0
    option_entrances = 1
    option_shortcuts = 2
    option_full = 3
    default = 0
# endregion


# region Items and Inventory
class MonstersAlwaysDropEggs(Toggle):
    """If enabled, monsters will always drop an egg."""
    display_name = "Monsters always drop eggs"
    default = True


class MonstersAlwaysDropCatalysts(Toggle):
    """If enabled, evolved monsters will always drop their own catalyst."""
    display_name = "Evolved monsters always drop catalysts"
    default = False


class IncludeChaosRelics(Choice):
    """Include Relics of Chaos in the random item pool

    Off: Relics of Chaos will not show up
    On: Relics of Chaos can be added to the item pool, but are not guaranteed
    Some: At least 5 Relics of Chaos will be included in the item pool
    All: All Relics of Chaos will be added to the item pool"""
    display_name = "Include Relics of Chaos"
    option_off = 0
    option_on = 1
    option_some = 2
    option_all = 3
    default = 1


class IncludeLootersHandbook(Toggle):
    """If enabled, this adds a new item, the Looter's Handbook, to the item pool. When the player has this item in their inventory, all chests will have their appearance updated to match their contents. Progression items will be in purple chests, and useful items will be in green chests."""
    display_name = "Include the Looter's Handbook item"
    default = True


class StartWithSmokeBombs(Toggle):
    """If enabled, the player will start with 50 Smoke Bombs."""
    display_name = "Start with 50 Smoke Bombs"
    default = True


class StartingGold(Range):
    """Override the player's starting gold, counted in increments of 100 gold"""
    display_name = "Starting Gold (counted in increments of 100)"
    range_start = 0
    range_end = 1000
    default = 1


class AutomaticallyScaleEquipment(Choice):
    """If enabled, equipment that is sent to the player will be automatically leveled according to the player's progress in the game

    Disabled: Weapon and accessory levels are randomized when the item pool is generated
    By Level: Weapons and accessories are scaled with the highest monster level the player has
    By Rank: Weapons and accessories are scaled with the number of champions the player has defeated
    By Map Progress: Weapons and accessories are scaled with the percentage of the map the player has uncovered"""
    display_name = "Automatically Scale Equipment Level"
    option_disabled = 0
    option_by_level = 1
    option_by_rank = 2
    option_by_map_progress = 3
    default = 0


class GiveKeyOfPowerWhenChampionsAreDefeated(Range):
    """When this is set to a value greater than 0, the Key of Power will be automatically given to the player when they defeat the set number of champions. This is disabled when set to 0"""
    display_name = "Give Key of Power When Champions Are Defeated"
    range_start = 0
    range_end = 26
    default = 0
#endregion


class AddHints(Toggle):
    """Adds hints for common checks, items, and monsters"""
    display_name = "Add Hints"
    default = True


class Goal(Choice):
    """Goal to complete.

    Defeat Mad Lord: Defeat the Mad Lord
    Defeat All Champions: Defeat all 27 Champions"""
    display_name = "Goal"
    option_defeat_mad_lord = 0
    option_defeat_all_champions = 1
    default = 0


@dataclass
class MonsterSanctuaryOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
    tedious_checks: TediousChecks

    randomize_monsters: RandomizeMonsters
    monster_shift_rule: RandomizeMonsterShifts
    improved_mobility_limit: ImprovedMobilityLimitation
    include_spectral_familiars_in_pool: IncludeSpectralFamiliarsInMonsterPool
    include_bard_in_pool: IncludeBardInMonsterPool
    randomize_monster_skill_trees: RandomizeMonsterSkillTrees
    randomize_monster_ultimates: RandomizeMonsterUltimates
    randomize_monster_shift_skills: RandomizeMonsterShiftSkills
    lock_explore_abilities: ExploreAbilitiesMustBeUnlocked

    cryomancer_check_restrictions: CryomancerPlacementRestriction
    koi_egg_placement: KoiEggPlacementRestriction
    bard_egg_placement: BardEggPlacementRestriction
    skorch_egg_placement: SkorchEggPlacementRestriction
    spectral_familiar_egg_placement: SpectralFamiliarEggPlacementRestriction
    no_progression_in_underworld: NoProgressionInUnderworld
    no_progression_in_forgotten_world: NoProgressionInForgottenWorld
    old_man_check_restrictions: OldManPlacementRestriction
    fisherman_check_restrictions: FishermanPlacementRestriction
    wanderers_gift_check_restrictions: WandererGiftPlacementRestriction

    monsters_always_drop_egg: MonstersAlwaysDropEggs
    monsters_always_drop_catalyst: MonstersAlwaysDropCatalysts
    include_chaos_relics: IncludeChaosRelics
    include_looters_handbook: IncludeLootersHandbook
    add_smoke_bombs: StartWithSmokeBombs
    starting_gold: StartingGold
    automatically_scale_equipment: AutomaticallyScaleEquipment
    key_of_power_champion_unlock: GiveKeyOfPowerWhenChampionsAreDefeated

    drop_chance_craftingmaterial: CraftingMaterialDropChance
    drop_chance_consumable: ConsumableDropChance
    drop_chance_food: FoodDropChance
    drop_chance_catalyst: CatalystDropChance
    drop_chance_weapon: WeaponDropChance
    drop_chance_accessory: AccessoryDropChance
    drop_chance_currency: GoldDropChance

    skip_plot: SkipPlot
    skip_keeper_battles: SkipBattles
    remove_locked_doors: RemoveLockedDoors
    local_area_keys: LocalAreaKeys
    open_blue_caves: OpenBlueCaves
    open_stronghold_dungeon: OpenStrongholdDungeon
    open_ancient_woods: OpenAncientWoods
    open_snowy_peaks: OpenSnowyPeaks
    open_sun_palace: OpenSunPalace
    open_horizon_beach: OpenHorizonBeach
    open_magma_chamber: OpenMagmaChamber
    open_blob_burg: OpenBlobBurg
    open_forgotten_world: OpenForgottenWorld
    open_mystical_workshop: OpenMysticalWorkshop
    open_underworld: OpenUnderworld
    open_abandoned_tower: OpenAbandonedTower

    hints: AddHints
    goal: Goal
    death_link: DeathLink
