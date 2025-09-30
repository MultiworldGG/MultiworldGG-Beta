from . import SmsWorld, SmsWebWorld
from .SMSClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Super Mario Sunshine World Registration

This file contains the metadata and class references for the sms world.
"""

# Required metadata
WORLD_NAME = "sms"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SmsWorld
WEB_WORLD_CLASS = SmsWebWorld
CLIENT_FUNCTION = launch
