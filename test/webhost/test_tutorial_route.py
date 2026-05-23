"""Tests for the canonical ``/learn/<lang>/tutorial/<game>/<file>`` route
and the ``_split_tutorial_file`` helper that powers the legacy redirects.

The handler reads from ``static/generated/docs/<game>/<file>_<lang>.md``,
which is populated by ``copy_tutorials_files_to_static`` at app startup.
The session-scoped ``app`` fixture in conftest.py runs that copy step
once (via ``get_app``), so the on-disk Archipelago tutorial files
(``setup_en.md`` etc.) are available for these tests.
"""
from __future__ import annotations

import pytest

from WebHostLib.misc import _split_tutorial_file


class TestSplitTutorialFile:
    @pytest.mark.parametrize("file_in, base_out, lang_out", [
        ("setup_en", "setup", "en"),
        ("setup_fr", "setup", "fr"),
        ("advanced_settings_en", "advanced_settings", "en"),
        ("commands_en", "commands", "en"),
    ])
    def test_splits_two_letter_lang_suffix(self, file_in, base_out, lang_out):
        assert _split_tutorial_file(file_in) == (base_out, lang_out)

    def test_defaults_to_en_when_no_underscore(self):
        assert _split_tutorial_file("intro") == ("intro", "en")

    def test_does_not_split_three_letter_suffix(self):
        assert _split_tutorial_file("setup_eng") == ("setup_eng", "en")

    def test_does_not_split_numeric_suffix(self):
        assert _split_tutorial_file("setup_v2") == ("setup_v2", "en")

    def test_uses_rightmost_underscore(self):
        """``advanced_settings_en`` must split into ``("advanced_settings", "en")``
        — rpartition splits from the right, not the left.
        """
        assert _split_tutorial_file("advanced_settings_en") == (
            "advanced_settings", "en",
        )

    def test_custom_default_lang(self):
        assert _split_tutorial_file("intro", default_lang="fr") == ("intro", "fr")


class TestCanonicalTutorialRoute:
    def test_serves_existing_tutorial(self, client):
        response = client.get("/learn/en/tutorial/Archipelago/setup")
        assert response.status_code == 200
        assert b"<html" in response.data.lower() or b"<!doctype" in response.data.lower()

    def test_unknown_file_404s(self, client):
        response = client.get("/learn/en/tutorial/Archipelago/nonexistent")
        assert response.status_code == 404

    def test_unknown_game_404s(self, client):
        response = client.get("/learn/en/tutorial/NoSuchGame/setup")
        assert response.status_code == 404

    def test_missing_lang_variant_404s(self, client):
        """Asking for a language whose file doesn't exist on disk 404s
        rather than falling back to English.
        """
        response = client.get("/learn/xx/tutorial/Archipelago/setup")
        assert response.status_code == 404
