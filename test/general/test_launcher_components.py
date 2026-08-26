"""Tests for worlds.LauncherComponents: the standalone Launcher process (Phase 1
foundations) contract -- FROZEN_TARGETS as the single source of truth for built
exe names, spawn_client's argv/env/detach construction, and the builtin/other
component-origin classification that keeps builtin_components() trustworthy.
"""
import re

import BaseUtils
import Utils
import worlds.LauncherComponents as lc


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
    monkeypatch.setattr(lc.subprocess, "DETACHED_PROCESS", 0x00000008, raising=False)
    monkeypatch.setattr(lc.subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200, raising=False)
    monkeypatch.setattr(lc, "is_frozen", lambda: False)
    monkeypatch.setattr(lc, "is_windows", True)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(lc.subprocess, "Popen", fake_popen)

    lc.spawn_client("kh2", server_address="localhost:38281", slot_name="P1", password="secret",
                    client_type="game")

    argv = captured["argv"]
    assert argv[:2] == [lc.sys.executable, lc.local_path("MultiWorld.py")]
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
        lc.subprocess.DETACHED_PROCESS | lc.subprocess.CREATE_NEW_PROCESS_GROUP
    )
    assert "start_new_session" not in captured["kwargs"]


def test_spawn_client_builds_argv_and_env_posix(monkeypatch):
    monkeypatch.setattr(lc, "is_frozen", lambda: False)
    monkeypatch.setattr(lc, "is_windows", False)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(lc.subprocess, "Popen", fake_popen)

    lc.spawn_client(client_type="text", extra_args=("--foo",))

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


def test_spawn_client_launch_file_is_positional_before_flags(monkeypatch):
    monkeypatch.setattr(lc, "is_frozen", lambda: False)
    monkeypatch.setattr(lc, "is_windows", False)
    captured = {}

    def fake_popen(argv, **kwargs):
        captured["argv"] = argv
        return object()

    monkeypatch.setattr(lc.subprocess, "Popen", fake_popen)

    lc.spawn_client(launch_file="C:/seed.apkh3")

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
