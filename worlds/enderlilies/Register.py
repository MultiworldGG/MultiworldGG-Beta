from . import EnderLiliesWorld
from . import EnderLiliesWeb

"""
Ender Lilies World Registration

This file contains the metadata and class references for the enderlilies world.
"""

# Required metadata
WORLD_NAME = "enderlilies"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EnderLiliesWorld
WEB_WORLD_CLASS = EnderLiliesWeb
CLIENT_FUNCTION = None
