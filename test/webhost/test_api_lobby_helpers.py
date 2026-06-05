"""Unit tests pinning the pure helper behaviors in WebHostLib/api/lobby.py.

Each test name documents a non-obvious behavioral fact previously carried by an
inline comment or docstring in the source module.
"""
import json

from Utils import Version

from WebHostLib.api.lobby import (
    _extract_game_info,
    _has_name_template,
    _manual_game_segment,
    _safe_zip_name,
    _split_yaml_documents,
    _version_mismatch_direction,
)


def test_safe_zip_name_sanitizes_and_defaults_to_unnamed():
    # Allowed characters (word, whitespace, dot, parens, hyphen) survive.
    assert _safe_zip_name("My_Game (v1.2)-final") == "My_Game (v1.2)-final"
    # Disallowed characters become underscores.
    assert _safe_zip_name("a/b:c*d") == "a_b_c_d"
    # Surrounding whitespace is stripped.
    assert _safe_zip_name("  spaced  ") == "spaced"
    # Empty or whitespace-only input falls back to the literal "unnamed".
    assert _safe_zip_name("") == "unnamed"
    assert _safe_zip_name("   ") == "unnamed"
    # Disallowed chars map to underscores, which are NOT stripped, so an
    # all-invalid (non-whitespace) name stays as underscores, not "unnamed".
    assert _safe_zip_name("///") == "___"


def test_has_name_template_matches_player_and_number_placeholders():
    for token in ("{player}", "{PLAYER}", "{number}", "{NUMBER}"):
        assert _has_name_template(f"Slot{token}") is True
    # No placeholder -> False, and mixed/other casings are not matched.
    assert _has_name_template("PlainName") is False
    assert _has_name_template("{Player}") is False
    assert _has_name_template("{playerX}") is False


def test_manual_game_segment_extracts_first_segment_after_prefix():
    # First underscore-delimited segment after the "Manual_" prefix.
    assert _manual_game_segment("Manual_GameName_Player") == "GameName"
    assert _manual_game_segment("Manual_GameName") == "GameName"
    # Names not starting with "Manual_" yield an empty string.
    assert _manual_game_segment("GameName") == ""
    assert _manual_game_segment("manual_lowercase") == ""


def test_extract_game_info_bare_string_becomes_exact_constraint():
    bare = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    Clique: 1.2.3\n"
    assert _extract_game_info(bare) == ("Bob", "Clique", json.dumps({"exact": "1.2.3"}))

    # A dict constraint is encoded verbatim (min/max preserved).
    as_dict = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    Clique: {min: 1.0.0, max: 2.0.0}\n"
    name, game, requires_json = _extract_game_info(as_dict)
    assert (name, game) == ("Bob", "Clique")
    assert json.loads(requires_json) == {"min": "1.0.0", "max": "2.0.0"}

    # A constraint for a *different* game than the YAML's game is ignored.
    other_game = b"name: Bob\ngame: Clique\nrequires:\n  game:\n    NotClique: 1.2.3\n"
    assert _extract_game_info(other_game) == ("Bob", "Clique", None)

    # str input is accepted and returns the same shape as bytes.
    assert _extract_game_info("name: Bob\ngame: Clique\n") == ("Bob", "Clique", None)

    # No game present, or unparseable content, returns ('', '', None).
    assert _extract_game_info(b"name: Bob\n") == ("Bob", "", None)
    assert _extract_game_info(b": : not yaml [") == ("", "", None)


def test_version_mismatch_direction_exact_min_max_and_malformed():
    exact = lambda v: json.dumps({"exact": v})  # noqa: E731
    # exact: greater than server -> newer, less than -> older, equal -> None.
    assert _version_mismatch_direction(exact("1.2.3"), Version(1, 0, 0)) == "newer"
    assert _version_mismatch_direction(exact("1.0.0"), Version(1, 2, 3)) == "older"
    assert _version_mismatch_direction(exact("1.2.3"), Version(1, 2, 3)) is None

    # min: above server -> newer; satisfied -> None.
    assert _version_mismatch_direction(json.dumps({"min": "2.0.0"}), Version(1, 0, 0)) == "newer"
    assert _version_mismatch_direction(json.dumps({"min": "1.0.0"}), Version(1, 0, 0)) is None

    # max: below server -> older; satisfied -> None.
    assert _version_mismatch_direction(json.dumps({"max": "1.0.0"}), Version(2, 0, 0)) == "older"
    assert _version_mismatch_direction(json.dumps({"max": "3.0.0"}), Version(2, 0, 0)) is None

    # Malformed JSON yields None rather than raising.
    assert _version_mismatch_direction("not json", Version(1, 0, 0)) is None


def test_split_yaml_documents_single_unchanged_multi_indexed_from_one():
    # Single-document content is returned unchanged under its own filename.
    single = b"name: Solo\ngame: Clique\n"
    assert _split_yaml_documents("solo.yaml", single) == {"solo.yaml": single}

    # Multi-document content splits into 1-indexed {base}_N{ext} entries.
    multi = b"name: One\ngame: Clique\n---\nname: Two\ngame: Clique\n"
    out = _split_yaml_documents("party.yaml", multi)
    assert sorted(out.keys()) == ["party_1.yaml", "party_2.yaml"]
    assert b"One" in out["party_1.yaml"]
    assert b"Two" in out["party_2.yaml"]

    # Missing extension defaults to .yaml on the split entries.
    out_noext = _split_yaml_documents("party", multi)
    assert sorted(out_noext.keys()) == ["party_1.yaml", "party_2.yaml"]
