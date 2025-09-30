from . import DoronkoWankoWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DoronkoWankoWeb

"""
DORONKO WANKO World Registration

This file contains the metadata and class references for the doronko_wanko world.
"""

# Required metadata
WORLD_NAME = "doronko_wanko"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DoronkoWankoWorld
WEB_WORLD_CLASS = DoronkoWankoWeb
CLIENT_FUNCTION = None
