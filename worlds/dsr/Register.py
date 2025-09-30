from . import DSRWorld
from . import DSRWeb

"""
Dark Souls is a game where you die. World Registration

This file contains the metadata and class references for the dsr world.
"""

# Required metadata
WORLD_NAME = "dsr"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DSRWorld
WEB_WORLD_CLASS = DSRWeb
CLIENT_FUNCTION = None
