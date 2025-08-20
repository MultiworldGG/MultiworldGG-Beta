from . import MMBN3World, MMBN3Web
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
MegaMan Battle Network 3 World Registration

This file contains the metadata and class references for the mmbn3 world.
"""

# Required metadata
WORLD_NAME = "mmbn3"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MMBN3World
WEB_WORLD_CLASS = MMBN3Web
CLIENT_FUNCTION = launch
