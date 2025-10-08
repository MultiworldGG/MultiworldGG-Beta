from __future__ import annotations

import os
import sys
import zipfile
import json
from typing import Tuple, Optional, TypedDict, List
from pathlib import Path
import logging

logger = logging.getLogger("Patch")

from Utils import set_game_names

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

from worlds.Files import AutoPatchRegister, APAutoPatchInterface

class RomMeta(TypedDict):
    server: str
    player: Optional[int]
    player_name: str


def create_rom_file(patch_file: str) -> Tuple[RomMeta, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APAutoPatchInterface = auto_handler(patch_file)
        target = os.path.splitext(patch_file)[0]+handler.result_file_ending
        handler.patch(target)
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
