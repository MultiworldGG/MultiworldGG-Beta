from . import RaftWorld, RaftWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Raft World Registration

This file contains the metadata and class references for the raft world.
"""

# Required metadata
WORLD_NAME = "raft"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RaftWorld
WEB_WORLD_CLASS = RaftWeb
CLIENT_FUNCTION = None
