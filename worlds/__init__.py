import importlib
import logging
import os
import time
import dataclasses
from typing import Dict, List

from NetUtils import DataPackage
from Utils import local_path, user_path, Version, version_tuple, tuplize_version

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:  # can't access/write?
    user_folder = None

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