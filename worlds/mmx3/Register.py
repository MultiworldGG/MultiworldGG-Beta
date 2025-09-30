from . import MMX3World
from . import MMX3Web

"""
Mega Man X3 World Registration

This file contains the metadata and class references for the mmx3 world.
"""

# Required metadata
WORLD_NAME = "mmx3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MMX3World
WEB_WORLD_CLASS = MMX3Web
CLIENT_FUNCTION = None
