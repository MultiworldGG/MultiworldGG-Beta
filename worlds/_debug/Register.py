from . import DebugWorld

"""
debug World Registration

This file contains the metadata and class references for the debug world.
"""

# Required metadata
WORLD_NAME = "debug"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DebugWorld
WEB_WORLD_CLASS = None
CLIENT_FUNCTION = None
