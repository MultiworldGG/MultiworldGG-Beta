from . import OOTWorld, OOTWeb
from .Client import launch

"""
The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods, World Registration

This file contains the metadata and class references for the oot world.
"""

# Required metadata
WORLD_NAME = "oot"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OOTWorld
WEB_WORLD_CLASS = OOTWeb
CLIENT_FUNCTION = launch
