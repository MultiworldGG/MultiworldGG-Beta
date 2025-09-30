from . import PowerwashSimulator, PowerwashSimulatorWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pokemon Mystery Dungeon Explorers of Sky World Registration

This file contains the metadata and class references for the pmd_eos world.
"""

# Required metadata
WORLD_NAME = "powerwashsimulator"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PowerwashSimulator
WEB_WORLD_CLASS = PowerwashSimulatorWebWorld
CLIENT_FUNCTION = None
