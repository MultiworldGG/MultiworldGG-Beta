"""Webhost routing tests; add new routing/redirect tests here.

Covers WebHostLib.short_id (generator, normalization, well-formedness check,
assignment with collision retry), the ``/r/<short>`` short-room route, the
canonical ``/learn/<lang>/tutorial/<game>/<file>`` route plus the
``_split_tutorial_file`` helper that powers the legacy redirects, and the
/play and /learn hub pages. test_route_redirects.py (the route-rename
redirect matrix) merges here later.

The tutorial handler reads from ``static/generated/docs/<game>/<file>_<lang>.md``,
which is populated by ``copy_tutorials_files_to_static`` at app startup. The
session-scoped ``app`` fixture runs that copy step once (via ``get_app``), so
the on-disk Archipelago tutorial files (``setup_en.md`` etc.) are available.
"""
from __future__ import annotations

import pathlib
import shutil
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import quote

import pytest
from werkzeug.utils import secure_filename

from BaseClasses import Tutorial
from WebHostLib import to_url
from WebHostLib.misc import _resolve_setup_tutorial, _split_tutorial_file
from WebHostLib.short_id import (
    ALPHABET,
    SHORT_ID_LENGTH,
    ShortIDExhaustedError,
    assign_short_id,
    generate_short_id,
    is_well_formed,
    normalize_short_id,
)
from worlds.AutoWorld import AutoWorldRegister

pytestmark = pytest.mark.usefixtures("_wipe_rooms_after_test")


# ---------------------------------------------------------------------------
# short_id: alphabet invariants
# ---------------------------------------------------------------------------

class TestAlphabet:
    def test_alphabet_is_canonical_crockford_base32(self):
        """The alphabet must be exactly the 32-symbol Crockford base32 set,
        in order: digits 0-9 then A-Z minus I, L, O, U. A base32 alphabet is
        only correct if all 32 symbols are distinct, so also pin the distinct
        count (a duplicated symbol would keep ``len`` at 32 yet break decoding).
        """
        expected = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
        assert ALPHABET == expected
        assert len(ALPHABET) == 32
        assert len(set(ALPHABET)) == 32

    def test_alphabet_excludes_i_l_o_u(self):
        """Crockford convention: I, L, O, U are excluded."""
        for excluded in ("I", "L", "O", "U"):
            assert excluded not in ALPHABET, f"{excluded} should be excluded"

    def test_alphabet_uppercase_only(self):
        assert ALPHABET == ALPHABET.upper()

    def test_short_id_length_is_six_and_is_enforced(self):
        """The configured length is 6, and that length is actually the one
        the behavior enforces: ``generate_short_id`` emits 6-char IDs and
        ``is_well_formed`` accepts exactly 6 chars while rejecting 5 and 7.
        Ties the named constant to the concrete value *and* to observable
        behavior, so changing the length (or the generation loop) is caught.
        """
        assert SHORT_ID_LENGTH == 6
        assert len(generate_short_id()) == 6
        sample = generate_short_id()
        assert is_well_formed(sample)
        assert not is_well_formed(sample[:5])
        assert not is_well_formed(sample + "A")


# ---------------------------------------------------------------------------
# short_id: generate_short_id
# ---------------------------------------------------------------------------

class TestGenerate:
    def test_correct_length(self):
        for _ in range(100):
            assert len(generate_short_id()) == SHORT_ID_LENGTH

    def test_only_uses_alphabet(self):
        valid_chars = set(ALPHABET)
        for _ in range(100):
            generated = generate_short_id()
            assert all(c in valid_chars for c in generated), (
                f"Generated {generated!r} contains invalid characters"
            )

    def test_outputs_are_uppercase(self):
        for _ in range(100):
            generated = generate_short_id()
            assert generated == generated.upper()

    def test_outputs_are_different(self):
        """100 generations should not all be the same. Sanity check
        that we're using random and not, e.g., a constant."""
        samples = {generate_short_id() for _ in range(100)}
        # With 32^6 namespace, getting 100 dupes in 100 draws is
        # vanishingly improbable. Expect close to 100 unique values.
        assert len(samples) >= 95


# ---------------------------------------------------------------------------
# short_id: normalize_short_id
# ---------------------------------------------------------------------------

class TestNormalize:
    @pytest.mark.parametrize("raw, expected", [
        ("K7M3QX", "K7M3QX"),
        ("k7m3qx", "K7M3QX"),
        ("K7m3Qx", "K7M3QX"),
    ])
    def test_case_insensitive(self, raw, expected):
        assert normalize_short_id(raw) == expected

    @pytest.mark.parametrize("raw, expected", [
        ("I00000", "100000"),  # I -> 1
        ("i00000", "100000"),  # lowercase i -> 1
        ("L00000", "100000"),  # L -> 1
        ("l00000", "100000"),  # lowercase l -> 1
        ("O00000", "000000"),  # O -> 0
        ("o00000", "000000"),  # lowercase o -> 0
    ])
    def test_ambiguous_char_substitution(self, raw, expected):
        assert normalize_short_id(raw) == expected

    def test_combined_normalization(self):
        """Mixed case + ambiguous chars: all handled in one pass."""
        # User typed lowercase i, l, o; expected canonical 1, 1, 0
        assert normalize_short_id("ilOabc") == "110ABC"

    def test_no_change_for_canonical(self):
        canonical = "K7M3QX"
        assert normalize_short_id(canonical) == canonical


# ---------------------------------------------------------------------------
# short_id: is_well_formed
# ---------------------------------------------------------------------------

class TestIsWellFormed:
    def test_accepts_canonical_short_id(self):
        assert is_well_formed("K7M3QX")

    def test_rejects_too_short(self):
        assert not is_well_formed("ABC")

    def test_rejects_too_long(self):
        assert not is_well_formed("K7M3QXEXTRA")

    def test_rejects_invalid_characters(self):
        # I, L, O, U should never appear in well-formed canonical IDs
        assert not is_well_formed("IIIIIII"[:6])
        assert not is_well_formed("LLLLLL")
        assert not is_well_formed("OOOOOO")
        assert not is_well_formed("UUUUUU")

    def test_rejects_lowercase(self):
        """Well-formedness is the canonical form check."""
        assert not is_well_formed("k7m3qx")


# ---------------------------------------------------------------------------
# short_id: assign_short_id (requires DB)
# ---------------------------------------------------------------------------

class TestAssign:
    def test_assigns_value_to_room(self, db_session, room_factory):
        room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, room)
        assert room.short_id == assigned
        assert len(assigned) == SHORT_ID_LENGTH

    def test_returns_the_assigned_value(self, db_session, room_factory):
        room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, room)
        assert assigned is not None
        assert is_well_formed(assigned)

    def test_avoids_existing_short_ids(self, db_session, room_factory):
        existing = room_factory(short_id="EXIST1")
        new_room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, new_room)
        assert assigned != "EXIST1"

    def test_retries_on_collision(self, db_session, room_factory):
        """When the first candidate collides, generate is called again
        until a unique one is produced."""
        # Pre-create rooms with known short_ids
        room_factory(short_id="AAAAAA")
        room_factory(short_id="BBBBBB")

        with patch(
            "WebHostLib.short_id.generate_short_id",
            side_effect=["AAAAAA", "BBBBBB", "CCCCCC"],
        ) as mock_gen:
            new_room = room_factory(short_id=None)
            assigned = assign_short_id(db_session, new_room)
            assert assigned == "CCCCCC"
            assert mock_gen.call_count == 3

    def test_raises_when_all_attempts_collide(self, db_session, room_factory):
        """If every candidate from generate collides, raise rather
        than loop forever."""
        room_factory(short_id="AAAAAA")
        with patch(
            "WebHostLib.short_id.generate_short_id",
            return_value="AAAAAA",
        ):
            new_room = room_factory(short_id=None)
            with pytest.raises(ShortIDExhaustedError):
                assign_short_id(db_session, new_room, max_attempts=3)

    def test_respects_max_attempts_argument(self, db_session, room_factory):
        """The retry loop honors the max_attempts kwarg."""
        room_factory(short_id="AAAAAA")
        with patch(
            "WebHostLib.short_id.generate_short_id",
            return_value="AAAAAA",
        ) as mock_gen:
            new_room = room_factory(short_id=None)
            with pytest.raises(ShortIDExhaustedError):
                assign_short_id(db_session, new_room, max_attempts=5)
            assert mock_gen.call_count == 5


# ---------------------------------------------------------------------------
# /r/<short>: basic resolution
# ---------------------------------------------------------------------------

class TestShortRoomRedirect:
    def test_resolves_to_canonical_room_url(self, client, room_factory):
        room = room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=False)

        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )

    def test_uses_301_not_302(self, client, room_factory):
        """The short->canonical mapping never changes once created, so
        301 (permanent) is correct. Discord and browsers cache 301s
        aggressively."""
        room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=False)
        assert response.status_code == 301

    def test_following_redirect_loads_room_page(self, client, room_factory):
        """Round-trip: hit /r/, follow the redirect, get the actual
        room page."""
        room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=True)
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# /r/<short>: case insensitivity (Crockford convention)
# ---------------------------------------------------------------------------

class TestCaseInsensitivity:
    @pytest.mark.parametrize("typed", [
        "K7M3QX",
        "k7m3qx",
        "K7m3Qx",
        "k7M3qX",
    ])
    def test_resolves_regardless_of_case(self, client, room_factory, typed):
        """All case variants of the canonical short_id should resolve."""
        room = room_factory(short_id="K7M3QX")
        response = client.get(f"/r/{typed}", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )


# ---------------------------------------------------------------------------
# /r/<short>: ambiguous character substitution
# ---------------------------------------------------------------------------

class TestAmbiguousChars:
    """Crockford convention: I/L -> 1, O -> 0. Voice-shared codes survive
    listener typos. The stored canonical form never contains I/L/O/U."""

    @pytest.mark.parametrize("stored, typed", [
        pytest.param("1ABCDE", "IABCDE", id="uppercase_i_substitutes_for_1"),
        pytest.param("1ABCDE", "labcde", id="lowercase_l_substitutes_for_1"),
        pytest.param("0ABCDE", "OABCDE", id="uppercase_o_substitutes_for_0"),
        pytest.param("110ABC", "ILOABC", id="combined_substitutions"),
    ])
    def test_substituted_input_resolves(self, client, room_factory, stored, typed):
        room = room_factory(short_id=stored)
        response = client.get(f"/r/{typed}", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )


# ---------------------------------------------------------------------------
# /r/<short>: negative cases
# ---------------------------------------------------------------------------

class TestNotFound:
    @pytest.mark.parametrize("bad", [
        pytest.param("NOPATH", id="unknown_short_id"),
        # We don't auto-pad short input.
        pytest.param("AB", id="too_short"),
        pytest.param("K7M3QXEXTRA", id="too_long"),
    ])
    def test_unresolvable_input_404s(self, client, bad):
        response = client.get(f"/r/{bad}", follow_redirects=False)
        assert response.status_code == 404


def test_short_room_endpoint_registered(client):
    """The /r/ route must be registered in url_map. Catches the case
    where the blueprint or route decorator was missed during the merge."""
    from WebHostLib import app

    rules = [rule for rule in app.url_map.iter_rules()
             if rule.endpoint == "short_room"]
    assert len(rules) == 1, "short_room endpoint not registered"
    assert "/r/" in str(rules[0].rule)


# ---------------------------------------------------------------------------
# Tutorials: _split_tutorial_file
# ---------------------------------------------------------------------------

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
        - rpartition splits from the right, not the left.
        """
        assert _split_tutorial_file("advanced_settings_en") == (
            "advanced_settings", "en",
        )

    def test_custom_default_lang(self):
        assert _split_tutorial_file("intro", default_lang="fr") == ("intro", "fr")


# ---------------------------------------------------------------------------
# Tutorials: canonical /learn/<lang>/tutorial/<game>/<file> route
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tutorials: "setup" aliases to the world's real primary guide
# ---------------------------------------------------------------------------

ALIAS_GAME = "Setup Alias Test Game!"
ALIAS_GAME_URL = quote(ALIAS_GAME, safe="")


def _tutorial(tutorial_name: str, file_name: str) -> Tutorial:
    return Tutorial(tutorial_name, "A guide.", "English", file_name, "unused", ["Nobody"])


def _stub_world(tutorials: list[Tutorial]) -> SimpleNamespace:
    return SimpleNamespace(
        game=ALIAS_GAME,
        hidden=False,
        web=SimpleNamespace(tutorials=tutorials, theme="grass", display_name=ALIAS_GAME),
    )


@pytest.fixture
def alias_world(tmp_path):
    def _register(tutorials: list[Tutorial], on_disk: list[str]):
        for file_name in on_disk:
            (tmp_path / file_name).write_text("# Guide\n\nBody.\n", encoding="utf-8")
        return patch.dict(AutoWorldRegister.world_types, {ALIAS_GAME: _stub_world(tutorials)})
    return _register


class TestResolveSetupTutorial:
    def test_prefers_a_setup_ish_tutorial_name(self, alias_world, tmp_path):
        tutorials = [_tutorial("Plando Guide", "plando_en.md"),
                     _tutorial("Multiworld Setup Guide", "multiworld_en.md")]
        with alias_world(tutorials, ["plando_en.md", "multiworld_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) == ("multiworld", "en")

    def test_first_setup_ish_name_wins(self, alias_world, tmp_path):
        """A Link to the Past's shape: "MSU-1 Setup Guide" matches too."""
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_en.md"),
                     _tutorial("MSU-1 Setup Guide", "msu1_en.md"),
                     _tutorial("Plando Guide", "plando_en.md")]
        with alias_world(tutorials, ["multiworld_en.md", "msu1_en.md", "plando_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) == ("multiworld", "en")

    def test_matches_start_guide(self, alias_world, tmp_path):
        with alias_world([_tutorial("Start Guide", "guide_en.md")], ["guide_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) == ("guide", "en")

    def test_falls_back_to_first_tutorial_when_no_name_matches(self, alias_world, tmp_path):
        tutorials = [_tutorial("How To Play", "howto_en.md"), _tutorial("Plando Guide", "plando_en.md")]
        with alias_world(tutorials, ["howto_en.md", "plando_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) == ("howto", "en")

    def test_prefers_the_requested_language(self, alias_world, tmp_path):
        tutorials = [_tutorial("Setup Guide", "guide_en.md"),
                     _tutorial("Guide d installation", "guide_fr.md")]
        with alias_world(tutorials, ["guide_en.md", "guide_fr.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "fr", str(tmp_path)) == ("guide", "fr")

    def test_crosses_languages_only_when_the_requested_one_has_none(self, alias_world, tmp_path):
        tutorials = [_tutorial("Setup Guide", "guide_en.md")]
        with alias_world(tutorials, ["guide_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "de", str(tmp_path)) == ("guide", "en")

    def test_skips_candidates_with_no_file_on_disk(self, alias_world, tmp_path):
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_en.md"),
                     _tutorial("Setup Guide", "guide_en.md")]
        with alias_world(tutorials, ["guide_en.md"]):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) == ("guide", "en")

    def test_returns_none_when_nothing_is_on_disk(self, alias_world, tmp_path):
        with alias_world([_tutorial("Setup Guide", "guide_en.md")], []):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) is None

    def test_returns_none_for_unknown_game(self, tmp_path):
        assert _resolve_setup_tutorial("No Such Game", "en", str(tmp_path)) is None

    def test_returns_none_when_world_declares_no_tutorials(self, alias_world, tmp_path):
        with alias_world([], []):
            assert _resolve_setup_tutorial(ALIAS_GAME, "en", str(tmp_path)) is None


class TestSetupAliasRoute:
    """One URL per case; ``@cache.cached()`` would let one answer another."""

    @pytest.fixture
    def docs_dir(self, app):
        path = pathlib.Path(app.static_folder) / "generated" / "docs" / secure_filename(ALIAS_GAME)
        path.mkdir(parents=True, exist_ok=True)
        yield path
        shutil.rmtree(path, ignore_errors=True)

    @pytest.fixture
    def alias_route_world(self, docs_dir):
        def _register(tutorials: list[Tutorial], on_disk: list[str]):
            for file_name in on_disk:
                (docs_dir / file_name).write_text("# Guide\n\nBody.\n", encoding="utf-8")
            return patch.dict(AutoWorldRegister.world_types, {ALIAS_GAME: _stub_world(tutorials)})
        return _register

    def test_missing_setup_redirects_to_the_real_guide(self, client, alias_route_world):
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_en.md")]
        with alias_route_world(tutorials, ["multiworld_en.md"]):
            response = client.get(f"/learn/en/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=False)
            assert response.status_code == 302
            assert response.headers["Location"].endswith("/multiworld")

    def test_redirect_lands_on_a_rendered_page(self, client, alias_route_world):
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_fr.md")]
        with alias_route_world(tutorials, ["multiworld_fr.md"]):
            response = client.get(f"/learn/fr/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=True)
            assert response.status_code == 200
            assert b"<html" in response.data.lower() or b"<!doctype" in response.data.lower()

    def test_other_missing_files_still_404(self, client, alias_route_world):
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_en.md")]
        with alias_route_world(tutorials, ["multiworld_en.md"]):
            response = client.get(f"/learn/en/tutorial/{ALIAS_GAME_URL}/setpu")
            assert response.status_code == 404

    def test_existing_setup_file_is_served_not_redirected(self, client, alias_route_world):
        tutorials = [_tutorial("Setup Guide", "setup_de.md"), _tutorial("Plando Guide", "plando_de.md")]
        with alias_route_world(tutorials, ["setup_de.md", "plando_de.md"]):
            response = client.get(f"/learn/de/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=False)
            assert response.status_code == 200

    def test_unknown_language_redirects_to_one_that_has_the_guide(self, client, alias_route_world):
        with alias_route_world([_tutorial("Setup Guide", "setup_pt.md")], ["setup_pt.md"]):
            response = client.get(f"/learn/xx/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=False)
            assert response.status_code == 302
            assert "/learn/pt/tutorial/" in response.headers["Location"]
            assert response.headers["Location"].endswith("/setup")

    def test_redirect_is_cached_under_the_requested_path(self, client, alias_route_world):
        """The repeat runs with the world unregistered: only the cache can answer."""
        tutorials = [_tutorial("Multiworld Setup Guide", "multiworld_es.md")]
        with alias_route_world(tutorials, ["multiworld_es.md"]):
            first = client.get(f"/learn/es/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=False)
        second = client.get(f"/learn/es/tutorial/{ALIAS_GAME_URL}/setup", follow_redirects=False)
        assert first.status_code == 302
        assert second.status_code == 302
        assert first.headers["Location"] == second.headers["Location"]


# ---------------------------------------------------------------------------
# Hub pages: /play and /learn
# ---------------------------------------------------------------------------

def test_play_hub_renders(client):
    response = client.get("/play")
    assert response.status_code == 200


def test_learn_hub_renders(client):
    # /learn is a legacy 301 to the locale-prefixed canonical hub (/learn/en).
    response = client.get("/learn", follow_redirects=True)
    assert response.status_code == 200


def test_tutorial_landing_renders(client):
    # /learn/tutorials is a legacy 301 to /learn/en/tutorials.
    response = client.get("/learn/tutorials", follow_redirects=True)
    assert response.status_code == 200


def test_tutorial_legacy_redirect_lands_on_tutorial_landing(client):
    response = client.get("/tutorial", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/en/tutorials")
