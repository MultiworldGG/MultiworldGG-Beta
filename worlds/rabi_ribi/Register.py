from . import RabiRibiWorld, RabiRibiWeb

"""
Rabi Ribi World Registration

This file contains the metadata and class references for the rabi_ribi world.
"""

# Required metadata
WORLD_NAME = "rabi_ribi"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RabiRibiWorld
WEB_WORLD_CLASS = RabiRibiWeb
CLIENT_FUNCTION = None
