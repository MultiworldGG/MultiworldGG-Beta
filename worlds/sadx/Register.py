from . import SonicAdventureDXWorld
from . import SonicAdventureDXWeb

"""
Sonic Adventure DX World Registration

This file contains the metadata and class references for the sadx world.
"""

# Required metadata
WORLD_NAME = "sadx"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SonicAdventureDXWorld
WEB_WORLD_CLASS = SonicAdventureDXWeb
CLIENT_FUNCTION = None
