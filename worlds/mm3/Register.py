from . import MM3WebWorld, MM3World

"""
Mega Man 3 World Registration

This file contains the metadata and class references for the mm3 world.
"""

# Required metadata
WORLD_NAME = "mm3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MM3World
WEB_WORLD_CLASS = MM3WebWorld
CLIENT_FUNCTION = None
