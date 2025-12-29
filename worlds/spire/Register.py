from . import SpireWorld, SpireWeb

"""
Slay the Spire World Registration

This file contains the metadata and class references for the spire world.
"""

# Required metadata
WORLD_NAME = "spire"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SpireWorld
WEB_WORLD_CLASS = SpireWeb
CLIENT_FUNCTION = None
