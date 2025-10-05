from . import TrackerWorld, launch_client

"""
Universal Tracker World Registration

This file contains the metadata and class references for the tracker world.
"""

# Required metadata
WORLD_NAME = "tracker"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TrackerWorld
CLIENT_FUNCTION = launch_client
