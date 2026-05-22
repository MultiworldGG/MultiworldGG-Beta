"""
Unit tests for ``WebHostLib.short_id``.

Tests the generator, normalization, well-formedness check, and the
assignment function with collision retry.

Expects two fixtures from your conftest.py:

    @pytest.fixture
    def db_session():
        # Your SQLAlchemy session fixture, scoped to a single test.
        # Should yield a session, then roll back.
        ...

    @pytest.fixture
    def room_factory(db_session):
        # A factory that creates a Room row. Accepts kwargs for any
        # column override.
        def _make(**kwargs):
            from WebHostLib.models import Room, Seed
            seed = kwargs.pop("seed", None) or Seed()
            db_session.add(seed)
            db_session.flush()
            room = Room(seed_id=seed.id, **kwargs)
            db_session.add(room)
            db_session.flush()
            return room
        return _make
"""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def _wipe_rooms_after_test(app):
    """Tests in this module pre-seed rooms with hardcoded short_ids
    (e.g. "AAAAAA", "EXIST1"). Because the session-scoped ``app``
    fixture shares one in-memory DB across all tests, leftover rows
    would trip the UNIQUE constraint on the next test's hardcoded
    value. Wipe room/seed/command/lobby rows after each test.
    """
    yield
    from WebHostLib.models import db, Room, Seed, Command, Lobby, LobbyMessage
    with app.app_context():
        db.session.query(LobbyMessage).delete()
        db.session.query(Lobby).delete()
        db.session.query(Command).delete()
        db.session.query(Room).delete()
        db.session.query(Seed).delete()
        db.session.commit()

from WebHostLib.short_id import (
    ALPHABET,
    MAX_GENERATION_ATTEMPTS,
    SHORT_ID_LENGTH,
    ShortIDExhaustedError,
    assign_short_id,
    generate_short_id,
    is_well_formed,
    normalize_short_id,
)


# ---------------------------------------------------------------------------
# Alphabet invariants
# ---------------------------------------------------------------------------

class TestAlphabet:
    def test_alphabet_is_32_chars(self):
        assert len(ALPHABET) == 32

    def test_alphabet_excludes_i_l_o_u(self):
        """Crockford convention: I, L, O, U are excluded."""
        for excluded in ("I", "L", "O", "U"):
            assert excluded not in ALPHABET, f"{excluded} should be excluded"

    def test_alphabet_uppercase_only(self):
        assert ALPHABET == ALPHABET.upper()

    def test_short_id_length_is_six(self):
        assert SHORT_ID_LENGTH == 6


# ---------------------------------------------------------------------------
# generate_short_id
# ---------------------------------------------------------------------------

class TestGenerate:
    def test_correct_length(self):
        for _ in range(100):
            assert len(generate_short_id()) == SHORT_ID_LENGTH

    def test_only_uses_alphabet(self):
        valid_chars = set(ALPHABET)
        for _ in range(100):
            generated = generate_short_id()
            assert all(c in valid_chars for c in generated), (
                f"Generated {generated!r} contains invalid characters"
            )

    def test_outputs_are_uppercase(self):
        for _ in range(100):
            generated = generate_short_id()
            assert generated == generated.upper()

    def test_outputs_are_different(self):
        """100 generations should not all be the same. Sanity check
        that we're using random and not, e.g., a constant."""
        samples = {generate_short_id() for _ in range(100)}
        # With 32^6 namespace, getting 100 dupes in 100 draws is
        # vanishingly improbable. Expect close to 100 unique values.
        assert len(samples) >= 95


# ---------------------------------------------------------------------------
# normalize_short_id
# ---------------------------------------------------------------------------

class TestNormalize:
    @pytest.mark.parametrize("raw, expected", [
        ("K7M3QX", "K7M3QX"),
        ("k7m3qx", "K7M3QX"),
        ("K7m3Qx", "K7M3QX"),
    ])
    def test_case_insensitive(self, raw, expected):
        assert normalize_short_id(raw) == expected

    @pytest.mark.parametrize("raw, expected", [
        ("I00000", "100000"),  # I -> 1
        ("i00000", "100000"),  # lowercase i -> 1
        ("L00000", "100000"),  # L -> 1
        ("l00000", "100000"),  # lowercase l -> 1
        ("O00000", "000000"),  # O -> 0
        ("o00000", "000000"),  # lowercase o -> 0
    ])
    def test_ambiguous_char_substitution(self, raw, expected):
        assert normalize_short_id(raw) == expected

    def test_combined_normalization(self):
        """Mixed case + ambiguous chars: all handled in one pass."""
        # User typed lowercase i, l, o; expected canonical 1, 1, 0
        assert normalize_short_id("ilOabc") == "110ABC"

    def test_no_change_for_canonical(self):
        canonical = "K7M3QX"
        assert normalize_short_id(canonical) == canonical


# ---------------------------------------------------------------------------
# is_well_formed
# ---------------------------------------------------------------------------

class TestIsWellFormed:
    def test_accepts_canonical_short_id(self):
        assert is_well_formed("K7M3QX")

    def test_rejects_too_short(self):
        assert not is_well_formed("ABC")

    def test_rejects_too_long(self):
        assert not is_well_formed("K7M3QXEXTRA")

    def test_rejects_invalid_characters(self):
        # I, L, O, U should never appear in well-formed canonical IDs
        assert not is_well_formed("IIIIIII"[:6])
        assert not is_well_formed("LLLLLL")
        assert not is_well_formed("OOOOOO")
        assert not is_well_formed("UUUUUU")

    def test_rejects_lowercase(self):
        """Well-formedness is the canonical form check."""
        assert not is_well_formed("k7m3qx")


# ---------------------------------------------------------------------------
# assign_short_id (requires DB)
# ---------------------------------------------------------------------------

class TestAssign:
    def test_assigns_value_to_room(self, db_session, room_factory):
        room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, room)
        assert room.short_id == assigned
        assert len(assigned) == SHORT_ID_LENGTH

    def test_returns_the_assigned_value(self, db_session, room_factory):
        room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, room)
        assert assigned is not None
        assert is_well_formed(assigned)

    def test_avoids_existing_short_ids(self, db_session, room_factory):
        existing = room_factory(short_id="EXIST1")
        new_room = room_factory(short_id=None)
        assigned = assign_short_id(db_session, new_room)
        assert assigned != "EXIST1"

    def test_retries_on_collision(self, db_session, room_factory):
        """When the first candidate collides, generate is called again
        until a unique one is produced."""
        # Pre-create rooms with known short_ids
        room_factory(short_id="AAAAAA")
        room_factory(short_id="BBBBBB")

        with patch(
            "WebHostLib.short_id.generate_short_id",
            side_effect=["AAAAAA", "BBBBBB", "CCCCCC"],
        ) as mock_gen:
            new_room = room_factory(short_id=None)
            assigned = assign_short_id(db_session, new_room)
            assert assigned == "CCCCCC"
            assert mock_gen.call_count == 3

    def test_raises_when_all_attempts_collide(self, db_session, room_factory):
        """If every candidate from generate collides, raise rather
        than loop forever."""
        room_factory(short_id="AAAAAA")
        with patch(
            "WebHostLib.short_id.generate_short_id",
            return_value="AAAAAA",
        ):
            new_room = room_factory(short_id=None)
            with pytest.raises(ShortIDExhaustedError):
                assign_short_id(db_session, new_room, max_attempts=3)

    def test_respects_max_attempts_argument(self, db_session, room_factory):
        """The retry loop honors the max_attempts kwarg."""
        room_factory(short_id="AAAAAA")
        with patch(
            "WebHostLib.short_id.generate_short_id",
            return_value="AAAAAA",
        ) as mock_gen:
            new_room = room_factory(short_id=None)
            with pytest.raises(ShortIDExhaustedError):
                assign_short_id(db_session, new_room, max_attempts=5)
            assert mock_gen.call_count == 5
