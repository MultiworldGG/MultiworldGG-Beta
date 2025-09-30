from .world import ZorkGrandInquisitorWorld, ZorkGrandInquisitorWebWorld
from .client import launch

"""
Zork Grand Inquisitor World Registration

This file contains the metadata and class references for the zork_grand_inquisitor world.
"""

# Required metadata
WORLD_NAME = "zork_grand_inquisitor"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ZorkGrandInquisitorWorld
WEB_WORLD_CLASS = ZorkGrandInquisitorWebWorld
CLIENT_FUNCTION = launch
