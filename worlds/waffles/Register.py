from . import GenericWorld, GenericWeb

"""
Generic World Registration

This file contains the metadata and class references for the waffles world.
"""

# Required metadata
WORLD_NAME = "waffles"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GenericWorld
WEB_WORLD_CLASS = GenericWeb
CLIENT_FUNCTION = None
