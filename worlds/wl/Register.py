from . import WLWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import WLWeb

"""
Wario Land: Super Mario Land 3 is a 1994 platform game developed and published by Nintendo for the Game Boy. World Registration

This file contains the metadata and class references for the wl world.
"""

# Required metadata
WORLD_NAME = "wl"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WLWorld
WEB_WORLD_CLASS = WLWeb
CLIENT_FUNCTION = None
