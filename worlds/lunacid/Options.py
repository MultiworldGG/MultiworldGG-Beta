from dataclasses import dataclass
from typing import ClassVar, Protocol

from Options import Choice, Toggle, DeathLink, PerGameCommonOptions, Range, OptionSet, OptionDict
from worlds.lunacid.data.item_data import all_filler_items, default_filler_weights, default_trap_weights
from .strings.items import Trap, Coins


class LunacidOption(Protocol):
    internal_name: ClassVar[str]


class Ending(Choice):
    """Choose which ending is required to complete the game.
    Ending A: Reach Chamber of the Sleeper without all spells and awaken the Dreamer.
    Ending B: Obtain enough Strange Coins and enter the door located in the Labyrinth of Ash.
    Ending CD: Reach Chamber of the Sleeper and stare into the water pool.
    Ending E: Reach Chamber of the Sleeper with all spells after watching the White VHS Tape and awaken the Dreamer."""
    internal_name = "ending"
    display_name = "Ending"
    option_any_ending = 0
    option_ending_a = 1
    option_ending_b = 2
    option_ending_cd = 3
    option_ending_e = 4
    default = 1


class Class(Choice):
    """The class you play as.
    Note: The following classes are handled differently in the game:
    Vampire has free access to the cattle cells and the first area, so the first vampiric symbol is unnecessary.
    Custom is an advanced option.  If on a website its values will not be visible.  You know how it is smh."""
    internal_name = "starting_class"
    display_name = "Class"
    option_thief = 0
    option_knight = 1
    option_witch = 2
    option_vampire = 3
    option_undead = 4
    option_royal = 5
    option_cleric = 6
    option_shinobi = 7
    option_forsaken = 8
    option_custom = 9


class StartingArea(Choice):
    """Where the player starts.  You will always land in the starting spot in Hollow Basin but it will be blocked off.
    Demi will warp you to Wing's Rest, and the crystal will have the given starting area.
    If starting area is Accursed Tomb, Clive will give you an Oil Lantern."""
    internal_name = "starting_area"
    display_name = "Starting Area"
    option_basin = 0
    option_mire = 1
    option_forest = 2
    option_archives = 3
    option_tomb = 4
    option_castle = 5
    option_grotto = 6
    option_prison = 7
    option_arena = 8
    option_ash = 9
    default = 0


class EntranceRandomization(Toggle):
    """Shuffles the entrances around.  The only untouched entrances are crystal warps (including spell/item), entrance to Chamber of Fate, entrance to
    Grave of the Sleeper, and the doors of Tower of Abyss."""
    internal_name = "entrance_randomization"
    display_name = "Entrance Randomization"


class Experience(Range):
    """Multiplier for gained experience as a percent.  Ranges from 25% to 400%."""
    internal_name = "experience"
    display_name = "Experience Modifier"
    range_start = 25
    range_end = 400
    default = 100


class WeaponExperience(Range):
    """Multiplier for gained weapon experience as a percent.  Ranges from 25% to 400%"""
    internal_name = "weapon_experience"
    display_name = "Weapon Experience Modifier"
    range_start = 25
    range_end = 400
    default = 100


class RequiredStrangeCoins(Range):
    """Changes the required coins needed to open the door for Ending B."""
    internal_name = "required_strange_coin"
    display_name = "Required Strange Coins"
    range_start = 1
    range_end = 60
    default = 30


class TotalStrangeCoins(Range):
    """The total amount of strange coins placed in the multiworld.  Matches required if lower than it.
    Note: Filler will be replaced to compensate."""
    internal_name = "total_strange_coin"
    display_name = "Total Strange Coins"
    range_start = 1
    range_end = 60
    default = 30


class RandomElements(Toggle):
    """Randomizes the elements of almost all weapons and spells.  Guaranteed Poison ranged option.
    Lucid Blade and Wand of Power are not randomized (either due to limitation, or to guarantee victory)"""
    internal_name = "random_elements"
    display_name = "Random Elements"


class EnemyRandomization(Toggle):
    """Shuffles the in-game enemies around. Each enemy in the game is replaced by some other enemy.
    THIS IS EXPERIMENTAL.  Report any weirdness or problems."""
    internal_name = "enemy_randomization"
    display_name = "Enemy Randomization"


class Shopsanity(Toggle):
    """Choose whether the unique items Sheryl the Crow sells are locations.
    Adds 9 locations."""
    internal_name = "shopsanity"
    display_name = "Shuffle Shop Items"


class Dropsanity(Choice):
    """Choose whether the items monsters drop are locations.
    Off: All drops are vanilla.
    Uniques: Only the unique first-drop items (weapons, spells, elixirs) are locations.  Adds 19 locations.
    Randomized: Each drop is a location.  WARNING SOME DROPS ARE HORRIBLE TO GET.  Adds 143 locations."""
    internal_name = "dropsanity"
    display_name = "Mob Drops"
    option_off = 0
    option_uniques = 1
    option_randomized = 2
    default = 0


class Quenchsanity(Toggle):
    """If a weapon can gain experience, if it is quenched, it returns a check.
    Quenching a weapon now no longer upgrades the weapons, and all quench weapons are added to the pool.
    Exceptions: Brittle Arming Sword repairs itself for the sake of the player, and Death Scythe is removed from the inventory as normal."""
    internal_name = "quenchsanity"
    display_name = "Quenchsanity"


class EtnasPupil(Toggle):
    """Become Etna's pupil!  As in, all alchemy creations are locations to check.  Cmon saying -sanity a lot is boring.
    If Dropsanity: Randomized is selected, each material is force placed on drops or alchemy spots to ensure repeatability."""
    internal_name = "etnas_pupil"
    display_name = "Etna's Pupil"


class Bookworm(Toggle):
    """Love reading?  Of course you do!  Every lore spot is a check.  Does not include basic signs.  All of this will be on the exam.
    Adds 67 locations."""
    internal_name = "bookworm"
    display_name = "Bookworm"


class Levelsanity(Toggle):
    """The experience you would gain instead gives you checks for every level.  Levels in the form of Deep Knowledge items are given to compensate which do give a level.
    Adds up to 100 locations (amount depends on starting class)."""
    internal_name = "levelsanity"
    display_name = "Levelsanity"


class Grasssanity(Toggle):
    """Every foliage object that normally drops something is a check.  The original drops do drop as normal for now.  Adds 502 locations."""
    internal_name = "grasssanity"
    display_name = "Grasssanity"


class Breakables(Toggle):
    """Every non-foliage breakable object that normally drops something is a check.  The original drops do drop as normal for now.  Adds 318 locations."""
    internal_name = "breakables"
    display_name = "Breakables"


class NormalizedDrops(Toggle):
    """Every enemy drop is normalized against the chance of dropping nothing.  Specifically, if an enemy
    has a weight of X to drop nothing, everything else also has a weight of X, and is split evenly for every
    item it could drop.  Helps with the sin of the Angel Feather."""
    internal_name = "normalized_drops"
    display_name = "Normalized Drops"


class SwitchLocks(Toggle):
    """All physical switches (not mirages) are locked, and cannot be flipped without their relevant item.
    Note: Removes filler at random to compensate."""
    internal_name = "switch_lock"
    display_name = "Lock Switches"


class DoorLocks(Toggle):
    """All physical doors leading to new zones are locked, and cannot be opened without their relevant item.
    Note: Removes filler at random to compensate."""
    internal_name = "door_lock"
    display_name = "Lock Doors"


class SecretDoorLock(Toggle):
    """All secret doors are locked until receiving the Dusty Crystal Orb."""
    internal_name = "secret_door_lock"
    display_name = "Secret Door Lock"


class Filler(OptionDict):
    """Lets you decide which filler are added to the game and their weights.  If the set is empty or all values are zero,
    Silver and Deep Knowledge will be forced included with weights of 1. Amount received in game is a random value between 1~5, favoring 1~2."""
    internal_name = "filler"
    display_name = "Filler"
    valid_keys = [item for item in default_filler_weights]
    default = default_filler_weights


class FillerLocalPercent(Range):
    """How much of filler is forced local?  Helpful when you don't want to fill the multiworld with your own junk but its fine if some of it bleeds out.
    Note that 0% just means none of it is *forced* to be local, not that it is all non-local."""
    internal_name = "filler_local_percent"
    display_name = "Filler Local Percent"
    range_start = 0
    range_end = 98
    default = 0


class Traps(OptionDict):
    """Lets you decide which traps are in your game and their weights.  If empty or all values are zero, same as having 0 Trap Percent.
    Certain joyous traps are allowed during Christmas, otherwise are ignored.
    Acceptable Traps: "Bleed Trap", "Poison Trap", "Curse Trap", "Slowness Trap", "Blindness Trap", "Mana Drain Trap", "XP Drain Trap", Coal, Eggnog."""
    internal_name = "traps"
    display_name = "Traps"
    valid_keys = [trap for trap in default_trap_weights]
    default = default_trap_weights


class TrapPercent(Range):
    """Percent of filler items to be converted to traps."""
    internal_name = "trap_percent"
    display_name = "Trap Percent"
    range_start = 0
    range_end = 100
    default = 20


class CustomMusic(Toggle):
    """Lets you use custom music.  If on, will read from a CustomMusic folder in the game's base directory.  Only accepts mp3 files.
    If no music is supplied, will be the same as if this setting was off."""
    internal_name = "custom_music"
    display_name = "Custom Music"


class ItemColors(OptionDict):
    """Lets you determine the colors of items in-game using hexadecimal.  This includes Progression, Useful, Trap, Filler, Gifts, and
    Cheated (!getitem, starting inventory, etc)."""
    internal_name = "item_colors"
    valid_keys = ["ProgUseful", "Progression", "Useful", "Trap", "Filler", "Gift", "Cheat"]
    display_name = "Item Colors"
    default = {
        "ProgUseful": "#FF8000",
        "Progression": "#A335EE",
        "Useful": "#0070DD",
        "Trap": "#FA8072",
        "Filler": "#1EFF00",
        "Gift": "#FF8DA1",
        "Cheat": "#FF0000",
    }


class CustomClass(OptionDict):
    """If 'Custom' is chosen for starting class, this is used as a stand-in for that information.
    If Name or Description is 'RANDOM', or any stat is -1, a random value will be supplied.
    Level ranges from 1 to 10.
    Stats (Strength to Resistance) range from 1 to 20.
    Resistances (Normal Res to Dark Res) range from 0 to 300."""
    internal_name = "custom_class"
    display_name = "Custom Class"
    valid_keys = ["Name", "Description", "Level", "Strength", "Speed", "Intelligence", "Defense", "Dexterity", "Resistance", "Normal Res",
                  "Fire Res", "Ice Res", "Poison Res", "Light Res", "Dark Res"]
    default = {
        "Name": "RANDOM",
        "Description": "RANDOM",
        "Level": -1,
        "Strength": -1,
        "Speed": -1,
        "Intelligence": -1,
        "Defense": -1,
        "Dexterity": -1,
        "Resistance": -1,
        "Normal Res": -1,
        "Fire Res": -1,
        "Ice Res": -1,
        "Poison Res": -1,
        "Light Res": -1,
        "Dark Res": -1,
    }


@dataclass
class LunacidOptions(PerGameCommonOptions):
    ending: Ending
    starting_class: Class
    starting_area: StartingArea
    entrance_randomization: EntranceRandomization
    experience: Experience
    weapon_experience: WeaponExperience
    random_elements: RandomElements
    enemy_randomization: EnemyRandomization
    required_strange_coin: RequiredStrangeCoins
    total_strange_coin: TotalStrangeCoins
    shopsanity: Shopsanity
    dropsanity: Dropsanity
    quenchsanity: Quenchsanity
    etnas_pupil: EtnasPupil
    bookworm: Bookworm
    levelsanity: Levelsanity
    grasssanity: Grasssanity
    breakables: Breakables
    normalized_drops: NormalizedDrops
    secret_door_lock: SecretDoorLock
    switch_locks: SwitchLocks
    door_locks: DoorLocks
    filler: Filler
    filler_local_percent: FillerLocalPercent
    traps: Traps
    trap_percent: TrapPercent
    custom_music: CustomMusic
    item_colors: ItemColors
    custom_class: CustomClass
    death_link: DeathLink
