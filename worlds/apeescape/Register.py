from . import ApeEscapeWorld
from . import ApeEscapeWeb

"""
Ape Escape World Registration

This file contains the metadata and class references for the apeescape world.
"""

# Required metadata
WORLD_NAME = "apeescape"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ApeEscapeWorld
WEB_WORLD_CLASS = ApeEscapeWeb
CLIENT_FUNCTION = None
