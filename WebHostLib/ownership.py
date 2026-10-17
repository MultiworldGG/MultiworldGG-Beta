"""Co-ownership helpers for rooms and lobbies.

The .owner UUID on Room/Lobby is the *primary owner* - invites, co-owner
removal, and disowning all require it. Anyone listed in the
``room_co_owner`` / ``lobby_co_owner`` table is a co-owner and may perform
all other authorised actions (play, manage settings, kick, server commands).

Usage at call sites::

    from .ownership import is_authorized, is_primary_owner

    if not is_authorized(room, session["_id"]):
        abort(403)

    if not is_primary_owner(lobby, session["_id"]):
        abort(403, "only the primary owner may do that")
"""
from __future__ import annotations

from typing import Iterable, List
from uuid import UUID

from sqlalchemy import select

from .models import (
    Lobby,
    LobbyCoOwner,
    LOBBY_CLOSED,
    OwnershipInvite,
    Room,
    RoomCoOwner,
    UNOWNED,
    db,
)


def is_primary_owner(record, session_id: UUID) -> bool:
    """True iff session_id is the .owner column on this record.

    Required for invite-mint, transfer, co-owner removal, and disown.
    """
    return record.owner == session_id


def is_authorized(record, session_id: UUID) -> bool:
    """True iff session_id is the primary owner OR a co-owner.

    Use this for every "can this session interact with this room/lobby"
    check that isn't specifically a primary-only operation.
    """
    if record.owner == session_id:
        return True
    if isinstance(record, Room):
        co_table = RoomCoOwner
        target_col = RoomCoOwner.room_id
    elif isinstance(record, Lobby):
        co_table = LobbyCoOwner
        target_col = LobbyCoOwner.lobby_id
    else:
        return False
    return db.session.scalar(
        select(co_table.session_id).where(
            target_col == record.id,
            co_table.session_id == session_id,
        ).limit(1)
    ) is not None


def list_co_owners(record) -> List[UUID]:
    """All co-owner session UUIDs for a room or lobby (excludes primary)."""
    if isinstance(record, Room):
        rows = db.session.scalars(
            select(RoomCoOwner.session_id).where(RoomCoOwner.room_id == record.id)
        ).all()
    elif isinstance(record, Lobby):
        rows = db.session.scalars(
            select(LobbyCoOwner.session_id).where(LobbyCoOwner.lobby_id == record.id)
        ).all()
    else:
        return []
    return list(rows)


def list_authorized_rooms(session_id: UUID) -> List[Room]:
    """All rooms where session_id is primary OR co-owner.

    Order: primary-owned first (by last_activity desc), then co-owned.
    Used by /me dashboard and /me/rooms.
    """
    primary = db.session.scalars(
        select(Room).where(Room.owner == session_id).order_by(Room.last_activity.desc())
    ).all()
    co_owned = db.session.scalars(
        select(Room)
        .join(RoomCoOwner, RoomCoOwner.room_id == Room.id)
        .where(RoomCoOwner.session_id == session_id)
        .order_by(Room.last_activity.desc())
    ).all()
    return _dedupe_by_id(primary, co_owned)


def list_authorized_lobbies(session_id: UUID, *, include_closed: bool = False) -> List[Lobby]:
    """All lobbies where session_id is primary OR co-owner.

    By default excludes closed lobbies - matches the legacy /me filter.
    """
    primary = db.session.scalars(
        select(Lobby).where(Lobby.owner == session_id).order_by(Lobby.last_activity.desc())
    ).all()
    co_owned = db.session.scalars(
        select(Lobby)
        .join(LobbyCoOwner, LobbyCoOwner.lobby_id == Lobby.id)
        .where(LobbyCoOwner.session_id == session_id)
        .order_by(Lobby.last_activity.desc())
    ).all()
    merged = _dedupe_by_id(primary, co_owned)
    if not include_closed:
        merged = [l for l in merged if l.state != LOBBY_CLOSED]
    return merged


def release(record, session_id: UUID) -> bool:
    """Drop session_id's ownership of a room, lobby or seed; the caller commits.

    A co-owner loses its co-owner row. A primary owner revokes its pending
    invites, then hands the record to the longest-standing co-owner or, with
    none left, marks it for deletion by setting the owner to UNOWNED.

    Returns:
        True if the record is now marked for deletion.
    """
    if isinstance(record, Room):
        co_table, target_col = RoomCoOwner, RoomCoOwner.room_id
    elif isinstance(record, Lobby):
        co_table, target_col = LobbyCoOwner, LobbyCoOwner.lobby_id
    else:
        co_table = target_col = None

    if record.owner != session_id:
        row = db.session.get(co_table, (record.id, session_id)) if co_table else None
        if row is not None:
            db.session.delete(row)
        return False

    if co_table:
        for invite in db.session.scalars(select(OwnershipInvite).where(
            OwnershipInvite.target_id == record.id, OwnershipInvite.consumed_at.is_(None),
        )):
            db.session.delete(invite)
    successor = db.session.scalars(
        select(co_table).where(target_col == record.id).order_by(co_table.granted_at).limit(1)
    ).first() if co_table else None
    if successor is None:
        record.owner = UNOWNED
        return True
    record.owner = successor.session_id
    db.session.delete(successor)
    return False


def _dedupe_by_id(*sequences: Iterable) -> list:
    seen: set = set()
    out: list = []
    for seq in sequences:
        for item in seq:
            if item.id in seen:
                continue
            seen.add(item.id)
            out.append(item)
    return out
