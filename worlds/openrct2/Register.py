from . import OpenRCT2World, OpenRCT2WebWorld
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
OpenRCT2 World Registration

This file contains the metadata and class references for the openrct2 world.
"""

# Required metadata
WORLD_NAME = "openrct2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OpenRCT2World
WEB_WORLD_CLASS = OpenRCT2WebWorld
CLIENT_FUNCTION = launch
