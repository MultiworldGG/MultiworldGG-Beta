from . import ToontownWorld, ToontownWeb

"""
Toontown World Registration

This file contains the metadata and class references for the toontown world.
"""

# Required metadata
WORLD_NAME = "toontown"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ToontownWorld
WEB_WORLD_CLASS = ToontownWeb
CLIENT_FUNCTION = None
