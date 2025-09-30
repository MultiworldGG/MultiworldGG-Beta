from . import JigsawWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import JigsawWeb

"""
Make a Jigsaw puzzle! But first you'll have to find your pieces. World Registration

This file contains the metadata and class references for the jigsaw world.
"""

# Required metadata
WORLD_NAME = "jigsaw"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = JigsawWorld
WEB_WORLD_CLASS = JigsawWeb
CLIENT_FUNCTION = None
