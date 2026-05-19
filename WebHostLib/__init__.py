import base64
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

from Utils import title_sorted, get_file_safe_name,world_list_sorted, set_game_names, add_bundled_worlds
from mwgg_igdb import GameIndex
# Must be done before worlds is imported
set_game_names(list(GameIndex.game_names.keys()), strict=False)

add_bundled_worlds(("tracker", "_manual", "_bizhawk", "_sni", "_debug", "generic"))

from APContainer import is_ap_player_container
from .cli import CLI

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)
LOBBY_APWORLD_FOLDER = os.path.join(UPLOAD_FOLDER, "lobby_apworlds")
os.makedirs(LOBBY_APWORLD_FOLDER, exist_ok=True)
AVATAR_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "avatars")
os.makedirs(AVATAR_UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

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
app.config["LOBBY_APWORLD_PATH"] = os.path.abspath(LOBBY_APWORLD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64 megabyte limit
# if you want to deploy, make sure you have a non-guessable secret key
app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
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
# at what amount of worlds should scheduling be used, instead of rolling in the web-thread
app.config["JOB_THRESHOLD"] = 1
# after what time in seconds should generation be aborted, freeing the queue slot. Can be set to None to disable.
app.config["JOB_TIME"] = 600
# maximum time in seconds since last activity for a room to be hosted
app.config["MAX_ROOM_TIMEOUT"] = 259200
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
    'filename': os.path.abspath('ap.db3'),
    'create_db': True
}
# flask-sqlalchemy configuration — populated by get_app() from the PONY dict
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath('ap.db3')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_ROLL"] = 20
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes default
app.config["CACHE_KEY_PREFIX"] = "multiworld_"
app.config["HOST_ADDRESS"] = ""
app.config["ASSET_RIGHTS"] = False
app.config["MONITORING_ADMIN_TOKEN"] = None  # Admin token for monitoring API endpoints

# Profile-picture uploader (see WebHostLib/api/avatar.py)
app.config["AVATAR_UPLOAD_FOLDER"] = os.path.abspath(AVATAR_UPLOAD_FOLDER)
app.config["AVATAR_PUBLIC_BASE_URL"] = ""        # empty -> derive from request.host_url
app.config["AVATAR_MAX_UPLOAD_BYTES"] = 5 * 1024 * 1024
app.config["AVATAR_MAX_PIXELS"] = 4_000_000
app.config["AVATAR_OUTPUT_DIM"] = 512

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
