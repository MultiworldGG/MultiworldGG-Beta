from . import StardewWorld, StardewWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Stardew Valley World Registration

This file contains the metadata and class references for the stardew_valley world.
"""

# Required metadata
WORLD_NAME = "stardew_valley"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = StardewWorld
WEB_WORLD_CLASS = StardewWebWorld
CLIENT_FUNCTION = None
