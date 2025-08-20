from . import Rac2World, Rac2Web
from .Rac2Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Ratchet & Clank 2 World Registration

This file contains the metadata and class references for the rac2 world.
"""

# Required metadata
WORLD_NAME = "rac2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Rac2World
WEB_WORLD_CLASS = Rac2Web
CLIENT_FUNCTION = launch
