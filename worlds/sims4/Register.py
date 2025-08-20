from . import Sims4World, Sims4Web
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Sims 4 World Registration

This file contains the metadata and class references for the sims4 world.
"""

# Required metadata
WORLD_NAME = "sims4"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Sims4World
WEB_WORLD_CLASS = Sims4Web
CLIENT_FUNCTION = launch
