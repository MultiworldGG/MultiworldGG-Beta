from . import MessengerWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import MessengerWeb

"""
The Messenger World Registration

This file contains the metadata and class references for the messenger world.
"""

# Required metadata
WORLD_NAME = "messenger"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MessengerWorld
WEB_WORLD_CLASS = MessengerWeb
CLIENT_FUNCTION = None
