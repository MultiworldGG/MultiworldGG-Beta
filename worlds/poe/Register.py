from . import PathOfExileWebWorld, PathOfExileWorld
from .Client import launch

"""
Path of Exile World Registration

This file contains the metadata and class references for the poe world.
"""

# Required metadata
WORLD_NAME = "poe"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PathOfExileWorld
WEB_WORLD_CLASS = PathOfExileWebWorld
CLIENT_FUNCTION = launch
