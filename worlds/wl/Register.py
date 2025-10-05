from . import WLWorld
from . import WLWeb

"""
Wario Land: Super Mario Land 3 is a 1994 platform game developed and published by Nintendo for the Game Boy. World Registration

This file contains the metadata and class references for the wl world.
"""

# Required metadata
WORLD_NAME = "wl"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WLWorld
WEB_WORLD_CLASS = WLWeb
CLIENT_FUNCTION = None
