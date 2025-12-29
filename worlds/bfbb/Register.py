from . import BattleForBikiniBottom, BattleForBikiniBottomWeb

"""
Battle For Bikini Bottom World Registration

This file contains the metadata and class references for the bfbb world.
"""

# Required metadata
WORLD_NAME = "bfbb"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BattleForBikiniBottom
WEB_WORLD_CLASS = BattleForBikiniBottomWeb
CLIENT_FUNCTION = None
