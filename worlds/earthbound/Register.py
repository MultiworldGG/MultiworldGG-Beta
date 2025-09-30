from . import EarthBoundWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import EBWeb

"""
EarthBound World Registration

This file contains the metadata and class references for the earthbound world.
"""

# Required metadata
WORLD_NAME = "earthbound"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EarthBoundWorld
WEB_WORLD_CLASS = EBWeb
CLIENT_FUNCTION = None
