"""
Data classes to store User data and hint information locally
"""
from __future__ import annotations
__all__ = ("UIHint", "UIPlayerData")
from dataclasses import dataclass
import re
from NetUtils import Hint, HintStatus, MWGGUIHintStatus
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
    my_item: bool
    _for_bk_mode: bool
    _for_goal: bool
    _from_shop: bool
    _hide: bool
    hint_status: HintStatus
    mwgg_hint_status: MWGGUIHintStatus

    def __init__(self, hint: Hint, my_item: bool, location_names: dict[int, str], item_names: dict[int, str], hint_status: Optional[HintStatus], mwgg_hint_status: Optional[MWGGUIHintStatus]):
        """
        Initialize a UIHint from a base Hint and status information.
        
        Args:
            hint: The base Hint object to wrap
            hint_status: Optional status indicating user-defined status
            mwgg_hint_status: Optional MWGG GUI specific hint information
        """
        self.location_id = hint['location']
        self.item = item_names.lookup_in_slot(hint['item'], hint['receiving_player'])
        self.location = location_names.lookup_in_slot(hint['location'], hint['finding_player'])
        self.entrance = location_names.lookup_in_slot(hint['entrance'], hint['finding_player']) if hint['entrance'] else ""
        self.found = hint['found']
        self.item_flags = hint['item_flags']  # Store the flags for status derivation
        self.assigned_classification = ""
        self.classification = self.get_classification(hint['item_flags'])
        self.my_item = my_item
        self._for_bk_mode = False    
        self._for_goal = False
        self._from_shop = False
        self._hide = False
        self.set_status(hint_status)
        self.set_status_from_mwgg(mwgg_hint_status)

    def set_status(self, hint_status: HintStatus):
        """
        Update the hint's status and classification based on status flags.
        
        Args:
            hint_status: The hint's user-defined status (found, unspecified, etc.)
            mwgg_status: MWGG GUI specific status information (shop, goal, bk_mode, etc.)
        """
        if hint_status == HintStatus.HINT_FOUND:
            self.found = True
        elif hint_status == HintStatus.HINT_UNSPECIFIED:
            # Derive hint status from item flags (inverse mapping)
            hint_status = self._derive_status_from_flags()
        elif hint_status == HintStatus.HINT_NO_PRIORITY:
            self.assigned_classification = self.get_classification(ItemClassification.filler)
        elif hint_status == HintStatus.HINT_AVOID:
            self.assigned_classification = self.get_classification(ItemClassification.trap)
        elif hint_status == HintStatus.HINT_PRIORITY:
            self.assigned_classification = self.get_classification(ItemClassification.progression)

        self.hint_status = hint_status

    def set_status_from_mwgg(self, mwgg_status: MWGGUIHintStatus):
        """
        Update the hint's status and classification based on MWGG GUI specific status information.
        """
        self.from_shop = mwgg_status & MWGGUIHintStatus.HINT_SHOP
        self.for_goal = mwgg_status & MWGGUIHintStatus.HINT_GOAL
        self.for_bk_mode = mwgg_status & MWGGUIHintStatus.HINT_BK_MODE

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

    @property
    def hide(self) -> bool:
        return self._hide
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _derive_status_from_flags(self) -> HintStatus:
        """
        Derive hint status from item classification flags.
        
        Returns:
            The appropriate HintStatus based on the item's flags
        """
        if self.item_flags & ItemClassification.progression:
            return HintStatus.HINT_PRIORITY
        elif self.item_flags & ItemClassification.trap:
            return HintStatus.HINT_AVOID
        else:  # useful or filler
            return HintStatus.HINT_NO_PRIORITY

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
    deafened: bool
    pronouns: str
    end_user: bool
    game_status: str
    game: str
    hints: dict[int, UIHint]

    # Mapping-like helpers for legacy code paths that treat this as a dict
    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        setattr(self, key, value)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    # Backwards compatibility: some UI code refers to "in_bk"
    # @property
    # def in_bk(self) -> bool:
    #     return self.bk_mode

    # @in_bk.setter
    # def in_bk(self, value: bool):
    #     self.bk_mode = value

