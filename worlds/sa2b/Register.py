from . import SA2BWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SA2BWeb

"""
Sonic Adventure 2 Battle is an action platforming game. Play as Sonic, Tails, Knuckles, Shadow, Rouge, and Eggman across 31 stages and prevent the destruction of the earth. World Registration

This file contains the metadata and class references for the sa2b world.
"""

# Required metadata
WORLD_NAME = "sa2b"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SA2BWorld
WEB_WORLD_CLASS = SA2BWeb
CLIENT_FUNCTION = None
