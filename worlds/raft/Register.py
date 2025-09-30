from . import RaftWorld, RaftWeb

"""
Raft World Registration

This file contains the metadata and class references for the raft world.
"""

# Required metadata
WORLD_NAME = "raft"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RaftWorld
WEB_WORLD_CLASS = RaftWeb
CLIENT_FUNCTION = None
