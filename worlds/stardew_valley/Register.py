from . import StardewWorld, StardewWebWorld
from .client import launch

"""
Stardew Valley World Registration

This file contains the metadata and class references for the stardew_valley world.
"""

# Required metadata
WORLD_NAME = "stardew_valley"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = StardewWorld
WEB_WORLD_CLASS = StardewWebWorld
CLIENT_FUNCTION = launch
