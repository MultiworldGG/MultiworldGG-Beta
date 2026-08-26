"""Smoke tests for the Phase 7 /play and /learn hub pages."""
from __future__ import annotations


def test_play_hub_renders(client):
    response = client.get("/play")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Multiworld Play" in body                  # hub heading
    assert "Click here for Setup Instructions" in body  # quickstart CTA
    assert "Lobby Home" in body
    assert "<h3>Games</h3>" in body
    assert "Generate a new game" in body
    assert "Host a pre-generated game" in body
    assert "Validate YAML" in body
    assert "Your saved stuff" in body


def test_learn_hub_renders(client):
    # /learn is a legacy 301 to the locale-prefixed canonical hub (/learn/en).
    response = client.get("/learn", follow_redirects=True)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Learn MultiworldGG" in body               # hub heading
    assert "Setup guides" in body
    assert "FAQ" in body
    assert "Glossary" in body


def test_tutorial_landing_renders(client):
    # /learn/tutorials is a legacy 301 to /learn/en/tutorials.
    response = client.get("/learn/tutorials", follow_redirects=True)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # The legacy tutorial-list page has this heading.
    assert "MultiworldGG Guides" in body


def test_tutorial_legacy_redirect_lands_on_tutorial_landing(client):
    response = client.get("/tutorial", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/en/tutorials")
