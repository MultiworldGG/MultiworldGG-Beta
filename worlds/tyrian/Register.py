from . import TyrianWebWorld, TyrianWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Tyrian World Registration

This file contains the metadata and class references for the tyrian world.
"""

# Required metadata
WORLD_NAME = "tyrian"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TyrianWorld
WEB_WORLD_CLASS = TyrianWebWorld
CLIENT_FUNCTION = None
