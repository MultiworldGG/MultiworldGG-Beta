"""SQLAlchemy 2.x data model definitions for the MultiworldGG webhost.

Previously backed by pony.orm; migrated to SQLAlchemy 2.x + flask-sqlalchemy.
The on-disk schema (column names, types, constraints) is preserved so that
existing SQLite/PostgreSQL databases are readable without any DDL migration.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean, DateTime, Integer, LargeBinary, String, Text, UUID as SA_UUID,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, deferred

from Utils import utcnow


# ---------------------------------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Base class that adds pony-compatible .get() classmethod and auto-add on __init__."""

    # Entity classes use legacy `attr: T = mapped_column(...)` annotations rather
    # than `attr: Mapped[T] = mapped_column(...)`. This opt-in tells SQLAlchemy's
    # Annotated Declarative form to ignore those and rely on mapped_column for
    # type inference. See https://sqlalche.me/e/20/zlpr.
    __allow_unmapped__ = True

    @classmethod
    def get(cls, **kwargs):
        """Fetch a single instance matching all keyword filters, or None.

        Mirrors pony's Entity.get(field=value, ...).
        For primary-key lookups prefers Session.get() for identity-map hits.
        """
        from sqlalchemy import select as _select
        session = _get_session()
        # Fast path: single PK column named 'id' or 'token' or 'checksum'
        pk_cols = [c.key for c in cls.__table__.primary_key.columns]
        if len(pk_cols) == 1 and pk_cols[0] in kwargs and len(kwargs) == 1:
            return session.get(cls, kwargs[pk_cols[0]])
        stmt = _select(cls)
        for attr, value in kwargs.items():
            col = getattr(cls, attr)
            stmt = stmt.where(col == value)
        return session.scalars(stmt.limit(1)).first()

    def delete(self) -> None:
        """Delete this instance from the session (mirrors pony's entity.delete())."""
        _get_session().delete(self)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__ if "__init__" in cls.__dict__ else None

        def _auto_add_init(self, *args, **kw):
            if original_init is not None:
                original_init(self, *args, **kw)
            else:
                super(cls, self).__init__(*args, **kw)
            # Auto-add to session so callers don't need an explicit session.add()
            try:
                session = _get_session()
                session.add(self)
            except RuntimeError:
                # Outside application context — caller must manage session manually
                pass

        # Only patch if not already patched (avoid double-patching on reimport)
        if getattr(cls.__init__, "_auto_add_patched", False):
            return
        _auto_add_init._auto_add_patched = True
        cls.__init__ = _auto_add_init


db = SQLAlchemy(model_class=Base)

# ---------------------------------------------------------------------------
# Lobby state constants (unchanged from pony version)
# ---------------------------------------------------------------------------

STATE_QUEUED = 0
STATE_STARTED = 1
STATE_ERROR = -1

LOBBY_OPEN = 0
LOBBY_GENERATING = 1
LOBBY_DONE = 2
LOBBY_CLOSED = -1
LOBBY_LOCKED = 3


# ---------------------------------------------------------------------------
# Entity models
# ---------------------------------------------------------------------------

class Slot(Base):
    __tablename__ = "slot"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: int = mapped_column(Integer, nullable=False)
    player_name: str = mapped_column(String, nullable=False)
    # lazy=True equivalent: deferred — not loaded unless accessed
    data: bytes | None = deferred(mapped_column("data", LargeBinary, nullable=True))
    seed_id: UUID | None = mapped_column(SA_UUID(as_uuid=True), ForeignKey("seed.id"), nullable=True, index=True)
    game: str = mapped_column(String, nullable=False, index=True)

    seed: "Seed | None" = relationship("Seed", back_populates="slots")


class Room(Base):
    __tablename__ = "room"

    id: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    last_activity: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    creation_time: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    owner: UUID = mapped_column(SA_UUID(as_uuid=True), nullable=False, index=True)
    seed_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("seed.id"), nullable=False, index=True)
    # lazy=True equivalent
    multisave: bytes | None = deferred(mapped_column("multisave", LargeBinary, nullable=True))
    show_spoiler: int = mapped_column(Integer, nullable=False, default=0)
    timeout: int = mapped_column(Integer, nullable=False, default=lambda: 4 * 60 * 60)
    tracker: UUID | None = mapped_column(SA_UUID(as_uuid=True), nullable=True, index=True)
    last_port: int = mapped_column(Integer, nullable=True, default=0)

    seed: "Seed" = relationship("Seed", back_populates="rooms")
    commands: list["Command"] = relationship(
        "Command", back_populates="room", cascade="all, delete-orphan"
    )
    # back-reference from Lobby.room
    lobby: "Lobby | None" = relationship("Lobby", back_populates="room", uselist=False)


class Seed(Base):
    __tablename__ = "seed"

    id: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    # lazy=True equivalent
    multidata: bytes = deferred(mapped_column("multidata", LargeBinary, nullable=False))
    owner: UUID = mapped_column(SA_UUID(as_uuid=True), nullable=False, index=True)
    creation_time: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    spoiler: str | None = deferred(mapped_column("spoiler", Text, nullable=True))
    meta: str = mapped_column(Text, nullable=False, default=lambda: '{"race": false}')

    rooms: list[Room] = relationship("Room", back_populates="seed", cascade="all, delete-orphan")
    slots: list[Slot] = relationship("Slot", back_populates="seed", cascade="all, delete-orphan")
    lobbies: list["Lobby"] = relationship("Lobby", back_populates="seed")


class Command(Base):
    __tablename__ = "command"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("room.id"), nullable=False)
    commandtext: str = mapped_column(String, nullable=False)

    room: Room = relationship("Room", back_populates="commands")


class Generation(Base):
    __tablename__ = "generation"

    id: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner: UUID = mapped_column(SA_UUID(as_uuid=True), nullable=False)
    # lazy=True equivalent
    options: bytes = deferred(mapped_column("options", LargeBinary, nullable=False))
    meta: str = mapped_column(Text, nullable=False, default=lambda: '{"race": false}')
    state: int = mapped_column(Integer, nullable=False, default=0, index=True)


class GameDataPackage(Base):
    __tablename__ = "gamedatapackage"

    checksum: str = mapped_column(String, primary_key=True)
    data: bytes = mapped_column(LargeBinary, nullable=False)


class Lobby(Base):
    __tablename__ = "lobby"

    id: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: str = mapped_column(String, nullable=False)
    owner: UUID = mapped_column(SA_UUID(as_uuid=True), nullable=False, index=True)
    password_hash: str | None = mapped_column(String, nullable=True)
    creation_time: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    last_activity: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    timeout_minutes: int = mapped_column(Integer, nullable=False, default=60)
    max_yamls_per_player: int = mapped_column(Integer, nullable=False, default=1)
    race: bool = mapped_column(Boolean, nullable=False, default=False)
    meta: str = mapped_column(Text, nullable=False, default=lambda: "{}")
    state: int = mapped_column(Integer, nullable=False, default=0, index=True)
    max_players: int = mapped_column(Integer, nullable=False, default=0)
    allow_custom_apworlds: bool = mapped_column(Boolean, nullable=False, default=False)
    seed_id: UUID | None = mapped_column(SA_UUID(as_uuid=True), ForeignKey("seed.id"), nullable=True)
    room_id: UUID | None = mapped_column(SA_UUID(as_uuid=True), ForeignKey("room.id"), nullable=True)
    generation_id: UUID | None = mapped_column(SA_UUID(as_uuid=True), nullable=True)

    seed: Seed | None = relationship("Seed", back_populates="lobbies")
    room: Room | None = relationship("Room", back_populates="lobby")
    players: list["LobbyPlayer"] = relationship(
        "LobbyPlayer", back_populates="lobby", cascade="all, delete-orphan"
    )
    messages: list["LobbyMessage"] = relationship(
        "LobbyMessage", back_populates="lobby", cascade="all, delete-orphan"
    )
    yamls: list["LobbyYaml"] = relationship(
        "LobbyYaml", back_populates="lobby", cascade="all, delete-orphan"
    )
    apworlds: list["LobbyApworld"] = relationship(
        "LobbyApworld", back_populates="lobby", cascade="all, delete-orphan"
    )
    apworld_requests: list["LobbyApworldRequest"] = relationship(
        "LobbyApworldRequest", back_populates="lobby", cascade="all, delete-orphan"
    )


class LobbyPlayer(Base):
    __tablename__ = "lobbyplayer"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    lobby_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False, index=True)
    session_id: UUID = mapped_column(SA_UUID(as_uuid=True), nullable=False, index=True)
    player_name: str = mapped_column(String, nullable=False)
    joined_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow)
    is_ready: bool = mapped_column(Boolean, nullable=False, default=False)

    lobby: Lobby = relationship("Lobby", back_populates="players")
    yamls: list["LobbyYaml"] = relationship(
        "LobbyYaml", back_populates="player", cascade="all, delete-orphan"
    )
    messages: list["LobbyMessage"] = relationship(
        "LobbyMessage", back_populates="player"
    )
    apworld_requests: list["LobbyApworldRequest"] = relationship(
        "LobbyApworldRequest", back_populates="requester", cascade="all, delete-orphan"
    )


class LobbyYaml(Base):
    __tablename__ = "lobbyyaml"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    lobby_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False, index=True)
    player_id: int = mapped_column(Integer, ForeignKey("lobbyplayer.id"), nullable=False, index=True)
    filename: str = mapped_column(String, nullable=False)
    yaml_player_name: str | None = mapped_column(String, nullable=True)
    yaml_game: str | None = mapped_column(String, nullable=True)
    is_custom: bool = mapped_column(Boolean, nullable=False, default=False)
    requires_game_version: str | None = mapped_column(String, nullable=True)
    # lazy=True equivalent
    content: bytes = deferred(mapped_column("content", LargeBinary, nullable=False))
    uploaded_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow)
    apworld_id: int | None = mapped_column(Integer, ForeignKey("lobbyapworld.id"), nullable=True)

    lobby: Lobby = relationship("Lobby", back_populates="yamls")
    player: LobbyPlayer = relationship("LobbyPlayer", back_populates="yamls")
    # Many-to-one: this yaml points at one apworld entry (independent FK, no back_populates)
    apworld: "LobbyApworld | None" = relationship(
        "LobbyApworld", foreign_keys=[apworld_id]
    )
    apworld_requests: list["LobbyApworldRequest"] = relationship(
        "LobbyApworldRequest", back_populates="yaml", cascade="all, delete-orphan"
    )


class LobbyApworld(Base):
    __tablename__ = "lobbyapworld"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    lobby_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False, index=True)
    yaml_id: int = mapped_column(Integer, ForeignKey("lobbyyaml.id"), nullable=False)
    game_name: str = mapped_column(String, nullable=False, index=True)
    original_filename: str = mapped_column(String, nullable=False)
    storage_path: str = mapped_column(String, nullable=False)
    file_size: int = mapped_column(Integer, nullable=False, default=0)
    world_version: str | None = mapped_column(String, nullable=True)
    uploaded_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow)

    lobby: Lobby = relationship("Lobby", back_populates="apworlds")
    # Many-to-one: this apworld entry points at one yaml (independent FK, no back_populates)
    yaml: LobbyYaml = relationship(
        "LobbyYaml", foreign_keys=[yaml_id]
    )


class LobbyApworldRequest(Base):
    __tablename__ = "lobbyapworldrequest"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    lobby_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False, index=True)
    yaml_id: int = mapped_column(Integer, ForeignKey("lobbyyaml.id"), nullable=False, index=True)
    requester_id: int = mapped_column(Integer, ForeignKey("lobbyplayer.id"), nullable=False, index=True)
    game_name: str = mapped_column(String, nullable=False, index=True)
    original_filename: str = mapped_column(String, nullable=False)
    storage_path: str = mapped_column(String, nullable=False)
    file_size: int = mapped_column(Integer, nullable=False, default=0)
    world_version: str | None = mapped_column(String, nullable=True)
    submitted_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow)

    lobby: Lobby = relationship("Lobby", back_populates="apworld_requests")
    yaml: LobbyYaml = relationship("LobbyYaml", back_populates="apworld_requests")
    requester: LobbyPlayer = relationship("LobbyPlayer", back_populates="apworld_requests")


class LobbyMessage(Base):
    __tablename__ = "lobbymessage"

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    lobby_id: UUID = mapped_column(SA_UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False, index=True)
    player_id: int | None = mapped_column(Integer, ForeignKey("lobbyplayer.id"), nullable=True)
    sender_name: str = mapped_column(String, nullable=False)
    content: str = mapped_column(Text, nullable=False)
    sent_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow)

    lobby: Lobby = relationship("Lobby", back_populates="messages")
    player: LobbyPlayer | None = relationship("LobbyPlayer", back_populates="messages")


class AvatarToken(Base):
    __tablename__ = "avatartoken"

    token: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)
    last_used_at: datetime | None = mapped_column(DateTime, nullable=True)
    revoked: bool = mapped_column(Boolean, nullable=False, default=False)
    note: str | None = mapped_column(String, nullable=True)

    avatars: list["Avatar"] = relationship(
        "Avatar", back_populates="owner_token", cascade="all, delete-orphan"
    )


class Avatar(Base):
    __tablename__ = "avatar"

    id: UUID = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_token_id: UUID = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("avatartoken.token"), nullable=False, index=True
    )
    mime_type: str = mapped_column(String, nullable=False)
    file_size: int = mapped_column(Integer, nullable=False)
    original_sha256: str = mapped_column(String, nullable=False, index=True)
    created_at: datetime = mapped_column(DateTime, nullable=False, default=utcnow, index=True)

    owner_token: AvatarToken = relationship("AvatarToken", back_populates="avatars")


# ---------------------------------------------------------------------------
# Pony-compatible shim layer
# ---------------------------------------------------------------------------
# The routes use a pony-style API: Entity.get(...), Entity(...) to create,
# select(x for x in E ...), commit(), flush(), etc.
# Rather than rewriting every callsite, we provide thin shims here that
# delegate to db.session (the flask-sqlalchemy scoped session).
#
# IMPORTANT: This shim is ONLY valid inside a Flask request context, which
# is where flask-sqlalchemy's session is bound. Non-request code (CLI,
# autolauncher, customserver) must use explicit session management — see
# those files for their own `with Session(engine) as session:` patterns.
# ---------------------------------------------------------------------------

def _get_session():
    """Return the current flask-sqlalchemy session."""
    return db.session


def commit():
    """Commit the current SQLAlchemy session."""
    _get_session().commit()


def flush():
    """Flush pending changes to the database without committing."""
    _get_session().flush()


def rollback():
    """Roll back the current SQLAlchemy session."""
    _get_session().rollback()


# ---------------------------------------------------------------------------
# QueryProxy — wraps a SQLAlchemy Select query with pony-like methods
# ---------------------------------------------------------------------------

class QueryProxy:
    """Thin wrapper around a SQLAlchemy scalars result to mimic pony's query API."""

    def __init__(self, stmt, session=None, scalar=False):
        self._stmt = stmt
        self._session = session or _get_session()
        self._scalar = scalar  # True if query returns single-column scalars

    # --- terminal methods ---

    def __iter__(self):
        return iter(self._session.scalars(self._stmt).all())

    def __getitem__(self, item):
        """Support [:] and [n:m] slicing."""
        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            if step is not None:
                raise ValueError("Step slices not supported in QueryProxy")
            stmt = self._stmt
            if start:
                stmt = stmt.offset(start)
            if stop is not None:
                limit = stop if start is None else stop - (start or 0)
                stmt = stmt.limit(limit)
            return self._session.scalars(stmt).all()
        raise TypeError(f"QueryProxy indices must be slices, not {type(item).__name__}")

    def all(self):
        return self._session.scalars(self._stmt).all()

    def first(self):
        from sqlalchemy import select as sa_select
        # Add LIMIT 1 if not already there
        stmt = self._stmt.limit(1)
        return self._session.scalars(stmt).first()

    def count(self):
        from sqlalchemy import func, select as sa_select
        count_stmt = sa_select(func.count()).select_from(self._stmt.subquery())
        return self._session.scalar(count_stmt)

    def exists(self):
        from sqlalchemy import exists as sa_exists, select as sa_select
        stmt = sa_select(sa_exists(self._stmt))
        return self._session.scalar(stmt)

    def delete(self, bulk=False):
        """Delete all matching rows."""
        objs = self._session.scalars(self._stmt).all()
        count = len(objs)
        for obj in objs:
            self._session.delete(obj)
        return count

    def order_by(self, *cols):
        return QueryProxy(self._stmt.order_by(*cols), self._session, self._scalar)

    def limit(self, n):
        return QueryProxy(self._stmt.limit(n), self._session, self._scalar)

    def offset(self, n):
        return QueryProxy(self._stmt.offset(n), self._session, self._scalar)

    def for_update(self):
        return QueryProxy(self._stmt.with_for_update(), self._session, self._scalar)

    def __bool__(self):
        return self.exists()


# ---------------------------------------------------------------------------
# Public exports for backward compatibility
# ---------------------------------------------------------------------------
# Re-export uuid4 so callers that import from .models get it
__all__ = [
    "db", "Base",
    "Slot", "Room", "Seed", "Command", "Generation", "GameDataPackage",
    "Lobby", "LobbyPlayer", "LobbyYaml", "LobbyApworld", "LobbyApworldRequest",
    "LobbyMessage", "AvatarToken", "Avatar",
    "STATE_QUEUED", "STATE_STARTED", "STATE_ERROR",
    "LOBBY_OPEN", "LOBBY_GENERATING", "LOBBY_DONE", "LOBBY_CLOSED", "LOBBY_LOCKED",
    "commit", "flush", "rollback",
    "UUID", "uuid4",
]
