from . import SMWWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SMWWeb

"""
Super Mario World is an action platforming game. World Registration

This file contains the metadata and class references for the smw world.
"""

# Required metadata
WORLD_NAME = "smw"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMWWorld
WEB_WORLD_CLASS = SMWWeb
CLIENT_FUNCTION = None
