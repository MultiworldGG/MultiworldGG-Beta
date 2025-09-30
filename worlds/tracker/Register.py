from . import TrackerWorld, launch_client
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Universal Tracker World Registration

This file contains the metadata and class references for the tracker world.
"""

# Required metadata
WORLD_NAME = "tracker"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TrackerWorld
CLIENT_FUNCTION = launch_client
