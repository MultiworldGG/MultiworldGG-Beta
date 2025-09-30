from . import AdventureWorld, AdventureWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Adventure for the Atari 2600 is an early graphical adventure game. World Registration

This file contains the metadata and class references for the adventure world.
"""

# Required metadata
WORLD_NAME = "adventure"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AdventureWorld
WEB_WORLD_CLASS = AdventureWeb
CLIENT_FUNCTION = launch
