from . import CupheadWorld, CupheadWebWorld

"""
Log options that are overridden from incompatible combinations to console. World Registration

This file contains the metadata and class references for the cuphead world.
"""

# Required metadata
WORLD_NAME = "cuphead"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CupheadWorld
WEB_WORLD_CLASS = CupheadWebWorld
CLIENT_FUNCTION = None
