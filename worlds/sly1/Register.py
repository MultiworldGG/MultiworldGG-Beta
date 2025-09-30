from . import Sly1World, Sly1Web
from .Sly1Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
