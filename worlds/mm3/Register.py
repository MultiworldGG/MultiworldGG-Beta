from . import MM3WebWorld, MM3World
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Mega Man 3 World Registration

This file contains the metadata and class references for the mm3 world.
"""

# Required metadata
WORLD_NAME = "mm3"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MM3World
WEB_WORLD_CLASS = MM3WebWorld
CLIENT_FUNCTION = None
