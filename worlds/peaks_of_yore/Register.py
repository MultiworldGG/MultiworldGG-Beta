from . import PeaksOfWorld
from . import PeaksOfWeb

"""
Peaks of Yore World Registration

This file contains the metadata and class references for the peaks_of_yore world.
"""

# Required metadata
WORLD_NAME = "peaks_of_yore"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PeaksOfWorld
WEB_WORLD_CLASS = PeaksOfWeb
CLIENT_FUNCTION = None
