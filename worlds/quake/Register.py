from . import Q1World, Q1Web
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Quake 1 World Registration

This file contains the metadata and class references for the quake world.
"""

# Required metadata
WORLD_NAME = "quake"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Q1World
WEB_WORLD_CLASS = Q1Web
CLIENT_FUNCTION = None
