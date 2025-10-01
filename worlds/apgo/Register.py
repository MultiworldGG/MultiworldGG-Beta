from . import APGOWorld
from . import APGOWebWorld

"""
Archipela-Go! World Registration

This file contains the metadata and class references for the apgo world.
"""

# Required metadata
WORLD_NAME = "apgo"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = APGOWorld
WEB_WORLD_CLASS = APGOWebWorld
CLIENT_FUNCTION = None
