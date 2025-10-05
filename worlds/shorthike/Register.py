from . import ShortHikeWorld
from . import ShortHikeWeb

"""
A Short Hike World Registration

This file contains the metadata and class references for the shorthike world.
"""

# Required metadata
WORLD_NAME = "shorthike"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ShortHikeWorld
WEB_WORLD_CLASS = ShortHikeWeb
CLIENT_FUNCTION = None
