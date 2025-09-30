from . import SavingPrincessWorld, SavingPrincessWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
Explore a space station crawling with rogue machines and even rival bounty hunters World Registration

This file contains the metadata and class references for the saving_princess world.
"""

# Required metadata
WORLD_NAME = "saving_princess"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SavingPrincessWorld
WEB_WORLD_CLASS = SavingPrincessWeb
CLIENT_FUNCTION = launch
