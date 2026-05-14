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

from BaseUtils import local_path, write_path, is_frozen, init_logging, is_windows
from mwgg_splash import main as splash_main

# Ensure ctypes is imported early (fixes WinDLL issues in frozen builds)
import ctypes

if is_frozen():
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_DATA_DIR"] = local_path("lib", "kivy", "data")
    default_libs_dir = os.path.join(sys.exec_prefix, "lib")
    if str(default_libs_dir) not in sys.path:
        sys.path.append(default_libs_dir)
    venv_site_packages_path = write_path("mwgg_venv", "Lib", "site-packages")
    if venv_site_packages_path not in sys.path:
        sys.path.append(venv_site_packages_path)
else:
    os.environ["KIVY_DATA_DIR"] = local_path("kivy", "data")
os.environ["KIVY_HOME"] = write_path("data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)


def run_client(*args, queue=None):
    """Start the MWGG client"""

    async def main(args: list[str]):
        from CommonClient import InitContext

        logger = logging.getLogger("MultiWorld")
        ctx = InitContext()
        
        # Check if a specific module was requested
        try:
            if args and args.game and args.server_address:
                logger.info(f"Attempting to launch game: {args.game}")
                from Utils import get_available_worlds, discover_and_launch_module

                if args.game not in get_available_worlds():
                    raise Exception(f"Game {args.game} not found in available worlds")

                # Try to launch the module via entrypoints
                try:
                    discover_and_launch_module(module_name=args.game,
                                            server_address=args.server_address,
                                            _restarted=getattr(args, "no_restart", False))
                    return  # Module takeover successful, exit initial client
                except Exception as e:
                    logger.error(f"Module launch failed: {e}")
                    # Fall back to initial client
                    logger.info("Falling back to launcher")
        except Exception as e:
            pass
        
        # Default initial client behavior
        logger.info("Launching default GUI")
        try:
            ctx.run_gui(splash_queue=queue)
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

if __name__ == "__main__":
    # Multiprocessing protection for frozen executables
    # This prevents fork bombs when creating subprocesses in cx_Freeze builds
    freeze_support()

    # Parse the command line arguments
    parser = ArgumentParser()
    parser.add_argument("--game", type=str, default=None, required=False, help="The game module to launch\nGame Name will not work, use the apworld abbreviation")
    parser.add_argument("--server-address", type=str, default=None, required=False, help="The server address to connect to")
    parser.add_argument("--slot-name", type=str, default=None, required=False, help="The slot name to connect to")
    parser.add_argument("--password", type=str, default=None, required=False, help="The password to connect to")
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

    if sys.argv[1:]:
        args = parser.parse_args(sys.argv[1:])

        if args.update_modules:
            import ModuleUpdate
            ModuleUpdate.install_worlds(worlds=args.worlds if args.worlds else [])
            sys.exit(0)
    else:
        args = parser.parse_args([])

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

    # Start the splash screen process — only for the Kivy GUI frontend (TUI doesn't have
    # the ~30s Kivy load that the splash exists to mask).
    splash_queue = None

    if is_windows and args.frontend == "gui":
        set_start_method("spawn")
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
        
    # Run the main client in the current process
    run_client(args, queue=splash_queue)