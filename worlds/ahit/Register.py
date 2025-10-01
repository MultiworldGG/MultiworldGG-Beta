from . import HatInTimeWorld, AWebInTime
from .Client import launch

"""
A Hat in Time World Registration

This file contains the metadata and class references for the ahit world.
"""

# Required metadata
WORLD_NAME = "ahit"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HatInTimeWorld
WEB_WORLD_CLASS = AWebInTime
CLIENT_FUNCTION = launch
