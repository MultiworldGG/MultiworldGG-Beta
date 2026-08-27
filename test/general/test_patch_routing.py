"""Tests for patch-file routing: opening a patch file (OS file-association
double-click or CLI positional) must launch the right game client with it.

Guards the pieces the flow is built from:
  * MultiWorld's argument parser accepts an optional positional file/URL --
    every installer file association and URL protocol points at
    `MultiWorldGG.exe "%1"`, which used to be an unrecognized argument
    (SystemExit 2) for every game;
  * Utils.read_patch_game_name reads the game name from a patch container's
    root archipelago.json without importing any worlds (Patch.py pattern);
  * Utils._client_launch_argv translates launcher kwargs into the CLI argv
    world clients parse (positional patch file first, then --connect/--name);
  * LauncherComponents.identify/get_exe route non-patch files (e.g. a
    .archipelago multidata) to their tool component without the
    `from Launcher import ...` paths that don't exist in beta.
"""
import json
import sys
import zipfile

import LauncherComponents as launcher_components
import MultiWorld
import Utils
from LauncherComponents import Component, SuffixIdentifier, Type, components, get_exe, identify


def _make_patch_container(path, game_name: str) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("archipelago.json", json.dumps({"game": game_name, "compatible_version": 5}))


# --- MultiWorld argument parser ---

def test_parser_accepts_positional_patch_path():
    args = MultiWorld.make_arg_parser().parse_args(["C:\\seeds\\AP_1234_P1.aplttp"])
    assert args.launch_file == "C:\\seeds\\AP_1234_P1.aplttp"
    assert args.game is None


def test_parser_no_args_defaults():
    args = MultiWorld.make_arg_parser().parse_args([])
    assert args.launch_file is None
    assert args.frontend == "gui"


def test_parser_positional_combines_with_flags():
    args = MultiWorld.make_arg_parser().parse_args(["seed.apkh3", "--frontend", "tui", "--loglevel", "info"])
    assert args.launch_file == "seed.apkh3"
    assert args.frontend == "tui"
    assert args.loglevel == "info"


def test_parser_accepts_launch_url():
    args = MultiWorld.make_arg_parser().parse_args(["archipelago://player:pass@multiworld.gg:38281"])
    assert args.launch_file == "archipelago://player:pass@multiworld.gg:38281"


# --- Utils.read_patch_game_name ---

def test_read_patch_game_name_reads_root_manifest(tmp_path):
    patch = tmp_path / "seed.apemerald"
    _make_patch_container(patch, "Pokemon Emerald")
    assert Utils.read_patch_game_name(str(patch)) == "Pokemon Emerald"


def test_read_patch_game_name_rejects_non_zip(tmp_path):
    multidata = tmp_path / "AP_1234.archipelago"
    multidata.write_bytes(b"\x78\x9c not a zip")
    assert Utils.read_patch_game_name(str(multidata)) is None


def test_read_patch_game_name_rejects_zip_without_root_manifest(tmp_path):
    apworld = tmp_path / "some.apworld"
    with zipfile.ZipFile(apworld, "w") as zf:
        zf.writestr("some/archipelago.json", json.dumps({"game": "Nested"}))
    assert Utils.read_patch_game_name(str(apworld)) is None


def test_read_patch_game_name_missing_file(tmp_path):
    assert Utils.read_patch_game_name(str(tmp_path / "missing.aplttp")) is None


def test_read_patch_game_name_manifest_without_game(tmp_path):
    patch = tmp_path / "broken.aplttp"
    with zipfile.ZipFile(patch, "w") as zf:
        zf.writestr("archipelago.json", json.dumps({"compatible_version": 5}))
    assert Utils.read_patch_game_name(str(patch)) is None


# --- Utils._client_launch_argv ---

def test_client_launch_argv_patch_file_is_positional_before_connect():
    argv = Utils._client_launch_argv("localhost:38281", None, "kh3", patch_file="C:/seed.apkh3")
    assert argv == ["C:/seed.apkh3", "--connect=localhost:38281"]


def test_client_launch_argv_patch_file_only():
    assert Utils._client_launch_argv(None, None, "bizhawk", patch_file="seed.apemerald") == ["seed.apemerald"]


def test_client_launch_argv_empty():
    assert Utils._client_launch_argv(None, None, "kh3") == []


def test_client_launch_argv_tracker_gets_slot_name():
    argv = Utils._client_launch_argv("host:1", "Player1", "universal_tracker")
    assert argv == ["--connect=host:1", "--name=Player1"]


def test_client_launch_argv_slot_name_ignored_for_regular_clients():
    assert Utils._client_launch_argv("host:1", "Player1", "alttp") == ["--connect=host:1"]


# --- LauncherComponents.identify / get_exe ---

def test_identify_routes_multidata_to_host():
    component = identify("AP_1234.archipelago")
    assert component is not None
    assert component.display_name == "Host"


def test_identify_unknown_suffix_returns_none():
    assert identify("photo.png") is None
    assert identify(None) is None
    assert identify("") is None


def test_identify_routes_apworld_to_install_apworld():
    component = identify("some_world.apworld")
    assert component is not None
    assert component.display_name == "Install APWorld"


def test_identify_world_registered_suffix():
    component = Component("Patch Routing Test Client", func=lambda *args: None,
                          component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".aproutingtest"))
    components.append(component)
    try:
        assert identify("seed.aproutingtest") is component
    finally:
        components.remove(component)


def test_get_exe_resolves_script_component_in_dev():
    host = next(c for c in components if c.display_name == "Host")
    exe = get_exe(host)
    assert exe is not None
    assert exe[0] == sys.executable
    assert exe[1].endswith("MultiServer.py")


def test_get_exe_func_only_component_has_no_exe():
    component = Component("Func Only", func=lambda *args: None)
    assert get_exe(component) is None


def test_get_exe_resolves_literal_frozen_names_when_frozen(monkeypatch):
    """Host/Generate must resolve to the exact built exe name under a frozen
    build regardless of the (possibly test-channel-overridden) instance_name --
    application.yaml's app_name overriding instance_name at runtime was exactly
    the bug that made frozen_name resolution silently match nothing."""
    monkeypatch.setattr(launcher_components, "is_frozen", lambda: True)
    monkeypatch.setattr(launcher_components, "is_windows", True)

    host = next(c for c in components if c.display_name == "Host")
    generate = next(c for c in components if c.display_name == "Generate")

    assert get_exe(host) == [launcher_components.local_path("MultiWorldGGServer.exe")]
    assert get_exe(generate) == [launcher_components.local_path("MultiWorldGGGenerate.exe")]
