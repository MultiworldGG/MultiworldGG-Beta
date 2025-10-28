from dataclasses import dataclass
from typing import Protocol, ClassVar

from Options import Range, OptionSet, Toggle, PerGameCommonOptions, Choice


class MadouOption(Protocol):
    internal_name: ClassVar[str]


class Goal(Choice):
    """What action is required to completed to goal?
    Certificate: Open the chest that gives you the certificate.
    Tower: Climb the Magical Tower, and defeat Devil.
    Souvenirs: Get the 7 souvenirs and give them to your mother.
    gems: Get the 7 gems and open the secret door in the library."""
    option_certificate = 0
    option_tower = 1
    option_souvenirs = 2
    option_gems = 3
    default = 1


class RequiredStones(Range):
    """How many secret stones are required to get the final exam certificate.  If zero, the ability to ascend Sage's Mountain
    is all that is needed to get it.  Note that the Magical Tower requires nothing save combat experience to clear."""
    internal_name = "required_secret_stones"
    display_name = "Required Secret Stones"
    range_start = 0
    range_end = 8
    default = 8


class SchoolLunch(Choice):
    """Whether the starting 'school lunch' you have (the four Pickled Scallions) are randomized.
    Vanilla: Don't touch the items.
    Consumables: They are four random consumables or equipment items instead.
    Anything: They can be any item."""
    internal_name = "school_lunch"
    display_name = "School Lunch"
    option_vanilla = 0
    option_consumables = 1
    option_anything = 2
    default = 0


class StartingMagic(OptionSet):
    """What magic Arle should start with, out of the starting spells.
    If this list is not default the other spells will be locations that send on start."""
    internal_name = "starting_magic"
    display_name = "Starting Magic"
    valid_keys = ["Healing", "Fire", "Ice Storm", "Thunder"]
    default = valid_keys


class SouvenirHunt(Toggle):
    """The shop souvenirs are shuffled, try to find them!"""
    internal_name = "souvenir_hunt"
    display_name = "Souvenir Hunt"


# One time herbs are required to make 2 very good items.
"""class Mixologist(Toggle):
    Penny's concoctions are randomized!  Mix and match to find out what!
    internal_name = "mixologist"
    display_name = "Mixologist" """


class StartingCookies(Range):
    """How many cookies you start with."""
    internal_name = "starting_cookies"
    display_name = "Starting Cookies"
    range_start = 0
    range_end = 9999
    default = 0


class ExperienceMultiplier(Range):
    """How much experience is multiplied by.  While the game level generous, the other setting for reducing encounters can hurt the grind.
    Does not affect Wanderlust, so rates would be this times the 2x boost from it."""
    internal_name = "experience_multiplier"
    display_name = "Experience Multiplier"
    range_start = 50
    range_end = 500
    default = 100


class CookieMultiplier(Range):
    """How many cookies you get after combat.  Helps with money grinding for expensive items.
    Does not affect Scorpion's Wallet, so rates would be this times the 2x boost from it."""
    internal_name = "cookie_multiplier"
    display_name = "Cookie Multiplier"
    range_start = 50
    range_end = 500
    default = 100


class ReducedEncounters(Toggle):
    """Halves the rate of encounters.  Helps as some places are labyrinthine and will cause a lot of encounters to happen.
    Also can offset the 4x encounter rate from holding Scorpion's Wallet"""
    internal_name = "reduced_encounters"
    display_name = "Reduced Encounters"


class ShopPrices(Range):
    """Determine how much the shop items should cost as a percentage of their original price.  The final price is capped at 9999."""
    internal_name = "shop_prices"
    display_name = "Shop Prices"
    range_start = 0
    range_end = 200
    default = 100


class SquirrelStations(Toggle):
    """Randomizes the ability to use the squirrel station to go to certain locations.  Reaching destinations is a location."""
    internal_name = "squirrel_stations"
    display_name = "Squirrel Stations"


class Bestiary(Toggle):
    """Whether meeting an encounter for the first time is a location."""
    internal_name = "bestiary"
    display_name = "Bestiary"


class SkipFairySearch(Toggle):
    """Skips the event where the fairy at the top of Sage Mountain goes missing, so when you have the necessary secrest stones you
    can immediately get the certificate.  If Bestiary is on, this removes the Owlbear location as it is not encountered."""
    internal_name = "skip_fairy_search"
    display_name = "Skip Fairy Search"


@dataclass
class MadouOptions(PerGameCommonOptions):
    goal: Goal
    required_secret_stones: RequiredStones
    school_lunch: SchoolLunch
    starting_magic: StartingMagic
    souvenir_hunt: SouvenirHunt
    starting_cookies: StartingCookies
    # experience_multiplier: ExperienceMultiplier
    # cookie_multiplier: CookieMultiplier
    reduced_encounters: ReducedEncounters
    # shop_prices: ShopPrices
    squirrel_stations: SquirrelStations
    bestiary: Bestiary
    skip_fairy_search: SkipFairySearch
