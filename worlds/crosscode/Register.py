from .world import CrossCodeWorld, CrossCodeWebWorld

"""
Crosscode World Registration

This file contains the metadata and class references for the crosscode world.
"""

# Required metadata
WORLD_NAME = "crosscode"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CrossCodeWorld
WEB_WORLD_CLASS = CrossCodeWebWorld
CLIENT_FUNCTION = None
