from . import SonicHeroesWorld
from . import SonicHeroesWeb

"""
Sonic Heroes is a 2003 platform game developed by Sonic Team USA. The player races a team of series characters through levels to amass rings, World Registration

This file contains the metadata and class references for the sonic_heroes world.
"""

# Required metadata
WORLD_NAME = "sonic_heroes"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SonicHeroesWorld
WEB_WORLD_CLASS = SonicHeroesWeb
CLIENT_FUNCTION = None
