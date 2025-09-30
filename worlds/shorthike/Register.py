from . import ShortHikeWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ShortHikeWeb

"""
A Short Hike World Registration

This file contains the metadata and class references for the shorthike world.
"""

# Required metadata
WORLD_NAME = "shorthike"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ShortHikeWorld
WEB_WORLD_CLASS = ShortHikeWeb
CLIENT_FUNCTION = None
