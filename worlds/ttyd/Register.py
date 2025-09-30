from . import TTYDWorld, TTYDWebWorld
from .TTYDClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
