"""Beta rule_builder tests (resolved-rule invariants, OptionFilter operand order); add new rule_builder tests here."""

import unittest
from dataclasses import dataclass
from typing import Any, ClassVar

from typing_extensions import override

from BaseClasses import CollectionState, Item, Location, MultiWorld
from Options import Choice, PerGameCommonOptions
from rule_builder.options import OPERATORS, REVERSE_OPERATORS, OptionFilter
from rule_builder.rules import (
    And,
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
from worlds.AutoWorld import AutoWorldRegister, World


# --------------------------------------------------------------------------- #
# Behavioral invariants for rule_builder.rules: each test pins a
# non-obvious behavior of a resolved rule so the source no longer needs an
# inline prose comment to describe it.
# --------------------------------------------------------------------------- #

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



# --------------------------------------------------------------------------- #
# rule_builder.options.OptionFilter operand ordering: the "in" operator
# listed in REVERSE_OPERATORS swaps the operands inside OptionFilter.check
# so the option value is tested for membership in the filter value
# (option in value), rather than the filter value being tested against the
# option.
# --------------------------------------------------------------------------- #

GAME_NAME = "Rule Builder OptionFilter Test Game"


class ChoiceOption(Choice):
    auto_display_name = True
    option_first = 0
    option_second = 1
    option_third = 2
    default = 0


@dataclass
class _Options(PerGameCommonOptions):
    choice_option: ChoiceOption


class _FilterItem(Item):
    game = GAME_NAME


class _FilterLocation(Location):
    game = GAME_NAME


class OptionFilterReverseOperatorTest(unittest.TestCase):
    world_cls: ClassVar[type[World]]

    @override
    def setUp(self) -> None:
        self._old_world_types = AutoWorldRegister.world_types.copy()

        class _FilterWorld(World):
            game = GAME_NAME
            item_name_to_id: ClassVar = {"Item 1": 1}
            location_name_to_id: ClassVar = {"Location 1": 1}
            hidden = True
            options_dataclass = _Options
            options: _Options  # pyright: ignore[reportIncompatibleVariableOverride]
            origin_region_name = "Region 1"

            @override
            def create_item(self, name: str) -> _FilterItem:
                from BaseClasses import ItemClassification

                return _FilterItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

        self.world_cls = _FilterWorld

    @override
    def tearDown(self) -> None:
        AutoWorldRegister.world_types = self._old_world_types

    def _world_with_choice(self, world_value: int) -> World:
        multiworld = setup_solo_multiworld(self.world_cls, steps=("generate_early",), seed=0)
        world = multiworld.worlds[1]
        world.options.choice_option = ChoiceOption.from_any(world_value)
        return world

    def test_in_operator_is_registered_as_reversed(self) -> None:
        # Guards the literal mapping the behavior depends on.
        self.assertIn("in", REVERSE_OPERATORS)
        self.assertNotIn("contains", REVERSE_OPERATORS)
        self.assertIs(OPERATORS["in"], OPERATORS["contains"])

    def test_in_operator_fails_when_option_value_is_not_member_of_filter_value(self) -> None:
        world = self._world_with_choice(ChoiceOption.option_third)  # value == 2
        self.assertFalse(OptionFilter(ChoiceOption, (0, 1), "in").check(world.options))

    def test_in_operator_tests_option_against_filter_not_filter_against_option(self) -> None:
        # Reversed order means the scalar option is the needle and the filter is the
        # haystack. The non-reversed order (filter-in-option) would instead attempt
        # ``container in <Choice>`` which raises, so a passing assertion here proves
        # the operands were swapped.
        world = self._world_with_choice(ChoiceOption.option_first)  # value == 0
        option_filter = OptionFilter(ChoiceOption, (0, 1), "in")
        self.assertTrue(option_filter.check(world.options))
        opt = world.options.choice_option
        with self.assertRaises(TypeError):
            _ = (0, 1) in opt  # the non-reversed direction is not even valid
