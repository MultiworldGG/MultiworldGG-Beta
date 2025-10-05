from . import SM64HackWorld, SM64HackWebWorld

"""
SM64 Romhack World Registration

This file contains the metadata and class references for the sm64hacks world.
"""

# Required metadata
WORLD_NAME = "sm64hacks"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SM64HackWorld
WEB_WORLD_CLASS = SM64HackWebWorld
CLIENT_FUNCTION = None
