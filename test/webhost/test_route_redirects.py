"""
Tests for ``WebHostLib.route_redirects``.

Every URL the site exposed before the route migration must continue to
return a 301 to the corresponding new path. These tests are the contract.

The ``client``, ``room_factory``, and ``lobby_factory`` fixtures live in
``test/webhost/conftest.py``.
"""

from uuid import uuid4

import pytest


def _suuid():
    """Generate a real short-UUID string for parameterized routes."""
    from WebHostLib import to_url
    return to_url(uuid4())


# ---------------------------------------------------------------------------
# Static path redirects
# ---------------------------------------------------------------------------

STATIC_REDIRECTS = [
    ("/start-playing",   "/play"),
    ("/generate",        "/play/new"),
    ("/uploads",         "/play/host"),
    ("/check",           "/play/validate"),
    ("/lobbies",         "/play/lobbies"),
    ("/user-content",    "/me"),
    ("/tutorial",        "/learn/tutorials"),
]


@pytest.mark.parametrize("old_path, expected_new_path", STATIC_REDIRECTS)
def test_static_redirect_returns_301(client, old_path, expected_new_path):
    """Each renamed page returns a 301 with the right Location header."""
    response = client.get(old_path, follow_redirects=False)
    assert response.status_code == 301, (
        f"Expected 301 from {old_path}, got {response.status_code}"
    )
    assert response.headers["Location"].endswith(expected_new_path), (
        f"Expected redirect target {expected_new_path}, "
        f"got {response.headers['Location']}"
    )


@pytest.mark.parametrize("old_path, expected_new_path", STATIC_REDIRECTS)
def test_static_redirect_lands_on_real_page(client, old_path, expected_new_path):
    """Following the redirect actually reaches a working page."""
    response = client.get(old_path, follow_redirects=True)
    assert response.status_code == 200, (
        f"Following {old_path} -> {expected_new_path} returned "
        f"{response.status_code}"
    )


# ---------------------------------------------------------------------------
# Parameterized path redirects
# ---------------------------------------------------------------------------

def test_legacy_lobby_redirects_to_play_lobby(client):
    lobby = _suuid()
    response = client.get(f"/lobby/{lobby}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith(f"/play/lobby/{lobby}")


def test_legacy_seed_redirects_to_play_seed(client):
    seed = _suuid()
    response = client.get(f"/seed/{seed}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith(f"/play/seed/{seed}")


def test_legacy_room_redirects_to_canonical_with_seed(client, room_factory):
    """
    The old /room/<id> redirect has to look up the seed because the new
    canonical URL is /play/seed/<seed>/room/<id>.
    """
    from WebHostLib import to_url
    room = room_factory()
    response = client.get(f"/room/{to_url(room.id)}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith(
        f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
    )


def test_legacy_room_404s_when_room_missing(client):
    """Old /room/<id> for a deleted room must 404, not 301 to a bad URL."""
    response = client.get(f"/room/{_suuid()}", follow_redirects=False)
    assert response.status_code == 404


def test_legacy_faq_with_trailing_slash(client):
    """The old /faq/en/ (with trailing slash, the wart) 301s to /learn/en/faq."""
    response = client.get("/faq/en/", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/en/faq")


def test_legacy_faq_without_trailing_slash(client):
    response = client.get("/faq/en", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/en/faq")


def test_legacy_glossary(client):
    response = client.get("/glossary/en", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/learn/en/glossary")


def test_legacy_game_info(client):
    response = client.get("/games/info/Kingdom Hearts 2", follow_redirects=False)
    assert response.status_code == 301
    assert "/games/Kingdom%20Hearts%202" in response.headers["Location"]


# ---------------------------------------------------------------------------
# Tutorial: language-suffix peeling
# ---------------------------------------------------------------------------

class TestLegacyTutorial:
    """Old tutorial URLs encoded language as a filename suffix: ``setup_en``.

    The redirect peels off the suffix and surfaces the language as a path
    segment under ``/learn/<lang>/tutorial/<game>/<file>``.
    """

    def test_extracts_language_suffix(self, client):
        response = client.get(
            "/tutorial/Archipelago/setup_en", follow_redirects=False
        )
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            "/learn/en/tutorial/Archipelago/setup"
        )

    def test_defaults_to_en_when_no_suffix(self, client):
        response = client.get(
            "/tutorial/Archipelago/commands", follow_redirects=False
        )
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            "/learn/en/tutorial/Archipelago/commands"
        )

    def test_handles_non_language_underscore(self, client):
        """``advanced_settings_en`` should split on the rightmost ``_``
        (rpartition), peel ``en`` as lang, and keep ``advanced_settings``
        as the file base.
        """
        response = client.get(
            "/tutorial/Archipelago/advanced_settings_en",
            follow_redirects=False,
        )
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            "/learn/en/tutorial/Archipelago/advanced_settings"
        )

    def test_trailing_lang_redirects_directly_to_canonical(self, client):
        """``/tutorial/<game>/<file>/<lang>`` 301s straight to the new
        canonical URL — no double-hop through the suffix form.
        """
        response = client.get(
            "/tutorial/Archipelago/setup/en", follow_redirects=False,
        )
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            "/learn/en/tutorial/Archipelago/setup"
        )

    def test_trailing_lang_preserves_lang_segment(self, client):
        """Non-default lang in the trailing form survives the redirect."""
        response = client.get(
            "/tutorial/Archipelago/setup/fr", follow_redirects=False,
        )
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            "/learn/fr/tutorial/Archipelago/setup"
        )


# ---------------------------------------------------------------------------
# New routes — sanity checks that they exist
# ---------------------------------------------------------------------------

# /me/seeds, /me/rooms, /me/lobbies are new pages explicitly out of Phase 1
# scope (prompt: "Don't create the new /me dashboard page").
NEW_ROUTES_THAT_SHOULD_EXIST = [
    "/",
    "/about",
    "/play",
    "/play/new",
    "/play/host",
    "/play/validate",
    "/play/lobbies",
    "/me",
    "/learn",
    "/learn/en/faq",
    "/learn/en/glossary",
    "/learn/en/quickstart",
    "/games",
    "/downloads",
    "/sitemap",
]


@pytest.mark.parametrize("path", NEW_ROUTES_THAT_SHOULD_EXIST)
def test_new_route_does_not_404(client, path):
    """Every new route should resolve (200 OK, or 302/200 after redirects)."""
    response = client.get(path, follow_redirects=True)
    assert response.status_code == 200, (
        f"New route {path} returned {response.status_code} "
        f"after following redirects"
    )


# ---------------------------------------------------------------------------
# Lobby-to-room shortcut
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="Phase 1 ships paths only — /play/lobby/<id>/room is a new route")
def test_lobby_to_room_redirects_when_room_exists(client, lobby_factory):
    """
    /play/lobby/<id>/room is a convenience: it 302s to the canonical
    room URL once the lobby has produced a room.
    """
    lobby = lobby_factory(with_finished_room=True)
    response = client.get(
        f"/play/lobby/{lobby.id}/room", follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        f"/play/seed/{lobby.seed_id}/room/{lobby.room.id}"
    )


@pytest.mark.skip(reason="Phase 1 ships paths only — /play/lobby/<id>/room is a new route")
def test_lobby_to_room_404s_when_no_room_yet(client, lobby_factory):
    """
    A lobby that hasn't generated yet (state 0/1) has no room. The shortcut
    should 404 rather than redirect to a placeholder.
    """
    lobby = lobby_factory(with_finished_room=False)
    response = client.get(
        f"/play/lobby/{lobby.id}/room", follow_redirects=False
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Short-share alias (Phase 2)
# ---------------------------------------------------------------------------

class TestShortRoomAlias:
    """
    /r/<short_id> is the Discord-shareable form. It 301s to the canonical
    room URL. Skipped until Phase 2 ships the short_id column.
    """

    @pytest.mark.skip(reason="Phase 2 — requires short_id column on rooms")
    def test_short_room_alias_redirects_to_canonical(self, client, room_factory):
        room = room_factory(short_id="rSiScs")
        response = client.get("/r/rSiScs", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{room.seed_id}/room/{room.id}"
        )

    @pytest.mark.skip(reason="Phase 2 — requires short_id column on rooms")
    def test_short_room_404s_when_id_unknown(self, client):
        response = client.get("/r/nopath", follow_redirects=False)
        assert response.status_code == 404
