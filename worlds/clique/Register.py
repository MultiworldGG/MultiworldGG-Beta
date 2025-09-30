from . import CliqueWebWorld, CliqueWorld

"""
Clique World Registration

This file contains the metadata and class references for the clique world.
"""

# Required metadata
WORLD_NAME = "clique"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CliqueWorld
WEB_WORLD_CLASS = CliqueWebWorld
CLIENT_FUNCTION = None
