from . import UndertaleWorld, UndertaleWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Undertale World Registration

This file contains the metadata and class references for the undertale world.
"""

# Required metadata
WORLD_NAME = "undertale"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = UndertaleWorld
WEB_WORLD_CLASS = UndertaleWeb
CLIENT_FUNCTION = launch
