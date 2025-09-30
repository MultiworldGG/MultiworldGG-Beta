from . import PseudoregaliaWorld, PseudoregaliaWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pseudoregalia World Registration

This file contains the metadata and class references for the pseudoregalia world.
"""

# Required metadata
WORLD_NAME = "pseudoregalia"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PseudoregaliaWorld
WEB_WORLD_CLASS = PseudoregaliaWeb
CLIENT_FUNCTION = None
