from . import AdventureWorld, AdventureWeb
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Adventure for the Atari 2600 is an early graphical adventure game. World Registration

This file contains the metadata and class references for the adventure world.
"""

# Required metadata
WORLD_NAME = "adventure"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AdventureWorld
WEB_WORLD_CLASS = AdventureWeb
CLIENT_FUNCTION = launch
