from . import PathOfExileWebWorld, PathOfExileWorld
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Path of Exile World Registration

This file contains the metadata and class references for the poe world.
"""

# Required metadata
WORLD_NAME = "poe"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PathOfExileWorld
WEB_WORLD_CLASS = PathOfExileWebWorld
CLIENT_FUNCTION = launch
