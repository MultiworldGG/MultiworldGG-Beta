from . import BumpStikWorld
from . import BumpStikWeb

"""
Bumper Stickers World Registration

This file contains the metadata and class references for the bumpstik world.
"""

# Required metadata
WORLD_NAME = "bumpstik"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BumpStikWorld
WEB_WORLD_CLASS = BumpStikWeb
CLIENT_FUNCTION = None
