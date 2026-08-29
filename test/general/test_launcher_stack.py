"""Launcher stack tests (entry points, components, spawn/routing, connect URLs, installer refs); add new launcher-stack tests here."""

import json
import logging
import os
import re
import subprocess
import sys
import urllib.parse
import zipfile

import pytest

import BaseUtils
import Launcher
import LauncherComponents as lc
import ModuleUpdate
import MultiWorld
import Utils
from CommonClient import parse_connect_url, safe_avatar_source
from LauncherComponents import (Component, SuffixIdentifier, Type, components, get_exe, identify,
                                launch as launch_component, launch_subprocess)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


# --------------------------------------------------------------------------- #
# Entry-point split: MultiWorld.main()'s role computation and MWGG_ROLE
# assignment (assigned, never setdefault), the connect-address composer
# forwarded to spawned clients, the --client-type parser surface, splash
# gating (MWGG_NO_SPLASH escape hatch, MWGG_SKIP_UPDATE for spawned clients),
# and the thin Launcher.py dispatcher (headless --version before any heavy
# import, component dispatch, verbatim delegation to MultiWorld.main).
# --------------------------------------------------------------------------- #

def _parsed_args(argv=(), **overrides):
    """Parse argv like MultiWorld.main does, including the post-routing
    patch_module/patch_file attributes it stamps onto args."""
    args = MultiWorld.make_arg_parser().parse_args(list(argv))
    args.patch_module = None
    args.patch_file = None
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


# --- compute_role: client iff --game / --client-type / routed patch ---

def test_compute_role_bare_invocation_is_launcher():
    assert MultiWorld.compute_role(_parsed_args()) == "launcher"


def test_compute_role_game_is_client():
    assert MultiWorld.compute_role(_parsed_args(["--game", "kh2"])) == "client"


def test_compute_role_client_type_is_client():
    assert MultiWorld.compute_role(_parsed_args(["--client-type", "text"])) == "client"


def test_compute_role_routed_patch_is_client():
    args = _parsed_args(["seed.apkh3"], patch_module="kh3", patch_file="seed.apkh3")
    assert MultiWorld.compute_role(args) == "client"


def test_compute_role_connection_flags_alone_stay_launcher():
    """Server/slot/password without a game or client type seed the launcher's
    fields; they must not flip the process into client role."""
    args = _parsed_args(["--server-address", "localhost:38281", "--slot-name", "P1", "--password", "x"])
    assert MultiWorld.compute_role(args) == "launcher"


def test_compute_role_unrouted_launch_file_stays_launcher():
    """A positional that could not be routed leaves patch_module unset, so the
    graceful fallback lands in the launcher."""
    args = _parsed_args(["not_a_patch.zip"])
    assert MultiWorld.compute_role(args) == "launcher"


# --- assign_role_env: assignment, never setdefault ---

def test_assign_role_env_overwrites_stale_client_value(monkeypatch):
    """A spawned child inherits MWGG_ROLE=client from spawn_client's env; a
    launcher-role process must overwrite it, not setdefault around it."""
    monkeypatch.setenv("MWGG_ROLE", "client")
    assert MultiWorld.assign_role_env(_parsed_args()) == "launcher"
    assert os.environ["MWGG_ROLE"] == "launcher"


def test_assign_role_env_overwrites_stale_launcher_value(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "launcher")
    assert MultiWorld.assign_role_env(_parsed_args(["--game", "kh2"])) == "client"
    assert os.environ["MWGG_ROLE"] == "client"


def test_assign_role_env_sets_when_unset(monkeypatch):
    monkeypatch.delenv("MWGG_ROLE", raising=False)
    MultiWorld.assign_role_env(_parsed_args())
    assert os.environ["MWGG_ROLE"] == "launcher"


# --- parser: --client-type ---

@pytest.mark.parametrize("client_type", ["game", "text", "universal_tracker", "manual"])
def test_parser_accepts_client_type_choices(client_type):
    args = MultiWorld.make_arg_parser().parse_args(["--client-type", client_type])
    assert args.client_type == client_type


def test_parser_client_type_defaults_to_none():
    assert MultiWorld.make_arg_parser().parse_args([]).client_type is None


def test_parser_rejects_unknown_client_type(capsys):
    with pytest.raises(SystemExit):
        MultiWorld.make_arg_parser().parse_args(["--client-type", "bogus"])
    capsys.readouterr()  # swallow argparse's usage message


# --- _compose_connect_address ---

def test_compose_connect_address_none_without_server():
    assert MultiWorld._compose_connect_address(None, None, None) is None
    assert MultiWorld._compose_connect_address(None, "P1", "secret") is None
    assert MultiWorld._compose_connect_address("", "P1", None) is None


def test_compose_connect_address_bare_address_passes_through():
    assert MultiWorld._compose_connect_address("localhost:38281", None, None) == "localhost:38281"


def test_compose_connect_address_slot_only():
    assert MultiWorld._compose_connect_address("localhost:38281", "P1", None) == "P1@localhost:38281"


def test_compose_connect_address_slot_and_password():
    composed = MultiWorld._compose_connect_address("localhost:38281", "P1", "secret")
    assert composed == "P1:secret@localhost:38281"


def test_compose_connect_address_password_without_slot_is_dropped():
    """InitContext._set_server_address ignores a password with an empty
    username (urlparse yields username='' for ':pass@host'), so composing one
    would silently lose it anyway."""
    assert MultiWorld._compose_connect_address("localhost:38281", None, "secret") == "localhost:38281"


def test_compose_connect_address_existing_userinfo_not_double_composed():
    """The archipelago:// URL path pre-composes name@host:port into
    args.server_address AND sets args.slot_name; composing again would yield
    name@name@host:port."""
    assert MultiWorld._compose_connect_address("P1@localhost:38281", "P1", None) == "P1@localhost:38281"


def test_compose_connect_address_preserves_scheme():
    composed = MultiWorld._compose_connect_address("ws://localhost:38281", "P1", "secret")
    assert composed == "ws://P1:secret@localhost:38281"


def test_compose_connect_address_round_trips_through_urlparse():
    """The composed form must parse the way _set_server_address parses it
    (prefix "ws://", then urlparse userinfo/host/port), ports intact."""
    composed = MultiWorld._compose_connect_address("multiworld.gg:12345", "Slot One", "hunter2")
    parsed = urllib.parse.urlparse(f"ws://{composed}")
    assert parsed.username == "Slot One"
    assert parsed.password == "hunter2"
    assert parsed.hostname == "multiworld.gg"
    assert parsed.port == 12345


def test_compose_connect_address_warns_on_colon_in_slot_name(caplog):
    """A ':' in the slot name mis-splits downstream (InitContext partitions
    userinfo at the first colon, so 'P:1' parses as user P, password 1@...).
    Behavior is preserved - the composer warns, it does not reject."""
    with caplog.at_level(logging.WARNING, logger="MultiWorld"):
        composed = MultiWorld._compose_connect_address("localhost:38281", "P:1", None)
    assert composed == "P:1@localhost:38281"
    assert any("contains ':'" in record.message for record in caplog.records)


def test_compose_connect_address_no_warning_without_colon(caplog):
    with caplog.at_level(logging.WARNING, logger="MultiWorld"):
        MultiWorld._compose_connect_address("localhost:38281", "P1", "secret")
    assert not caplog.records


# --- _resolve_client_route: dead-client guard fallback matrix ---

def _resolve_with_role(args):
    """Mirror MultiWorld.main's flow: assign the role env from args, then
    resolve the route (which may fall the role back to launcher)."""
    MultiWorld.assign_role_env(args)
    return MultiWorld._resolve_client_route(args)


@pytest.mark.parametrize("argv", [
    ["--client-type", "universal_tracker"],
    ["--client-type", "manual"],
    ["--client-type", "game"],
])
def test_resolve_route_unroutable_client_type_falls_back_to_launcher(argv, monkeypatch, caplog):
    """--client-type without a routable --game computes role=client yet
    resolves no route; without the guard that boots a dead client GUI
    (console + permanent loading overlay, nothing ever launches)."""
    monkeypatch.setenv("MWGG_ROLE", "stale")  # registers teardown restore
    monkeypatch.setenv("MWGG_GAME", "stale")
    with caplog.at_level(logging.WARNING, logger="MultiWorld"):
        route_module, route_kwargs = _resolve_with_role(_parsed_args(argv))
    assert route_module is None
    assert route_kwargs == {}
    assert os.environ["MWGG_ROLE"] == "launcher"
    assert "MWGG_GAME" not in os.environ
    assert any("falling back to launcher" in record.message for record in caplog.records)


def test_resolve_route_unavailable_game_falls_back_to_launcher(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "stale")
    monkeypatch.setattr(Utils, "get_available_worlds", lambda: ["kh2"])
    route_module, route_kwargs = _resolve_with_role(_parsed_args(["--game", "not_installed"]))
    assert route_module is None
    assert route_kwargs == {}
    assert os.environ["MWGG_ROLE"] == "launcher"


def test_resolve_route_resolution_error_falls_back_to_launcher(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "stale")

    def boom():
        raise RuntimeError("world index unavailable")
    monkeypatch.setattr(Utils, "get_available_worlds", boom)
    route_module, route_kwargs = _resolve_with_role(_parsed_args(["--game", "kh2"]))
    assert route_module is None
    assert route_kwargs == {}
    assert os.environ["MWGG_ROLE"] == "launcher"


def test_resolve_route_available_game_stays_client(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "stale")
    monkeypatch.delenv("MWGG_GAME", raising=False)
    monkeypatch.setattr(Utils, "get_available_worlds", lambda: ["kh2"])
    args = _parsed_args(["--game", "kh2", "--server-address", "localhost:38281",
                         "--slot-name", "P1"])
    route_module, route_kwargs = _resolve_with_role(args)
    assert route_module == "kh2"
    assert route_kwargs["server_address"] == "P1@localhost:38281"
    assert route_kwargs["client_type"] == "game"
    assert os.environ["MWGG_ROLE"] == "client"
    # Exported for the client-role frontend's cover-art lookup.
    assert os.environ["MWGG_GAME"] == "kh2"


def test_resolve_route_text_client_sentinel_stays_client(monkeypatch):
    """client_type=="text" routes via the "" sentinel (a real route, hence
    the `is None` guard rather than a bool check)."""
    monkeypatch.setenv("MWGG_ROLE", "stale")
    monkeypatch.setenv("MWGG_GAME", "stale")
    route_module, route_kwargs = _resolve_with_role(_parsed_args(["--client-type", "text"]))
    assert route_module == ""
    assert route_kwargs == {"server_address": None, "client_type": "text"}
    assert os.environ["MWGG_ROLE"] == "client"
    # No game routed: a stale inherited value must not leak a wrong cover.
    assert "MWGG_GAME" not in os.environ


def test_resolve_route_routed_patch_stays_client(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "stale")
    monkeypatch.delenv("MWGG_GAME", raising=False)
    args = _parsed_args(["seed.apkh3"], patch_module="kh3",
                        patch_file="C:\\seeds\\seed.apkh3")
    route_module, route_kwargs = _resolve_with_role(args)
    assert route_module == "kh3"
    assert route_kwargs == {"patch_file": "C:\\seeds\\seed.apkh3"}
    assert os.environ["MWGG_ROLE"] == "client"
    assert os.environ["MWGG_GAME"] == "kh3"


def test_resolve_route_launcher_role_untouched(monkeypatch, caplog):
    """A launcher-role process (bare invocation) resolves no route and must
    not trip the guard or its warning."""
    monkeypatch.setenv("MWGG_ROLE", "stale")
    with caplog.at_level(logging.WARNING, logger="MultiWorld"):
        route_module, route_kwargs = _resolve_with_role(_parsed_args())
    assert route_module is None
    assert route_kwargs == {}
    assert os.environ["MWGG_ROLE"] == "launcher"
    assert not any("falling back to launcher" in record.message for record in caplog.records)


# --- splash gating ---

def test_splash_shown_on_windows_gui_cold_start(monkeypatch):
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    assert MultiWorld.should_show_splash("gui") is True


def test_splash_skipped_under_mwgg_no_splash(monkeypatch):
    """MWGG_NO_SPLASH is the manual escape hatch: the whole splash block,
    including the 60s wait, must skip."""
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.setenv("MWGG_NO_SPLASH", "1")
    assert MultiWorld.should_show_splash("gui") is False


def test_splash_still_shown_under_mwgg_skip_update(monkeypatch):
    """spawn_client sets MWGG_SKIP_UPDATE=1 in the child env; that skips the
    updater (inline here, in-thread in the splash process), not the splash
    itself -- spawned clients front their boot with it too."""
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    monkeypatch.setenv("MWGG_SKIP_UPDATE", "1")
    assert MultiWorld.should_show_splash("gui") is True


def test_splash_skipped_for_tui_frontend(monkeypatch):
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    assert MultiWorld.should_show_splash("tui") is False


def test_splash_skipped_off_windows(monkeypatch):
    monkeypatch.setattr(MultiWorld, "is_windows", False)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    assert MultiWorld.should_show_splash("gui") is False


# --- client component unwrapping (in-process launch) ---

def _inner_launch(*args):
    """Stands in for a world's Client.launch."""


def _launch_subprocess_wrapper(*args):
    launch_subprocess(_inner_launch, name="TestClient", args=args)


def _launch_component_wrapper(*args):
    launch_component(_inner_launch, name="TestClient", args=args)


def _opaque_wrapper(*args):
    print(_inner_launch)


def test_unwrap_launch_subprocess_wrapper():
    """Wheel worlds that ship the upstream launch_subprocess(<launch>) wrapper
    must unwrap to the inner callable so the client launches in-process instead
    of spawning a second GUI process."""
    assert Utils._resolve_launch_from_custom_world(_launch_subprocess_wrapper, "worlds.x") is _inner_launch


def test_unwrap_launch_component_wrapper():
    assert Utils._resolve_launch_from_custom_world(_launch_component_wrapper, "worlds.x") is _inner_launch


def test_unwrap_unrecognized_wrapper_returns_none():
    assert Utils._resolve_launch_from_custom_world(_opaque_wrapper, "worlds.x") is None


# --- Launcher.py dispatcher ---

def test_launcher_version_prints_and_returns_zero(capsys):
    assert Launcher.main(["--version"]) == 0
    out = capsys.readouterr().out
    assert BaseUtils.__version__ in out


def test_launcher_help_returns_zero(capsys):
    assert Launcher.main(["--help"]) == 0
    out = capsys.readouterr().out
    assert "MultiworldGGLauncher" in out


@pytest.mark.parametrize("argv", [["--frontend=tui"], ["--frontend", "tui"]])
def test_launcher_rejects_tui_frontend(argv, capsys):
    assert Launcher.main(argv) == 2
    err = capsys.readouterr().err
    assert "--frontend=tui" in err


def test_launcher_gui_frontend_is_not_rejected(monkeypatch):
    """--frontend gui must fall through to MultiWorld.main, argv verbatim."""
    calls = []
    monkeypatch.setattr(MultiWorld, "main", lambda argv=None: calls.append(argv))
    assert Launcher.main(["--frontend", "gui"]) == 0
    assert calls == [["--frontend", "gui"]]


def test_launcher_runs_component_and_joins_processes(monkeypatch):
    ran = {}
    fake = lc.Component("Entry Point Test Component", func=lambda *a: None)
    monkeypatch.setattr(lc, "find_component",
                        lambda name: fake if name == "Entry Point Test Component" else None)
    monkeypatch.setattr(lc, "run_component", lambda component, *a: ran.update(component=component, args=a))
    monkeypatch.setattr(Utils, "init_logging", lambda name, *a, **kw: ran.update(logging=name))

    assert Launcher.main(["Entry Point Test Component", "one", "two"]) == 0
    assert ran["component"] is fake
    assert ran["args"] == ("one", "two")
    assert ran["logging"] == "Launcher"


def test_launcher_delegates_unmatched_positional_verbatim(monkeypatch):
    """A patch/URL positional is not a component: the untouched argv goes to
    MultiWorld.main, whose parser owns the launch_file positional."""
    calls = []
    monkeypatch.setattr(MultiWorld, "main", lambda argv=None: calls.append(argv))
    assert Launcher.main(["C:\\seeds\\seed.aplttp", "--loglevel", "info"]) == 0
    assert calls == [["C:\\seeds\\seed.aplttp", "--loglevel", "info"]]


def test_launcher_bare_invocation_delegates_to_launcher_mode(monkeypatch):
    calls = []
    monkeypatch.setattr(MultiWorld, "main", lambda argv=None: calls.append(argv))
    assert Launcher.main([]) == 0
    assert calls == [[]]


def test_launcher_version_subprocess_is_fast_and_headless():
    """CI smokes `Launcher --version` headless on Linux: it must exit 0
    without importing Kivy, MultiWorld, or the worlds package. Runs in a clean
    subprocess (test_client_compat.py pattern) because a fresh interpreter is the
    only rigorous way to assert what got imported."""
    script = (
        "import sys, runpy\n"
        "sys.argv = ['Launcher.py', '--version']\n"
        "code = 0\n"
        "try:\n"
        "    runpy.run_path('Launcher.py', run_name='__main__')\n"
        "except SystemExit as e:\n"
        "    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)\n"
        "assert code == 0, f'exit {code}'\n"
        "assert 'kivy' not in sys.modules, 'Kivy was imported for --version'\n"
        "assert 'MultiWorld' not in sys.modules, 'MultiWorld was imported for --version'\n"
        "assert 'worlds' not in sys.modules, 'worlds was imported for --version'\n"
        "print('LAUNCHER_VERSION_OK')\n"
    )
    result = subprocess.run([sys.executable, "-c", script], cwd=REPO_ROOT,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "LAUNCHER_VERSION_OK" in result.stdout


def test_launcher_py_version_exits_zero_as_own_process():
    result = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "Launcher.py"), "--version"],
                            cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert BaseUtils.__version__ in result.stdout


# --------------------------------------------------------------------------- #
# Launcher component surface: FROZEN_TARGETS as the single source of truth
# for built exe names, BaseUtils.spawn_client's argv/env/detach
# construction, the builtin/other component-origin classification that keeps
# builtin_components() trustworthy, the install_apworld confirm gate, and the
# worlds.LauncherComponents re-export shim.
# --------------------------------------------------------------------------- #

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
    assert env["MWGG_SKIP_UPDATE"] == "1"
    assert "MWGG_NO_SPLASH" not in env
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
    assert env["MWGG_SKIP_UPDATE"] == "1"
    assert "MWGG_NO_SPLASH" not in env
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
    assert env["MWGG_SKIP_UPDATE"] == "1"


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


# --- install_apworld confirm gate / Utils.messagebox_confirm cascade ---

def test_install_apworld_declines_without_confirm(monkeypatch):
    monkeypatch.setattr(lc, "is_kivy_running", lambda: False)
    monkeypatch.setattr(Utils, "messagebox_confirm", lambda title, text: False)
    installed = []
    monkeypatch.setattr(lc, "_install_apworld", lambda path="": installed.append(path))
    boxes = []
    monkeypatch.setattr(Utils, "messagebox", lambda *args, **kwargs: boxes.append((args, kwargs)))

    lc.install_apworld("C:/downloads/some.apworld")

    assert installed == []
    assert boxes == []


def test_install_apworld_proceeds_on_confirm(monkeypatch):
    monkeypatch.setattr(lc, "is_kivy_running", lambda: False)
    monkeypatch.setattr(Utils, "messagebox_confirm", lambda title, text: True)
    installed = []
    monkeypatch.setattr(lc, "_install_apworld", lambda path="": installed.append(path) or None)

    lc.install_apworld("C:/downloads/some.apworld")

    assert installed == ["C:/downloads/some.apworld"]


def test_install_apworld_skips_native_confirm_when_kivy_running(monkeypatch):
    # the GUI pre-confirms with its own dialog; a second native confirm would
    # double-warn every GUI install
    monkeypatch.setattr(lc, "is_kivy_running", lambda: True)

    def _fail_confirm(*args, **kwargs):
        raise AssertionError("core confirm must not fire when the GUI pre-confirms")

    monkeypatch.setattr(Utils, "messagebox_confirm", _fail_confirm)
    installed = []
    monkeypatch.setattr(lc, "_install_apworld", lambda path="": installed.append(path) or None)

    lc.install_apworld("C:/downloads/some.apworld")

    assert installed == ["C:/downloads/some.apworld"]


def test_messagebox_confirm_auto_confirms_without_gui(monkeypatch):
    monkeypatch.setattr(Utils, "gui_enabled", False)
    assert Utils.messagebox_confirm("Title", "text") is True


def test_messagebox_confirm_auto_confirms_under_kivy(monkeypatch, caplog):
    monkeypatch.setattr(Utils, "gui_enabled", True)
    monkeypatch.setattr(Utils, "is_kivy_running", lambda: True)
    with caplog.at_level(logging.WARNING):
        assert Utils.messagebox_confirm("Title", "text") is True
    assert any("pre-confirm" in record.message for record in caplog.records)


def test_messagebox_confirm_textual_branch_beats_native_backends(monkeypatch, caplog):
    # a running TUI must not fall through to a blocking native dialog
    import ctypes

    monkeypatch.setattr(Utils, "gui_enabled", True)
    monkeypatch.setattr(Utils, "is_kivy_running", lambda: False)
    monkeypatch.setattr(Utils, "is_textual_running", lambda: True)
    monkeypatch.setattr(Utils, "is_linux", False)
    monkeypatch.setattr(Utils, "is_windows", True)

    class _Tripwire:
        def __getattr__(self, name):
            raise AssertionError("native dialog must not open under a running TUI")

    monkeypatch.setattr(ctypes, "windll", _Tripwire(), raising=False)
    with caplog.at_level(logging.WARNING):
        assert Utils.messagebox_confirm("Title", "text") is True
    assert any("pre-confirm" in record.message for record in caplog.records)


@pytest.mark.parametrize("box_result, expected", [(1, True), (2, False)])
def test_messagebox_confirm_windows_okcancel(monkeypatch, box_result, expected):
    import ctypes

    monkeypatch.setattr(Utils, "gui_enabled", True)
    monkeypatch.setattr(Utils, "is_kivy_running", lambda: False)
    monkeypatch.setattr(Utils, "is_textual_running", lambda: False)
    monkeypatch.setattr(Utils, "is_linux", False)
    monkeypatch.setattr(Utils, "is_windows", True)
    calls = {}

    class _User32:
        @staticmethod
        def MessageBoxW(hwnd, text, title, style):
            calls.update(text=text, title=title, style=style)
            return box_result

    class _WinDLL:
        user32 = _User32()

    monkeypatch.setattr(ctypes, "windll", _WinDLL(), raising=False)

    assert Utils.messagebox_confirm("Install APWorld?", "body") is expected
    assert calls["style"] == 0x31  # MB_OKCANCEL | MB_ICONWARNING


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


# --------------------------------------------------------------------------- #
# Named-client-component launch path (--component):
# spawn_client(component=...) appends `--component <display_name>` to the
# child argv; the child forwards it through _resolve_client_route's
# route_kwargs and Utils._perform_module_launch resolves it via
# Utils._resolve_named_client_component -- a module-scoped scan that must
# never let another world's registrations be reachable by name, and must
# fall back to default client resolution (never die) on an unknown or
# non-client name.
# --------------------------------------------------------------------------- #

def _fake_launch(*args):
    pass


def _other_launch(*args):
    pass


@pytest.fixture
def registered(request):
    """Append Components to the live registry and always remove them."""
    added: list[lc.Component] = []

    def _register(component: lc.Component) -> lc.Component:
        lc.components.append(component)
        added.append(component)
        return component

    yield _register
    for component in added:
        lc.components.remove(component)


def test_resolve_named_client_component_scoped_match(registered, monkeypatch):
    monkeypatch.setattr(_fake_launch, "__module__", "worlds.kh2.submod", raising=False)
    monkeypatch.setattr(_other_launch, "__module__", "worlds.other", raising=False)
    registered(lc.Component("Alt Client", func=_other_launch, component_type=lc.Type.CLIENT))
    target = registered(lc.Component("Alt Client", func=_fake_launch, component_type=lc.Type.CLIENT))

    resolved = Utils._resolve_named_client_component("worlds.kh2", "Alt Client")

    assert resolved is target.func


def test_resolve_named_client_component_rejects_other_modules(registered, monkeypatch, caplog):
    monkeypatch.setattr(_other_launch, "__module__", "worlds.other", raising=False)
    registered(lc.Component("Alt Client", func=_other_launch, component_type=lc.Type.CLIENT))

    with caplog.at_level(logging.WARNING):
        resolved = Utils._resolve_named_client_component("worlds.kh2", "Alt Client")

    assert resolved is None
    assert any("falling back" in record.message for record in caplog.records)


def test_resolve_named_client_component_rejects_non_client_types(registered, monkeypatch, caplog):
    monkeypatch.setattr(_fake_launch, "__module__", "worlds.kh2", raising=False)
    registered(lc.Component("KH2 Fixup", func=_fake_launch, component_type=lc.Type.TOOL))

    with caplog.at_level(logging.WARNING):
        resolved = Utils._resolve_named_client_component("worlds.kh2", "KH2 Fixup")

    assert resolved is None


def test_resolve_client_route_forwards_component(monkeypatch):
    import MultiWorld

    monkeypatch.setattr(Utils, "get_available_worlds", lambda: {"kh2"})
    args = MultiWorld.make_arg_parser().parse_args(
        ["--game", "kh2", "--component", "Alt Client"])

    route_module, route_kwargs = MultiWorld._resolve_client_route(args)

    assert route_module == "kh2"
    assert route_kwargs["component"] == "Alt Client"


def test_resolve_client_route_component_defaults_to_none(monkeypatch):
    import MultiWorld

    monkeypatch.setattr(Utils, "get_available_worlds", lambda: {"kh2"})
    args = MultiWorld.make_arg_parser().parse_args(["--game", "kh2"])

    _route_module, route_kwargs = MultiWorld._resolve_client_route(args)

    assert route_kwargs["component"] is None


# --------------------------------------------------------------------------- #
# Patch-file routing: opening a patch file (OS file-association
# double-click or CLI positional) must launch the right game client with
# it. Guards the pieces the flow is built from: the optional positional
# file/URL on MultiWorld's parser (installer file associations point at
# `MultiworldGG.exe "%1"`, once an unrecognized argument / SystemExit 2),
# Utils.read_patch_game_name (root archipelago.json, no world imports),
# Utils._client_launch_argv (positional patch file first, then
# --connect/--name), and LauncherComponents.identify/get_exe routing of
# non-patch files (e.g. a .archipelago multidata).
# --------------------------------------------------------------------------- #

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
    monkeypatch.setattr(lc, "is_frozen", lambda: True)
    monkeypatch.setattr(lc, "is_windows", True)

    host = next(c for c in components if c.display_name == "Host")
    generate = next(c for c in components if c.display_name == "Generate")

    assert get_exe(host) == [lc.local_path("MultiworldGGServer.exe")]
    assert get_exe(generate) == [lc.local_path("MultiworldGGGenerate.exe")]


# --------------------------------------------------------------------------- #
# mwgg:// launch-URL parser and avatar gate (deep-link PR4): a website
# "Connect via Game Client" link decomposes into connection prefs + the
# chosen avatar, which get persisted before the GUI opens (backs
# MultiWorld.py's protocol-launch handling).
# --------------------------------------------------------------------------- #

def test_parse_full_room_link():
    url = ("mwgg://FlatDelilah:None@mw.prismativerse.com:62252"
           "?game=A%20Link%20to%20the%20Past&room=abc"
           "&avatar=https%3A%2F%2Fmw.prismativerse.com%2Favatar%2Fabc.png")
    parsed = parse_connect_url(url)
    assert parsed["hostname"] == "mw.prismativerse.com"
    assert parsed["port"] == 62252
    assert parsed["name"] == "FlatDelilah"
    assert parsed["password"] is None  # :None@ encodes "no password"
    assert parsed["game"] == "A Link to the Past"
    assert parsed["avatar"] == "https://mw.prismativerse.com/avatar/abc.png"


def test_parse_archipelago_scheme_and_real_password():
    parsed = parse_connect_url("archipelago://name:secret@host:38281")
    assert parsed["hostname"] == "host"
    assert parsed["port"] == 38281
    assert parsed["name"] == "name"
    assert parsed["password"] == "secret"


def test_parse_rejects_non_connection_urls():
    assert parse_connect_url("https://example.com") is None
    assert parse_connect_url("/path/to/patch.aplttp") is None
    assert parse_connect_url("") is None
    assert parse_connect_url(None) is None


def test_safe_avatar_source_allows_trusted_https():
    for url in ("https://mw.prismativerse.com/avatar/abc.png",
                "https://multiworld.gg/avatar/abc.png"):
        assert safe_avatar_source(url) == url


def test_safe_avatar_source_rejects_untrusted_or_insecure():
    assert safe_avatar_source("https://evil.example/x.png") == ""
    assert safe_avatar_source("http://multiworld.gg/avatar/x.png") == ""  # not https
    assert safe_avatar_source("") == ""
    assert safe_avatar_source("not a url") == ""


# --------------------------------------------------------------------------- #
# inno_setup.iss lint: {app}\<name>.exe references setup.py doesn't build.
# The allowed set is derived, not hand-maintained: every literal
# target_name in setup.py, every BaseUtils.FROZEN_TARGETS value, plus the
# LauncherDebug name setup.py derives at build time (it has no
# FROZEN_TARGETS entry of its own).
# --------------------------------------------------------------------------- #

_INNO_PATH = Utils.local_path("inno_setup.iss")

# Historically stale exe names, kept as an explicit regression guard on top of the
# derived allow-list (a name could start being built for unrelated reasons).
_KNOWN_STALE_NAMES = {
    "MultiworldGGBizHawkClient",
    "MultiworldGGSNIClient",
    "ArchipelagoBizHawkClient",
    # pre-2026-08 capital-W names, retired when every exe took the
    # MultiworldGG prefix (upstream instance_name convention)
    "MultiWorldGG",
    "MultiWorldGGServer",
    "MultiWorldGGGenerate",
    "MultiWorldGGPatch",
    "MultiWorldGGClientDebug",
}

def _known_built_exe_names() -> set[str]:
    """Every exe base name (no .exe) that setup.py is known to build."""
    names = _setup_py_target_names() | set(BaseUtils.FROZEN_TARGETS.values())
    # LauncherDebug is derived in setup.py (_launcher_debug_exe_name), never a
    # quoted literal, so _setup_py_target_names() can't see it.
    names.add(BaseUtils.FROZEN_TARGETS["Launcher"] + "Debug")
    names.discard("")
    return names


def _inno_exe_references() -> list[str]:
    with open(_INNO_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    return re.findall(r"\{app\}\\(\w+\.exe)", text)


def test_inno_exe_references_resolve_to_a_built_executable():
    allowed = {f"{name}.exe" for name in _known_built_exe_names()}
    references = _inno_exe_references()
    assert references, "expected to find at least one {app}\\<name>.exe reference in inno_setup.iss"

    stale = sorted(set(references) - allowed)
    assert not stale, (
        f"inno_setup.iss references exe(s) setup.py doesn't build: {stale}. "
        f"Known-built names: {sorted(allowed)}"
    )


def test_inno_has_no_known_stale_exe_references():
    references = {ref[:-4] for ref in _inno_exe_references()}
    stale_hits = references & _KNOWN_STALE_NAMES
    assert not stale_hits, f"inno_setup.iss still references retired exe(s): {sorted(stale_hits)}"


def test_inno_app_exe_name_is_the_launcher():
    with open(_INNO_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    match = re.search(r'#define MyAppExeName "([^"]+)"', text)
    assert match, "expected a #define MyAppExeName line in inno_setup.iss"
    assert match.group(1) == f"{BaseUtils.FROZEN_TARGETS['Launcher']}.exe"


# --------------------------------------------------------------------------- #
# Inno's predownload step (--update-modules -> MultiWorld._run_predownload).
# Must never raise out to Inno's [Run] entry (non-fatal by design: worlds also
# install on demand at first launch) but must make failures observable --
# the prior implementation only wrote a log on a *raised* exception, so a
# "successful" no-op (e.g. install_worlds silently skipping because it thinks
# the venv is read-only) left zero trace anywhere.
# --------------------------------------------------------------------------- #

@pytest.fixture
def _predownload_stub(monkeypatch, tmp_path):
    """Route diagnostics to a temp file and stub uv discovery (irrelevant to
    these tests, which control ModuleUpdate's behavior directly)."""
    log_path = tmp_path / "predownload.log"
    monkeypatch.setattr(MultiWorld, "_predownload_log_paths", lambda: [str(log_path)])
    monkeypatch.setattr(MultiWorld, "_ensure_uv_discoverable", lambda: None)
    original_level = logging.getLogger().level
    yield log_path
    logging.getLogger().setLevel(original_level)


def test_predownload_logs_diagnostic_when_venv_unhealthy_without_raising(monkeypatch, _predownload_stub, capsys):
    monkeypatch.setattr(ModuleUpdate, "install_worlds", lambda worlds: ModuleUpdate.WorldInstallResult())
    monkeypatch.setattr(ModuleUpdate, "venv_is_healthy", lambda path: False)
    monkeypatch.setattr(ModuleUpdate, "install_path", lambda: _predownload_stub.parent)
    monkeypatch.setattr("importlib.util.find_spec", lambda name: object())

    MultiWorld._run_predownload(["mwgg_igdb_nr"])

    assert "Unable to fully predownload" in capsys.readouterr().out
    assert "venv_healthy=False" in _predownload_stub.read_text(encoding="utf-8")


def test_predownload_swallows_exceptions_and_logs_traceback(monkeypatch, _predownload_stub, capsys):
    def _boom(worlds):
        raise RuntimeError("uv exploded")

    monkeypatch.setattr(ModuleUpdate, "install_worlds", _boom)

    MultiWorld._run_predownload(["mwgg_igdb_nr"])  # must not raise

    assert "Unable to predownload" in capsys.readouterr().out
    assert "uv exploded" in _predownload_stub.read_text(encoding="utf-8")


def test_predownload_is_quiet_on_full_success(monkeypatch, _predownload_stub, capsys):
    monkeypatch.setattr(ModuleUpdate, "install_worlds", lambda worlds: ModuleUpdate.WorldInstallResult())
    monkeypatch.setattr(ModuleUpdate, "venv_is_healthy", lambda path: True)
    monkeypatch.setattr(ModuleUpdate, "install_path", lambda: _predownload_stub.parent)
    monkeypatch.setattr("importlib.util.find_spec", lambda name: object())

    MultiWorld._run_predownload(["mwgg_igdb_nr"])

    assert "Unable" not in capsys.readouterr().out


def test_predownload_reports_failed_worlds(monkeypatch, _predownload_stub, capsys):
    result = ModuleUpdate.WorldInstallResult()
    result.failed.append("worlds.hk")
    monkeypatch.setattr(ModuleUpdate, "install_worlds", lambda worlds: result)
    monkeypatch.setattr(ModuleUpdate, "venv_is_healthy", lambda path: True)
    monkeypatch.setattr(ModuleUpdate, "install_path", lambda: _predownload_stub.parent)
    monkeypatch.setattr("importlib.util.find_spec", lambda name: object())

    MultiWorld._run_predownload(["mwgg_igdb_nr", "worlds.hk"])

    assert "Unable to fully predownload" in capsys.readouterr().out
    assert "worlds.hk" in _predownload_stub.read_text(encoding="utf-8")
