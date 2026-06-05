"""Behavioral tests for ``settings.Group.update`` value coercion and change tracking.

These pin the non-obvious type-coercion branches of ``Group.update`` (bool vs int,
Optional/None, scalar upcast to the declared type, list -> tuple/set) and the
"key missing from the supplied dict marks the Group as changed" semantics.
"""
from typing import Optional, Tuple
from unittest import TestCase

from settings import Group, ServerOptions


class _Tup(Tuple[int, ...]):
    """Bare tuple subclass so the annotation resolves to a real ``type``."""


class TestGroupUpdateCoercion(TestCase):
    def test_update_preserves_bool_for_bool_field(self) -> None:
        class G(Group):
            flag: bool = False

        g = G()
        g.update({"flag": True})
        # not coerced to int, even though issubclass(int, bool) is True
        self.assertIs(type(g.flag), bool)
        self.assertIs(g.flag, True)

    def test_update_assigns_none_for_optional(self) -> None:
        class G(Group):
            opt: Optional[int] = 7

        g = G()
        g.update({"opt": None})
        self.assertIsNone(g.opt)

    def test_update_upcasts_int_to_intenum(self) -> None:
        class G(Group):
            comp: ServerOptions.Compatibility = ServerOptions.Compatibility(2)

        g = G()
        g.update({"comp": 0})
        self.assertIsInstance(g.comp, ServerOptions.Compatibility)
        self.assertIs(g.comp, ServerOptions.Compatibility.OFF)

    def test_update_converts_list_to_tuple_field(self) -> None:
        class G(Group):
            tup: _Tup = _Tup()

        g = G()
        g.update({"tup": [1, 2, 3]})
        self.assertIsInstance(g.tup, _Tup)
        self.assertEqual(g.tup, (1, 2, 3))


class TestGroupUpdateChanged(TestCase):
    def test_update_marks_changed_on_missing_key(self) -> None:
        class G(Group):
            a: int = 1
            b: int = 2

        g = G()
        self.assertFalse(g.changed)
        g.update({"a": 5})  # "b" absent from the supplied dict
        self.assertTrue(g.changed)

    def test_update_not_changed_when_all_keys_present(self) -> None:
        class G(Group):
            a: int = 1
            b: int = 2

        g = G()
        g.update({"a": 5, "b": 6})
        self.assertFalse(g.changed)
