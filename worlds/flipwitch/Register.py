from . import FlipwitchWorld, FlipwitchWeb

"""
Flipwitch World Registration

This file contains the metadata and class references for the flipwitch world.
"""

# Required metadata
WORLD_NAME = "flipwitch"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FlipwitchWorld
WEB_WORLD_CLASS = FlipwitchWeb
CLIENT_FUNCTION = None