from . import ZillionWebWorld, ZillionWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .client import launch

"""
Zillion World Registration

This file contains the metadata and class references for the zillion world.
"""

# Required metadata
WORLD_NAME = "zillion"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ZillionWorld
WEB_WORLD_CLASS = ZillionWebWorld
CLIENT_FUNCTION = launch
