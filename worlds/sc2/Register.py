from . import Starcraft2World, Starcraft2WebWorld
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Starcraft 2 World Registration

This file contains the metadata and class references for the sc2 world.
"""

# Required metadata
WORLD_NAME = "sc2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Starcraft2World
WEB_WORLD_CLASS = Starcraft2WebWorld
CLIENT_FUNCTION = launch
