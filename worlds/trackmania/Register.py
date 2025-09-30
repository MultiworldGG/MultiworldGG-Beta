from . import TrackmaniaWorld, TrackmaniaWeb, launch_client
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Trackmania World Registration

This file contains the metadata and class references for the trackmania world.
"""

# Required metadata
WORLD_NAME = "trackmania"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TrackmaniaWorld
WEB_WORLD_CLASS = TrackmaniaWeb
CLIENT_FUNCTION = launch_client
