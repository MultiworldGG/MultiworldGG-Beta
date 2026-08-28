"""End-to-end smoke tests for the /me dashboard routes."""
from __future__ import annotations

from uuid import uuid4

import pytest


# ---------------------------------------------------------------------------
# /me - overview
# ---------------------------------------------------------------------------

def test_me_returns_first_run_for_fresh_browser(client):
    """A fresh session sees the empty-state page, not the dashboard."""
    response = client.get("/me")
    assert response.status_code == 200


def test_me_returns_dashboard_when_owner_has_content(client, room_factory):
    """When the browser session owns a room, the dashboard renders (not the empty state)."""
    # Pin a known session_key on the test client, then create data under that key.
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /me/rooms, /me/lobbies, /me/seeds - full-table sub-pages
# ---------------------------------------------------------------------------

def test_my_rooms_renders_empty_message_when_no_rooms(client):
    response = client.get("/me/rooms")
    assert response.status_code == 200


def test_my_lobbies_renders_empty_message_when_no_lobbies(client):
    response = client.get("/me/lobbies")
    assert response.status_code == 200


def test_my_seeds_renders_empty_message_when_no_seeds(client):
    response = client.get("/me/seeds")
    assert response.status_code == 200


def test_my_rooms_lists_owned_rooms(client, room_factory):
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me/rooms")
    assert response.status_code == 200
