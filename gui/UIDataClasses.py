from dataclasses import dataclass
from NetUtils import Hint, HintStatus
from BaseClasses import ItemClassification


@dataclass
class UIHint:
    item: str
    location: str
    entrance: str
    found: str
    classification: str
    for_bk_mode: bool
    for_goal: bool
    from_shop: bool
    hint_status: HintStatus

    def __init__(self, hint: Hint):
        self.item = hint.item
        self.location = hint.location
        self.entrance = hint.entrance
        self.found = hint.found
        self.classification = self.get_classification(hint.item_flags)
        self.for_bk_mode = hint.for_bk_mode
        self.for_goal = hint.for_goal
        self.from_shop = hint.from_shop
        self.hint_status = hint.status

    def set_status(self, status: HintStatus):
        self.for_bk_mode = False
        self.for_goal = False
        self.from_shop = False
        if status == HintStatus.HINT_FOUND:
            self.found = True
        elif status == HintStatus.HINT_UNSPECIFIED:
            pass
        elif status == HintStatus.HINT_NO_PRIORITY:
            self.for_goal = True
        elif status == HintStatus.HINT_AVOID:
            self.for_goal = True
        elif status == HintStatus.HINT_PRIORITY:
            self.for_bk_mode = True
        self.hint_status = status

    def get_classification(self, flags: int) -> str:
        if flags & ItemClassification.progression_skip_balancing:
            return "Goal"
        elif flags & ItemClassification.progression:
            return "Progression"
        elif flags & ItemClassification.progression_deprioritized:
            return "Logically Relevant"
        elif flags & ItemClassification.progression_deprioritized_skip_balancing:
            return "Logically Relevant"
        elif flags & ItemClassification.skip_balancing:
            return "Currency"
        elif flags & ItemClassification.deprioritized:
            return "Logically Relevant"
        elif flags & ItemClassification.useful:
            return "Useful"
        elif flags & ItemClassification.trap:
            return "Trap"
        else:
            return "Filler"


    filler = 0b00000
    """ aka trash, as in filler items like ammo, currency etc """

    progression = 0b00001
    """ Item that is logically relevant.
    Protects this item from being placed on excluded or unreachable locations. """

    useful = 0b00010
    """ Item that is especially useful.
    Protects this item from being placed on excluded or unreachable locations.
    When combined with another flag like "progression", it means "an especially useful progression item". """

    trap = 0b00100
    """ Item that is detrimental in some way. """

    skip_balancing = 0b01000
    """ should technically never occur on its own
    Item that is logically relevant, but progression balancing should not touch.

    Possible reasons for why an item should not be pulled ahead by progression balancing:
    1. This item is quite insignificant, so pulling it earlier doesn't help (currency/etc.)
    2. It is important for the player experience that this item is evenly distributed in the seed (e.g. goal items) """

    deprioritized = 0b10000
    """ Should technically never occur on its own.
    Will not be considered for priority locations,
    unless Priority Locations Fill runs out of regular progression items before filling all priority locations. 
    
    Should be used for items that would feel bad for the player to find on a priority location.
    Usually, these are items that are plentiful or insignificant. """

    progression_deprioritized_skip_balancing = 0b11001
    """ Since a common case of both skip_balancing and deprioritized is "insignificant progression", 
    these items often want both flags. """

    progression_skip_balancing = 0b01001  # only progression gets balanced
    progression_deprioritized = 0b10001 

@dataclass
class UIPlayerData:
    slot_name: str
    avatar: str
    bk_mode: bool
    in_call: bool
    pronouns: str
    end_user: bool
    game_status: str
    game: str
    hints: list[UIHint]

