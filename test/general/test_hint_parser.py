"""Classic hint screen ref parser (NetUtils.KivyRefJSONtoTextParser).

Escape placement is the load-bearing contract: the parent flow escapes inside
the typed handlers and _handle_plaintext, while player_id/player_name and raw
"color" nodes reach _handle_color unescaped — the ref parser must escape exactly
those once and never re-escape anything, and the plain KivyMarkupJSONtoTextParser
console pipeline must stay byte-identical (including its '#'-prefixed
hex_colormap values and unescaped player names).
"""
import unittest

from NetUtils import (
    KivyMarkupJSONtoTextParser,
    KivyRefJSONtoTextParser,
    NetworkSlot,
    SlotType,
    TEXT_COLORS,
)


class _StubCtx:
    slot_info = {
        1: NetworkSlot(name="Alice", game="A Game", type=SlotType.player),
        2: NetworkSlot(name="Bob [BR]", game="B Game", type=SlotType.group, group_members=[1]),
    }
    player_names = {1: "Alice", 2: "Bob [BR]", 3: "Carol"}

    def slot_concerns_self(self, slot):
        return slot == 1


class _ParserTestBase(unittest.TestCase):
    def setUp(self):
        # Both classes seed their color table lazily on first construction;
        # reset so each test controls construction order.
        KivyMarkupJSONtoTextParser.color_codes = None
        KivyRefJSONtoTextParser.color_codes = None

    def tearDown(self):
        KivyMarkupJSONtoTextParser.color_codes = None
        KivyRefJSONtoTextParser.color_codes = None


class KivyRefParserRefEmissionTest(_ParserTestBase):
    def _parse_item(self, flags: int) -> str:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        return parser([{"type": "item_name", "text": "Sword", "flags": flags}])

    def test_item_ref_categories_from_flags(self) -> None:
        cases = {
            0: ("normal", TEXT_COLORS["regular_item_color"]),
            0b00001: ("progression", TEXT_COLORS["progression_item_color"]),
            0b01001: ("progression (goal)", TEXT_COLORS["progression_goal_item_color"]),
            0b10001: ("progression (deprioritized)", TEXT_COLORS["progression_deprioritized_item_color"]),
            0b00110: ("useful, trap", TEXT_COLORS["trap_item_color"]),
        }
        for flags, (categories, color) in cases.items():
            with self.subTest(flags=bin(flags)):
                self.assertEqual(
                    self._parse_item(flags),
                    f"[ref=0|Item Class: {categories}][color={color}]Sword[/color][/ref]",
                )

    def test_player_id_ref_carries_game_type_and_escaped_members(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"type": "player_id", "text": "2"}])
        self.assertEqual(
            out,
            "[ref=0|Game: B Game<br>Type: group<br>Members:<br> Alice]"
            f"[color={TEXT_COLORS['player2_color']}]Bob &bl;BR&br;[/color][/ref]",
        )

    def test_player_id_without_slot_info_emits_no_ref(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"type": "player_id", "text": "3"}])
        self.assertNotIn("[ref=", out)
        self.assertEqual(out, f"[color={TEXT_COLORS['player2_color']}]Carol[/color]")

    def test_ref_count_resets_per_call(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        nodes = [
            {"type": "item_name", "text": "Sword", "flags": 1},
            {"type": "player_id", "text": "1"},
        ]
        first = parser([dict(node) for node in nodes])
        second = parser([dict(node) for node in nodes])
        self.assertEqual(first, second)
        self.assertIn("[ref=0|", first)
        self.assertIn("[ref=1|", first)
        self.assertNotIn("[ref=2|", first)


class KivyRefParserSingleEscapeTest(_ParserTestBase):
    """Each classic hint column's node shape must be escaped exactly once."""

    def test_bracketed_player_name_escapes_once(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"type": "player_id", "text": "2"}])
        self.assertIn("Bob &bl;BR&br;", out)
        self.assertNotIn("&amp;bl;", out)

    def test_entrance_color_node_escapes_once(self) -> None:
        # The entrance cell is a raw "color" node built by HintLog.refresh_hints.
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"type": "color", "color": "entrance_color", "text": "Door [East]"}])
        self.assertEqual(
            out, f"[color={TEXT_COLORS['entrance_color']}]Door &bl;East&br;[/color]"
        )

    def test_untyped_plaintext_escapes_once(self) -> None:
        # Untyped nodes route through _handle_plaintext, which already escapes;
        # _handle_color/_handle_text must not escape again.
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"text": "A [B] & C"}])
        self.assertEqual(
            out, f"[color={TEXT_COLORS['default_color']}]A &bl;B&br; &amp; C[/color]"
        )

    def test_text_typed_node_escapes_once(self) -> None:
        # Explicit "text" nodes dispatch straight to _handle_text unescaped.
        parser = KivyRefJSONtoTextParser(_StubCtx())
        self.assertEqual(parser([{"type": "text", "text": "[x]"}]), "&bl;x&br;")

    def test_item_name_escapes_once(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        out = parser([{"type": "item_name", "text": "Sword [S]", "flags": 1}])
        self.assertIn("Sword &bl;S&br;", out)
        self.assertNotIn("&amp;bl;", out)


class KivyRefParserColorTableTest(_ParserTestBase):
    def test_subclass_table_is_bare_hex(self) -> None:
        parser = KivyRefJSONtoTextParser(_StubCtx())
        offenders = [name for name, value in parser.color_codes.items()
                     if value.startswith("#")]
        self.assertFalse(offenders, f"'#'-prefixed color values remain: {offenders[:5]}")
        self.assertEqual(parser.color_codes["red"], "ff0000")
        self.assertEqual(parser.color_codes["entrance_color"], TEXT_COLORS["entrance_color"])


class KivyMarkupParserRegressionTest(_ParserTestBase):
    """The console parser must be byte-identical to its pre-ref-parser behavior,
    even after the subclass has been constructed and normalized its own table."""

    def test_base_parser_output_and_table_unchanged(self) -> None:
        ref_parser = KivyRefJSONtoTextParser(_StubCtx())
        ref_parser([{"type": "player_id", "text": "2"}])

        base = KivyMarkupJSONtoTextParser(_StubCtx())
        # hex_colormap-derived values keep their leading '#'.
        self.assertEqual(base.color_codes["red"], "#ff0000")
        # Plaintext: escaped once, default color.
        self.assertEqual(
            base([{"text": "A [B] & C"}]),
            f"[color={TEXT_COLORS['default_color']}]A &bl;B&br; &amp; C[/color]",
        )
        # Player names stay UNescaped (legacy console behavior, pinned).
        self.assertEqual(
            base([{"type": "player_id", "text": "2"}]),
            f"[color={TEXT_COLORS['player2_color']}]Bob [BR][/color]",
        )
        # Raw color nodes stay UNescaped and emit no refs.
        self.assertEqual(
            base([{"type": "color", "color": "entrance_color", "text": "Door [East]"}]),
            f"[color={TEXT_COLORS['entrance_color']}]Door [East][/color]",
        )


if __name__ == "__main__":
    unittest.main()
