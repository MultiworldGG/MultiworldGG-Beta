from . import DK64World, DK64Web
from .archipelago.DK64Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Donkey Kong 64 is a 3D collectathon platforming game. World Registration

This file contains the metadata and class references for the dk64 world.
"""

# Required metadata
WORLD_NAME = "dk64"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DK64World
WEB_WORLD_CLASS = DK64Web
CLIENT_FUNCTION = launch
