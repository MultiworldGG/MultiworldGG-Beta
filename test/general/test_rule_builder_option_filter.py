"""Behavioral pins for ``rule_builder.options.OptionFilter`` operand ordering.

These tests document the non-obvious fact that the ``"in"`` operator listed in
``REVERSE_OPERATORS`` swaps the operands inside ``OptionFilter.check`` so that the
option value is tested for membership in the filter value (``option in value``),
rather than the filter value being tested against the option (``value in option``).
"""

import unittest
from dataclasses import dataclass
from typing import Any, ClassVar

from typing_extensions import override

from BaseClasses import Item, Location
from Options import Choice, PerGameCommonOptions
from rule_builder.options import OPERATORS, REVERSE_OPERATORS, OptionFilter
from test.general import setup_solo_multiworld
from worlds.AutoWorld import AutoWorldRegister, World

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

    def test_in_operator_passes_when_option_value_is_member_of_filter_value(self) -> None:
        world = self._world_with_choice(ChoiceOption.option_second)  # value == 1
        self.assertTrue(OptionFilter(ChoiceOption, (0, 1), "in").check(world.options))

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


if __name__ == "__main__":
    unittest.main()
