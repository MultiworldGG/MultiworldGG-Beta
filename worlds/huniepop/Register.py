from . import HuniePop, HuniePopWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Huniepop World Registration

This file contains the metadata and class references for the huniepop world.
"""

# Required metadata
WORLD_NAME = "huniepop"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HuniePop
WEB_WORLD_CLASS = HuniePopWeb
CLIENT_FUNCTION = None
