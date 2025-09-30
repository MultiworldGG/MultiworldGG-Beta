from . import SoEWorld, SoEWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
File name of the SoE US ROM World Registration

This file contains the metadata and class references for the soe world.
"""

# Required metadata
WORLD_NAME = "soe"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SoEWorld
WEB_WORLD_CLASS = SoEWebWorld
CLIENT_FUNCTION = None
