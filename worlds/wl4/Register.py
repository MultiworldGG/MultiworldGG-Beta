from . import WL4World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import WL4Web

"""
A golden pyramid has been discovered deep in the jungle, and Wario has set World Registration

This file contains the metadata and class references for the wl4 world.
"""

# Required metadata
WORLD_NAME = "wl4"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WL4World
WEB_WORLD_CLASS = WL4Web
CLIENT_FUNCTION = None
