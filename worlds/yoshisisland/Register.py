from . import YoshisIslandWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import YoshisIslandWeb

"""
Yoshi World Registration

This file contains the metadata and class references for the yoshisisland world.
"""

# Required metadata
WORLD_NAME = "yoshisisland"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = YoshisIslandWorld
WEB_WORLD_CLASS = YoshisIslandWeb
CLIENT_FUNCTION = None
