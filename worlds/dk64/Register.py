from . import DK64World, DK64Web

"""
DK64 World Registration

This file contains the metadata and class references for the dk64 world.
"""

# Required metadata
WORLD_NAME = "dk64"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DK64World
WEB_WORLD_CLASS = DK64Web
CLIENT_FUNCTION = None
