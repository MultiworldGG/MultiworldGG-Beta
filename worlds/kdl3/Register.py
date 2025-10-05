from . import KDL3World,KDL3WebWorld

"""
Kirby World Registration

This file contains the metadata and class references for the kdl3 world.
"""

# Required metadata
WORLD_NAME = "kdl3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = KDL3World
WEB_WORLD_CLASS = KDL3WebWorld
CLIENT_FUNCTION = None
