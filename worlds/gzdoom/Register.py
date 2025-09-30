from . import GZDoomWorld, GZDoomWeb
from .client.GZDoomClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
gzDoom World Registration

This file contains the metadata and class references for the gzdoom world.
"""

# Required metadata
WORLD_NAME = "gzdoom"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GZDoomWorld
WEB_WORLD_CLASS = GZDoomWeb
CLIENT_FUNCTION = launch
