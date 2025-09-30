from . import MessengerWorld
from . import MessengerWeb

"""
The Messenger World Registration

This file contains the metadata and class references for the messenger world.
"""

# Required metadata
WORLD_NAME = "messenger"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MessengerWorld
WEB_WORLD_CLASS = MessengerWeb
CLIENT_FUNCTION = None
