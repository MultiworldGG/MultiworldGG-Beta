from . import ResidentEvil3Remake, ResidentEvil3RemakeWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Residentevil3Remake World Registration

This file contains the metadata and class references for the residentevil3remake world.
"""

# Required metadata
WORLD_NAME = "residentevil3remake"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ResidentEvil3Remake
WEB_WORLD_CLASS = ResidentEvil3RemakeWeb
CLIENT_FUNCTION = None
