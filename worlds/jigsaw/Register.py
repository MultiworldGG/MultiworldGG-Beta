from . import JigsawWorld
from . import JigsawWeb

"""
Make a Jigsaw puzzle! But first you'll have to find your pieces. World Registration

This file contains the metadata and class references for the jigsaw world.
"""

# Required metadata
WORLD_NAME = "jigsaw"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = JigsawWorld
WEB_WORLD_CLASS = JigsawWeb
CLIENT_FUNCTION = None
