from . import K64World, K64WebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Kirby 64 - The Crystal Shards World Registration

This file contains the metadata and class references for the k64 world.
"""

# Required metadata
WORLD_NAME = "k64"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = K64World
WEB_WORLD_CLASS = K64WebWorld
CLIENT_FUNCTION = None
