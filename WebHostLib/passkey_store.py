"""SQLAlchemy-backed CredentialStore for the passkey blueprint.

Implements the protocol defined in :mod:`WebHostLib.passkeys` against the
project's ``flask-sqlalchemy`` session. The store reads and writes the
``passkey_credential`` table defined on
:class:`WebHostLib.models.PasskeyCredential`.

The store needs a *callable* that returns the active session, not a session
directly — flask-sqlalchemy's session is scoped per-request and must be
resolved each time we touch the DB.
"""
from __future__ import annotations

from typing import Callable, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session as _Session

from Utils import utcnow
from .models import PasskeyCredential, commit
from .passkeys import StoredCredential


class SQLAlchemyCredentialStore:
    """CredentialStore over the project's SQLAlchemy session."""

    def __init__(self, session_factory: Callable[[], _Session]) -> None:
        self._session_factory = session_factory

    def _s(self) -> _Session:
        return self._session_factory()

    def add(self, cred: StoredCredential) -> None:
        PasskeyCredential(
            credential_id=cred.credential_id,
            public_key=cred.public_key,
            sign_count=cred.sign_count,
            session_id=cred.session_id,
        )
        commit()

    def get(self, credential_id: bytes) -> Optional[StoredCredential]:
        row = self._s().get(PasskeyCredential, credential_id)
        if row is None:
            return None
        return StoredCredential(
            credential_id=row.credential_id,
            public_key=row.public_key,
            sign_count=row.sign_count,
            session_id=row.session_id,
        )

    def update_sign_count(self, credential_id: bytes, new_count: int) -> None:
        row = self._s().get(PasskeyCredential, credential_id)
        if row is None:
            return
        row.sign_count = new_count
        row.last_used = utcnow()
        commit()

    def list_for_session(self, session_id: str) -> List[StoredCredential]:
        rows = self._s().scalars(
            select(PasskeyCredential).where(PasskeyCredential.session_id == session_id)
        ).all()
        return [
            StoredCredential(
                credential_id=r.credential_id,
                public_key=r.public_key,
                sign_count=r.sign_count,
                session_id=r.session_id,
            )
            for r in rows
        ]

    def remove(self, credential_id: bytes) -> bool:
        row = self._s().get(PasskeyCredential, credential_id)
        if row is None:
            return False
        self._s().delete(row)
        commit()
        return True
