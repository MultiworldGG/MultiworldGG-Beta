from . import HKWorld
from . import HKWeb

"""
Hollow Knight World Registration

This file contains the metadata and class references for the hk world.
"""

# Required metadata
WORLD_NAME = "hk"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HKWorld
WEB_WORLD_CLASS = HKWeb
CLIENT_FUNCTION = None
