from . import SavingPrincessWorld, SavingPrincessWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
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
