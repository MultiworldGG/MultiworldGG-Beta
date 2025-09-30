from . import EarthBoundWorld
from . import EBWeb

"""
EarthBound World Registration

This file contains the metadata and class references for the earthbound world.
"""

# Required metadata
WORLD_NAME = "earthbound"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EarthBoundWorld
WEB_WORLD_CLASS = EBWeb
CLIENT_FUNCTION = None
