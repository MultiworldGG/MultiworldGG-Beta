"""Console markup parser (NetUtils.KivyMarkupJSONtoTextParser).

Refs are emitted inline as ``[ref=N|payload][color=..]text[/color][/ref]`` with
``<br>`` for line breaks inside the payload; a raw newline in a payload cannot
be rendered by the console. Escape placement: the typed handlers escape before
delegating to _handle_color, while player_id/player_name and raw "color" nodes
reach it unescaped (pinned below, see the note in NetUtils). hex_colormap values
keep their leading '#'; TEXT_COLORS values are bare hex.
"""
import unittest

import pytest

# The bundled kivy/ dir at repo root is an __init__-less namespace-package
# decoy: plain `importorskip("kivy")` passes without kivy installed. Guard on
# the submodule the parser actually imports.
pytest.importorskip("kivy.utils")

from NetUtils import (
    KivyMarkupJSONtoTextParser,
    NetworkSlot,
    SlotType,
    TEXT_COLORS,
)


class _StubCtx:
    slot_info = {
        1: NetworkSlot(name="Alice [A]", game="A Game", type=SlotType.player),
        2: NetworkSlot(name="Bob [BR]", game="B Game", type=SlotType.group, group_members=[1]),
    }
    player_names = {1: "Alice [A]", 2: "Bob [BR]", 3: "Carol"}

    def slot_concerns_self(self, slot):
        return slot == 1


class _ParserTestBase(unittest.TestCase):
    def setUp(self):
        # The color table is seeded lazily on first construction.
        KivyMarkupJSONtoTextParser.color_codes = None
        self.parser = KivyMarkupJSONtoTextParser(_StubCtx())

    def tearDown(self):
        KivyMarkupJSONtoTextParser.color_codes = None


class RefEmissionTest(_ParserTestBase):
    def test_item_ref_categories_from_flags(self) -> None:
        cases = {
            0: ("normal", TEXT_COLORS["regular_item_color"]),
            0b00001: ("progression", TEXT_COLORS["progression_item_color"]),
            0b01001: ("progression, skip_balancing", TEXT_COLORS["progression_goal_item_color"]),
            0b10001: ("progression, deprioritized", TEXT_COLORS["progression_deprioritized_item_color"]),
            0b00110: ("useful, trap", TEXT_COLORS["trap_item_color"]),
        }
        for flags, (categories, color) in cases.items():
            with self.subTest(flags=bin(flags)):
                self.assertEqual(
                    self.parser([{"type": "item_name", "text": "Sword", "flags": flags}]),
                    f"[ref=0|Item Class: {categories}][color={color}]Sword[/color][/ref]",
                )

    def test_player_id_ref_carries_game_type_and_escaped_members(self) -> None:
        out = self.parser([{"type": "player_id", "text": "2"}])
        self.assertEqual(
            out,
            "[ref=0|Game: B Game<br>Type: group<br>Members:<br> Alice &bl;A&br;]"
            f"[color={TEXT_COLORS['player2_color']}]Bob [BR][/color][/ref]",
        )

    def test_own_slot_uses_player1_color(self) -> None:
        self.assertEqual(
            self.parser([{"type": "player_id", "text": "1"}]),
            f"[ref=0|Game: A Game<br>Type: player][color={TEXT_COLORS['player1_color']}]Alice [A][/color][/ref]",
        )

    def test_player_id_without_slot_info_emits_no_ref(self) -> None:
        out = self.parser([{"type": "player_id", "text": "3"}])
        self.assertNotIn("[ref=", out)
        self.assertEqual(out, f"[color={TEXT_COLORS['player2_color']}]Carol[/color]")

    def test_refs_are_inline_and_never_contain_newlines(self) -> None:
        out = self.parser([
            {"type": "player_id", "text": "2"},
            {"text": " sent "},
            {"type": "item_name", "text": "Sword", "flags": 1},
        ])
        self.assertNotIn("\n", out)
        self.assertTrue(out.startswith("[ref=0|"))
        self.assertIn(f"[/ref][color={TEXT_COLORS['default_color']}] sent [/color][ref=1|", out)

    def test_ref_count_resets_per_call(self) -> None:
        nodes = [
            {"type": "item_name", "text": "Sword", "flags": 1},
            {"type": "player_id", "text": "1"},
        ]
        first = self.parser([dict(node) for node in nodes])
        second = self.parser([dict(node) for node in nodes])
        self.assertEqual(first, second)
        self.assertIn("[ref=0|", first)
        self.assertIn("[ref=1|", first)
        self.assertNotIn("[ref=2|", first)


class EscapePlacementTest(_ParserTestBase):
    def test_untyped_plaintext_escapes_once(self) -> None:
        self.assertEqual(
            self.parser([{"text": "A [B] & C"}]),
            f"[color={TEXT_COLORS['default_color']}]A &bl;B&br; &amp; C[/color]",
        )

    def test_item_name_escapes_once(self) -> None:
        out = self.parser([{"type": "item_name", "text": "Sword [S]", "flags": 1}])
        self.assertIn("Sword &bl;S&br;", out)
        self.assertNotIn("&amp;bl;", out)

    def test_location_name_escapes_once(self) -> None:
        self.assertEqual(
            self.parser([{"type": "location_name", "text": "Cave [1]"}]),
            f"[color={TEXT_COLORS['location_color']}]Cave &bl;1&br;[/color]",
        )

    def test_player_and_raw_color_nodes_stay_unescaped(self) -> None:
        # Known gap, pinned so a change here is deliberate (see the note in
        # KivyMarkupJSONtoTextParser._handle_color).
        self.assertIn("]Bob [BR][/color]", self.parser([{"type": "player_id", "text": "2"}]))
        self.assertEqual(
            self.parser([{"type": "color", "color": "entrance_color", "text": "Door [East]"}]),
            f"[color={TEXT_COLORS['entrance_color']}]Door [East][/color]",
        )


class ColorTableTest(_ParserTestBase):
    def test_hex_colormap_keeps_hash_and_text_colors_are_bare(self) -> None:
        self.assertEqual(self.parser.color_codes["red"], "#ff0000")
        self.assertEqual(self.parser.color_codes["entrance_color"], TEXT_COLORS["entrance_color"])
        self.assertEqual(
            self.parser([{"type": "color", "color": "red", "text": "warn"}]),
            "[color=#ff0000]warn[/color]",
        )


if __name__ == "__main__":
    unittest.main()
