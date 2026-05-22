"""Smoke tests for the Phase 7 /play and /learn hub pages."""
from __future__ import annotations


def test_play_hub_renders(client):
    response = client.get("/play")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "What do you want to do?" in body          # hub heading
    assert "Browse lobbies" in body
    assert "Create a lobby" in body
    assert "Generate a new game" in body
    assert "Host a pre-generated game" in body
    assert "Validate YAML" in body
    assert "Your saved stuff" in body


def test_learn_hub_renders(client):
    response = client.get("/learn")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Learn MultiworldGG" in body               # hub heading
    assert "Setup tutorials" in body
    assert "FAQ" in body
    assert "Glossary" in body


def test_tutorial_landing_renders(client):
    response = client.get("/learn/tutorials")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # The legacy tutorial-list page has this heading.
    assert "MultiworldGG Guides" in body


def test_tutorial_legacy_redirect_lands_on_tutorial_landing(client):
    response = client.get("/tutorial", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/tutorials")
