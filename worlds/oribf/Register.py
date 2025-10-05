from . import OriBlindForestWorld, OriBlindForestWebWorld

"""
Ori and the Blind Forest World Registration

This file contains the metadata and class references for the oribf world.
"""

# Required metadata
WORLD_NAME = "oribf"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OriBlindForestWorld
WEB_WORLD_CLASS = OriBlindForestWebWorld
CLIENT_FUNCTION = None
