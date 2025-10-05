from . import MetroidPrimeWorld, MetroidPrimeWeb
from .MetroidPrimeClient import launch

"""
Metroid Prime World Registration

This file contains the metadata and class references for the metroidprime world.
"""

# Required metadata
WORLD_NAME = "metroidprime"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MetroidPrimeWorld
WEB_WORLD_CLASS = MetroidPrimeWeb
CLIENT_FUNCTION = launch
