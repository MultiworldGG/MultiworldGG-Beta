from . import OuterWildsWorld, OuterWildsWebWorld

"""
Outer Wilds World Registration

This file contains the metadata and class references for the outer_wilds world.
"""

# Required metadata
WORLD_NAME = "outer_wilds"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OuterWildsWorld
WEB_WORLD_CLASS = OuterWildsWebWorld
CLIENT_FUNCTION = None
