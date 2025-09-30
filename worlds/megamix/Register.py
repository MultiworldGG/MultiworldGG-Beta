from . import MegaMixWorld, MegaMixWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Hatsune Miku Project Diva Mega Mix+ World Registration

This file contains the metadata and class references for the megamix world.
"""

# Required metadata
WORLD_NAME = "megamix"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MegaMixWorld
WEB_WORLD_CLASS = MegaMixWeb
CLIENT_FUNCTION = launch
