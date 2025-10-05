from . import CTJoTWorld, CTJoTWebWorld

"""
Chrono Trigger Jets of Time World Registration

This file contains the metadata and class references for the ctjot world.
"""

# Required metadata
WORLD_NAME = "ctjot"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CTJoTWorld
WEB_WORLD_CLASS = CTJoTWebWorld
CLIENT_FUNCTION = None
