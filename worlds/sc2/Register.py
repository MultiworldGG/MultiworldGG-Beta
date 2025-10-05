from . import Starcraft2World, Starcraft2WebWorld
from .Client import launch

"""
Starcraft 2 World Registration

This file contains the metadata and class references for the sc2 world.
"""

# Required metadata
WORLD_NAME = "sc2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Starcraft2World
WEB_WORLD_CLASS = Starcraft2WebWorld
CLIENT_FUNCTION = launch
