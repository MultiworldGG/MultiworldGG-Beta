from . import DoronkoWankoWorld
from . import DoronkoWankoWeb

"""
DORONKO WANKO World Registration

This file contains the metadata and class references for the doronko_wanko world.
"""

# Required metadata
WORLD_NAME = "doronko_wanko"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DoronkoWankoWorld
WEB_WORLD_CLASS = DoronkoWankoWeb
CLIENT_FUNCTION = None
