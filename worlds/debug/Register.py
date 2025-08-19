from . import DebugWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

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
