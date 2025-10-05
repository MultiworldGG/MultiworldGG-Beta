from . import DarkSouls3World
from . import DarkSouls3Web

"""
Dark Souls III World Registration

This file contains the metadata and class references for the dark_souls_3 world.
"""

# Required metadata
WORLD_NAME = "dark_souls_3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DarkSouls3World
WEB_WORLD_CLASS = DarkSouls3Web
CLIENT_FUNCTION = None
