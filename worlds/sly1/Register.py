from . import Sly1World, Sly1Web
from .Sly1Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Sly Cooper and the Thievius Raccoonus World Registration

This file contains the metadata and class references for the sly1 world.
"""

# Required metadata
WORLD_NAME = "sly1"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Sly1World
WEB_WORLD_CLASS = Sly1Web
CLIENT_FUNCTION = launch
