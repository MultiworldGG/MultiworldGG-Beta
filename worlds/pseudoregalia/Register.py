from . import PseudoregaliaWorld, PseudoregaliaWeb

"""
Pseudoregalia World Registration

This file contains the metadata and class references for the pseudoregalia world.
"""

# Required metadata
WORLD_NAME = "pseudoregalia"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PseudoregaliaWorld
WEB_WORLD_CLASS = PseudoregaliaWeb
CLIENT_FUNCTION = None
