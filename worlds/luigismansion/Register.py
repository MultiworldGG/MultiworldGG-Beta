from . import LMWorld, LMWeb
from .LMClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi. World Registration

This file contains the metadata and class references for the luigismansion world.
"""

# Required metadata
WORLD_NAME = "luigismansion"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LMWorld
WEB_WORLD_CLASS = LMWeb
CLIENT_FUNCTION = launch
