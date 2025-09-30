from . import LethalCompanyWorld
from . import LethalCompanyWeb

"""
Lethal Company World Registration

This file contains the metadata and class references for the lethal_company world.
"""

# Required metadata
WORLD_NAME = "lethal_company"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LethalCompanyWorld
WEB_WORLD_CLASS = LethalCompanyWeb
CLIENT_FUNCTION = None
