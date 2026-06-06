"""Regression tests for scanning custom_worlds/ into the in-memory GameIndex.

custom_worlds are apworld **zip files**: on launch they must be scanned, their
manifest read (never imported), and each handed to ``GameIndex.add_game`` so it
lands in the search index and a user can find it by name -- and it must *remain*
there. This has regressed repeatedly, so the guarantees are pinned here:

  * a stray non-world file (e.g. a README.txt) in custom_worlds/ must not abort
    the scan;
  * an apworld dropped in custom_worlds/ is registered via ``GameIndex.add_game``
    so it is searchable by name (the launcher resolves its game list through
    ``GameIndex.search``) and resolvable module<->name;
  * the world stays registered across a second scan (idempotent); and
  * the scan never imports the world module -- only the zip manifest is read.
"""
import importlib
import json
import sys
import zipfile

import pytest

import ModuleUpdate
import Utils
from mwgg_igdb import GameIndex


def _make_apworld(path, game_name: str) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("archipelago.json", json.dumps({"game": game_name, "compatible_version": 5}))


@pytest.fixture(autouse=True)
def _restore_game_index():
    """Snapshot the GameIndex singleton and restore it after each test.

    The index is a process-global singleton seeded with every shipped world in
    test/__init__.py; restoring keeps those available during the test while
    preventing a test's custom-world additions from leaking into the rest of the
    suite. Containers are copied (deep for the search index, whose values are
    sets the tests mutate in place) and restored via clear()+update() so the
    singleton's dict identities are preserved.
    """
    games = dict(GameIndex._games)
    game_names = dict(GameIndex._game_names)
    module_to_name = dict(GameIndex._module_to_name)
    search_index = {key: set(slugs) for key, slugs in GameIndex._search_index.items()}
    try:
        yield
    finally:
        for live, snapshot in (
            (GameIndex._games, games),
            (GameIndex._game_names, game_names),
            (GameIndex._module_to_name, module_to_name),
            (GameIndex._search_index, search_index),
        ):
            live.clear()
            live.update(snapshot)


def test_register_custom_worlds_skips_readme_and_registers_apworld(tmp_path, monkeypatch):
    (tmp_path / "README.txt").write_text("Drop your apworlds here.\n")
    _make_apworld(tmp_path / "test_custom.apworld", "Test Custom Game")
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    found = Utils.register_custom_worlds()  # must not raise on README.txt

    assert "test_custom" in found
    assert GameIndex.get_game_name_for_module("test_custom") == "Test Custom Game"


def test_discover_returns_none_for_stray_file(tmp_path):
    readme = tmp_path / "README.txt"
    readme.write_text("not a world")
    assert Utils.discover_custom_world_module(readme) is None


def test_register_custom_worlds_tolerates_missing_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path / "does_not_exist")
    assert Utils.register_custom_worlds() == []


def test_custom_apworld_scanned_indexed_and_searchable(tmp_path, monkeypatch):
    """End-to-end launch contract: an apworld in custom_worlds/ is scanned, added
    to the index (searchable by name, resolvable both ways), stays after a rescan,
    is surfaced by get_available_worlds(), and is never imported."""
    slug = "test_custom_selectable"
    # Name words deliberately disjoint from the slug, so search() hits prove the
    # *name* was indexed (not merely the slug derived from the filename).
    name = "Quest For The Crystal"
    (tmp_path / "README.txt").write_text("Drop your apworlds here.\n")
    _make_apworld(tmp_path / f"{slug}.apworld", name)
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    # apworlds are zip files: the scan must read the manifest, never import the
    # world. Record any importlib.import_module call to catch a regression that
    # starts importing worlds.<slug> (the legit `from mwgg_igdb import ...` /
    # `from APContainer import ...` go through __import__, not this seam).
    assert f"worlds.{slug}" not in sys.modules
    imported: list[str] = []
    real_import_module = importlib.import_module

    def _spy_import_module(module_name, *args, **kwargs):
        imported.append(module_name)
        return real_import_module(module_name, *args, **kwargs)

    monkeypatch.setattr(importlib, "import_module", _spy_import_module)

    found = Utils.register_custom_worlds()

    assert slug in found                       # scanned
    assert "README" not in found               # stray file skipped, not aborting the scan

    # Added to the index and resolvable both ways.
    assert slug in GameIndex.get_all_games()
    assert GameIndex.get_game_name_for_module(slug) == name
    assert GameIndex.get_module_for_game(name) == slug

    # Searchable by name -- the launcher resolves its typed query through search().
    assert slug in GameIndex.search("crystal")   # a name word absent from the slug
    assert slug in GameIndex.search(name)

    # Never imported the world module.
    assert f"worlds.{slug}" not in sys.modules
    assert not any(m == f"worlds.{slug}" or m.startswith(f"worlds.{slug}.") for m in imported)

    # Remains after a second scan: idempotent, no duplicate growth, no raise.
    count_before = len(GameIndex.get_all_games())
    found_again = Utils.register_custom_worlds()
    assert slug in found_again
    assert slug in GameIndex.search("crystal")
    assert len(GameIndex.get_all_games()) == count_before

    # get_available_worlds() unions custom worlds with on-disk worlds. Stub out the
    # uv-backed find_world_modules so the test is hermetic and the union is provable.
    monkeypatch.setattr(ModuleUpdate, "find_world_modules", lambda: {"sentinel_world"})
    available = Utils.get_available_worlds()
    assert "sentinel_world" in available       # union preserved
    assert slug in available                   # custom world surfaced as selectable


def test_add_game_indexes_into_search_index():
    """add_game must place a world in the search index so a user can search for it
    by name -- pinned independently of the scan plumbing. The name words are
    disjoint from the slug so a hit proves the name itself was indexed."""
    GameIndex.add_game("probe_widget", {"game_name": "Galaxy Explorer"})

    assert "probe_widget" in GameIndex.search("galaxy")
    assert "probe_widget" in GameIndex.search("explorer")
    assert GameIndex.get_module_for_game("Galaxy Explorer") == "probe_widget"
