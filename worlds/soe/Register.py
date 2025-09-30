from . import SoEWorld, SoEWebWorld

"""
File name of the SoE US ROM World Registration

This file contains the metadata and class references for the soe world.
"""

# Required metadata
WORLD_NAME = "soe"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SoEWorld
WEB_WORLD_CLASS = SoEWebWorld
CLIENT_FUNCTION = None
