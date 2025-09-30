from . import RimworldWorld, RimworldWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Raft World Registration

This file contains the metadata and class references for the raft world.
"""

# Required metadata
WORLD_NAME = "rimworld"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RimworldWorld
WEB_WORLD_CLASS = RimworldWebWorld
CLIENT_FUNCTION = None
