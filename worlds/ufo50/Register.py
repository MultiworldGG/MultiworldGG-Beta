from . import UFO50World, UFO50Web
from .constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Client import launch

"""
UFO 50 World Registration

This file contains the metadata and class references for the ufo50 world.
"""

# Required metadata
WORLD_NAME = "ufo50"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = UFO50World
WEB_WORLD_CLASS = UFO50Web
CLIENT_FUNCTION = launch
