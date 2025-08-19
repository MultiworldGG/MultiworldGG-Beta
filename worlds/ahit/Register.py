from . import HatInTimeWorld, HatInTimeWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
A Hat in Time World Registration

This file contains the metadata and class references for the ahit world.
"""

# Required metadata
WORLD_NAME = "ahit"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HatInTimeWorld
WEB_WORLD_CLASS = HatInTimeWeb
CLIENT_FUNCTION = None
