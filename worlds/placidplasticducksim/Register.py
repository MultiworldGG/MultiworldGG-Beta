from . import PlacidPlasticDuckSimulator, PPDSWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Peaks of Yore World Registration

This file contains the metadata and class references for the peaks_of_yore world.
"""

# Required metadata
WORLD_NAME = "placidplasticducksim"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PlacidPlasticDuckSimulator
WEB_WORLD_CLASS = PPDSWebWorld
CLIENT_FUNCTION = None
