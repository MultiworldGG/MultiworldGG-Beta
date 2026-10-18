"""Profile-picture upload, retrieval, and token-mint endpoints.

The desktop client mints a token on first use, then POSTs images here. The
server validates with Pillow, re-encodes as PNG with metadata stripped, and
returns a stable URL. The wire payload between clients (multiserver `Set` on
key `profile_data_{team}_{slot}`) remains an opaque URL string; the client
allowlists trusted hosts on the render side.
"""
import hashlib
import io
import os
import re
import uuid
from uuid import UUID

import requests
from flask import abort, jsonify, request, send_from_directory
from flask_limiter.util import get_remote_address
from PIL import Image, ImageOps, UnidentifiedImageError

from Utils import utcnow
from WebHostLib import app, limiter
from WebHostLib.models import Avatar, AvatarToken, commit
from . import api_endpoints


PNG_EXTENSION = ".png"
HEX_ID_RE = re.compile(r"^[0-9a-f]{32}$")

# Exposed-nudity labels emitted by the NudeNet sidecar (deploy/docker-compose.yml
# `nudenet`). MALE_BREAST_EXPOSED is intentionally absent: ordinary topless
# photos aren't what we're filtering.
_NSFW_BLOCKED_CLASSES = frozenset({
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "BUTTOCKS_EXPOSED",
    "ANUS_EXPOSED",
})
_NSFW_SCORE_THRESHOLD = 0.5
_NSFW_REQUEST_TIMEOUT = 10  # seconds to wait on the moderation sidecar
_NSFW_SAMPLE_MAX_DIM = 1024  # max edge of the re-encoded moderation sample


def _bearer_token() -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return ""
    return auth_header[7:].strip()


def _bearer_or_ip_key() -> str:
    """Limiter key: prefer the Bearer token, fall back to IP."""
    token = _bearer_token()
    if token:
        return f"token:{token}"
    return f"ip:{get_remote_address()}"


def _resolve_token() -> AvatarToken:
    raw = _bearer_token()
    if not raw:
        abort(401)
    try:
        token_uuid = UUID(raw)
    except ValueError:
        abort(401)
    record = AvatarToken.get(token=token_uuid)
    if record is None or record.revoked:
        abort(401)
    return record


def _avatar_base_url() -> str:
    """Canonical public origin for avatar URLs (no trailing slash): honour
    `SHARE_BASE_HOST` so URLs point at the public hostname, not Flask's
    internal bind behind the reverse proxy."""
    base_host = app.config.get("SHARE_BASE_HOST") or request.host
    return f"{base_host}"


def avatar_public_url(avatar_id: UUID) -> str:
    """Absolute cross-host wire URL for an avatar (what clients store in profile_data)."""
    return f"{_avatar_base_url()}/avatar/{avatar_id.hex}{PNG_EXTENSION}"


class AvatarUploadError(Exception):
    """A validation/moderation failure with the HTTP status to surface it as;
    keeps the shared processing core framework-agnostic."""

    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.message = message
        self.status = status


def read_avatar_upload(req, field: str = "image") -> bytes:
    """Pull and size-check the uploaded image bytes from a request.

    Raises AvatarUploadError on a missing/empty/oversized upload.
    """
    max_bytes = int(app.config.get("AVATAR_MAX_UPLOAD_BYTES", 5 * 1024 * 1024))
    content_length = req.content_length
    if content_length and content_length > max_bytes:
        raise AvatarUploadError(f"Image too large (max {max_bytes // (1024 * 1024)} MB)", 413)

    if field not in req.files:
        raise AvatarUploadError(f"Missing '{field}' field", 400)
    upload = req.files[field]
    if not upload or not upload.filename:
        raise AvatarUploadError("Empty upload", 400)

    raw = upload.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise AvatarUploadError(f"Image too large (max {max_bytes // (1024 * 1024)} MB)", 413)
    if not raw:
        raise AvatarUploadError("Empty upload", 400)
    return raw


def _screen_for_nsfw(moderation_sample: Image.Image) -> None:
    """Reject the upload if the NudeNet sidecar flags exposed nudity.

    No-op when AVATAR_NSFW_ENDPOINT is unset (local dev). Raises
    AvatarUploadError on a hit or when the sidecar is unreachable.
    """
    nsfw_endpoint = app.config.get("AVATAR_NSFW_ENDPOINT", "")
    if not nsfw_endpoint:
        return

    sample_buf = io.BytesIO()
    moderation_sample.save(sample_buf, format="JPEG", quality=90)
    try:
        resp = requests.post(
            nsfw_endpoint,
            files={"f1": ("avatar.jpg", sample_buf.getvalue(), "image/jpeg")},
            timeout=_NSFW_REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        predictions = resp.json().get("prediction") or []
    except (requests.RequestException, ValueError):
        raise AvatarUploadError("Content moderation unavailable", 503)
    # /infer returns one detection list per uploaded file; we send only f1.
    detections = predictions[0] if predictions and isinstance(predictions[0], list) else predictions
    for detection in detections:
        if not isinstance(detection, dict):
            continue
        if (detection.get("class") in _NSFW_BLOCKED_CLASSES
                and detection.get("score", 0.0) >= _NSFW_SCORE_THRESHOLD):
            raise AvatarUploadError("Image rejected by content policy", 422)


def store_avatar(raw: bytes, token: AvatarToken) -> Avatar:
    """Validate, NSFW-screen, re-encode (square PNG, metadata stripped) and persist `raw`.

    Returns the new Avatar row owned by `token`; the caller is responsible for
    ``commit()``. Raises AvatarUploadError on any rejection.
    """
    original_sha256 = hashlib.sha256(raw).hexdigest()

    Image.MAX_IMAGE_PIXELS = int(app.config.get("AVATAR_MAX_PIXELS", 4_000_000))
    try:
        with Image.open(io.BytesIO(raw)) as probe:
            probe.verify()
    except Image.DecompressionBombError:
        raise AvatarUploadError("Image dimensions exceed safety limit", 413)
    except (UnidentifiedImageError, OSError, ValueError):
        raise AvatarUploadError("Could not decode image", 400)

    # Never forward the raw upload to the sidecar: an image Pillow accepts but
    # OpenCV can't decode crashes NudeNet's inference loop, so send a re-encoded
    # baseline-JPEG moderation sample instead.
    try:
        with Image.open(io.BytesIO(raw)) as img:
            img.load()
            moderation_sample = img.convert("RGB")
            moderation_sample.thumbnail(
                (_NSFW_SAMPLE_MAX_DIM, _NSFW_SAMPLE_MAX_DIM),
                Image.Resampling.LANCZOS,
            )
            dim = int(app.config.get("AVATAR_OUTPUT_DIM", 100))
            fitted = ImageOps.fit(img.convert("RGBA"), (dim, dim), method=Image.Resampling.LANCZOS)
    except Image.DecompressionBombError:
        raise AvatarUploadError("Image dimensions exceed safety limit", 413)
    except (UnidentifiedImageError, OSError, ValueError):
        raise AvatarUploadError("Could not decode image", 400)

    _screen_for_nsfw(moderation_sample)

    upload_dir = os.path.abspath(app.config["AVATAR_UPLOAD_FOLDER"])
    os.makedirs(upload_dir, exist_ok=True)

    avatar_id = uuid.uuid4()
    final_path = os.path.abspath(os.path.join(upload_dir, f"{avatar_id.hex}{PNG_EXTENSION}"))
    if not final_path.startswith(upload_dir + os.sep):
        raise AvatarUploadError("Invalid storage path", 500)
    temp_path = final_path + ".tmp"

    fitted.info = {}
    fitted.save(temp_path, format="PNG", optimize=True)
    file_size = os.path.getsize(temp_path)
    os.replace(temp_path, final_path)

    avatar = Avatar(
        id=avatar_id,
        owner_token=token,
        mime_type="image/png",
        file_size=file_size,
        original_sha256=original_sha256,
    )
    token.last_used_at = utcnow()
    return avatar


@api_endpoints.route("/avatar/token", methods=["POST"])
@limiter.limit("5 per hour", key_func=get_remote_address)
def avatar_mint_token():
    token_uuid = uuid.uuid4()
    AvatarToken(token=token_uuid)
    commit()
    return jsonify({
        "token": str(token_uuid),
        "upload_url": f"{_avatar_base_url()}/api/avatar/upload",
    })


@api_endpoints.route("/avatar/upload", methods=["POST"])
@limiter.limit("10 per hour", key_func=_bearer_or_ip_key)
@limiter.limit("30 per hour", key_func=get_remote_address)
def avatar_upload():
    token = _resolve_token()
    try:
        raw = read_avatar_upload(request)
        avatar = store_avatar(raw, token)
    except AvatarUploadError as exc:
        return jsonify({"error": exc.message}), exc.status
    commit()
    return jsonify({"url": avatar_public_url(avatar.id)})


@app.route("/avatar/<avatar_url_id>", methods=["GET"])
def avatar_serve(avatar_url_id: str):
    """Dev-mode fallback. In production, nginx aliases /avatar/ directly."""
    if not avatar_url_id.endswith(PNG_EXTENSION):
        abort(404)
    hex_id = avatar_url_id[: -len(PNG_EXTENSION)]
    if not HEX_ID_RE.match(hex_id):
        abort(404)
    filename = f"{hex_id}{PNG_EXTENSION}"
    upload_dir = os.path.realpath(app.config["AVATAR_UPLOAD_FOLDER"])
    full_path = os.path.realpath(os.path.join(upload_dir, filename))
    if os.path.commonpath([upload_dir, full_path]) != upload_dir:
        abort(404)
    if not os.path.isfile(full_path):
        abort(404)
    return send_from_directory(
        upload_dir,
        filename,
        mimetype="image/png",
        max_age=7 * 24 * 60 * 60,
    )
