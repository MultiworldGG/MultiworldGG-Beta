"""Data aggregation for the /me dashboard.

All queries are scoped to the current browser session. There are no
user accounts in MultiworldGG — the session key in cookies is the
identity. Rooms, seeds, and lobbies "owned by this browser" are those
where the owner UUID matches session["_id"].
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select

from Utils import utcnow
from .models import Lobby, Room, Seed, db


# Matches the filter the legacy /me handler used.
_ACTIVE_LOBBY_STATES = (0, 1, 2, 3)


@dataclass
class RoomStatus:
    """Categorized state of a room for the dashboard."""

    label: str       # "Running" | "Paused"
    pill_class: str  # CSS class suffix, e.g. mw-pill-running
    icon: str        # Material Design Icons class (see me.css @font-face block)


def classify_room(room: Room) -> RoomStatus:
    """Return a RoomStatus for the given room.

    A room is "Running" if its last activity is within its own configured
    timeout window — same threshold the autolauncher uses to decide whether
    a server is currently up. Otherwise "Paused".
    """
    last_activity = getattr(room, "last_activity", None)
    timeout_seconds = getattr(room, "timeout", 0) or 0
    if last_activity is not None and timeout_seconds > 0:
        now = utcnow()
        if now - last_activity < timedelta(seconds=timeout_seconds):
            return RoomStatus("Running", "running", "mdi-play")
    return RoomStatus("Paused", "paused", "mdi-pause")


@dataclass
class DashboardStats:
    """The four headline numbers on the dashboard."""

    active_rooms: int = 0
    active_rooms_sub: str = ""        # "2 running · 1 paused"
    open_lobbies: int = 0
    open_lobbies_sub: str = ""        # "1 open · 1 locked"
    saved_seeds: int = 0
    saved_seeds_sub: str = ""         # "4 with spoilers"
    games_tracked: int = 0
    games_tracked_sub: str = ""       # "8 unique titles"


@dataclass
class DashboardData:
    """All the data the dashboard template needs."""

    stats: DashboardStats = field(default_factory=DashboardStats)
    active_rooms: list = field(default_factory=list)  # list of (room, RoomStatus)
    my_lobbies: list = field(default_factory=list)
    recent_seeds: list = field(default_factory=list)
    total_active_rooms: int = 0
    total_lobbies: int = 0
    total_seeds: int = 0
    is_empty: bool = True


def _seed_has_spoiler(seed: Seed) -> bool:
    """Read the deferred spoiler column. Each call is one query — use sparingly."""
    return seed.spoiler is not None


def get_dashboard_data(session_key: UUID, *, max_per_section: int = 3) -> DashboardData:
    """Aggregate all data for the /me dashboard for one browser session.

    Args:
        session_key: The current browser's session identifier (UUID — matches
            the type of Room/Seed/Lobby.owner columns).
        max_per_section: How many items to show in each section (Active rooms,
            My lobbies, Recent seeds). The full counts are kept in
            ``total_*`` fields so the template can render "View all N →".

    Returns:
        DashboardData with stats and item lists populated. If the browser has
        no data, returns an empty dataclass with ``is_empty=True``.
    """
    # Rooms / lobbies include co-owned entries; seeds remain primary-owner-only.
    from .ownership import list_authorized_rooms, list_authorized_lobbies
    owned_rooms = list_authorized_rooms(session_key)
    owned_lobbies = [
        l for l in list_authorized_lobbies(session_key)
        if l.state in _ACTIVE_LOBBY_STATES
    ]
    owned_seeds = db.session.scalars(
        select(Seed).where(Seed.owner == session_key)
    ).all()

    if not owned_rooms and not owned_lobbies and not owned_seeds:
        return DashboardData(is_empty=True)

    classified = [(r, classify_room(r)) for r in owned_rooms]
    running = [r for r, s in classified if s.label == "Running"]
    paused = [r for r, s in classified if s.label == "Paused"]
    active_rooms_sorted = sorted(
        running + paused,
        key=lambda r: r.last_activity or utcnow().replace(year=1970),
        reverse=True,
    )

    open_count = sum(1 for l in owned_lobbies if l.state == 0)
    locked_count = sum(1 for l in owned_lobbies if l.state == 3)
    generating_count = sum(1 for l in owned_lobbies if l.state == 1)
    done_count = sum(1 for l in owned_lobbies if l.state == 2)

    lobby_subs = []
    if open_count:
        lobby_subs.append(f"{open_count} open")
    if generating_count:
        lobby_subs.append(f"{generating_count} generating")
    if locked_count:
        lobby_subs.append(f"{locked_count} locked")
    if done_count:
        lobby_subs.append(f"{done_count} done")

    lobbies_sorted = sorted(
        owned_lobbies,
        key=lambda l: l.last_activity,
        reverse=True,
    )

    seeds_sorted = sorted(
        owned_seeds,
        key=lambda s: s.creation_time,
        reverse=True,
    )

    # Unique game titles across all owned seeds (slots live on the seed,
    # not the room). One pass over the slot relationship per seed.
    games_set: set[str] = set()
    slot_total = 0
    for seed in owned_seeds:
        for slot in seed.slots:
            if slot.game:
                games_set.add(slot.game)
                slot_total += 1

    # Spoiler count uses a separate count query to avoid loading the deferred
    # column for every seed.
    from sqlalchemy import func
    spoiler_count = db.session.scalar(
        select(func.count())
        .select_from(Seed)
        .where(Seed.owner == session_key, Seed.spoiler.is_not(None))
    ) or 0

    active_room_subs = []
    if running:
        active_room_subs.append(f"{len(running)} running")
    if paused:
        active_room_subs.append(f"{len(paused)} paused")

    stats = DashboardStats(
        active_rooms=len(active_rooms_sorted),
        active_rooms_sub=" · ".join(active_room_subs) if active_room_subs else "None active",
        open_lobbies=len(owned_lobbies),
        open_lobbies_sub=" · ".join(lobby_subs) if lobby_subs else "None active",
        saved_seeds=len(owned_seeds),
        saved_seeds_sub=(
            f"{spoiler_count} with spoilers"
            if owned_seeds else ""
        ),
        games_tracked=len(games_set),
        games_tracked_sub=(
            f"{slot_total} player slots" if games_set else ""
        ),
    )

    return DashboardData(
        stats=stats,
        active_rooms=[
            (r, classify_room(r))
            for r in active_rooms_sorted[:max_per_section]
        ],
        my_lobbies=lobbies_sorted[:max_per_section],
        recent_seeds=seeds_sorted[:max_per_section],
        total_active_rooms=len(active_rooms_sorted),
        total_lobbies=len(owned_lobbies),
        total_seeds=len(owned_seeds),
        is_empty=False,
    )
