"""Behavioral invariants for WebHostLib.autolauncher.

These tests pin non-obvious facts the module relies on, so the source stays
self-documenting via test names instead of inline comments.
"""
from __future__ import annotations

from uuid import UUID, uuid4


def test_null_owner_uuid_is_truthy():
    """The all-zero "null owner" sentinel UUID is truthy, unlike int 0.

    ``cleanup()`` selects unowned rows with ``Room.owner == UUID(int=0)``
    rather than a falsiness check, because ``bool(UUID(int=0))`` is ``True``.
    A ``if not owner``-style guard would therefore never match the sentinel.
    """
    null_owner = UUID(int=0)

    assert bool(null_owner) is True
    # Contrast with the int it wraps, which IS falsy.
    assert bool(0) is False

    # cleanup() depends on equality (not falsiness) to find the sentinel,
    # so the sentinel must compare equal to itself and unequal to real owners.
    assert null_owner == UUID(int=0)
    assert null_owner != uuid4()
