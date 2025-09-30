from . import SOTWorld, SOTWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Sea of Thieves World Registration

This file contains the metadata and class references for the seaofthieves world.
"""

# Required metadata
WORLD_NAME = "seaofthieves"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SOTWorld
WEB_WORLD_CLASS = SOTWebWorld
CLIENT_FUNCTION = None
