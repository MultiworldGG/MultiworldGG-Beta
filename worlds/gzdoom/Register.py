from . import GZDoomWorld, GZDoomWeb
from .client.GZDoomClient import launch

"""
gzDoom World Registration

This file contains the metadata and class references for the gzdoom world.
"""

# Required metadata
WORLD_NAME = "gzdoom"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GZDoomWorld
WEB_WORLD_CLASS = GZDoomWeb
CLIENT_FUNCTION = launch
