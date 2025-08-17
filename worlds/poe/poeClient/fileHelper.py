import asyncio
import hashlib
import logging
import re
import pickle
import asyncio
import importlib.util
import sys
import types
from collections import deque
from pathlib import Path
import winreg

import typing
if typing.TYPE_CHECKING:
    from worlds.poe.Client import PathOfExileContext


_debug = True
lock = asyncio.Lock()  # Lock to ensure thread-safe access to settings file
settings_file_path = Path("poe_settings")
client_txt_last_modified_time = None
callbacks_on_file_change: list[callable] = []
logger = logging.getLogger("poeClient")

def _ensure_stdlib_shims():
    """Provide minimal shims for stdlib modules missing in the frozen runtime."""
    if 'doctest' not in sys.modules:
        shim = types.ModuleType('doctest')
        # minimal API; pyrect only imports doctest, doesn't use at import time
        def testmod(*args, **kwargs):
            return None
        shim.testmod = testmod
        sys.modules['doctest'] = shim

def load_vendor_modules():
    import os
    import sys
    import importlib.util
    import zipfile
    import tempfile
    import atexit
    import shutil

    # Prevent double-load
    if getattr(sys, "_vendor_modules_loaded", False):
        return
    sys._vendor_modules_loaded = True

    # Use consistent temp directory for vendor extraction
    temp_dir = os.path.join(tempfile.gettempdir(), "archipelago_vendor")

    # Default vendor path (source mode)
    base_dir = os.path.dirname(__file__)
    base_vendor_dir = os.path.join(base_dir, "vendor")

    if not os.path.isdir(base_vendor_dir):
        # Try to detect if running from zip
        archive_path = os.path.abspath(__file__)
        while not os.path.isfile(archive_path) and archive_path != os.path.dirname(archive_path):
            archive_path = os.path.dirname(archive_path)

        if zipfile.is_zipfile(archive_path):
            logger.info(f"[vendor] Extracting vendor from zip: {archive_path}")

            # Clean up the temp dir first
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            os.makedirs(temp_dir, exist_ok=True)

            with zipfile.ZipFile(archive_path, 'r') as z:
                for name in z.namelist():
                    if name.startswith("poe/poeClient/vendor/") and not name.endswith("/"):
                        z.extract(name, temp_dir)

            base_vendor_dir = os.path.join(temp_dir, "poe", "poeClient", "vendor")

            # Clean up after exit
            atexit.register(lambda: shutil.rmtree(temp_dir, ignore_errors=True))

        if not os.path.isdir(base_vendor_dir):
            raise FileNotFoundError(f"Vendor directory could not be found or extracted: {base_vendor_dir}")

    _ensure_stdlib_shims()  # ensure shims before importing vendor modules

    for entry in os.listdir(base_vendor_dir):
        entry_path = os.path.join(base_vendor_dir, entry)

        if entry in sys.modules:
            continue

        # Single-file module
        if os.path.isfile(entry_path) and entry_path.endswith(".py"):
            modname = os.path.splitext(entry)[0]
            if modname in sys.modules:
                continue
            spec = importlib.util.spec_from_file_location(modname, entry_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            sys.modules[modname] = mod
            logger.info(f"[vendor] Loaded single-file module '{modname}' from {entry_path}")

        # Single-layer or double-layer package
        elif os.path.isdir(entry_path):
            single_layer = os.path.join(entry_path, "__init__.py")
            double_layer = os.path.join(entry_path, entry, "__init__.py")

            if os.path.isfile(double_layer):
                if entry_path not in sys.path:
                    sys.path.insert(0, entry_path)
                spec = importlib.util.spec_from_file_location(entry, double_layer)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[entry] = mod
                logger.info(f"[vendor] Loaded double-layer package '{entry}' from {double_layer}")

            elif os.path.isfile(single_layer):
                if base_vendor_dir not in sys.path:
                    sys.path.insert(0, base_vendor_dir)
                spec = importlib.util.spec_from_file_location(entry, single_layer)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[entry] = mod
                logger.info(f"[vendor] Loaded single-layer package '{entry}' from {single_layer}")


def safe_filename(filename: str) -> str:
    # Replace problematic characters with underscores
    return re.sub(r"[^\w\-_\. ]", "", filename)

async def callback_on_file_change(filepath: Path, async_callbacks: list[callable]):
    """Monitor file for changes and call callbacks. Can be cancelled."""
    async def zone_change_callback(line: str):
        for callback in async_callbacks:
            if callable(callback):
                try:
                    await callback(line)
                except asyncio.CancelledError:
                    logger.info("Callback cancelled during execution")
                    raise
                except Exception as e:
                    logger.error(f"Error in callback: {e}")
                    raise
    
    try:
        await callback_on_file_line_change(filepath, zone_change_callback)
    except asyncio.CancelledError:
        logger.info(f"File monitoring cancelled for {filepath}")
        raise


async def callback_on_file_line_change(filepath: Path, async_callback: callable):
    """Monitor file line changes. Cancelable version."""
    logger.info(f"Starting file monitoring for {filepath}")
    
    try:
        if not filepath.exists():
            logger.warning(f"File does not exist: {filepath}")
            return
            
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, 2)  # Move to end of file
            
            while True:
                if asyncio.current_task().cancelled():
                    logger.info("File monitoring task cancelled")
                    break
                
                try:
                    line = f.readline()
                    if not line:
                        await asyncio.sleep(0.3)
                        continue

                    line = line.strip()
                    await async_callback(line)
                        
                except asyncio.CancelledError:
                    logger.info("File monitoring cancelled during callback")
                    raise
                except Exception as e:
                    logger.error(f"Error reading file {filepath}: {e}")
                    raise
                    
    except asyncio.CancelledError:
        logger.info(f"File monitoring for {filepath} was cancelled")
        raise
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except PermissionError:
        logger.error(f"Permission denied reading file: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error monitoring {filepath}: {e}")
        raise
    finally:
        logger.info(f"File monitoring stopped for {filepath}")

def get_last_n_lines_of_file(filepath, n=1):
    with open(filepath, 'r') as f:
        return list(deque(f, n))


def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8]



def build_world_key(ctx: "PathOfExileContext") -> str:
    """
    Build a unique key for the world based on the context.
    This key is used to store and retrieve settings for the specific world.
    """
    world_prefix = ctx.slot_data.get('poe-uuid', '')
    return f"world {str((ctx.seed_name if ctx.seed_name is not None else '') + world_prefix + ctx.username)}"

async def save_settings(ctx: "PathOfExileContext", path: Path = settings_file_path):
    # Read existing settings first
    async with lock:
        existing_settings = await read_dict_from_pickle_file(path)
    
        # Create new world entry
        world_key = build_world_key(ctx)
        default_key = "world default"
        new_world_data = {
            "tts_speed": str(ctx.client_options["ttsSpeed"]),
            "tts_enabled": str(ctx.client_options["ttsEnabled"]),
            "client_txt": str(ctx.client_text_path),
            "last_char": str(ctx.character_name),
            "base_item_filter": str(ctx.base_item_filter),
        }
        
        # Add/update the world entry in existing settings
        existing_settings[world_key] = new_world_data
        existing_settings[default_key] = new_world_data
        
        # Write back the merged settings
        await write_dict_to_pickle_file(existing_settings, path)
    
    if _debug:
        logger.info(f"[DEBUG] Saved settings for {world_key}. Total worlds: {len(existing_settings)}")

async def load_settings(ctx: "PathOfExileContext", path: Path = settings_file_path,) -> dict:

    if not path.exists():
        if _debug:
            logger.info(f"[DEBUG] Settings file {path} does not exist. Returning empty settings.")
        return {}
    try:
        async with lock:
            all_settings = await read_dict_from_pickle_file(path)
        # Get settings for the specific world
        world_key = build_world_key(ctx)
        default_key = "world default"
        world_settings = all_settings.get(world_key, {})
        default_settings = all_settings.get(default_key, {})
        if _debug:
            logger.info(f"[DEBUG] Loaded settings from {path}.")
            if world_settings:
                logger.info(f"[DEBUG] Found settings for {world_key}")
            else:
                logger.info(f"[DEBUG] No settings found for {world_key}")

        loaded_data = {
            "tts_speed": world_settings.get("tts_speed", default_settings.get("ttsSpeed")),
            "tts_enabled": world_settings.get("tts_enabled", default_settings.get("ttsEnabled")),
            "client_txt": world_settings.get("client_txt", default_settings.get("clientTextPath", find_possible_client_txt_path())),
            "last_char": world_settings.get("last_char", default_settings.get("lastChar")),
            "base_item_filter": world_settings.get("base_item_filter", default_settings.get("baseItemFilter")),
        }

        return loaded_data
        
    except Exception as e:
        logger.info(f"[ERROR] Failed to load settings from {path}: {e}")
        return {}

async def write_dict_to_pickle_file(data: dict, file_path: Path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    if _debug:
        logger.info(f"[DEBUG] Dictionary with {len(data)} items written to {file_path}")

async def read_dict_from_pickle_file(file_path: Path) -> dict:
    data = {}
    if not file_path.exists():
        logger.info(f"File {file_path} does not exist.")
        return data

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        if _debug:
            logger.info(f"[DEBUG] Dictionary with {len(data)} items read from {file_path}")
    except (pickle.PickleError, EOFError, FileNotFoundError) as e:
        logger.info(f"[ERROR] Failed to read pickle file {file_path}: {e}")
        data = {}
    
    return data

def get_poe_install_location_from_registry() -> str | None:
    """Retrieve the Path of Exile install location from the Windows registry."""
    try:
        registry_key = r"Software\GrindingGearGames\Path of Exile"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
            install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
            return install_location
    except FileNotFoundError:
        print("Registry key not found.")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None

def find_possible_client_txt_path() -> Path | None:
    """Return the first valid path for the client.txt file."""
    if get_poe_install_location_from_registry():
        log_path = Path(get_poe_install_location_from_registry()) / "logs" / "client.txt"
        if log_path.exists():
            print(f"Found client.txt (via registry) at: {log_path}")
            logger.debug(f"Found client.txt (via registry) at: {log_path}")
            return log_path
    intermediate_paths = [
        Path(""),
        Path("games"),
        Path("Program Files (x86)"),
        Path("Program Files"),
        Path("Program Files (x86)/Steam"),
        Path("Program Files/Steam"),
        Path("Steam"),
        Path("SteamLibrary"),
        Path("games/SteamLibrary"),
        Path("steamlibraryd"),
    ]
    possible_paths = [
        Path("steamapps/common/Path of Exile"),
        Path("Path of Exile"),
        Path("poe"),
    ]
    suffix_path = Path("logs") /"client.txt"
    # Windows specific, I know....
    for drive in ["D", "C", "E", "F", "G"]:
        drive_path = Path(f"{drive}:/")
        for intermediate in intermediate_paths:
            for possible in possible_paths:
                to_check = drive_path / intermediate / possible / suffix_path
                print(f"Checking path: {to_check}")
                if to_check.exists():
                    print(f"Found client.txt at: {to_check}")
                    logger.debug(f"Found client.txt at: {to_check}")
                    return to_check

    return None


if __name__ == "__main__":
    # For testing purposes, find the client.txt path

    print("Finding client.txt path...")
    client_txt_path = find_possible_client_txt_path()

    print("log check")
    if client_txt_path:
        print(f"Found client.txt at: {client_txt_path}")
    else:
        print("Could not find client.txt in any of the expected locations.")