from . import Starcraft2World, Starcraft2WebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Starcraft 2 World Registration

This file contains the metadata and class references for the sc2 world.
"""

# Required metadata
WORLD_NAME = "sc2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Starcraft2World
WEB_WORLD_CLASS = Starcraft2WebWorld
CLIENT_FUNCTION = None
