from dataclasses import dataclass
from Options import (DefaultOnToggle, Toggle, Choice, Range, PerGameCommonOptions, DeathLink)
from .Locations import victory_names
from .Items import item_table


class FillerTrapPercent(Range):
    diplay_name = "Filler Traps"
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100


class Goal(Choice):
    """Choose your victory condition."""
    display_name = "Goal"
    default = 0
    option_goal_all_missions_complete = 0
    option_goal_all_story_missions_complete = 1
    option_goal_final_missionl7m7 = 2
    option_goal_wasps_and_cards_collected = 3


class LevelSanity(Choice):
    """Choose how you want missions to be sent in the multiworld. Levels logically require the level access item and at least 1 car from that level or higher. You're guaranteed to start with a level and it's default car with either option.
       Linear will add progressive levels to the pool. You'll start with Level 1 and the Family Sedan, then get the next level each time you receive a progressive level item.
       Levels will add levels to the pool. You'll start the game with a random level and it's required items and receive levels from the multiworld.
       Regardless of your choice, missions can be played in any order on an unlocked level.
       """
    display_name = "Levelsanity"
    option_linear = 0
    option_levels = 1
    default = 1

class MoveRando(Toggle):
    """Choose whether or not to shuffle moves into the item pool.
       Moves that are shuffled are Double Jump and Attack for each character.
       These have logical implications for wasp and card collection
       as well as L7M4 requiring Homer Double Jump.
       """

    default = True
    display_name = "Move Randomizer"

class ShuffleEBrakes(Toggle):
    """Choose whether or not to shuffle ability to use the E-Brake
       for each character into the item pool. *WARNING* This is not
       considered in logic and has not been heavily tested.
       It may create unreasonably hard seeds.
       """

    default = True
    display_name = "Shuffle E-Brake"

class EnableWaspPercent(Toggle):
    """Whether to include Wasps in goal requirements.
       This setting is always treated as true if your
       goal is Goal: Wasps and Cards Collected!"""

    default = True
    display_name = "Enable Wasp Requirements"

class WaspPercent(Range):
    """ Percent of Wasps required to goal if Wasp Requirements is enabled."""
    display_name = "Required Wasp Percent"
    range_start = 10
    range_end = 100
    default = 50

class EnableCardPercent(Toggle):
    """Whether to include Cards in goal requirements.
       This setting is always treated as true if your
       goal is Goal: Wasps and Cards Collected!"""

    default = True
    display_name = "Enable Card Requirements"

class CardPercent(Range):
    """Percent of Cards required to goal if Card Requirements is enabled."""
    display_name = "Required Card Percent"
    range_start = 10
    range_end = 100
    default = 50

class MinShopPrice(Range):
    """The minimum cost of any item in Gil's Shop. If this is greater than the max shop price, then the max will be used instead."""
    display_name = "Min Shop Price"
    range_start = 0
    range_end = 500
    default = 100

class MaxShopPrice(Range):
    """The maximum cost of any item in Gil's Shop."""
    display_name = "Max Shop Price"
    range_start = 0
    range_end = 500
    default = 300

class ShopScaleMod(Range):
    """The multiplier for shop costs per levels
       L2 costs = L1 * multiplier, L3 = L1 * 2(multiplier), etc"""
    display_name = "Shop Price Level Scale Multiplier"
    range_start = 1
    range_end = 5
    default = 2

@dataclass
class SimpsonsHitAndRunOptions(PerGameCommonOptions):
    goal: Goal
    levelsanity: LevelSanity
    moverandomizer: MoveRando
    shuffleebrake: ShuffleEBrakes
    EnableWaspPercent: EnableWaspPercent
    wasppercent: WaspPercent
    EnableCardPercent: EnableCardPercent
    cardpercent: CardPercent
    minprice: MinShopPrice
    maxprice: MaxShopPrice
    shopscalemod: ShopScaleMod
    filler_traps: FillerTrapPercent
    death_link: DeathLink


SimpsonsHitAndRunOptions = SimpsonsHitAndRunOptions
