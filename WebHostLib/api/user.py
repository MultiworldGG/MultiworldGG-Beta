from flask import session, jsonify
from sqlalchemy import select

from WebHostLib import to_url
from WebHostLib.models import Room, Seed, db
from WebHostLib.ownership import list_authorized_rooms
from . import api_endpoints, get_players


@api_endpoints.route('/get_rooms')
def get_rooms():
    response = []
    # Includes primary-owned and co-owned rooms.
    for room in list_authorized_rooms(session["_id"]):
        response.append({
            "room_id": to_url(room.id),
            "seed_id": to_url(room.seed_id),
            "creation_time": room.creation_time,
            "last_activity": room.last_activity,
            "last_port": room.last_port,
            "timeout": room.timeout,
            "tracker": to_url(room.tracker),
        })
    return jsonify(response)


@api_endpoints.route('/get_seeds')
def get_seeds():
    response = []
    for seed in db.session.scalars(select(Seed).where(Seed.owner == session["_id"])).all():
        response.append({
            "seed_id": to_url(seed.id),
            "creation_time": seed.creation_time,
            "players": get_players(seed),
        })
    return jsonify(response)
