from . import EnderLiliesWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import EnderLiliesWeb

"""
Ender Lilies World Registration

This file contains the metadata and class references for the enderlilies world.
"""

# Required metadata
WORLD_NAME = "enderlilies"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EnderLiliesWorld
WEB_WORLD_CLASS = EnderLiliesWeb
CLIENT_FUNCTION = None
