"""Behavioral invariants for ui_dataclasses.UIHint.

Each test pins a non-obvious behavior that previously lived only as an inline
comment in the source. UIHint instances are built with __new__ so the bit-flag
logic can be exercised without the dict lookups __init__ requires.
"""
import unittest

from BaseClasses import ItemClassification
from NetUtils import HintStatus, MWGGUIHintStatus
from ui_dataclasses import UIHint


class TestGetClassification(unittest.TestCase):
    def test_get_classification_progression_takes_precedence(self) -> None:
        flags = ItemClassification.progression | ItemClassification.useful
        self.assertEqual(UIHint.get_classification(flags), "Progression")

    def test_get_classification_progression_deprioritized(self) -> None:
        flags = ItemClassification.progression | ItemClassification.deprioritized
        self.assertEqual(
            UIHint.get_classification(flags), "Progression - Logically Relevant"
        )

    def test_get_classification_progression_skip_balancing(self) -> None:
        flags = ItemClassification.progression | ItemClassification.skip_balancing
        self.assertEqual(
            UIHint.get_classification(flags), "Progression - Requried for Goal"
        )

    def test_get_classification_deprioritized_beats_skip_balancing(self) -> None:
        # When both extra bits are set, the deprioritized branch wins.
        flags = (
            ItemClassification.progression
            | ItemClassification.deprioritized
            | ItemClassification.skip_balancing
        )
        self.assertEqual(
            UIHint.get_classification(flags), "Progression - Logically Relevant"
        )

    def test_get_classification_useful(self) -> None:
        self.assertEqual(
            UIHint.get_classification(ItemClassification.useful), "Useful"
        )

    def test_get_classification_trap_alone_is_trap(self) -> None:
        self.assertEqual(
            UIHint.get_classification(ItemClassification.trap), "Trap"
        )

    def test_get_classification_useful_trap_is_useful_not_trap(self) -> None:
        # useful is checked before trap in the elif chain, so a trap that is
        # also flagged useful resolves to "Useful", not "Trap".
        flags = ItemClassification.useful | ItemClassification.trap
        self.assertEqual(UIHint.get_classification(flags), "Useful")

    def test_get_classification_filler(self) -> None:
        self.assertEqual(
            UIHint.get_classification(ItemClassification.filler), "Filler"
        )


class TestDeriveStatusFromFlags(unittest.TestCase):
    def _hint_with_flags(self, flags: int) -> UIHint:
        hint = UIHint.__new__(UIHint)
        hint.item_flags = flags
        return hint

    def test_derive_status_useful_or_filler_is_no_priority(self) -> None:
        self.assertEqual(
            self._hint_with_flags(ItemClassification.useful)._derive_status_from_flags(),
            HintStatus.HINT_NO_PRIORITY,
        )
        self.assertEqual(
            self._hint_with_flags(ItemClassification.filler)._derive_status_from_flags(),
            HintStatus.HINT_NO_PRIORITY,
        )

    def test_derive_status_progression_is_priority(self) -> None:
        self.assertEqual(
            self._hint_with_flags(
                ItemClassification.progression
            )._derive_status_from_flags(),
            HintStatus.HINT_PRIORITY,
        )

    def test_derive_status_trap_is_avoid(self) -> None:
        self.assertEqual(
            self._hint_with_flags(ItemClassification.trap)._derive_status_from_flags(),
            HintStatus.HINT_AVOID,
        )


class TestToggleMwggFlag(unittest.TestCase):
    def _hint_with_status(self, status: MWGGUIHintStatus) -> UIHint:
        hint = UIHint.__new__(UIHint)
        hint.mwgg_hint_status = status
        return hint

    def test_toggle_mwgg_flag_set_preserves_existing(self) -> None:
        hint = self._hint_with_status(
            MWGGUIHintStatus.HINT_SHOP | MWGGUIHintStatus.HINT_GOAL
        )
        hint.toggle_mwgg_flag(MWGGUIHintStatus.HINT_BK_MODE, True)
        self.assertEqual(
            hint.mwgg_hint_status,
            MWGGUIHintStatus.HINT_SHOP
            | MWGGUIHintStatus.HINT_GOAL
            | MWGGUIHintStatus.HINT_BK_MODE,
        )
        self.assertTrue(hint.from_shop)
        self.assertTrue(hint.for_goal)
        self.assertTrue(hint.for_bk_mode)

    def test_toggle_mwgg_flag_clear_keeps_others(self) -> None:
        hint = self._hint_with_status(
            MWGGUIHintStatus.HINT_SHOP
            | MWGGUIHintStatus.HINT_GOAL
            | MWGGUIHintStatus.HINT_BK_MODE
        )
        hint.toggle_mwgg_flag(MWGGUIHintStatus.HINT_GOAL, False)
        self.assertEqual(
            hint.mwgg_hint_status,
            MWGGUIHintStatus.HINT_SHOP | MWGGUIHintStatus.HINT_BK_MODE,
        )
        self.assertTrue(hint.from_shop)
        self.assertFalse(hint.for_goal)
        self.assertTrue(hint.for_bk_mode)


if __name__ == "__main__":
    unittest.main()
