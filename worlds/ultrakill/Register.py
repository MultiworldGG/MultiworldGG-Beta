from . import UltrakillWorld
from . import UltrakillWeb

"""
ULTRAKILL World Registration

This file contains the metadata and class references for the ultrakill world.
"""

# Required metadata
WORLD_NAME = "ultrakill"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = UltrakillWorld
WEB_WORLD_CLASS = UltrakillWeb
CLIENT_FUNCTION = None
