from __future__ import annotations

import os
import sys
import zipfile
import json
from typing import Tuple, Optional, TypedDict, List

from Utils import set_game_names

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

    games = List[str]

    for file in sys.argv[1:]:
        try:
            with zipfile.ZipFile(file, "r") as zipf:
                ap_json = zipf.open("archipelago.json").read()
                games.append(json.loads(ap_json)["game"])
        except FileNotFoundError:
            raise FileNotFoundError(f"archipelago.json not found in {file}")
        except Exception as e:
            raise Exception(f"Error reading archipelago.json in {file}: {e}")
    
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
        meta_data, result_file = create_rom_file(file)
        print(f"Patch with meta-data {meta_data} was written to {result_file}")
