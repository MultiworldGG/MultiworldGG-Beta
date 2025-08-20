from . import OpenRCT2World, OpenRCT2WebWorld
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
OpenRCT2 World Registration

This file contains the metadata and class references for the openrct2 world.
"""

# Required metadata
WORLD_NAME = "openrct2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OpenRCT2World
WEB_WORLD_CLASS = OpenRCT2WebWorld
CLIENT_FUNCTION = launch
