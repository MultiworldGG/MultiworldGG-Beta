import importlib
import importlib.abc
import importlib.machinery
import logging
import os
import time
import dataclasses
from typing import Optional, Union

from NetUtils import DataPackage
from BaseUtils import Version, get_archipelago_json, tuplize_version, mwgg_venv_site_packages, use_worlds_venv
from APContainer import APWorldContainer

# Extend __path__ to include python installed worlds for namespace package behavior.
if use_worlds_venv():
    venv_worlds_path = mwgg_venv_site_packages("worlds")
    if venv_worlds_path not in __path__:
        __path__.append(venv_worlds_path)
else:
    from sysconfig import get_path
    worlds_path = os.path.join(get_path("purelib"), "worlds")
    if worlds_path not in __path__:
        __path__.append(worlds_path)

__all__ = [
    "network_data_package",
    "network_data_package_single_game",
    "AutoWorldRegister",
    "world_sources",
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

        except Exception as e:
            # A single world failing can still mean enough is working for the user, log and carry on
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