"""Behavioral invariant tests for rule_builder.rules.

Each test here pins a non-obvious behavior of a resolved rule so the source no longer
needs an inline prose comment to describe it. Names are chosen so the asserted fact is
self-documenting.
"""

from typing import Any

from BaseClasses import CollectionState, MultiWorld
from rule_builder.rules import (
    And,
    AtLeast,
    False_,
    Has,
    HasAll,
    HasAllCounts,
    HasAny,
    HasAnyCount,
    HasFromList,
    HasFromListUnique,
    HasGroup,
    Or,
    Rule,
    True_,
)
from test.general import setup_solo_multiworld
from test.general.test_rule_builder import RuleBuilderTestCase
from worlds.AutoWorld import World


class RuleInvariantTestCase(RuleBuilderTestCase):
    multiworld: MultiWorld  # pyright: ignore[reportUninitializedInstanceVariable]
    world: World  # pyright: ignore[reportUninitializedInstanceVariable]
    state: CollectionState  # pyright: ignore[reportUninitializedInstanceVariable]
    player: int = 1

    def setUp(self) -> None:
        super().setUp()
        self.multiworld = setup_solo_multiworld(self.world_cls, seed=0)
        self.world = self.multiworld.worlds[1]
        self.state = self.multiworld.state

    def _resolve(self, rule: Rule[Any]) -> Rule.Resolved:
        resolved = rule.resolve(self.world)
        self.world.register_rule_dependencies(resolved)
        return resolved

    def _give(self, item_name: str, copies: int = 1) -> None:
        for _ in range(copies):
            self.state.collect(self.world.create_item(item_name))


class TestHasEvaluation(RuleInvariantTestCase):
    def test_has_evaluate_at_count_boundary(self) -> None:
        resolved = self._resolve(Has("Item 1", count=2))
        self.assertFalse(resolved(self.state))
        self._give("Item 1")  # one copy, below the required count
        self.assertFalse(resolved(self.state))
        self._give("Item 1")  # exactly the required count
        self.assertTrue(resolved(self.state))


class TestEmptyResolutions(RuleInvariantTestCase):
    def test_has_all_empty_resolves_true(self) -> None:
        self.assertEqual(HasAll().resolve(self.world), True_.Resolved(player=self.player))

    def test_has_any_empty_resolves_false(self) -> None:
        self.assertEqual(HasAny().resolve(self.world), False_.Resolved(player=self.player))

    def test_has_all_counts_empty_resolves_true(self) -> None:
        self.assertEqual(HasAllCounts({}).resolve(self.world), True_.Resolved(player=self.player))

    def test_has_any_count_empty_resolves_false(self) -> None:
        self.assertEqual(HasAnyCount({}).resolve(self.world), False_.Resolved(player=self.player))

    def test_has_from_list_empty_resolves_false(self) -> None:
        self.assertEqual(HasFromList(count=2).resolve(self.world), False_.Resolved(player=self.player))

    def test_has_from_list_unique_insufficient_resolves_false(self) -> None:
        # zero item_names cannot satisfy any positive count
        self.assertEqual(HasFromListUnique(count=1).resolve(self.world), False_.Resolved(player=self.player))
        # fewer unique item_names than count can never be satisfied
        self.assertEqual(
            HasFromListUnique("Item 1", "Item 2", count=3).resolve(self.world),
            False_.Resolved(player=self.player),
        )


class TestCopyCounting(RuleInvariantTestCase):
    def test_has_from_list_counts_total_copies(self) -> None:
        # two distinct names keep it a HasFromList.Resolved; duplicates of a single name
        # accumulate toward the running total.
        resolved = self._resolve(HasFromList("Item 1", "Item 2", count=3))
        self.assertFalse(resolved(self.state))
        self._give("Item 1", 2)
        self.assertFalse(resolved(self.state))
        self._give("Item 1")  # third copy of the same item reaches the count
        self.assertTrue(resolved(self.state))

    def test_has_group_counts_total_copies(self) -> None:
        # Group 1 = {Item 1, Item 2, Item 3}; stacking copies of a single group item
        # counts toward the total.
        resolved = self._resolve(HasGroup("Group 1", count=3))
        self.assertFalse(resolved(self.state))
        self._give("Item 1", 2)
        self.assertFalse(resolved(self.state))
        self._give("Item 1")
        self.assertTrue(resolved(self.state))


class TestAndSimplification(RuleInvariantTestCase):
    def test_and_dedupes_true_children(self) -> None:
        # multiple always-true children collapse to a single one; an And of only
        # True_ children is vacuously True_.
        self.assertEqual(
            And(True_(), True_(), True_()).resolve(self.world),
            True_.Resolved(player=self.player),
        )


class TestAtLeastReduction(RuleInvariantTestCase):
    def test_at_least_one_reduces_to_or(self) -> None:
        # Rule()/Rule() stay opaque so AtLeast cannot fold them into a single Has.
        resolved = AtLeast(1, Rule(), Rule()).resolve(self.world)
        self.assertEqual(
            resolved,
            Or.Resolved((Rule.Resolved(player=self.player), Rule.Resolved(player=self.player)), player=self.player),
        )

    def test_at_least_all_reduces_to_and(self) -> None:
        resolved = AtLeast(2, Rule(), Rule()).resolve(self.world)
        self.assertEqual(
            resolved,
            And.Resolved((Rule.Resolved(player=self.player), Rule.Resolved(player=self.player)), player=self.player),
        )
