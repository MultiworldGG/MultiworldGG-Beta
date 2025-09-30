from . import V6World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import V6Web

"""
VVVVVV is a platform game all about exploring one simple mechanical idea - what if you reversed gravity instead of jumping? World Registration

This file contains the metadata and class references for the v6 world.
"""

# Required metadata
WORLD_NAME = "v6"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = V6World
WEB_WORLD_CLASS = V6Web
CLIENT_FUNCTION = None
