from datetime import timedelta

from flask import render_template

from sqlalchemy import select, func

from Utils import utcnow
from WebHostLib import app, cache
from .models import Room, Seed, Lobby, LOBBY_OPEN, LOBBY_GENERATING, db


@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=300)  # cache has to appear under app route for caching to work
def landing():
    # The Play hub is the home page.
    return render_template("play_hub.html")


@app.route('/about')
@cache.cached(timeout=300)
def about():
    return render_template("about.html")


@cache.memoize(timeout=300)
def _footer_stats() -> dict:
    """7-day rooms/seeds/open-lobbies counts shown in the site footer.

    Memoized so high page volume hits the database at most once per timeout.
    Any failure degrades to zeros rather than 500-ing every page.
    """
    try:
        cutoff = utcnow() - timedelta(days=7)
        return {
            "seeds": db.session.scalar(
                select(func.count()).select_from(Seed).where(Seed.creation_time >= cutoff)
            ) or 0,
            "rooms": db.session.scalar(
                select(func.count()).select_from(Room).where(Room.creation_time >= cutoff)
            ) or 0,
            "open_lobbies": db.session.scalar(
                select(func.count()).select_from(Lobby)
                .where(Lobby.state.in_([LOBBY_OPEN, LOBBY_GENERATING]))
            ) or 0,
        }
    except Exception:
        return {"seeds": 0, "rooms": 0, "open_lobbies": 0}


@app.context_processor
def inject_footer_stats() -> dict:
    return {"footer_stats": _footer_stats()}
