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
from urllib.parse import urlparse, urlunparse
from uuid import UUID

from flask import abort, jsonify, request, send_from_directory
from flask_limiter.util import get_remote_address
from PIL import Image, ImageOps, UnidentifiedImageError

from Utils import utcnow
from WebHostLib import app, limiter
from WebHostLib.models import Avatar, AvatarToken
from . import api_endpoints


PNG_EXTENSION = ".png"
HEX_ID_RE = re.compile(r"^[0-9a-f]{32}$")


def _bearer_token() -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return ""
    return auth_header[7:].strip()


def _bearer_or_ip_key() -> str:
    """Limiter key — prefer the Bearer token, fall back to IP."""
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
    configured = (app.config.get("AVATAR_PUBLIC_BASE_URL") or "").rstrip("/")
    if configured:
        return configured
    parsed = urlparse(request.host_url)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")


@api_endpoints.route("/avatar/token", methods=["POST"])
@limiter.limit("5 per hour", key_func=get_remote_address)
def avatar_mint_token():
    token_uuid = uuid.uuid4()
    AvatarToken(token=token_uuid)
    return jsonify({
        "token": str(token_uuid),
        "upload_url": f"{_avatar_base_url()}/api/avatar/upload",
    })


@api_endpoints.route("/avatar/upload", methods=["POST"])
@limiter.limit("10 per hour", key_func=_bearer_or_ip_key)
@limiter.limit("30 per hour", key_func=get_remote_address)
def avatar_upload():
    token = _resolve_token()

    max_bytes = int(app.config.get("AVATAR_MAX_UPLOAD_BYTES", 5 * 1024 * 1024))
    content_length = request.content_length
    if content_length and content_length > max_bytes:
        return jsonify({"error": f"Image too large (max {max_bytes // (1024 * 1024)} MB)"}), 413

    if "image" not in request.files:
        return jsonify({"error": "Missing 'image' field"}), 400
    upload = request.files["image"]
    if not upload or not upload.filename:
        return jsonify({"error": "Empty upload"}), 400

    raw = upload.read(max_bytes + 1)
    if len(raw) > max_bytes:
        return jsonify({"error": f"Image too large (max {max_bytes // (1024 * 1024)} MB)"}), 413
    if not raw:
        return jsonify({"error": "Empty upload"}), 400

    original_sha256 = hashlib.sha256(raw).hexdigest()

    Image.MAX_IMAGE_PIXELS = int(app.config.get("AVATAR_MAX_PIXELS", 4_000_000))
    try:
        with Image.open(io.BytesIO(raw)) as probe:
            probe.verify()
    except Image.DecompressionBombError:
        return jsonify({"error": "Image dimensions exceed safety limit"}), 413
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "Could not decode image"}), 400

    try:
        with Image.open(io.BytesIO(raw)) as img:
            img.load()
            dim = int(app.config.get("AVATAR_OUTPUT_DIM", 512))
            fitted = ImageOps.fit(img.convert("RGBA"), (dim, dim), method=Image.Resampling.LANCZOS)
    except Image.DecompressionBombError:
        return jsonify({"error": "Image dimensions exceed safety limit"}), 413
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "Could not decode image"}), 400

    upload_dir = os.path.abspath(app.config["AVATAR_UPLOAD_FOLDER"])
    os.makedirs(upload_dir, exist_ok=True)

    avatar_id = uuid.uuid4()
    final_path = os.path.abspath(os.path.join(upload_dir, f"{avatar_id.hex}{PNG_EXTENSION}"))
    if not final_path.startswith(upload_dir + os.sep):
        return jsonify({"error": "Invalid storage path"}), 500
    temp_path = final_path + ".tmp"

    fitted.info = {}
    fitted.save(temp_path, format="PNG", optimize=True)
    file_size = os.path.getsize(temp_path)
    os.replace(temp_path, final_path)

    Avatar(
        id=avatar_id,
        owner_token=token,
        mime_type="image/png",
        file_size=file_size,
        original_sha256=original_sha256,
    )
    token.last_used_at = utcnow()

    return jsonify({"url": f"{_avatar_base_url()}/avatar/{avatar_id.hex}{PNG_EXTENSION}"})


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
