from . import LandstalkerWorld, LandstalkerWeb

"""
Landstalker - The Treasures of King Nole World Registration

This file contains the metadata and class references for the landstalker world.
"""

# Required metadata
WORLD_NAME = "landstalker"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LandstalkerWorld
WEB_WORLD_CLASS = LandstalkerWeb
CLIENT_FUNCTION = None
