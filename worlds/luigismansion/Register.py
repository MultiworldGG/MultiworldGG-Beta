from . import LMWorld, LMWeb
from .LMClient import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi. World Registration

This file contains the metadata and class references for the luigismansion world.
"""

# Required metadata
WORLD_NAME = "luigismansion"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LMWorld
WEB_WORLD_CLASS = LMWeb
CLIENT_FUNCTION = launch
