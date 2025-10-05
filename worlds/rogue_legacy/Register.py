from . import RLWorld
from . import RLWeb

"""
Rogue Legacy World Registration

This file contains the metadata and class references for the rogue_legacy world.
"""

# Required metadata
WORLD_NAME = "rogue_legacy"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RLWorld
WEB_WORLD_CLASS = RLWeb
CLIENT_FUNCTION = None
