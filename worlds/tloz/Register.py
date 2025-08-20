from . import TLoZWorld, TLoZWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Client import launch

"""
The Legend of Zelda World Registration

This file contains the metadata and class references for the tloz world.
"""

# Required metadata
WORLD_NAME = "tloz"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TLoZWorld
WEB_WORLD_CLASS = TLoZWeb
CLIENT_FUNCTION = launch
