from . import BanjoTooieWorld, BanjoTooieWeb
from .BTClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective. World Registration

This file contains the metadata and class references for the banjo_tooie world.
"""

# Required metadata
WORLD_NAME = "banjo_tooie"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BanjoTooieWorld
WEB_WORLD_CLASS = BanjoTooieWeb
CLIENT_FUNCTION = launch
