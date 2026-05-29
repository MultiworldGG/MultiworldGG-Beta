"""
Out-of-process worker that extracts option data for a single world.

Invoked as a subprocess (the GUI must not import worlds into its own
interpreter — `AutoWorldRegister` carries a lot of state). Reads one
JSON request from stdin describing the game and visibility level,
writes one JSON response to stdout.

Request (one JSON object, single line or pretty-printed):
    {
        "game_name": "A Link to the Past",
        "visibility": "simple" | "complex"
    }

Response on success:
    {
        "ok": true,
        "game_name": "A Link to the Past",
        "world": {
            "item_names": [...],
            "location_names": [...],
            "item_name_groups": {group_name: [item_names...]},
            "location_name_groups": {group_name: [location_names...]}
        },
        "groups": {
            group_name: [
                {
                    "name": option_name,
                    "type": "toggle" | "choice" | ...,
                    "display_name": str,
                    "docstring": str,
                    "default": <jsonable>,
                    # type-specific extras (see _describe_option for the
                    # full set per type)
                },
                ...
            ]
        }
    }

Response on failure:
    {"ok": false, "error": "human-readable message"}

The worker pip-installs missing apworlds via `set_game_names` before
extracting data, mirroring how `Generate.py` resolves worlds.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import traceback

logging.basicConfig(level=logging.WARNING)

# Pip / install_worlds / loader chatter would otherwise scribble onto
# stdout and corrupt the JSON channel the parent reads. Swap stdout for
# stderr for the duration of `main()`; the real stdout is preserved as
# `_JSON_OUT` and used only for the final `_emit()` call.
_JSON_OUT = sys.stdout
sys.stdout = sys.stderr


def _serialize_default(value):
    """Coerce option defaults into JSON-safe values."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_serialize_default(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _serialize_default(v) for k, v in value.items()}
    return str(value)


def _clean_docstring(text):
    if not text:
        return ""
    return " ".join(line.strip() for line in text.strip().splitlines() if line.strip())


def _describe_option(option_name, option_class):
    """Return a JSON-safe descriptor for one option class.

    Lazy-imports Options so this module is cheap to load even if a
    fast-fail happens before the worlds package is available.
    """
    import Options

    desc = {
        "name": option_name,
        "display_name": getattr(option_class, "display_name", None) or option_name,
        "docstring": _clean_docstring(getattr(option_class, "__doc__", "") or ""),
        "default": _serialize_default(getattr(option_class, "default", None)),
    }

    # Order matters: subclasses before superclasses.
    if issubclass(option_class, Options.Toggle):
        desc["type"] = "toggle"
        return desc

    if issubclass(option_class, Options.TextChoice):
        desc["type"] = "text_choice"
        desc.update(_choice_extras(option_class))
        return desc

    if issubclass(option_class, Options.Choice):
        desc["type"] = "choice"
        desc.update(_choice_extras(option_class))
        return desc

    if issubclass(option_class, Options.NamedRange):
        desc["type"] = "named_range"
        desc.update(_range_extras(option_class))
        desc["special_range_names"] = {
            str(k): int(v)
            for k, v in (getattr(option_class, "special_range_names", {}) or {}).items()
        }
        return desc

    if issubclass(option_class, Options.Range):
        desc["type"] = "range"
        desc.update(_range_extras(option_class))
        return desc

    if issubclass(option_class, Options.FreeText):
        desc["type"] = "free_text"
        return desc

    if issubclass(option_class, Options.ItemSet):
        desc["type"] = "item_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc

    if issubclass(option_class, Options.LocationSet):
        desc["type"] = "location_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc

    if issubclass(option_class, Options.OptionCounter):
        desc["type"] = "option_counter"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        desc["verify_item_name"] = bool(getattr(option_class, "verify_item_name", False))
        desc["verify_location_name"] = bool(getattr(option_class, "verify_location_name", False))
        return desc

    if issubclass(option_class, (Options.OptionSet, Options.OptionList)):
        desc["type"] = "option_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc

    if issubclass(option_class, Options.OptionDict):
        desc["type"] = "option_dict"
        return desc

    # Fallback for option subclasses we don't yet model — let the GUI
    # render a free-text field and let the user edit YAML directly.
    desc["type"] = "free_text"
    return desc


def _choice_extras(option_class):
    """Build `choices` (key -> machine name) and `display_names` (key ->
    human label) for Choice / TextChoice."""
    lookup = dict(getattr(option_class, "name_lookup", {}) or {})
    choices = {}
    display_names = {}
    for key, name in lookup.items():
        if name == "random":
            continue
        choices[str(key)] = name
        try:
            display_names[str(key)] = option_class.get_option_name(key)
        except Exception:
            display_names[str(key)] = name
    return {"choices": choices, "display_names": display_names}


def _range_extras(option_class):
    return {
        "range_start": int(getattr(option_class, "range_start", 0)),
        "range_end": int(getattr(option_class, "range_end", 100)),
    }


def _describe_world(world):
    return {
        "item_names": sorted(getattr(world, "item_names", []) or []),
        "location_names": sorted(getattr(world, "location_names", []) or []),
        "item_name_groups": {
            name: sorted(members or [])
            for name, members in (getattr(world, "item_name_groups", {}) or {}).items()
        },
        "location_name_groups": {
            name: sorted(members or [])
            for name, members in (getattr(world, "location_name_groups", {}) or {}).items()
        },
    }


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        _fail("empty request")
        return
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        _fail(f"could not parse request JSON: {e}")
        return

    game_name = req.get("game_name")
    visibility = req.get("visibility", "simple")
    if not game_name:
        _fail("missing 'game_name'")
        return

    try:
        # Heavy imports happen here — keeping them inside main keeps a
        # fast-fail on bad input cheap.
        from Utils import set_game_names, _worlds_to_load
        from mwgg_igdb import GameIndex
        import Options

        # Diagnostic: is the world even known to the index?
        known_module = GameIndex.game_names.get(game_name)
        if known_module is None:
            _fail(
                f"'{game_name}' is not listed in the game index. "
                f"Worker can't install or load it. "
                f"(Custom apworlds must be dropped into custom_worlds/.)"
            )
            return

        # set_game_names appends to _worlds_to_load and pip-installs
        # any missing wheels via ModuleUpdate.install_worlds. With
        # strict=False it logs warnings instead of raising.
        #
        # CAVEAT: set_game_names calls `importlib.util.find_spec` on
        # `worlds.<module>` to check for a bundled world before
        # installing. That side-effects an `import worlds`, which runs
        # worlds/__init__.py and its `WorldSource(...).load()` loop
        # against the current `_worlds_to_load`. By the time we install
        # the missing wheel and `worlds.<module>` is on the import path,
        # the load loop has already finished — and `from worlds import
        # AutoWorldRegister` here returns the cached module with no
        # re-load.
        #
        # Fix: after set_game_names completes, manually instantiate +
        # load WorldSource for any entries that aren't already in
        # `world_sources`. This is only safe because we're in a fresh
        # subprocess; the GUI process must never do this (it would
        # pollute AutoWorldRegister for the whole app lifetime).
        set_game_names([game_name], strict=False)

        expected_entry = f"worlds.{known_module}"
        if expected_entry not in _worlds_to_load:
            _fail(
                f"set_game_names did not queue '{game_name}' for loading. "
                f"_worlds_to_load={_worlds_to_load!r}"
            )
            return

        from worlds import (
            AutoWorldRegister,
            WorldSource,
            failed_world_loads,
            world_sources,
        )
        already_loaded = {ws.game_module for ws in world_sources}
        for entry in _worlds_to_load:
            if entry in already_loaded:
                continue
            source = WorldSource(entry)
            source.load()
            world_sources.append(source)

        world = AutoWorldRegister.world_types.get(game_name)
        if world is None:
            if expected_entry in failed_world_loads:
                _fail(
                    f"World module '{expected_entry}' failed to import. "
                    f"The pip install may have failed (offline? auth? wheel URL "
                    f"missing?). Check the parent app's log for the subprocess "
                    f"pip output."
                )
            else:
                _fail(
                    f"World '{game_name}' is queued but did not register a World "
                    f"subclass. AutoWorldRegister has "
                    f"{len(AutoWorldRegister.world_types)} types: "
                    f"{sorted(AutoWorldRegister.world_types)[:10]}…"
                )
            return

        visibility_flag = (
            Options.Visibility.complex_ui
            if visibility == "complex"
            else Options.Visibility.simple_ui
        )

        option_groups = Options.get_option_groups(world, visibility_level=visibility_flag)

        groups_out = {}
        for group_name, options in option_groups.items():
            if not options:
                continue
            descs = []
            for option_name, option_class in options.items():
                try:
                    descs.append(_describe_option(option_name, option_class))
                except Exception as e:
                    # Don't let one bad option kill the whole response.
                    logging.warning("describe_option(%s) failed: %s", option_name, e)
                    continue
            if descs:
                groups_out[group_name] = descs

        response = {
            "ok": True,
            "game_name": game_name,
            "world": _describe_world(world),
            "groups": groups_out,
        }
        _emit(response)
    except SystemExit:
        raise
    except Exception as e:
        # Worlds with broken __init__ etc. — surface to the GUI rather
        # than crashing the parent.
        _fail(f"{type(e).__name__}: {e}", trace=traceback.format_exc())


def _emit(payload):
    """Write the JSON response to the real stdout (preserved at module
    load before we redirected stdout to stderr)."""
    _JSON_OUT.write(json.dumps(payload))
    _JSON_OUT.flush()


def _fail(message, trace=None):
    payload = {"ok": False, "error": message}
    if trace:
        payload["trace"] = trace
    _emit(payload)
    sys.exit(0)  # exit 0 so the parent reads the JSON error cleanly


if __name__ == "__main__":
    main()
