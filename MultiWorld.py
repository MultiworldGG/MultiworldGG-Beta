from multiprocessing import freeze_support, Process, Queue, set_start_method
import argparse
import asyncio
import sys
import logging
import os
import re
import subprocess
import time
from importlib import metadata
from argparse import ArgumentParser

os.environ["KIVY_NO_CONSOLELOG"] = "0"
os.environ["KIVY_NO_FILELOG"] = "0"
os.environ["KIVY_LOG_ENABLE"] = "1"
# Disable Kivy's own CLI argument parsing so our argparse (and --frontend in
# particular) doesn't get intercepted on dev runs. Frozen builds already set
# this below; doing it unconditionally is safe since we never use Kivy's CLI args.
os.environ["KIVY_NO_ARGS"] = "1"

from BaseUtils import local_path, write_path, use_worlds_venv, init_logging, is_windows, mwgg_venv_site_packages

# Force the SDL2 clipboard provider on Linux. Without this, Kivy probes
# clipboard_xclip / clipboard_xsel / clipboard_dbusklipper / clipboard_gtk3
# first and logs noisy FileNotFoundError tracebacks when xclip/xsel aren't
# installed; it then falls back to sdl2 anyway. Selecting sdl2 explicitly
# skips the probes. macOS keeps its native provider; Windows is unaffected.
if sys.platform.startswith("linux"):
    os.environ.setdefault("KIVY_CLIPBOARD", "sdl2")

# Frozen builds: point OpenSSL at certifi's CA bundle. The bundled Python
# interpreter ships its own OpenSSL, whose compiled-in default cert paths
# point at the *build runner's* filesystem (e.g. /etc/ssl/certs/...), so
# any caller that uses Python's default SSL context — kivy.loader fetching
# IGDB box art, urllib.request, requests, websockets — fails with
# "CERTIFICATE_VERIFY_FAILED: unable to get local issuer certificate" on
# the user's machine. Setting SSL_CERT_FILE / REQUESTS_CA_BUNDLE before
# the ssl module is loaded patches every call site at once.
if use_worlds_venv():
    try:
        import certifi
        _ca_bundle = certifi.where()
        os.environ.setdefault("SSL_CERT_FILE", _ca_bundle)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", _ca_bundle)
    except ImportError:
        pass  # certifi unavailable — leave OpenSSL defaults in place

# Ensure ctypes is imported early (fixes WinDLL issues in frozen builds)
import ctypes

# Linux frozen build: pre-load libmtdev.so.1 by absolute path BEFORE Kivy is
# imported. Kivy's `kivy/lib/mtdev.py` does `ctypes.CDLL("libmtdev.so.1")`
# without a path, which only succeeds if the lib is on the dlopen search
# path. setup.py's post_build_setup() copies it to the bundle root; loading
# it here registers the SONAME with ld.so, so Kivy's later name-only CDLL
# call gets the cached handle instead of OSError.
if sys.platform.startswith("linux") and use_worlds_venv():
    _bundled_mtdev = local_path("libmtdev.so.1")
    if os.path.exists(_bundled_mtdev):
        try:
            ctypes.CDLL(_bundled_mtdev)
        except OSError:
            pass  # let Kivy log its own benign "MTDev is not supported" warning


def _ensure_writable_kivy_data(src: str) -> str:
    """Mirror the bundled Kivy data dir into a writable location and return it.

    On the Linux AppImage (and macOS .app), `local_path(...)` resolves under a
    read-only mount, but Kivy needs to write to its data dir at startup
    (recoloring `defaulttheme-0.png`). We mirror it under `write_path()`
    — the parent of `mwgg_venv` in `~/.local/share/MultiworldGG/` — and
    re-sync whenever the bundled copy is newer than the mirror.
    """
    import shutil
    dst = write_path("kivy", "data")
    marker = "defaulttheme-0.png"
    src_marker = os.path.join(src, marker)
    dst_marker = os.path.join(dst, marker)
    needs_copy = not os.path.exists(dst_marker) or (
        os.path.exists(src_marker)
        and os.path.getmtime(src_marker) > os.path.getmtime(dst_marker)
    )
    if needs_copy:
        # Overlay-copy instead of rmtree+copytree. On Windows a font in `dst`
        # may be locked by another MWGG process or the Windows Font Cache
        # service, and rmtree/overwrite of an open file raises PermissionError
        # [WinError 32]. POSIX read-only mounts (AppImage/.app) tolerate
        # unlinking open files; Windows does not. Skipping a locked file is
        # safe — bundled fonts are byte-identical to the in-use copy; only
        # defaulttheme-0.png actually changes.
        os.makedirs(dst, exist_ok=True)
        for root, _dirs, files in os.walk(src):
            rel = os.path.relpath(root, src)
            dst_root = dst if rel == "." else os.path.join(dst, rel)
            os.makedirs(dst_root, exist_ok=True)
            for name in files:
                try:
                    shutil.copy2(os.path.join(root, name), os.path.join(dst_root, name))
                except PermissionError:
                    pass  # in use by another process; bundled copy is identical
    return dst


# TODO: Move kivy settings out of here and into the kivy module.
if use_worlds_venv():
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_DATA_DIR"] = _ensure_writable_kivy_data(local_path("lib", "kivy", "data"))
    default_libs_dir = os.path.join(sys.exec_prefix, "lib")
    if str(default_libs_dir) not in sys.path:
        sys.path.append(default_libs_dir)
    venv_site_packages_path = mwgg_venv_site_packages()
    if venv_site_packages_path not in sys.path:
        sys.path.append(venv_site_packages_path)
else:
    os.environ["KIVY_DATA_DIR"] = local_path("kivy", "data")
os.environ["KIVY_HOME"] = write_path("data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)


def make_arg_parser() -> ArgumentParser:
    """Build the MultiWorldGG argument parser.

    The optional positional is what OS file associations and the
    archipelago://-style URL protocols hand us: every registered suffix and
    protocol points at `MultiWorldGG.exe "%1"`."""
    parser = ArgumentParser()
    parser.add_argument("launch_file", type=str, default=None, nargs="?", metavar="PATCH_FILE|URL",
                        help="A patch file to route to its game's client (OS file-association double-click), "
                             "a file handled by a tool component (e.g. a .archipelago multidata for the Host), "
                             "or an archipelago:// launch URL")
    parser.add_argument("--game", type=str, default=None, required=False, help="The game module to launch\nGame Name will not work, use the apworld abbreviation")
    parser.add_argument("--server-address", type=str, default=None, required=False, help="The server address to connect to")
    parser.add_argument("--slot-name", type=str, default=None, required=False, help="The slot name to connect to")
    parser.add_argument("--password", type=str, default=None, required=False, help="The password to connect to")
    parser.add_argument("--client-type", type=str, default=None, required=False,
                        choices=["game", "text", "universal_tracker", "manual"],
                        help="Which client to boot directly into: a game module's client (default when --game "
                             "is given), the text client, the universal tracker, or a manual client")
    parser.add_argument("--component", type=str, default=None, required=False,
                        help="Display name of a specific client component registered by --game's world "
                             "module, e.g. a map tracker. Requires --game; unknown names fall back to the "
                             "module's default client")
    parser.add_argument("--update-modules", action="store_true", default=False, required=False, help="Whether to update modules")
    parser.add_argument("--worlds", nargs="+", default=None, required=False, help="List of worlds to update")
    parser.add_argument("--loglevel", default="debug",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="Set the logging level")
    parser.add_argument("--frontend", default="gui", choices=["gui", "tui"],
                        help="Which frontend to launch: 'gui' (Kivy desktop, default) or 'tui' (Textual terminal)")
    # Internal: set by Utils._restart_client_with_args() so a second launch
    # failure surfaces an error dialog instead of looping forever.
    parser.add_argument("--no-restart", action="store_true", default=False,
                        help=argparse.SUPPRESS)
    return parser


def compute_role(args) -> str:
    """Compute this process's role: "client" iff a client launch was requested
    (--game, --client-type, or a positional patch file that routed to a world
    module), else "launcher". Evaluated after launch-file routing so a routed
    patch counts."""
    is_client = bool(getattr(args, "game", None)
                     or getattr(args, "client_type", None)
                     or getattr(args, "patch_module", None))
    return "client" if is_client else "launcher"


def assign_role_env(args) -> str:
    """Assign os.environ["MWGG_ROLE"] from compute_role(args) and return it.

    Deliberately an assignment, never setdefault: a client spawned by the
    launcher inherits the parent's env, so a stale inherited value must never
    leak into this process (or its own children)."""
    role = compute_role(args)
    os.environ["MWGG_ROLE"] = role
    return role


def should_show_splash(frontend: str) -> bool:
    """Windows + Kivy GUI cold starts show the splash; spawned clients don't.

    LauncherComponents.spawn_client sets MWGG_NO_SPLASH=1 in the child env
    (there is no CLI flag), which skips the whole splash block including its
    update check and up-to-60s wait -- a child must not re-run the updater
    under a live launcher."""
    return is_windows and frontend == "gui" and not os.environ.get("MWGG_NO_SPLASH")


def _compose_connect_address(server_address: "str | None", slot_name: "str | None",
                             password: "str | None") -> "str | None":
    """Compose the "slot[:password]@host:port" form that CommonClient's
    InitContext._set_server_address natively parses, honoring its quirks:
    it prefixes "ws://" only when no scheme is present and never
    percent-decodes userinfo, so raw values are joined verbatim; a password
    without a slot name is unusable (urlparse yields an empty username, which
    _set_server_address ignores), so it is dropped; an address that already
    carries userinfo (the archipelago:// URL path pre-composes name@host:port)
    is returned unchanged rather than double-composed."""
    if not server_address:
        return None
    if not slot_name:
        return server_address
    if ":" in slot_name:
        # Userinfo cannot escape a ':' in this form: _set_server_address
        # partitions it at the first colon, so everything after it becomes
        # the password downstream. Warn but compose as-is (do not reject).
        logging.getLogger("MultiWorld").warning(
            f"Slot name {slot_name!r} contains ':'; the client splits user info at the "
            f"first colon, so the text after it will be treated as the password")
    scheme, separator, rest = server_address.partition("://")
    host_part = rest if separator else server_address
    if "@" in host_part:
        return server_address
    userinfo = f"{slot_name}:{password}" if password else slot_name
    composed = f"{userinfo}@{host_part}"
    return f"{scheme}://{composed}" if separator else composed


def _resolve_client_route(args) -> "tuple[str | None, dict]":
    """Resolve a requested module launch (CLI --game / --client-type, or a
    routed patch file) to a (route_module, route_kwargs) pair for
    _route_module_when_ui_ready. route_module "" is the text-client sentinel
    (a valid route: it makes discover_and_launch_module skip the
    specialized-client gate and land at the main_textclient fallback);
    None means no route.

    Must run BEFORE InitContext is constructed: a client-role process that
    resolves no route (--game not available, --client-type
    universal_tracker/manual without a routable game, or a resolution error)
    would otherwise boot a dead client-role GUI — console plus a permanent
    loading overlay, no launcher screen, nothing ever launches. The guard at
    the end re-assigns MWGG_ROLE="launcher" for that whole class, so
    ctx.launch_mode and the frontend role both see the fallback."""
    logger = logging.getLogger("MultiWorld")
    route_module = None
    route_kwargs: dict = {}
    try:
        client_type = getattr(args, "client_type", None) if args else None
        composed_address = _compose_connect_address(
            getattr(args, "server_address", None) if args else None,
            getattr(args, "slot_name", None) if args else None,
            getattr(args, "password", None) if args else None)
        if args and args.game:
            logger.info(f"Attempting to launch game: {args.game}")
            from Utils import get_available_worlds

            if args.game in get_available_worlds():
                route_module = args.game
                route_kwargs = {"server_address": composed_address,
                                "slot_name": args.slot_name,
                                "client_type": client_type or "game",
                                "component": getattr(args, "component", None),
                                "_restarted": getattr(args, "no_restart", False)}
            else:
                logger.error(f"Game {args.game} not found in available worlds; falling back to launcher")
        elif args and getattr(args, "patch_module", None):
            route_module = args.patch_module
            route_kwargs = {"patch_file": args.patch_file}
            if composed_address:
                route_kwargs["server_address"] = composed_address
        elif client_type == "text":
            route_module = ""
            route_kwargs = {"server_address": composed_address,
                            "client_type": "text"}
    except Exception:
        logger.exception("Could not resolve requested module launch; falling back to launcher")
        route_module = None
        route_kwargs = {}

    # Dead-client guard: client role with no resolved route falls back to a
    # live launcher window instead of a client GUI with nothing to launch.
    if route_module is None and os.environ.get("MWGG_ROLE") == "client":
        logger.warning("Client role was requested but no client launch could be resolved; "
                       "falling back to launcher")
        os.environ["MWGG_ROLE"] = "launcher"
    return route_module, route_kwargs


async def _route_module_when_ui_ready(module_name: str, timeout: float = 30.0, **launch_kwargs) -> None:
    """Launch a world module's client once the launcher frontend is up.

    Beta clients cannot run standalone — they take over the launcher UI — so
    this mirrors the GUI's own launch flow (mwgg_gui launcher._launch_module):
    wait for the frontend, then route through Utils.discover_and_launch_module,
    which installs the world on demand and forwards `launch_kwargs` (e.g.
    patch_file from a double-clicked patch, or server_address from a CLI
    --game launch) to the resolved client. The screen-flip hooks are
    feature-detected so the TUI (or an older GUI) simply skips them."""
    from frontend_protocol import resolve_frontend_class

    logger = logging.getLogger("MultiWorld")
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    app = None
    while loop.time() < deadline:
        app = getattr(resolve_frontend_class(), "_active_instance", None)
        if app is not None and (getattr(app, "root", None) is not None      # Kivy: root built
                                or getattr(app, "is_running", False)):      # Textual: running
            break
        await asyncio.sleep(0.2)
    if app is None:
        logger.error(f"Frontend did not come up; cannot launch module {module_name}")
        return

    pre_hook = getattr(app, "client_console_init", None)
    if callable(pre_hook):
        try:
            pre_hook()
        except Exception:
            logger.exception("client_console_init failed; continuing module launch")

    def ready_callback(*_cb_args):
        try:
            console_init = getattr(app, "console_init", None)
            change_screen = getattr(app, "change_screen", None)
            hide_loading = getattr(app, "hide_loading", None)
            if callable(console_init):
                console_init()
            if callable(change_screen):
                change_screen("console")
            if callable(hide_loading):
                hide_loading()
        except Exception:
            logger.exception("Could not switch to the console screen after module launch")

    def error_callback(*_cb_args):
        logger.error(f"Failed to launch a client for module {module_name}")

    from Utils import discover_and_launch_module
    try:
        discover_and_launch_module(module_name=module_name,
                                   ready_callback=ready_callback,
                                   error_callback=error_callback,
                                   **launch_kwargs)
    except Exception:
        logger.exception(f"Module launch failed for {module_name}")


def run_client(args=None, queue=None):
    """Start the MWGG client"""

    async def main(args):
        from CommonClient import InitContext

        logger = logging.getLogger("MultiWorld")

        # Resolve a requested module launch (CLI --game / --client-type, or a
        # routed patch file) BEFORE constructing InitContext, so a fallback to
        # launcher role is already visible in MWGG_ROLE when the context and
        # frontend read it. Beta clients take over the launcher UI rather than
        # running standalone, so the launch itself is deferred until the
        # frontend is up.
        route_module, route_kwargs = _resolve_client_route(args)

        ctx = InitContext()

        # Default initial client behavior
        logger.info("Launching default GUI")
        try:
            ctx.run_gui(splash_queue=queue)
            if route_module is not None:
                # Keep a reference so the routing task isn't garbage-collected.
                # "" (text client) is a valid route, hence the None check.
                routing_task = asyncio.create_task(  # noqa: F841
                    _route_module_when_ui_ready(route_module, **route_kwargs),
                    name="ModuleRouting")
            await ctx.exit_event.wait()
        except Exception as e:
            logger.error(f"Error during GUI execution: {e}", exc_info=True)
            # Don't exit immediately - let the user see the error
            print(f"\nCRITICAL ERROR: {e}")
            print("Press Enter to exit...")
            input()
        finally:
            # Ensure cleanup happens even if there are errors
            try:
                await ctx.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}", exc_info=True)
            finally:
                sys.exit()

    import colorama
    colorama.just_fix_windows_console()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()
    finally:
        colorama.deinit()


def main(argv: "list[str] | None" = None) -> None:
    """Entry point for the client/launcher process.

    `argv` defaults to sys.argv[1:]; Launcher.py delegates here with its own
    argv when the positional it received is not a component name."""
    # Multiprocessing protection for frozen executables
    # This prevents fork bombs when creating subprocesses in cx_Freeze builds
    freeze_support()

    # Parse the command line arguments
    parser = make_arg_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.update_modules:
        # Inno's predownload step. Worlds also install on demand at first
        # launch, so any failure here is non-fatal: show a friendly note and
        # exit 0 rather than letting a traceback escape to the installer.
        try:
            import ModuleUpdate
            ModuleUpdate.install_worlds(worlds=args.worlds if args.worlds else [])
        except Exception:
            # NB: no local `import os` here -- that would make `os` function-local
            # for all of main() and break every later os.* reference in it.
            import traceback, tempfile
            try:
                with open(os.path.join(tempfile.gettempdir(), "mwgg_predownload_error.log"),
                          "w", encoding="utf-8") as f:
                    traceback.print_exc(file=f)
            except OSError:
                pass
            print("Unable to predownload packages, please start the MultiworldGG Client from your Start Menu")
        sys.exit(0)

    # Guard: tracker and manual clients use Kivy-only UI affordances. They cannot run under TUI.
    KIVY_ONLY_GAMES = {"tracker", "manual"}
    if args.frontend == "tui" and args.game and args.game.lower() in KIVY_ONLY_GAMES:
        print(f"Error: --game={args.game} requires --frontend=gui (uses Kivy-only UI features).", file=sys.stderr)
        sys.exit(2)

    # Propagate the frontend selection to the lazy importer in frontend_protocol.resolve_frontend_class()
    os.environ["MWGG_FRONTEND"] = args.frontend

    init_logging("MultiWorld", args.loglevel.lower(), show_logo=True)
    logger = logging.getLogger("MultiWorld")

    if not is_windows:
        # need to check for mwgg_igdb and install it if it's not installed
        try:
            import mwgg_igdb
        except ImportError:
            import ModuleUpdate
            ModuleUpdate.install_worlds(worlds=["mwgg_igdb_sixteen"])

    # Start the splash screen process — Windows + Kivy GUI only.
    # Skipped on Mac/Linux: the splash crashes there, and the long Kivy load
    # the splash exists to mask is much shorter on those platforms anyway.
    # TUI also skips it (no Kivy load to hide), as do clients spawned by the
    # standalone Launcher (MWGG_NO_SPLASH=1 in the child env, see
    # should_show_splash) — only cold starts splash and run the update check.
    splash_queue = None

    if should_show_splash(args.frontend):
        from mwgg_splash import main as splash_main
        # force: on Python 3.13+ the freeze_support() call above already fixed the
        # default context (cpython gh-76327), so a plain set_start_method raises.
        set_start_method("spawn", force=True)
        splash_queue = Queue()
        Process(target=splash_main, name="SplashScreen", args=(splash_queue,)).start()
        
        # Wait for splash process to signal ready (after checking/applying updates)
        logger.info("Checking for updates...")
        try:
            message = splash_queue.get(timeout=60)  # Wait up to 60 seconds
            if isinstance(message, dict):
                msg_type = message.get("type")
                if msg_type == "update_complete":
                    logger.info("Updates applied successfully")
                elif msg_type == "ready":
                    pass
                elif msg_type == "error":
                    logger.error(f"Splash screen error: {message.get('error')}")
        except Exception as e:
            logger.warning(f"Timeout or error waiting for splash screen: {e}")
        
    # Scan custom_worlds/ on launch and register each into the in-memory index
    # (GameIndex.add_game per world) so locally-dropped apworlds are selectable.
    # The apworlds are zip files; only their manifest is read — nothing is imported.
    try:
        from Utils import register_custom_worlds
        register_custom_worlds()
    except Exception as e:
        logger.warning(f"Could not scan custom_worlds on launch: {e}", exc_info=True)

    # Route a double-clicked / positional file before the GUI comes up. Patch
    # containers carry their game name in their root archipelago.json (same
    # pre-load pattern as Patch.py), which resolves to a world module without
    # importing any worlds; the client launch itself is deferred until the
    # launcher UI is running (beta clients take over the launcher UI). Files
    # claimed by a builtin tool component (.archipelago/.mwgg/.zip multidata ->
    # Host) launch that component directly instead.
    args.patch_module = None
    args.patch_file = None
    if args.launch_file:
        if args.launch_file.startswith(("archipelago://", "mwgg://", "multiworldgg://")):
            # Decompose the launch URL into connection prefs + the website-chosen
            # avatar. Persist them so the launcher seeds its hostname/port/slot
            # fields (from last_server_*) and its avatar (from client.avatar), and
            # set the launch args so the UI-ready routing below auto-connects to
            # the room when its game is installed.
            logger.info(f"Launched with URL {args.launch_file}")
            try:
                from CommonClient import parse_connect_url, safe_avatar_source
                from Utils import persistent_store
                parsed = parse_connect_url(args.launch_file)
                if parsed:
                    host, port, name = parsed["hostname"], parsed["port"], parsed["name"]
                    if host:
                        persistent_store("client", "last_server_hostname", host)
                        if port:
                            persistent_store("client", "last_server_port", port)
                        host_port = f"{host}:{port}" if port else host
                        args.server_address = f"{name}@{host_port}" if name else host_port
                    if name:
                        persistent_store("client", "last_username", name)
                        args.slot_name = name
                    safe_avatar = safe_avatar_source(parsed["avatar"])
                    if safe_avatar:
                        persistent_store("client", "avatar", safe_avatar)
                    if parsed["game"]:
                        from mwgg_igdb import GameIndex
                        module_name = GameIndex.get_module_for_game(parsed["game"])
                        if module_name:
                            args.game = module_name
            except Exception:
                logger.warning("Failed to apply launch URL %r", args.launch_file, exc_info=True)
        elif os.path.isfile(args.launch_file):
            from Utils import read_patch_game_name
            game_name = read_patch_game_name(args.launch_file)
            if game_name:
                from mwgg_igdb import GameIndex
                module_name = GameIndex.get_module_for_game(game_name)
                if module_name:
                    args.patch_module = module_name
                    args.patch_file = os.path.abspath(args.launch_file)
                    logger.info(f"Routing patch file {args.launch_file} to {game_name} ({module_name})")
                else:
                    logger.warning(f"No installed or indexed world handles game {game_name!r} "
                                   f"from {args.launch_file}; opening launcher.")
            else:
                from LauncherComponents import identify, get_exe
                from BaseUtils import launch_exe
                component = identify(args.launch_file)
                if component is not None:
                    logger.info(f"Routing {args.launch_file} to component {component.display_name}")
                    if component.func:
                        component.func(args.launch_file)
                        sys.exit(0)
                    exe = get_exe(component)
                    if exe:
                        launch_exe([*exe, args.launch_file], component.cli)
                        sys.exit(0)
                    logger.warning(f"Component {component.display_name} is not executable; opening launcher.")
                else:
                    logger.warning(f"Could not identify a handler for {args.launch_file}; opening launcher.")
        else:
            logger.warning(f"File not found: {args.launch_file}; opening launcher.")

    # Role is computed after launch-file routing (a routed patch counts as a
    # client launch) and always assigned, never setdefault: see assign_role_env.
    # The unroutable-file/URL warnings above leave game/patch_module unset, so
    # those fallbacks compute back to "launcher" here by construction.
    assign_role_env(args)

    # Run the main client in the current process
    run_client(args, queue=splash_queue)


if __name__ == "__main__":
    main()