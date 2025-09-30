from . import StardewWorld, StardewWebWorld
from .client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Stardew Valley World Registration

This file contains the metadata and class references for the stardew_valley world.
"""

# Required metadata
WORLD_NAME = "stardew_valley"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = StardewWorld
WEB_WORLD_CLASS = StardewWebWorld
CLIENT_FUNCTION = launch
