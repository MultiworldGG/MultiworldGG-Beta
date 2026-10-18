from __future__ import annotations

import asyncio
import os
import sys
import zipfile
import json
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Tuple, Optional, TypedDict, List
from pathlib import Path
import logging

logger = logging.getLogger("Patch")

from Utils import set_game_names, use_worlds_venv, mwgg_venv_site_packages

if use_worlds_venv():
    venv_site_packages_path = mwgg_venv_site_packages()
    if venv_site_packages_path not in sys.path:
        sys.path.append(venv_site_packages_path)
    venv_worlds_path = mwgg_venv_site_packages("worlds")
    if os.path.exists(venv_worlds_path) and venv_worlds_path not in sys.path:
        sys.path.append(venv_worlds_path)

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

    games: List[str] = [""]

    for arg in sys.argv[1:]:
        if arg.startswith("--") or Path(arg).suffix == "":
            continue
        try:
            with zipfile.ZipFile(arg, "r") as zipf:
                ap_data = zipf.read("archipelago.json")
                ap_json = json.loads(ap_data.decode('utf-8'))
                games.append(ap_json["game"])
        except zipfile.BadZipFile:
            continue
        except Exception as e:
            logger.error(f"Error reading archipelago.json in {arg}: {e}")
            continue

    games = [game for game in games if game]

    # Set games to load into worlds for autoregister.
    set_game_names(games)

from worlds.Files import AutoPatchRegister, APAutoPatchInterface, APProcedurePatch

class RomMeta(TypedDict):
    server: str
    player: Optional[int]
    player_name: str


def _run_off_loop[T](func: Callable[..., T], *args: Any) -> T:
    """Run a blocking call on a worker thread while a running asyncio loop keeps
    driving the frontend; a plain call when no loop is running."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return func(*args)
    # A Tk dialog opened inside patch() runs on the worker; macOS only allows Tk on the main
    # thread, so an `is_macos` inline-call guard would go here if a world needs one.
    import nest_asyncio
    nest_asyncio.apply(loop)
    with ThreadPoolExecutor(max_workers=1) as pool:
        return loop.run_until_complete(asyncio.wrap_future(pool.submit(func, *args), loop=loop))


def create_rom_file(patch_file: str) -> Tuple[RomMeta, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APAutoPatchInterface = auto_handler(patch_file)
        target = os.path.splitext(patch_file)[0]+handler.result_file_ending
        if isinstance(handler, APProcedurePatch):
            # The base ROM lookup can open a file prompt, so it stays on the calling thread.
            handler.get_source_data_with_cache()
        _run_off_loop(handler.patch, target)
        return {"server": handler.server,
                "player": handler.player,
                "player_name": handler.player_name}, target
    raise NotImplementedError(f"No Handler for {patch_file} found.")


if __name__ == "__main__":
    for file in sys.argv[1:]:
        if file.startswith('--') or Path(file).suffix == "":
            continue
        meta_data, result_file = create_rom_file(file)
        print(f"Patch with meta-data {meta_data} was written to {result_file}")
