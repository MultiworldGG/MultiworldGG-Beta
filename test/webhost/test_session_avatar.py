"""Website (session-cookie) avatar management — PR1 of the persistent-avatar
feature.

Covers the /me/avatar upload/replace/remove flow, the nav context processor,
and that the refactored Bearer-token API in ``api/avatar.py`` still works.
"""
from __future__ import annotations

import io
import os
from uuid import uuid4

import pytest
from PIL import Image


def _png_bytes(color=(10, 120, 200, 255), size=(64, 64)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGBA", size, color).save(buf, format="PNG")
    return buf.getvalue()


def _upload(client, png: bytes, filename: str = "a.png"):
    return client.post(
        "/me/avatar",
        data={"image": (io.BytesIO(png), filename)},
        content_type="multipart/form-data",
    )


def _pin_session(client):
    sid = uuid4()
    with client.session_transaction() as sess:
        sess["_id"] = sid
    return sid


def _session_avatar_hex(app, sid):
    from WebHostLib.models import SessionAvatar
    with app.app_context():
        record = SessionAvatar.get(session_id=sid)
        return record.avatar_id.hex if record else None


@pytest.fixture(autouse=True)
def _isolated_avatar_dir(app, tmp_path):
    """Point avatar storage at a per-test temp dir so uploads don't litter the repo."""
    original = app.config["AVATAR_UPLOAD_FOLDER"]
    app.config["AVATAR_UPLOAD_FOLDER"] = str(tmp_path)
    yield
    app.config["AVATAR_UPLOAD_FOLDER"] = original


# ---------------------------------------------------------------------------
# Page + happy path
# ---------------------------------------------------------------------------

def test_me_avatar_page_renders_default(client):
    resp = client.get("/me/avatar")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Your avatar" in body
    # No avatar yet -> falls back to the controller icon.
    assert "controller-icon.png" in body


def test_upload_sets_session_avatar(client, app):
    sid = _pin_session(client)

    resp = _upload(client, _png_bytes())
    assert resp.status_code == 302  # redirect back to /me/avatar

    hex_id = _session_avatar_hex(app, sid)
    assert hex_id is not None
    assert os.path.isfile(os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], f"{hex_id}.png"))

    body = client.get("/me/avatar").get_data(as_text=True)
    assert f"/avatar/{hex_id}.png" in body


def test_nav_avatar_uses_session_avatar(client, app):
    """The baseHeader nav <img> (present on every page) shows the session avatar."""
    sid = _pin_session(client)
    _upload(client, _png_bytes())
    hex_id = _session_avatar_hex(app, sid)

    body = client.get("/me/seeds").get_data(as_text=True)
    assert f"/avatar/{hex_id}.png" in body


# ---------------------------------------------------------------------------
# Replace + remove lifecycle
# ---------------------------------------------------------------------------

def test_upload_replaces_previous(client, app):
    from sqlalchemy import func, select
    from WebHostLib.models import SessionAvatar, db

    sid = _pin_session(client)
    _upload(client, _png_bytes(color=(255, 0, 0, 255)))
    first = _session_avatar_hex(app, sid)
    _upload(client, _png_bytes(color=(0, 255, 0, 255)))
    second = _session_avatar_hex(app, sid)

    assert second != first
    avatars_dir = app.config["AVATAR_UPLOAD_FOLDER"]
    assert os.path.isfile(os.path.join(avatars_dir, f"{second}.png"))
    assert not os.path.isfile(os.path.join(avatars_dir, f"{first}.png"))  # old file removed

    with app.app_context():
        count = db.session.scalar(
            select(func.count()).select_from(SessionAvatar).where(SessionAvatar.session_id == sid)
        )
    assert count == 1  # exactly one row per session


def test_remove_clears_avatar(client, app):
    sid = _pin_session(client)
    _upload(client, _png_bytes())
    hex_id = _session_avatar_hex(app, sid)
    avatars_dir = app.config["AVATAR_UPLOAD_FOLDER"]

    resp = client.post("/me/avatar/remove")
    assert resp.status_code == 302
    assert _session_avatar_hex(app, sid) is None
    assert not os.path.isfile(os.path.join(avatars_dir, f"{hex_id}.png"))
    assert "controller-icon.png" in client.get("/me/avatar").get_data(as_text=True)


# ---------------------------------------------------------------------------
# Rejections + API regression guard
# ---------------------------------------------------------------------------

def test_reject_non_image(client, app):
    sid = _pin_session(client)
    resp = _upload(client, b"this is not an image", filename="x.png")
    assert resp.status_code == 302  # error flashed, redirected
    assert _session_avatar_hex(app, sid) is None


def test_mwgg_viewer_avatar_url(app):
    """The Jinja global feeding mwgg:// &avatar= returns the session's absolute
    avatar URL, or '' when the session has none."""
    from flask import session as flask_session
    from WebHostLib.avatars import mwgg_viewer_avatar_url
    from WebHostLib.models import Avatar, AvatarToken, SessionAvatar, commit, db

    sid = uuid4()
    with app.app_context():
        token = AvatarToken()
        db.session.flush()
        avatar = Avatar(id=uuid4(), owner_token=token, mime_type="image/png",
                        file_size=1, original_sha256="0" * 64)
        db.session.flush()
        SessionAvatar(session_id=sid, avatar_id=avatar.id)
        avatar_hex = avatar.id.hex
        commit()

    with app.test_request_context():
        flask_session["_id"] = sid
        assert mwgg_viewer_avatar_url().endswith(f"/avatar/{avatar_hex}.png")

    with app.test_request_context():
        flask_session["_id"] = uuid4()  # different session, no avatar
        assert mwgg_viewer_avatar_url() == ""


def test_bearer_api_upload_still_works(client):
    """Guards the avatar.py refactor: the desktop-client Bearer flow is intact."""
    mint = client.post("/api/avatar/token")
    assert mint.status_code == 200
    token = mint.get_json()["token"]

    resp = client.post(
        "/api/avatar/upload",
        data={"image": (io.BytesIO(_png_bytes()), "a.png")},
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert "/avatar/" in resp.get_json()["url"]
