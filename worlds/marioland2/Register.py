from . import MarioLand2World, MarioLand2WebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Super Mario Land 2 World Registration

This file contains the metadata and class references for the marioland2 world.
"""

# Required metadata
WORLD_NAME = "marioland2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MarioLand2World
WEB_WORLD_CLASS = MarioLand2WebWorld
CLIENT_FUNCTION = None
