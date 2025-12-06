from dataclasses import dataclass
from Options import Toggle, StartInventoryPool, DeathLink, PerGameCommonOptions, Choice, Range, DefaultOnToggle, \
    OptionGroup


def adjust_options(world):
    if world.options.max_kiosk_cost < world.options.min_kiosk_cost:
        world.options.max_kiosk_cost.value, world.options.min_kiosk_cost.value = \
         world.options.min_kiosk_cost.value, world.options.max_kiosk_cost.value

    if world.options.max_elevator_cost < world.options.min_elevator_cost:
        world.options.max_elevator_cost.value, world.options.min_elevator_cost.value = \
         world.options.min_elevator_cost.value, world.options.max_elevator_cost.value

    if world.options.max_custom_goal_cost < world.options.min_custom_goal_cost:
        world.options.max_custom_goal_cost.value, world.options.min_custom_goal_cost.value = \
         world.options.min_custom_goal_cost.value, world.options.max_custom_goal_cost.value

    tot_coins: int = total_coins(world)
    if world.options.max_kiosk_cost > tot_coins - 6:
        world.options.max_kiosk_cost.value = min(70, tot_coins - 6)

    if world.options.min_kiosk_cost > tot_coins - 6:
        world.options.min_kiosk_cost.value = min(70, tot_coins - 6)

    if world.options.max_elevator_cost > tot_coins:
        world.options.max_elevator_cost.value = min(79, tot_coins)

    if world.options.min_elevator_cost > tot_coins:
        world.options.min_elevator_cost.value = min(79, tot_coins)

    if world.options.max_custom_goal_cost > tot_coins:
        world.options.max_custom_goal_cost.value = tot_coins

    if world.options.min_custom_goal_cost > tot_coins:
        world.options.min_custom_goal_cost.value = tot_coins

    if world.options.swimming.value == 0:
        world.options.precisejumps.value = 0

    if world.options.cassette_logic.value == 0:
        world.options.extra_cassettes.value = 0

    if world.options.shuffle_kiosk_reward.value == 0:
        world.options.access_garys_garden.value = 0

    if world.options.goal_completion.value == 3:
        world.options.shuffle_garys_garden.value = 1

    if world.options.goal_completion.value == 4:
        world.options.shuffle_kiosk_reward.value = 1
        world.options.shuffle_garys_garden.value = 1
        world.options.access_garys_garden.value = 2
        if world.options.cassette_logic.value == 1:
            world.options.cassette_logic.value = 2
        world.options.fishsanity.value = 2
        world.options.seedsanity.value = 2
        world.options.flowersanity.value = 2
        world.options.bonesanity.value = 2

    if world.options.shuffle_kiosk_reward.value == 0:
        world.options.start_with_ticket.value = 1

def total_coins(world) -> int:
    count: int = 76
    if world.options.shuffle_garys_garden.value:
        count += 3
    return count

class ShuffleKioskReward(DefaultOnToggle):
    """Choose whether to shuffle the Kiosk to NOT give the next Ticket but instead something else.
    Compatible with 'Start with Ticket'.
    Check the in-game Tracker for Kiosk Cost and if you bought it."""
    display_name = "Shuffle Kiosk Reward"


class StartWithTicket(DefaultOnToggle):
    """You'll start with a random Ticket. Highly recommended as there are only 3 checks at Home!"""
    display_name = "Start with Ticket"


class EnableAchievements(Choice):
    """Enables if Achievements should be a location.
    Frog Fan only needs 10 bumps & Volley Dreams only needs a highscore of 5 in every level."""
    display_name = "Enable Achievements"
    option_all_achievements = 0
    option_except_snail_fashion_show = 1
    option_disabled = 2
    default = 2


class ShuffleHandsomeFrog(Toggle):
    """Enables if talking to Handsome Frog should be a location."""
    display_name = "Shuffle Handsome Frog"


class ShuffleGarysGarden(DefaultOnToggle):
    """Choose whether Gary's Garden should have locations."""
    display_name = "Shuffle Gary's Garden"


class GarysGardenAccess(Choice):
    """Changes when Gary's Garden is accessible.
    Tadpole HQ: Gary's Garden will be accessible when Tadpole HQ is accessible.
    -----------------------------------------------------------
    Tadpole HQ & Gary's Garden: Gary's Garden won't be accessible until Tadpole HQ Ticket & Gary's Garden Ticket are obtained.
    -----------------------------------------------------------
    Gary's Garden: Gary's Garden will be accessible in 'Home' when Gary's Garden Ticket has been obtained."""
    display_name = "Gary's Garden Access"
    option_tadpole_hq = 0
    option_tadpole_and_garden = 1
    option_garden = 2
    default = 1


class KeysLevelBased(Toggle):
    """If this option is enabled, Keys will be specific to the level.
    Hairball City Keys only open Hairball City Locks, Turbine Town Keys only open Turbine Town Locks etc."""
    display_name = "Level Specific Keys"


class GoalCompletion(Choice):
    """Set your Completion Goal.
    Hired: Reach Pepper's Interview and get hired!
    Employee: Get 76 Coins and be the Employee Of The Month!
    Custom: Get a custom amount of coins to complete the game!
    Garden: Restore Gary's Garden to its former glory!
    Friend: Be everyone's best friend by helping Mitch, Mai, Little Gabi, Fischer, Moomy and co. (This will enable Fishsanity, Seedsanity, Flowersanity and Bonesanity)"""
    display_name = "Completion Goal"
    option_hired = 0
    option_employee = 1
    option_custom = 2
    option_garden = 3
    option_friend = 4
    default = 0


class MinKioskCost(Range):
    """Determines the lowest possible cost for a Kiosk.
    Disabled if 'Shuffle Kiosk Reward' is false"""
    display_name = "Minimum Kiosk Cost"
    range_start = 0
    range_end = 55
    default = 1


class MaxKioskCost(Range):
    """Determines the highest possible cost for a Kiosk.
    Disabled if 'Shuffle Kiosk Reward' is false"""
    display_name = "Maximum Kiosk Cost"
    range_start = 20
    range_end = 70
    default = 38


class MinElevatorCost(Range):
    """Determines the lowest possible cost for the elevator"""
    display_name = "Minimum Elevator Repair Cost"
    range_start = 0
    range_end = 79
    default = 46


class MaxElevatorCost(Range):
    """Determines the highest possible cost for the elevator"""
    display_name = "Maximum Elevator Repair Cost"
    range_start = 0
    range_end = 79
    default = 46


class MinCustomGoalCost(Range):
    """Determines the lowest possible cost the custom goal."""
    display_name = "Minimum Custom Goal Cost"
    range_start = 10
    range_end = 79
    default = 20


class MaxCustomGoalCost(Range):
    """Determines the highest possible cost the custom goal."""
    display_name = "Maximum Custom Goal Cost"
    range_start = 20
    range_end = 79
    default = 50


class CassetteLogic(Choice):
    """This changes how Mitch & Mai work

    LevelBased: Cassettes have been split up into level specific variants.
    So you need 'Hairball City Cassette' 5x/10x to trade with Mitch/Mai in Hairball City.
    -----------------------------------------------------------
    Progressive: Mitch and Mai require increasing numbers of cassettes to unlock their locations.
    Unlock order is fixed: The number of cassettes needed progresses incrementally -> 5 -> 10 -> 15 -> 20 -> 25.
    The in-game Cassette Tracker shows from left to right your progress.
    When you buy the first progressive unlock, the first Mitch/Mai icon will be marked as purchased.
    If Gary's Garden is shuffled -> The tracker starts at Gary's Garden. If not shuffled -> The tracker starts at Hairball City.
    -----------------------------------------------------------
    Scattered: Prices are randomly shuffled between all Mitch & Mai Locations."""
    display_name = "Cassette Logic"
    option_Level_Based = 0
    option_progressive = 1
    option_scattered = 2
    default = 2


class ExtraAmountOfCassettes(Range):
    """This option will try to add extra 'Cassettes' to the Item Pool.
    If there are not enough locations, it will add as many as it can!"""
    display_name = "Extra Cassettes in Item Pool"
    range_start = 0
    range_end = 50
    default = 10


class ProgressiveContactList(DefaultOnToggle):
    """If this option is enabled, the Contact Lists will not be separate, so you cannot get Contact List 2 before Contact List 1."""
    display_name = "Progressive Contact List"


class SnailShopLocations(Toggle):
    """When enabled the clothes shop from the Tamagotchi Snail will contain AP Items."""
    display_name = "Snail Shop"


class SpeedBoostAmountInPool(Range):
    """Determines how many 'Speed Boost' are in the pool."""
    display_name = "Speed Boost in Item Pool"
    range_start = 0
    range_end = 8
    default = 4


class BonkPermit(Toggle):
    """When enabled, a 'Safety Helmet' is required to break breakable blocks."""
    display_name = "Safety Helmet"


class BugNet(Toggle):
    """When enabled, a 'Bug Net' is required to catch bugs."""
    display_name = "Bug net"


class SodaCans(Toggle):
    """When enabled, soda cannons are broken, the item 'Soda Repair' will make the frog engineers repair them.
    DOESN'T INCLUDE THE ELEVATOR!"""
    display_name = "Soda Cans"


class Parasols(Toggle):
    """When enabled, Parasols are broken, the item 'Parasol Repair' will make the frog engineers repair them."""
    display_name = "Parasols"


class Swimming(Toggle):
    """When enabled, a 'Swim Course' is required to swim in water."""
    display_name = "Swimming"


class Textbox(Choice):
    """Want to have a break talking with NPCs?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Global: The item 'Textbox' is required to interact with anything that uses the textbox
    -----------------------------------------------------------
    Level: Every level requires its own textbox item to interact with anything that uses the textbox, so Hairball City needs 'Hairball City Textbox'"""
    display_name = "Textbox"
    option_vanilla = 0
    option_global = 1
    option_level = 2
    default = 0

class AirConditioning(Toggle):
    """When enabled, ACs are broken, the item 'AC Repair' will make the frog engineers repair them."""
    display_name = "Air Conditioners"


class AppleBasket(Toggle):
    """When enabled, Apples cannot be picked up until you have the item 'Apple Basket' to store them in."""
    display_name = "Apple Basket"


class PreciseJumps(Toggle):
    """Only available when Swimming is enabled.
    When this option is enabled, the logic will expect you to reach locations that require precise jumps"""
    display_name = "Precise Jumps"


class Fishsanity(Choice):
    """Need more checks or are you just insane?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Location: Every single fish you can fish with Fischer is a unique location
    -----------------------------------------------------------
    Insanity: Same as location with the change that Fischer won't give you the 'Fish with Fischer' item until you have all 5 fish for that level obtained.
    So you need the item 'Hairball City Fish' 5x before being able to obtain Fischer's reward in Hairball City.
    Check the in-game menu, to see if you have enough fish and obtained the reward from Fischer."""
    display_name = "Fishsanity"
    option_vanilla = 0
    option_location = 1
    option_insanity = 2
    default = 0


class Seedsanity(Choice):
    """Need more checks or are you just insane?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Location: Every single seed you can collect with the hamster ball is a unique location
    -----------------------------------------------------------
    Insanity: Same as location with the change that Moomy won't give you the reward for collecting all seeds until you have been sent all 10 seeds for that level.
    So you need the item 'Hairball City Seed' 10x before being able to obtain Moomy's reward in Hairball City.
    Check the in-game menu, to see if you have enough seeds and obtained the reward from Moomy."""
    display_name = "Seedsanity"
    option_vanilla = 0
    option_location = 1
    option_insanity = 2
    default = 0


class Flowerbedsanity(Choice):
    """Need more checks or are you just insane?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Location: Every single flower bed is a unique location
    -----------------------------------------------------------
    Insanity: Same as location with the change that Little Gabi won't give you the reward for completing all flower beds until you have been sent all flowers for that level.
    So you need the item 'Hairball City Flower' 3x before being able to obtain Little Gabi's reward in Hairball City.
    Check the in-game menu, to see if you have enough flowers and obtained the reward from Little Gabi."""
    display_name = "Flowersanity"
    option_vanilla = 0
    option_location = 1
    option_insanity = 2
    default = 0


class Bonesanity(Choice):
    """Need more checks or are you just insane?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Location: Every single bone is a unique location
    -----------------------------------------------------------
    Insanity: Same as location with the change that Bone Dog won't give you the reward for collecting all bones until you have been sent all bones for that level.
    So you need the item 'Hairball City Bone' 5x before being able to obtain Bone Dog's reward in Hairball City.
    Check the in-game menu, to see if you have enough bones and obtained the reward from Bone Dog."""
    display_name = "Bonesanity"
    option_vanilla = 0
    option_location = 1
    option_insanity = 2
    default = 0


class Applesanity(Toggle):
    """Need more checks or are you just insane?
    When enabled, freestanding apples will be randomized.
    This adds ~290 locations."""
    display_name = "Applesanity"


class Bugsanity(Toggle):
    """Need more checks or are you just insane?
    When enabled, bugs will be randomized.
    This adds 349 locations."""
    display_name = "Bugsanity"


class Chatsanity(Choice):
    """Need more checks or are you just insane?
    Vanilla: Normal Here Comes Niko! behaviour
    -----------------------------------------------------------
    Level Based: Every single NPC you can talk to is a unique location in every level
    -----------------------------------------------------------
    Global: Every single NPC you can talk to is a unique location, but only once, regardless of level"""
    display_name = "Chatsanity"
    option_vanilla = 0
    option_level_based = 1
    option_global = 2


class Thoughtsanity(Toggle):
    """Chatsanity Part 2
    When enabled, Niko's thoughts will send a unique location similar to Chatsanity
    Niko's thought are found at places with a magnifying glass"""
    display_name = "Thoughtsanity"


class TrapChance(Range):
    """The chance for any junk item in the pool to be replaced by a trap."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 25


class FreezeTrapWeight(Range):
    """The weight of Freeze Traps in the trap pool.
    Freeze Traps will temporarily make Niko unable to move."""
    display_name = "Freeze Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class IronBootsTrapWeight(Range):
    """The weight of Iron Boots Traps in the trap pool.
    Iron Boots Traps will make Niko slow & heavy."""
    display_name = "Iron Boots Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class WhoopsTrapWeight(Range):
    """The weight of Whoops! Traps in the trap pool.
    Whoops! Traps will send Niko way up in the sky."""
    display_name = "Whoops! Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class MyTurnTrapWeight(Range):
    """The weight of My Turn! Traps in the trap pool.
    My Turn! Traps will make Niko jump, dive and move in random directions."""
    display_name = "My Turn! Trap Weight"
    range_start = 0
    range_end = 100
    default = 30


class GravityTrapWeight(Range):
    """The weight of Gravity Traps in the trap pool.
    Gravity Traps will temporarily remove gravity."""
    display_name = "Gravity Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class HomeTrapWeight(Range):
    """The weight of Home Traps in the trap pool.
    Home Traps will send Niko back to Home."""
    display_name = "Home Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class WideTrapWeight(Range):
    """The weight of W I D E Traps in the trap pool.
    W I D E Traps will make Niko very wide."""
    display_name = "W I D E Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class PhoneTrapWeight(Range):
    """The weight of Phone Traps in the trap pool.
    Phone Traps will force Niko to receive an unskippable phone call."""
    display_name = "Phone Trap Weight"
    range_start = 0
    range_end = 100
    default = 25


class TinyTrapWeight(Range):
    """The weight of Tiny Traps in the trap pool.
    Tiny Traps will make Niko very tiny."""
    display_name = "Tiny Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class JumpingJacksTrapWeight(Range):
    """The weight of Jumping Jacks Traps in the trap pool.
    Jumping Jacks Traps will make Niko jump continuously."""
    display_name = "Jumping Jacks Trap Weight"
    range_start = 0
    range_end = 100
    default = 25


class CameraStuckTrapWeight(Range):
    """The weight of Camera Stuck Traps in the trap pool.
    Camera Stuck Traps will stop the camera from turning."""
    display_name = "Camera Stuck Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class InvertedCameraTrapWeight(Range):
    """The weight of Inverted Camera Traps in the trap pool.
    Inverted Camera Traps will invert the cameras X and Y controls."""
    display_name = "Inverted Camera Trap Weight"
    range_start = 0
    range_end = 100
    default = 25


class ThereGoesNikoTrapWeight(Range):
    """The weight of There Goes Niko Traps in the trap pool.
    There Goes Niko Traps will make the camera stop in place."""
    display_name = "There Goes Niko Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class HCNDeathLink(DeathLink):
    """When somebody dies the level will be reloaded.
    Can be toggled with '/deathlink' in-game"""


class DeathLinkAmnesty(Range):
    """How many water/scissor touches it takes to send a DeathLink"""
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10


class TrapLink(Toggle):
    """Traps with other TrapLink players are shared.
    Can be toggled with '/traplink' in-game"""
    display_name = "Trap Link"


class RingLink(Toggle):
    """Apples will be shared with other RingLink players.
    Can be toggled with '/ringlink' in-game"""
    display_name = "Ring Link"


@dataclass
class HereComesNikoOptions(PerGameCommonOptions):
    death_link: HCNDeathLink
    death_link_amnesty: DeathLinkAmnesty
    trap_link: TrapLink
    #ring_link: RingLink

    shuffle_kiosk_reward: ShuffleKioskReward
    start_with_ticket: StartWithTicket
    enable_achievements: EnableAchievements
    shuffle_handsome_frog: ShuffleHandsomeFrog
    shuffle_garys_garden: ShuffleGarysGarden
    access_garys_garden: GarysGardenAccess
    level_based_keys: KeysLevelBased
    cassette_logic: CassetteLogic
    extra_cassettes: ExtraAmountOfCassettes
    progressive_contact_list: ProgressiveContactList
    snail_shop: SnailShopLocations
    speed_boost_amount: SpeedBoostAmountInPool

    goal_completion: GoalCompletion
    min_kiosk_cost: MinKioskCost
    max_kiosk_cost: MaxKioskCost
    min_elevator_cost: MinElevatorCost
    max_elevator_cost: MaxElevatorCost
    min_custom_goal_cost: MinCustomGoalCost
    max_custom_goal_cost: MaxCustomGoalCost

    bonk_permit: BonkPermit
    bug_catching: BugNet
    soda_cans: SodaCans
    parasols: Parasols
    swimming: Swimming
    precisejumps: PreciseJumps
    textbox: Textbox
    ac_repair: AirConditioning
    applebasket: AppleBasket

    fishsanity: Fishsanity
    seedsanity: Seedsanity
    flowersanity: Flowerbedsanity
    bonesanity: Bonesanity
    applesanity: Applesanity
    bugsanity: Bugsanity
    chatsanity: Chatsanity
    thoughtsanity: Thoughtsanity

    trapchance: TrapChance
    freeze_trapweight: FreezeTrapWeight
    ironboots_trapweight: IronBootsTrapWeight
    whoops_trapweight: WhoopsTrapWeight
    myturn_trapweight: MyTurnTrapWeight
    gravity_trapweight: GravityTrapWeight
    home_trapweight: HomeTrapWeight
    wide_trapweight: WideTrapWeight
    phone_trapweight: PhoneTrapWeight
    tiny_trapweight: TinyTrapWeight
    jumpingjacks_trapweight: JumpingJacksTrapWeight
    camerastuck_trapweight: CameraStuckTrapWeight
    invertedcamera_trapweight: InvertedCameraTrapWeight
    theregoesniko_trapweight: ThereGoesNikoTrapWeight
    start_inventory_from_pool: StartInventoryPool

hcniko_option_groups = [
    OptionGroup("Goal Options", [
        GoalCompletion,
        MinKioskCost,
        MaxKioskCost,
        MinElevatorCost,
        MaxElevatorCost,
        MinCustomGoalCost,
        MaxCustomGoalCost
    ]),
    OptionGroup("General Options", [
        ShuffleKioskReward,
        StartWithTicket,
        CassetteLogic,
        ExtraAmountOfCassettes,
        EnableAchievements,
        ShuffleHandsomeFrog,
        ShuffleGarysGarden,
        GarysGardenAccess,
        SnailShopLocations,
        SpeedBoostAmountInPool
    ]),
    OptionGroup("Item & Logic Options", [
        KeysLevelBased,
        ProgressiveContactList,
        BonkPermit,
        BugNet,
        SodaCans,
        Parasols,
        Swimming,
        PreciseJumps,
        Textbox,
        AirConditioning,
        AppleBasket
    ]),
    OptionGroup("Location Options", [
        Fishsanity,
        Seedsanity,
        Flowerbedsanity,
        Bonesanity,
        Applesanity,
        Bugsanity,
        Chatsanity,
        Thoughtsanity
    ]),
    OptionGroup("Trap Options", [
        TrapChance,
        FreezeTrapWeight,
        IronBootsTrapWeight,
        WhoopsTrapWeight,
        MyTurnTrapWeight,
        GravityTrapWeight,
        HomeTrapWeight,
        WideTrapWeight,
        PhoneTrapWeight,
        TinyTrapWeight,
        JumpingJacksTrapWeight,
        CameraStuckTrapWeight,
        InvertedCameraTrapWeight,
        ThereGoesNikoTrapWeight
    ])
]