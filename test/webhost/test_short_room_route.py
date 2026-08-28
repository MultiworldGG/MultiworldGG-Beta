"""
Integration tests for the ``/r/<short>`` short-room route. Uses the
``client`` and ``room_factory`` fixtures from conftest.py.
"""

import pytest

from WebHostLib import to_url


@pytest.fixture(autouse=True)
def _wipe_rooms_after_test(app):
    """Hardcoded short_ids plus the session-scoped shared in-memory DB would
    trip the UNIQUE constraint across tests; wipe rows after each test."""
    yield
    from WebHostLib.models import db, Room, Seed, Command, Lobby, LobbyMessage
    with app.app_context():
        db.session.query(LobbyMessage).delete()
        db.session.query(Lobby).delete()
        db.session.query(Command).delete()
        db.session.query(Room).delete()
        db.session.query(Seed).delete()
        db.session.commit()


# ---------------------------------------------------------------------------
# Basic resolution
# ---------------------------------------------------------------------------

class TestShortRoomRedirect:
    def test_resolves_to_canonical_room_url(self, client, room_factory):
        room = room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=False)

        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )

    def test_uses_301_not_302(self, client, room_factory):
        """The short->canonical mapping never changes once created, so
        301 (permanent) is correct. Discord and browsers cache 301s
        aggressively."""
        room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=False)
        assert response.status_code == 301

    def test_following_redirect_loads_room_page(self, client, room_factory):
        """Round-trip: hit /r/, follow the redirect, get the actual
        room page."""
        room_factory(short_id="K7M3QX")
        response = client.get("/r/K7M3QX", follow_redirects=True)
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Case insensitivity (Crockford convention)
# ---------------------------------------------------------------------------

class TestCaseInsensitivity:
    @pytest.mark.parametrize("typed", [
        "K7M3QX",
        "k7m3qx",
        "K7m3Qx",
        "k7M3qX",
    ])
    def test_resolves_regardless_of_case(self, client, room_factory, typed):
        """All case variants of the canonical short_id should resolve."""
        room = room_factory(short_id="K7M3QX")
        response = client.get(f"/r/{typed}", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )


# ---------------------------------------------------------------------------
# Ambiguous character substitution
# ---------------------------------------------------------------------------

class TestAmbiguousChars:
    """Crockford convention: I/L -> 1, O -> 0. Voice-shared codes survive
    listener typos."""

    def test_uppercase_i_substitutes_for_1(self, client, room_factory):
        # Canonical stored form uses 1, not I (I isn't in the alphabet)
        room = room_factory(short_id="1ABCDE")
        # User typed I (looks like 1)
        response = client.get("/r/IABCDE", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )

    def test_lowercase_l_substitutes_for_1(self, client, room_factory):
        room = room_factory(short_id="1ABCDE")
        response = client.get("/r/labcde", follow_redirects=False)
        assert response.status_code == 301

    def test_uppercase_o_substitutes_for_0(self, client, room_factory):
        room = room_factory(short_id="0ABCDE")
        response = client.get("/r/OABCDE", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )

    def test_combined_substitutions(self, client, room_factory):
        """A short_id of `110ABC` should resolve from `ILOABC` (I->1, L->1, O->0)."""
        room = room_factory(short_id="110ABC")
        response = client.get("/r/ILOABC", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["Location"].endswith(
            f"/play/seed/{to_url(room.seed_id)}/room/{to_url(room.id)}"
        )


# ---------------------------------------------------------------------------
# Negative cases
# ---------------------------------------------------------------------------

class TestNotFound:
    def test_unknown_short_id_404s(self, client):
        response = client.get("/r/NOPATH", follow_redirects=False)
        assert response.status_code == 404

    def test_too_short_404s(self, client):
        """We don't auto-pad short input."""
        response = client.get("/r/AB", follow_redirects=False)
        assert response.status_code == 404

    def test_too_long_404s(self, client):
        response = client.get("/r/K7M3QXEXTRA", follow_redirects=False)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Route exists and is registered
# ---------------------------------------------------------------------------

def test_short_room_endpoint_registered(client):
    """The /r/ route must be registered in url_map. Catches the case
    where the blueprint or route decorator was missed during the merge."""
    from WebHostLib import app

    rules = [rule for rule in app.url_map.iter_rules()
             if rule.endpoint == "short_room"]
    assert len(rules) == 1, "short_room endpoint not registered"
    assert "/r/" in str(rules[0].rule)
