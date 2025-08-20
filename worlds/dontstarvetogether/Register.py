from . import DSTWorld, DSTWeb
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Don World Registration

This file contains the metadata and class references for the dontstarvetogether world.
"""

# Required metadata
WORLD_NAME = "dontstarvetogether"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DSTWorld
WEB_WORLD_CLASS = DSTWeb
CLIENT_FUNCTION = launch
