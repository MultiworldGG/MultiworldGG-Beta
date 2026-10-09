"""API endpoints package."""
from typing import List, Tuple

from flask import Blueprint
from flask_cors import CORS

from ..models import Seed

api_endpoints = Blueprint('api', __name__, url_prefix="/api")
cors = CORS(api_endpoints, resources={
                r"/api/datapackage/*": {"origins": "*"},
                r"/api/datapackage": {"origins": "*"},
                r"/api/datapackage_checksum/*": {"origins": "*"},
                r"/api/room_status/*": {"origins": "*"},
                r"/api/tracker/*": {"origins": "*"},
                r"/api/static_tracker/*": {"origins": "*"},
                r"/api/slot_data_tracker/*": {"origins": "*"},
                r"/api/sphere_tracker/*": {"origins": "*"}
            })


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in sorted(seed.slots, key=lambda slot: slot.player_id)]

# trigger endpoint registration
from . import datapackage, generate, lobby, monitoring, room, tracker, user, sphere_tracker, avatar
