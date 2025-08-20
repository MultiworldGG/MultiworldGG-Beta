from . import ALBWWebWorld, ALBWWorld 
from .Client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
File name of your decrypted North American A Link Between Worlds ROM World Registration

This file contains the metadata and class references for the albw world.
"""

# Required metadata
WORLD_NAME = "albw"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ALBWWorld
WEB_WORLD_CLASS = ALBWWebWorld
CLIENT_FUNCTION = launch
