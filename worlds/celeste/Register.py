from . import CelesteWebWorld, CelesteWorld

"""
Celeste World Registration

This file contains the metadata and class references for the celeste world.
"""

# Required metadata
WORLD_NAME = "celeste"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CelesteWorld
WEB_WORLD_CLASS = CelesteWebWorld
CLIENT_FUNCTION = None
