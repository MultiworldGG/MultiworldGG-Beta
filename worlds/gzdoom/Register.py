from . import GZDoomWorld, GZDoomWeb
from .client.GZDoomClient import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
gzDoom World Registration

This file contains the metadata and class references for the gzdoom world.
"""

# Required metadata
WORLD_NAME = "gzdoom"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GZDoomWorld
WEB_WORLD_CLASS = GZDoomWeb
CLIENT_FUNCTION = launch
