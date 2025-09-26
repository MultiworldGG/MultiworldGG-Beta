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

from NetUtils import DataPackage
from Utils import local_path, user_path, Version, version_tuple

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
# TODO: FIX FOR DYNAMIC LOADING
# if apworlds:
#     # encapsulation for namespace / gc purposes
#     def load_apworlds() -> None:
#         global apworlds
#         from .Files import APWorldContainer, InvalidDataError
#         core_compatible: list[tuple[WorldSource, APWorldContainer]] = []

#         def fail_world(game_name: str, reason: str, add_as_failed_to_load: bool = True) -> None:
#             if add_as_failed_to_load:
#                 failed_world_loads.append(game_name)
#             logging.warning(reason)

#         for apworld_source in apworlds:
#             apworld: APWorldContainer = APWorldContainer(apworld_source.resolved_path)
#             # populate metadata
#             try:
#                 apworld.read()
#             except InvalidDataError as e:
#                 if version_tuple >= (0, 8, 0):
#                     logging.error(
#                         f"Invalid or missing manifest file for {apworld_source.resolved_path}. "
#                         "Make sure it is added properly."
#                     )
#                     logging.error(e)


#             if apworld.minimum_ap_version and apworld.minimum_ap_version > version_tuple:
#                 fail_world(apworld.game,
#                            f"Did not load {apworld_source.path} "
#                            f"as its minimum core version {apworld.minimum_ap_version} "
#                            f"is higher than current core version {version_tuple}.")
#             elif apworld.maximum_ap_version and apworld.maximum_ap_version < version_tuple:
#                 fail_world(apworld.game,
#                            f"Did not load {apworld_source.path} "
#                            f"as its maximum core version {apworld.maximum_ap_version} "
#                            f"is lower than current core version {version_tuple}.")
#             else:
#                 core_compatible.append((apworld_source, apworld))
#         # load highest version first
#         core_compatible.sort(
#             key=lambda element: element[1].world_version if element[1].world_version else Version(0, 0, 0),
#             reverse=True)
#         for apworld_source, apworld in core_compatible:
#             if apworld.game and apworld.game in AutoWorldRegister.world_types:
#                 fail_world(apworld.game,
#                            f"Did not load {apworld_source.path} "
#                            f"as its game {apworld.game} is already loaded.",
#                            add_as_failed_to_load=False)
#             else:
#                 apworld_source.load()
#     load_apworlds()
#     del load_apworlds

# del apworlds

# Build the data package for each game.
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

network_data_package_single_game: Dict[str, DataPackage] = {
    game_name: {"games": {game_name: pkg_data}}
    for game_name, pkg_data in network_data_package["games"].items()
}