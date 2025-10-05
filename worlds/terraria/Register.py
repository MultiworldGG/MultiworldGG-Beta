from . import TerrariaWorld
from . import TerrariaWeb

"""
Terraria World Registration

This file contains the metadata and class references for the terraria world.
"""

# Required metadata
WORLD_NAME = "terraria"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TerrariaWorld
WEB_WORLD_CLASS = TerrariaWeb
CLIENT_FUNCTION = None
