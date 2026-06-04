import warnings
from unittest import TestCase

from settings import Group
from worlds.AutoWorld import AutoWorldRegister


class TestSettings(TestCase):
    def test_settings_can_update(self) -> None:
        """
        Test that every world's settings Group can update from an empty dict without crashing.
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=game_name):
                if world_type.settings is not None:
                    self.assertIsInstance(world_type.settings, Group)
                    world_type.settings.update({})  # a previous bug had a crash in this call to update


class TestGroupUpdate(TestCase):
    """Directly exercise ``settings.Group.update`` so that mutations to its logic are caught."""

    def test_update_upcasts_values_to_annotated_types(self) -> None:
        """Scalars/collections are coerced to the field's annotated type."""
        class Sub(Group):
            name: str = "default"
            count: int = 0
            coords: tuple = (0, 0)
            members: set = set()
            flag: bool = False

        sub = Sub()
        sub.update({
            "name": "hello",
            "count": 5,
            "coords": [1, 2, 3],      # list -> tuple
            "members": [1, 2, 2, 3],  # list -> set
            "flag": True,
        })

        self.assertEqual(sub.name, "hello")
        self.assertEqual(sub.count, 5)
        self.assertEqual(sub.coords, (1, 2, 3))
        self.assertIsInstance(sub.coords, tuple)
        self.assertEqual(sub.members, {1, 2, 3})
        self.assertIsInstance(sub.members, set)
        self.assertIs(sub.flag, True)

    def test_update_recurses_into_nested_group_with_copy_isolation(self) -> None:
        """A nested Group is updated on a per-instance copy, leaving the class default untouched."""
        class Inner(Group):
            x: int = 1

        class Outer(Group):
            inner: Inner = Inner()

        outer = Outer()
        outer.update({"inner": {"x": 42}})

        self.assertIsInstance(outer.inner, Inner)
        self.assertEqual(outer.inner.x, 42)
        # the shared class-level default must not be mutated by the per-instance update
        self.assertEqual(Outer.__dict__["inner"].x, 1)
        self.assertIsNot(outer.__dict__["inner"], Outer.__dict__["inner"])

    def test_update_marks_changed_when_annotated_key_missing(self) -> None:
        """A field absent from the update dict flags the Group as changed (host.yaml is stale)."""
        class Sub(Group):
            a: int = 0
            b: int = 0

        complete = Sub()
        complete.update({"a": 1, "b": 2})
        self.assertFalse(complete._changed)

        partial = Sub()
        partial.update({"a": 1})  # 'b' missing
        self.assertTrue(partial._changed)
        self.assertEqual(partial.a, 1)

    def test_update_rejects_non_dict_argument(self) -> None:
        """Passing a non-dict raises AssertionError naming the offending type."""
        class Sub(Group):
            a: int = 0

        with self.assertRaises(AssertionError) as ctx:
            Sub().update(["not", "a", "dict"])  # type: ignore[arg-type]
        self.assertIn("list instead of dict", str(ctx.exception))

    def test_update_warns_when_updating_group_from_non_dict(self) -> None:
        """Feeding a Group field a scalar warns instead of silently corrupting it."""
        class Inner(Group):
            x: int = 0

        class Outer(Group):
            inner: Inner = Inner()

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            Outer().update({"inner": 5})

        self.assertTrue(any("tried to update Group" in str(w.message) for w in caught))
