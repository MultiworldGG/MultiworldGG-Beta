from . import GOIWorld, GOIWeb

"""
Getting Over It World Registration

This file contains the metadata and class references for the getting_over_it world.
"""

# Required metadata
WORLD_NAME = "getting_over_it"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GOIWorld
WEB_WORLD_CLASS = GOIWeb
CLIENT_FUNCTION = None
