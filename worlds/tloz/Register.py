from . import TLoZWorld, TLoZWeb
from .Client import launch

"""
The Legend of Zelda World Registration

This file contains the metadata and class references for the tloz world.
"""

# Required metadata
WORLD_NAME = "tloz"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TLoZWorld
WEB_WORLD_CLASS = TLoZWeb
CLIENT_FUNCTION = launch
