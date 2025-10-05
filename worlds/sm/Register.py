from . import SMWorld
from . import SMWeb

"""
Super Metroid World Registration

This file contains the metadata and class references for the sm world.
"""

# Required metadata
WORLD_NAME = "sm"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMWorld
WEB_WORLD_CLASS = SMWeb
CLIENT_FUNCTION = None
