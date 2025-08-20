from . import TTYDWorld, TTYDWebWorld
from .TTYDClient import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Paper Mario The Thousand Year Door World Registration

This file contains the metadata and class references for the ttyd world.
"""

# Required metadata
WORLD_NAME = "ttyd"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TTYDWorld
WEB_WORLD_CLASS = TTYDWebWorld
CLIENT_FUNCTION = launch
