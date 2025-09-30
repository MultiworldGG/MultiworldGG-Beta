from . import Sims4World, Sims4Web
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
The Sims 4 World Registration

This file contains the metadata and class references for the sims4 world.
"""

# Required metadata
WORLD_NAME = "sims4"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Sims4World
WEB_WORLD_CLASS = Sims4Web
CLIENT_FUNCTION = launch
