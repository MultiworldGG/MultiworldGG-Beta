from . import JakAndDaxterWorld, JakAndDaxterWebWorld
from .client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Jak and Daxter: The Precursor Legacy World Registration

This file contains the metadata and class references for the jakanddaxter world.
"""

# Required metadata
WORLD_NAME = "jakanddaxter"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = JakAndDaxterWorld
WEB_WORLD_CLASS = JakAndDaxterWebWorld
CLIENT_FUNCTION = launch
