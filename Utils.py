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

import re

from argparse import Namespace
from settings import Settings, get_settings
from time import sleep
from typing import BinaryIO, Coroutine, Optional, Set, Dict, Any, Union, TypeGuard
from yaml import load, load_all, dump

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

if typing.TYPE_CHECKING:
    import tkinter
    import pathlib
    from BaseClasses import Region
    import multiprocessing

def normalize_tag(tag: str) -> str:
    return tag[1:] if tag and tag[0].lower() == "v" else tag

def get_config_file_path() -> str:
    if getattr(sys, 'frozen', False):
        # When frozen, the executable's directory is the base path.
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "application.yaml")

config_file = get_config_file_path()

# Check for APP_VERSION environment variable first (set by GitHub Actions build)
env_version = os.environ.get("APP_VERSION")
if env_version:
    __version__ = env_version
    version_tuple = tuplize_version(__version__)
    version = Version(*version_tuple)
    logger.info("Using version from APP_VERSION environment variable: %s", __version__)

if os.path.exists(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = load(f, Loader=SafeLoader)
        if isinstance(config_data, dict):
            app_options = config_data.get("application_options", {})
            if isinstance(app_options, dict):
                new_name = app_options.get("app_name")
                if new_name is not None:
                    instance_name = new_name
                new_guid = app_options.get("app_guid")
                if new_guid is not None:
                    archipelago_guid = new_guid
                # Only override version from config if not set by environment variable
                if not env_version:
                    new_version = app_options.get("app_version")
                    if new_version is not None:
                        __version__ = new_version
                        version_tuple = tuplize_version(__version__)
                        version = Version(*version_tuple)
    except Exception as e:
        logger.warning("Failed to load configuration from %s: %s", config_file, e)

is_linux = sys.platform.startswith("linux")
is_macos = sys.platform == "darwin"
is_windows = sys.platform in ("win32", "cygwin", "msys")

_worlds_to_load: typing.List[str] = ["worlds.generic"]

def set_game_names(game_names: typing.List[str]):
    """Set the game names to the list of game names"""
    from mwgg_igdb import GameIndex
    # lazy import
    for game in game_names:
        module_name = GameIndex.get_module_for_game(game_name=game, worlds=True)
        _worlds_to_load.append(module_name) if module_name else update_logger.warning(f"Game {game} not found in game index")
    _worlds_to_install: typing.List[str] = []
    for module_name in _worlds_to_load:
        try:
            importlib.metadata.distribution(module_name)
        except importlib.metadata.PackageNotFoundError:
            update_logger.warning(f"Module {module_name} not found, looking in worlds pypi index.")
            _worlds_to_install.append(module_name)
    if _worlds_to_install:
        restart_needed = ModuleUpdate.install_worlds(_worlds_to_install)
        if restart_needed:
            # Library updates were staged, need to restart
            exit_restart_for_update()

def game_names() -> typing.List[str]:
    """Get a list of only the game names that we're using"""
    return _worlds_to_load

def get_available_worlds() -> typing.List[str]:
    """Get a list of all of the available worlds"""

    from ModuleUpdate import find_world_modules
    available_worlds = find_world_modules()
    return available_worlds

def discover_and_launch_module(module_name: str, **kwargs) -> Optional[callable]:
    """Discover and launch module via entrypoints"""
    import threading
    import asyncio
    from kivy.clock import Clock
    
    # First, try to import the module to see if it exists
    if not module_name.startswith("worlds."):
        module_name = f"worlds.{module_name}"
    
    def _install_module_threaded():
        """Install module in a separate thread"""
        try:
            restart = ModuleUpdate.install_worlds([module_name])
            if restart:
                # Restart needed - schedule callback on main thread
                raise ModuleUpdate.RestartException
            else:
                # No restart needed - proceed with launch
                Clock.schedule_once(lambda dt: _launch_module_after_install(), 0)
        except ModuleUpdate.RestartException as re:
            # Restart needed - schedule callback on main thread
            Clock.schedule_once(lambda dt: _handle_install_error("Restart required for world updates."), 0)

        except Exception as e:
            update_logger.error(f"Failed to update module {module_name}: {str(e)}")
            # Schedule error handling on main thread
            Clock.schedule_once(lambda dt: _handle_install_error(str(e)), 0)
    
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
        # Log the error but don't raise it since we're in a Clock callback
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
        if module_id:
            while True:
                # Wait until the module is installed before trying to import it
                try:
                    # Invalidate import caches to pick up freshly installed modules
                    importlib.invalidate_caches()
                    importlib.import_module(module_id)
                    break
                except ModuleNotFoundError:
                    sleep(1)
                except Exception as e:
                    update_logger.error(f"Failed to import module {module_id}: {e}")
                    raise e

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
                result = launch_function(**kwargs)
                
                # Check if the launch function returned a task (GUI mode)
                if hasattr(result, '_coro'):
                    logging.info(f"Launch function returned a task for {module_id}, running in GUI mode")
                    # The task is already scheduled in the event loop
                    return result
                else:
                    logging.info(f"Launch function completed synchronously for {module_id}")
                    return result
                            
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
        # Call error callback if provided
        if 'error_callback' in kwargs and kwargs['error_callback']:
            try:
                kwargs['error_callback']()
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
        cache: Optional[Dict[T, RetType]] = getattr(self, cache_name, None)
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

        env = os.environ
        if "LD_LIBRARY_PATH" in env:
            env = env.copy()
            del env["LD_LIBRARY_PATH"]  # exe is a system binary, so reset LD_LIBRARY_PATH
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


def persistent_load() -> Dict[str, Dict[str, Any]]:
    storage: Union[Dict[str, Dict[str, Any]], None] = getattr(persistent_load, "storage", None)
    if storage:
        return storage
    path = user_path("_persistent_storage.yaml")
    storage = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                storage = unsafe_parse_yaml(f.read())
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


def load_data_package_for_checksum(game: str, checksum: typing.Optional[str]) -> Dict[str, Any]:
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


def _mp_open_filename(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(open_file_input_dialog(*args))


def _mp_save_filename(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(save_filename(*args))
    
def _run_for_stdout(*args: str):
    env = os.environ
    if "LD_LIBRARY_PATH" in env:
        env = env.copy()
        del env["LD_LIBRARY_PATH"]  # exe is a system binary, so reset LD_LIBRARY_PATH
    return subprocess.run(args, capture_output=True, text=True, env=env).stdout.split("\n", 1)[0] or None


def _mp_open_directory(res: "multiprocessing.Queue[typing.Optional[str]]", *args: Any) -> None:
    if is_kivy_running():
        raise RuntimeError("kivy should not be running in multiprocess")
    res.put(open_directory(*args))


def messagebox(title: str, text: str, error: bool = False) -> None:
    if is_kivy_running():
        from Gui import MessageBox
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


def title_sorted(data: typing.Iterable, key=None, ignore: typing.AbstractSet[str] = frozenset(("a", "the"))):
    """Sorts a sequence of text ignoring typical articles like "a" or "the" in the beginning."""
    def sorter(element: Union[str, Dict[str, Any]]) -> str:
        if (not isinstance(element, str)):
            element = element["title"]

        parts = element.split(maxsplit=1)
        
        return element.lower()
    return sorted(data, key=lambda i: sorter(key(i)) if key else sorter(i))

def world_list_sorted(data: typing.Iterable, worlds: Dict[str, Any]):
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


_faf_tasks: "Set[asyncio.Task[typing.Any]]" = set()


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

_extend_freeze_support()

def visualize_regions(root_region: Region, file_name: str, *,
                      show_entrance_names: bool = False, show_locations: bool = True, show_other_regions: bool = True,
                      linetype_ortho: bool = True, regions_to_highlight: set[Region] | None = None) -> None:
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
            if exit_.connected_region:
                if show_entrance_names:
                    uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\" : \"{fmt(exit_)}\"")
                else:
                    try:
                        uml.remove(f"\"{fmt(exit_.connected_region)}\" --> \"{fmt(region)}\"")
                        uml.append(f"\"{fmt(exit_.connected_region)}\" <--> \"{fmt(region)}\"")
                    except ValueError:
                        uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\"")
            else:
                uml.append(f"circle \"unconnected exit:\\n{fmt(exit_)}\"")
                uml.append(f"\"{fmt(region)}\" --> \"unconnected exit:\\n{fmt(exit_)}\"")

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
                uml.append(f"class \"{fmt(region)}\"")
            uml.append("}")

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
    if show_other_regions:
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
