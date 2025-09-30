from . import BumpStikWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import BumpStikWeb

"""
Bumper Stickers World Registration

This file contains the metadata and class references for the bumpstik world.
"""

# Required metadata
WORLD_NAME = "bumpstik"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BumpStikWorld
WEB_WORLD_CLASS = BumpStikWeb
CLIENT_FUNCTION = None
