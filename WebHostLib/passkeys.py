"""
Passkey (WebAuthn) recovery for MultiworldGG sessions.

The existing ``session["_id"]`` UUID stays the source of truth. A passkey is
an *additional* way to recover it after a browser wipes its cookie jar; it
does not replace the cookie-based session. No PII is stored or requested.

Wiring it up::

    from WebHostLib.passkeys import passkeys_bp
    app.config["WEBAUTHN_RP_ID"] = "mw.prismativerse.com"
    app.config["WEBAUTHN_ORIGIN"] = "https://mw.prismativerse.com"
    app.config["WEBAUTHN_RP_NAME"] = "MultiworldGG"
    app.config["WEBAUTHN_USER_HANDLE_SECRET"] = os.environ["WEBAUTHN_HANDLE_SECRET"]
    passkeys_bp.credential_store = MyCredentialStore(db)  # see CredentialStore
    app.register_blueprint(passkeys_bp)
"""

from __future__ import annotations

import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import dataclass
from hashlib import sha256
from typing import List, Optional, Protocol

from flask import Blueprint, abort, current_app, jsonify, request, session
from flask_limiter.util import get_remote_address
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

passkeys_bp = Blueprint("passkeys", __name__, url_prefix="/session/passkey")


def _maybe_rate_limit(limit: str):
    """Decorator that applies a per-IP rate limit when the host app has a
    flask-limiter ``limiter`` available. Falls through as a no-op when the
    blueprint is registered standalone (e.g. in unit tests).
    """
    def decorator(view):
        try:
            from WebHostLib import limiter as _limiter
        except (ImportError, RuntimeError):
            return view
        return _limiter.limit(limit, key_func=get_remote_address)(view)
    return decorator


# ---------------------------------------------------------------------------
# Storage interface - implement against whatever ORM the host app uses
# ---------------------------------------------------------------------------

@dataclass
class StoredCredential:
    """One row in the passkey table. No PII fields by design."""
    credential_id: bytes
    public_key: bytes
    sign_count: int
    session_id: str


class CredentialStore(Protocol):
    def add(self, cred: StoredCredential) -> None: ...
    def get(self, credential_id: bytes) -> Optional[StoredCredential]: ...
    def update_sign_count(self, credential_id: bytes, new_count: int) -> None: ...
    def list_for_session(self, session_id: str) -> List[StoredCredential]: ...
    def remove(self, credential_id: bytes) -> bool: ...


def _store() -> CredentialStore:
    store = getattr(passkeys_bp, "credential_store", None)
    if store is None:
        raise RuntimeError("passkeys_bp.credential_store has not been configured")
    return store


# ---------------------------------------------------------------------------
# Config accessors
# ---------------------------------------------------------------------------

def _rp_id() -> str:
    return current_app.config["WEBAUTHN_RP_ID"]


def _rp_name() -> str:
    return current_app.config.get("WEBAUTHN_RP_NAME", "MultiworldGG")


def _origin() -> str:
    return current_app.config["WEBAUTHN_ORIGIN"]


def _handle_secret() -> bytes:
    secret = current_app.config.get("WEBAUTHN_USER_HANDLE_SECRET")
    if not secret:
        raise RuntimeError("WEBAUTHN_USER_HANDLE_SECRET is not configured")
    return secret if isinstance(secret, bytes) else secret.encode()


def _user_handle_for(session_id: str) -> bytes:
    """Stable, opaque 32-byte handle derived from a session id.

    HMAC is one-way: even if the handle leaks, the session id is not
    recoverable from it. Stability lets the OS group multiple passkeys
    that belong to the same logical user when the picker is shown.
    """
    return hmac.new(_handle_secret(), session_id.encode("utf-8"), sha256).digest()


def _b64url_decode(value: str) -> bytes:
    """Decode unpadded base64url as WebAuthn sends it from the browser."""
    padding = "=" * (-len(value) % 4)
    return urlsafe_b64decode(value + padding)


# ---------------------------------------------------------------------------
# Registration (user already has a session)
# ---------------------------------------------------------------------------

@passkeys_bp.route("/register/start", methods=["POST"])
def register_start():
    raw_id = session.get("_id")
    if not raw_id:
        abort(401, "must be signed in to add a passkey")
    # session["_id"] is a UUID in the host app; the store / WebAuthn want a string.
    session_id = str(raw_id)

    existing = _store().list_for_session(session_id)
    options = generate_registration_options(
        rp_id=_rp_id(),
        rp_name=_rp_name(),
        user_id=_user_handle_for(session_id),
        user_name="MultiworldGG session",
        user_display_name="MultiworldGG",
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
        exclude_credentials=[
            PublicKeyCredentialDescriptor(id=c.credential_id) for c in existing
        ],
    )
    session["webauthn_register_challenge"] = urlsafe_b64encode(options.challenge).decode()
    return current_app.response_class(options_to_json(options), mimetype="application/json")


@passkeys_bp.route("/register/finish", methods=["POST"])
def register_finish():
    raw_id = session.get("_id")
    if not raw_id:
        abort(401)
    session_id = str(raw_id)

    challenge_b64 = session.pop("webauthn_register_challenge", None)
    if not challenge_b64:
        abort(400, "no pending registration")
    expected_challenge = urlsafe_b64decode(challenge_b64.encode())

    verification = verify_registration_response(
        credential=request.get_json(force=True),
        expected_challenge=expected_challenge,
        expected_origin=_origin(),
        expected_rp_id=_rp_id(),
        require_user_verification=False,
    )

    _store().add(StoredCredential(
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
        session_id=session_id,
    ))
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Authentication (no session needed: this is the recovery path)
# ---------------------------------------------------------------------------

@passkeys_bp.route("/auth/start", methods=["POST"])
@_maybe_rate_limit("10/minute")
def auth_start():
    # Empty allow_credentials triggers the discoverable-credential flow: the OS
    # shows the user's passkeys without the server hinting at which ones exist.
    options = generate_authentication_options(
        rp_id=_rp_id(),
        user_verification=UserVerificationRequirement.PREFERRED,
        allow_credentials=[],
    )
    session["webauthn_auth_challenge"] = urlsafe_b64encode(options.challenge).decode()
    return current_app.response_class(options_to_json(options), mimetype="application/json")


@passkeys_bp.route("/auth/finish", methods=["POST"])
@_maybe_rate_limit("10/minute")
def auth_finish():
    challenge_b64 = session.pop("webauthn_auth_challenge", None)
    if not challenge_b64:
        abort(400, "no pending authentication")
    expected_challenge = urlsafe_b64decode(challenge_b64.encode())

    body = request.get_json(force=True)
    credential_id = _b64url_decode(body["rawId"])
    stored = _store().get(credential_id)
    if not stored:
        # Use the same generic message we'd return for any failure, so a
        # caller can't distinguish "unknown credential" from "bad signature".
        abort(400, "passkey not recognised")

    verification = verify_authentication_response(
        credential=body,
        expected_challenge=expected_challenge,
        expected_origin=_origin(),
        expected_rp_id=_rp_id(),
        credential_public_key=stored.public_key,
        credential_current_sign_count=stored.sign_count,
        require_user_verification=False,
    )

    _store().update_sign_count(credential_id, verification.new_sign_count)
    session.permanent = True
    # Stored as a UUID string in the DB; re-hydrate for the host app's invariant.
    import uuid as _uuid
    session["_id"] = _uuid.UUID(stored.session_id)
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Inspection and revocation (user is logged in)
# ---------------------------------------------------------------------------

@passkeys_bp.route("/list", methods=["GET"])
def list_credentials():
    """Return the caller's enrolled passkeys so the UI can offer revocation.

    Only the credential id is exposed; the public key and sign count are
    server-internal. The id is what the client passes back to ``/remove``.
    """
    raw_id = session.get("_id")
    if not raw_id:
        abort(401)
    session_id = str(raw_id)
    return jsonify({
        "credentials": [
            {"id": urlsafe_b64encode(c.credential_id).rstrip(b"=").decode()}
            for c in _store().list_for_session(session_id)
        ],
    })


@passkeys_bp.route("/remove", methods=["POST"])
def remove_credential():
    """Delete one of the caller's passkeys.

    Only the holder of the owning session may remove a passkey; a user who
    lost the cookie must recover the session first. A recovery endpoint must
    not be able to destroy recovery.
    """
    raw_id = session.get("_id")
    if not raw_id:
        abort(401)
    session_id = str(raw_id)

    body = request.get_json(force=True) or {}
    raw_id = body.get("id")
    if not raw_id:
        abort(400, "id is required")
    credential_id = _b64url_decode(raw_id)

    stored = _store().get(credential_id)
    if not stored or stored.session_id != session_id:
        # Same response shape for "doesn't exist" and "belongs to someone
        # else" so the endpoint isn't an ownership oracle.
        abort(404)

    _store().remove(credential_id)
    return jsonify({"ok": True})
