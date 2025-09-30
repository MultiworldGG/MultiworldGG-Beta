from . import DebugWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
debug World Registration

This file contains the metadata and class references for the debug world.
"""

# Required metadata
WORLD_NAME = "debug"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DebugWorld
WEB_WORLD_CLASS = None
CLIENT_FUNCTION = None
