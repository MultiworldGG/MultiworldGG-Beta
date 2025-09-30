from . import FactorioWorld, FactorioWeb
from .Client import launch

"""
Factorio Saws World Registration

This file contains the metadata and class references for the factorio_saws world.
"""

# Required metadata
WORLD_NAME = "factorio_saws"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FactorioWorld
WEB_WORLD_CLASS = FactorioWeb
CLIENT_FUNCTION = launch
