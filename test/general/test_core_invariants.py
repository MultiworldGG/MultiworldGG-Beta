"""Core behavioral invariants (Utils, BaseUtils, Generate, Options, ui_dataclasses, APContainer); add new core-invariant tests here."""

import builtins
import copy
import io
import os
import pickle
import unittest
from collections import Counter
from dataclasses import dataclass
from tempfile import TemporaryDirectory

import Generate
from APContainer import APContainer, APPlayerContainer, container_version, parse_client_function
from BaseClasses import ItemClassification
from BaseUtils import Version, tuplize_version
from NetUtils import HintStatus, MWGGUIHintStatus
from Options import (
    Accessibility,
    Choice,
    CommonOptions,
    OptionSet,
    ProgressionBalancing,
    Toggle,
    triangular,
)
from ui_dataclasses import UIHint
from Utils import (
    _expand_game_choices,
    get_fuzzy_results,
    is_iterable_except_str,
    players_path,
    read_snes_rom,
    restricted_dumps,
    restricted_loads,
)


# --------------------------------------------------------------------------- #
# Utils.py helper invariants: each test pins a non-obvious behavior that
# previously lived only as an inline comment in the source.
# --------------------------------------------------------------------------- #

class TestExpandGameChoices(unittest.TestCase):
    def test_expand_game_choices_keeps_unparseable_weight_drops_nonpositive_and_dedups(self) -> None:
        # Weighted mapping: positive weight kept, non-positive dropped,
        # unparseable weight kept (cannot be int()-parsed -> selectable).
        result = _expand_game_choices([
            {"Keep": 1, "Drop": 0, "AlsoDrop": -5, "Unparseable": "notanint"},
        ])
        self.assertEqual(result, ["Keep", "Unparseable"])

    def test_expand_game_choices_preserves_first_seen_order_and_dedups(self) -> None:
        result = _expand_game_choices(["A", "B", "A", ["C", "B"], "D"])
        self.assertEqual(result, ["A", "B", "C", "D"])


class TestReadSnesRom(unittest.TestCase):
    def test_read_snes_rom_strips_512_byte_header_only_on_odd_bank_offset(self) -> None:
        # len % 0x400 == 0x200 -> the 0x200-byte SMC header is stripped.
        with_header = bytes(0x200) + bytes(b"\xAB") * 0x400
        self.assertEqual(len(with_header) % 0x400, 0x200)
        stripped = read_snes_rom(io.BytesIO(with_header))
        self.assertEqual(stripped, bytearray(b"\xAB" * 0x400))

    def test_read_snes_rom_keeps_buffer_when_no_header_offset(self) -> None:
        # len % 0x400 != 0x200 -> buffer returned unchanged.
        no_header = bytes(b"\xCD") * 0x400
        self.assertEqual(read_snes_rom(io.BytesIO(no_header)), bytearray(no_header))

    def test_read_snes_rom_keeps_header_when_strip_header_false(self) -> None:
        with_header = bytes(0x200) + bytes(b"\xAB") * 0x400
        self.assertEqual(
            read_snes_rom(io.BytesIO(with_header), strip_header=False),
            bytearray(with_header),
        )


class TestRestrictedUnpickler(unittest.TestCase):
    def test_restricted_loads_forbids_unlisted_global(self) -> None:
        # A pickle referencing builtins.eval (not on the allowlist) must be rejected.
        payload = pickle.dumps(eval)
        with self.assertRaises(pickle.UnpicklingError):
            restricted_loads(payload)

    def test_restricted_dumps_reraises_forbidden_object_as_pickling_error(self) -> None:
        with self.assertRaises(pickle.PicklingError):
            restricted_dumps(eval)

    def test_restricted_loads_allows_listed_builtin(self) -> None:
        # set is on the safe_builtins allowlist and must round-trip.
        self.assertEqual(restricted_loads(restricted_dumps({1, 2, 3})), {1, 2, 3})


class TestIsIterableExceptStr(unittest.TestCase):
    def test_is_iterable_except_str_excludes_strings(self) -> None:
        self.assertFalse(is_iterable_except_str("abc"))

    def test_is_iterable_except_str_accepts_other_iterables(self) -> None:
        self.assertTrue(is_iterable_except_str([1, 2]))
        self.assertTrue(is_iterable_except_str((1, 2)))
        self.assertTrue(is_iterable_except_str({"a": 1}))
        self.assertTrue(is_iterable_except_str(x for x in range(3)))

    def test_is_iterable_except_str_rejects_non_iterable(self) -> None:
        self.assertFalse(is_iterable_except_str(5))


class TestGetFuzzyResults(unittest.TestCase):
    def test_get_fuzzy_results_sorts_descending_and_exact_match_is_101(self) -> None:
        words = ["banana", "apple", "applf"]
        results = get_fuzzy_results("apple", words)
        # Descending by ratio.
        percents = [pct for _, pct in results]
        self.assertEqual(percents, sorted(percents, reverse=True))
        # Exact match scores 1.01*100 -> 101 and ranks first.
        self.assertEqual(results[0], ("apple", 101))

    def test_get_fuzzy_results_truncates_to_limit(self) -> None:
        words = ["apple", "applf", "applg", "applh"]
        self.assertEqual(len(get_fuzzy_results("apple", words, limit=2)), 2)


class TestPlayersPath(unittest.TestCase):
    def test_players_path_resolves_under_settings_value_and_creates_dir(self) -> None:
        from settings import get_settings
        settings = get_settings()
        with TemporaryDirectory(prefix="AP_players_") as tempdir:
            target = os.path.join(tempdir, "Players")
            original = settings.generator.player_files_path
            # settings.Group's setattr needs the upcast to the APPathLib subclass
            settings.generator.player_files_path = settings.generator.PlayerFilesPath(target)
            settings._filename = None  # don't write to disk
            try:
                self.assertFalse(os.path.isdir(target))
                result = players_path("Player1.yaml")
                self.assertEqual(result, os.path.join(target, "Player1.yaml"))
                self.assertTrue(os.path.isdir(target), "players_path must create the base dir")
                self.assertEqual(players_path(), target)
            finally:
                settings.generator.player_files_path = original


# --------------------------------------------------------------------------- #
# BaseUtils version parsing.
# --------------------------------------------------------------------------- #

class TestTuplizeVersionPrerelease(unittest.TestCase):
    def test_tuplize_version_strips_prerelease_suffix_to_release_tuple(self) -> None:
        self.assertEqual(tuplize_version("0.8.0b7"), Version(0, 8, 0))
        self.assertNotEqual(tuplize_version("0.8.0b7"), Version(0, 0, 0))

    def test_tuplize_version_fallback_strips_prerelease_when_packaging_missing(self) -> None:
        real_import = builtins.__import__

        def blocking_import(name, *args, **kwargs):
            if name == "packaging" or name.startswith("packaging."):
                raise ImportError("packaging blocked for fallback test")
            return real_import(name, *args, **kwargs)

        builtins.__import__ = blocking_import
        try:
            self.assertEqual(tuplize_version("0.8.0b7"), Version(0, 8, 0))
            self.assertEqual(tuplize_version("1.2b3"), Version(1, 2, 0))
            self.assertEqual(tuplize_version("5rc1"), Version(5, 0, 0))
        finally:
            builtins.__import__ = real_import


# --------------------------------------------------------------------------- #
# Generate.py core helpers (handle_name, update_weights, mystery_argparse).
# --------------------------------------------------------------------------- #

class TestHandleName(unittest.TestCase):
    def test_handle_name_truncates_to_16_chars_and_strips_twice(self):
        # After the leading/trailing strip the slice can land mid-whitespace,
        # leaving boundary whitespace that the second strip must remove.
        counter: Counter[str] = Counter()
        result = Generate.handle_name("   abcdefghijklmno  trailing", 1, counter)
        # post-strip: "abcdefghijklmno  trailing"; [:16] -> "abcdefghijklmno "
        # second strip removes the boundary space the slice exposed.
        self.assertEqual(result, "abcdefghijklmno")

    def test_handle_name_never_exceeds_16_chars(self):
        counter: Counter[str] = Counter()
        result = Generate.handle_name("0123456789abcdefGHIJ", 1, counter)
        self.assertLessEqual(len(result), 16)
        self.assertEqual(result, "0123456789abcdef")

    def test_handle_name_rejects_reserved_names(self):
        for reserved in ("Archipelago", "MultiworldGG"):
            with self.subTest(reserved=reserved):
                with self.assertRaises(Exception):
                    Generate.handle_name(reserved, 1, Counter())


class TestUpdateWeightsCopiesPlainValues(unittest.TestCase):
    def test_update_weights_copies_plain_values_to_avoid_shared_mutation(self):
        shared = {"mutable_list": ["a", "b"], "mutable_dict": {"k": 1}}
        snapshot = copy.deepcopy(shared)

        first = Generate.update_weights({}, shared, "Tested", "slot_a")
        # Mutating the stored result must not reach back into the shared source.
        first["mutable_list"].append("mutated")
        first["mutable_dict"]["k"] = 999

        self.assertEqual(shared, snapshot)

        # A second slot rolling from the same source still sees the originals.
        second = Generate.update_weights({}, shared, "Tested", "slot_b")
        self.assertEqual(second["mutable_list"], ["a", "b"])
        self.assertEqual(second["mutable_dict"], {"k": 1})
        self.assertIsNot(second["mutable_list"], shared["mutable_list"])


class TestMysteryArgparsePaths(unittest.TestCase):
    def test_mystery_argparse_resolves_relative_weights_and_meta_paths(self):
        player_files_path = os.path.join("some", "players")
        absolute_output = os.path.abspath(os.path.join(os.sep, "tmp", "out"))
        args = Generate.mystery_argparse([
            "--player-files-path", player_files_path,
            "--weights-file-path", "w.yaml",
            "--meta-file-path", "m.yaml",
            "--outputpath", absolute_output,
        ])

        self.assertEqual(args.weights_file_path, os.path.join(player_files_path, "w.yaml"))
        self.assertEqual(args.meta_file_path, os.path.join(player_files_path, "m.yaml"))
        # An absolute outputpath is left untouched.
        self.assertEqual(args.outputpath, absolute_output)

    def test_mystery_argparse_keeps_absolute_weights_path(self):
        absolute_weights = os.path.abspath(os.path.join(os.sep, "elsewhere", "w.yaml"))
        args = Generate.mystery_argparse([
            "--player-files-path", os.path.join("some", "players"),
            "--weights-file-path", absolute_weights,
        ])
        self.assertEqual(args.weights_file_path, absolute_weights)


# --------------------------------------------------------------------------- #
# Options.py gotchas previously stated only in inline comments.
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
# ui_dataclasses.UIHint invariants. UIHint instances are built with __new__
# so the bit-flag logic can be exercised without the dict lookups __init__
# requires.
# --------------------------------------------------------------------------- #

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
            UIHint.get_classification(flags), "Progression - Required for Goal"
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


# --------------------------------------------------------------------------- #
# APContainer manifest building and client-function parsing: the manifest
# version fields, the player container's default `server` value, and what
# parse_client_function extracts (and when it returns None).
# --------------------------------------------------------------------------- #

def test_get_manifest_reports_compatible_version_5_and_container_version():
    manifest = APContainer().get_manifest()
    assert manifest["compatible_version"] == 5
    assert manifest["version"] == container_version
    assert container_version == 7


def test_player_container_manifest_server_defaults_to_empty_string():
    manifest = APPlayerContainer().get_manifest()
    assert manifest["server"] == ""


def test_parse_client_function_returns_name_for_client_component_else_none():
    client = (
        'components.append(Component("My Client", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(client) == "launch_client"

    # Not a components.append(Component(...)) call -> None.
    not_append = (
        'registry.add(Component("My Client", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(not_append) is None

    # Unparseable input is swallowed and yields None.
    assert parse_client_function("def (((") is None


def test_parse_client_function_requires_both_client_type_and_func():
    missing_func = 'components.append(Component("X", component_type=Type.CLIENT))'
    assert parse_client_function(missing_func) is None

    missing_type = 'components.append(Component("X", func=launch_client))'
    assert parse_client_function(missing_type) is None

    wrong_type = (
        'components.append(Component("X", '
        "func=launch_client, component_type=Type.TOOL))"
    )
    assert parse_client_function(wrong_type) is None

    both = (
        'components.append(Component("X", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(both) == "launch_client"
