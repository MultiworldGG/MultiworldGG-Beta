from . import MK64World
from . import MK64Web

"""
Mario Kart 64 World Registration

This file contains the metadata and class references for the mk64 world.
"""

# Required metadata
WORLD_NAME = "mk64"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MK64World
WEB_WORLD_CLASS = MK64Web
CLIENT_FUNCTION = None
