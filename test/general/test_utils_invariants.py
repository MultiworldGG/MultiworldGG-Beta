"""Behavioral invariants for helpers in Utils.py.

Each test pins a non-obvious behavior that previously lived only as an inline
comment in the source.
"""
import io
import pickle
import unittest

from Utils import (
    _expand_game_choices,
    get_fuzzy_results,
    is_iterable_except_str,
    read_snes_rom,
    restricted_dumps,
    restricted_loads,
)


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


if __name__ == "__main__":
    unittest.main()
