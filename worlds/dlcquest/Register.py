from . import DLCqworld, DLCqwebworld

"""
Dlcquest World Registration

This file contains the metadata and class references for the dlcquest world.
"""

# Required metadata
WORLD_NAME = "dlcquest"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DLCqworld
WEB_WORLD_CLASS = DLCqwebworld
CLIENT_FUNCTION = None
