from . import Q1World, Q1Web
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

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
