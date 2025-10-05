from . import TrackmaniaWorld, TrackmaniaWeb, launch_client

"""
Trackmania World Registration

This file contains the metadata and class references for the trackmania world.
"""

# Required metadata
WORLD_NAME = "trackmania"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TrackmaniaWorld
WEB_WORLD_CLASS = TrackmaniaWeb
CLIENT_FUNCTION = launch_client
