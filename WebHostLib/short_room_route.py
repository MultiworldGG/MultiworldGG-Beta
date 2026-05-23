"""
The /r/<short> route — Discord-shareable short-URL alias for rooms.

Registered as a top-level route (not a blueprint) so its endpoint stays
``short_room`` for url_for() and test assertions. Wire up in the app
factory via::

    from WebHostLib.short_room_route import short_room
    app.add_url_rule("/r/<short>", "short_room", short_room)
"""

from flask import abort, redirect, url_for

from WebHostLib.short_id import normalize_short_id


def short_room(short):
    """301-redirect a short room URL to the canonical room page.

    Looks up the room by its ``short_id`` column. Lookups are
    case-insensitive and substitute Crockford's ambiguous characters
    (``I``/``L`` -> ``1``, ``O`` -> ``0``) so voice-shared URLs survive
    listener typos.

    The redirect is a 301 because the short->canonical mapping never
    changes once a room is created. Discord and browsers can cache
    aggressively.
    """
    from WebHostLib.models import Room

    normalized = normalize_short_id(short)

    room = Room.get(short_id=normalized)
    if not room:
        abort(404)

    return redirect(
        url_for("host_room", seed=room.seed_id, room=room.id),
        code=301,
    )
