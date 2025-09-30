from . import Rac2World, Rac2Web
from .Rac2Client import launch

"""
Ratchet & Clank 2 World Registration

This file contains the metadata and class references for the rac2 world.
"""

# Required metadata
WORLD_NAME = "rac2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Rac2World
WEB_WORLD_CLASS = Rac2Web
CLIENT_FUNCTION = launch
