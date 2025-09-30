from . import ShiversWorld
from . import ShiversWeb

"""
Shivers World Registration

This file contains the metadata and class references for the shivers world.
"""

# Required metadata
WORLD_NAME = "shivers"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ShiversWorld
WEB_WORLD_CLASS = ShiversWeb
CLIENT_FUNCTION = None
