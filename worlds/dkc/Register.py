from . import DKCWorld
from . import DKCWeb

"""
Donkey Kong Country World Registration

This file contains the metadata and class references for the dkc world.
"""

# Required metadata
WORLD_NAME = "dkc"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKCWorld
WEB_WORLD_CLASS = DKCWeb
CLIENT_FUNCTION = None
