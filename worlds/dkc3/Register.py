from . import DKC3World
from . import DKC3Web

"""
Donkey Kong Country 3 is an action platforming game. World Registration

This file contains the metadata and class references for the dkc3 world.
"""

# Required metadata
WORLD_NAME = "dkc3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKC3World
WEB_WORLD_CLASS = DKC3Web
CLIENT_FUNCTION = None
