from . import UltrakillWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import UltrakillWeb

"""
ULTRAKILL World Registration

This file contains the metadata and class references for the ultrakill world.
"""

# Required metadata
WORLD_NAME = "ultrakill"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = UltrakillWorld
WEB_WORLD_CLASS = UltrakillWeb
CLIENT_FUNCTION = None
