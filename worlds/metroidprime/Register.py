from . import MetroidPrimeWorld, MetroidPrimeWeb
from .MetroidPrimeClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Metroid Prime World Registration

This file contains the metadata and class references for the metroidprime world.
"""

# Required metadata
WORLD_NAME = "metroidprime"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MetroidPrimeWorld
WEB_WORLD_CLASS = MetroidPrimeWeb
CLIENT_FUNCTION = launch
