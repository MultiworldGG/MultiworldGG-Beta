from . import InscryptionWorld, InscrypWeb

"""
Inscryption World Registration

This file contains the metadata and class references for the inscryption world.
"""

# Required metadata
WORLD_NAME = "inscryption"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = InscryptionWorld
WEB_WORLD_CLASS = InscrypWeb
CLIENT_FUNCTION = None
