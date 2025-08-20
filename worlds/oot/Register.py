from . import OOTWorld, OOTWeb
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods, World Registration

This file contains the metadata and class references for the oot world.
"""

# Required metadata
WORLD_NAME = "oot"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OOTWorld
WEB_WORLD_CLASS = OOTWeb
CLIENT_FUNCTION = launch
