"""Smoke tests for the passkey-flavoured /me modals and /session/recover.

The full blueprint behavior is covered by test_passkeys.py; this file just
confirms the templates render with the right markup and the recovery page
mounts at /session/recover.
"""
from __future__ import annotations


def test_me_includes_passkey_move_device_modal(client, room_factory):
    # Populate the session so /me renders the dashboard (not the empty state).
    from uuid import uuid4
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # The move-device modal must be present with passkey-specific markup.
    assert 'id="move-device-modal"' in body
    assert "Add a passkey on this device" in body
    assert "/session/passkey/register/start" in body
    # No QR markup left over from Phase 8.
    assert "qr.png" not in body
    assert "Copy" not in body or "Passkeys on file" in body  # only Copy left would be in QR flow


def test_me_first_run_includes_passkey_restore_modal(client):
    response = client.get("/me")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'id="restore-session-modal"' in body
    assert "Sign in with a passkey" in body
    assert "/session/passkey/auth/start" in body


def test_session_recover_page_renders(client):
    response = client.get("/session/recover")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Recover your session" in body
    assert "/session/passkey/auth/start" in body
