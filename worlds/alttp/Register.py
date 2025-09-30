from . import ALTTPWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ALTTPWeb

"""
A Link to the Past World Registration

This file contains the metadata and class references for the alttp world.
"""

# Required metadata
WORLD_NAME = "alttp"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ALTTPWorld
WEB_WORLD_CLASS = ALTTPWeb
CLIENT_FUNCTION = None
