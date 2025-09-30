from . import CandyBox2World, CandyBox2WebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Candy Box 2 World Registration

This file contains the metadata and class references for the candybox2 world.
"""

# Required metadata
WORLD_NAME = "candybox2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CandyBox2World
WEB_WORLD_CLASS = CandyBox2WebWorld
CLIENT_FUNCTION = None
