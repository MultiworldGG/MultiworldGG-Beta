from . import SM64HackWorld, SM64HackWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
