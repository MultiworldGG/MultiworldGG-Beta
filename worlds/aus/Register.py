from . import AUSWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import AnUntitledStoryWeb

"""
An Untitled Story World Registration

This file contains the metadata and class references for the aus world.
"""

# Required metadata
WORLD_NAME = "aus"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AUSWorld
WEB_WORLD_CLASS = AnUntitledStoryWeb
CLIENT_FUNCTION = None
