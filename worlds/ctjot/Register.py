from . import CTJoTWorld, CTJoTWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

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
