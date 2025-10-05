from . import L2ACWorld
from . import L2ACWeb

"""
The Ancient Cave is a roguelike dungeon crawling game built into World Registration

This file contains the metadata and class references for the lufia2ac world.
"""

# Required metadata
WORLD_NAME = "lufia2ac"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = L2ACWorld
WEB_WORLD_CLASS = L2ACWeb
CLIENT_FUNCTION = None
