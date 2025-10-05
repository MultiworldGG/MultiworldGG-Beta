from . import SmsWorld, SmsWebWorld
from .SMSClient import launch

"""
Super Mario Sunshine World Registration

This file contains the metadata and class references for the sms world.
"""

# Required metadata
WORLD_NAME = "sms"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SmsWorld
WEB_WORLD_CLASS = SmsWebWorld
CLIENT_FUNCTION = launch
