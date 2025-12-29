from . import DoSWorld, DoSWeb

"""
Castlevania: Dawn of Sorrow World Registration

This file contains the metadata and class references for the cv_dos world.
"""

# Required metadata
WORLD_NAME = "cv_dos"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DoSWorld
WEB_WORLD_CLASS = DoSWeb
CLIENT_FUNCTION = None
