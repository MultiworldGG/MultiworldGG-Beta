from . import HereComesNikoWorld, HereComesNikoWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Here Comes Niko! World Registration

This file contains the metadata and class references for the hcniko world.
"""

# Required metadata
WORLD_NAME = "hcniko"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HereComesNikoWorld
WEB_WORLD_CLASS = HereComesNikoWebWorld
CLIENT_FUNCTION = None
