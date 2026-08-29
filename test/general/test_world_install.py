"""World install/update tests (ModuleUpdate, custom_worlds scan, install_worlds, upgrader, set_game_names, Updater); add new world-install tests here."""

import datetime
import importlib
import importlib.metadata
import importlib.util
import json
import logging
import os
import subprocess
import sys
import textwrap
import types
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import pytest

import LauncherComponents as lc
import ModuleUpdate
import MultiWorld
import Updater
import Utils
from mwgg_igdb import GameIndex

REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Pure / filesystem-only ModuleUpdate.py helpers -- no real network or
# pip/uv runs. ModuleUpdate keeps module-level globals (update_ran, the
# resolved variant trio, the uv-resolution cache); every test that flips
# one restores it so collection order can't leak state. test/__init__.py
# forces update_ran=True.
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# _parse_url_requirement
# --------------------------------------------------------------------------- #
def test_parse_url_requirement_tarball_to_pinned_spec():
    out = ModuleUpdate._parse_url_requirement(
        "https://github.com/owner/repo/archive/foo-1.2.3.tar.gz"
    )
    assert out == "foo==1.2.3"


def test_parse_url_requirement_zip_to_pinned_spec():
    out = ModuleUpdate._parse_url_requirement("https://example.com/dl/bar-0.9.zip")
    assert out == "bar==0.9"


def test_parse_url_requirement_at_in_filename_raises():
    # An '@' in the trailing filename means the version can't be deduced.
    with pytest.raises(ValueError):
        ModuleUpdate._parse_url_requirement("https://example.com/foo@1.0.zip")


def test_parse_url_requirement_unsplittable_returns_empty():
    # Only one '-' segment after suffix substitution -> ValueError -> "".
    assert ModuleUpdate._parse_url_requirement("https://example.com/noseparator.zip") == ""


# --------------------------------------------------------------------------- #
# _parse_custom_pep508_requirement
# --------------------------------------------------------------------------- #
def test_parse_custom_pep508_basic():
    out = ModuleUpdate._parse_custom_pep508_requirement(
        "mypackage @ git+https://example.com/x.git#1.2.3"
    )
    assert out == "mypackage==1.2.3"


def test_parse_custom_pep508_preserves_environment_marker():
    out = ModuleUpdate._parse_custom_pep508_requirement(
        "mypackage @ git+https://example.com/x.git#1.2.3 ; python_version >= '3.8'"
    )
    assert out == "mypackage==1.2.3; python_version >= '3.8'"


# --------------------------------------------------------------------------- #
# _module_location_tag
# --------------------------------------------------------------------------- #
def test_module_location_tag_extracts_wheel_version():
    url = (
        "https://github.com/o/r/releases/download/v1.4.2/"
        "mypkg-1.4.2-py3-none-any.whl#sha256=deadbeef"
    )
    assert ModuleUpdate._module_location_tag(url) == "1.4.2"


def test_module_location_tag_non_wheel_and_short_return_none():
    # Legacy git+...@ref URL (not a wheel) and a too-short wheel name both -> None.
    assert ModuleUpdate._module_location_tag("git+https://github.com/o/r@abc123") is None
    assert ModuleUpdate._module_location_tag("https://x/y/short-1.0.whl") is None
    assert ModuleUpdate._module_location_tag("") is None


# --------------------------------------------------------------------------- #
# _parse_variant_token
# --------------------------------------------------------------------------- #
def test_parse_variant_token_known_and_unknown():
    assert ModuleUpdate._parse_variant_token("mwgg_igdb") == "sixteen"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_twelve") == "twelve"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_nr") == "nr"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_bogus") is None
    assert ModuleUpdate._parse_variant_token("worlds.alttp") is None


# --------------------------------------------------------------------------- #
# _igdb_install_date / _igdb_upgraded_recently  (mtime-driven)
# --------------------------------------------------------------------------- #
def _fake_spec_for(path):
    return types.SimpleNamespace(origin=str(path))


def test_igdb_install_date_reads_file_mtime(tmp_path, monkeypatch):
    pkg = tmp_path / "mwgg_igdb.py"
    pkg.write_text("__variant__ = 'sixteen'\n")
    known = datetime.datetime(2021, 6, 15, 12, 0, 0).timestamp()
    os.utime(pkg, (known, known))
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: _fake_spec_for(pkg))

    assert ModuleUpdate._igdb_install_date() == datetime.date(2021, 6, 15)


def test_igdb_install_date_none_when_not_installed(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: None)
    assert ModuleUpdate._igdb_install_date() is None


def test_igdb_upgraded_recently_true_only_for_today(tmp_path, monkeypatch):
    pkg = tmp_path / "mwgg_igdb.py"
    pkg.write_text("x\n")
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: _fake_spec_for(pkg))

    now = datetime.datetime.now().timestamp()
    os.utime(pkg, (now, now))
    assert ModuleUpdate._igdb_upgraded_recently() is True

    old = datetime.datetime(2000, 1, 1).timestamp()
    os.utime(pkg, (old, old))
    assert ModuleUpdate._igdb_upgraded_recently() is False


# --------------------------------------------------------------------------- #
# _detect_installed_variant / _resolve_variant
# --------------------------------------------------------------------------- #
@pytest.fixture
def restore_variant_globals():
    """Snapshot/restore the resolved-variant trio + explicit-override sentinel."""
    saved = (
        ModuleUpdate._EXPLICIT_VARIANT,
        ModuleUpdate.MWGG_IGDB_VARIANT,
        ModuleUpdate.MWGG_IGDB_BRANCH,
        ModuleUpdate.MWGG_IGDB_GIT_URL,
    )
    yield
    (
        ModuleUpdate._EXPLICIT_VARIANT,
        ModuleUpdate.MWGG_IGDB_VARIANT,
        ModuleUpdate.MWGG_IGDB_BRANCH,
        ModuleUpdate.MWGG_IGDB_GIT_URL,
    ) = saved


def test_detect_installed_variant_reads_module_attr(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: object())
    fake_mod = types.ModuleType("mwgg_igdb")
    fake_mod.__variant__ = "twelve"
    monkeypatch.setitem(__import__("sys").modules, "mwgg_igdb", fake_mod)
    assert ModuleUpdate._detect_installed_variant() == "twelve"


def test_detect_installed_variant_rejects_unknown_value(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: object())
    fake_mod = types.ModuleType("mwgg_igdb")
    fake_mod.__variant__ = "not_a_real_variant"
    monkeypatch.setitem(__import__("sys").modules, "mwgg_igdb", fake_mod)
    assert ModuleUpdate._detect_installed_variant() is None


def test_detect_installed_variant_none_when_no_spec(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: None)
    assert ModuleUpdate._detect_installed_variant() is None


def test_resolve_variant_explicit_override_wins(monkeypatch, restore_variant_globals):
    # Even when detection would yield 'twelve', an explicit set_variant wins
    # and the derived globals are kept consistent.
    monkeypatch.setattr(ModuleUpdate, "_detect_installed_variant", lambda: "twelve")
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", "ao")

    assert ModuleUpdate._resolve_variant() == "ao"
    assert ModuleUpdate.MWGG_IGDB_VARIANT == "ao"
    assert ModuleUpdate.MWGG_IGDB_BRANCH == "game_index_ao"
    assert ModuleUpdate.MWGG_IGDB_GIT_URL == (
        "git+https://github.com/MultiworldGG/MultiworldGG-Index@game_index_ao"
    )


def test_resolve_variant_falls_back_to_default_when_undetectable(monkeypatch, restore_variant_globals):
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", None)
    monkeypatch.setattr(ModuleUpdate, "_detect_installed_variant", lambda: None)

    assert ModuleUpdate._resolve_variant() == ModuleUpdate.DEFAULT_MWGG_IGDB_VARIANT
    assert ModuleUpdate.MWGG_IGDB_BRANCH == f"game_index_{ModuleUpdate.DEFAULT_MWGG_IGDB_VARIANT}"


# --------------------------------------------------------------------------- #
# custom_worlds scan -> worlds_files["wheels"] / ["apworlds"]
# --------------------------------------------------------------------------- #
def test_custom_worlds_scan_populates_worlds_files(tmp_path, monkeypatch):
    """_scan_custom_worlds() collects every .whl and .apworld in custom_worlds_dir
    into the two RequirementsSets, guarded by `not update_ran`."""
    wheel = tmp_path / "worlds.example-1.0-py3-none-any.whl"
    apworld = tmp_path / "example.apworld"
    decoy = tmp_path / "README.txt"
    for f in (wheel, apworld, decoy):
        f.write_text("x")

    saved_update_ran = ModuleUpdate.update_ran
    saved_wheels = set(ModuleUpdate.worlds_files["wheels"])
    saved_apworlds = set(ModuleUpdate.worlds_files["apworlds"])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)
    try:
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.worlds_files["apworlds"].clear()
        ModuleUpdate.update_ran = False

        ModuleUpdate._scan_custom_worlds()

        assert ModuleUpdate.worlds_files["wheels"] == {str(wheel)}
        assert ModuleUpdate.worlds_files["apworlds"] == {str(apworld)}
        # The stray non-world file is collected into neither set.
        assert str(decoy) not in ModuleUpdate.worlds_files["wheels"]
        assert str(decoy) not in ModuleUpdate.worlds_files["apworlds"]

        # The update_ran guard short-circuits the scan (no re-collection after update).
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.update_ran = True
        ModuleUpdate._scan_custom_worlds()
        assert ModuleUpdate.worlds_files["wheels"] == set()
    finally:
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.worlds_files["wheels"].update(saved_wheels)
        ModuleUpdate.worlds_files["apworlds"].clear()
        ModuleUpdate.worlds_files["apworlds"].update(saved_apworlds)
        ModuleUpdate.update_ran = saved_update_ran


# --------------------------------------------------------------------------- #
# _uv_candidate_paths / _uv_run  (no real uv, no network)
# --------------------------------------------------------------------------- #
def test_uv_candidate_paths_includes_bare_uv_and_is_nonempty():
    cands = ModuleUpdate._uv_candidate_paths()
    assert isinstance(cands, list) and cands
    # PATH lookup ("uv") is always one of the candidates regardless of platform.
    assert any(str(c) == "uv" for c in cands)


@pytest.fixture
def reset_uv_resolution_cache():
    """_uv_run caches the resolved binary path / unavailability across calls."""
    saved = (ModuleUpdate._uv_resolved_path, ModuleUpdate._uv_unavailable)
    ModuleUpdate._uv_resolved_path = None
    ModuleUpdate._uv_unavailable = False
    yield
    ModuleUpdate._uv_resolved_path, ModuleUpdate._uv_unavailable = saved


def test_uv_run_constructs_candidate_plus_args_command(monkeypatch, reset_uv_resolution_cache):
    """_uv_run runs `<candidate> <args>` and caches the first usable candidate."""
    recorded = {}

    def fake_run(cmd, check=False, **kwargs):
        recorded["cmd"] = list(cmd)
        recorded["kwargs"] = kwargs
        return subprocess.CompletedProcess(cmd, 0, "ok-stdout", "")

    monkeypatch.setattr(ModuleUpdate, "_uv_candidate_paths", lambda: [ModuleUpdate.Path("uv")])
    monkeypatch.setattr(subprocess, "run", fake_run)

    result = ModuleUpdate._uv_run(["pip", "list"], timeout=12)

    assert result.returncode == 0
    assert result.stdout == "ok-stdout"
    # Command is candidate binary followed verbatim by the supplied args.
    assert recorded["cmd"] == [ModuleUpdate.Path("uv"), "pip", "list"]
    # Non-interactive: stdin is detached and the requested timeout is forwarded.
    assert recorded["kwargs"]["stdin"] is subprocess.DEVNULL
    assert recorded["kwargs"]["timeout"] == 12
    assert recorded["kwargs"]["capture_output"] is True
    # First usable candidate is cached for subsequent calls.
    assert ModuleUpdate._uv_resolved_path == ModuleUpdate.Path("uv")


def test_uv_run_falls_through_oserror_then_returns_127(monkeypatch, reset_uv_resolution_cache):
    """Every candidate raising OSError marks uv unavailable and returns a 127
    CompletedProcess instead of raising."""
    tried = []

    def fake_run(cmd, check=False, **kwargs):
        tried.append(cmd[0])
        raise OSError("no such uv")

    monkeypatch.setattr(
        ModuleUpdate,
        "_uv_candidate_paths",
        lambda: [ModuleUpdate.Path("uv-a"), ModuleUpdate.Path("uv-b")],
    )
    monkeypatch.setattr(subprocess, "run", fake_run)

    result = ModuleUpdate._uv_run(["pip", "list"])

    assert result.returncode == 127
    assert tried == [ModuleUpdate.Path("uv-a"), ModuleUpdate.Path("uv-b")]
    assert ModuleUpdate._uv_unavailable is True


def test_uv_run_short_circuits_when_unavailable(monkeypatch, reset_uv_resolution_cache):
    """Once uv is known-unavailable, _uv_run returns 127 without touching subprocess."""
    ModuleUpdate._uv_unavailable = True

    def explode(*a, **k):  # pragma: no cover - must not be called
        raise AssertionError("subprocess.run must not run when uv is unavailable")

    monkeypatch.setattr(subprocess, "run", explode)
    result = ModuleUpdate._uv_run(["pip", "list"])
    assert result.returncode == 127


def test_uv_pip_appends_python_target():
    cmd = ModuleUpdate._uv_pip("install", "somepkg", "--no-cache")
    assert cmd[0] == "pip"
    assert cmd[1:4] == ["install", "somepkg", "--no-cache"]
    # The interpreter is pinned via --python <python_cmd> as the trailing pair.
    assert cmd[-2] == "--python"
    assert cmd[-1] == str(ModuleUpdate.python_cmd)


# --------------------------------------------------------------------------- #
# First-launch race: a sys.path entry probed before it exists is None-cached
# in sys.path_importer_cache; only invalidate_caches() clears it.
# --------------------------------------------------------------------------- #
def test_missing_syspath_dir_hides_module_until_invalidated(tmp_path, monkeypatch):
    """Proves the actual Python import-cache pitfall the fix addresses (no
    mocks): a sys.path entry looked up before it exists on disk stays
    unimportable -- even after the directory and module are created --
    until invalidate_caches() runs."""
    site_dir = str(tmp_path / "site-packages")  # does not exist yet
    monkeypatch.syspath_prepend(site_dir)
    module_name = "mwgg_test_fresh_module_xyz"

    # Poison sys.path_importer_cache[site_dir] with None: looked up before it exists.
    assert importlib.util.find_spec(module_name) is None
    assert sys.path_importer_cache.get(site_dir) is None

    os.makedirs(site_dir)
    with open(os.path.join(site_dir, f"{module_name}.py"), "w") as f:
        f.write("value = 1\n")
    try:
        # The cached None verdict predates the files and is never rechecked.
        assert importlib.util.find_spec(module_name) is None

        importlib.invalidate_caches()
        assert importlib.util.find_spec(module_name) is not None
    finally:
        sys.modules.pop(module_name, None)


def test_bootstrap_fresh_venv_igdb_noop_when_venv_not_just_created(monkeypatch):
    monkeypatch.setattr(ModuleUpdate, "_venv_just_created", False)
    with mock.patch.object(ModuleUpdate, "install_mwgg_igdb") as install, \
            mock.patch.object(ModuleUpdate, "invalidate_caches") as invalidate:
        ModuleUpdate._bootstrap_fresh_venv_mwgg_igdb()
    install.assert_not_called()
    invalidate.assert_not_called()


def test_bootstrap_fresh_venv_igdb_installs_and_invalidates_when_just_created(monkeypatch):
    monkeypatch.setattr(ModuleUpdate, "_venv_just_created", True)
    with mock.patch.object(ModuleUpdate, "install_mwgg_igdb") as install, \
            mock.patch.object(ModuleUpdate, "invalidate_caches") as invalidate:
        ModuleUpdate._bootstrap_fresh_venv_mwgg_igdb()
    install.assert_called_once_with()
    invalidate.assert_called_once_with()


def test_register_custom_worlds_invalidates_import_caches(tmp_path, monkeypatch):
    """register_custom_worlds is one of the two first-launch call sites that
    import mwgg_igdb (via discover_custom_world_module); it must refresh the
    import cache before scanning so a just-installed mwgg_igdb is visible."""
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)
    with mock.patch.object(Utils.importlib, "invalidate_caches") as invalidate:
        Utils.register_custom_worlds()
    invalidate.assert_called_once_with()


# --------------------------------------------------------------------------- #
# custom_worlds/ scan into the in-memory GameIndex. custom_worlds are
# apworld zip files: on launch they must be scanned, their manifest read
# (never imported), and each handed to GameIndex.add_game so it lands in
# the search index and a user can find it by name -- and it must *remain*
# there. This has regressed repeatedly; the pinned guarantees:
#   * a stray non-world file (e.g. a README.txt) in custom_worlds/ must
#     not abort the scan;
#   * an apworld dropped in custom_worlds/ is registered via
#     GameIndex.add_game so it is searchable by name (the launcher resolves
#     its game list through GameIndex.search) and resolvable module<->name;
#   * the world stays registered across a second scan (idempotent); and
#   * the scan never imports the world module -- only the zip manifest is
#     read.
# The _restore_game_index fixture below is module-wide autouse, so every
# test in this module runs against a snapshotted-and-restored GameIndex.
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
# install_worlds must report worlds it could not install to its caller. A
# world that fails outright used to be a log line and nothing more, so
# tools/mwgg_upgrade.py exited 0 and the compose consumers booted against a
# venv missing that world. `.failed` is what makes the failure visible.
# --------------------------------------------------------------------------- #

ABSENT = "world_that_is_in_no_index_and_has_no_apworld"
TARGET = f"worlds.{ABSENT}"


class TestInstallWorldsReportsFailures(unittest.TestCase):
    def setUp(self):
        # Nothing here reaches the network -- the absent slug has no module_location to
        # install from -- but install_worlds also prunes the real venv on the way out.
        patcher = mock.patch.object(ModuleUpdate, "_prune_stale_apworld_extractions")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_uninstallable_world_is_reported(self):
        result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertIn(TARGET, result.failed)
        self.assertNotIn(TARGET, result, "a world with no apworld is not an apworld fallback")

    def test_result_still_behaves_as_the_apworld_list(self):
        # Existing callers use the return value as a plain list of apworld fallbacks.
        result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertIsInstance(result, list)
        self.assertFalse(result)
        self.assertEqual(list(result), [])

    def test_skipped_installs_still_expose_failed(self):
        with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=True):
            result = ModuleUpdate.install_worlds([TARGET], with_deps=True)
        self.assertEqual(result.failed, [])
        self.assertFalse(result)


# --------------------------------------------------------------------------- #
# The mwgg_upgrader is the sole writer of the shared worlds venv and every
# other compose service gates on `service_completed_successfully`. Its exit
# code therefore decides whether the site comes up against an incomplete
# venv.
# --------------------------------------------------------------------------- #

def _load_upgrader():
    # tools/ is not a package; load the script by path. Importing it pops the
    # install-skip env vars, so snapshot and restore them around the load.
    saved = {k: os.environ.get(k) for k in ("SKIP_ALL_INSTALLS", "SKIP_REQUIREMENTS_UPDATE")}
    spec = importlib.util.spec_from_file_location(
        "mwgg_upgrade_under_test", REPO_ROOT / "tools" / "mwgg_upgrade.py"
    )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return module


class TestUpgraderExitCodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upgrader = _load_upgrader()

    def _run(self, index_slugs, failed, installed_before, installed_after, env=None):
        result = ModuleUpdate.WorldInstallResult()
        result.failed.extend(failed)
        games = {slug: {} for slug in index_slugs}
        slug_dirs = iter([set(installed_before), set(installed_after)])
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=True), \
                mock.patch.object(ModuleUpdate, "invalidate_caches"), \
                mock.patch.object(ModuleUpdate, "install_worlds", return_value=result), \
                mock.patch.object(ModuleUpdate, "_venv_has_worlds", return_value=True), \
                mock.patch.object(self.upgrader, "_installed_world_slugs", lambda: next(slug_dirs)), \
                mock.patch.dict(os.environ, env or {}, clear=False):
            from mwgg_igdb import GameIndex
            with mock.patch.object(GameIndex, "get_all_games", return_value=games):
                return self.upgrader.main()

    def test_clean_run_exits_zero(self):
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, [], slugs, slugs), 0)

    def test_one_bad_world_does_not_block_the_deploy(self):
        # With the catalog no longer truncating, a single uninstallable world costs
        # that one game; blocking every other service over it is the worse outcome.
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, ["worlds.w0"], slugs[1:], slugs[1:]), 0)

    def test_widespread_failure_blocks_the_deploy(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(self._run(slugs, failed, slugs[5:], slugs[5:]), 1)

    def test_regression_blocks_the_deploy_however_small(self):
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, ["worlds.w0"], slugs, slugs[1:]), 1)

    def test_failure_tolerance_is_overridable(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "5"}),
            0,
        )
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "0"}),
            1,
        )

    def test_empty_venv_still_blocks(self):
        slugs = [f"w{i}" for i in range(20)]
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=True), \
                mock.patch.object(ModuleUpdate, "invalidate_caches"), \
                mock.patch.object(ModuleUpdate, "install_worlds",
                                  return_value=ModuleUpdate.WorldInstallResult()), \
                mock.patch.object(ModuleUpdate, "_venv_has_worlds", return_value=False), \
                mock.patch.object(self.upgrader, "_installed_world_slugs", set):
            from mwgg_igdb import GameIndex
            with mock.patch.object(GameIndex, "get_all_games", return_value={s: {} for s in slugs}):
                self.assertEqual(self.upgrader.main(), 1)

    def test_empty_index_blocks_the_deploy(self):
        # The venv may still hold yesterday's worlds, so 0-of-0 failures must not
        # read as a clean run.
        self.assertEqual(self._run([], [], ["w0"], ["w0"]), 1)

    def test_bad_tolerance_override_falls_back_to_default(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "banana"}),
            1,
        )
        self.assertEqual(
            self._run(slugs, ["worlds.w0"], slugs[1:], slugs[1:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "banana"}),
            0,
        )

    def test_installed_world_slugs_missing_dir_is_empty(self):
        with mock.patch.object(ModuleUpdate, "_venv_worlds_dir",
                               return_value=REPO_ROOT / "no_such_dir_for_this_test"):
            self.assertEqual(self.upgrader._installed_world_slugs(), set())

    def test_installed_world_slugs_filters_non_worlds(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "alpha").mkdir()
            (root / "_infra").mkdir()
            (root / "__pycache__").mkdir()
            (root / "stray.txt").write_text("x")
            with mock.patch.object(ModuleUpdate, "_venv_worlds_dir", return_value=root):
                self.assertEqual(self.upgrader._installed_world_slugs(), {"alpha"})

    def test_failed_index_install_still_blocks(self):
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=False):
            self.assertEqual(self.upgrader.main(), 1)


# --------------------------------------------------------------------------- #
# set_game_names must not import the `worlds` package. worlds/__init__.py
# is one-shot: on import it snapshots Utils._worlds_to_load, loads exactly
# those entries and builds network_data_package. If set_game_names imports
# it while still queueing, every game queued afterwards is silently dropped
# from the catalog. A single uninstallable world once cost the site 236 of
# 244 games this way.
# --------------------------------------------------------------------------- #

# Real worlds that live as source directories in the repo, so they have no pip
# metadata and take the same code path the missing world took. The bogus entry
# sits in the middle: everything after it must still reach the loader.
ON_DISK_SLUGS = ["_debug", "apquest", "mwquest"]
MISSING_SLUG = "world_that_is_not_installed_anywhere"

CHILD = textwrap.dedent("""
    import json, os, sys
    sys.path.insert(0, {stubs!r})
    sys.path.insert(0, {root!r})

    import settings
    settings.no_gui = True
    settings.skip_autosave = True

    import Utils
    import ModuleUpdate
    import tempfile
    from pathlib import Path
    # Hermetic: set_game_names scans custom_worlds_dir at call time; the machine's
    # real directory may hold arbitrary (or corrupt) apworlds.
    ModuleUpdate.custom_worlds_dir = Path(tempfile.mkdtemp())
    from mwgg_igdb import GameIndex

    on_disk = {on_disk!r}
    missing = {missing!r}
    games = []
    for slug in on_disk[:1] + [missing] + on_disk[1:]:
        name = f"Game {{slug}}"
        GameIndex.add_game(slug, {{"game_name": name}})
        games.append(name)

    Utils.set_game_names(games, strict=False)

    imported_early = "worlds" in sys.modules
    queued = [e for e in Utils.game_names() if isinstance(e, str)]

    import worlds
    loaded = [s.game_module for s in worlds.world_sources if isinstance(s.game_module, str)]

    print("@@RESULT@@" + json.dumps({{
        "imported_early": imported_early,
        "queued": queued,
        "loaded": loaded,
        "served": sorted(worlds.network_data_package["games"]),
        "failed_loads": worlds.failed_world_loads,
    }}))
""")


def _run_child() -> dict:
    env = dict(os.environ)
    env.update(
        SKIP_ALL_INSTALLS="1",
        SKIP_REQUIREMENTS_UPDATE="1",
        KIVY_NO_CONSOLELOG="1",
        KIVY_NO_ARGS="1",
        PYTHONIOENCODING="utf-8",
    )
    env.pop("AP_TEST_WORLDS", None)
    # If set (e.g. inside the Docker image), ModuleUpdate would rank the worlds-venv
    # site-packages ahead of the stub dir on the child's sys.path.
    env.pop("MWGG_USE_WORLDS_VENV", None)
    source = CHILD.format(
        stubs=str(REPO_ROOT / "test" / "_stubs"),
        root=str(REPO_ROOT),
        on_disk=ON_DISK_SLUGS,
        missing=MISSING_SLUG,
    )
    proc = subprocess.run(
        [sys.executable, "-c", source],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=600,
    )
    marker = "@@RESULT@@"
    for line in proc.stdout.splitlines():
        if line.startswith(marker):
            return json.loads(line[len(marker):])
    raise AssertionError(
        f"child produced no result (rc={proc.returncode})\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )


class TestSetGameNamesDoesNotImportWorlds(unittest.TestCase):
    """Runs in a subprocess: the suite's own bootstrap has already imported `worlds`."""

    @classmethod
    def setUpClass(cls):
        cls.result = _run_child()

    def test_worlds_not_imported_while_queueing(self):
        self.assertFalse(
            self.result["imported_early"],
            "set_game_names imported the `worlds` package, freezing the catalog mid-queue",
        )

    def test_missing_world_does_not_truncate_the_catalog(self):
        loaded = set(self.result["loaded"])
        for slug in ON_DISK_SLUGS:
            self.assertIn(
                f"worlds.{slug}", loaded,
                f"worlds.{slug} was queued but never reached the loader; a missing "
                f"world truncated the catalog",
            )
        self.assertNotIn(f"worlds.{MISSING_SLUG}", loaded)

    def test_missing_world_does_not_abort_queueing(self):
        queued = set(self.result["queued"])
        for slug in ON_DISK_SLUGS:
            self.assertIn(f"worlds.{slug}", queued)

    def test_missing_world_costs_exactly_one_game(self):
        # What the site actually serves. The outage shipped 8 of 244 entries here.
        served = set(self.result["served"])
        self.assertEqual(self.result["failed_loads"], [])
        self.assertTrue(
            {"Archipelago", "Universal Tracker"} <= served,
            f"baseline worlds missing from the data package: {sorted(served)}",
        )
        self.assertEqual(
            len(served), len(ON_DISK_SLUGS) + 2,
            f"expected every on-disk world plus the two baseline entries, got {sorted(served)}",
        )


class TestWorldModuleOnDisk(unittest.TestCase):
    def test_absent_world_is_not_on_disk(self):
        self.assertFalse(Utils._world_module_on_disk(MISSING_SLUG))

    def test_present_world_is_on_disk(self):
        self.assertTrue(Utils._world_module_on_disk("generic"))

    def test_worlds_dir_itself_is_not_a_world(self):
        # A bare directory matches as a namespace package; only real packages count.
        self.assertFalse(Utils._world_module_on_disk("__pycache__"))


# --------------------------------------------------------------------------- #
# update_worlds: the platform- and freeze-neutral world-wheel update run on
# every launcher cold start (fronted by the splash on Windows GUI).
# --------------------------------------------------------------------------- #

def test_update_worlds_skips_when_installs_disabled():
    with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=True), \
            mock.patch.object(ModuleUpdate, "check_for_updates") as check:
        assert ModuleUpdate.update_worlds() is None
    check.assert_not_called()


def test_update_worlds_returns_none_when_current():
    with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=False), \
            mock.patch.object(ModuleUpdate, "check_for_updates", return_value=[]) as check, \
            mock.patch.object(ModuleUpdate, "install_worlds") as install:
        assert ModuleUpdate.update_worlds() is None
    check.assert_called_once_with(worlds_only=True)
    install.assert_not_called()


def test_update_locked_skips_all_update_work_under_skip_update(monkeypatch):
    """SKIP_REQUIREMENTS_UPDATE children (yaml-options spawns, clients under a
    live launcher) must not re-run any updater work."""
    monkeypatch.setattr(ModuleUpdate, "_skip_update", True)
    with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=False), \
            mock.patch.object(ModuleUpdate, "install_mwgg_igdb") as igdb, \
            mock.patch.object(ModuleUpdate, "update_worlds") as worlds:
        ModuleUpdate._update_locked(yes=True, force=False, worlds=None)
    igdb.assert_not_called()
    worlds.assert_not_called()


def test_update_locked_runs_world_update_when_not_skipped(monkeypatch):
    monkeypatch.setattr(ModuleUpdate, "_skip_update", False)
    monkeypatch.setattr(ModuleUpdate, "update_ran", True)
    with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=False), \
            mock.patch.object(ModuleUpdate, "install_mwgg_igdb"), \
            mock.patch.object(ModuleUpdate, "update_worlds", return_value=None) as worlds:
        ModuleUpdate._update_locked(yes=True, force=False, worlds=None)
    worlds.assert_called_once_with()


def test_update_worlds_installs_outdated_worlds():
    result = ModuleUpdate.WorldInstallResult()
    with mock.patch.object(ModuleUpdate, "_skip_all_installs", return_value=False), \
            mock.patch.object(ModuleUpdate, "check_for_updates", return_value=["worlds.albw"]), \
            mock.patch.object(ModuleUpdate, "install_worlds", return_value=result) as install:
        assert ModuleUpdate.update_worlds() is result
    install.assert_called_once_with(["worlds.albw"])


# --------------------------------------------------------------------------- #
# Updater gating: update checks only run from installed frozen builds.
# --------------------------------------------------------------------------- #

def _platform(is_windows: bool = False, is_linux: bool = False, is_macos: bool = False):
    return mock.patch.multiple(
        Updater, is_windows=is_windows, is_linux=is_linux, is_macos=is_macos
    )


class TestCanCheckForUpdates(unittest.TestCase):
    def test_source_checkout_never_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=False):
            for platform_kwargs in (
                {"is_windows": True},
                {"is_linux": True},
                {"is_macos": True},
            ):
                with _platform(**platform_kwargs):
                    self.assertFalse(Updater.can_check_for_updates())

    def test_frozen_windows_always_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_windows=True):
            self.assertTrue(Updater.can_check_for_updates())

    def test_frozen_linux_requires_appimage_env(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_linux=True):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertFalse(Updater.can_check_for_updates())
            with mock.patch.dict(os.environ, {"APPIMAGE": "/opt/MultiworldGG.AppImage"}):
                self.assertTrue(Updater.can_check_for_updates())

    def test_frozen_macos_requires_app_bundle_path(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_macos=True):
            bundle_exe = "/Applications/MultiworldGG.app/Contents/MacOS/MultiworldGG"
            with mock.patch("os.path.realpath", return_value=bundle_exe):
                self.assertTrue(Updater.can_check_for_updates())
            with mock.patch("os.path.realpath", return_value="/usr/local/bin/MultiworldGG"):
                self.assertFalse(Updater.can_check_for_updates())

    def test_unknown_platform_never_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), _platform():
            self.assertFalse(Updater.can_check_for_updates())


class TestReleasePageUrl(unittest.TestCase):
    def test_release_page_url_points_at_releases_list(self) -> None:
        url = Updater.get_release_page_url()
        self.assertEqual(
            url,
            f"https://github.com/{Updater.GITHUB_OWNER}/{Updater.GITHUB_REPO}/releases",
        )


# --------------------------------------------------------------------------- #
# _uv_candidate_paths: Windows winget-Packages fallback. The WinGet "Links"
# shim is an AppExecLink some tokens can't stat/exec (WinError 448); the real
# installed PE under Packages/astral-sh.uv_*/.../uv.exe is a plain file.
# --------------------------------------------------------------------------- #

def test_uv_candidate_paths_windows_globs_winget_packages(tmp_path, monkeypatch):
    pkg_dir = tmp_path / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages" / "astral-sh.uv_pub"
    (pkg_dir / "uv-x86_64-pc-windows-msvc").mkdir(parents=True)
    uv_exe = pkg_dir / "uv-x86_64-pc-windows-msvc" / "uv.exe"
    uv_exe.write_text("x")
    monkeypatch.setattr(ModuleUpdate, "is_windows", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: False)
    monkeypatch.setattr(ModuleUpdate.Path, "home", lambda: tmp_path)

    cands = ModuleUpdate._uv_candidate_paths()

    assert uv_exe in cands
    links_shim = tmp_path / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "uv.exe"
    assert cands.index(uv_exe) > cands.index(links_shim)


def test_uv_candidate_paths_windows_tolerates_missing_packages_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(ModuleUpdate, "is_windows", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: False)
    monkeypatch.setattr(ModuleUpdate.Path, "home", lambda: tmp_path)  # no Packages dir at all

    cands = ModuleUpdate._uv_candidate_paths()  # must not raise

    assert any(str(c) == "uv" for c in cands)


# --------------------------------------------------------------------------- #
# wheel_cache/: Inno's native [Files] download step stages selected worlds'
# wheels here, next to the exe, before first launch -- replacing the broken
# de-elevated `runasoriginaluser --update-modules` exec (WinError 448).
# ModuleUpdate claims the dir atomically and installs it into the worlds venv
# once at import time; a custom_worlds/ apworld still wins as a manual override.
# --------------------------------------------------------------------------- #

def _make_wheel_cache(exe_dir, variant=None, wheels=()):
    cache_dir = exe_dir / "wheel_cache"
    cache_dir.mkdir()
    if variant is not None:
        (cache_dir / "mwgg_igdb_variant.txt").write_text(variant, encoding="utf-8")
    for name in wheels:
        (cache_dir / name).write_text("fake wheel contents", encoding="utf-8")
    return cache_dir


@pytest.fixture
def wheel_cache_exe(tmp_path, monkeypatch):
    """Point ModuleUpdate's wheel_cache resolution at tmp_path (a fake exe dir)."""
    fake_exe = tmp_path / "MultiworldGG.exe"
    fake_exe.write_text("x")
    monkeypatch.setattr(sys, "executable", str(fake_exe))
    return tmp_path


def test_wheel_cache_dir_is_next_to_executable(wheel_cache_exe):
    assert ModuleUpdate._wheel_cache_dir() == wheel_cache_exe / "wheel_cache"


def test_wheel_cache_variant_token_reads_valid_marker(wheel_cache_exe):
    _make_wheel_cache(wheel_cache_exe, variant="nr")
    assert ModuleUpdate._wheel_cache_variant_token() == "nr"


def test_wheel_cache_variant_token_rejects_unknown_value(wheel_cache_exe):
    _make_wheel_cache(wheel_cache_exe, variant="bogus")
    assert ModuleUpdate._wheel_cache_variant_token() is None


def test_wheel_cache_variant_token_none_when_absent(wheel_cache_exe):
    assert ModuleUpdate._wheel_cache_variant_token() is None


def test_wheel_cache_variant_token_reads_explicit_dir(tmp_path):
    cache_dir = _make_wheel_cache(tmp_path, variant="twelve")
    assert ModuleUpdate._wheel_cache_variant_token(cache_dir) == "twelve"


def test_apply_wheel_cache_variant_precedes_first_igdb_install(wheel_cache_exe, monkeypatch, restore_variant_globals):
    """Pins the ordering: the marker must be applied before
    _bootstrap_fresh_venv_mwgg_igdb() runs install_mwgg_igdb(), so a `nr`
    selection can never silently install `sixteen` on the very first pull."""
    _make_wheel_cache(wheel_cache_exe, variant="nr")
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)
    monkeypatch.setattr(ModuleUpdate, "_venv_just_created", True)
    monkeypatch.setattr(ModuleUpdate, "invalidate_caches", lambda: None)

    seen_variant = []

    def fake_install_mwgg_igdb(*a, **k):
        seen_variant.append(ModuleUpdate.MWGG_IGDB_VARIANT)
        return True

    monkeypatch.setattr(ModuleUpdate, "install_mwgg_igdb", fake_install_mwgg_igdb)

    ModuleUpdate._apply_wheel_cache_variant()
    ModuleUpdate._bootstrap_fresh_venv_mwgg_igdb()

    assert seen_variant == ["nr"]


def test_apply_wheel_cache_variant_noop_when_not_frozen(wheel_cache_exe, monkeypatch, restore_variant_globals):
    _make_wheel_cache(wheel_cache_exe, variant="nr")
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: False)
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", None)

    ModuleUpdate._apply_wheel_cache_variant()

    assert ModuleUpdate._EXPLICIT_VARIANT is None


def test_apply_wheel_cache_variant_noop_when_installs_skipped(wheel_cache_exe, monkeypatch, restore_variant_globals):
    _make_wheel_cache(wheel_cache_exe, variant="nr")
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", None)

    ModuleUpdate._apply_wheel_cache_variant()

    assert ModuleUpdate._EXPLICIT_VARIANT is None


def test_install_wheel_cache_wheels_single_invocation_with_deps(monkeypatch):
    """Contract: exactly one `uv pip install`, every wheel path, no --no-deps
    and no --offline -- transitive deps must resolve against PyPI."""
    recorded = []

    def fake_uv_run(args, timeout=120, check=False):
        recorded.append(args)
        return subprocess.CompletedProcess(args, 0, "ok", "")

    monkeypatch.setattr(ModuleUpdate, "_uv_run", fake_uv_run)
    monkeypatch.setattr(ModuleUpdate, "invalidate_caches", lambda: None)

    wheel_a = "/c/wheel_cache/worlds.a-1.0-py3-none-any.whl"
    wheel_b = "/c/wheel_cache/worlds.b-1.0-py3-none-any.whl"
    ModuleUpdate._install_wheel_cache_wheels([wheel_a, wheel_b])

    assert len(recorded) == 1
    cmd = recorded[0]
    assert cmd[0] == "pip"
    assert cmd[1] == "install"
    assert wheel_a in cmd
    assert wheel_b in cmd
    assert "--no-deps" not in cmd
    assert "--offline" not in cmd
    assert cmd[-2] == "--python"


def test_install_wheel_cache_wheels_logs_failure_without_raising(monkeypatch, caplog):
    monkeypatch.setattr(
        ModuleUpdate, "_uv_run",
        lambda args, timeout=120, check=False: subprocess.CompletedProcess(args, 1, "", "boom"),
    )
    with caplog.at_level(logging.WARNING):
        ModuleUpdate._install_wheel_cache_wheels(["/c/wheel_cache/a-1.0-py3-none-any.whl"])
    assert any("a-1.0-py3-none-any.whl" in r.message for r in caplog.records)


def test_consume_wheel_cache_noop_when_not_frozen(wheel_cache_exe, monkeypatch):
    _make_wheel_cache(wheel_cache_exe, variant="nr", wheels=["a-1.0-py3-none-any.whl"])
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: False)
    monkeypatch.setattr(ModuleUpdate.os, "rename",
                        lambda *a: (_ for _ in ()).throw(AssertionError("dev launch must not touch wheel_cache")))

    ModuleUpdate._consume_wheel_cache()

    assert (wheel_cache_exe / "wheel_cache").exists()


def test_consume_wheel_cache_noop_when_installs_skipped(wheel_cache_exe, monkeypatch):
    _make_wheel_cache(wheel_cache_exe, variant="nr", wheels=["a-1.0-py3-none-any.whl"])
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: True)
    monkeypatch.setattr(ModuleUpdate.os, "rename",
                        lambda *a: (_ for _ in ()).throw(AssertionError("must not touch wheel_cache")))

    ModuleUpdate._consume_wheel_cache()

    assert (wheel_cache_exe / "wheel_cache").exists()


def test_consume_wheel_cache_claim_is_atomic_loser_skips(wheel_cache_exe, monkeypatch):
    """A concurrent loser's os.rename raises OSError (EAFP); it just skips."""
    _make_wheel_cache(wheel_cache_exe, variant="nr", wheels=["a-1.0-py3-none-any.whl"])
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)
    monkeypatch.setattr(ModuleUpdate.os, "rename",
                        lambda *a: (_ for _ in ()).throw(OSError("lost the race")))

    install_called = []
    monkeypatch.setattr(ModuleUpdate, "_install_wheel_cache_wheels", lambda paths: install_called.append(paths))

    ModuleUpdate._consume_wheel_cache()

    assert install_called == []
    # Left alone for whoever actually holds the claim.
    assert (wheel_cache_exe / "wheel_cache").exists()


def test_consume_wheel_cache_installs_wheels_and_sets_variant(wheel_cache_exe, monkeypatch, restore_variant_globals):
    _make_wheel_cache(
        wheel_cache_exe, variant="ao",
        wheels=["worlds.a-1.0-py3-none-any.whl", "worlds.b-1.0-py3-none-any.whl"],
    )
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)

    installed = []
    monkeypatch.setattr(ModuleUpdate, "_install_wheel_cache_wheels", lambda paths: installed.append(sorted(paths)))

    ModuleUpdate._consume_wheel_cache()

    assert ModuleUpdate.MWGG_IGDB_VARIANT == "ao"
    assert len(installed) == 1 and len(installed[0]) == 2
    assert all(p.endswith(".whl") for p in installed[0])
    # The claim is released once processing finishes.
    assert not (wheel_cache_exe / "wheel_cache").exists()
    assert not (wheel_cache_exe / "wheel_cache.consuming").exists()


def test_consume_wheel_cache_empty_dir_marker_only_skips_uv_call(wheel_cache_exe, monkeypatch, restore_variant_globals):
    """A cache dir with zero worlds selected (marker only) is a clean no-op."""
    _make_wheel_cache(wheel_cache_exe, variant="sixteen")
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)

    def _fail(*a, **k):
        raise AssertionError("must not invoke uv with zero wheels")

    monkeypatch.setattr(ModuleUpdate, "_install_wheel_cache_wheels", _fail)

    ModuleUpdate._consume_wheel_cache()

    assert ModuleUpdate.MWGG_IGDB_VARIANT == "sixteen"
    assert not (wheel_cache_exe / "wheel_cache").exists()


def test_consume_wheel_cache_cleans_stale_consuming_dir_from_crash(wheel_cache_exe, monkeypatch):
    stale = wheel_cache_exe / "wheel_cache.consuming"
    stale.mkdir()
    (stale / "leftover.whl").write_text("x")
    _make_wheel_cache(wheel_cache_exe, wheels=["fresh-1.0-py3-none-any.whl"])
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)

    installed = []
    monkeypatch.setattr(ModuleUpdate, "_install_wheel_cache_wheels", lambda paths: installed.append(paths))

    ModuleUpdate._consume_wheel_cache()

    assert len(installed) == 1
    assert any("fresh" in p for p in installed[0])
    assert not any("leftover" in p for p in installed[0])
    assert not stale.exists()


def test_consume_wheel_cache_survives_unexpected_failure_and_cleans_up(wheel_cache_exe, monkeypatch, caplog):
    """Best effort: an unexpected failure mid-processing must not raise out of
    module import, and must not leave wheel_cache.consuming stuck for future launches."""
    _make_wheel_cache(wheel_cache_exe, wheels=["a-1.0-py3-none-any.whl"])
    monkeypatch.setattr(ModuleUpdate, "is_frozen", lambda: True)
    monkeypatch.setattr(ModuleUpdate, "_skip_all_installs", lambda: False)

    def _boom(paths):
        raise RuntimeError("simulated failure mid-install")

    monkeypatch.setattr(ModuleUpdate, "_install_wheel_cache_wheels", _boom)

    with caplog.at_level(logging.WARNING):
        ModuleUpdate._consume_wheel_cache()  # must not raise

    assert not (wheel_cache_exe / "wheel_cache").exists()
    assert not (wheel_cache_exe / "wheel_cache.consuming").exists()


# --------------------------------------------------------------------------- #
# MultiWorld._ensure_uv_discoverable / _uv_binary_works: a PATH hit from
# shutil.which is not proof uv actually runs -- the WinGet Links AppExecLink
# shim resolves but some tokens can't exec it (WinError 448).
# --------------------------------------------------------------------------- #

def test_uv_binary_works_true_on_success(monkeypatch):
    monkeypatch.setattr(MultiWorld.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(a, 0))
    assert MultiWorld._uv_binary_works("uv") is True


def test_uv_binary_works_false_on_oserror(monkeypatch):
    def _raise(*a, **k):
        raise OSError("no such file")
    monkeypatch.setattr(MultiWorld.subprocess, "run", _raise)
    assert MultiWorld._uv_binary_works("uv") is False


def test_uv_binary_works_false_on_timeout(monkeypatch):
    def _raise(*a, **k):
        raise subprocess.TimeoutExpired(cmd="uv", timeout=5)
    monkeypatch.setattr(MultiWorld.subprocess, "run", _raise)
    assert MultiWorld._uv_binary_works("uv") is False


def test_ensure_uv_discoverable_revalidates_which_result(monkeypatch, tmp_path):
    """A broken shim on PATH must not short-circuit discovery; a working
    fallback candidate directory is prepended instead."""
    import shutil
    fallback_dir = tmp_path / ".local" / "bin"
    fallback_dir.mkdir(parents=True)
    (fallback_dir / "uv.exe").write_text("x")
    monkeypatch.setattr(os.path, "expanduser",
                        lambda p: str(tmp_path) if p == "~" else os.path.expanduser(p))
    monkeypatch.setattr(shutil, "which", lambda name: "C:/broken/links/uv.exe")
    monkeypatch.setattr(MultiWorld, "_uv_binary_works", lambda path: path == str(fallback_dir / "uv.exe"))

    saved_environ = dict(os.environ)
    try:
        os.environ.pop("PATH", None)
        MultiWorld._ensure_uv_discoverable()
        assert os.environ["PATH"].startswith(str(fallback_dir) + os.pathsep)
    finally:
        os.environ.clear()
        os.environ.update(saved_environ)


def test_ensure_uv_discoverable_noop_when_which_uv_already_works(monkeypatch):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/uv")
    monkeypatch.setattr(MultiWorld, "_uv_binary_works", lambda path: True)

    def _fail_listdir(path):
        raise AssertionError("must not walk WinGet Packages once PATH's uv already works")
    monkeypatch.setattr(os, "listdir", _fail_listdir)

    saved_path = os.environ.get("PATH")
    MultiWorld._ensure_uv_discoverable()
    assert os.environ.get("PATH") == saved_path


def test_ensure_uv_discoverable_never_raises_when_nothing_works(monkeypatch, tmp_path):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(os.path, "expanduser",
                        lambda p: str(tmp_path) if p == "~" else os.path.expanduser(p))
    monkeypatch.setattr(MultiWorld, "_uv_binary_works", lambda path: False)

    saved_path = os.environ.get("PATH")
    MultiWorld._ensure_uv_discoverable()  # must not raise
    assert os.environ.get("PATH") == saved_path
