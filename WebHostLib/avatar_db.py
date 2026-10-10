"""Avatar queries shared by the room server and the autohost.

Both run outside a request context and must not import the web routes, so these
take an explicit SQLAlchemy session.
"""
import os

from sqlalchemy import func, or_, select

from WebHostLib.models import Avatar, AvatarToken, SessionAvatar, SlotAvatar

PNG_EXTENSION = ".png"


def apply_slot_avatars_to_stored_data(session, room_id, stored_data: dict) -> None:
    """Inject web-set slot avatars into a room's ``stored_data`` profile_data.

    Called by the live room process at boot (customserver) so connected desktop
    clients render web-set avatars. Takes an explicit SQLAlchemy session because
    the room process isn't in a Flask request context, and mutates ``stored_data``
    in place. Only explicit ``SlotAvatar`` rows are seeded - lobby-derived session
    avatars stay web-only (the client carries its own via persistent storage).
    """
    rows = session.scalars(select(SlotAvatar).where(SlotAvatar.room_id == room_id)).all()
    for row in rows:
        if not row.avatar_url:
            continue
        key = f"profile_data_{row.team}_{row.slot}"
        profile = stored_data.get(key)
        profile = profile if isinstance(profile, dict) else {}
        profile["avatar"] = row.avatar_url
        stored_data[key] = profile


def prune_unreferenced_avatars(session, cutoff, upload_dir: str) -> int:
    """Delete avatars created before ``cutoff`` that nothing uses; returns the count.

    Kept: every SessionAvatar/SlotAvatar target, and a client token's newest
    upload (the desktop client persists only its latest URL). Takes an explicit
    session because the autohost runs outside a request context.
    """
    newest = (
        select(Avatar.owner_token_id, func.max(Avatar.created_at).label("created_at"))
        .group_by(Avatar.owner_token_id)
        .subquery()
    )
    stale = session.scalars(
        select(Avatar)
        .join(Avatar.owner_token)
        .join(newest, Avatar.owner_token_id == newest.c.owner_token_id)
        .where(
            Avatar.created_at < cutoff,
            or_(AvatarToken.note.is_not(None), Avatar.created_at < newest.c.created_at),
            Avatar.id.not_in(select(SessionAvatar.avatar_id)),
            Avatar.id.not_in(select(SlotAvatar.avatar_id)),
        )
    ).all()
    for avatar in stale:
        try:
            os.remove(os.path.join(upload_dir, f"{avatar.id.hex}{PNG_EXTENSION}"))
        except FileNotFoundError:
            pass
        session.delete(avatar)
    session.commit()
    return len(stale)
