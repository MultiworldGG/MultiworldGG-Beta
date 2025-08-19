from . import MMRWorld, MMRWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Majora World Registration

This file contains the metadata and class references for the mm_recomp world.
"""

# Required metadata
WORLD_NAME = "mm_recomp"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MMRWorld
WEB_WORLD_CLASS = MMRWebWorld
CLIENT_FUNCTION = None
