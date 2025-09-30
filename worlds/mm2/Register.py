from . import MM2World, MM2WebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Mega Man 2 World Registration

This file contains the metadata and class references for the mm2 world.
"""

# Required metadata
WORLD_NAME = "mm2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MM2World
WEB_WORLD_CLASS = MM2WebWorld
CLIENT_FUNCTION = None
