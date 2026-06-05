"""Pins non-obvious behaviors of Generate.py core helpers (handle_name,
update_weights, mystery_argparse) that were previously documented only by
inline comments."""

import copy
import os
import unittest
from collections import Counter

import Generate


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


if __name__ == "__main__":
    unittest.main()
