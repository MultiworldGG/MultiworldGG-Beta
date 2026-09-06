import base64
import multiprocessing
import os
import socket
import threading
import typing
import uuid

from flask import Flask, session
from flask_caching import Cache
from flask_compress import Compress
from flask_limiter import Limiter
from werkzeug.routing import BaseConverter

from Utils import title_sorted, get_file_safe_name,world_list_sorted, set_game_names
from mwgg_igdb import GameIndex
# Must run before worlds is imported. Only the main process seeds the full IGDB
# list (workers would OOM); workers narrow it per-job in autolauncher._mp_gen_game.
if multiprocessing.current_process().name == "MainProcess":
    set_game_names(list(GameIndex.game_names.keys()), strict=False)
    from worlds.AutoWorld import AutoWorldRegister

from APContainer import is_ap_player_container
from .cli import CLI



def _env_path(var: str, default: str) -> str:
    return os.path.abspath(os.environ.get(var) or default)


# Runtime data folders. The env vars give the Docker image its layout
# (Dockerfile ENV), config.yaml may override any key, and resolve_paths()
# derives the upload subfolders and creates everything once config is loaded.
UPLOAD_FOLDER = _env_path("MWGG_UPLOAD_FOLDER", "uploads")
LOGS_FOLDER = _env_path("MWGG_LOGS_FOLDER", "logs")
GENERATED_FOLDER = _env_path("MWGG_GENERATED_FOLDER",
                             os.path.join(os.path.dirname(__file__), "static", "generated"))
DB_FILE = _env_path("MWGG_DB_FILE", "ap.db3")
_UPLOAD_SUBFOLDERS = {"LOBBY_APWORLD_PATH": "lobby_apworlds", "AVATAR_UPLOAD_FOLDER": "avatars"}
DATA_FOLDER_KEYS = ("UPLOAD_FOLDER", "LOGS_FOLDER", "GENERATED_FOLDER", *_UPLOAD_SUBFOLDERS)

app = Flask(__name__)


def resolve_paths(flask_app: Flask) -> None:
    """Absolutize the data folders once config.yaml is applied and create them.

    Upload subfolders still carrying their import-time derivation follow a
    reconfigured UPLOAD_FOLDER; ones set explicitly in config are kept.
    """
    upload = os.path.abspath(flask_app.config["UPLOAD_FOLDER"])
    for key, sub in _UPLOAD_SUBFOLDERS.items():
        if flask_app.config[key] == os.path.join(UPLOAD_FOLDER, sub):
            flask_app.config[key] = os.path.join(upload, sub)
    flask_app.config["UPLOAD_FOLDER"] = upload
    for key in DATA_FOLDER_KEYS:
        flask_app.config[key] = os.path.abspath(flask_app.config[key])
        os.makedirs(flask_app.config[key], exist_ok=True)


_dynamic_tracker_lock = threading.Lock()
_dynamic_tracker_registered = False

app.jinja_env.filters['any'] = any
app.jinja_env.filters['all'] = all
app.jinja_env.filters['get_file_safe_name'] = get_file_safe_name
app.jinja_env.filters['is_applayercontainer'] = is_ap_player_container

# overwrites of flask default config
app.config["DEBUG"] = False
app.config["PORT"] = 80
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["LOGS_FOLDER"] = LOGS_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER
for _key, _sub in _UPLOAD_SUBFOLDERS.items():
    app.config[_key] = os.path.join(UPLOAD_FOLDER, _sub)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64 megabyte limit
# SECRET_KEY signs session cookies: $MWGG_SECRET_KEY, else config.yaml
# SECRET_KEY, else the hostname fallback (dev only; get_app() refuses it in prod).
app.config["SECRET_KEY"] = (
    os.environ.get("MWGG_SECRET_KEY", "").encode("utf-8")
    or bytes(socket.gethostname(), encoding="utf-8")
)
app.config["SESSION_PERMANENT"] = True
app.config["MAX_FORM_MEMORY_SIZE"] = 2 * 1024 * 1024  # 2 MB, needed for large option pages such as SC2
app.config["MAX_FORM_PARTS"] = 10_000  # Werkzeug 3.x default is 1000; games with many items can exceed this

# custom config
app.config["SELFHOST"] = True  # application process is in charge of running the websites
app.config["GENERATORS"] = 8  # maximum concurrent world gens
app.config["HOSTERS"] = 8  # maximum concurrent room hosters
app.config["SELFLAUNCH"] = True  # application process is in charge of launching Rooms.
app.config["SELFLAUNCHCERT"] = None  # can point to a SSL Certificate to encrypt Room websocket connections
app.config["SELFLAUNCHKEY"] = None  # can point to a SSL Certificate Key to encrypt Room websocket connections
app.config["SELFGEN"] = True  # application process is in charge of scheduling Generations.
app.config["GAME_PORTS"] = ["49152-65535", 0]
# at what amount of worlds should scheduling be used, instead of rolling in the web-thread
app.config["JOB_THRESHOLD"] = 1
# after what time in seconds should generation be aborted, freeing the queue slot. Can be set to None to disable.
app.config["JOB_TIME"] = 600
# maximum time in seconds since last activity for a room to be hosted
app.config["MAX_ROOM_TIMEOUT"] = 259200
# minimum time in days since last activity for a room to be deleted. 0 to disable.
app.config["ROOM_AUTO_DELETE"] = 0
# memory limit for generator processes in bytes
app.config["GENERATOR_MEMORY_LIMIT"] = 4294967296
app.config['SESSION_PERMANENT'] = True
# set worlds requested to be removed by maintainer as hidden by default
app.config['HIDDEN_WEBWORLDS'] = ["Super Mario World", "Sonic Adventure 2 Battle", "Celeste 64", "Donkey Kong Country 3", "Celeste (Open World)"]

# waitress uses one thread for I/O, these are for processing of views that then get sent
# multiworld.gg uses gunicorn + nginx; ignoring this option
app.config["WAITRESS_THREADS"] = 10
# a default that just works. multiworld.gg runs on postgresql.
# PONY key kept for backward-compatibility with config.yaml files;
# get_app() in WebHost.py converts it to SQLALCHEMY_DATABASE_URI.
app.config["PONY"] = {
    'provider': 'sqlite',
    'filename': DB_FILE,
    'create_db': True
}
# flask-sqlalchemy configuration; populated by get_app() from the PONY dict
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_ROLL"] = 20
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes default
app.config["CACHE_KEY_PREFIX"] = "multiworld_"
app.config["HOST_ADDRESS"] = ""
app.config["ASSET_RIGHTS"] = False
app.config["MONITORING_ADMIN_TOKEN"] = None  # Admin token for monitoring API endpoints
# Canonical public host (no scheme, no trailing slash) used to render
# shareable URLs like the /r/<short> room link.
app.config["SHARE_BASE_HOST"] = ""

# Profile-picture uploader (see WebHostLib/api/avatar.py); public URL origin
# comes from SHARE_BASE_HOST above.
app.config["AVATAR_MAX_UPLOAD_BYTES"] = 5 * 1024 * 1024
app.config["AVATAR_MAX_PIXELS"] = 4_000_000
app.config["AVATAR_OUTPUT_DIM"] = 100
# NudeNet moderation sidecar (deploy/docker-compose.yml `nudenet` service);
# empty disables screening (local dev without the sidecar).
app.config["AVATAR_NSFW_ENDPOINT"] = os.environ.get("AVATAR_NSFW_ENDPOINT", "")
# Replaced avatars are never deleted (their URLs stay pinned to slots and in
# clients); the autohost prunes ones this old that nothing uses. 0 disables.
app.config["AVATAR_RETENTION_DAYS"] = 180
# Hosts whose avatar URLs we render (HTTPS only); mirrors the desktop client's
# safe_avatar_source allowlist. SHARE_BASE_HOST is trusted implicitly.
app.config["AVATAR_TRUSTED_HOSTS"] = ("multiworld.gg", "mw.prismativerse.com")

# WebAuthn / passkey recovery (see WebHostLib/passkeys.py). Production MUST
# override RP_ID / ORIGIN: browsers reject mismatched RP_IDs and non-localhost HTTP.
app.config["WEBAUTHN_RP_ID"] = "localhost"
app.config["WEBAUTHN_ORIGIN"] = "http://localhost:5050"
app.config["WEBAUTHN_RP_NAME"] = "MultiworldGG"
# Derives the stable opaque per-session user-handle for the OS passkey picker;
# production should set a dedicated random secret (falls back to SECRET_KEY).
app.config["WEBAUTHN_USER_HANDLE_SECRET"] = None  # resolved in register()

cache = Cache()
Compress(app)
CLI(app)

# Basic Rate Limiter for lobbies
limiter = Limiter(
    key_func=lambda s=session: s.get("_id", "") or "",
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

def to_python(value: str) -> uuid.UUID:
    if "=" in value or any(c.isspace() for c in value):
        raise ValueError("Invalid UUID format")
    return uuid.UUID(bytes=base64.urlsafe_b64decode(value + '=' * (-len(value) % 4)))


def to_url(value: uuid.UUID) -> str:
    return base64.urlsafe_b64encode(value.bytes).rstrip(b'=').decode('ascii')


class B64UUIDConverter(BaseConverter):

    def to_python(self, value: str) -> uuid.UUID:
        return to_python(value)

    def to_url(self, value: typing.Any) -> str:
        assert isinstance(value, uuid.UUID)
        return to_url(value)


# short UUID
app.url_map.converters["suuid"] = B64UUIDConverter
app.jinja_env.filters["suuid"] = to_url
app.jinja_env.filters["title_sorted"] = title_sorted
app.jinja_env.filters["world_list_sorted"] = world_list_sorted


def register() -> None:
    """Import submodules, triggering their registering on flask routing.
    Note: initializes worlds subsystem."""
    import importlib

    from werkzeug.utils import find_modules

    from WebHostLib.customserver import run_server_process

    for module in find_modules("WebHostLib", include_packages=True):
        importlib.import_module(module)

    from . import api
    app.register_blueprint(api.api_endpoints)

    from .route_redirects import legacy_routes
    app.register_blueprint(legacy_routes)

    from .short_room_route import short_room
    app.add_url_rule("/r/<short>", "short_room", short_room)

    # Passkey blueprint: $MWGG_WEBAUTHN_HANDLE_SECRET, else config.yaml value,
    # else SECRET_KEY (passkey clustering then rotates with the signing key).
    from .passkeys import passkeys_bp
    from .models import db as _db
    from .passkey_store import SQLAlchemyCredentialStore
    env_handle_secret = os.environ.get("MWGG_WEBAUTHN_HANDLE_SECRET", "")
    if env_handle_secret:
        app.config["WEBAUTHN_USER_HANDLE_SECRET"] = env_handle_secret.encode("utf-8")
    elif not app.config.get("WEBAUTHN_USER_HANDLE_SECRET"):
        app.config["WEBAUTHN_USER_HANDLE_SECRET"] = app.config["SECRET_KEY"]
    passkeys_bp.credential_store = SQLAlchemyCredentialStore(lambda: _db.session)
    app.register_blueprint(passkeys_bp)

    from .scripts.backfill_short_ids import register_cli
    register_cli(app)

    @app.before_request
    def _ensure_dynamic_tracker_routes():
        global _dynamic_tracker_registered
        if _dynamic_tracker_registered:
            return
        with _dynamic_tracker_lock:
            if _dynamic_tracker_registered:
                return
            from .tracker import _register_dynamic_tracker_routes
            _register_dynamic_tracker_routes()
            _dynamic_tracker_registered = True
