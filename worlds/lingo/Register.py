from . import LingoWorld, LingoWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Lingo World Registration

This file contains the metadata and class references for the lingo world.
"""

# Required metadata
WORLD_NAME = "lingo"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LingoWorld
WEB_WORLD_CLASS = LingoWebWorld
CLIENT_FUNCTION = None
