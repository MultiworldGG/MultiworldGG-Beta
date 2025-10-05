from . import FMWorld
from . import FMWeb

"""
Yu-Gi-Oh! Forbidden Memories is a PlayStation RPG with card-battling mechanics. Assume the role of the Prince of World Registration

This file contains the metadata and class references for the fm world.
"""

# Required metadata
WORLD_NAME = "fm"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FMWorld
WEB_WORLD_CLASS = FMWeb
CLIENT_FUNCTION = None
