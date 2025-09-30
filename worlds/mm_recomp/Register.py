from . import MMRWorld, MMRWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
