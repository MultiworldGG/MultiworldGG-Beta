from . import MuseDashWorld, MuseDashWebWorld

"""
Muse Dash World Registration

This file contains the metadata and class references for the musedash world.
"""

# Required metadata
WORLD_NAME = "musedash"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MuseDashWorld
WEB_WORLD_CLASS = MuseDashWebWorld
CLIENT_FUNCTION = None
