import importlib
import logging
import os
import time
import dataclasses
from typing import Dict, List

from NetUtils import DataPackage
from BaseUtils import Version, write_path, is_frozen

# Extend __path__ to include venv site-packages for namespace package behavior
if is_frozen():
    venv_worlds_path = write_path("mwgg_venv", "Lib", "site-packages", "worlds")
    if os.path.exists(venv_worlds_path) and venv_worlds_path not in __path__:
        __path__.append(venv_worlds_path)

__all__ = {
    "network_data_package",
    "network_data_package_single_game",
    "AutoWorldRegister",
    "world_sources",
    "failed_world_loads",
}

failed_world_loads: List[str] = []

@dataclasses.dataclass(order=True)
class WorldSource:
    game_module: str
    time_taken: float = -1.0
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.game_module})"

    def load(self) -> bool:
        try:
            start = time.perf_counter()
            # Load the world class from the entry point
            world_class = importlib.import_module(self.game_module)
            self.time_taken = time.perf_counter()-start
            return True

        except Exception:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {self}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(self.game_module).rsplit(".", 1)[0])
            return False

from Utils import game_names

world_sources: List[WorldSource] = []
for game in game_names():
    world_sources.append(WorldSource(game))

world_sources.sort()
for world_source in world_sources:
    world_source.load()

from .AutoWorld import AutoWorldRegister

# Build the data package for each game.
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

network_data_package_single_game: Dict[str, DataPackage] = {
    game_name: {"games": {game_name: pkg_data}}
    for game_name, pkg_data in network_data_package["games"].items()
}