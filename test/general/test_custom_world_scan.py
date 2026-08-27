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
import importlib.metadata
import json
import logging
import sys
import zipfile
from pathlib import Path

import pytest

import LauncherComponents as lc
import ModuleUpdate
import Utils
from mwgg_igdb import GameIndex


def _make_apworld(path, game_name: str, components: "list | None" = None,
                  extra_members: "dict[str, bytes] | None" = None) -> None:
    slug = Path(path).stem
    manifest: dict = {"game": game_name, "compatible_version": 5}
    if components is not None:
        manifest["components"] = components
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(f"{slug}/archipelago.json", json.dumps(manifest))
        for member, data in (extra_members or {}).items():
            zf.writestr(f"{slug}/{member}", data)


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


def test_custom_worlds_dir_is_executable_folder_even_when_frozen(monkeypatch):
    """custom_worlds must resolve next to the executable / source checkout -- the
    upstream location, and where users actually drop apworlds -- never to
    write_path()/AppData. Splitting the scan dir from the launch dir is what makes
    custom worlds silently un-selectable in frozen builds.

    The is_frozen() mock is a tripwire: it has no effect on the current resolver,
    but if anyone reintroduces an `if is_frozen(): write_path(...)` branch this test
    fails because the resolved dir would jump to write_path under the mock.
    """
    from BaseUtils import write_path
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)

    resolved = ModuleUpdate._resolve_custom_worlds_dir()

    assert resolved == Path(ModuleUpdate.local_path("custom_worlds"))
    assert resolved != Path(write_path("custom_worlds"))


def test_world_tool_entries_finds_declared_tools(tmp_path, monkeypatch):
    _make_apworld(tmp_path / "toolworld.apworld", "Tool World", components=[
        {"name": "Tool World Client", "type": "client"},
        {"name": "Tool World Manager", "type": "adjuster", "description": "Edit things."},
        {"name": "Tool World Spriter", "type": "tool"},
    ])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    entries = lc.world_tool_entries()

    # client entries are the game list's business -- only tool/adjuster get cards
    assert [(e.module, e.world_name, e.name, e.type) for e in entries] == [
        ("toolworld", "Tool World", "Tool World Manager", "adjuster"),
        ("toolworld", "Tool World", "Tool World Spriter", "tool"),
    ]
    assert entries[0].description == "Edit things."
    assert entries[1].description == ""


def test_world_manifest_components_includes_clients(tmp_path, monkeypatch):
    """world_manifest_components returns all declared types (the play page's
    per-game strip needs clients too); the world_tool_entries wrapper keeps
    its historical tool/adjuster-only view."""
    _make_apworld(tmp_path / "toolworld.apworld", "Tool World", components=[
        {"name": "Tool World Client", "type": "client"},
        {"name": "Tool World Manager", "type": "adjuster", "description": "Edit things."},
        {"name": "Tool World Spriter", "type": "tool"},
    ])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    entries = lc.world_manifest_components()

    assert [(e.module, e.name, e.type) for e in entries] == [
        ("toolworld", "Tool World Client", "client"),
        ("toolworld", "Tool World Manager", "adjuster"),
        ("toolworld", "Tool World Spriter", "tool"),
    ]
    assert [(e.name, e.type) for e in lc.world_tool_entries()] == [
        ("Tool World Manager", "adjuster"),
        ("Tool World Spriter", "tool"),
    ]


def test_world_manifest_components_include_filter(tmp_path, monkeypatch):
    _make_apworld(tmp_path / "toolworld.apworld", "Tool World", components=[
        {"name": "Tool World Client", "type": "client"},
        {"name": "Tool World Spriter", "type": "tool"},
    ])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    entries = lc.world_manifest_components(include=("client",))

    assert [(e.name, e.type) for e in entries] == [("Tool World Client", "client")]


def test_world_manifest_components_never_imports_world_module(tmp_path, monkeypatch):
    slug = "manifestworld_noimport"
    _make_apworld(tmp_path / f"{slug}.apworld", "No Import World", components=[
        {"name": "No Import Client", "type": "client"},
        {"name": "No Import Tool", "type": "tool"},
    ])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    assert f"worlds.{slug}" not in sys.modules
    imported: list[str] = []
    real_import_module = importlib.import_module

    def _spy_import_module(module_name, *args, **kwargs):
        imported.append(module_name)
        return real_import_module(module_name, *args, **kwargs)

    monkeypatch.setattr(importlib, "import_module", _spy_import_module)

    entries = lc.world_manifest_components()

    assert [e.name for e in entries] == ["No Import Client", "No Import Tool"]
    assert f"worlds.{slug}" not in sys.modules
    assert not any(m == f"worlds.{slug}" or m.startswith(f"worlds.{slug}.") for m in imported)


def test_world_tool_entries_skips_malformed_entries_keeps_valid(tmp_path, monkeypatch, caplog):
    _make_apworld(tmp_path / "toolworld.apworld", "Tool World", components=[
        "not-a-mapping",
        {"type": "tool"},                     # missing name
        {"name": "Weird", "type": "banana"},  # unknown type
        {"name": "Typeless"},                 # missing type
        {"name": "Survivor", "type": "tool"},
    ])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    with caplog.at_level(logging.WARNING):
        entries = lc.world_tool_entries()

    assert [e.name for e in entries] == ["Survivor"]
    assert len(caplog.records) == 4


def test_world_tool_entries_survives_corrupt_zip(tmp_path, monkeypatch, caplog):
    (tmp_path / "broken.apworld").write_bytes(b"this is not a zip")
    _make_apworld(tmp_path / "goodworld.apworld", "Good World",
                  components=[{"name": "Good Tool", "type": "tool"}])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    with caplog.at_level(logging.WARNING):
        entries = lc.world_tool_entries()

    assert [e.name for e in entries] == ["Good Tool"]
    assert any("broken.apworld" in record.message for record in caplog.records)


def test_world_tool_entries_never_imports_world_module(tmp_path, monkeypatch):
    slug = "toolworld_noimport"
    _make_apworld(tmp_path / f"{slug}.apworld", "No Import World",
                  components=[{"name": "No Import Tool", "type": "tool"}])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)

    assert f"worlds.{slug}" not in sys.modules
    imported: list[str] = []
    real_import_module = importlib.import_module

    def _spy_import_module(module_name, *args, **kwargs):
        imported.append(module_name)
        return real_import_module(module_name, *args, **kwargs)

    monkeypatch.setattr(importlib, "import_module", _spy_import_module)

    entries = lc.world_tool_entries()

    assert [e.name for e in entries] == ["No Import Tool"]
    assert f"worlds.{slug}" not in sys.modules
    assert not any(m == f"worlds.{slug}" or m.startswith(f"worlds.{slug}.") for m in imported)


def test_world_tool_entries_dedups_custom_over_index(tmp_path, monkeypatch):
    """A slug present both as a custom apworld and a GameIndex entry must only
    contribute the custom manifest's components (custom wins)."""
    slug = "dedup_world"
    _make_apworld(tmp_path / f"{slug}.apworld", "Dedup World",
                  components=[{"name": "Custom Tool", "type": "tool"}])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)
    GameIndex.add_game(slug, {"game_name": "Dedup World",
                              "components": [{"name": "Index Tool", "type": "tool"}]})
    # Pretend the indexed dist is installed; the custom apworld must still win.
    real_distribution = importlib.metadata.distribution
    monkeypatch.setattr(importlib.metadata, "distribution",
                        lambda name: object() if name == f"worlds.{slug}" else real_distribution(name))

    entries = lc.world_tool_entries()

    names = [e.name for e in entries]
    assert "Custom Tool" in names
    assert "Index Tool" not in names


def test_world_tool_entries_reads_index_entries_only_when_installed(tmp_path, monkeypatch):
    """GameIndex entries carrying `components` surface only for installed dists,
    probed per slug -- never via the uv-backed find_world_modules."""
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)  # empty dir
    GameIndex.add_game("installed_index_world",
                       {"game_name": "Installed Index World",
                        "components": [{"name": "Indexed Tool", "type": "tool"}]})
    GameIndex.add_game("absent_index_world",
                       {"game_name": "Absent Index World",
                        "components": [{"name": "Absent Tool", "type": "tool"}]})

    def fake_distribution(name):
        if name == "worlds.installed_index_world":
            return object()
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(importlib.metadata, "distribution", fake_distribution)

    def _fail_find_world_modules():
        raise AssertionError("world_tool_entries must not shell out via find_world_modules")

    monkeypatch.setattr(ModuleUpdate, "find_world_modules", _fail_find_world_modules)

    entries = lc.world_tool_entries()

    names = [e.name for e in entries]
    assert "Indexed Tool" in names
    assert "Absent Tool" not in names
    indexed = next(e for e in entries if e.name == "Indexed Tool")
    assert indexed.module == "installed_index_world"
    assert indexed.world_name == "Installed Index World"


def test_add_game_indexes_into_search_index():
    """add_game must place a world in the search index so a user can search for it
    by name -- pinned independently of the scan plumbing. The name words are
    disjoint from the slug so a hit proves the name itself was indexed."""
    GameIndex.add_game("probe_widget", {"game_name": "Galaxy Explorer"})

    assert "probe_widget" in GameIndex.search("galaxy")
    assert "probe_widget" in GameIndex.search("explorer")
    assert GameIndex.get_module_for_game("Galaxy Explorer") == "probe_widget"
