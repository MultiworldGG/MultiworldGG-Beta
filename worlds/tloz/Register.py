from . import TLoZWorld, TLoZWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
The Legend of Zelda World Registration

This file contains the metadata and class references for the tloz world.
"""

# Required metadata
WORLD_NAME = "tloz"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TLoZWorld
WEB_WORLD_CLASS = TLoZWeb
CLIENT_FUNCTION = launch
