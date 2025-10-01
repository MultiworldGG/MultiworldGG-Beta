from . import CelesteOpenWebWorld, CelesteOpenWorld

"""
Celeste (Open World) World Registration

This file contains the metadata and class references for the celeste (open world) world.
"""

# Required metadata
WORLD_NAME = "celeste_open_world"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CelesteOpenWorld
WEB_WORLD_CLASS = CelesteOpenWebWorld
CLIENT_FUNCTION = None