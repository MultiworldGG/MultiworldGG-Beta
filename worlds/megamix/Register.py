from . import MegaMixWorld, MegaMixWeb
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Hatsune Miku Project Diva Mega Mix+ World Registration

This file contains the metadata and class references for the megamix world.
"""

# Required metadata
WORLD_NAME = "megamix"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MegaMixWorld
WEB_WORLD_CLASS = MegaMixWeb
CLIENT_FUNCTION = launch
