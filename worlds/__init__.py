import importlib
import importlib.metadata
import importlib.util
import logging
import os
import sys
import warnings
import zipimport
import time
import dataclasses
from typing import Dict, List, TypedDict

# from Utils import local_path, user_path

# local_folder = os.path.dirname(__file__)
# user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
# try:
#     os.makedirs(user_folder, exist_ok=True)
# except OSError:  # can't access/write?
#     user_folder = None

__all__ = {
    "network_data_package",
    "network_data_package_single_game",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "GamesPackage",
    "DataPackage",
    "failed_world_loads",
}

failed_world_loads: List[str] = []

class GamesPackage(TypedDict, total=False):
    item_name_groups: Dict[str, List[str]]
    item_name_to_id: Dict[str, int]
    location_name_groups: Dict[str, List[str]]
    location_name_to_id: Dict[str, int]
    checksum: str

class DataPackage(TypedDict):
    games: Dict[str, GamesPackage]

@dataclasses.dataclass(order=True)
class WorldSource:
    game_module: str
    time_taken: float = -1.0

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

# Build the data package for each game.
from .AutoWorld import AutoWorldRegister
    
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

network_data_package_single_game: Dict[str, DataPackage] = {
    game_name: {"games": {game_name: pkg_data}}
    for game_name, pkg_data in network_data_package["games"].items()
}