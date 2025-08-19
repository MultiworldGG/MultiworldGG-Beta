from . import SM64HackWorld, SM64HackWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
SM64 Romhack World Registration

This file contains the metadata and class references for the sm64hacks world.
"""

# Required metadata
WORLD_NAME = "sm64hacks"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SM64HackWorld
WEB_WORLD_CLASS = SM64HackWebWorld
CLIENT_FUNCTION = None
