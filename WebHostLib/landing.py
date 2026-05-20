from datetime import timedelta

from flask import render_template
from sqlalchemy import select, func

from Utils import utcnow
from WebHostLib import app, cache
from .models import Room, Seed, Lobby, LOBBY_OPEN, LOBBY_GENERATING, db


@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=300)  # cache has to appear under app route for caching to work
def landing():
    cutoff = utcnow() - timedelta(days=7)
    rooms = db.session.scalar(
        select(func.count()).select_from(Room).where(Room.creation_time >= cutoff)
    ) or 0
    seeds = db.session.scalar(
        select(func.count()).select_from(Seed).where(Seed.creation_time >= cutoff)
    ) or 0
    open_lobbies = db.session.scalar(
        select(func.count()).select_from(Lobby)
        .where(Lobby.state.in_([LOBBY_OPEN, LOBBY_GENERATING]))
    ) or 0
    return render_template("landing.html", rooms=rooms, seeds=seeds, open_lobbies=open_lobbies)
