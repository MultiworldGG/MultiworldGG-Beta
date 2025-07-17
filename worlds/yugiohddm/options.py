import typing
import dataclasses

from Options import Range, Choice, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Progression(Choice):
    """
    Free Duel mode means all progression will be made through the Free Duel menu
    culminating in a fight against Yami Yugi.
    Your game will be longer per duelist you set to play against.
    Grandpa's Shop will never advance in this mode.

    Tournament mode means all progression will be made in Tournaments with the
    goal being completing The Last Judgement in the Dark Tournament Division.
    24 - 72 duel wins required, depending on checks you receive.
    """
    display_name = "Goal"
    option_free_duel = 0
    option_tournaments = 1
    default = 1

class DuelistRematches(Choice):
    """
    This option only matters when your Progression mode is Free Duel.

    No matter what choice is made here, Yami Yugi will be unlocked after defeating every duelist
    at least once.

    "No Rematches" means each duelist you unlock can be beaten only once to yield a check.

    "One Rematch" means each duelist you unlock can be beaten twice to yield two different checks.

    The more rematches you add, the more game time you can expect to have.
    Extra check locations are randomized dice rewards that get added to your dice pool.
    """
    display_name = "Duelist Rematches"
    option_no_rematches = 0
    option_one_rematch = 1
    default = 0

class StartingDuelists(Range):
    """
    This option only matters when your Progression mode is Free Duel.
     
    The number of Duelists to start with unlocked.
    There are 92 duelists in total, Yami Yugi is reserved for the game's goal so the limit is 91.
    Setting the number to 91 would automatically put you in go-mode.
    Each extra duelist you start with unlocked also represents one more filler item for you
    instead of their normal progression item.
    """
    display_name = "Starting Duelists"
    range_start = 1
    range_end = 91
    default = 10

class RandomizeStartingDice(Toggle):
    """
    In the base game your starting pool is lightly randomized to begin with,
    but this setting takes off the guardrails and generates you with any
    15 dice from the game (no duplicates).

    It is impossible to generate a starting pool with only items and no creatures to summon.

    With this option active you have to select all of your new dice from your collection
    before the first duel begins.
    """
    display_name = "Randomize Starting Dice"

#class BonusItemMode(Choice):
#    """
#    Decide what you would like to receive from filler checks.
#
#    Random Dice will reward any random die from the game. You won't receive
#    two of the same dice as rewards in this way, all rewards are unique.
#    In Tournament Progression mode, Grandpa's Shop can still progress this way
#    although it is quite slow. Approximately 3-6 Tournament wins per shop level.
#
#    Shop Progress will divide the number of filler checks between
#    Shop Levels and Gold items. This will halt normal shop progression
#    if you have chosen Tournament mode instead of Free Duel.
#    """
#    display_name = "Bonus Item Mode"
#    option_random_dice = 0
#    option_shop_progress = 1
#    default = 0
#
#class GoldRewardMinimum(Range):
#    """
#    This option only matters when your Bonus Item Mode option is Shop Progress.
#    
#    The minimum amount of gold you will receive from Gold filler checks.
#    """
#    display_name = "Gold Reward Minimum"
#    range_start = 0
#    range_end = 65534
#    default = 1000
#
#class GoldRewardMaximum(Range):
#    """
#    This option only matters when your Bonus Item Mode option is Shop Progress.
#    
#    The maximum amount of gold you will receive from Gold filler checks.
#    The player can't hold more than 65,535 gold at a time. Any gold received
#    that would overflow is capped at 65,535.
#    The most expensive shop item costs 50,000 gold.
#    """
#    display_name = "Gold Reward Maximum"
#    range_start = 1
#    range_end = 65535
#    default = 10000

@dataclass
class YGODDMOptions(PerGameCommonOptions):
    progression: Progression
    duelist_rematches: DuelistRematches
    starting_duelists: StartingDuelists
    randomize_starting_dice: RandomizeStartingDice
    #bonus_item_mode: BonusItemMode
    #gold_reward_minimum: GoldRewardMinimum
    #gold_reward_maximum: GoldRewardMaximum

    

    def serialize(self) -> typing.Dict[str, int]:
        return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}