"""Webhost identity tests; add new identity tests here.

Covers the passkeys Flask blueprint (registration, authentication/recovery,
inspection/revocation - with the ``webauthn`` library's verify functions
mocked so the tests stay focused on routing, storage interaction, and
challenge bookkeeping; end-to-end testing against a real authenticator
belongs in a Selenium / Playwright suite using the virtual-authenticator
API), the passkey-flavoured /me modals and the /session/recover page, and
the SECRET_KEY production-default guardrail in ``WebHost.get_app()``.

The blueprint tests run on a standalone Flask app to isolate the blueprint
from the rest of the project's wiring, and use real UUID strings for session
ids since the host blueprint re-hydrates them via uuid.UUID().
"""
from __future__ import annotations

import json
import socket
from base64 import urlsafe_b64encode
from types import SimpleNamespace
from typing import Dict, List, Optional
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from flask import Flask

from WebHostLib import passkeys
from WebHostLib.passkeys import StoredCredential, passkeys_bp


# ---------------------------------------------------------------------------
# Passkey blueprint fixtures
# ---------------------------------------------------------------------------

class InMemoryStore:
    """Trivial CredentialStore implementation for tests."""

    def __init__(self) -> None:
        self.rows: Dict[bytes, StoredCredential] = {}

    def add(self, cred: StoredCredential) -> None:
        self.rows[cred.credential_id] = cred

    def get(self, credential_id: bytes) -> Optional[StoredCredential]:
        return self.rows.get(credential_id)

    def update_sign_count(self, credential_id: bytes, new_count: int) -> None:
        self.rows[credential_id].sign_count = new_count

    def list_for_session(self, session_id: str) -> List[StoredCredential]:
        return [c for c in self.rows.values() if c.session_id == session_id]

    def remove(self, credential_id: bytes) -> bool:
        return self.rows.pop(credential_id, None) is not None


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


@pytest.fixture
def passkey_app(store: InMemoryStore) -> Flask:
    fresh = Flask(__name__)
    fresh.config.update(
        TESTING=True,
        SECRET_KEY="test-secret",
        WEBAUTHN_RP_ID="example.test",
        WEBAUTHN_RP_NAME="MultiworldGG Test",
        WEBAUTHN_ORIGIN="https://example.test",
        WEBAUTHN_USER_HANDLE_SECRET=b"unit-test-secret",
    )
    passkeys_bp.credential_store = store
    fresh.register_blueprint(passkeys_bp)
    return fresh


@pytest.fixture
def passkey_client(passkey_app: Flask):
    return passkey_app.test_client()


def _with_session(client, session_id_uuid: UUID) -> None:
    # The host app stores session["_id"] as a UUID; passkeys.py calls str()
    # on it before handing it to the store / WebAuthn helpers.
    with client.session_transaction() as s:
        s["_id"] = session_id_uuid


# Stable UUIDs for tests that need known session-ids on both ends.
SESSION_A = UUID("11111111-1111-1111-1111-111111111111")
SESSION_B = UUID("22222222-2222-2222-2222-222222222222")


# ---------------------------------------------------------------------------
# Passkeys: pure functions
# ---------------------------------------------------------------------------

def test_user_handle_is_stable_per_session(passkey_app: Flask):
    with passkey_app.app_context():
        h1 = passkeys._user_handle_for("session-abc")
        h2 = passkeys._user_handle_for("session-abc")
        assert h1 == h2
        assert len(h1) == 32


def test_user_handle_differs_between_sessions(passkey_app: Flask):
    with passkey_app.app_context():
        assert passkeys._user_handle_for("a") != passkeys._user_handle_for("b")


def test_user_handle_does_not_contain_session_id(passkey_app: Flask):
    with passkey_app.app_context():
        sid = "secret-session-12345"
        handle = passkeys._user_handle_for(sid)
        assert sid.encode() not in handle


def test_b64url_decode_handles_unpadded_input():
    raw = b"\x01\x02\x03\x04\x05"
    encoded = urlsafe_b64encode(raw).rstrip(b"=").decode()
    assert passkeys._b64url_decode(encoded) == raw


# ---------------------------------------------------------------------------
# Passkeys: registration flow
# ---------------------------------------------------------------------------

def test_register_start_requires_session(passkey_client):
    res = passkey_client.post("/session/passkey/register/start")
    assert res.status_code == 401


def test_register_start_stashes_a_challenge(passkey_client):
    _with_session(passkey_client, SESSION_A)
    res = passkey_client.post("/session/passkey/register/start")
    assert res.status_code == 200
    body = res.get_json()
    assert "challenge" in body
    assert body["rp"]["id"] == "example.test"

    with passkey_client.session_transaction() as s:
        assert "webauthn_register_challenge" in s


def test_register_finish_stores_credential(passkey_client, store: InMemoryStore):
    _with_session(passkey_client, SESSION_A)
    passkey_client.post("/session/passkey/register/start")

    fake_verification = SimpleNamespace(
        credential_id=b"cred-id-bytes-001",
        credential_public_key=b"public-key-bytes",
        sign_count=0,
    )
    with patch.object(passkeys, "verify_registration_response", return_value=fake_verification):
        res = passkey_client.post(
            "/session/passkey/register/finish",
            data=json.dumps({"id": "stub", "rawId": "stub", "response": {}, "type": "public-key"}),
            content_type="application/json",
        )

    assert res.status_code == 200
    # The blueprint stringifies session["_id"] before handing to the store.
    assert store.rows[b"cred-id-bytes-001"].session_id == str(SESSION_A)
    assert store.rows[b"cred-id-bytes-001"].sign_count == 0


def test_register_finish_rejects_without_pending_challenge(passkey_client):
    _with_session(passkey_client, SESSION_A)
    res = passkey_client.post(
        "/session/passkey/register/finish",
        data=json.dumps({}), content_type="application/json",
    )
    assert res.status_code == 400


def test_register_finish_consumes_challenge_once(passkey_client, store: InMemoryStore):
    _with_session(passkey_client, SESSION_A)
    passkey_client.post("/session/passkey/register/start")

    fake = SimpleNamespace(credential_id=b"c", credential_public_key=b"p", sign_count=0)
    with patch.object(passkeys, "verify_registration_response", return_value=fake):
        first = passkey_client.post(
            "/session/passkey/register/finish",
            data=json.dumps({"id": "x", "rawId": "x", "response": {}, "type": "public-key"}),
            content_type="application/json",
        )
        assert first.status_code == 200
        # Replay: same challenge must not be accepted again
        second = passkey_client.post(
            "/session/passkey/register/finish",
            data=json.dumps({"id": "x", "rawId": "x", "response": {}, "type": "public-key"}),
            content_type="application/json",
        )
        assert second.status_code == 400


def test_register_start_excludes_existing_credentials(passkey_client, store: InMemoryStore):
    _with_session(passkey_client, SESSION_A)
    store.add(StoredCredential(
        credential_id=b"already-have", public_key=b"pk",
        sign_count=0, session_id=str(SESSION_A),
    ))
    res = passkey_client.post("/session/passkey/register/start")
    body = res.get_json()
    excluded_ids = [c["id"] for c in body.get("excludeCredentials", [])]
    expected = urlsafe_b64encode(b"already-have").rstrip(b"=").decode()
    assert expected in excluded_ids


# ---------------------------------------------------------------------------
# Passkeys: authentication / recovery flow
# ---------------------------------------------------------------------------

def test_auth_start_works_without_session(passkey_client):
    res = passkey_client.post("/session/passkey/auth/start")
    assert res.status_code == 200
    body = res.get_json()
    assert "challenge" in body
    assert body.get("allowCredentials", []) == []


def test_auth_finish_restores_session_id(passkey_client, store: InMemoryStore):
    store.add(StoredCredential(
        credential_id=b"cred-id-bytes-002",
        public_key=b"public-key-bytes",
        sign_count=3,
        session_id=str(SESSION_A),
    ))
    passkey_client.post("/session/passkey/auth/start")

    raw_id = urlsafe_b64encode(b"cred-id-bytes-002").rstrip(b"=").decode()
    fake = SimpleNamespace(new_sign_count=4)
    with patch.object(passkeys, "verify_authentication_response", return_value=fake):
        res = passkey_client.post(
            "/session/passkey/auth/finish",
            data=json.dumps({"rawId": raw_id, "id": raw_id, "response": {}, "type": "public-key"}),
            content_type="application/json",
        )

    assert res.status_code == 200
    assert store.rows[b"cred-id-bytes-002"].sign_count == 4
    with passkey_client.session_transaction() as s:
        # The blueprint re-hydrates the stored str back to a UUID for the host app.
        assert s["_id"] == SESSION_A


def test_auth_finish_rejects_unknown_credential(passkey_client):
    passkey_client.post("/session/passkey/auth/start")
    raw_id = urlsafe_b64encode(b"not-in-store").rstrip(b"=").decode()
    res = passkey_client.post(
        "/session/passkey/auth/finish",
        data=json.dumps({"rawId": raw_id, "id": raw_id, "response": {}, "type": "public-key"}),
        content_type="application/json",
    )
    assert res.status_code == 400


def test_auth_finish_requires_pending_challenge(passkey_client, store: InMemoryStore):
    store.add(StoredCredential(
        credential_id=b"c", public_key=b"p", sign_count=0, session_id=str(SESSION_A),
    ))
    raw_id = urlsafe_b64encode(b"c").rstrip(b"=").decode()
    res = passkey_client.post(
        "/session/passkey/auth/finish",
        data=json.dumps({"rawId": raw_id, "id": raw_id, "response": {}, "type": "public-key"}),
        content_type="application/json",
    )
    assert res.status_code == 400


# ---------------------------------------------------------------------------
# Passkeys: privacy properties
# ---------------------------------------------------------------------------

def test_stored_credential_has_no_pii_fields():
    fields = set(StoredCredential.__dataclass_fields__.keys())
    forbidden = {"email", "name", "display_name", "phone", "username", "ip"}
    assert fields.isdisjoint(forbidden)


# ---------------------------------------------------------------------------
# Passkeys: inspection / revocation
# ---------------------------------------------------------------------------

def test_list_requires_session(passkey_client):
    assert passkey_client.get("/session/passkey/list").status_code == 401


def test_list_returns_only_caller_credentials(passkey_client, store: InMemoryStore):
    store.add(StoredCredential(b"mine-1", b"pk", 0, str(SESSION_A)))
    store.add(StoredCredential(b"mine-2", b"pk", 0, str(SESSION_A)))
    store.add(StoredCredential(b"other", b"pk", 0, str(SESSION_B)))
    _with_session(passkey_client, SESSION_A)

    ids = {c["id"] for c in passkey_client.get("/session/passkey/list").get_json()["credentials"]}
    expected = {
        urlsafe_b64encode(b"mine-1").rstrip(b"=").decode(),
        urlsafe_b64encode(b"mine-2").rstrip(b"=").decode(),
    }
    assert ids == expected


def test_remove_deletes_caller_credential(passkey_client, store: InMemoryStore):
    store.add(StoredCredential(b"to-remove", b"pk", 0, str(SESSION_A)))
    _with_session(passkey_client, SESSION_A)

    raw_id = urlsafe_b64encode(b"to-remove").rstrip(b"=").decode()
    res = passkey_client.post("/session/passkey/remove",
                              data=json.dumps({"id": raw_id}), content_type="application/json")

    assert res.status_code == 200
    assert b"to-remove" not in store.rows


def test_remove_rejects_other_users_credential(passkey_client, store: InMemoryStore):
    store.add(StoredCredential(b"belongs-to-B", b"pk", 0, str(SESSION_B)))
    _with_session(passkey_client, SESSION_A)

    raw_id = urlsafe_b64encode(b"belongs-to-B").rstrip(b"=").decode()
    res = passkey_client.post("/session/passkey/remove",
                              data=json.dumps({"id": raw_id}), content_type="application/json")

    assert res.status_code == 404
    assert b"belongs-to-B" in store.rows  # untouched


def test_remove_returns_same_status_for_missing_and_others(passkey_client, store: InMemoryStore):
    """The endpoint must not reveal whether a credential exists at all."""
    store.add(StoredCredential(b"belongs-to-B", b"pk", 0, str(SESSION_B)))
    _with_session(passkey_client, SESSION_A)

    missing_id = urlsafe_b64encode(b"no-such-credential").rstrip(b"=").decode()
    others_id = urlsafe_b64encode(b"belongs-to-B").rstrip(b"=").decode()

    a = passkey_client.post("/session/passkey/remove",
                            data=json.dumps({"id": missing_id}), content_type="application/json")
    b = passkey_client.post("/session/passkey/remove",
                            data=json.dumps({"id": others_id}), content_type="application/json")

    assert a.status_code == b.status_code == 404


# ---------------------------------------------------------------------------
# Passkey-flavoured /me modals and /session/recover (against the real app)
# ---------------------------------------------------------------------------

def test_me_includes_passkey_move_device_modal(client, room_factory):
    # Populate the session so /me renders the dashboard (not the empty state).
    owner = uuid4()
    with client.session_transaction() as session:
        session["_id"] = owner
    room_factory(owner=owner)

    response = client.get("/me")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # The move-device modal must be present with passkey-specific markup.
    assert 'id="move-device-modal"' in body
    assert "/session/passkey/register/start" in body


def test_me_first_run_includes_passkey_restore_modal(client):
    response = client.get("/me")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'id="restore-session-modal"' in body
    assert "/session/passkey/auth/start" in body


def test_session_recover_page_renders(client):
    response = client.get("/session/recover")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "/session/passkey/auth/start" in body


# ---------------------------------------------------------------------------
# SECRET_KEY production-default guardrail in WebHost.get_app()
# ---------------------------------------------------------------------------

def test_get_app_refuses_hostname_secret_in_production(monkeypatch):
    """The webhost must refuse to boot if SECRET_KEY is still the hostname-derived
    default and TESTING is False: that key signs session cookies and is
    trivially forgeable by anyone who can guess the host name."""
    from WebHostLib import app as raw_app
    import WebHost

    # Force the hostname-derived default and clear any test-mode override.
    raw_app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
    raw_app.config["TESTING"] = False

    # Don't let an actual config.yaml on disk override it during the test.
    monkeypatch.setattr(WebHost.os.path, "exists", lambda p: False)

    with pytest.raises(RuntimeError, match="SECRET_KEY is still the hostname-derived default"):
        WebHost.get_app()


def test_get_app_allows_hostname_secret_when_testing(monkeypatch):
    """The same default is fine under TESTING=True (the project's pytest fixture sets it)."""
    from WebHostLib import app as raw_app
    import WebHost

    raw_app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
    raw_app.config["TESTING"] = True
    raw_app.config["PONY"] = {"provider": "sqlite", "filename": ":memory:", "create_db": True}

    monkeypatch.setattr(WebHost.os.path, "exists", lambda p: False)

    # Should not raise: TESTING=True bypasses the guardrail. We don't care
    # about the return value; if it returns, the guardrail didn't trip.
    try:
        WebHost.get_app()
    except (AssertionError, ValueError) as e:
        # get_app() raises on duplicate blueprint registration when called more than once
        # in the same process (AssertionError on older Flask, ValueError on Flask 3.x);
        # that's fine for this test (we only care that RuntimeError isn't raised by the guardrail).
        message = e.args[0] if e.args else str(e)
        if "register_blueprint" not in message and "already registered" not in message:
            raise
