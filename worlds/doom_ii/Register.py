from . import DOOM2World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DOOM2Web

"""
DOOM II World Registration

This file contains the metadata and class references for the doom_ii world.
"""

# Required metadata
WORLD_NAME = "doom_ii"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DOOM2World
WEB_WORLD_CLASS = DOOM2Web
CLIENT_FUNCTION = None
