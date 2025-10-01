from . import FrogmonsterWorld, FrogmonsterWeb

"""
Frogmonster World Registration

This file contains the metadata and class references for the frogmonster world.
"""

# Required metadata
WORLD_NAME = "frogmonster"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FrogmonsterWorld
WEB_WORLD_CLASS = FrogmonsterWeb
CLIENT_FUNCTION = None
