from .world import APQuestWorld
from .web_world import APQuestWebWorld

"""
APQuest World Registration

This file contains the metadata and class references for the apquest world.
"""

# Required metadata
WORLD_NAME = "apquest"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = APQuestWorld
WEB_WORLD_CLASS = APQuestWebWorld
CLIENT_FUNCTION = None
