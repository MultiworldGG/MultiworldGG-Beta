from . import WargrooveWorld, WargrooveWeb
from .Client import launch

"""
Wargroove World Registration

This file contains the metadata and class references for the wargroove world.
"""

# Required metadata
WORLD_NAME = "wargroove"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WargrooveWorld
WEB_WORLD_CLASS = WargrooveWeb
CLIENT_FUNCTION = launch
