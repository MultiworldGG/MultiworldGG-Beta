from . import InscryptionWorld, InscrypWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Inscryption World Registration

This file contains the metadata and class references for the inscryption world.
"""

# Required metadata
WORLD_NAME = "inscryption"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = InscryptionWorld
WEB_WORLD_CLASS = InscrypWeb
CLIENT_FUNCTION = None
