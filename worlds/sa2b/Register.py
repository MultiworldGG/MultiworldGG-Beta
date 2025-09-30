from . import SA2BWorld
from . import SA2BWeb

"""
Sonic Adventure 2 Battle is an action platforming game. Play as Sonic, Tails, Knuckles, Shadow, Rouge, and Eggman across 31 stages and prevent the destruction of the earth. World Registration

This file contains the metadata and class references for the sa2b world.
"""

# Required metadata
WORLD_NAME = "sa2b"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SA2BWorld
WEB_WORLD_CLASS = SA2BWeb
CLIENT_FUNCTION = None
