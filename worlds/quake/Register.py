from . import Q1World, Q1Web

"""
Quake 1 World Registration

This file contains the metadata and class references for the quake world.
"""

# Required metadata
WORLD_NAME = "quake"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Q1World
WEB_WORLD_CLASS = Q1Web
CLIENT_FUNCTION = None
