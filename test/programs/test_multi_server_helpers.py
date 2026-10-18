"""Behavioral tests for MultiServer's stand-alone data-mutation helpers.

These pin the non-obvious edge-case behavior of the storable-data helper
functions (the building blocks of modify_functions) and the Client
items_handling flag codec, without needing a live Context or sockets.
"""

import unittest

from MultiServer import (
    modify_functions,
    pop_from_container,
    remove_from_list,
    update_container_unique,
)


class TestModifyFunctionsAdd(unittest.TestCase):
    def test_modify_functions_add_concatenates_and_sums(self) -> None:
        add = modify_functions["add"]
        # numeric "+" sums
        self.assertEqual(add(2, 3), 5)
        # string "+" concatenates (append semantics)
        self.assertEqual(add("foo", "bar"), "foobar")
        # list "+" concatenates (append semantics)
        self.assertEqual(add([1, 2], [3, 4]), [1, 2, 3, 4])


class TestRemoveFromList(unittest.TestCase):
    def test_remove_from_list_removes_present_value(self) -> None:
        self.assertEqual(remove_from_list([1, 2, 3], 2), [1, 3])

    def test_remove_from_list_missing_value_is_noop(self) -> None:
        container = [1, 2, 3]
        result = remove_from_list(container, 99)
        # absent value: no raise, container returned unchanged (same object)
        self.assertIs(result, container)
        self.assertEqual(result, [1, 2, 3])


class TestPopFromContainer(unittest.TestCase):
    def test_pop_from_container_pops_valid_index_and_key(self) -> None:
        self.assertEqual(pop_from_container([10, 20, 30], 1), [10, 30])
        self.assertEqual(pop_from_container({"a": 1, "b": 2}, "a"), {"b": 2})

    def test_pop_from_container_ignores_missing_index_and_key(self) -> None:
        out_of_range = [10, 20, 30]
        # index >= len is a no-op, original list returned unchanged
        self.assertIs(pop_from_container(out_of_range, 5), out_of_range)
        self.assertEqual(out_of_range, [10, 20, 30])

        missing_key = {"a": 1, "b": 2}
        # absent dict key is a no-op, original mapping returned unchanged
        self.assertIs(pop_from_container(missing_key, "z"), missing_key)
        self.assertEqual(missing_key, {"a": 1, "b": 2})


class TestUpdateContainerUnique(unittest.TestCase):
    def test_update_container_unique_skips_existing_list_entries(self) -> None:
        container = [1, 2, 3]
        result = update_container_unique(container, [2, 3, 4, 5])
        # only entries not already present are appended, in given order, no dupes
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_update_container_unique_uses_dict_update_for_mappings(self) -> None:
        container = {"a": 1}
        result = update_container_unique(container, {"a": 9, "b": 2})
        # dict branch is a plain update: existing keys overwritten, new keys added
        self.assertEqual(result, {"a": 9, "b": 2})


class TestClientItemsHandling(unittest.TestCase):
    def _client(self):
        # Build a Client without a real socket; items_handling only touches the
        # boolean flag slots set in __init__, not the connection.
        from MultiServer import Client

        client = Client.__new__(Client)
        client.no_items = False
        client.remote_items = False
        client.remote_start_inventory = False
        return client

    def test_client_items_handling_roundtrips_valid_values(self) -> None:
        client = self._client()
        for value in (0, 0b001, 0b011, 0b101, 0b111):
            client.items_handling = value
            self.assertEqual(client.items_handling, value)

    def test_client_items_handling_invalid_flag_combo_raises(self) -> None:
        client = self._client()
        # remote / start-inventory bits (0b110) without the base 0b001 bit
        for bad in (0b010, 0b100, 0b110):
            with self.assertRaises(ValueError):
                client.items_handling = bad


if __name__ == "__main__":
    unittest.main()
