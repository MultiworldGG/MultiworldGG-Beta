from . import ALBWWebWorld, ALBWWorld 
from .Client import launch

"""
File name of your decrypted North American A Link Between Worlds ROM World Registration

This file contains the metadata and class references for the albw world.
"""

# Required metadata
WORLD_NAME = "albw"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ALBWWorld
WEB_WORLD_CLASS = ALBWWebWorld
CLIENT_FUNCTION = launch
