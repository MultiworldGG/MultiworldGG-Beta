from . import OOTWorld, OOTWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods, World Registration

This file contains the metadata and class references for the oot world.
"""

# Required metadata
WORLD_NAME = "oot"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OOTWorld
WEB_WORLD_CLASS = OOTWeb
CLIENT_FUNCTION = launch
