
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld



from dataclasses import dataclass
from Options import *
from .constants import *


class GoalUnlockCondition(Choice):
    """
    How should Metal Madness/Overlord be unlocked?
    Level Completions will require reaching the goal ring in a certain number of levels
    Emerald Hunt will only require the 7 chaos emeralds (received as Items)
    """
    internal_name = "goal_unlock_condition"
    display_name = "Goal Unlock Condition"
    option_level_completions = 0
    option_emerald_hunt = 1
    option_level_completions_and_emeralds = 2
    #option_all_abilities = 3
    default = 0


class GoalLevelCompletions(Range):
    """
    How Many Level Completions are needed per Story to unlock Metal Madness/Overlord?
    This Requires Level Completion Goal Unlock Condition.
    Each Story will require at least this many completed levels.
    Required Rank will also affect this.
    """
    internal_name = "goal_level_completions"
    display_name = "Goal Level Completions"
    range_start = 0
    range_end = 14
    default = 7


class AbilityUnlocks(Choice):
    """
    How should Ability Unlocks be Handled?
    Entire Story will make there be a "Homing Attack" item for each Team that unlocks Homing Attack on all levels for that team.
    All Regions Separate will have 7 sets of ability items (Per Team) that unlock the ability for that respective region. (A Region is a set of levels that follow the same theme)
    For example, Seaside Hill and Ocean Palace are both in the Ocean Region

    Dev Note: All Regions Separate can cause significant BK in syncs (depending on speed of other games)
    Recommended for asyncs only (or with proper consideration)
    """
    internal_name = "ability_unlocks"
    display_name = "Ability Unlocks"
    option_all_regions_separate = 0
    option_entire_story = 1
    default = 1



class SonicStory(Choice):
    """
    Should Sonic Story Missions be enabled?
    """
    internal_name = "sonic_story"
    display_name = "Sonic Story"
    #option_disabled = 0
    option_mission_a_only = 1
    option_mission_b_only = 2
    option_both_missions_enabled = 3
    default = 1

class SonicStoryStartingCharacter(Choice):
    """
    Which Character should be unlocked for Sonic Story from the Start?
    Knuckles has the largest sphere 1
    Sonic and Tails are even though Tails is slightly more restrictive logically
    """
    internal_name = "sonic_story_starting_character"
    display_name = "Sonic Story Starting Character"
    option_sonic = 0
    option_tails = 1
    option_knuckles = 2
    # noinspection PyClassVar
    default = 'random'  # type: ignore


class SonicKeySanity(Choice):
    """
    Getting a bonus key sends a check.
    This is separate per team enabled
    Only 1 Set makes it only 1 set of keys to collect (for the team) (this allows getting the key in either Act without being a separate check)
    Set For Each Act has one set of keys for each Act enabled (requires both Acts enabled to have both sets)
    """
    internal_name = "sonic_key_sanity"
    display_name = "Sonic Key Sanity"
    option_disabled = 0
    option_Only1Set = 1
    option_SetForEachAct = 2
    default = 1


class SonicCheckpointSanity(Choice):
    """
    Getting a checkpoint sends a check. (This is easier than KeySanity)
    This is separate per team enabled
    Only 1 Set makes it only 1 set of checkpoints to collect (for the team) (this allows getting the checkpoint in either Act without being a separate check)
    Set For Each Act has one set of checkpoints for each Act enabled (requires both Acts enabled to have both sets)
    """
    internal_name = "sonic_checkpoint_sanity"
    display_name = "Sonic Checkpoint Sanity"
    option_disabled = 0
    option_Only1SetNormal = 1
    #option_OnlySuperHard = 2
    option_SetForEachAct = 3
    default = 1


class RemoveCasinoParkVIPTableLaserGate(DefaultOnToggle):
    """
    This Option will Remove the Laser Gate in front of the ramp before the VIP Table in Casino Park.
    This allows access to the Bonus Key there and the VIP table without having to get the switch on the pinball table before.
    """
    internal_name = "remove_casino_park_vip_table_laser_gate"
    display_name = "Remove Casino Park VIP Table Laser Gate"
    """"""




#class SecretLocations(Toggle):
    """
    This option currently does nothing but is planned for later.
    """
    #internal_name = "secret_locations"
    #display_name = "Secret/OOB Locations"




sonic_heroes_option_groups = \
    [
        OptionGroup("Goal",
            [
                GoalUnlockCondition,
                GoalLevelCompletions,
                AbilityUnlocks,
            ]),


        OptionGroup("Stories",
            [
                SonicStory,
                SonicStoryStartingCharacter,
                #SecretLocations,
            ]),

        OptionGroup("Sanity",
            [
                SonicKeySanity,
                SonicCheckpointSanity
            ]),
        OptionGroup("QOL",
            [
                RemoveCasinoParkVIPTableLaserGate,
            ]),
        OptionGroup("DeathLink",
            [
                DeathLink
            ]),
]


@dataclass
class SonicHeroesOptions(PerGameCommonOptions):

    goal_unlock_condition: GoalUnlockCondition
    goal_level_completions: GoalLevelCompletions
    ability_unlocks: AbilityUnlocks

    sonic_story: SonicStory
    sonic_story_starting_character: SonicStoryStartingCharacter
    sonic_key_sanity: SonicKeySanity
    sonic_checkpoint_sanity: SonicCheckpointSanity
    #secret_locations: SecretLocations
    remove_casino_park_vip_table_laser_gate: RemoveCasinoParkVIPTableLaserGate

    death_link: DeathLink



def check_invalid_options(world: SonicHeroesWorld):

    #if world.options.sonic_story == "disabled":
        #raise OptionError(f"SONIC STORY MUST BE ENABLED")

    if world.options.ability_unlocks == AbilityUnlocks.option_all_regions_separate:
        if world.options.sonic_story != SonicStory.option_both_missions_enabled: #Not Both Acts
            if (world.options.sonic_key_sanity == SonicKeySanity.option_disabled or
                    world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_disabled):
                raise OptionError(f"Region Based Ability Unlocks with only 1 Act Requires "
                                  f"Both Key Sanity and Checkpoint Sanity")
        else:
            if (world.options.sonic_key_sanity == SonicKeySanity.option_disabled or
                    world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_disabled):
                if (world.options.sonic_key_sanity != SonicKeySanity.option_SetForEachAct and
                        world.options.sonic_checkpoint_sanity != SonicCheckpointSanity.option_SetForEachAct):
                    raise OptionError(f"Region Based Ability Unlocks with both acts Requires "
                                      f"either Both Key Sanity and Checkpoint Sanity or one of "
                                      f"those with both sets (Set For Each Act)")

    else:
        if (world.options.sonic_key_sanity == SonicKeySanity.option_disabled and
                world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_disabled):
            raise OptionError(f"Entire Story Ability Unlocks Requires Either Key Sanity "
                              f"or Checkpoint Sanity To Be Enabled")






