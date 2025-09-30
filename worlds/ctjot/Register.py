from . import CTJoTWorld, CTJoTWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Chrono Trigger Jets of Time World Registration

This file contains the metadata and class references for the ctjot world.
"""

# Required metadata
WORLD_NAME = "ctjot"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CTJoTWorld
WEB_WORLD_CLASS = CTJoTWebWorld
CLIENT_FUNCTION = None
