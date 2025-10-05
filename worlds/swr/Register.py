from . import SWRWorld
from . import SWRWeb

"""
Star Wars Episode I: Racer is a racing game where the player wins prize money and buys upgrades for their vehicle. World Registration

This file contains the metadata and class references for the swr world.
"""

# Required metadata
WORLD_NAME = "swr"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SWRWorld
WEB_WORLD_CLASS = SWRWeb
CLIENT_FUNCTION = None
