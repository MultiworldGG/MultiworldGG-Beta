from . import OsuWorld, OsuWebWorld
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
osu! is a free to play rhythm game featuring 4 modes, an online ranking system/statistics, World Registration

This file contains the metadata and class references for the osu world.
"""

# Required metadata
WORLD_NAME = "osu"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OsuWorld
WEB_WORLD_CLASS = OsuWebWorld
CLIENT_FUNCTION = launch
