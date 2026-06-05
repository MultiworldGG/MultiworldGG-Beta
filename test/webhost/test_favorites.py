import re
import unittest
from unittest.mock import patch

from . import TestBase


class TestFavoritesFeature(TestBase):
    def _visible_worlds_stub(self):
        # The test env only loads infra worlds (generic, tracker, _debug), all of which
        # have hidden=True, so get_visible_worlds() returns {}. Reuse the generic world
        # as a stand-in visible world so the /games template's per-world loop renders.
        from worlds.AutoWorld import AutoWorldRegister
        return {"Archipelago": AutoWorldRegister.world_types["Archipelago"]}

    def _get_games_with_visible_world(self):
        from WebHostLib import cache as wh_cache
        wh_cache.clear()
        with patch("WebHostLib.misc.get_visible_worlds", side_effect=self._visible_worlds_stub):
            return self.client.get('/games')

    def test_supported_games_page_loads_with_favorites_section(self):
        """The /games route renders the favorites section and a per-world entry.

        Exercises the real Flask route + supportedGames.html template: the static
        favorites-section block AND the per-world loop driven by get_visible_worlds().
        The stub injects the "Archipelago" world (web.display_name "MultiworldGG-Test"),
        so the rendered <details> must carry data-game="Archipelago" and the
        display-name fallback resolves to the WebWorld display_name, not the game key.
        """
        response = self._get_games_with_visible_world()
        self.assertEqual(response.status_code, 200)
        body = response.data.decode("utf-8")

        # Static favorites-section scaffolding rendered by the template.
        self.assertIn('<div id="favorites-section"', body)
        self.assertIn('id="favorites-list"', body)
        self.assertIn("<h2>Favorite Games</h2>", body)

        # The per-world loop rendered the injected world. data-display-name must be the
        # WebWorld display_name ("MultiworldGG-Test"), proving the
        # `display_name | default(game_name)` filter ran (a mutation that emitted the raw
        # game key instead would change this to "Archipelago").
        details = re.findall(
            r'<details\s+data-game="([^"]+)"\s+data-display-name="([^"]+)"', body
        )
        self.assertIn(("Archipelago", "MultiworldGG-Test"), details)

        # The per-world star icon renders with its game key and the default tooltip.
        self.assertIn(
            '<span class="star-icon" data-game="Archipelago" title="Add to favorites">',
            body,
        )

    def test_star_icons_have_correct_attributes(self):
        """Each rendered star icon carries data-game (the game key) and the add tooltip.

        Pins the template's star-icon markup: a mutation dropping the data-game
        attribute (which the JS keys favorites off of) or changing the default title
        would fail here.
        """
        response = self._get_games_with_visible_world()
        self.assertEqual(response.status_code, 200)
        body = response.data.decode("utf-8")

        star_games = re.findall(
            r'<span class="star-icon" data-game="([^"]+)" title="Add to favorites">',
            body,
        )
        # The injected world produced exactly one star icon keyed to its game name.
        self.assertEqual(star_games, ["Archipelago"])

    def test_favorites_section_is_hidden_by_default(self):
        """The favorites section ships collapsed (inline display:none on that div).

        The section is shown client-side only once a favorite exists, so the server
        must render it hidden. Asserting the style on the favorites-section element
        itself (not just "display: none" appearing anywhere) pins that contract; a
        mutation removing the inline style would fail.
        """
        response = self._get_games_with_visible_world()
        self.assertEqual(response.status_code, 200)
        body = response.data.decode("utf-8")

        self.assertRegex(
            body,
            r'<div id="favorites-section"[^>]*\bstyle="display: none;"',
        )
        # It is also gated behind js-only so non-JS clients never see an empty section.
        self.assertRegex(body, r'<div id="favorites-section"[^>]*\bclass="js-only"')


if __name__ == '__main__':
    unittest.main()
