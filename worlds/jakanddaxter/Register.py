from . import JakAndDaxterWorld, JakAndDaxterWebWorld
from .client import launch

"""
Jak and Daxter: The Precursor Legacy World Registration

This file contains the metadata and class references for the jakanddaxter world.
"""

# Required metadata
WORLD_NAME = "jakanddaxter"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = JakAndDaxterWorld
WEB_WORLD_CLASS = JakAndDaxterWebWorld
CLIENT_FUNCTION = launch
