from . import DSRWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DSRWeb

"""
Dark Souls is a game where you die. World Registration

This file contains the metadata and class references for the dsr world.
"""

# Required metadata
WORLD_NAME = "dsr"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DSRWorld
WEB_WORLD_CLASS = DSRWeb
CLIENT_FUNCTION = None
