import os
import sys
import typing
import logging
import io
import warnings
import json
import subprocess
from pathlib import Path

__all__ = ("Version",
           "tuplize_version",
           "__version__",
           "version_tuple",
           "core_version",
           "core_version_tuple",
           "instance_name",
           "archipelago_guid",
           "FROZEN_TARGETS",
           "is_linux",
           "is_macos",
           "is_windows",
           "is_frozen",
           "local_path",
           "user_path",
           "output_path",
           "cache_path",
           "write_path",
           "use_worlds_venv",
           "mwgg_venv_site_packages",
           "mwgg_venv_python",
           "reload_application_options",
           "get_frontend_versions",
           "init_logging",
           "loglevel_mapping",
           "ByValue",
           "get_client_exe",
           "launch_exe",
           "spawn_client")

class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int

    def as_simple_string(self) -> str:
        """Return version as a simple dot-separated string."""
        return ".".join(str(item) for item in self)
    
    def as_pep440_string(self) -> str:
        """Return version as a PEP 440 compliant string."""
        return f"{self.major}.{self.minor}.{self.build}"
    
    def __str__(self) -> str:
        """String representation defaults to PEP 440 format."""
        return self.as_pep440_string()

def tuplize_version(version: str) -> Version:
    """Parse a version string into a Version object, supporting both simple and PEP 440 formats."""
    try:
        # Try using packaging library for PEP 440 support
        from packaging.version import Version as PackagingVersion
        pkg_version = PackagingVersion(version)
        # Extract the release components (major.minor.micro)
        release = pkg_version.release
        if len(release) >= 3:
            return Version(release[0], release[1], release[2])
        elif len(release) == 2:
            return Version(release[0], release[1], 0)
        elif len(release) == 1:
            return Version(release[0], 0, 0)
        else:
            return Version(0, 0, 0)
    except ImportError:
        # Fallback to simple parsing if packaging is not available
        pass
    except Exception:
        # If packaging fails to parse, fall back to simple parsing
        pass
    
    # int() would crash on suffixed parts like "0b7" and yield Version(0, 0, 0),
    # making every Connect packet get refused with IncompatibleVersion.
    import re
    def _leading_int(part: str) -> int:
        m = re.match(r"^(\d+)", part)
        return int(m.group(1)) if m else 0
    try:
        parts = version.split(".")
        return Version(
            _leading_int(parts[0]) if len(parts) > 0 else 0,
            _leading_int(parts[1]) if len(parts) > 1 else 0,
            _leading_int(parts[2]) if len(parts) > 2 else 0,
        )
    except (ValueError, IndexError):
        return Version(0, 0, 0)

__version__ = "0.6.7"
version_tuple = tuplize_version(__version__)
# Core compatibility should ignore application.yaml branding/version overrides.
core_version = __version__
core_version_tuple = version_tuple

instance_name = "MultiworldGG"
archipelago_guid = "{{918BA46A-FAB8-460C-9DFF-AE691E1C865D}}"

# Frozen exe base names (no .exe suffix), single source of truth. Do NOT derive
# from instance_name: application.yaml's app_name overrides it at runtime and
# silently breaks exe resolution in non-default channels.
FROZEN_TARGETS = {
    "MultiWorld": "MultiworldGG",
    "MultiServer": "MultiworldGGServer",
    "Generate": "MultiworldGGGenerate",
    "Patch": "MultiworldGGPatch",
    "MultiWorldDebug": "MultiworldGGClientDebug",
    "Launcher": "MultiworldGGLauncher",
}

_default_version = __version__
_default_instance_name = instance_name
_default_archipelago_guid = archipelago_guid

is_linux = sys.platform.startswith("linux")
is_macos = sys.platform == "darwin"
is_windows = sys.platform in ("win32", "cygwin", "msys")

_stdio_wrapped_for_logging = False

def get_config_file_path() -> str:
    if getattr(sys, 'frozen', False):
        # When frozen, the executable's directory is the base path.
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "application.yaml")

config_file = get_config_file_path()

def reload_application_options() -> None:
    global __version__, version_tuple, instance_name, archipelago_guid

    __version__ = _default_version
    version_tuple = tuplize_version(__version__)
    instance_name = _default_instance_name
    archipelago_guid = _default_archipelago_guid

    if os.path.exists(config_file):
        try:
            from yaml import safe_load
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = safe_load(f)
            if isinstance(config_data, dict):
                app_options = config_data.get("application_options", {})
                if isinstance(app_options, dict):
                    new_name = app_options.get("app_name")
                    if new_name is not None:
                        instance_name = new_name
                    new_guid = app_options.get("app_guid")
                    if new_guid is not None:
                        archipelago_guid = new_guid
                    new_version = app_options.get("app_version")
                    if new_version is not None:
                        __version__ = new_version
                        version_tuple = tuplize_version(__version__)
        except Exception as e:
            logging.warning("Failed to load configuration from %s: %s", config_file, e)

reload_application_options()

def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))

def use_worlds_venv() -> bool:
    return os.environ.get("MWGG_USE_WORLDS_VENV", "") or is_frozen()

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
        try:
            import platformdirs
            home_path.cached_path = platformdirs.user_data_dir("Archipelago", False)
        except (AttributeError, OSError, ImportError) as e:
            # Fallback for macOS if platformdirs fails
            import warnings
            warnings.warn(f"platformdirs failed on macOS ({type(e).__name__}: {e}), using fallback")
            home_path.cached_path = os.path.expanduser(f'~/Library/Application Support/{instance_name}')
        os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    elif sys.platform.startswith('win'):
        # Temporary fix for Windows: SHGetFolderPathW was deprecated and removed
        try:
            import platformdirs
            home_path.cached_path = platformdirs.user_data_dir(instance_name, False)
        except (AttributeError, OSError, ImportError) as e:
            import warnings
            warnings.warn(f"platformdirs failed on Windows ({type(e).__name__}: {e}), using fallback")
            # Use AppData\Local fallback for Windows user data
            appdata_local = os.environ.get('APPDATA', os.path.expanduser('~\\AppData\\Local'))
            home_path.cached_path = os.path.join(appdata_local, instance_name)
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
        try:
            import platformdirs
            cache_path.cached_path = platformdirs.user_cache_dir(instance_name, False)
        except (AttributeError, OSError, ImportError) as e:
            # Temporary fix for Windows: SHGetFolderPathW was deprecated and removed
            import warnings
            warnings.warn(f"platformdirs failed ({type(e).__name__}: {e}), using fallback cache directory")
            
            if sys.platform.startswith('win'):
                # Use AppData\Local fallback for Windows
                appdata_local = os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
                cache_path.cached_path = os.path.join(appdata_local, instance_name)
            else:
                # Fallback for other platforms
                cache_path.cached_path = os.path.expanduser(f'~/.cache/{instance_name}')
        
        # Ensure the cache directory exists
        os.makedirs(cache_path.cached_path, exist_ok=True)

    return os.path.join(cache_path.cached_path, *path)

def output_path(*path: str) -> str:
    """Sets output path
    TODO: This is a Utils override so that the Settings module
    isn't loaded yet. Need to pull the correct output path without
    loading Settings."""
    if hasattr(output_path, 'cached_path'):
        return os.path.join(output_path.cached_path, *path)
    output_path.cached_path = user_path("output")
    path = os.path.join(output_path.cached_path, *path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def write_path(*path: str) -> str:
    """I think that this is the same as home_path, but I don't want to mess with the paths rn"""
    if is_windows:
        return os.path.join((Path.home() / "AppData" / "Local" / "MultiworldGG"), *path)
    elif is_macos:
        return os.path.join((Path.home() / "Library" / "Application Support" / "MultiworldGG"), *path)
    elif is_linux:
        return os.path.join((Path.home() / ".local" / "share" / "MultiworldGG"), *path)
    else:
        raise RuntimeError("Unsupported platform")

def mwgg_venv_python() -> str:
    """Path to the Python interpreter inside the mwgg_venv.

    Frozen builds need this to spawn helper subprocesses that have to actually
    run Python code (e.g. mwgg-gui's yaml worker, pip introspection);
    `sys.executable` in a frozen build points at the cx_Freeze launcher, which
    just runs MultiWorld.py and rejects unknown CLI args.

    On Windows: <write_path('mwgg_venv')>/Scripts/python.exe
    On Linux/macOS: <write_path('mwgg_venv')>/bin/python
    """
    if is_windows:
        return write_path("mwgg_venv", "Scripts", "python.exe")
    return write_path("mwgg_venv", "bin", "python")


def mwgg_venv_site_packages(*path: str) -> str:
    """Path under <write_path('mwgg_venv')>/<lib>/site-packages, where <lib> is
    'Lib' on Windows and 'lib/python<X>.<Y>' on Linux/macOS"""
    if is_windows:
        lib_segments = ("Lib",)
    else:
        lib_segments = ("lib", f"python{sys.version_info.major}.{sys.version_info.minor}")
    return write_path("mwgg_venv", *lib_segments, "site-packages", *path)

class ByValue:
    """
    Mixin for enums to pickle value instead of name (restores pre-3.11 behavior). Use as left-most parent.
    See https://github.com/python/cpython/pull/26658 for why this exists.
    """
    def __reduce_ex__(self, prot):
        return self.__class__, (self._value_, )

loglevel_mapping = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}

_startup_logo_printed = False


def _supports_truecolor() -> bool:
    """Heuristic check for 24-bit color support across common terminals.

    Why not just COLORTERM: Windows Terminal, VS Code, and most Windows
    truecolor terminals don't set it. Each terminal advertises itself
    differently, so we cover the common identifiers explicitly.
    """
    if os.environ.get("COLORTERM", "").strip().lower() in ("truecolor", "24bit"):
        return True
    if os.environ.get("WT_SESSION"):  # Windows Terminal
        return True
    if os.environ.get("TERM_PROGRAM") in ("vscode", "iTerm.app", "WezTerm", "Hyper"):
        return True
    term = os.environ.get("TERM", "")
    if term.startswith("alacritty") or term == "xterm-kitty" or term.endswith("-direct"):
        return True
    return False


def _print_startup_logo() -> None:
    global _startup_logo_printed
    if _startup_logo_printed:
        return
    try:
        if not sys.stdout or not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            _startup_logo_printed = True
            return
        if is_windows:
            try:
                import colorama
                colorama.just_fix_windows_console()
            except ImportError:
                pass
        name = "logo_ascii_true" if _supports_truecolor() else "logo_ascii_256"
        path = local_path("data", "icon", name)
        with open(path, "rb") as f:
            data = f.read()
        buf = getattr(sys.stdout, "buffer", None)
        if buf is not None:
            buf.write(data)
            buf.flush()
        else:
            sys.stdout.write(data.decode("utf-8", errors="replace"))
            sys.stdout.flush()
    except Exception:
        pass
    finally:
        _startup_logo_printed = True


_FRONTEND_PACKAGES = ("mwgg_gui", "mwgg_tui", "mwgg_splash")


def get_frontend_versions() -> "dict[str, str]":
    """Return {package: version} for the bundled frontend packages.

    Reads dist-info via importlib.metadata so the heavy modules (which pull in
    Kivy) are never imported just to read a version. Packages with no
    discoverable metadata report "unknown".
    """
    import importlib.metadata as _md
    versions: dict[str, str] = {}
    for name in _FRONTEND_PACKAGES:
        try:
            versions[name] = _md.version(name)
        except Exception:
            versions[name] = "unknown"
    return versions


def init_logging(name: str, loglevel: typing.Union[str, int] = logging.INFO,
                 write_mode: str = "w", log_format: str = "[%(name)s at %(asctime)s]: %(message)s",
                 add_timestamp: bool = False, exception_logger: typing.Optional[str] = None,
                 show_logo: bool = False):
    import datetime
    loglevel: int = loglevel_mapping.get(loglevel, loglevel)
    log_folder = user_path("logs")
    os.makedirs(log_folder, exist_ok=True)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    root_logger.setLevel(loglevel)
    logging.getLogger("websockets").setLevel(loglevel)  # make sure level is applied for websockets
    for logger_name in ("asyncio", "PIL"):
        logging.getLogger(logger_name).setLevel(max(loglevel, logging.INFO))
    if "a" not in write_mode:
        name += f"_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    file_handler = logging.FileHandler(
        os.path.join(log_folder, f"{name}.txt"),
        write_mode,
        encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter(log_format))

    class Filter(logging.Filter):
        def __init__(self, filter_name: str, condition: typing.Callable[[logging.LogRecord], bool]) -> None:
            super().__init__(filter_name)
            # TODO: filter_name = 'NoFile' (only to cli and eventually to gui too)
            self.condition = condition

        def filter(self, record: logging.LogRecord) -> bool:
            return self.condition(record)

    class BytesCleanupFilter(logging.Filter):
        """Remove b'...' notation from bytes objects in log messages."""
        def filter(self, record: logging.LogRecord) -> bool:
            import re
            # Match b'...' or b"..." patterns and extract the inner content
            record.msg = re.sub(r"b(['\"])(.+?)\1", r"\2", str(record.msg))
            return True
    
    class UnescapeMarkupFilter(logging.Filter):
        """Convert Kivy markup entities back to normal characters."""
        def filter(self, record: logging.LogRecord) -> bool:
            msg = str(record.msg)
            record.msg = msg.replace('&bl;', '[').replace('&br;', ']').replace('&amp;', '&')
            return True

    file_handler.addFilter(Filter("NoStream", lambda record: not getattr(record, "NoFile", False)))
    file_handler.addFilter(Filter("NoCarriageReturn", lambda record: '\r' not in record.getMessage()))
    file_handler.addFilter(BytesCleanupFilter())
    file_handler.addFilter(UnescapeMarkupFilter())
    root_logger.addHandler(file_handler)
    # TODO: Make console better, use rich/blessed/something else
    # Force UTF-8 stream wrapper for stdout/stderr (fixes UnicodeEncodeError in macOS .app bundles).
    # Only wrap once per process; see _stdio_wrapped_for_logging above.
    global _stdio_wrapped_for_logging
    if (not _stdio_wrapped_for_logging
            and hasattr(sys.stdout, "buffer") and hasattr(sys.stderr, "buffer")
            and (is_macos or is_linux) and is_frozen()):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
        _stdio_wrapped_for_logging = True
    # TODO: Fix here to use rich/blessed
    if sys.stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        # TODO: this is the output to cli!
        stream_handler.addFilter(Filter("NoFile", lambda record: not getattr(record, "NoStream", False)))
        stream_handler.addFilter(BytesCleanupFilter())
        stream_handler.addFilter(UnescapeMarkupFilter())
        if add_timestamp:
            formatter = logging.Formatter(fmt='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            stream_handler.setFormatter(formatter)
        else:
            stream_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
        root_logger.addHandler(stream_handler)
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if show_logo:
        _print_startup_logo()

    # Relay unhandled exceptions to logger.
    if not getattr(sys.excepthook, "_wrapped", False):  # skip if already modified
        orig_hook = sys.excepthook

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logging.getLogger(exception_logger).exception("Uncaught exception",
                                                          exc_info=(exc_type, exc_value, exc_traceback),
                                                          extra={"NoStream": exception_logger is None})
            return orig_hook(exc_type, exc_value, exc_traceback)

        handle_exception._wrapped = True

        sys.excepthook = handle_exception

    def _cleanup():
        for file in os.scandir(log_folder):
            if file.name.endswith(".txt"):
                last_change = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                if datetime.datetime.now() - last_change > datetime.timedelta(days=7):
                    try:
                        os.unlink(file.path)
                    except Exception as e:
                        logging.exception(e)
                    else:
                        logging.debug(f"Deleted old logfile {file.path}")
    import threading
    threading.Thread(target=_cleanup, name="LogCleaner").start()
    import platform
    logging.info(
        f"{instance_name} ({__version__}) logging initialized"
        f" on {platform.platform()} process {os.getpid()}"
        f" running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        f"{' (frozen)' if is_frozen() else ''}"
    )
    logging.info(
        "Frontends: " + ", ".join(f"{name} {ver}" for name, ver in get_frontend_versions().items())
    )

def get_archipelago_json(world: str) -> typing.Tuple[str, list[str], str, str]:
    """ Get the constants from the archipelago.json file for a given world
    
    Args:
        world: The name of the world to get the constants for

    Returns:
        A tuple of the game name, authors, minimum AP version, and world version
    """
    from mwgg_igdb import GameIndex
    import pkgutil
    data: dict = {}
    try:
        if is_frozen():
            # In frozen builds, worlds are installed as wheels in venv site-packages
            archipelago_json_path = mwgg_venv_site_packages("worlds", world, "archipelago.json")
            if not os.path.exists(archipelago_json_path):
                # Fall back to local_path for worlds bundled with the executable
                archipelago_json_path = local_path("lib", "worlds", world, "archipelago.json")
            with open(archipelago_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            # Resolve via the import system so archipelago.json comes from wherever
            # worlds.<name> actually loaded from. Matches WebHostLib/misc.py.
            manifest_bytes = None
            try:
                manifest_bytes = pkgutil.get_data("worlds." + world, "archipelago.json")
            except (ImportError, FileNotFoundError, OSError):
                manifest_bytes = None
            if manifest_bytes:
                data = json.loads(manifest_bytes.decode("utf-8-sig"))
            else:
                with open(local_path("worlds", world, "archipelago.json"), "r", encoding="utf-8") as f:
                    data = json.load(f)
    except FileNotFoundError:
        pass
    game_name = "Archipelago" if world == "generic" else data.get("game", GameIndex.get_game(world).get("game_name"))
    authors = data.get("authors", ["Unknown"])
    minimum_ap_version = data.get("minimum_ap_version", "0.5.0")
    version = data.get("world_version", "0.0.1")
    return game_name, authors, minimum_ap_version, version

def get_apworld_manifest(world: str) -> dict[str, object]:
    '''
    Get the manifest from archipelago.json for a given world that is not in a zipfile

    TODO: Swap this out for all get_archipelago_json calls. This requires full world
    rebuilds and removes the need for the "Register.py" file.
    '''
    try:
        if is_frozen():
            # In frozen builds, worlds are installed as wheels in venv site-packages
            archipelago_json_path = mwgg_venv_site_packages("worlds", world, "archipelago.json")
            if not os.path.exists(archipelago_json_path):
                # Fall back to local_path for worlds bundled with the executable
                archipelago_json_path = local_path("lib", "worlds", world, "archipelago.json")
            with open(archipelago_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            with open(local_path("worlds", world, "archipelago.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
        return data
    except FileNotFoundError:
        return {}


def _detached_popen_kwargs() -> dict[str, typing.Any]:
    """Popen kwargs that detach the child from this process. Children
    deliberately survive launcher exit: closing the launcher window must not
    kill an in-progress game session or tool."""
    if is_windows:
        return {"creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def get_client_exe() -> list[str]:
    """Resolve the command line that launches the beta's single client entry point.

    Centralizes exe-name resolution (frozen name vs source script) so callers
    never hardcode "MultiworldGG(.exe)" themselves."""
    if is_frozen():
        suffix = ".exe" if is_windows else ""
        return [local_path(f"{FROZEN_TARGETS['MultiWorld']}{suffix}")]
    return [sys.executable, local_path("MultiWorld.py")]


def launch_exe(exe: typing.Iterable[str], in_terminal: bool = False) -> bool:
    """Run the command line `exe` in a new process. With `in_terminal`, try to
    run it in a terminal window; the return value reports whether one was used.
    Beta equivalent of upstream Launcher.launch (which the monorepo lacks)."""
    exe = list(exe)
    if in_terminal:
        if is_windows:
            # intentionally using a window title with a space so it gets quoted and treated as a title
            subprocess.Popen(["start", f"Running {instance_name}", *exe], shell=True)
            return True
        elif sys.platform.startswith("linux"):
            from shutil import which
            xdg = which("xdg-terminal-exec")
            if xdg:
                subprocess.Popen([xdg, "--", *exe])
                return True
            terminal = which("x-terminal-emulator") or which("konsole") or which("gnome-terminal") or which("xterm")
            if terminal:
                import shlex
                subprocess.Popen([terminal, "-e", shlex.join(exe)])
                return True
        elif sys.platform == "darwin":
            from shutil import which
            subprocess.Popen([which("open"), "-W", "-a", "Terminal.app", *exe])
            return True
    subprocess.Popen(exe)
    return False


def spawn_client(game: typing.Optional[str] = None, *, server_address: typing.Optional[str] = None,
                 slot_name: typing.Optional[str] = None, password: typing.Optional[str] = None,
                 client_type: str = "game", component: typing.Optional[str] = None,
                 launch_file: typing.Optional[str] = None,
                 extra_args: typing.Iterable[str] = ()) -> "subprocess.Popen[typing.Any]":
    """Spawn a detached client process; children deliberately survive launcher
    exit. MWGG_NO_SPLASH=1 goes in the child env (there is no CLI flag).

    `component` names a `Component.display_name` registered by `game`'s world
    module (e.g. a map tracker); the child resolves it after its world load and
    falls back to default client resolution if the name doesn't match."""
    argv = list(get_client_exe())
    if launch_file:
        argv.append(launch_file)
    if game is not None:
        argv += ["--game", game]
    if server_address is not None:
        argv += ["--server-address", server_address]
    if slot_name is not None:
        argv += ["--slot-name", slot_name]
    if password is not None:
        argv += ["--password", password]
    argv += ["--client-type", client_type]
    if component is not None:
        if game is None:
            raise ValueError("spawn_client(component=...) requires game=")
        argv += ["--component", component]
    argv += list(extra_args)

    env = os.environ.copy()
    env["MWGG_ROLE"] = "client"
    env["MWGG_CLIENT_TYPE"] = client_type
    env["MWGG_NO_SPLASH"] = "1"

    return subprocess.Popen(argv, env=env, **_detached_popen_kwargs())

