from . import CrystalProjectWorld
from .constants import GAME_NAME as from BaseUtils import get_archipelago_json()
game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from . import CrystalProjectWeb

"""
Crystal Project World Registration

This file contains the metadata and class references for the crystal_project world.
"""

# Required metadata
WORLD_NAME = "crystal_project"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CrystalProjectWorld
WEB_WORLD_CLASS = CrystalProjectWeb
CLIENT_FUNCTION = None
