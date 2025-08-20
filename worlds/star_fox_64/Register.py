from . import StarFox64World, StarFox64WebWorld
from .client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Star Fox 64 World Registration

This file contains the metadata and class references for the star_fox_64 world.
"""

# Required metadata
WORLD_NAME = "star_fox_64"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = StarFox64World
WEB_WORLD_CLASS = StarFox64WebWorld
CLIENT_FUNCTION = launch
