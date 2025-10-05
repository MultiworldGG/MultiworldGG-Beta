from . import K64World, K64WebWorld

"""
Kirby 64 - The Crystal Shards World Registration

This file contains the metadata and class references for the k64 world.
"""

# Required metadata
WORLD_NAME = "k64"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = K64World
WEB_WORLD_CLASS = K64WebWorld
CLIENT_FUNCTION = None
