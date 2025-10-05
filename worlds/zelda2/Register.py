from . import Z2World
from . import Z2Web

"""
Zelda II: The Adventure of Link World Registration

This file contains the metadata and class references for the zelda2 world.
"""

# Required metadata
WORLD_NAME = "zelda2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Z2World
WEB_WORLD_CLASS = Z2Web
CLIENT_FUNCTION = None
