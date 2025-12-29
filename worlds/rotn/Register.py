from . import RotNWorld, RotNWeb

"""
Rogue Legacy 2 World Registration

This file contains the metadata and class references for the rotn world.
"""

# Required metadata
WORLD_NAME = "rotn"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RotNWorld
WEB_WORLD_CLASS = RotNWeb
CLIENT_FUNCTION = None
