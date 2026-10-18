"""Monitoring API endpoints for active rooms and games."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from flask import jsonify, request, abort
from sqlalchemy import select

from Utils import restricted_loads, utcnow
from WebHostLib import app, to_url

from ..models import Room, Command, db, commit

from . import api_endpoints


def require_admin_token():
    """Check if admin token is required and validate it from request."""
    admin_token = app.config.get("MONITORING_ADMIN_TOKEN")
    
    # Block endpoints if no token is configured
    if not admin_token:
        abort(503)
    
    # Check for token in Authorization header (Bearer token format)
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401)
    provided_token = auth_header[7:]
    if provided_token != admin_token:
        abort(401)


def is_room_active(room: Room) -> bool:
    """Check if a room is currently active (hasn't timed out and has a valid port)."""
    # Only consider rooms with a valid port (> 0)
    if not room.last_port or room.last_port <= 0:
        return False
    now = utcnow()
    time_since_activity = now - room.last_activity
    return time_since_activity <= timedelta(seconds=room.timeout + 5)


def get_per_player_last_activity(room: Room) -> Dict[int, Optional[float]]:
    """Get the activity timestamp for each player in a room.
    Returns a dict mapping player_id to the activity timestamp (or None if no activity)."""
    player_activity: Dict[int, Optional[float]] = {}
    
    if not room.multisave:
        for slot in room.seed.slots:
            player_activity[slot.player_id] = None
        return player_activity
    
    try:
        multisave = restricted_loads(room.multisave)
        client_activity_timers = multisave.get("client_activity_timers", [])
        
        # Initialize all players to None
        for slot in room.seed.slots:
            player_activity[slot.player_id] = None
        
        # client_activity_timers is stored as tuple of ((team, player), timestamp) pairs
        # Handle both tuple and list formats
        if isinstance(client_activity_timers, (tuple, list)):
            for entry in client_activity_timers:
                if isinstance(entry, (tuple, list)) and len(entry) == 2:
                    (team, player_id), timestamp = entry
                    if player_id in player_activity:
                        if player_activity[player_id] is None or timestamp > player_activity[player_id]:
                            player_activity[player_id] = timestamp
    except Exception:
        for slot in room.seed.slots:
            player_activity[slot.player_id] = None
    
    return player_activity


@api_endpoints.route('/monitoring/rooms')
def monitoring_rooms() -> Dict[str, Any]:
    """Get a list of all active rooms with port and last activity time."""
    require_admin_token()
    if True:  # replaced with db_session; flask-sqlalchemy handles session lifecycle
        now = utcnow()
        rooms = db.session.scalars(
            select(Room).where(Room.last_activity >= now - timedelta(days=3))
        ).all()
        
        active_rooms = []
        for room in rooms:
            if is_room_active(room):
                player_activity = get_per_player_last_activity(room)
                games = []
                for slot in room.seed.slots:
                    activity_timestamp = player_activity.get(slot.player_id)
                    games.append({
                        "game": slot.game,
                        "player_id": slot.player_id,
                        "player_name": slot.player_name,
                        "last_activity_timestamp": datetime.fromtimestamp(activity_timestamp, tz=timezone.utc).isoformat() if activity_timestamp else None,
                    })
                
                active_rooms.append({
                    "room_id": str(room.id),
                    "room_id_short": to_url(room.id),
                    "port": room.last_port,
                    "last_activity_timestamp": room.last_activity.isoformat(),
                    "time_until_timeout": int(room.timeout - (now - room.last_activity).total_seconds()),
                    "games": games,
                    "player_count": len(room.seed.slots),
                    "creation_time": room.creation_time.isoformat(),
                })
        
        return jsonify({
            "active_rooms": active_rooms,
            "total_active_rooms": len(active_rooms),
            "timestamp": now.isoformat(),
        })


@api_endpoints.route('/monitoring/games')
def monitoring_games() -> Dict[str, Any]:
    """Get a list of all games with port and time of last action."""
    require_admin_token()
    if True:  # replaced with db_session; flask-sqlalchemy handles session lifecycle
        now = utcnow()
        rooms = db.session.scalars(
            select(Room).where(Room.last_activity >= now - timedelta(days=3))
        ).all()

        games_dict: Dict[str, List[Dict[str, Any]]] = {}
        
        for room in rooms:
            if not is_room_active(room):
                continue

            player_activity = get_per_player_last_activity(room)
            
            for slot in room.seed.slots:
                game = slot.game
                if game not in games_dict:
                    games_dict[game] = []
                
                activity_timestamp = player_activity.get(slot.player_id)
                
                games_dict[game].append({
                    "room_id": str(room.id),
                    "room_id_short": to_url(room.id),
                    "port": room.last_port,
                    "last_activity_timestamp": room.last_activity.isoformat(),
                    "game_last_activity_timestamp": datetime.fromtimestamp(activity_timestamp, tz=timezone.utc).isoformat() if activity_timestamp else None,
                    "player_name": slot.player_name,
                    "player_id": slot.player_id,
                    "time_until_timeout": int(room.timeout - (now - room.last_activity).total_seconds()),
                })
        
        games_list = [
            {
                "game": game,
                "active_instances": instances,
                "instance_count": len(instances),
            }
            for game, instances in sorted(games_dict.items())
        ]
        
        return jsonify({
            "games": games_list,
            "total_games": len(games_dict),
            "total_instances": sum(len(instances) for instances in games_dict.values()),
            "timestamp": now.isoformat(),
        })


@api_endpoints.route('/monitoring/broadcast', methods=['POST'])
def broadcast() -> Dict[str, Any]:
    """Send a message to all active rooms (or specific ones)."""
    require_admin_token()

    data = request.get_json()
    if not data or "message" not in data:
        abort(400, description="Message is required")

    message = data["message"]
    room_ids = data.get("rooms")  # optional

    now = utcnow()

    if room_ids:
        try:
            room_uuids = [UUID(rid) for rid in room_ids]
        except ValueError:
            abort(400, description="Invalid room ID format")

        rooms = db.session.scalars(
            select(Room).where(Room.id.in_(room_uuids))
        ).all()
    else:
        # Default to all active rooms
        candidates = db.session.scalars(
            select(Room).where(Room.last_activity >= now - timedelta(days=3))
        ).all()
        rooms = [r for r in candidates if is_room_active(r)]

    cmd_count = 0
    for room in rooms:
        Command(room_id=room.id, commandtext=message)
        cmd_count += 1
    commit()

    return jsonify({
        "message": f"Broadcast sent to {cmd_count} rooms",
        "count": cmd_count,
        "timestamp": now.isoformat(),
    })
