from . import RoR1World
from . import RiskOfWeb

"""
Risk of Rain World Registration

This file contains the metadata and class references for the ror1 world.
"""

# Required metadata
WORLD_NAME = "ror1"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RoR1World
WEB_WORLD_CLASS = RiskOfWeb
CLIENT_FUNCTION = None
