import os
import sys
import typing
import logging
import io
import warnings
import json
from pathlib import Path

__all__ = ("Version", 
           "tuplize_version", 
           "__version__", 
           "version_tuple", 
           "instance_name", 
           "archipelago_guid", 
           "is_linux", 
           "is_macos",
           "is_windows",
           "is_frozen",
           "local_path",
           "user_path",
           "output_path",
           "cache_path",
           "write_path",
           "init_logging",
           "loglevel_mapping",
           "ByValue")

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
    
    # Simple parsing fallback for backward compatibility
    try:
        parts = version.split(".")
        return Version(
            int(parts[0]) if len(parts) > 0 else 0,
            int(parts[1]) if len(parts) > 1 else 0,
            int(parts[2]) if len(parts) > 2 else 0
        )
    except (ValueError, IndexError):
        return Version(0, 0, 0)

__version__ = "0.6.5"
version_tuple = tuplize_version(__version__)

instance_name = "MultiworldGG"
archipelago_guid = "{{918BA46A-FAB8-460C-9DFF-AE691E1C865D}}"

is_linux = sys.platform.startswith("linux")
is_macos = sys.platform == "darwin"
is_windows = sys.platform in ("win32", "cygwin", "msys")

def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))

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

class ByValue:
    """
    Mixin for enums to pickle value instead of name (restores pre-3.11 behavior). Use as left-most parent.
    See https://github.com/python/cpython/pull/26658 for why this exists.
    """
    def __reduce_ex__(self, prot):
        return self.__class__, (self._value_, )

loglevel_mapping = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}

def init_logging(name: str, loglevel: typing.Union[str, int] = logging.INFO,
                 write_mode: str = "w", log_format: str = "[%(name)s at %(asctime)s]: %(message)s",
                 add_timestamp: bool = False, exception_logger: typing.Optional[str] = None):
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
    # Force UTF-8 stream wrapper for stdout/stderr (fixes UnicodeEncodeError in macOS .app bundles)
    if hasattr(sys.stdout, "buffer") and hasattr(sys.stderr, "buffer") and (is_macos or is_linux) and is_frozen():
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
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

def get_archipelago_json(world: str) -> typing.Tuple[str, list[str], str, str]:
    """ Get the constants from the archipelago.json file for a given world
    
    Args:
        world: The name of the world to get the constants for

    Returns:
        A tuple of the game name, authors, minimum AP version, and world version
    """
    try:
        if is_frozen():
            # In frozen builds, worlds are installed as wheels in venv site-packages
            archipelago_json_path = write_path("mwgg_venv", "Lib", "site-packages", "worlds", world, "archipelago.json")
            with open(archipelago_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            with open(local_path("worlds", world, "archipelago.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
    except FileNotFoundError:
        return world, ["Unknown"], "0.0.0", "0.0.0"
    return data["game"], data["authors"], data["minimum_ap_version"], data["world_version"]

