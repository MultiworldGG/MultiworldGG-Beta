from . import CCCharlesWeb, CCCharlesWorld

"""
Choo-Choo Charles World Registration

This file contains the metadata and class references for the choo-choo charles world.
"""

# Required metadata
WORLD_NAME = "cccharles"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CCCharlesWorld
WEB_WORLD_CLASS = CCCharlesWeb
CLIENT_FUNCTION = None
