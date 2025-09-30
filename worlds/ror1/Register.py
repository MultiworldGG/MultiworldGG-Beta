from . import RoR1World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import RiskOfWeb

"""
Risk of Rain World Registration

This file contains the metadata and class references for the ror1 world.
"""

# Required metadata
WORLD_NAME = "ror1"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RoR1World
WEB_WORLD_CLASS = RiskOfWeb
CLIENT_FUNCTION = None
