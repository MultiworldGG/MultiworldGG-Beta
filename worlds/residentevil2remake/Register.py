from . import ResidentEvil2Remake, ResidentEvil2RemakeWeb

"""
Residentevil2Remake World Registration

This file contains the metadata and class references for the residentevil2remake world.
"""

# Required metadata
WORLD_NAME = "residentevil2remake"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ResidentEvil2Remake
WEB_WORLD_CLASS = ResidentEvil2RemakeWeb
CLIENT_FUNCTION = None
