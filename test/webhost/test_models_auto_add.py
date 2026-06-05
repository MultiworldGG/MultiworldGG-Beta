"""Pins the pony-style auto-add behaviour of WebHostLib.models.Base.

Constructing any Base subclass inside a Flask app context registers the new
instance with db.session as a pending insert via the patched __init__ -- no
explicit db.session.add() call is required.
"""
from __future__ import annotations

from uuid import uuid4

import pytest


def test_constructing_entity_auto_adds_to_session(app):
    from WebHostLib.models import db, Seed

    with app.app_context():
        before = set(db.session.new)
        seed = Seed(multidata=b"", owner=uuid4())
        # No explicit db.session.add(seed) call happens anywhere above.
        new_objects = set(db.session.new)

    assert seed not in before
    assert seed in new_objects


def test_auto_added_entity_persists_on_commit_without_explicit_add(app):
    from WebHostLib.models import db, commit, Seed

    owner = uuid4()
    with app.app_context():
        seed = Seed(multidata=b"x", owner=owner)
        # Only commit() -- still never an explicit session.add().
        commit()
        seed_id = seed.id

    with app.app_context():
        fetched = Seed.get(id=seed_id)
        assert fetched is not None
        assert fetched.owner == owner
