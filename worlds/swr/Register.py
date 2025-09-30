from . import SWRWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SWRWeb

"""
Star Wars Episode I: Racer is a racing game where the player wins prize money and buys upgrades for their vehicle. World Registration

This file contains the metadata and class references for the swr world.
"""

# Required metadata
WORLD_NAME = "swr"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SWRWorld
WEB_WORLD_CLASS = SWRWeb
CLIENT_FUNCTION = None
