from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, OptionSet, Toggle


class enabled_girls(OptionSet):
    """girls enabled to be accessed NOTE if goal is to give in panties kyu will be enabled no matter this setting"""
    display_name = "enabled girls"
    valid_keys = [
        "tiffany",
        "aiko",
        "kyanna",
        "audrey",
        "lola",
        "nikki",
        "jessie",
        "beli",
        "kyu",
        "momo",
        "celeste",
        "venus"
    ]
    default = valid_keys.copy()

class goal(Toggle):
    """true will set the goal to be giving kyu all available girls panties, false will set the goal to have sex with all available girls"""
    display_name = "goal"
    default = True

class starting_girls(Range):
    """number of girls you start unlocked"""
    display_name = "Girls Unlocked"
    range_start = 2
    range_end = 12
    default = 3

class puzzle_moves(Range):
    """number of moves you start the puzzles with"""
    display_name = "puzzle moves"
    range_start = 10
    range_end = 99
    default = 20

class puzzle_affection_base(Range):
    """the base affection you start the puzzles with"""
    display_name = "puzzle affection base"
    range_start = 1
    range_end = 5000
    default = 200

class puzzle_affection_add(Range):
    """affection added to base affection after every successful date capped at 999999"""
    display_name = "puzzle affection add"
    range_start = 10
    range_end = 500
    default = 100

class shop_items(Range):
    """number of archipelago items in the shop Note if there is not enough locations for items it will add shop locations to satisfy the locations needed, MAX is 480 so total locations isn't over 1000"""
    display_name = "shop items"
    range_start = 0
    range_end = 480
    default = 0

class exclude_shop_items(Range):
    """shop items after the number set will be excluded from having progression items in them. will do nothing if set higher than the number of shop items,
    NOTE will cause world generation to fail if number is set too low as there will be not enough location slots for progression items"""
    display_name = "shop location exclude start"
    range_start = 0
    range_end = 480
    default = 20

class shop_item_cost(Range):
    """the cost of each arch item location in the shop"""
    display_name = "shop item cost"
    range_start = 100
    range_end = 50000
    default = 1000

class shop_gift_cost(Range):
    """the cost of each gift item in the shop"""
    display_name = "shop item cost"
    range_start = 100
    range_end = 50000
    default = 2500

class hunie_gift_cost(Range):
    """the cost of each gift item when buying using hunie"""
    display_name = "hunie item cost"
    range_start = 1000
    range_end = 99999
    default = 10000

class filler_item(Range):
    """how the filler item is handled by making them all either:
    1:nothing items,
    2:random non progression item"""
    display_name = "filler item"
    range_start = 1
    range_end = 2
    default = 2


@dataclass
class HPOptions(PerGameCommonOptions):
    enabled_girls: enabled_girls
    number_of_starting_girls: starting_girls
    number_shop_items: shop_items
    exclude_shop_items: exclude_shop_items
    shop_item_cost: shop_item_cost
    shop_gift_cost: shop_gift_cost
    hunie_gift_cost: hunie_gift_cost
    puzzle_moves: puzzle_moves
    puzzle_affection_base: puzzle_affection_base
    puzzle_affection_add: puzzle_affection_add
    filler_item:filler_item
    goal: goal
