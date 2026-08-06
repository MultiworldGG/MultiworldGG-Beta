"""Pin non-obvious NetUtils behaviors that were previously only described by inline comments."""

import enum
import unittest

from BaseUtils import Version
from NetUtils import (
    ITEM_CLASS_TOOLTIP_LABELS,
    TEXT_COLORS,
    Hint,
    HintStatus,
    JSONtoTextParser,
    NetworkPlayer,
    NetworkSlot,
    Permission,
    SlotType,
    find_enclosing_color_span,
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
        self.assertEqual(self._color_for(0), "regular_item_color")
        self.assertEqual(self._color_for(0b00010), "useful_item_color")

    def test_handle_item_name_trap_overrides_useful(self) -> None:
        self.assertEqual(self._color_for(0b00100), "trap_item_color")
        # useful bit also set -> trap still wins
        self.assertEqual(self._color_for(0b00110), "trap_item_color")

    def test_handle_item_name_progression_variants_precedence(self) -> None:
        # plain progression
        self.assertEqual(self._color_for(0b00001), "progression_item_color")
        # progression overrides a preceding useful bit
        self.assertEqual(self._color_for(0b00011), "progression_item_color")
        # deprioritized takes priority over skip_balancing
        self.assertEqual(self._color_for(0b10001), "progression_deprioritized_item_color")
        self.assertEqual(self._color_for(0b11001), "progression_deprioritized_item_color")
        # skip_balancing only (no deprioritized) -> goal color
        self.assertEqual(self._color_for(0b01001), "progression_goal_item_color")


class FindEnclosingColorSpanTest(unittest.TestCase):
    SPAN = "[color=ffbe00]Progressive Sword[/color]"
    TEXT = "You found " + SPAN + " at Link's House"
    EXPECTED = (10, 10 + len(SPAN), "ffbe00")

    def test_index_inside_span_text(self) -> None:
        index = self.TEXT.index("Progressive") + 3
        self.assertEqual(find_enclosing_color_span(self.TEXT, index), self.EXPECTED)

    def test_index_between_spans_returns_none(self) -> None:
        two = "[color=ffbe00]A[/color] and [color=6EC471]B[/color]"
        self.assertIsNone(find_enclosing_color_span(two, two.index(" and ") + 2))
        # plain text before the first span and after the last one
        self.assertIsNone(find_enclosing_color_span(self.TEXT, 0))
        self.assertIsNone(find_enclosing_color_span(self.TEXT, len(self.TEXT) - 1))
        # the character immediately after the close tag is outside
        self.assertIsNone(find_enclosing_color_span(self.TEXT, 10 + len(self.SPAN)))

    def test_index_inside_open_tag_literal_counts_as_inside(self) -> None:
        for offset in (0, 1, len("[color="), len("[color=ffbe00]") - 1):
            self.assertEqual(
                find_enclosing_color_span(self.TEXT, 10 + offset), self.EXPECTED,
                f"offset {offset}",
            )

    def test_index_inside_close_tag_literal_counts_as_inside(self) -> None:
        close_start = self.TEXT.index("[/color]")
        for offset in range(len("[/color]")):
            self.assertEqual(
                find_enclosing_color_span(self.TEXT, close_start + offset), self.EXPECTED,
                f"offset {offset}",
            )

    def test_wrapped_multi_line_span(self) -> None:
        text = "line one\n[color=6EC471]Multi\nline item\nname[/color]\ntail"
        expected = (text.index("[color="), text.index("[/color]") + len("[/color]"), "6EC471")
        self.assertEqual(find_enclosing_color_span(text, text.index("item")), expected)

    def test_default_color_span_still_resolved(self) -> None:
        # filtering to item classes is the caller's job; the scan itself is color-agnostic
        text = "[color=cdcdcd]plain chat[/color]"
        self.assertEqual(find_enclosing_color_span(text, text.index("chat")), (0, len(text), "cdcdcd"))

    def test_hash_prefixed_hex_is_normalized(self) -> None:
        # hex_colormap-derived emissions carry a leading '#'
        text = "[color=#008000](found)[/color]"
        self.assertEqual(find_enclosing_color_span(text, text.index("found")), (0, len(text), "008000"))

    def test_window_caps_backward_scan(self) -> None:
        text = "[color=ffbe00]" + "x" * 100 + "[/color]"
        index = text.index("[/color]") - 1
        self.assertIsNotNone(find_enclosing_color_span(text, index, window=200))
        self.assertIsNone(find_enclosing_color_span(text, index, window=50))

    def test_window_caps_forward_scan(self) -> None:
        text = "[color=ffbe00]" + "x" * 100 + "[/color]"
        index = text.index("x")
        self.assertIsNotNone(find_enclosing_color_span(text, index, window=200))
        self.assertIsNone(find_enclosing_color_span(text, index, window=50))

    def test_malformed_markup_returns_none(self) -> None:
        # open tag missing its closing bracket
        self.assertIsNone(find_enclosing_color_span("[color=ffbe00 text", 8))
        # color value is not hex
        self.assertIsNone(find_enclosing_color_span("[color=goldish]item[/color]", 16))
        # unclosed span
        self.assertIsNone(find_enclosing_color_span("[color=ffbe00]item", 15))
        # bare close tag with no opener
        self.assertIsNone(find_enclosing_color_span("text [/color] more", 7))
        # out-of-range index
        self.assertIsNone(find_enclosing_color_span(self.TEXT, -1))
        self.assertIsNone(find_enclosing_color_span(self.TEXT, len(self.TEXT)))

    def test_unescaped_bracket_text_degrades_gracefully(self) -> None:
        # _handle_player_id inserts player names without escape_markup, so a
        # bracket-bearing slot name can unbalance the emitted tags. The scan
        # must return None or a span containing the index, never raise.
        samples = (
            "[color=ff87d7]we[ird[]name[/color] sent [color=00c51b]X[/color]",
            "[color=ff87d7]name[/color]tail[/color]",
            "[color=ff87d7][color=5fafff]nested[/color]",
        )
        for text in samples:
            for index in range(len(text) + 2):
                result = find_enclosing_color_span(text, index)
                if result is not None:
                    start, end, _ = result
                    self.assertLessEqual(start, index, f"{text!r} @ {index}")
                    self.assertLess(index, end, f"{text!r} @ {index}")


class ItemClassTooltipLabelsTest(unittest.TestCase):
    def test_labels_keyed_by_known_text_colors(self) -> None:
        self.assertLessEqual(set(ITEM_CLASS_TOOLTIP_LABELS), set(TEXT_COLORS))

    def test_labels_cover_exactly_the_item_class_colors(self) -> None:
        # the allowlist is the six *_item_color entries — nothing shared with
        # command echo, players, locations, or entrances
        item_colors = {name for name in TEXT_COLORS if name.endswith("_item_color")}
        self.assertEqual(set(ITEM_CLASS_TOOLTIP_LABELS), item_colors)


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
