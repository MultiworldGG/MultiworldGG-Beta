from . import LMWorld, LMWeb
from .LMClient import launch

"""
Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi. World Registration

This file contains the metadata and class references for the luigismansion world.
"""

# Required metadata
WORLD_NAME = "luigismansion"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LMWorld
WEB_WORLD_CLASS = LMWeb
CLIENT_FUNCTION = launch
