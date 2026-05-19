import importlib
import importlib.abc
import importlib.machinery
import logging
import os
import time
import dataclasses
from typing import Optional, Union

from NetUtils import DataPackage
from BaseUtils import (local_path, user_path, Version, version_tuple, tuplize_version,
                       get_archipelago_json, mwgg_venv_site_packages, use_worlds_venv)
from APContainer import APWorldContainer
from pathlib import Path

# Some imports are "unnecessary", but they may be imported by random world modules.

# Extend __path__ to include python installed worlds for namespace package behavior.
local_folder = Path(__file__).parent
user_folder = None

if use_worlds_venv():
    user_folder = mwgg_venv_site_packages("worlds")
    if user_folder not in __path__:
        __path__.append(user_folder)
else:
    from sysconfig import get_path
    user_folder = os.path.join(get_path("purelib"), "worlds")
    if user_folder not in __path__:
        __path__.append(user_folder)

__all__ = [
    "network_data_package",
    "network_data_package_single_game",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "failed_world_loads",
]

failed_world_loads: list[str] = []

@dataclasses.dataclass(order=True)
class WorldSource:
    game_module: Union[str, APWorldContainer]
    time_taken: float = -1.0
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.game_module})"

    def load(self) -> bool:
        try:
            start = time.perf_counter()
            if isinstance(self.game_module, str):
                # Load the world class from the entry point
                self.game = self.game_module
                world_class = importlib.import_module(self.game_module)
                
            else: # APWorldContainer
                self.game = self.game_module.game
                world_class = self.game_module.sys_modules_import_apworld()
            self.time_taken = time.perf_counter()-start
            return True

        except BaseException as e:
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                raise
            # A single world failing can still mean enough is working for the user, log and carry on.
            # Catches BaseException so C-extension panics (e.g. pyo3_runtime.PanicException) don't
            # bring the whole process down.
            logging.warning(f"Could not load world {self}: {type(e).__name__}: {e}")
            logging.debug("Full traceback for %s:", self, exc_info=True)
            if isinstance(self.game_module, str):
                failed_world_loads.append(self.game)
            elif isinstance(self.game_module, APWorldContainer):
                failed_world_loads.append(self.game_module.game)
            else:
                failed_world_loads.append(self.game_module) # this may be a mix list of modules/game names
            return False

from Utils import game_names

world_sources: list[WorldSource] = []
for game_module in game_names():
    world_sources.append(WorldSource(game_module))

for world_source in world_sources:
    world_source.load()


def load_missing_worlds() -> None:
    """Load worlds added to game_names() after this module's first import."""
    loaded_ids = {id(ws.game_module) for ws in world_sources}
    for game_module in game_names():
        if id(game_module) in loaded_ids:
            continue
        ws = WorldSource(game_module)
        world_sources.append(ws)
        ws.load()

from .AutoWorld import AutoWorldRegister
# Add version for each world.
for world in AutoWorldRegister.world_types.values():
    if world.game not in ["Archipelago"]:
        world_name, author, minimum_ap_version, version = get_archipelago_json(world.__module__.split(".")[1])
        AutoWorldRegister.world_types[world.game].world_version = tuplize_version(version)

# Build the data package for each game.
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

network_data_package_single_game: dict[str, DataPackage] = {
    game_name: {"games": {game_name: pkg_data}}
    for game_name, pkg_data in network_data_package["games"].items()
}