from . import FFMQWorld, FFMQWebWorld

"""
Final Fantasy Mystic Quest World Registration

This file contains the metadata and class references for the ffmq world.
"""

# Required metadata
WORLD_NAME = "ffmq"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FFMQWorld
WEB_WORLD_CLASS = FFMQWebWorld
CLIENT_FUNCTION = None
