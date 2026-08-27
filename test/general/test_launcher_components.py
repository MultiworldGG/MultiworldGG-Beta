"""Tests for the launcher component surface: the standalone Launcher process
(Phase 1 foundations) contract -- FROZEN_TARGETS as the single source of truth
for built exe names, BaseUtils.spawn_client's argv/env/detach construction, the
builtin/other component-origin classification that keeps builtin_components()
trustworthy, and the worlds.LauncherComponents re-export shim.
"""
import re
import sys

import pytest

import BaseUtils
import LauncherComponents as lc
import Utils


def _setup_py_target_names() -> set[str]:
    with open(Utils.local_path("setup.py"), "r", encoding="utf-8") as f:
        text = f.read()
    names: set[str] = set()
    for line in text.splitlines():
        if "target_name" not in line:
            continue
        for match in re.findall(r'"([^"]+)"', line):
            names.add(match[:-4] if match.endswith(".exe") else match)
    return names


# --- FROZEN_TARGETS single source of truth ---

def test_frozen_targets_covers_every_setup_py_executable():
    """Every exe setup.py actually builds must resolve through FROZEN_TARGETS.

    Subset check in one direction only: FROZEN_TARGETS may contain entries
    setup.py doesn't build yet (the Launcher exe lands in a later phase)."""
    setup_py_names = _setup_py_target_names()
    assert setup_py_names, "expected to find at least one target_name in setup.py"
    assert setup_py_names <= set(BaseUtils.FROZEN_TARGETS.values())


def test_host_and_generate_frozen_names_match_frozen_targets():
    host = lc.find_component("Host")
    generate = lc.find_component("Generate")
    assert host is not None and generate is not None
    assert host.frozen_name == BaseUtils.FROZEN_TARGETS["MultiServer"]
    assert generate.frozen_name == BaseUtils.FROZEN_TARGETS["Generate"]


def test_builtin_frozen_names_do_not_derive_from_live_instance_name(monkeypatch):
    """Regression guard for the app_name-override bug: application.yaml's
    app_name (e.g. "MultiworldGG-Test") used to override instance_name at
    runtime, and frozen_name = apname + script_name silently broke. Every
    builtin frozen_name must be a literal FROZEN_TARGETS value, unaffected by
    instance_name."""
    monkeypatch.setattr(BaseUtils, "instance_name", "MultiworldGG-Test")
    frozen_values = set(BaseUtils.FROZEN_TARGETS.values())
    checked_any = False
    for component in lc.builtin_components():
        if component.frozen_name:
            checked_any = True
            assert component.frozen_name in frozen_values
    assert checked_any


# --- spawn_client argv/env/detach construction ---

def test_spawn_client_builds_argv_and_env_windows(monkeypatch):
    # DETACHED_PROCESS/CREATE_NEW_PROCESS_GROUP only exist on the stdlib subprocess
    # module under `if _mswindows:`, so they're absent on POSIX Pythons; CI runs this
    # suite on ubuntu/macos too, so stand in real Windows values (raising=False handles
    # the on-Windows case where the attributes already exist).
    monkeypatch.setattr(BaseUtils.subprocess, "DETACHED_PROCESS", 0x00000008, raising=False)
    monkeypatch.setattr(BaseUtils.subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200, raising=False)
    monkeypatch.setattr(BaseUtils, "is_frozen", lambda: False)
    monkeypatch.setattr(BaseUtils, "is_windows", True)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(BaseUtils.subprocess, "Popen", fake_popen)

    BaseUtils.spawn_client("kh2", server_address="localhost:38281", slot_name="P1", password="secret",
                           client_type="game")

    argv = captured["argv"]
    assert argv[:2] == [sys.executable, BaseUtils.local_path("MultiWorld.py")]
    assert argv[argv.index("--game") + 1] == "kh2"
    assert argv[argv.index("--server-address") + 1] == "localhost:38281"
    assert argv[argv.index("--slot-name") + 1] == "P1"
    assert argv[argv.index("--password") + 1] == "secret"
    assert argv[argv.index("--client-type") + 1] == "game"

    env = captured["kwargs"]["env"]
    assert env["MWGG_ROLE"] == "client"
    assert env["MWGG_CLIENT_TYPE"] == "game"
    assert env["MWGG_NO_SPLASH"] == "1"
    assert captured["kwargs"]["creationflags"] == (
        BaseUtils.subprocess.DETACHED_PROCESS | BaseUtils.subprocess.CREATE_NEW_PROCESS_GROUP
    )
    assert "start_new_session" not in captured["kwargs"]


def test_spawn_client_builds_argv_and_env_posix(monkeypatch):
    monkeypatch.setattr(BaseUtils, "is_frozen", lambda: False)
    monkeypatch.setattr(BaseUtils, "is_windows", False)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(BaseUtils.subprocess, "Popen", fake_popen)

    BaseUtils.spawn_client(client_type="text", extra_args=("--foo",))

    argv = captured["argv"]
    assert "--game" not in argv
    assert "--server-address" not in argv
    assert argv[argv.index("--client-type") + 1] == "text"
    assert argv[-1] == "--foo"

    env = captured["kwargs"]["env"]
    assert env["MWGG_ROLE"] == "client"
    assert env["MWGG_CLIENT_TYPE"] == "text"
    assert env["MWGG_NO_SPLASH"] == "1"
    assert captured["kwargs"]["start_new_session"] is True
    assert "creationflags" not in captured["kwargs"]


def test_spawn_client_component_flag(monkeypatch):
    monkeypatch.setattr(BaseUtils, "is_frozen", lambda: False)
    monkeypatch.setattr(BaseUtils, "is_windows", False)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(BaseUtils.subprocess, "Popen", fake_popen)

    BaseUtils.spawn_client(game="kh2", component="Map Tracker")

    argv = captured["argv"]
    assert argv[argv.index("--game") + 1] == "kh2"
    assert argv[argv.index("--component") + 1] == "Map Tracker"
    # Additive contract: --component goes after --client-type, so component-less
    # argv stays byte-identical to older cores.
    assert argv.index("--component") > argv.index("--client-type")

    env = captured["kwargs"]["env"]
    assert env["MWGG_ROLE"] == "client"
    assert env["MWGG_NO_SPLASH"] == "1"


def test_spawn_client_component_requires_game(monkeypatch):
    monkeypatch.setattr(BaseUtils, "is_frozen", lambda: False)
    monkeypatch.setattr(BaseUtils, "is_windows", False)

    def _fail_popen(*args, **kwargs):
        raise AssertionError("Popen must not run when spawn_client validation fails")

    monkeypatch.setattr(BaseUtils.subprocess, "Popen", _fail_popen)

    with pytest.raises(ValueError):
        BaseUtils.spawn_client(component="Map Tracker")


def test_spawn_client_launch_file_is_positional_before_flags(monkeypatch):
    monkeypatch.setattr(BaseUtils, "is_frozen", lambda: False)
    monkeypatch.setattr(BaseUtils, "is_windows", False)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        return object()

    monkeypatch.setattr(BaseUtils.subprocess, "Popen", fake_popen)

    BaseUtils.spawn_client(launch_file="C:/seed.apkh3")

    argv = captured["argv"]
    launch_index = argv.index("C:/seed.apkh3")
    assert argv[launch_index + 1] == "--client-type"


# --- origin classification / builtin_components / find_component ---

def test_builtin_components_excludes_component_appended_after_flip():
    marker = lc.Component("Late Marker Component", func=lambda *a: None)
    lc.components.append(marker)
    try:
        assert marker in lc.components
        assert marker not in lc.builtin_components()
    finally:
        lc.components.remove(marker)


def test_builtin_components_includes_known_builtins():
    names = {c.display_name for c in lc.builtin_components()}
    assert {"Host", "Generate", "Install APWorld", "Text Client", "Export Datapackage"} <= names


def test_find_component_matches_display_name_and_script_name():
    host_by_display = lc.find_component("Host")
    host_by_script = lc.find_component("MultiServer")
    assert host_by_display is not None
    assert host_by_display is host_by_script


def test_find_component_no_match_returns_none():
    assert lc.find_component("Definitely Not A Real Component") is None


# --- the synthesized YAML strip entry ---

def test_yaml_component_is_a_world_tool():
    """Frontends render it through the same WorldTool shape as scanned
    components, so there is one dataclass rather than a per-frontend clone."""
    entry = lc.yaml_component("oot")

    assert isinstance(entry, lc.WorldTool)
    assert entry.module == "oot"
    assert entry.type == "yaml"
    assert entry.name == lc.YAML_COMPONENT_NAME


def test_yaml_type_is_not_manifest_declarable():
    """The YAML entry is the frontend's own; a world must not be able to
    declare one and have it rendered as if core synthesized it."""
    assert "yaml" not in lc._MANIFEST_COMPONENT_TYPES
    assert lc._coerce_manifest_component(
        {"name": "Sneaky", "type": "yaml"}, "world.apworld") is None


# --- worlds.LauncherComponents re-export shim ---

def test_worlds_shim_shares_objects_with_top_level_module():
    """World modules keep importing worlds.LauncherComponents; the shim must
    hand them the very same objects (identity, not equality) so registrations
    land in the one live registry the launcher renders."""
    import worlds.LauncherComponents as wlc

    assert wlc.components is lc.components
    assert wlc.Component is lc.Component
    assert wlc.Type is lc.Type
    assert wlc.spawn_client is BaseUtils.spawn_client
    assert wlc.find_component is lc.find_component


def test_top_level_module_never_imports_worlds_package():
    """The point of the top-level module: launcher-side consumers import it
    without executing worlds/__init__, whose one-shot world load belongs to
    client processes only. Subprocess because this suite already has worlds
    in sys.modules."""
    import subprocess
    code = ("import sys\n"
            "import LauncherComponents\n"
            "assert 'worlds' not in sys.modules\n")
    result = subprocess.run([sys.executable, "-c", code], cwd=Utils.local_path(),
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
