from . import HuniePop2, HuniePop2Web
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Huniepop2 World Registration

This file contains the metadata and class references for the huniepop2 world.
"""

# Required metadata
WORLD_NAME = "huniepop2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HuniePop2
WEB_WORLD_CLASS = HuniePop2Web
CLIENT_FUNCTION = None
