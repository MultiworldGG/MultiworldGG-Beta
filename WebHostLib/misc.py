from __future__ import annotations

import datetime
import os
import warnings
from enum import StrEnum
from typing import Any, IO, Dict, Iterator, List, Tuple, Union, TYPE_CHECKING

import jinja2.exceptions
from flask import request, redirect, url_for, render_template, Response, session, abort, send_from_directory
from mwgg_igdb import GameIndex
from sqlalchemy import select, func
from werkzeug.utils import secure_filename
from Utils import __version__

from . import app, cache
from .markdown import render_markdown
from .models import Seed, Room, Command, UUID, uuid4, db, commit
from .short_id import assign_short_id
from Utils import title_sorted, utcnow

if TYPE_CHECKING:
    from worlds.AutoWorld import World

class WebWorldTheme(StrEnum):
    DIRT = "dirt"
    GRASS = "grass"
    GRASS_FLOWERS = "grassFlowers"
    ICE = "ice"
    JUNGLE = "jungle"
    OCEAN = "ocean"
    PARTY_TIME = "partyTime"
    STONE = "stone"

def get_world_theme(game_name: str) -> str:
    from worlds.AutoWorld import AutoWorldRegister
    if game_name not in AutoWorldRegister.world_types:
        return "grass"
    chosen_theme = AutoWorldRegister.world_types[game_name].web.theme
    available_themes = [theme.value for theme in WebWorldTheme]
    if chosen_theme not in available_themes:
        warnings.warn(f"Theme '{chosen_theme}' for {game_name} not valid, switching to default 'grass' theme.")
        return "grass"
    return chosen_theme


def format_authors_string(authors: list[str]) -> str:
    """Format a list of authors with proper grammar (commas and &)."""
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} & {authors[1]}"
    return f"{', '.join(authors[:-1])} & {authors[-1]}"


def get_world_version(world: type(World)) -> str:
    """Get the world version from archipelago.json manifest, if it exists and is not 0.0.0."""
    try:
        import json
        import pkgutil

        # Get the world's module path
        world_module = world.__module__
        if world_module.startswith('worlds.'):
            # Try to load archipelago.json from the world folder
            try:
                manifest_data = pkgutil.get_data(world_module, 'archipelago.json')
                if manifest_data:
                    manifest = json.loads(manifest_data.decode('utf-8-sig'))
                    # Prefer world_version_full if it exists
                    if 'world_version_full' in manifest and manifest['world_version_full']:
                        return f"{manifest['world_version_full']}"
                    elif 'world_version' in manifest and manifest['world_version']:
                        world_version = manifest['world_version']
                        # Don't show version if it's 0.0.0
                        if world_version != "0.0.0":
                            return f"{world_version}"
            except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
                pass
    except (ImportError, AttributeError, OSError):
        pass

    return ""


def get_world_authors(world: type(World)) -> str:
    """Get the formatted authors string for a world, preferring manifest authors over the author field."""
    # Try to load manifest data first
    try:
        import json
        import os
        import pkgutil
        
        # Get the world's module path
        world_module = world.__module__
        if world_module.startswith('worlds.'):
            world_folder = world_module[7:]  # Remove 'worlds.' prefix
            world_path = os.path.join('worlds', world_folder)
            
            # Try to load archipelago.json from the world folder
            try:
                manifest_data = pkgutil.get_data(world_module, 'archipelago.json')
                if manifest_data:
                    manifest = json.loads(manifest_data.decode('utf-8-sig'))
                    if 'authors' in manifest and manifest['authors']:
                        return format_authors_string(manifest['authors'])
            except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
                pass
    except (ImportError, AttributeError, OSError):
        pass
    
    # Fallback to the author field
    return getattr(world, 'author', '')


# Age-rating tiers mirror VARIANT_FILTERS in MultiworldGG-Index scripts/build_variants.py:
# sixteen tier listed by default, nsfw tier behind the client-side toggle, AO/unindexed never.
SIXTEEN_AGE_RATINGS = frozenset({"MW", "3", "7", "12", "16", "E", "T"})
NSFW_AGE_RATINGS = frozenset({"18", "M", "NR"})
LISTED_AGE_RATINGS = SIXTEEN_AGE_RATINGS | NSFW_AGE_RATINGS


def get_game_age_rating(game: str) -> str | None:
    module = GameIndex.game_names.get(game)
    return GameIndex.get_game(module).get("age_rating") if module else None


def is_game_nsfw(game: str) -> bool:
    return get_game_age_rating(game) in NSFW_AGE_RATINGS


def get_visible_worlds() -> dict[str, type(World)]:
    from worlds.AutoWorld import AutoWorldRegister
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if (not world.hidden and game not in app.config["HIDDEN_WEBWORLDS"]
                and get_game_age_rating(game) in LISTED_AGE_RATINGS):
            worlds[game] = world
    return worlds


@app.template_filter("relative_time")
def relative_time(dt: datetime.datetime | None) -> str:
    """Render a (tz-naive UTC) datetime as a relative string like '2 min ago'.

    Matches the convention in Utils.utcnow(): model timestamps are tz-naive UTC.
    """
    if not dt:
        return ""
    # If we receive a tz-aware value, drop the tz to align with utcnow()'s naive output.
    if dt.tzinfo is not None:
        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    seconds = int((utcnow() - dt).total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60} min ago"
    if seconds < 86400:
        return f"{seconds // 3600} hr ago"
    if seconds < 172800:
        return "Yesterday"
    days = seconds // 86400
    if days < 7:
        return f"{days} days ago"
    return dt.strftime("%b %d")


def get_world_display_name(game: str) -> str:
    """Return the WebWorld display_name for a game, falling back to the game key."""
    from worlds.AutoWorld import AutoWorldRegister
    world = AutoWorldRegister.world_types.get(game)
    if world is None:
        return game
    return getattr(world.web, "display_name", None) or world.game


def get_tutorial_name(game: str, file_base: str, lang: str | None = None) -> str | None:
    """Return the tutorial_name for a given URL file base under a game, or None if not found.

    The URL carries the language separately, so ``file_base`` is the bare slug
    (``"setup"``) while the declared file names keep the suffix (``"setup_en.md"``);
    they have to be compared after the split. Translations may name the guide in
    their own language, so ``lang`` selects that entry, falling back to the first
    one declared for the base.
    """
    from worlds.AutoWorld import AutoWorldRegister
    world = AutoWorldRegister.world_types.get(game)
    if world is None or not hasattr(world.web, "tutorials"):
        return None
    fallback = None
    for tutorial in world.web.tutorials:
        if not hasattr(tutorial, "tutorial_name"):
            continue
        base, tutorial_lang = _split_tutorial_file(secure_filename(tutorial.file_name).rsplit(".", 1)[0])
        if base != file_base:
            continue
        if tutorial_lang == lang:
            return tutorial.tutorial_name
        if fallback is None:
            fallback = tutorial.tutorial_name
    return fallback


@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(err):
    return render_template('404.html'), 404


# Play hub - landing page for /play, six action cards
@app.route('/play')
@cache.cached()
def play_hub():
    return render_template("play_hub.html")


@app.route('/games/<string:game>')
@cache.cached()
def game_info(game):
    """Game Info Pages"""
    try:
        theme = get_world_theme(game)
        secure_game_name = secure_filename(game)
        lang = "en"
        file_dir = os.path.join(app.static_folder, "generated", "docs", secure_game_name)
        file_dir_url = url_for("static", filename=f"generated/docs/{secure_game_name}")
        document = render_markdown(os.path.join(file_dir, f"{lang}_{secure_game_name}.md"), file_dir_url)
        return render_template(
            "markdown_document.html",
            title=f"{game} Guide",
            html_from_markdown=document,
            theme=theme,
            breadcrumb_crumbs=[
                ("Games", url_for("games")),
                (get_world_display_name(game), None),
            ],
        )
    except FileNotFoundError:
        return abort(404)


@app.route('/games')
@cache.cached()
def games():
    """List of supported games"""
    return render_template("supportedGames.html", worlds=get_visible_worlds(), get_world_authors=get_world_authors, get_world_version=get_world_version, is_game_nsfw=is_game_nsfw)


def _split_tutorial_file(file: str, default_lang: str = "en") -> tuple[str, str]:
    """Split a tutorial file slug into ``(base, lang)``.

    ``"setup_en"`` -> ``("setup", "en")``;
    ``"advanced_settings_en"`` -> ``("advanced_settings", "en")``;
    ``"intro"`` -> ``("intro", "en")`` (no suffix, default).

    Uses ``rpartition`` so only the rightmost ``_`` is considered, and
    only treats the suffix as a language if it's a 2-letter alpha token.
    """
    base, sep, maybe_lang = file.rpartition('_')
    if sep and base and len(maybe_lang) == 2 and maybe_lang.isalpha():
        return base, maybe_lang
    return file, default_lang


def get_tutorial_languages(game: str, file_base: str, current_lang: str) -> list[dict[str, Any]]:
    """Return the languages a tutorial is available in, as switcher entries.

    Discovery mirrors ``tutorial_landing``: every ``web.tutorials`` entry whose
    file slug shares ``file_base`` is the same guide in another language. Returns
    an empty list when there is nothing to switch between, so the template can
    skip the control entirely.
    """
    from worlds.AutoWorld import AutoWorldRegister
    world = AutoWorldRegister.world_types.get(game)
    if world is None or not hasattr(world.web, "tutorials"):
        return []
    languages: dict[str, dict[str, Any]] = {}
    for tutorial in world.web.tutorials:
        if not hasattr(tutorial, "tutorial_name"):
            continue
        base, lang = _split_tutorial_file(secure_filename(tutorial.file_name).rsplit(".", 1)[0])
        if base != file_base or lang in languages:
            continue
        languages[lang] = {
            "lang": lang,
            "language": tutorial.language,
            "url": url_for("tutorial", lang=lang, game=game, file=base),
            "current": lang == current_lang,
        }
    return list(languages.values()) if len(languages) > 1 else []


_SETUP_TUTORIAL_HINTS = ("setup", "start guide")


def _resolve_setup_tutorial(game: str, lang: str, file_dir: str) -> tuple[str, str] | None:
    """Resolve the ``setup`` slug to the guide a world actually declares.

    Prefers ``lang``, crossing languages only when it has none. Matches on
    ``tutorial_name``, first-match-wins: A Link to the Past declares "Multiworld
    Setup Guide" ahead of "MSU-1 Setup Guide", which matches too. Candidates
    with no file on disk are skipped, so this cannot resolve to its own URL.
    """
    from worlds.AutoWorld import AutoWorldRegister
    world = AutoWorldRegister.world_types.get(game)
    if world is None or not hasattr(world.web, "tutorials"):
        return None

    candidates: list[tuple[str, str, str]] = []
    for tutorial in world.web.tutorials:
        if not hasattr(tutorial, "tutorial_name"):
            continue
        file_base, file_lang = _split_tutorial_file(secure_filename(tutorial.file_name).rsplit(".", 1)[0])
        candidates.append((file_base, file_lang, (tutorial.tutorial_name or "").lower()))

    pool = [candidate for candidate in candidates if candidate[1] == lang] or candidates
    for file_base, file_lang, _name in sorted(
            pool, key=lambda c: not any(hint in c[2] for hint in _SETUP_TUTORIAL_HINTS)):
        if os.path.isfile(os.path.join(file_dir, f"{file_base}_{file_lang}.md")):
            return file_base, file_lang
    return None


@app.route('/learn/<string:lang>/tutorial/<string:game>/<string:file>')
@cache.cached()
def tutorial(lang: str, game: str, file: str):
    """Render a tutorial markdown file for the given language.

    Reads ``static/generated/docs/<game>/<file>_<lang>.md``: the on-disk layout
    keeps the suffix form; the URL exposes the language as a path segment.

    A missing ``setup`` file 302s to the guide the world does declare.
    """
    try:
        theme = get_world_theme(game)
        secure_game_name = secure_filename(game)
        secure_file = secure_filename(file)
        secure_lang = secure_filename(lang)
        file_dir = os.path.join(app.static_folder, "generated", "docs", secure_game_name)
        file_dir_url = url_for("static", filename=f"generated/docs/{secure_game_name}")
        document = render_markdown(os.path.join(file_dir, f"{secure_file}_{secure_lang}.md"), file_dir_url)
        return render_template(
            "markdown_document.html",
            title=f"{game} Guide",
            html_from_markdown=document,
            theme=theme,
            tutorial_languages=get_tutorial_languages(game, file, lang),
            breadcrumb_crumbs=[
                ("Learn", url_for("learn_hub", lang=lang)),
                ("Setup guides", url_for("tutorial_landing", lang=lang)),
                (get_world_display_name(game), url_for("game_info", game=game)),
                (get_tutorial_name(game, file, lang) or file, None),
            ],
        )
    except FileNotFoundError:
        # Only "setup"; a general alias would mask 404s from typo'd links.
        if secure_file == "setup":
            resolved = _resolve_setup_tutorial(game, secure_lang, file_dir)
            if resolved:
                return redirect(url_for("tutorial", lang=resolved[1], game=game, file=resolved[0]))
        return abort(404)


@app.route('/tutorial/<string:game>/<string:file>')
def tutorial_legacy_no_lang(game: str, file: str):
    """301-redirect ``/tutorial/<game>/<file>`` to the new canonical URL.

    If ``file`` ends in ``_<2-letter-lang>``, the suffix is peeled off and
    surfaced as the ``lang`` path segment. Otherwise defaults to ``en``.
    """
    base, lang = _split_tutorial_file(file)
    return redirect(url_for("tutorial", lang=lang, game=game, file=base), code=301)


@app.route('/tutorial/<string:game>/<string:file>/<string:lang>')
def tutorial_legacy_trailing_lang(game: str, file: str, lang: str):
    """301-redirect ``/tutorial/<game>/<file>/<lang>`` straight to the new
    canonical URL, with no double-hop through the suffix form.
    """
    return redirect(url_for("tutorial", lang=lang, game=game, file=file), code=301)


# Learn hub - landing page for /learn/<lang>, three top-level guides
@app.route('/learn/<string:lang>')
@cache.cached()
def learn_hub(lang: str):
    # 2-letter alpha codes, matching _split_tutorial_file. No content lookup at
    # this layer; the hub is language-neutral chrome around per-language links.
    if not (len(lang) == 2 and lang.isalpha()):
        abort(404)
    return render_template("learn_hub.html", lang=lang)


# Setup tutorials index - full per-world list
@app.route('/learn/<string:lang>/tutorials')
@cache.cached()
def tutorial_landing(lang: str):
    if not (len(lang) == 2 and lang.isalpha()):
        abort(404)
    from worlds.AutoWorld import AutoWorldRegister
    tutorials = {}
    worlds = AutoWorldRegister.world_types

    # Filter worlds based on hidden webworlds config. Unindexed worlds (e.g. the
    # generic Archipelago meta world) stay listed; AO-rated games never show.
    visible_worlds = {name: world for name, world in worlds.items()
                     if name not in app.config["HIDDEN_WEBWORLDS"]
                     and get_game_age_rating(name) != "AO"}

    for world_name, world_type in visible_worlds.items():
        current_world = tutorials[world_name] = {}
        if hasattr(world_type.web, 'tutorials'):
            for tutorial in world_type.web.tutorials:
                # Skip if tutorial is not a Tutorial object (e.g., if it's a string)
                if not hasattr(tutorial, 'tutorial_name'):
                    continue

                current_tutorial = current_world.setdefault(tutorial.tutorial_name, {
                    "description": tutorial.description, "files": {}})

                # Get the file name without extension for the new format
                file_key = secure_filename(tutorial.file_name).rsplit(".", 1)[0]

                # file_key "setup_en" splits to ("setup", "en") so the template
                # can build /learn/en/tutorial/<game>/setup.
                file_base, file_lang = _split_tutorial_file(file_key)

                file_data = {
                    "authors": tutorial.authors,
                    "language": tutorial.language,
                    "file_name": file_key,
                    "file_base": file_base,
                    "lang": file_lang,
                    "legacy_link": tutorial.link if tutorial.link != "unused" else None
                }

                current_tutorial["files"][file_key] = file_data
    tutorials = {world_name: tutorials for world_name, tutorials in title_sorted(
        tutorials.items(), key=lambda element: "\x00" if element[0] == "Archipelago" else (getattr(visible_worlds[element[0]].web, 'display_name', None) or visible_worlds[element[0]].game))}

    # Sort the worlds dictionary by display name for consistent ordering
    sorted_worlds = dict(title_sorted(
        visible_worlds.items(),
        key=lambda element: "\x00" if element[0] == "Archipelago" else (getattr(element[1].web, 'display_name', None) or element[1].game)
    ))

    return render_template("tutorialLanding.html", worlds=sorted_worlds, tutorials=tutorials, lang=lang, is_game_nsfw=is_game_nsfw)


@app.route('/learn/<string:lang>/faq')
@cache.cached()
def faq(lang: str):
    document = render_markdown(os.path.join(app.static_folder, "assets", "faq", secure_filename(lang)+".md"))
    return render_template(
        "markdown_document.html",
        title="Frequently Asked Questions",
        html_from_markdown=document,
        breadcrumb_crumbs=[
            ("Learn", url_for("learn_hub", lang=lang)),
            ("FAQ", None),
        ],
    )


@app.route('/learn/<string:lang>/glossary')
@cache.cached()
def glossary(lang: str):
    document = render_markdown(os.path.join(app.static_folder, "assets", "glossary", secure_filename(lang)+".md"))
    return render_template(
        "markdown_document.html",
        title="Glossary",
        html_from_markdown=document,
        breadcrumb_crumbs=[
            ("Learn", url_for("learn_hub", lang=lang)),
            ("Glossary", None),
        ],
    )


@app.route('/learn/<string:lang>/quickstart')
@cache.cached()
def quickstart(lang: str):
    try:
        document = render_markdown(
            os.path.join(app.static_folder, "assets", "quickstart", secure_filename(lang)+".md"))
    except FileNotFoundError:
        abort(404)
    return render_template(
        "markdown_document.html",
        title="Quickstart Guide",
        html_from_markdown=document,
        breadcrumb_crumbs=[
            ("Learn", url_for("learn_hub", lang=lang)),
            ("Quickstart", None),
        ],
    )


@app.route('/play/seed/<suuid:seed>')
def view_seed(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    from .models import Slot
    slot_count = db.session.scalar(
        select(func.count()).select_from(Slot).where(Slot.seed_id == seed.id)
    ) or 0
    return render_template("viewSeed.html", seed=seed, slot_count=slot_count)


@app.route('/new_room/<suuid:seed>')
def new_room(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    room = Room(seed_id=seed.id, owner=session["_id"], tracker=uuid4())
    assign_short_id(db.session, room)
    commit()
    return redirect(url_for("host_room", seed=room.seed_id, room=room.id))

# strict_slashes=False: the auto-308 for a missing slash builds an absolute URL
# from the proxied Host header, which can point at the upstream loopback.
@app.route('/downloads/', strict_slashes=False)
@cache.cached()
def downloads():
    return render_template("clients.html", version=__version__)


@app.route('/legal/', strict_slashes=False)
@cache.cached()
def legal():
    return render_template("legal.html")


def _read_log(log: IO[Any], offset: int = 0) -> Iterator[bytes]:
    marker = log.read(3)  # skip optional BOM
    if marker != b'\xEF\xBB\xBF':
        log.seek(0, os.SEEK_SET)
    log.seek(offset, os.SEEK_CUR)
    yield from log
    log.close()  # free file handle as soon as possible


@app.route('/log/<suuid:room>')
def display_log(room: UUID) -> Union[str, Response, Tuple[str, int]]:
    from .ownership import is_authorized
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    if is_authorized(room, session["_id"]):
        file_path = os.path.join("logs", str(room.id) + ".txt")
        try:
            log = open(file_path, "rb")
            range_header = request.headers.get("Range")
            if range_header:
                range_type, range_values = range_header.split('=')
                start, end = map(str.strip, range_values.split('-', 1))
                if range_type != "bytes" or end != "":
                    return "Unsupported range", 500
                # NOTE: we skip Content-Range in the response here, which isn't great but works for our JS
                return Response(_read_log(log, int(start)), mimetype="text/plain", status=206)
            return Response(_read_log(log), mimetype="text/plain")
        except FileNotFoundError:
            return Response(f"Logfile {file_path} does not exist. "
                            f"Likely a crash during spinup of multiworld instance or it is still spinning up.",
                            mimetype="text/plain")

    return "Access Denied", 403


@app.post("/play/seed/<suuid:seed>/room/<suuid:room>")
def host_room_command(seed: UUID, room: UUID):
    from .ownership import is_authorized
    room: Room = Room.get(id=room)
    if room is None or room.seed_id != seed:
        return abort(404)

    if is_authorized(room, session["_id"]):
        cmd = request.form["cmd"]
        if cmd:
            Command(room_id=room.id, commandtext=cmd)
            commit()
    return redirect(url_for("host_room", seed=room.seed_id, room=room.id))


@app.get("/play/seed/<suuid:seed>/room/<suuid:room>")
def host_room(seed: UUID, room: UUID):
    room: Room = Room.get(id=room)
    if room is None or room.seed_id != seed:
        return abort(404)

    now = utcnow()
    # indicate that the page should reload to get the assigned port
    should_refresh = (
        (not room.last_port and now - room.creation_time < datetime.timedelta(seconds=3))
        or room.last_activity < now - datetime.timedelta(seconds=room.timeout)
    )
    if now - room.last_activity > datetime.timedelta(minutes=1):
        # we only set last_activity if needed to avoid concurrent-write conflicts
        room.last_activity = now  # will trigger a spinup, if it's not already running
        commit()

    browser_tokens = "Mozilla", "Chrome", "Safari"
    automated = ("update" in request.args
                 or "Discordbot" in request.user_agent.string
                 or not any(browser_token in request.user_agent.string for browser_token in browser_tokens))

    def get_log(max_size: int = 0 if automated else 1024000) -> Tuple[str, int]:
        if max_size == 0:
            return "…", 0
        try:
            with open(os.path.join("logs", str(room.id) + ".txt"), "rb") as log:
                raw_size = 0
                fragments: List[str] = []
                for block in _read_log(log):
                    if raw_size + len(block) > max_size:
                        fragments.append("…")
                        break
                    raw_size += len(block)
                    fragments.append(block.decode("utf-8"))
                return "".join(fragments), raw_size
        except FileNotFoundError:
            return "", 0

    from .ownership import is_authorized, is_primary_owner
    is_authorized_room = is_authorized(room, session["_id"])
    is_primary_owner_room = is_primary_owner(room, session["_id"])
    return render_template(
        "hostRoom.html",
        room=room,
        should_refresh=should_refresh,
        get_log=get_log,
        is_authorized_room=is_authorized_room,
        is_primary_owner_room=is_primary_owner_room,
    )


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static", "static"),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/discord')
def discord():
    return redirect("https://discord.multiworld.gg")


@app.route('/datapackage')
@cache.cached()
def get_datapackage():
    """A pretty print version of /api/datapackage"""
    from worlds import network_data_package
    import json
    return Response(json.dumps(network_data_package, indent=4), mimetype="text/plain")

@app.route('/datapackage/<game_name>')
@cache.cached()
def get_datapackage_single(game_name):
    """A pretty print version of /api/datapackage, filtered by an individual game"""
    from worlds import network_data_package_single_game
    import json
    pkg = network_data_package_single_game.get(game_name)
    if pkg is None:
        abort(404, description=f"Game '{game_name}' not found")
    return Response(json.dumps(pkg, indent=4), mimetype='text/plain')

@app.route('/index')
@app.route('/sitemap')
@cache.cached()
def get_sitemap():
    from worlds.AutoWorld import AutoWorldRegister
    available_games: List[Dict[str, Union[str, bool]]] = []
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden and not game in app.config["HIDDEN_WEBWORLDS"]:
            has_settings: bool = isinstance(world.web.options_page, bool) and world.web.options_page
            available_games.append({ 'title': game, 'has_settings': has_settings })
    return render_template("siteMap.html", games=available_games)
