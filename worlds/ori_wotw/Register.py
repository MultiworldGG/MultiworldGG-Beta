from . import WotWWorld, WotWWeb

"""
Ori and the Will of the Wisps World Registration

This file contains the metadata and class references for the ori_wotw world.
"""

# Required metadata
WORLD_NAME = "ori_wotw"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WotWWorld
WEB_WORLD_CLASS = WotWWeb
CLIENT_FUNCTION = None
