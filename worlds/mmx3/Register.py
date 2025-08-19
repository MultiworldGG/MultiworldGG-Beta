from . import MMX3World
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from . import MMX3Web

"""
Mega Man X3 World Registration

This file contains the metadata and class references for the mmx3 world.
"""

# Required metadata
WORLD_NAME = "mmx3"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MMX3World
WEB_WORLD_CLASS = MMX3Web
CLIENT_FUNCTION = None
