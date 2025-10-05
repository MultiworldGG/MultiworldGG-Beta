from . import WL4World
from . import WL4Web

"""
A golden pyramid has been discovered deep in the jungle, and Wario has set World Registration

This file contains the metadata and class references for the wl4 world.
"""

# Required metadata
WORLD_NAME = "wl4"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WL4World
WEB_WORLD_CLASS = WL4Web
CLIENT_FUNCTION = None
