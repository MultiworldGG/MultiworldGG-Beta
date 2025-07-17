from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, StartInventoryPool, Toggle


class HardMode(Toggle):
    """Only for the most masochistically inclined... Requires button activation!"""

    display_name = "Hard Mode"


class ButtonColor(Choice):
    """Customize **The Button**! Now available in 12 unique colors."""

    display_name = "Button Color"
    option_red = 0
    option_orange = 1
    option_yellow = 2
    option_green = 3
    option_cyan = 4
    option_blue = 5
    option_magenta = 6
    option_purple = 7
    option_pink = 8
    option_brown = 9
    option_white = 10
    option_black = 11


class ForceButtonProgression(DefaultOnToggle):
    """Forces **The Button** to have a progression item. Overrides Excluded Locations."""

    display_name = "Force Button Progression"


@dataclass
class CliqueOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    color: ButtonColor
    hard_mode: HardMode
    force_progression: ForceButtonProgression

    # DeathLink is always on. Always.
    # death_link: DeathLink
