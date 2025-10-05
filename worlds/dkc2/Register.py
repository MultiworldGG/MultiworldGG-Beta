from . import DKC2World
from . import DKC2Web

"""
Donkey Kong Country 2 World Registration

This file contains the metadata and class references for the dkc2 world.
"""

# Required metadata
WORLD_NAME = "dkc2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKC2World
WEB_WORLD_CLASS = DKC2Web
CLIENT_FUNCTION = None
