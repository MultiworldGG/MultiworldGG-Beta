"""Regression tests for scanning custom_worlds/ into the in-memory GameIndex.

Two things that have regressed before and are guarded here:
  * a stray non-world file (e.g. a README.txt) in custom_worlds/ must not abort
    the scan -- discover_custom_world_module used to raise UnboundLocalError on
    any unrecognized suffix, which aborted the whole directory scan; and
  * an apworld dropped in custom_worlds/ must be registered via
    GameIndex.add_game so it becomes selectable on launch.
"""
import json
import zipfile

import ModuleUpdate
import Utils
from mwgg_igdb import GameIndex


def _make_apworld(path, game_name: str) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("archipelago.json", json.dumps({"game": game_name, "compatible_version": 5}))


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
