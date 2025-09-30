from . import LethalCompanyWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import LethalCompanyWeb

"""
Lethal Company World Registration

This file contains the metadata and class references for the lethal_company world.
"""

# Required metadata
WORLD_NAME = "lethal_company"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LethalCompanyWorld
WEB_WORLD_CLASS = LethalCompanyWeb
CLIENT_FUNCTION = None
