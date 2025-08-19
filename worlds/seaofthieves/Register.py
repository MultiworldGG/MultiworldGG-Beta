from . import SOTWorld, SOTWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Sea of Thieves World Registration

This file contains the metadata and class references for the seaofthieves world.
"""

# Required metadata
WORLD_NAME = "seaofthieves"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SOTWorld
WEB_WORLD_CLASS = SOTWebWorld
CLIENT_FUNCTION = None
