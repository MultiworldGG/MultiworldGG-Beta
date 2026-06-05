"""Behavioral tests pinning non-obvious facts in Options.py that were previously only stated in inline comments."""
import unittest
from dataclasses import dataclass

from Options import (
    Accessibility,
    Choice,
    CommonOptions,
    OptionSet,
    ProgressionBalancing,
    Toggle,
    triangular,
)


class TestTriangular(unittest.TestCase):
    def test_triangular_result_clamped_to_end(self) -> None:
        """random.triangular is inclusive of its upper bound, so triangular() must never exceed `end`."""
        lower, end = 3, 5
        # tri=1.0 biases sampling toward the upper bound, the case that can return exactly `end`.
        results = {triangular(lower, end, 1.0) for _ in range(50000)}
        for result in results:
            self.assertIsInstance(result, int)
            self.assertGreaterEqual(result, lower)
            self.assertLessEqual(result, end)
        # The clamped upper bound must actually be reachable, otherwise the test wouldn't exercise the clamp.
        self.assertIn(end, results)

    def test_triangular_degenerate_range_returns_single_value(self) -> None:
        """When lower == end the only valid integer result is that value."""
        for _ in range(1000):
            self.assertEqual(triangular(7, 7, 0.5), 7)


class TestToggleCoercion(unittest.TestCase):
    def test_toggle_coerces_arbitrary_value_to_bool_int(self) -> None:
        """Toggle.__init__ stores int(bool(value)): truthy -> 1, falsy -> 0, regardless of the raw value."""
        self.assertEqual(Toggle(0).value, 0)
        self.assertEqual(Toggle(1).value, 1)
        self.assertEqual(Toggle(5).value, 1)
        self.assertEqual(Toggle(-3).value, 1)
        self.assertEqual(Toggle("anything").value, 1)
        self.assertEqual(Toggle("").value, 0)
        self.assertEqual(Toggle([]).value, 0)
        self.assertEqual(Toggle(["x"]).value, 1)

    def test_toggle_get_option_name_no_yes(self) -> None:
        """Toggle.get_option_name maps 0 -> 'No' and 1 -> 'Yes'."""
        self.assertEqual(Toggle.get_option_name(0), "No")
        self.assertEqual(Toggle.get_option_name(1), "Yes")


class TestAssembleOptionsAliases(unittest.TestCase):
    def test_assemble_options_aliases_off_on_to_false_true(self) -> None:
        """An option named 'off'/'on' gets an auto-alias 'false'/'true' pointing at the same id."""
        class OffOnChoice(Choice):
            option_off = 0
            option_on = 1
            default = 0

        self.assertIn("false", OffOnChoice.options)
        self.assertIn("true", OffOnChoice.options)
        self.assertEqual(OffOnChoice.options["false"], OffOnChoice.options["off"])
        self.assertEqual(OffOnChoice.options["true"], OffOnChoice.options["on"])

    def test_assemble_options_no_false_true_without_off_on(self) -> None:
        """The alias is only added when the corresponding off/on member exists."""
        class PlainChoice(Choice):
            option_alpha = 0
            option_beta = 1
            default = 0

        self.assertNotIn("false", PlainChoice.options)
        self.assertNotIn("true", PlainChoice.options)


class TestOptionSetRandomDeferral(unittest.TestCase):
    def test_option_set_from_text_defers_random_token(self) -> None:
        """A lone 'random*' token with valid_keys set is stored as random_str with an empty value, not as a key."""
        class KeyedSet(OptionSet):
            valid_keys = frozenset({"A", "B", "C"})

        option = KeyedSet.from_text("random")
        self.assertEqual(set(option.value), set())
        self.assertEqual(option.random_str, "random")

        ranged = KeyedSet.from_text("random-range-1-2")
        self.assertEqual(set(ranged.value), set())
        self.assertEqual(ranged.random_str, "random-range-1-2")

    def test_option_set_from_text_keeps_random_as_key_without_valid_keys(self) -> None:
        """Without valid_keys/verify_*_name there is nothing to sample from, so 'random' stays a literal key."""
        class UnkeyedSet(OptionSet):
            pass

        option = UnkeyedSet.from_text("random")
        self.assertIn("random", option.value)
        self.assertIsNone(option.random_str)

    def test_option_set_from_text_multiple_tokens_not_deferred(self) -> None:
        """'random' is only deferred when it is the single token; in a list it is treated literally."""
        class KeyedSet(OptionSet):
            valid_keys = frozenset({"A", "B", "C"})

        option = KeyedSet.from_text("random, A")
        self.assertEqual(set(option.value), {"random", "A"})
        self.assertIsNone(option.random_str)


class _MySet(OptionSet):
    valid_keys = frozenset({"A", "B", "C"})


class _MyToggle(Toggle):
    default = 0


@dataclass
class _AsDictOptions(CommonOptions):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility
    some_set_option: _MySet
    a_toggle_option: _MyToggle


class TestAsDict(unittest.TestCase):
    def _make(self) -> _AsDictOptions:
        return _AsDictOptions(
            progression_balancing=ProgressionBalancing.from_any(ProgressionBalancing.default),
            accessibility=Accessibility.from_any(Accessibility.default),
            some_set_option=_MySet.from_any(["C", "A", "B"]),
            a_toggle_option=_MyToggle.from_any(1),
        )

    def test_as_dict_sorts_sets_and_casing_and_toggle_bools(self) -> None:
        """as_dict returns set values as a sorted list, applies key casing, and (opt-in) returns toggles as bool."""
        opts = self._make()

        result = opts.as_dict("some_set_option", "a_toggle_option", toggles_as_bools=True)
        self.assertEqual(result["some_set_option"], ["A", "B", "C"])  # set -> sorted list
        self.assertIsInstance(result["a_toggle_option"], bool)
        self.assertIs(result["a_toggle_option"], True)

    def test_as_dict_toggle_stays_int_without_flag(self) -> None:
        """toggles_as_bools defaults to False, leaving toggle values as their underlying int."""
        opts = self._make()
        result = opts.as_dict("a_toggle_option")
        self.assertEqual(result["a_toggle_option"], 1)
        self.assertNotIsInstance(result["a_toggle_option"], bool)

    def test_as_dict_casing_variants(self) -> None:
        """The casing argument controls the returned key style."""
        opts = self._make()
        self.assertIn("some_set_option", opts.as_dict("some_set_option", casing="snake"))
        self.assertIn("someSetOption", opts.as_dict("some_set_option", casing="camel"))
        self.assertIn("SomeSetOption", opts.as_dict("some_set_option", casing="pascal"))
        self.assertIn("some-set-option", opts.as_dict("some_set_option", casing="kebab"))


if __name__ == "__main__":
    unittest.main()
