from . import SMZ3World
from . import SMZ3Web

"""
SMZ3 World Registration

This file contains the metadata and class references for the smz3 world.
"""

# Required metadata
WORLD_NAME = "smz3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMZ3World
WEB_WORLD_CLASS = SMZ3Web
CLIENT_FUNCTION = None
