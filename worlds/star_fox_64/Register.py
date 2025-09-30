from . import StarFox64World, StarFox64WebWorld
from .client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Star Fox 64 World Registration

This file contains the metadata and class references for the star_fox_64 world.
"""

# Required metadata
WORLD_NAME = "star_fox_64"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = StarFox64World
WEB_WORLD_CLASS = StarFox64WebWorld
CLIENT_FUNCTION = launch
