from . import JakAndDaxterWorld, JakAndDaxterWebWorld
from .client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Jak and Daxter: The Precursor Legacy World Registration

This file contains the metadata and class references for the jakanddaxter world.
"""

# Required metadata
WORLD_NAME = "jakanddaxter"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = JakAndDaxterWorld
WEB_WORLD_CLASS = JakAndDaxterWebWorld
CLIENT_FUNCTION = launch
