from . import SM64World
from . import SM64Web

"""
The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons, World Registration

This file contains the metadata and class references for the sm64ex world.
"""

# Required metadata
WORLD_NAME = "sm64ex"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SM64World
WEB_WORLD_CLASS = SM64Web
CLIENT_FUNCTION = None
