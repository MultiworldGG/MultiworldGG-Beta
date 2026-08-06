"""Tests for the Phase 2 entry-point split: MultiWorld.main()'s role
computation and MWGG_ROLE assignment (assigned, never setdefault), the
connect-address composer forwarded to spawned clients, the --client-type
parser surface, splash gating under MWGG_NO_SPLASH, and the thin Launcher.py
dispatcher (headless --version before any heavy import, component dispatch,
verbatim delegation to MultiWorld.main).
"""
import logging
import os
import subprocess
import sys
import urllib.parse

import pytest

import BaseUtils
import Launcher
import MultiWorld
import Utils
import worlds.LauncherComponents as lc

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
    Behavior is preserved — the composer warns, it does not reject."""
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
    with caplog.at_level(logging.WARNING, logger="MultiWorld"):
        route_module, route_kwargs = _resolve_with_role(_parsed_args(argv))
    assert route_module is None
    assert route_kwargs == {}
    assert os.environ["MWGG_ROLE"] == "launcher"
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
    monkeypatch.setattr(Utils, "get_available_worlds", lambda: ["kh2"])
    args = _parsed_args(["--game", "kh2", "--server-address", "localhost:38281",
                         "--slot-name", "P1"])
    route_module, route_kwargs = _resolve_with_role(args)
    assert route_module == "kh2"
    assert route_kwargs["server_address"] == "P1@localhost:38281"
    assert route_kwargs["client_type"] == "game"
    assert os.environ["MWGG_ROLE"] == "client"


def test_resolve_route_text_client_sentinel_stays_client(monkeypatch):
    """client_type=="text" routes via the "" sentinel (a real route, hence
    the `is None` guard rather than a bool check)."""
    monkeypatch.setenv("MWGG_ROLE", "stale")
    route_module, route_kwargs = _resolve_with_role(_parsed_args(["--client-type", "text"]))
    assert route_module == ""
    assert route_kwargs == {"server_address": None, "client_type": "text"}
    assert os.environ["MWGG_ROLE"] == "client"


def test_resolve_route_routed_patch_stays_client(monkeypatch):
    monkeypatch.setenv("MWGG_ROLE", "stale")
    args = _parsed_args(["seed.apkh3"], patch_module="kh3",
                        patch_file="C:\\seeds\\seed.apkh3")
    route_module, route_kwargs = _resolve_with_role(args)
    assert route_module == "kh3"
    assert route_kwargs == {"patch_file": "C:\\seeds\\seed.apkh3"}
    assert os.environ["MWGG_ROLE"] == "client"


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
    """spawn_client sets MWGG_NO_SPLASH=1 in the child env (there is no CLI
    flag); the whole splash block, including the 60s update wait, must skip."""
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.setenv("MWGG_NO_SPLASH", "1")
    assert MultiWorld.should_show_splash("gui") is False


def test_splash_skipped_for_tui_frontend(monkeypatch):
    monkeypatch.setattr(MultiWorld, "is_windows", True)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    assert MultiWorld.should_show_splash("tui") is False


def test_splash_skipped_off_windows(monkeypatch):
    monkeypatch.setattr(MultiWorld, "is_windows", False)
    monkeypatch.delenv("MWGG_NO_SPLASH", raising=False)
    assert MultiWorld.should_show_splash("gui") is False


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
    subprocess (test_kvui_tui.py pattern) because a fresh interpreter is the
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
