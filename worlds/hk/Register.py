from . import HKWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import HKWeb

"""
Hollow Knight World Registration

This file contains the metadata and class references for the hk world.
"""

# Required metadata
WORLD_NAME = "hk"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HKWorld
WEB_WORLD_CLASS = HKWeb
CLIENT_FUNCTION = None
