from . import DSTWorld, DSTWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Don World Registration

This file contains the metadata and class references for the dontstarvetogether world.
"""

# Required metadata
WORLD_NAME = "dontstarvetogether"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DSTWorld
WEB_WORLD_CLASS = DSTWeb
CLIENT_FUNCTION = launch
