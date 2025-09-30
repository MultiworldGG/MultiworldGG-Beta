from . import MuseDashWorld, MuseDashWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Muse Dash World Registration

This file contains the metadata and class references for the musedash world.
"""

# Required metadata
WORLD_NAME = "musedash"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MuseDashWorld
WEB_WORLD_CLASS = MuseDashWebWorld
CLIENT_FUNCTION = None
