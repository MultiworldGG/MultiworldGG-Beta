from . import DOOM1993World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DOOM1993Web

"""
DOOM 1993 World Registration

This file contains the metadata and class references for the doom_1993 world.
"""

# Required metadata
WORLD_NAME = "doom_1993"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DOOM1993World
WEB_WORLD_CLASS = DOOM1993Web
CLIENT_FUNCTION = None
