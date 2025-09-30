from . import OriBlindForestWorld, OriBlindForestWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Ori and the Blind Forest World Registration

This file contains the metadata and class references for the oribf world.
"""

# Required metadata
WORLD_NAME = "oribf"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OriBlindForestWorld
WEB_WORLD_CLASS = OriBlindForestWebWorld
CLIENT_FUNCTION = None
