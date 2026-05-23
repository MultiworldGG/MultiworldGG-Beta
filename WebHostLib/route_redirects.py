"""
Legacy URL redirects for MultiWorldGG.

Every URL the site exposed before the route migration continues to work via a
301 redirect to the new canonical location. The destinations are computed
through ``url_for(...)`` so this module never needs editing if route paths
change again later.

Register on the app once::

    from WebHostLib.route_redirects import legacy_routes
    app.register_blueprint(legacy_routes)

After Phase 1 of the migration ships, all entries here should hit 301s in
production and the test suite should keep them all green.
"""

from flask import Blueprint, abort, redirect, url_for

legacy_routes = Blueprint("legacy_routes", __name__)


# ---------------------------------------------------------------------------
# Static one-to-one renames
# ---------------------------------------------------------------------------

_RENAMES = {
    # old path             # endpoint to redirect to
    "/start-playing":     "play_hub",
    "/generate":          "generate",
    "/uploads":           "uploads",
    "/check":             "check",
    "/lobbies":           "lobby_list",
    "/user-content":      "me",
}


def _make_static_redirect(endpoint):
    def view():
        return redirect(url_for(endpoint), code=301)
    return view


for old_path, target_endpoint in _RENAMES.items():
    # Use a stable per-path endpoint name to avoid Flask's "view function name
    # collision" errors when this module is reloaded in dev.
    endpoint_name = f"legacy__{old_path.strip('/').replace('-', '_').replace('/', '__') or 'root'}"
    legacy_routes.add_url_rule(
        old_path,
        endpoint=endpoint_name,
        view_func=_make_static_redirect(target_endpoint),
    )


# ---------------------------------------------------------------------------
# /learn/* — both the hub root and the tutorial-index root now require a
# <lang> segment. Old language-less URLs redirect to the English equivalents.
# ---------------------------------------------------------------------------

@legacy_routes.route("/learn")
def legacy_learn_hub_root():
    return redirect(url_for("learn_hub", lang="en"), code=301)


@legacy_routes.route("/learn/tutorials")
def legacy_tutorial_landing_root():
    return redirect(url_for("tutorial_landing", lang="en"), code=301)


@legacy_routes.route("/tutorial")
def legacy_tutorial_root():
    return redirect(url_for("tutorial_landing", lang="en"), code=301)


# ---------------------------------------------------------------------------
# Parameterized redirects
# ---------------------------------------------------------------------------

@legacy_routes.route("/lobby/<suuid:lobby>")
def legacy_lobby(lobby):
    return redirect(url_for("lobby_view", lobby=lobby), code=301)


@legacy_routes.route("/seed/<suuid:seed>")
def legacy_seed(seed):
    return redirect(url_for("view_seed", seed=seed), code=301)


@legacy_routes.route("/room/<suuid:room>")
def legacy_room(room):
    """
    The canonical room URL is now ``/play/seed/<seed_id>/room/<room_id>``.
    The seed ID isn't in the old URL, so we look it up. If the room doesn't
    exist anymore, 404 — the redirect chain shouldn't fabricate a destination.
    """
    # Import locally to avoid a circular import at module load time. Tests
    # patch this with a fixture, so production callers get the real model.
    from WebHostLib.models import Room  # noqa: WPS433

    room_obj = Room.get(id=room)
    if not room_obj:
        abort(404)
    return redirect(
        url_for("host_room", seed=room_obj.seed_id, room=room_obj.id),
        code=301,
    )


@legacy_routes.route("/faq/<lang>/")
@legacy_routes.route("/faq/<lang>")
def legacy_faq(lang):
    return redirect(url_for("faq", lang=lang), code=301)


@legacy_routes.route("/glossary/<lang>")
def legacy_glossary(lang):
    return redirect(url_for("glossary", lang=lang), code=301)


# Tutorial path redirects live on the ``tutorial_legacy_*`` view functions in
# WebHostLib/misc.py (not in this blueprint) because they share the
# ``/tutorial/...`` URL prefix with the canonical tutorial endpoint and the
# split-suffix logic is easier to keep colocated with it.


@legacy_routes.route("/games/info/<game>")
def legacy_game_info(game):
    return redirect(url_for("game_info", game=game), code=301)
