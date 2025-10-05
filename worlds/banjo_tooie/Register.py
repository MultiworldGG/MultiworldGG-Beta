from . import BanjoTooieWorld, BanjoTooieWeb
from .BTClient import launch

"""
Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective. World Registration

This file contains the metadata and class references for the banjo_tooie world.
"""

# Required metadata
WORLD_NAME = "banjo_tooie"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BanjoTooieWorld
WEB_WORLD_CLASS = BanjoTooieWeb
CLIENT_FUNCTION = launch
