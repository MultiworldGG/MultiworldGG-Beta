from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions, DeathLinkMixin, StartInventoryPool

class GameDifficulty(Choice):
    """Determines expected player skill. A harder difficulty means you will be expected to go further in the game with less resources."""
    display_name = "Game Difficulty"
#    option_easy = 0
    option_normal = 1
    option_hard = 2
#    option_very_hard = 3
    default = 1

class GoalCondition(Choice):
    """Determines the win condition for the game. Myzand 2: Traverse Myzand's Forest, defeat him, and lock him away. Eye Chest: Open the 6-Eye Door and collect the Eye Fragment."""
    display_name = "Goal"
    option_myzand_2 = 0
    option_eye_chest = 1
    default = 0

class ShufflePuzzles(Toggle):
    """When enabled, slide puzzles and their rewards will be shuffled into the pool."""
    display_name = "Shuffle Slide Puzzles"

class StartWithGear(Toggle):
    """When enabled, Blue in Lost Swamp will always give you a gun, and you will always find a spell at the Fireball location. (This may break gun/spell plando, so be warned.)"""
    display_name = "I Hate Seedling"

class ShuffleBugEffects(Toggle):
    """Randomizes the temporary effect gained when eating any bug other than Mushroom."""
    display_name = "Shuffle Bug-Eating Effects"

class ShuffleWorkshopKey(Choice):
    """When enabled, the Workshop Key will be shuffled into the item pool, and Bins will give you a random item after defeating Xoto."""
    display_name = "Shuffle Workshop Key"
    option_enabled = 1
    option_disabled = 0
    option_startwith = 2
    alias_true = 1
    alias_false = 0
    alias_on = 1
    alias_off = 0
    default = 1

class ShopMultiplier(Range):
    """Decreases the total cost of items in shops by a percentage. 100 = no discount, 0 = free shops. This does not impact gun upgrade costs, or buying from Supa."""
    display_name = "Shop Multiplier"
    range_start = 0
    range_end = 100
    default = 100

class OpenCity(Toggle):
    """When enabled, the Lost Swamp portal vine will be enabled from the beginning, allowing quick travel to City without needing to traverse through most of the early game first."""
    display_name = "Open City"

class AdvancedParkour(Toggle):
    """When enabled, the player will be expected to do more advanced or unituitive platform movement to get to some locations."""
    display_name = "Hardcore Parkour"

class WellLightLogic(Choice):
    """Chooses which items will be expected to be acquired for traversing the well. Glowbug for navigating dark passages, Fire Fruit Juicer for relighting the candle after Fire-Eaters, or both."""
    display_name = "Well Light Logic"
    option_none = 0
    option_glowbug = 1
    option_fire_fruit_juicer = 2
    option_both = 3
    default = 1

@dataclass
class FrogmonsterOptions(PerGameCommonOptions, DeathLinkMixin):
    start_inventory_from_pool: StartInventoryPool
    game_difficulty: GameDifficulty
    goal: GoalCondition
    shuffle_puzzles: ShufflePuzzles
    i_hate_seedling: StartWithGear
    shuffle_bug_effects: ShuffleBugEffects
    shuffle_workshop_key: ShuffleWorkshopKey
    shop_multiplier: ShopMultiplier
    open_city: OpenCity
    hardcore_parkour: AdvancedParkour
    well_light_logic: WellLightLogic

