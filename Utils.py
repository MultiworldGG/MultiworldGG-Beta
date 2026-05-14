from __future__ import annotations

from BaseUtils import *

import asyncio
import concurrent.futures
import json
import typing
import builtins
import os
import itertools
import subprocess
import sys
import pickle
import functools
import io
import collections
import importlib
import logging
import warnings
import zipfile

import re

from argparse import Namespace
from datetime import datetime, timezone

from settings import Settings, get_settings
from time import sleep
from typing import BinaryIO, Coroutine, Mapping, Optional, Set, Dict, Any, Union, TypeGuard
from yaml import load, load_all, dump
from pathspec import PathSpec, GitIgnoreSpec
from typing_extensions import deprecated
from pathlib import Path

logger = logging.getLogger("MultiWorld")

init_logging("Update")
update_logger = logging.getLogger("Update")

import ModuleUpdate

try:
    from yaml import CLoader as UnsafeLoader, CSafeLoader as SafeLoader, CDumper as Dumper
except ImportError:
    from yaml import Loader as UnsafeLoader, SafeLoader, Dumper

from FileUtils import FileUtils
open_directory = FileUtils.open_directory
open_filename = FileUtils.open_file_input_dialog
open_file_input_dialog = FileUtils.open_file_input_dialog
save_filename = FileUtils.save_file_input_dialog

if typing.TYPE_CHECKING:
    import tkinter
    import pathlib
    from BaseClasses import Region
    import multiprocessing

def normalize_tag(tag: str) -> str:
    return tag[1:] if tag and tag[0].lower() == "v" else tag


is_linux = sys.platform.startswith("linux")
is_macos = sys.platform == "darwin"
is_windows = sys.platform in ("win32", "cygwin", "msys")

_worlds_to_load: typing.List[str | "APWorldContainer"] = []

def set_game_names(game_names: typing.List[str]) -> typing.List[(str, bool)]:
    """Set the game names to the list of game names"""
    from mwgg_igdb import GameIndex
    from APContainer import APWorldContainer
    _worlds_to_install = {game: "" for game in game_names}
    _unknown_worlds = []
    custom_worlds_dir = Path(local_path("custom_worlds"))
    _unlisted_worlds = [world for world in ModuleUpdate.find_world_modules() if world not in GameIndex.game_names.values()]
    # We only have the module name here, not the game name, and that is buried deep in the metadata

    def check_world_installed(game: str):
        try:
            _worlds_to_install[game] = GameIndex.game_names[game]
            importlib.metadata.distribution(f"worlds.{_worlds_to_install[game]}")
            _worlds_to_load.append(f"worlds.{_worlds_to_install[game]}")
            _worlds_to_install.pop(game)
        except KeyError:
            # Game not found in index
            update_logger.warning(f"Game {game} not found in game index, looking for unlisted world.")
            _unknown_worlds.append(game)
            return
        except importlib.metadata.PackageNotFoundError:
            # Package not installed
            return

    for game in game_names:
        check_world_installed(game)

    if _unknown_worlds:
        _unlisted_worlds_names: dict[str, str] = {}
        # If we can't find the world, start in the unlisted worlds
        for module_name in _unlisted_worlds:
            try:
                dist = importlib.metadata.distribution(f"worlds.{module_name}")
                if dist:
                    _unlisted_worlds_names[dist.metadata.json['summary'].strip("MultiWorld: ")] = module_name
            except importlib.metadata.PackageNotFoundError:
                continue
        for world in _unknown_worlds:
            if world in _unlisted_worlds_names.keys():
                module = _unlisted_worlds_names[world]
                _worlds_to_load.append(f"worlds.{module}")
                _worlds_to_install.pop(world)
                _unknown_worlds.remove(world) # Not unknown

    if _worlds_to_install:
        modules_to_install = [module for module in _worlds_to_install.values() if module]
        custom_worlds = ModuleUpdate.install_worlds(modules_to_install)
        # install_worlds returns slugs that fell back to a custom apworld; pick up the
        # ones that actually pip-installed by checking importlib.metadata directly so
        # the loader sees them.
        for slug in modules_to_install:
            target = f"worlds.{slug}"
            if target in _worlds_to_load:
                continue
            if target in custom_worlds:
                continue
            try:
                importlib.metadata.distribution(target)
                _worlds_to_load.append(target)
            except importlib.metadata.PackageNotFoundError:
                pass
    else:
        custom_worlds = []

    # Snapshot installed-wheel versions for slugs already on _worlds_to_load.
    # Used to honor the precedence rule: higher world_version wins, tie -> installed wheel.
    _installed_versions: dict[str, str] = {}
    for entry in _worlds_to_load:
        if isinstance(entry, str) and entry.startswith("worlds."):
            slug = entry[len("worlds."):]
            try:
                _installed_versions[slug] = importlib.metadata.distribution(f"worlds.{slug}").version
            except importlib.metadata.PackageNotFoundError:
                pass

    if custom_worlds_dir.exists():
        for file in custom_worlds_dir.iterdir():
            if file.suffix != ".apworld":
                continue
            with zipfile.ZipFile(file, 'r') as zipf:
                apworld = APWorldContainer(file)
                manifest = apworld.read_contents(zipf)

            if manifest.get("game") in _unknown_worlds:
                _worlds_to_load.append(apworld)
                # Seed the in-memory GameIndex so subsequent get_module_for_game()
                # lookups (notably in Generate.roll_settings) can resolve this game
                # to its custom apworld module without waiting for
                # get_available_worlds() to scan custom_worlds_dir again.
                if not GameIndex.get_game_name_for_module(file.stem):
                    index_entry = dict(manifest)
                    index_entry["game_name"] = manifest["game"]
                    GameIndex.add_game(file.stem, index_entry)
                continue
            if f"worlds.{file.stem}" in custom_worlds:
                _worlds_to_load.append(apworld)
                continue
            if file.stem in _installed_versions:
                apworld_version = tuplize_version(manifest.get("world_version", "0.0.0"))
                installed_version = tuplize_version(_installed_versions[file.stem])
                if apworld_version > installed_version:
                    # apworld wins — replace the installed-wheel entry with the apworld
                    target = f"worlds.{file.stem}"
                    try:
                        _worlds_to_load.remove(target)
                    except ValueError:
                        pass
                    _worlds_to_load.append(apworld)
                # tie or apworld older -> installed wheel wins, leave _worlds_to_load alone

    # Compute the set of game names that _worlds_to_load can actually serve. Mirrors
    # what the loader will see: a `worlds.<slug>` entry serves whatever game the
    # installed wheel's summary advertises, and an APWorldContainer serves its
    # manifest .game.
    index_slug_to_name = {slug: name for name, slug in GameIndex.game_names.items()}
    served_games: set[str] = set()
    for entry in _worlds_to_load:
        if isinstance(entry, APWorldContainer):
            if entry.game:
                served_games.add(entry.game)
        elif isinstance(entry, str) and entry.startswith("worlds."):
            slug = entry[len("worlds."):]
            name = index_slug_to_name.get(slug)
            if name:
                served_games.add(name)
                continue
            try:
                dist = importlib.metadata.distribution(f"worlds.{slug}")
                summary = dist.metadata.json.get('summary', '') if dist else ''
                if summary:
                    served_games.add(summary.strip("MultiWorld: "))
            except importlib.metadata.PackageNotFoundError:
                pass
    missing = [g for g in game_names if g not in served_games]
    if missing:
        raise RuntimeError(
            "Cannot generate: the following games could not be installed and have no apworld fallback: "
            + ", ".join(repr(g) for g in missing)
        )

def game_names() -> typing.List[str]:
    """Get a list of only the game names that we're using"""
    return _worlds_to_load

def get_available_worlds() -> typing.List[str]:
    """Get a list of all of the available worlds"""
    from mwgg_igdb import GameIndex
    from ModuleUpdate import find_world_modules
    from BaseUtils import get_apworld_manifest
    
    available_worlds = find_world_modules()
    # Also add worlds from the custom_worlds directory
    custom_worlds_dir = Path(local_path("custom_worlds"))
    for world_file in custom_worlds_dir.iterdir():
        module_name = discover_custom_world_module(world_file)
        if module_name and module_name not in available_worlds:
            available_worlds.add(module_name)
    game_modules = set(GameIndex.get_all_games().keys())

    # Also check for currently installed world modules not in GameIndex
    try:
        for world_name in available_worlds:
            if world_name not in game_modules:
                manifest = get_apworld_manifest(world_name)
                manifest["game_name"] = manifest.pop("game", world_name)
                manifest["cover_url"] = manifest.pop("cover_url", "")
                GameIndex.add_game(world_name, manifest)

    except Exception as e:
        update_logger.warning(f"Error checking installed world modules: {e}")

    return list(sorted(available_worlds))

def discover_custom_world_module(custom_world: Path) -> Optional[str]:
    """Add worlds from the custom_worlds directory to the game index."""
    from mwgg_igdb import GameIndex
    from APContainer import APWorldContainer
    
    if custom_world.suffix in [".whl", ".egg", ".tar", ".gz", ".zip"]:
        with zipfile.ZipFile(custom_world, 'r') as zipf:
            for name in zipf.infolist():
                if name.filename.endswith("archipelago.json"):
                    apmanifest_path = name
                    break
            module_name = apmanifest_path.filename.split("/")[1].replace("-", "_")
            metadata = json.loads(zipf.read(apmanifest_path))
            metadata["game_name"] = metadata.pop("game", module_name)
            metadata["cover_url"] = metadata.pop("cover_url", "")
            if GameIndex.get_game_name_for_module(module_name):
                # Already known to the in-memory index (e.g. registered by a previous
                # call this run). Idempotent no-op; return the module name so callers
                # still see it as a discovered world.
                return module_name
            GameIndex.add_game(module_name, metadata)
    elif custom_world.suffix == ".apworld":
        with zipfile.ZipFile(custom_world, 'r') as custom_apworld:
            module_name = custom_world.stem
            manifest = APWorldContainer(custom_world).read_contents(custom_apworld)
            manifest["game_name"] = manifest.pop("game", module_name)
            manifest["cover_url"] = manifest.pop("cover_url", "")
            if GameIndex.get_game_name_for_module(module_name):
                # Already known to the in-memory index (e.g. registered by a previous
                # call this run). Idempotent no-op; return the module name so callers
                # still see it as a discovered world.
                return module_name
            GameIndex.add_game(module_name, manifest)
    return module_name if module_name else None


def discover_and_launch_module(module_name: str, **kwargs) -> Optional[callable]:
    """Discover and launch module via entrypoints.

    Frontend-neutral: worker-thread callbacks marshal back to the asyncio loop
    via loop.call_soon_threadsafe, which works for both the Kivy GUI and the
    Textual TUI (both run inside the same asyncio loop driven by MultiWorld.py).
    """
    import threading
    import asyncio

    # No game selected -> fall straight through to Text Client (CommonClient).
    # _perform_module_launch("") skips the specialized-client gate and lands at
    # the main_textclient fallback below.
    if not module_name:
        return _perform_module_launch("", **kwargs)

    # First, try to import the module to see if it exists
    if not module_name.startswith("worlds."):
        module_name = f"worlds.{module_name}"

    loop = asyncio.get_event_loop()

    def _install_module_threaded():
        """Install module in a separate thread"""
        try:
            restart = ModuleUpdate.install_worlds([module_name])
            if restart:
                # Restart needed - schedule callback on main thread
                raise ModuleUpdate.RestartException
            else:
                # No restart needed - proceed with launch
                loop.call_soon_threadsafe(_launch_module_after_install)
        except ModuleUpdate.RestartException as re:
            # Restart needed - schedule callback on main thread
            loop.call_soon_threadsafe(_handle_install_error, "Restart required for world updates.")

        except Exception as e:
            update_logger.error(f"Failed to update module {module_name}: {str(e)}")
            # Schedule error handling on main thread
            loop.call_soon_threadsafe(_handle_install_error, str(e))

    def _launch_module_after_install():
        """Launch the module after successful installation"""
        try:
            _perform_module_launch(module_name, **kwargs)
        except Exception as e:
            logging.error(f"Failed to launch module {module_name} after install: {e}")
            _handle_install_error(e)

    def _handle_install_error(error):
        """Handle installation errors on the main thread"""
        # Get error callback from kwargs if provided
        error_callback = kwargs.get('error_callback')
        if error_callback:
            error_callback()
        update_logger.error(f"Module installation failed: {error}")
    
    if not is_windows:
        _perform_module_launch("", **kwargs)
        return

    try:
        importlib.import_module(module_name)
        # Module exists, launch directly
        _perform_module_launch(module_name, **kwargs)
    except ModuleNotFoundError:
        # Module doesn't exist, install it in a separate thread
        update_logger.info(f"Module {module_name} not found, installing in background...")
        install_thread = threading.Thread(target=_install_module_threaded, daemon=True)
        install_thread.start()
        return  # Return early, launch will be scheduled after installation
    except Exception as e:
        update_logger.error(f"Failed to import module {module_name}: {e}")
        raise e

def _perform_module_launch(module_id: str, **kwargs):
    """Perform the actual module launch logic"""
    try:
        # Per-world launch() bodies are CLI-style and call asyncio.run(main()).
        # Without nest_asyncio that raises "cannot be called from a running
        # event loop" because the launcher's asyncio loop is already running
        # on this thread. nest_asyncio.apply() patches asyncio to allow the
        # nested run() call to re-enter the running loop; the launcher's loop
        # continues to service other tasks while it's re-entered, so the UI
        # stays responsive during the game session. apply() is idempotent.
        import nest_asyncio
        nest_asyncio.apply()

        # Stash launcher-provided ready/error callbacks centrally. CommonContext
        # picks them up in __init__ so world clients don't need to forward them
        # through their launch() signatures.
        import CommonClient
        ready_callback = kwargs.pop("ready_callback", None)
        error_callback = kwargs.pop("error_callback", None)
        CommonClient._set_pending_launch_callbacks(ready_callback, error_callback)

        if module_id:
            # Single attempt: by the time we get here, _install_module_threaded
            # has already returned successfully and the wheel is on disk. A
            # synchronous retry loop here used to block the asyncio loop and
            # freeze the UI. If the import fails now, it almost always means a
            # transitive dep is missing (the install used --no-deps), so we
            # hand off to _restart_with_deps below.
            try:
                importlib.invalidate_caches()
                importlib.import_module(module_id)
            except (ModuleNotFoundError, ImportError) as e:
                if kwargs.get("_restarted"):
                    update_logger.error(f"Module {module_id} still failed after dep reinstall: {e}")
                    raise
                update_logger.warning(
                    f"Launch import failed ({e}); reinstalling {module_id} with deps and restarting."
                )
                ModuleUpdate.install_worlds([module_id], with_deps=True)
                _restart_client_with_args()
                return None

            entry_points = importlib.metadata.entry_points(group="mwgg.client")
            entry_point_name = "{}.Client".format(module_id)
            
            # Check if the entry point exists by looking through the entry points
            module_entry_point = None
            for entry_point in entry_points:
                if entry_point.name == entry_point_name:
                    module_entry_point = entry_point
                    break
            
            if module_entry_point:
                # Load and execute the client entrypoint
                launch_function = module_entry_point.load()
                # Per-world launch() bodies are CLI-style: they parse sys.argv
                # and then call asyncio.run(main()). Two constraints stack:
                #   1. asyncio.run() inside a running loop normally raises;
                #      nest_asyncio.apply() (called at the top of this function)
                #      patches asyncio to allow re-entry.
                #   2. We're invoked from a Kivy event handler. If we call
                #      launch_function() synchronously here, the handler never
                #      returns while the game session is alive, and Kivy --
                #      being single-threaded -- can't dispatch any other UI
                #      events (the GUI freezes even though asyncio keeps
                #      pumping). To unblock Kivy, defer launch_function() to
                #      the next loop iteration via call_soon. By the time it
                #      runs, the Kivy event handler has returned and Kivy is
                #      back in its idle dispatch state.
                loop = asyncio.get_event_loop()
                server_address = kwargs.get("server_address")

                already_restarted = kwargs.get("_restarted", False)

                def _deferred_launch():
                    saved_argv = sys.argv[:]
                    try:
                        if isinstance(server_address, str) and server_address:
                            sys.argv = [sys.argv[0], f"--connect={server_address}"]
                        launch_function()
                    except (ModuleNotFoundError, ImportError) as dep_error:
                        if already_restarted:
                            logging.error(
                                f"Deferred world launch for {module_id} still missing deps after restart: {dep_error}",
                                exc_info=True,
                            )
                            import CommonClient as _CC
                            _, pending_error_cb = _CC._consume_pending_launch_callbacks()
                            if pending_error_cb is not None:
                                try:
                                    pending_error_cb()
                                except Exception as cb_err:
                                    logging.error(f"Error in error callback: {cb_err}")
                        else:
                            update_logger.warning(
                                f"Deferred launch import failed ({dep_error}); reinstalling {module_id} with deps and restarting."
                            )
                            try:
                                ModuleUpdate.install_worlds([module_id], with_deps=True)
                            except Exception as install_error:
                                logging.error(f"Failed to reinstall {module_id} with deps: {install_error}", exc_info=True)
                                return
                            _restart_client_with_args()
                    except Exception as launch_error:
                        logging.error(
                            f"Deferred world launch failed for {module_id}: {launch_error}",
                            exc_info=True,
                        )
                        import CommonClient as _CC
                        _, pending_error_cb = _CC._consume_pending_launch_callbacks()
                        if pending_error_cb is not None:
                            try:
                                pending_error_cb()
                            except Exception as cb_err:
                                logging.error(f"Error in error callback: {cb_err}")
                    finally:
                        sys.argv[:] = saved_argv

                loop.call_soon(_deferred_launch)
                logging.info(f"Scheduled deferred launch for {module_id} on next asyncio iteration")
                return None
                            
            # 2. Check SNI registry
            from mwgg_igdb import GameIndex
            game_name = GameIndex.get_game_name_for_module(module_name=module_id.strip("worlds."))
            try:
                from worlds._sni.client import AutoSNIClientRegister
                if AutoSNIClientRegister.is_sni_world(module_name=game_name):
                    logging.info(f"Detected SNI client for {game_name}")
                    from worlds._sni.context import launch
                    return launch(**kwargs)
            except ImportError:
                logging.debug("SNI client not available")
                
            # 3. Check BizHawk registry
            try:
                from worlds._bizhawk.client import AutoBizHawkClientRegister
                if AutoBizHawkClientRegister.is_bizhawk_world(module_name=game_name):
                    logging.info(f"Detected BizHawk client for {game_name}")
                    from worlds._bizhawk.context import launch
                    return launch(**kwargs)
            except ImportError:
                logging.debug("BizHawk client not available")

        # 4. Fallback to text client
        logging.info(f"No specialized client, using text client")
        from CommonClient import main_textclient
        result = main_textclient(**kwargs)

        # Check if the launch function returned a task (GUI mode)
        if hasattr(result, '_coro'):
            logging.info(f"Launch function returned a task for text client, running in GUI mode")
            # The task is already scheduled in the event loop
            return result
        else:
            logging.info(f"Launch function completed synchronously for text client")
            return result

    except Exception as e:
        logging.error(f"Failed to launch module {module_id}: {e}")
        # Fallback for the case where the world's launch() raised before any
        # CommonContext was constructed. If a context was built, it consumed
        # the pending dict and the context's own one-shot fired the callback
        # from _takeover_existing_ui's except arm — we don't double-fire here.
        _, pending_error_callback = CommonClient._consume_pending_launch_callbacks()
        if pending_error_callback is not None:
            try:
                pending_error_callback()
            except Exception as callback_error:
                logging.error(f"Error in error callback: {callback_error}")
        raise

def exit_restart_for_update():
    """
    Spawn a new process with the same arguments, then exit.
    The new process will have its splashscreen apply the updates.
    """
    # Spawn new process with same executable and arguments
    subprocess.Popen([sys.executable] + sys.argv,
                     cwd=os.getcwd(),
                     creationflags=subprocess.CREATE_NEW_CONSOLE if is_windows() else 0)

    logger.info("Exiting current process...")

    # Flush all logging handlers to ensure messages are displayed
    for handler in logging.root.handlers:
        handler.flush()

    # Use sys.exit with code 10 to signal "bad environment" - needs restart
    # This allows the calling process to handle the restart properly
    sys.exit(10)


def _restart_client_with_args():
    """Re-exec the client with the same argv plus --no-restart so a second
    launch failure surfaces an error instead of looping. Used when a world's
    transitive deps were missing and we just reinstalled them."""
    new_argv = list(sys.argv)
    if "--no-restart" not in new_argv:
        new_argv.append("--no-restart")
    subprocess.Popen([sys.executable, *new_argv],
                     cwd=os.getcwd(),
                     creationflags=subprocess.CREATE_NEW_CONSOLE if is_windows() else 0)
    logger.info("Restarting client to pick up freshly installed dependencies...")
    for handler in logging.root.handlers:
        handler.flush()
    sys.exit(0)

def int16_as_bytes(value: int) -> typing.List[int]:
    value = value & 0xFFFF
    return [value & 0xFF, (value >> 8) & 0xFF]


def int32_as_bytes(value: int) -> typing.List[int]:
    value = value & 0xFFFFFFFF
    return [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]


def pc_to_snes(value: int) -> int:
    return ((value << 1) & 0x7F0000) | (value & 0x7FFF) | 0x8000


def snes_to_pc(value: int) -> int:
    return ((value & 0x7F0000) >> 1) | (value & 0x7FFF)


RetType = typing.TypeVar("RetType")
S = typing.TypeVar("S")
T = typing.TypeVar("T")


def cache_argsless(function: typing.Callable[[], RetType]) -> typing.Callable[[], RetType]:
    assert not function.__code__.co_argcount, "Can only cache 0 argument functions with this cache."

    sentinel = object()
    result: typing.Union[object, RetType] = sentinel

    def _wrap() -> RetType:
        nonlocal result
        if result is sentinel:
            result = function()
        return typing.cast(RetType, result)

    return _wrap


def cache_self1(function: typing.Callable[[S, T], RetType]) -> typing.Callable[[S, T], RetType]:
    """Specialized cache for self + 1 arg. Does not keep global ref to self and skips building a dict key tuple."""

    assert function.__code__.co_argcount == 2, "Can only cache 2 argument functions with this cache."

    cache_name = f"__cache_{function.__name__}__"

    @functools.wraps(function)
    def wrap(self: S, arg: T) -> RetType:
        cache: Optional[dict[T, RetType]] = getattr(self, cache_name, None)
        if cache is None:
            res = function(self, arg)
            setattr(self, cache_name, {arg: res})
            return res
        try:
            return cache[arg]
        except KeyError:
            res = function(self, arg)
            cache[arg] = res
            return res

    wrap.__defaults__ = function.__defaults__

    return wrap


def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))


def is_webhost_mode() -> bool:
    """Detect whether this import is happening in WebHost/dedicated web runtime."""
    if "WebHost" in sys.modules:
        return True
    argv0 = os.path.basename(sys.argv[0]).lower() if sys.argv else ""
    return "webhost.py" in argv0 or "gunicorn" in argv0


def local_path(*path: str) -> str:
    """
    Returns path to a file in the local MultiworldGG installation or source.
    This might be read-only and user_path should be used instead for ROMs, configuration, etc.
    """
    if hasattr(local_path, 'cached_path'):
        pass
    elif is_frozen():
        if hasattr(sys, "_MEIPASS"):
            # we are running in a PyInstaller bundle
            local_path.cached_path = sys._MEIPASS  # pylint: disable=protected-access,no-member
        else:
            # cx_Freeze
            local_path.cached_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        import __main__
        if globals().get("__file__") and os.path.isfile(__file__):
            # we are running in a normal Python environment
            local_path.cached_path = os.path.dirname(os.path.abspath(__file__))
        elif hasattr(__main__, "__file__") and os.path.isfile(__main__.__file__):
            # we are running in a normal Python environment, but AP was imported weirdly
            local_path.cached_path = os.path.dirname(os.path.abspath(__main__.__file__))
        else:
            # pray
            local_path.cached_path = os.path.abspath(".")

    return os.path.join(local_path.cached_path, *path)


def home_path(*path: str) -> str:
    """Returns path to a file in the user home's MultiworldGG directory."""
    if hasattr(home_path, 'cached_path'):
        pass
    elif sys.platform.startswith('linux'):
        xdg_data_home = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        home_path.cached_path = f'{xdg_data_home}/{instance_name}'
        if not os.path.isdir(home_path.cached_path):
            legacy_home_path = os.path.expanduser(f'~/{instance_name}')
            if os.path.isdir(legacy_home_path):
                os.renames(legacy_home_path, home_path.cached_path)
                os.symlink(home_path.cached_path, legacy_home_path)
            else:
                os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    elif sys.platform == 'darwin':
        import platformdirs
        home_path.cached_path = platformdirs.user_data_dir("Archipelago", False)
        os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    else:
        # not implemented
        home_path.cached_path = local_path()  # this will generate the same exceptions we got previously

    return os.path.join(home_path.cached_path, *path)


def user_path(*path: str) -> str:
    """Returns either local_path or home_path based on write permissions."""
    if hasattr(user_path, "cached_path"):
        pass
    elif os.access(local_path(), os.W_OK) and not (is_macos and is_frozen()):
        user_path.cached_path = local_path()
    else:
        user_path.cached_path = home_path()
        # populate home from local
        if user_path.cached_path != local_path():
            import filecmp
            if not os.path.exists(user_path("manifest.json")) or \
                    not os.path.exists(local_path("manifest.json")) or \
                    not filecmp.cmp(local_path("manifest.json"), user_path("manifest.json"), shallow=True):
                import shutil
                for dn in ("Players", "data/sprites", "data/lua"):
                    shutil.copytree(local_path(dn), user_path(dn), dirs_exist_ok=True)
                if not os.path.exists(local_path("manifest.json")):
                    warnings.warn(f"Upgrading {user_path()} from something that is not a proper install")
                else:
                    shutil.copy2(local_path("manifest.json"), user_path("manifest.json"))
            os.makedirs(user_path("worlds"), exist_ok=True)

    return os.path.join(user_path.cached_path, *path)


def cache_path(*path: str) -> str:
    """Returns path to a file in the user's MultiworldGG cache directory."""
    if hasattr(cache_path, "cached_path"):
        pass
    else:
        import platformdirs
        cache_path.cached_path = platformdirs.user_cache_dir(instance_name, False)
        # Ensure the cache directory exists
        os.makedirs(cache_path.cached_path, exist_ok=True)

    return os.path.join(cache_path.cached_path, *path)


def output_path(*path: str) -> str:
    if hasattr(output_path, 'cached_path'):
        return os.path.join(output_path.cached_path, *path)
    output_path.cached_path = user_path(get_settings()["general_options"]["output_path"])
    path = os.path.join(output_path.cached_path, *path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def open_file(filename: typing.Union[str, "pathlib.Path"]) -> None:
    if is_windows:
        os.startfile(filename)  # type: ignore
    else:
        from shutil import which
        open_command = which("open") if is_macos else (which("xdg-open") or which("gnome-open") or which("kde-open"))
        assert open_command, "Didn't find program for open_file! Please report this together with system details."

        env = env_cleared_lib_path()
        subprocess.call([open_command, filename], env=env)


# from https://gist.github.com/pypt/94d747fe5180851196eb#gistcomment-4015118 with some changes
class UniqueKeyLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                logging.error(f"YAML duplicates sanity check failed{key_node.start_mark}")
                raise KeyError(f"Duplicate key {key} found in YAML. Already found keys: {mapping}.")
            if (str(key).startswith("+") and (str(key)[1:] in mapping)) or (f"+{key}" in mapping):
                logging.error(f"YAML merge duplicates sanity check failed{key_node.start_mark}")
                raise KeyError(f"Equivalent key {key} found in YAML. Already found keys: {mapping}.")
            mapping.add(key)
        return super().construct_mapping(node, deep)


parse_yaml = functools.partial(load, Loader=UniqueKeyLoader)
parse_yamls = functools.partial(load_all, Loader=UniqueKeyLoader)
unsafe_parse_yaml = functools.partial(load, Loader=UnsafeLoader)

del load, load_all  # should not be used. don't leak their names


def get_cert_none_ssl_context():
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


@cache_argsless
def get_public_ipv4() -> str:
    import socket
    import urllib.request
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        # if hostname or resolvconf is not set up properly, this may fail
        warnings.warn("Could not resolve own hostname, falling back to 127.0.0.1")
        ip = "127.0.0.1"

    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen("https://checkip.amazonaws.com/", context=ctx, timeout=10).read().decode("utf8").strip()
    except Exception as e:
        # noinspection PyBroadException
        try:
            ip = urllib.request.urlopen("https://v4.ident.me", context=ctx, timeout=10).read().decode("utf8").strip()
        except Exception:
            logging.exception(e)
            pass  # we could be offline, in a local game, so no point in erroring out
    return ip


@cache_argsless
def get_public_ipv6() -> str:
    import socket
    import urllib.request
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        # if hostname or resolvconf is not set up properly, this may fail
        warnings.warn("Could not resolve own hostname, falling back to ::1")
        ip = "::1"

    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen("https://v6.ident.me", context=ctx, timeout=10).read().decode("utf8").strip()
    except Exception as e:
        logging.exception(e)
        pass  # we could be offline, in a local game, or ipv6 may not be available
    return ip


@deprecated("Utils.get_options() is deprecated. Use the settings API instead.")
def get_options() -> Settings:
    deprecate("Utils.get_options() is deprecated. Use the settings API instead.")
    return get_settings()


def persistent_store(category: str, key: str, value: typing.Any):
    path = user_path("_persistent_storage.yaml")
    storage = persistent_load()
    category_dict = storage.setdefault(category, {})
    
    # Remove key if value is None or empty string to prevent malformed YAML
    if value is None or value == "":
        category_dict.pop(key, None)
    else:
        category_dict[key] = value
        
    with open(path, "wt") as f:
        f.write(dump(storage, Dumper=Dumper))


def persistent_load() -> dict[str, dict[str, Any]]:
    storage: Union[dict[str, dict[str, Any]], None] = getattr(persistent_load, "storage", None)
    if storage:
        return storage
    path = user_path("_persistent_storage.yaml")
    storage = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                storage = unsafe_parse_yaml(f.read())
            if "datapackage" in storage:
                del storage["datapackage"]
                logging.debug("Removed old datapackage from persistent storage")
        except Exception as e:
            logger.warning(f"Could not read persistent storage (file may be corrupted): {e}")
            # Attempt to backup the corrupted file
            try:
                import shutil
                backup_path = path + ".corrupted"
                shutil.copy2(path, backup_path)
                logger.info(f"Corrupted storage backed up to: {backup_path}")
            except Exception as backup_error:
                logger.debug(f"Could not backup corrupted storage: {backup_error}")
    if storage is None:
        storage = {}
    setattr(persistent_load, "storage", storage)
    return storage


def get_file_safe_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*')


def load_data_package_for_checksum(game: str, checksum: typing.Optional[str]) -> dict[str, Any]:
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        path = cache_path("datapackage", get_file_safe_name(game), f"{checksum}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except Exception as e:
                logger.debug(f"Could not load data package: {e}")

    # fall back to old cache
    cache = persistent_load().get("datapackage", {}).get("games", {}).get(game, {})
    if cache.get("checksum") == checksum:
        return cache

    # cache does not match
    return {}


def store_data_package_for_checksum(game: str, data: typing.Dict[str, Any]) -> None:
    checksum = data.get("checksum")
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        game_folder = cache_path("datapackage", get_file_safe_name(game))
        os.makedirs(game_folder, exist_ok=True)
        try:
            with open(os.path.join(game_folder, f"{checksum}.json"), "w", encoding="utf-8-sig") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        except Exception as e:
            logger.debug(f"Could not store data package: {e}")


def read_apignore(filename: str | pathlib.Path) -> PathSpec | None:
    try:
        with open(filename) as ignore_file:
            return GitIgnoreSpec.from_lines(ignore_file)
    except FileNotFoundError:
        return None


def get_adjuster_settings_no_defaults(game_name: str) -> Namespace:
    return persistent_load().get("adjuster", {}).get(game_name, Namespace())


@cache_argsless
def get_unique_identifier():
    common_path = cache_path("common.json")
    if os.path.exists(common_path):
        with open(common_path) as f:
            common_file = json.load(f)
            uuid = common_file.get("uuid", None)
    else:
        common_file = {}
        uuid = None

    if uuid:
        return uuid

    from uuid import uuid4
    uuid = str(uuid4())
    common_file["uuid"] = uuid
    with open(common_path, "w") as f:
        json.dump(common_file, f, separators=(",", ":"))
    return uuid


safe_builtins = frozenset((
    'set',
    'frozenset',
))


class RestrictedUnpickler(pickle.Unpickler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RestrictedUnpickler, self).__init__(*args, **kwargs)
        self.options_module = importlib.import_module("Options")
        self.net_utils_module = importlib.import_module("NetUtils")

    def find_class(self, module: str, name: str) -> type:
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # used by OptionCounter
        # necessary because the actual Options class instances are pickled when transfered to WebHost generation pool
        if module == "collections" and name == "Counter":
            return collections.Counter
        # used by MultiServer -> savegame/multidata
        if module == "NetUtils" and name in {"NetworkItem", "ClientStatus", "Hint",
                                             "SlotType", "NetworkSlot", "HintStatus"}:
            return getattr(self.net_utils_module, name)
        # Options and Plando are unpickled by WebHost -> Generate
        # pep 8 specifies that modules should have "all-lowercase names" (options, not Options)
        # check if the end module contains the word "option" in it
        if "option" in module.lower().rsplit('.', 1)[-1]:
            if module == "Options":
                mod = self.options_module
            else:
                mod = importlib.import_module(module)
            obj = getattr(mod, name)
            if issubclass(obj, (self.options_module.Option, self.options_module.PlandoConnection,
                                self.options_module.PlandoItem, self.options_module.PlandoText)):
                return obj
        # Forbid everything else.
        raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")


def restricted_loads(s: bytes) -> Any:
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()


def restricted_dumps(obj: Any) -> bytes:
    """Helper function analogous to pickle.dumps()."""
    s = pickle.dumps(obj)
    # Assert that the string can be successfully loaded by restricted_loads
    try:
        restricted_loads(s)
    except pickle.UnpicklingError as e:
        raise pickle.PicklingError(e) from e

    return s


class ByValue:
    """
    Mixin for enums to pickle value instead of name (restores pre-3.11 behavior). Use as left-most parent.
    See https://github.com/python/cpython/pull/26658 for why this exists.
    """
    def __reduce_ex__(self, prot):
        return self.__class__, (self._value_, )


class KeyedDefaultDict(collections.defaultdict):
    """defaultdict variant that uses the missing key as argument to default_factory"""
    default_factory: typing.Callable[[typing.Any], typing.Any]

    def __init__(self,
                 default_factory: typing.Callable[[Any], Any] = None,
                 seq: typing.Union[typing.Mapping, typing.Iterable, None] = None,
                 **kwargs):
        if seq is not None:
            super().__init__(default_factory, seq, **kwargs)
        else:
            super().__init__(default_factory, **kwargs)

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value


def get_text_between(text: str, start: str, end: str) -> str:
    return text[text.index(start) + len(start): text.rindex(end)]


def get_text_after(text: str, start: str) -> str:
    return text[text.index(start) + len(start):]


def stream_input(stream: typing.TextIO, queue: "asyncio.Queue[str]"):
    def queuer():
        while 1:
            try:
                text = stream.readline().strip()
            except UnicodeDecodeError as e:
                logging.exception(e)
            else:
                if text:
                    queue.put_nowait(text)
                else:
                    sleep(0.01)  # non-blocking stream

    from threading import Thread
    thread = Thread(target=queuer, name=f"Stream handler for {stream.name}", daemon=True)
    thread.start()
    return thread


def tkinter_center_window(window: "tkinter.Tk") -> None:
    window.update()
    x = int(window.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2)
    y = int(window.winfo_screenheight() / 2 - window.winfo_reqheight() / 2)
    window.geometry(f"+{x}+{y}")


class VersionException(Exception):
    pass


def chaining_prefix(index: int, labels: typing.Sequence[str]) -> str:
    text = ""
    max_label = len(labels) - 1
    while index > max_label:
        text += labels[-1]
        index -= max_label
    return labels[index] + text


# noinspection PyPep8Naming
def format_SI_prefix(value, power=1000, power_labels=("", "k", "M", "G", "T", "P", "E", "Z", "Y")) -> str:
    """Formats a value into a value + metric/si prefix. More info at https://en.wikipedia.org/wiki/Metric_prefix"""
    import decimal
    n = 0
    value = decimal.Decimal(value)
    limit = power - decimal.Decimal("0.005")
    while value >= limit:
        value /= power
        n += 1

    return f"{value.quantize(decimal.Decimal('1.00'))} {chaining_prefix(n, power_labels)}"


def get_fuzzy_results(input_word: str, word_list: typing.Collection[str], limit: typing.Optional[int] = None) \
        -> typing.List[typing.Tuple[str, int]]:
    import jellyfish

    def get_fuzzy_ratio(word1: str, word2: str) -> float:
        if word1 == word2:
            return 1.01
        return (1 - jellyfish.damerau_levenshtein_distance(word1.lower(), word2.lower())
                / max(len(word1), len(word2)))

    limit = limit if limit else len(word_list)
    return list(
        map(
            lambda container: (container[0], int(container[1]*100)),  # convert up to limit to int %
            sorted(
                map(lambda candidate: (candidate, get_fuzzy_ratio(input_word, candidate)), word_list),
                key=lambda element: element[1],
                reverse=True
            )[0:limit]
        )
    )


def get_intended_text(input_text: str, possible_answers) -> typing.Tuple[str, bool, str]:
    picks = get_fuzzy_results(input_text, possible_answers, limit=2)
    if len(picks) > 1:
        dif = picks[0][1] - picks[1][1]
        if picks[0][1] == 101:
            return picks[0][0], True, "Perfect Match"
        elif picks[0][1] == 100:
            return picks[0][0], True, "Case Insensitive Perfect Match"
        elif picks[0][1] < 75:
            return picks[0][0], False, f"Didn't find something that closely matches '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"
        elif dif > 5:
            return picks[0][0], True, "Close Match"
        else:
            return picks[0][0], False, f"Too many close matches for '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"
    else:
        if picks[0][1] > 90:
            return picks[0][0], True, "Only Option Match"
        else:
            return picks[0][0], False, f"Didn't find something that closely matches '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"


def get_input_text_from_response(text: str, command: str) -> typing.Optional[str]:
    if "did you mean " in text:
        for question in ("Didn't find something that closely matches",
                         "Too many close matches"):
            if text.startswith(question):
                name = get_text_between(text, "did you mean '",
                                        "'? (")
                return f"!{command} {name}"
    elif text.startswith("Missing: "):
        return text.replace("Missing: ", "!hint_location ")
    return None


def is_kivy_running() -> bool:
    if "kivy" in sys.modules:
        from kivy.app import App
        return App.get_running_app() is not None
    return False


def env_cleared_lib_path() -> Mapping[str, str]:
    """
    Creates a copy of the current environment vars with the LD_LIBRARY_PATH removed if set, as this can interfere when
    launching something in a subprocess.
    """
    env = os.environ
    if "LD_LIBRARY_PATH" in env:
        env = env.copy()
        del env["LD_LIBRARY_PATH"]

    return env


def _mp_open_filename(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(open_file_input_dialog(*args))


def _mp_save_filename(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(save_filename(*args))
    
def _run_for_stdout(*args: str):
    env = env_cleared_lib_path()
    return subprocess.run(args, capture_output=True, text=True, env=env).stdout.split("\n", 1)[0] or None


def _mp_open_directory(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(open_directory(*args))


def open_directory(title: str, suggest: str = "") -> typing.Optional[str]:
    if is_linux:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            return _run_for_stdout(kdialog, f"--title={title}", "--getexistingdirectory",
                       os.path.abspath(suggest) if suggest else ".")
        zenity = which("zenity")
        if zenity:
            z_filters = ("--directory",)
            selection = (f"--filename={os.path.abspath(suggest)}/",) if suggest else ()
            return _run_for_stdout(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because open_directory was used for "{title}".')
        raise e
    else:
        if is_macos and is_kivy_running():
            # on macOS, mixing kivy and tk does not work, so spawn a new process
            # FIXME: performance of this is pretty bad, and we should (also) look into alternatives
            from multiprocessing import Process, Queue
            res: "Queue[typing.Optional[str]]" = Queue()
            Process(target=_mp_open_directory, args=(res, title, suggest)).start()
            return res.get()
        try:
            root = tkinter.Tk()
        except tkinter.TclError:
            return None  # GUI not available. None is the same as a user clicking "cancel"
        root.withdraw()
        return tkinter.filedialog.askdirectory(title=title, mustexist=True, initialdir=suggest or None)


def messagebox(title: str, text: str, error: bool = False) -> None:
    if not gui_enabled:
        if error:
            logging.error(f"{title}: {text}")
        else:
            logging.info(f"{title}: {text}")
        return

    if is_kivy_running():
        from mwgg_gui.components.dialog import MessageBox
        MessageBox(title, text, error).open()
        return

    if is_linux and "tkinter" not in sys.modules:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            return _run_for_stdout(kdialog, f"--title={title}", "--error" if error else "--msgbox", text)
        zenity = which("zenity")
        if zenity:
            return _run_for_stdout(zenity, f"--title={title}", f"--text={text}", "--error" if error else "--info")

    elif is_windows:
        import ctypes
        style = 0x10 if error else 0x0
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    # fall back to tk
    try:
        import tkinter
        from tkinter.messagebox import showerror, showinfo
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because messagebox was used for "{title}".')
        raise e
    else:
        root = tkinter.Tk()
        root.withdraw()
        showerror(title, text) if error else showinfo(title, text)
        root.update()


gui_enabled = not sys.stdout or "--nogui" not in sys.argv
"""Checks if the user wanted no GUI mode and has a terminal to use it with."""

def title_sorted(data: typing.Iterable, key=None, ignore: typing.AbstractSet[str] = frozenset(("a", "the"))):
    """Sorts a sequence of text ignoring typical articles like "a" or "the" in the beginning."""
    def sorter(element: Union[str, dict[str, Any]]) -> str:
        if (not isinstance(element, str)):
            element = element["title"]

        parts = element.split(maxsplit=1)
        
        return element.lower()
    return sorted(data, key=lambda i: sorter(key(i)) if key else sorter(i))

def world_list_sorted(data: typing.Iterable, worlds: dict[str, Any]):
    def sorter(key_or_name):
        name = key_or_name
        world = worlds[name]

        raw = getattr(world.web, "display_name", None) or world.game or name

        return raw.lower()

    return sorted(data, key=lambda k: sorter(k))

def read_snes_rom(stream: BinaryIO, strip_header: bool = True) -> bytearray:
    """Reads rom into bytearray and optionally strips off any smc header"""
    buffer = bytearray(stream.read())
    if strip_header and len(buffer) % 0x400 == 0x200:
        return buffer[0x200:]
    return buffer


_faf_tasks: "set[asyncio.Task[typing.Any]]" = set()


def async_start(co: Coroutine[None, None, typing.Any], name: Optional[str] = None) -> None:
    """
    Use this to start a task when you don't keep a reference to it or immediately await it,
    to prevent early garbage collection. "fire-and-forget"
    """
    # https://docs.python.org/3.12/library/asyncio-task.html#asyncio.create_task
    # Python docs:
    # ```
    # Important: Save a reference to the result of [asyncio.create_task],
    # to avoid a task disappearing mid-execution.
    # ```
    # This implementation follows the pattern given in that documentation.

    task: asyncio.Task[typing.Any] = asyncio.create_task(co, name=name)
    _faf_tasks.add(task)
    task.add_done_callback(_faf_tasks.discard)


def deprecate(message: str, add_stacklevels: int = 0):
    """also use typing_extensions.deprecated wherever you use this"""
    if __debug__:
        raise Exception(message)
    warnings.warn(message, stacklevel=2 + add_stacklevels)


class DeprecateDict(dict):
    log_message: str
    should_error: bool

    def __init__(self, message: str, error: bool = False) -> None:
        self.log_message = message
        self.should_error = error
        super().__init__()

    def __getitem__(self, item: Any) -> Any:
        if self.should_error:
            deprecate(self.log_message, add_stacklevels=1)
        elif __debug__:
            warnings.warn(self.log_message, stacklevel=2)
        return super().__getitem__(item)


def _extend_freeze_support() -> None:
    """Extend multiprocessing.freeze_support() to also work on Non-Windows and without setting spawn method first."""
    # original upstream issue: https://github.com/python/cpython/issues/76327
    # code based on https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/hooks/rthooks/pyi_rth_multiprocessing.py#L26
    import multiprocessing
    import multiprocessing.spawn

    def _freeze_support() -> None:
        """Minimal freeze_support. Only apply this if frozen."""
        from subprocess import _args_from_interpreter_flags  # noqa

        # Prevent `spawn` from trying to read `__main__` in from the main script
        multiprocessing.process.ORIGINAL_DIR = None

        # Handle the first process that MP will create
        if (
            len(sys.argv) >= 2 and sys.argv[-2] == '-c' and sys.argv[-1].startswith((
                'from multiprocessing.resource_tracker import main',
                'from multiprocessing.forkserver import main'
            )) and set(sys.argv[1:-2]) == set(_args_from_interpreter_flags())
        ):
            exec(sys.argv[-1])
            sys.exit()

        # Handle the second process that MP will create
        if multiprocessing.spawn.is_forking(sys.argv):
            # In frozen builds, child processes may need to import world modules
            # packaged as .apworld archives (for example worlds.tracker).
            # Register zip specs before spawn_main unpickles target callables.
            try:
                import worlds
                world_sources = getattr(worlds, "world_sources", ())
                for world_source in world_sources:
                    if getattr(world_source, "is_zip", False):
                        worlds._register_apworld_zip_spec(world_source)  # type: ignore[attr-defined]
            except Exception:
                pass

            kwargs = {}
            for arg in sys.argv[2:]:
                name, value = arg.split('=')
                if value == 'None':
                    kwargs[name] = None
                else:
                    kwargs[name] = int(value)
            multiprocessing.spawn.spawn_main(**kwargs)
            sys.exit()

    def _noop() -> None:
        pass

    multiprocessing.freeze_support = multiprocessing.spawn.freeze_support = _freeze_support if is_frozen() else _noop


def freeze_support() -> None:
    """This now only calls multiprocessing.freeze_support since we are patching freeze_support on module load."""
    import multiprocessing

    deprecate("Use multiprocessing.freeze_support() instead")
    multiprocessing.freeze_support()


_extend_freeze_support()


def visualize_regions(
        root_region: Region,
        file_name: str,
        *,
        show_entrance_names: bool = False,
        show_locations: bool = True,
        show_other_regions: bool = True,
        linetype_ortho: bool = True,
        regions_to_highlight: set[Region] | None = None,
        entrance_highlighting: dict[int, int] | None = None,
        detail_other_regions: bool = False,
        auto_assign_colors: bool = False) -> None:
    """Visualize the layout of a world as a PlantUML diagram.

    :param root_region: The region from which to start the diagram from. (Usually the "Menu" region of your world.)
    :param file_name: The name of the destination .puml file.
    :param show_entrance_names: (default False) If enabled, the name of the entrance will be shown near each connection.
    :param show_locations: (default True) If enabled, the locations will be listed inside each region.
            Priority locations will be shown in bold.
            Excluded locations will be stricken out.
            Locations without ID will be shown in italics.
            Locked locations will be shown with a padlock icon.
            For filled locations, the item name will be shown after the location name.
            Progression items will be shown in bold.
            Items without ID will be shown in italics.
    :param show_other_regions: (default True) If enabled, regions that can't be reached by traversing exits are shown.
    :param linetype_ortho: (default True) If enabled, orthogonal straight line parts will be used; otherwise polylines.
    :param regions_to_highlight: Regions that will be highlighted in green if they are reachable.
    :param entrance_highlighting: a mapping from your world's entrance randomization groups to RGB values, used to color
            your entrances
    :param detail_other_regions: (default False) If enabled, will fully visualize regions that aren't reachable
            from root_region.
    :param auto_assign_colors: (default False) If enabled, will automatically assign random colors to entrances of the
            same randomization group. Uses entrance_highlighting first, and only picks random colors for entrance groups
            not found in the passed-in map

    Example usage in World code:
    from Utils import visualize_regions
    state = self.multiworld.get_all_state(False)
    state.update_reachable_regions(self.player)
    visualize_regions(self.get_region("Menu"), "my_world.puml", show_entrance_names=True,
                      regions_to_highlight=state.reachable_regions[self.player])

    Example usage in Main code:
    from Utils import visualize_regions
    for player in multiworld.player_ids:
        visualize_regions(multiworld.get_region("Menu", player), f"{multiworld.get_out_file_name_base(player)}.puml")
    """
    if regions_to_highlight is None:
        regions_to_highlight = set()
    assert root_region.multiworld, "The multiworld attribute of root_region has to be filled"
    from BaseClasses import Entrance, Item, Location, LocationProgressType, MultiWorld, Region
    from collections import deque
    import re

    uml: typing.List[str] = list()
    seen: typing.Set[Region] = set()
    regions: typing.Deque[Region] = deque((root_region,))
    multiworld: MultiWorld = root_region.multiworld

    colors_used: set[int] = set()
    if entrance_highlighting:
        for color in entrance_highlighting.values():
            # filter the colors to their most-significant bits to avoid too similar colors
            colors_used.add(color & 0xF0F0F0)
    else:
        # assign an empty dict to not crash later
        # the parameter is optional for ease of use when you don't care about colors
        entrance_highlighting = {}

    def select_color(group: int) -> int:
        # specifically spacing color indexes by three different prime numbers (3, 5, 7) for the RGB components to avoid
        # obvious cyclical color patterns
        COLOR_INDEX_SPACING: int = 0x357
        new_color_index: int = (group * COLOR_INDEX_SPACING) % 0x1000
        new_color = ((new_color_index & 0xF00) << 12) + \
                    ((new_color_index & 0xF0) << 8) + \
                    ((new_color_index & 0xF) << 4)
        while new_color in colors_used:
            # while this is technically unbounded, expected collisions are low. There are 4095 possible colors
            # and worlds are unlikely to get to anywhere close to that many entrance groups
            # intentionally not using multiworld.random to not affect output when debugging with this tool
            new_color_index += COLOR_INDEX_SPACING
            new_color = ((new_color_index & 0xF00) << 12) + \
                        ((new_color_index & 0xF0) << 8) + \
                        ((new_color_index & 0xF) << 4)
        return new_color

    def fmt(obj: Union[Entrance, Item, Location, Region]) -> str:
        name = obj.name
        if isinstance(obj, Item):
            name = multiworld.get_name_string_for_object(obj)
            if obj.advancement:
                name = f"**{name}**"
            if obj.code is None:
                name = f"//{name}//"
        if isinstance(obj, Location):
            if obj.progress_type == LocationProgressType.PRIORITY:
                name = f"**{name}**"
            elif obj.progress_type == LocationProgressType.EXCLUDED:
                name = f"--{name}--"
            if obj.address is None:
                name = f"//{name}//"
        return re.sub("[\".:]", "", name)

    def visualize_exits(region: Region) -> None:
        for exit_ in region.exits:
            color_code: str = ""
            if exit_.randomization_group in entrance_highlighting:
                color_code = f" #{entrance_highlighting[exit_.randomization_group]:0>6X}"
            if exit_.connected_region:
                if show_entrance_names:
                    uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\" : \"{fmt(exit_)}\"{color_code}")
                else:
                    try:
                        uml.remove(f"\"{fmt(exit_.connected_region)}\" --> \"{fmt(region)}\"{color_code}")
                        uml.append(f"\"{fmt(exit_.connected_region)}\" <--> \"{fmt(region)}\"{color_code}")
                    except ValueError:
                        uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\"{color_code}")
            else:
                uml.append(f"circle \"unconnected exit:\\n{fmt(exit_)}\" {color_code}")
                uml.append(f"\"{fmt(region)}\" --> \"unconnected exit:\\n{fmt(exit_)}\"{color_code}")
        for entrance in region.entrances:
            color_code: str = ""
            if entrance.randomization_group in entrance_highlighting:
                color_code = f" #{entrance_highlighting[entrance.randomization_group]:0>6X}"
            if not entrance.parent_region:
                uml.append(f"circle \"unconnected entrance:\\n{fmt(entrance)}\"{color_code}")
                uml.append(f"\"unconnected entrance:\\n{fmt(entrance)}\" --> \"{fmt(region)}\"{color_code}")

    def visualize_locations(region: Region) -> None:
        any_lock = any(location.locked for location in region.locations)
        for location in region.locations:
            lock = "<&lock-locked> " if location.locked else "<&lock-unlocked,color=transparent> " if any_lock else ""
            if location.item:
                uml.append(f"\"{fmt(region)}\" : {{method}} {lock}{fmt(location)}: {fmt(location.item)}")
            else:
                uml.append(f"\"{fmt(region)}\" : {{field}} {lock}{fmt(location)}")

    def visualize_region(region: Region) -> None:
        uml.append(f"class \"{fmt(region)}\" {'#00FF00' if region in regions_to_highlight else ''}")
        if show_locations:
            visualize_locations(region)
        visualize_exits(region)

    def visualize_other_regions() -> None:
        if other_regions := [region for region in multiworld.get_regions(root_region.player) if region not in seen]:
            uml.append("package \"other regions\" <<Cloud>> {")
            for region in other_regions:
                if detail_other_regions:
                    visualize_region(region)
                else:
                    uml.append(f"class \"{fmt(region)}\"")
            uml.append("}")

    if auto_assign_colors:
        all_entrances: list[Entrance] = []
        for region in multiworld.get_regions(root_region.player):
            all_entrances.extend(region.entrances)
            all_entrances.extend(region.exits)
        all_groups: list[int] = sorted(set([entrance.randomization_group for entrance in all_entrances]))
        for group in all_groups:
            if group not in entrance_highlighting:
                if len(colors_used) >= 0x1000:
                    # on the off chance someone makes 4096 different entrance groups, don't cycle forever
                    break
                new_color: int = select_color(group)
                entrance_highlighting[group] = new_color
                colors_used.add(new_color)

    uml.append("@startuml")
    uml.append("hide circle")
    uml.append("hide empty members")
    if linetype_ortho:
        uml.append("skinparam linetype ortho")
    while regions:
        if (current_region := regions.popleft()) not in seen:
            seen.add(current_region)
            visualize_region(current_region)
            regions.extend(exit_.connected_region for exit_ in current_region.exits if exit_.connected_region)
    if show_other_regions or detail_other_regions:
        visualize_other_regions()
    uml.append("@enduml")

    with open(file_name, "wt", encoding="utf-8") as f:
        f.write("\n".join(uml))


class RepeatableChain:
    def __init__(self, iterable: typing.Iterable):
        self.iterable = iterable

    def __iter__(self):
        return itertools.chain.from_iterable(self.iterable)

    def __bool__(self):
        return any(sub_iterable for sub_iterable in self.iterable)

    def __len__(self):
        return sum(len(iterable) for iterable in self.iterable)


def is_iterable_except_str(obj: object) -> TypeGuard[typing.Iterable[typing.Any]]:
    """ `str` is `Iterable`, but that's not what we want """
    if isinstance(obj, str):
        return False
    return isinstance(obj, typing.Iterable)


def utcnow() -> datetime:
    """
    Implementation of Python's datetime.utcnow() function for use after deprecation.
    Needed for timezone-naive UTC datetimes stored in databases with PonyORM (upstream).
    https://ponyorm.org/ponyorm-list/2014-August/000113.html
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class DaemonThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    """
    ThreadPoolExecutor that uses daemonic threads that do not keep the program alive.
    NOTE: use this with caution because killed threads will not properly clean up.
    """

    def _adjust_thread_count(self):
        # see upstream ThreadPoolExecutor for details
        import threading
        import weakref
        from concurrent.futures.thread import _worker

        if self._idle_semaphore.acquire(timeout=0):
            return

        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = f"{self._thread_name_prefix or self}_{num_threads}"
            t = threading.Thread(
                name=thread_name,
                target=_worker,
                args=(
                    weakref.ref(self, weakref_cb),
                    self._work_queue,
                    self._initializer,
                    self._initargs,
                ),
                daemon=True,
            )
            t.start()
            self._threads.add(t)
            # NOTE: don't add to _threads_queues so we don't block on shutdown


def get_full_typename(t: type) -> str:
    """Returns the full qualified name of a type, including its module (if not builtins)."""
    module = t.__module__
    if module and module != "builtins":
        return f"{module}.{t.__qualname__}"
    return t.__qualname__


def get_all_causes(ex: Exception) -> str:
    """Return a string describing the recursive causes of this exception.

    :param ex: The exception to be described.
    :return A multiline string starting with the initial exception on the first line and each resulting exception
            on subsequent lines with progressive indentation.

            For example:

            ```
            Exception: Invalid value 'bad'.
             Which caused: Options.OptionError: Error generating option
              Which caused: ValueError: File bad.yaml is invalid.
            ```
    """
    cause = ex
    causes = [f"{get_full_typename(type(ex))}: {ex}"]
    while cause := cause.__cause__:
        causes.append(f"{get_full_typename(type(cause))}: {cause}")
    top = causes[-1]
    others = "".join(f"\n{' ' * (i + 1)}Which caused: {c}" for i, c in enumerate(reversed(causes[:-1])))
    return f"{top}{others}"
