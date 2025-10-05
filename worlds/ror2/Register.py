from . import RiskOfRainWorld
from . import RiskOfWeb

"""
Risk of Rain 2 World Registration

This file contains the metadata and class references for the ror2 world.
"""

# Required metadata
WORLD_NAME = "ror2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RiskOfRainWorld
WEB_WORLD_CLASS = RiskOfWeb
CLIENT_FUNCTION = None
