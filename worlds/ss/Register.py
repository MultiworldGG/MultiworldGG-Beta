from . import SSWorld, SSWeb
from .SSClient import launch

"""
What if that's Zelda down there, and she's sending me a signal? It's a sign! World Registration

This file contains the metadata and class references for the ss world.
"""

# Required metadata
WORLD_NAME = "ss"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SSWorld
WEB_WORLD_CLASS = SSWeb
CLIENT_FUNCTION = launch
