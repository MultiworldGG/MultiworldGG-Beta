from . import SMWWorld
from . import SMWWeb

"""
Super Mario World is an action platforming game. World Registration

This file contains the metadata and class references for the smw world.
"""

# Required metadata
WORLD_NAME = "smw"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMWWorld
WEB_WORLD_CLASS = SMWWeb
CLIENT_FUNCTION = None
