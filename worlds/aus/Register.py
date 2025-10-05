from . import AUSWorld
from . import AnUntitledStoryWeb

"""
An Untitled Story World Registration

This file contains the metadata and class references for the aus world.
"""

# Required metadata
WORLD_NAME = "aus"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AUSWorld
WEB_WORLD_CLASS = AnUntitledStoryWeb
CLIENT_FUNCTION = None
