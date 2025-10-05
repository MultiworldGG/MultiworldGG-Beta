from . import Wargroove2World, Wargroove2Web
from .Client import launch

"""
Wargroove 2 World Registration

This file contains the metadata and class references for the wargroove2 world.
"""

# Required metadata
WORLD_NAME = "wargroove2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Wargroove2World
WEB_WORLD_CLASS = Wargroove2Web
CLIENT_FUNCTION = launch
