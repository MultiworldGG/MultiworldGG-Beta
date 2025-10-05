from . import V6World
from . import V6Web

"""
VVVVVV is a platform game all about exploring one simple mechanical idea - what if you reversed gravity instead of jumping? World Registration

This file contains the metadata and class references for the v6 world.
"""

# Required metadata
WORLD_NAME = "v6"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = V6World
WEB_WORLD_CLASS = V6Web
CLIENT_FUNCTION = None
