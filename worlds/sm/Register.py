from . import SMWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SMWeb

"""
Super Metroid World Registration

This file contains the metadata and class references for the sm world.
"""

# Required metadata
WORLD_NAME = "sm"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMWorld
WEB_WORLD_CLASS = SMWeb
CLIENT_FUNCTION = None
