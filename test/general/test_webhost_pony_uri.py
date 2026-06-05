"""Unit tests for WebHost._pony_config_to_sqlalchemy_uri.

Pins the legacy-PONY-config -> SQLAlchemy-URI mapping contract: sqlite filename
handling (including the :memory: special case), postgres/postgresql psycopg2
URIs, and the ValueError raised for unsupported providers.
"""
from __future__ import annotations

import pytest

from WebHost import _pony_config_to_sqlalchemy_uri


def test_pony_config_to_sqlalchemy_uri_sqlite_memory_postgres_and_unsupported():
    # sqlite with explicit :memory: filename is special-cased to an in-memory URI
    assert _pony_config_to_sqlalchemy_uri(
        {"provider": "sqlite", "filename": ":memory:"}
    ) == "sqlite:///:memory:"

    # sqlite with a regular filename maps to sqlite:///<filename>
    assert _pony_config_to_sqlalchemy_uri(
        {"provider": "sqlite", "filename": "ap.db3"}
    ) == "sqlite:///ap.db3"

    # provider defaults to sqlite and filename defaults to ap.db3
    assert _pony_config_to_sqlalchemy_uri({}) == "sqlite:///ap.db3"

    # both postgres and postgresql build the same psycopg2 URI
    pg_config = {
        "provider": "postgres",
        "host": "db.example",
        "port": 6543,
        "user": "u",
        "password": "p",
        "database": "mwgg",
    }
    expected = "postgresql+psycopg2://u:p@db.example:6543/mwgg"
    assert _pony_config_to_sqlalchemy_uri(pg_config) == expected
    assert _pony_config_to_sqlalchemy_uri({**pg_config, "provider": "postgresql"}) == expected

    # postgres falls back to localhost:5432 and empty credentials/database
    assert _pony_config_to_sqlalchemy_uri({"provider": "postgres"}) == \
        "postgresql+psycopg2://:@localhost:5432/"

    # an unsupported provider raises ValueError
    with pytest.raises(ValueError, match="Unsupported PONY provider"):
        _pony_config_to_sqlalchemy_uri({"provider": "mysql"})
