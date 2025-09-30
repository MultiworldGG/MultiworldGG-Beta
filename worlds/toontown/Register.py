from . import ToontownWorld, ToontownWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Toontown World Registration

This file contains the metadata and class references for the toontown world.
"""

# Required metadata
WORLD_NAME = "toontown"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ToontownWorld
WEB_WORLD_CLASS = ToontownWeb
CLIENT_FUNCTION = None
