from . import ManualWorld, ManualWeb
from ManualClient import launch

"""
Manual World Registration

This file contains the metadata and class references for the _manual world.
"""

# Required metadata
WORLD_NAME = "_manual"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ManualWorld
WEB_WORLD_CLASS = ManualWeb
CLIENT_FUNCTION = launch
