from . import MeritousWorld
from . import MeritousWeb

"""
Meritous Gaiden is a procedurally generated bullet-hell dungeon crawl game. World Registration

This file contains the metadata and class references for the meritous world.
"""

# Required metadata
WORLD_NAME = "meritous"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MeritousWorld
WEB_WORLD_CLASS = MeritousWeb
CLIENT_FUNCTION = None
