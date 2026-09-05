"""Pin non-obvious NetUtils behaviors that were previously only described by inline comments."""

import enum
import unittest

from BaseUtils import Version
from NetUtils import (
    Hint,
    HintStatus,
    JSONtoTextParser,
    NetworkPlayer,
    NetworkSlot,
    Permission,
    SlotType,
)


class NetworkSlotTest(unittest.TestCase):
    def test_network_slot_group_members_defaults_empty(self) -> None:
        slot = NetworkSlot(name="n", game="g", type=SlotType.player)
        self.assertEqual(slot.group_members, ())
        populated = NetworkSlot(name="n", game="g", type=SlotType.group, group_members=[1, 2, 3])
        self.assertEqual(populated.group_members, [1, 2, 3])


class ScanForTypedTuplesTest(unittest.TestCase):
    def test_scan_for_typedtuples_adds_class_key_for_namedtuple(self) -> None:
        from NetUtils import _scan_for_TypedTuples

        result = _scan_for_TypedTuples(NetworkPlayer(1, 2, "al", "nm"))
        self.assertEqual(
            result,
            {"team": 1, "slot": 2, "alias": "al", "name": "nm", "class": "NetworkPlayer"},
        )

    def test_scan_for_typedtuples_plain_tuple_stays_plain(self) -> None:
        from NetUtils import _scan_for_TypedTuples

        self.assertEqual(_scan_for_TypedTuples((1, 2, 3)), (1, 2, 3))

    def test_scan_for_typedtuples_recurses_into_nested_containers(self) -> None:
        from NetUtils import _scan_for_TypedTuples

        nested = {"players": [NetworkPlayer(1, 2, "al", "nm")]}
        result = _scan_for_TypedTuples(nested)
        self.assertEqual(result["players"][0]["class"], "NetworkPlayer")


class ConvertToBaseTypesTest(unittest.TestCase):
    def test_convert_to_base_types_unwraps_str_enum_subclass(self) -> None:
        from NetUtils import convert_to_base_types

        class MyStrEnum(enum.StrEnum):
            A = "hello"

        result = convert_to_base_types(MyStrEnum.A)
        self.assertEqual(result, "hello")
        self.assertIs(type(result), str)

    def test_convert_to_base_types_unwraps_int_enum_subclass(self) -> None:
        from NetUtils import convert_to_base_types

        class MyIntEnum(enum.IntEnum):
            A = 5

        result = convert_to_base_types(MyIntEnum.A)
        self.assertEqual(result, 5)
        self.assertIs(type(result), int)

    def test_convert_to_base_types_raises_on_unhandled_type(self) -> None:
        from NetUtils import convert_to_base_types

        with self.assertRaises(Exception):
            convert_to_base_types(object())


class GetAnyVersionTest(unittest.TestCase):
    def test_get_any_version_accepts_capitalized_keys(self) -> None:
        from NetUtils import get_any_version

        self.assertEqual(get_any_version({"Major": 1, "Minor": 2, "Build": 3}), Version(1, 2, 3))

    def test_get_any_version_accepts_lowercase_keys(self) -> None:
        from NetUtils import get_any_version

        self.assertEqual(get_any_version({"major": 4, "minor": 5, "build": 6}), Version(4, 5, 6))


class HandleItemNameColorTest(unittest.TestCase):
    def _color_for(self, flags: int) -> str:
        parser = JSONtoTextParser(ctx=None)
        node = {"type": "item_name", "text": "X", "flags": flags}
        parser._handle_item_name(node)
        return node["color"]

    def test_handle_item_name_flag_color_mapping(self) -> None:
        # 0 -> filler (regular), 0b10 -> useful
        self.assertEqual(self._color_for(0), "regular_item_color;")
        self.assertEqual(self._color_for(0b00010), "useful_item_color;")


class SlotTypeTest(unittest.TestCase):
    def test_slottype_always_goal_true_except_player(self) -> None:
        self.assertTrue(SlotType.spectator.always_goal)
        self.assertTrue(SlotType.group.always_goal)
        self.assertFalse(SlotType.player.always_goal)


class PermissionFromTextTest(unittest.TestCase):
    def test_permission_from_text_bit_combinations(self) -> None:
        self.assertEqual(Permission.from_text(""), Permission.disabled)
        self.assertEqual(int(Permission.from_text("")), 0)
        self.assertEqual(Permission.from_text("enabled"), Permission.enabled)
        self.assertEqual(int(Permission.from_text("enabled")), 0b001)
        self.assertEqual(Permission.from_text("goal"), Permission.goal)
        self.assertEqual(int(Permission.from_text("goal")), 0b010)
        # "auto" sets 0b110; elif means "auto" wins over "goal"
        self.assertEqual(Permission.from_text("auto"), Permission.auto)
        self.assertEqual(int(Permission.from_text("auto")), 0b110)
        self.assertEqual(Permission.from_text("auto_enabled"), Permission.auto_enabled)
        self.assertEqual(int(Permission.from_text("auto_enabled")), 0b111)
        # goal + enabled combine to 0b011
        self.assertEqual(int(Permission.from_text("goal_enabled")), 0b011)

    def test_permission_flag_composition_contracts(self) -> None:
        # disabled is the empty flag; it grants nothing.
        self.assertEqual(Permission.disabled, Permission(0))
        self.assertNotIn(Permission.enabled, Permission.disabled)
        # auto is goal-gated: it must carry the goal bit (this is why from_text's
        # elif is safe and why "auto implies goal" holds), but not the enabled bit.
        self.assertIn(Permission.goal, Permission.auto)
        self.assertNotIn(Permission.enabled, Permission.auto)
        self.assertEqual(Permission.auto & Permission.goal, Permission.goal)
        # auto_enabled is the full composition: auto plus manual (enabled) use.
        self.assertEqual(Permission.auto | Permission.enabled, Permission.auto_enabled)
        self.assertIn(Permission.enabled, Permission.auto_enabled)
        self.assertIn(Permission.goal, Permission.auto_enabled)
        # enabled (manual only) must not imply goal-completion access.
        self.assertNotIn(Permission.goal, Permission.enabled)


class ObjectHookDecodeTest(unittest.TestCase):
    def test_decode_object_hook_filters_unknown_fields(self) -> None:
        from NetUtils import decode

        slot = decode(
            '{"name":"n","game":"g","type":1,"group_members":[],'
            '"EXTRA":"drop","class":"NetworkSlot"}'
        )
        self.assertEqual(slot, NetworkSlot(name="n", game="g", type=1, group_members=[]))
        self.assertNotIn("EXTRA", slot._asdict())

    def test_decode_object_hook_version_custom_hook_takes_precedence(self) -> None:
        from NetUtils import decode

        version = decode('{"class":"Version","Major":1,"Minor":2,"Build":3}')
        self.assertEqual(version, Version(1, 2, 3))

    def test_decode_without_class_returns_plain_dict(self) -> None:
        from NetUtils import decode

        self.assertEqual(decode('{"a":1}'), {"a": 1})


class HintTest(unittest.TestCase):
    def _hint(self, **overrides) -> Hint:
        base = dict(
            receiving_player=1,
            finding_player=2,
            location=3,
            item=4,
            found=False,
            entrance="e",
        )
        base.update(overrides)
        return Hint(**base)

    def test_hint_hash_ignores_status_and_found(self) -> None:
        a = self._hint(found=False, status=HintStatus.HINT_UNSPECIFIED, item_flags=0, hidden=False)
        b = self._hint(found=True, status=HintStatus.HINT_FOUND, item_flags=99, hidden=True)
        self.assertEqual(hash(a), hash(b))
        # a difference in an identity field does change the hash
        self.assertNotEqual(hash(a), hash(self._hint(entrance="other")))

    def test_hint_re_check_marks_found_when_location_checked(self) -> None:
        class Ctx:
            pass

        ctx = Ctx()
        hint = self._hint()
        # location not in checked set -> unchanged self
        ctx.location_checks = {(0, 2): set()}
        self.assertIs(hint.re_check(ctx, 0), hint)
        # location checked -> a copy with found=True and HINT_FOUND
        ctx.location_checks = {(0, 2): {3}}
        result = hint.re_check(ctx, 0)
        self.assertIsNot(result, hint)
        self.assertTrue(result.found)
        self.assertEqual(result.status, HintStatus.HINT_FOUND)

    def test_hint_re_prioritize_found_forces_hint_found(self) -> None:
        found_hint = self._hint(found=True, status=HintStatus.HINT_UNSPECIFIED)
        result = found_hint.re_prioritize(None, HintStatus.HINT_AVOID)
        self.assertEqual(result.status, HintStatus.HINT_FOUND)
        # not-found hint keeps the requested status
        not_found = self._hint(found=False, status=HintStatus.HINT_UNSPECIFIED)
        self.assertEqual(
            not_found.re_prioritize(None, HintStatus.HINT_AVOID).status, HintStatus.HINT_AVOID
        )


if __name__ == "__main__":
    unittest.main()
