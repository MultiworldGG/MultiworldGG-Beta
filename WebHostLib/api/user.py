from uuid import UUID

from flask import abort, session, jsonify
from sqlalchemy import select

from WebHostLib import to_url
from WebHostLib.models import LOBBY_CLOSED, Lobby, Room, RoomVisit, Seed, commit, db
from WebHostLib.ownership import is_authorized, is_primary_owner, list_authorized_rooms, release
from . import api_endpoints, get_players
from .lobby import close_lobby


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


# DELETE only: a cross-site form can't send it, and /api/me/* has no CORS grant.
@api_endpoints.route('/me/rooms/<suuid:room>', methods=['DELETE'])
def remove_my_room(room: UUID):
    """Drop a room from this session's /me lists; the last owner out marks it for deletion."""
    record = Room.get(id=room)
    if record is None:
        abort(404)
    visit = db.session.get(RoomVisit, (record.id, session["_id"]))
    if visit is None and not is_authorized(record, session["_id"]):
        abort(403)
    if visit is not None:
        db.session.delete(visit)
    release(record, session["_id"])
    commit()
    return jsonify({"ok": True})


@api_endpoints.route('/me/lobbies/<suuid:lobby>', methods=['DELETE'])
def remove_my_lobby(lobby: UUID):
    """Drop a lobby from this session's /me lists; the last owner out closes it and marks it for deletion."""
    record = Lobby.get(id=lobby)
    if record is None:
        abort(404)
    if not is_authorized(record, session["_id"]):
        abort(403)
    if release(record, session["_id"]) and record.state != LOBBY_CLOSED:
        close_lobby(record)
    commit()
    return jsonify({"ok": True})


@api_endpoints.route('/me/seeds/<suuid:seed>', methods=['DELETE'])
def remove_my_seed(seed: UUID):
    """Mark a seed for deletion; rooms already made from it keep it until they go."""
    record = Seed.get(id=seed)
    if record is None:
        abort(404)
    if not is_primary_owner(record, session["_id"]):
        abort(403)
    release(record, session["_id"])
    commit()
    return jsonify({"ok": True})
