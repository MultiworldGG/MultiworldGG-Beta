from . import ShiversWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ShiversWeb

"""
Shivers World Registration

This file contains the metadata and class references for the shivers world.
"""

# Required metadata
WORLD_NAME = "shivers"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ShiversWorld
WEB_WORLD_CLASS = ShiversWeb
CLIENT_FUNCTION = None
