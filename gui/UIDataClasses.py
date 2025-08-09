from dataclasses import dataclass
from NetUtils import Hint, HintStatus, MWGGUIHintStatus, JSONtoTextParser
from BaseClasses import ItemClassification
from typing import Optional

@dataclass
class UIHint:
    """
    A UI-friendly wrapper that provides formatted text
    and additional metadata for display in the MultiWorld GUI.
    
    This class adds properties that are specifically
    formatted for UI display, including parsed item names, location names,
    and classification information.
    """
    location_id: int
    item: str
    location: str
    entrance: str
    found: str
    classification: str
    assigned_classification: str
    _for_bk_mode: bool
    _for_goal: bool
    _from_shop: bool
    hint_status: HintStatus
    mwgg_hint_status: MWGGUIHintStatus

    def __init__(self, hint: Hint, hint_status: Optional[HintStatus], mwgg_hint_status: Optional[MWGGUIHintStatus]):
        """
        Initialize a UIHint from a base Hint and status information.
        
        Args:
            hint: The base Hint object to wrap
            hint_status: Optional status indicating user-defined status
            mwgg_hint_status: Optional MWGG GUI specific hint information
        """
        parser = JSONtoTextParser()
        self.location_id = hint.location
        self.item = parser.handle_node({"type": "item_id", "text": hint.item, "flags": hint.item_flags, "player": hint.receiving_player})
        self.location = parser.handle_node({"type": "location_id", "text": hint.location, "player": hint.finding_player})
        self.entrance = parser.handle_node({"type": "color" if hint.entrance else "text", "color": 'entrancecolor', "text": hint.entrance if hint.entrance else "Vanilla"})
        self.found = hint.found
        self.classification = self.get_classification(hint.item_flags)
        self.for_bk_mode = mwgg_hint_status.for_bk_mode
        self.for_goal = mwgg_hint_status.for_goal
        self.from_shop = mwgg_hint_status.from_shop
        self.set_status(hint_status, mwgg_hint_status)

    def set_status(self, hint_status: Optional[HintStatus], mwgg_status: Optional[MWGGUIHintStatus]):
        """
        Update the hint's status and classification based on status flags.
        
        Args:
            hint_status: The hint's user-defined status (found, unspecified, etc.)
            mwgg_status: MWGG GUI specific status information (shop, goal, bk_mode, etc.)
        """
        if hint_status == HintStatus.HINT_FOUND:
            self.found = True
        elif hint_status == HintStatus.HINT_UNSPECIFIED:
            pass
        elif hint_status == HintStatus.HINT_NO_PRIORITY:
            self.assigned_classification = self.get_classification(ItemClassification.filler)
        elif hint_status == HintStatus.HINT_AVOID:
            self.assigned_classification = self.get_classification(ItemClassification.trap)
        elif hint_status == HintStatus.HINT_PRIORITY:
            self.assigned_classification = self.get_classification(ItemClassification.progression)

        if mwgg_status == MWGGUIHintStatus.HINT_SHOP:
            self.from_shop = True
        elif mwgg_status == MWGGUIHintStatus.HINT_GOAL:
            self.for_goal = True
        elif mwgg_status == MWGGUIHintStatus.HINT_BK_MODE:
            self.for_bk_mode = True
        elif mwgg_status == MWGGUIHintStatus.HINT_UNSPECIFIED:
            pass
        self.hint_status = hint_status
        self.mwgg_hint_status = mwgg_status

    @property
    def from_shop(self) -> bool:
        return self._from_shop
    @from_shop.setter
    def from_shop(self, value: bool):
        self._from_shop = value

    @property
    def for_bk_mode(self) -> bool:
        return self._for_bk_mode
    @for_bk_mode.setter
    def for_bk_mode(self, value: bool):
        self._for_bk_mode = value
    
    @property
    def for_goal(self) -> bool:
        return self._for_goal
    @for_goal.setter
    def for_goal(self, value: bool):
        self._for_goal = value

    @staticmethod
    def get_classification(flags: int) -> str:
        """
        Convert item classification flags to a human-readable string.
        
        Args:
            flags: Bit flags representing the item's classification
            
        Returns:
            A string describing the item's classification (Progression, Useful, Trap, or Filler)
        """
        if flags & ItemClassification.progression:  # Check for progression flag first!
            # "useful progression" gets marked progression
            if flags & ItemClassification.deprioritized:  # deprioritized, but still progression (skulls etc)
                return "Progression - Logically Relevant"
            elif flags & ItemClassification.skip_balancing:  # skip_balancing bit set on a priority item: macguffin
                return "Progression - Requried for Goal"
            else:
                return "Progression"
        elif flags & ItemClassification.useful:  # useful
            return "Useful"
        elif flags & ItemClassification.trap:  # "useful trap" gets marked trap
            return "Trap"
        else:
            return "Filler"

@dataclass
class UIPlayerData:
    """
    Container for player data formatted for UI display in the MultiWorld GUI.
    
    This class holds all the information needed to display a player's status,
    including their slot information, game status, and associated hints.
    """
    slot_id: int
    slot_name: str
    avatar: str
    bk_mode: bool
    in_call: bool
    pronouns: str
    end_user: bool
    game_status: str
    game: str
    hints: dict[int, UIHint]

