from . import TunicWorld, TunicWeb

"""
Tunic World Registration

This file contains the metadata and class references for the tunic world.
"""

# Required metadata
WORLD_NAME = "tunic"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TunicWorld
WEB_WORLD_CLASS = TunicWeb
CLIENT_FUNCTION = None
