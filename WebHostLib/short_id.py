"""
Short-ID generation and normalization for shareable room URLs
(``mw.prismativerse.com/r/K7M3QX``). Single source of truth for the
alphabet, length, generation, and lookup-normalization logic.
"""

import secrets

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Crockford base32 alphabet. 32 characters, no I/L/O/U.
#: https://www.crockford.com/base32.html
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

#: Length of every generated short_id. 32**6 = ~1 billion combinations.
SHORT_ID_LENGTH = 6

#: Random candidates to try before giving up. Collisions are astronomically
#: rare at our volume; if all 10 collide, the namespace needs expanding.
MAX_GENERATION_ATTEMPTS = 10

#: Lookup normalization: Crockford convention substitutes ambiguous chars.
#: Lowercase is handled by ``.upper()`` before applying this map.
_NORMALIZE_TRANSLATION = str.maketrans({
    "I": "1",
    "L": "1",
    "O": "0",
})


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ShortIDExhaustedError(RuntimeError):
    """Raised when no unique short_id could be generated after MAX_GENERATION_ATTEMPTS."""


# ---------------------------------------------------------------------------
# Generation and normalization
# ---------------------------------------------------------------------------

def generate_short_id() -> str:
    """Return a fresh random short_id from the Crockford alphabet.

    Uses ``secrets.choice`` (cryptographic randomness) rather than
    ``random.choice`` because short_ids are URL-visible and we don't want
    them to be predictable from each other.
    """
    return "".join(secrets.choice(ALPHABET) for _ in range(SHORT_ID_LENGTH))


def normalize_short_id(raw: str) -> str:
    """Normalize a user-supplied short_id for storage or lookup.

    Per Crockford convention: case-insensitive, with ambiguous-character
    substitution. ``I``/``L`` are read as ``1``; ``O`` is read as ``0``.

    Example:
        >>> normalize_short_id("ik7m3o")
        '1K7M30'

    Returns the canonical uppercase form. Always returns a string, even
    for malformed input; the caller decides whether to treat the result
    as a lookup target or reject it.
    """
    return raw.upper().translate(_NORMALIZE_TRANSLATION)


def is_well_formed(short_id: str) -> bool:
    """Return True if ``short_id`` has the right length and uses only
    valid Crockford characters (post-normalization).

    Used to early-reject obviously-bad inputs before hitting the DB.
    """
    if len(short_id) != SHORT_ID_LENGTH:
        return False
    return all(c in ALPHABET for c in short_id)


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------

def assign_short_id(session, room, max_attempts: int = MAX_GENERATION_ATTEMPTS) -> str:
    """Assign a unique short_id to ``room`` and return it.

    Performs a uniqueness pre-check on each candidate via the session;
    the database unique constraint is the actual safety net if a race
    slips through. Retries up to ``max_attempts`` times before raising.

    The caller is responsible for committing the session. This function
    mutates ``room.short_id`` and queries against ``session``, but does
    not commit.

    Args:
        session: SQLAlchemy session
        room: Room instance (must have a ``short_id`` column)
        max_attempts: How many candidates to try before giving up

    Returns:
        The assigned short_id string

    Raises:
        ShortIDExhaustedError: if every candidate collided
    """
    # Local import: keeps this module importable without the app's models package.
    from WebHostLib.models import Room  # noqa: WPS433

    for _ in range(max_attempts):
        candidate = generate_short_id()
        existing = (
            session.query(Room.id)
            .filter(Room.short_id == candidate)
            .first()
        )
        if not existing:
            room.short_id = candidate
            return candidate

    raise ShortIDExhaustedError(
        f"Could not generate unique short_id after {max_attempts} attempts. "
        f"Consider increasing SHORT_ID_LENGTH."
    )
