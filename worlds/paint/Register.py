from . import PaintWorld, PaintWebWorld

"""
Paint World Registration

This file contains the metadata and class references for the paint world.
"""

# Required metadata
WORLD_NAME = "paint"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PaintWorld
WEB_WORLD_CLASS = PaintWebWorld
CLIENT_FUNCTION = None
