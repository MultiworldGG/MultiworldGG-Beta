from . import AdventureWorld, AdventureWeb
from .Client import launch
"""
Adventure for the Atari 2600 is an early graphical adventure game. World Registration

This file contains the metadata and class references for the adventure world.
"""

# Required metadata
WORLD_NAME = "adventure"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AdventureWorld
WEB_WORLD_CLASS = AdventureWeb
CLIENT_FUNCTION = launch
