from . import AquariaWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import AquariaWeb

"""
Aquaria is a side-scrolling action-adventure game. It follows Naija, an World Registration

This file contains the metadata and class references for the aquaria world.
"""

# Required metadata
WORLD_NAME = "aquaria"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AquariaWorld
WEB_WORLD_CLASS = AquariaWeb
CLIENT_FUNCTION = None
