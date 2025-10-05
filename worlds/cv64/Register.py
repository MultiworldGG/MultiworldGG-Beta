from . import CV64World
from . import CV64Web

"""
Castlevania 64 World Registration

This file contains the metadata and class references for the cv64 world.
"""

# Required metadata
WORLD_NAME = "cv64"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CV64World
WEB_WORLD_CLASS = CV64Web
CLIENT_FUNCTION = None
