from . import SSWorld, SSWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .SSClient import launch

"""
What if that's Zelda down there, and she's sending me a signal? It's a sign! World Registration

This file contains the metadata and class references for the ss world.
"""

# Required metadata
WORLD_NAME = "ss"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SSWorld
WEB_WORLD_CLASS = SSWeb
CLIENT_FUNCTION = launch
