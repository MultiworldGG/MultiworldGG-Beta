from . import ALBWWebWorld, ALBWWorld 
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
