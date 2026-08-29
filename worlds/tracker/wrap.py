"""Universal Tracker overlay for game-specific clients.

When the launcher's "Universal Tracker" checkbox is set alongside a game
module, ``CommonContext.__init__`` calls ``attach_tracker_overlay``: it
installs a ``TrackerCore`` on the context, patches ``on_package`` to catch
the first ``Connected`` packet, and registers overlay features (Tracker tab,
periodic refresh) on ``ctx.client.features`` for ``ExtrasBuilder``.
"""

from __future__ import annotations

import asyncio
import functools
import logging
import os

logger = logging.getLogger("Client")


def attach_tracker_overlay(ctx) -> None:
    """Install ``tracker_core`` and patch ``on_package``; runs before
    ``server_task`` is scheduled so no packet can beat the patch."""
    if getattr(ctx, "tracker_core", None) is not None:
        # Standalone TrackerGameContext already owns its tracker_core.
        return

    from .TrackerCore import TrackerCore

    tracker_core = TrackerCore(logger, False, False)
    _noop = lambda *args, **kwargs: None
    tracker_core.set_set_page(_noop)
    tracker_core.set_log_to_tab(_noop)
    tracker_core.set_clear_page(_noop)
    tracker_core.set_get_ut_color(lambda _color: "DD00FF")
    ctx.tracker_core = tracker_core

    original_on_package = ctx.on_package

    @functools.wraps(original_on_package)
    def wrapped_on_package(cmd: str, args: dict) -> None:
        original_on_package(cmd, args)
        if cmd == "Connected":
            try:
                _handle_connected(ctx, args)
            except Exception:
                logger.exception("Tracker overlay failed to handle Connected packet")
        if cmd in ("Connected", "RoomUpdate"):
            _scout_checked_locations(ctx)
        if cmd in ("ReceivedItems", "RoomUpdate", "LocationInfo"):
            # New items/checks/scout replies change what is in logic; poke the
            # debounced refresh instead of waiting for the 60s tick.
            poke = getattr(ctx, "tracker_overlay_poke", None)
            if poke is not None:
                poke()

    ctx.on_package = wrapped_on_package

    client = getattr(ctx, "client", None)
    if client is not None:
        from .overlay_features import register_tracker_page_tab
        client.add(register_tracker_page_tab)
        client.add(start_overlay_ui_refresh)
    else:
        logger.warning(
            "Tracker overlay: ctx.client missing; "
            "Phase 2 features will not be scheduled"
        )


def _handle_connected(ctx, args: dict) -> None:
    """Populate ``tracker_core`` from the first ``Connected`` packet; mirrors the
    standalone on_package Connected branch minus map/entrance/scout plumbing."""
    from worlds import AutoWorld

    slot_info = args.get("slot_info") or {}
    slot_key = str(args.get("slot"))
    slot_entry = slot_info.get(slot_key)
    if not slot_entry:
        logger.warning(
            "Tracker overlay: Connected packet missing slot_info for slot %s",
            slot_key,
        )
        return

    slot_name, game = slot_entry[0], slot_entry[1]
    ctx.tracker_core.set_slot_params(game, ctx.slot, slot_name, ctx.team)

    connected_cls = AutoWorld.AutoWorldRegister.world_types.get(game)
    if connected_cls is None:
        logger.warning(
            "Tracker overlay: connected to world %r but no local apworld is installed; "
            "tracker pane will stay empty",
            game,
        )
        return

    raw_slot_data = args.get("slot_data") or {}

    # Worlds that can't rebuild from slot_data need a real generation against the
    # user's YAML; deferred to Connected so the picker only fires for tracked games.
    if (not getattr(connected_cls, "disable_ut", False)
            and not getattr(connected_cls, "ut_can_gen_without_yaml", False)
            and ctx.tracker_core.launch_multiworld is None):
        ctx.tracker_core.run_generator(None, None)

    ctx.tracker_core.initalize_tracker_core(connected_cls, raw_slot_data)
    if not ctx.tracker_core.multiworld:
        logger.error(
            "Tracker overlay: internal world generation failed for %r; "
            "tracker pane will stay empty",
            game,
        )


def _receives_own_items(ctx) -> bool:
    handling = getattr(ctx, "items_handling", None)
    return handling is None or bool(handling & 0b010)


def _scout_checked_locations(ctx) -> None:
    """Mirrors TrackerGameContext.scout_checked_locations: without the 0b010
    items_handling bit the server never echoes the player's own found items,
    so ask what sits at checked locations; replies land in ctx.locations_info."""
    if _receives_own_items(ctx):
        return
    locations_info = getattr(ctx, "locations_info", {}) or {}
    unknown = [location for location in (getattr(ctx, "checked_locations", set()) or set())
               if location not in locations_info]
    if unknown:
        asyncio.create_task(ctx.send_msgs([{
            "cmd": "LocationScouts", "locations": unknown, "create_as_hint": 0}]))


def _local_items(ctx) -> list:
    """Mirrors TrackerGameContext.update_tracker_items: the player's own items
    recovered from scouted checked locations."""
    if _receives_own_items(ctx):
        return []
    locations_info = getattr(ctx, "locations_info", {}) or {}
    checked = getattr(ctx, "checked_locations", set()) or set()
    slot = getattr(ctx, "slot", None)
    return [locations_info[location] for location in checked
            if location in locations_info and locations_info[location].player == slot]


def start_overlay_ui_refresh(ctx, app) -> None:
    """Schedule the periodic GUI refresh tick (invoked by ExtrasBuilder.build);
    no-ops on non-Kivy frontends -- the overlay is GUI-only."""
    if app is None:
        logger.debug("Tracker overlay: no app, skipping UI refresh")
        return

    if os.environ.get("MWGG_FRONTEND", "gui") == "tui":
        logger.debug("Tracker overlay: TUI frontend, skipping Kivy refresh")
        return

    try:
        from kivy.app import App as _KivyApp
        from kivy.clock import Clock
    except Exception:
        logger.debug("Tracker overlay: kivy not importable, skipping refresh")
        return

    if not isinstance(app, _KivyApp):
        logger.debug(
            "Tracker overlay: app %r is not Kivy-backed, skipping refresh",
            type(app).__name__,
        )
        return

    _enable_console_tracker_mode(app)

    def _tick(_dt: float) -> None:
        try:
            _refresh(ctx, app)
        except Exception:
            logger.exception("Tracker overlay: refresh tick failed")

    # Manual-refresh hook for the console refresh button.
    ctx.tracker_overlay_refresh = lambda: _refresh(ctx, app)
    # Debounced event hook: wrapped_on_package fires this on ReceivedItems/
    # RoomUpdate so logic updates land without waiting for the interval tick.
    ctx.tracker_overlay_poke = Clock.create_trigger(_tick, 0.5)

    Clock.schedule_once(_tick, 0)
    Clock.schedule_interval(_tick, 60)


def _enable_console_tracker_mode(app) -> None:
    """Enable the console appbar's Players/Logic toggle; the appbar's own
    client_type detection isn't reliable for the overlay path."""
    console_screen = getattr(app, "console_screen", None)
    appbar = getattr(console_screen, "important_appbar", None) if console_screen else None
    if appbar is None:
        logger.debug("Tracker overlay: console appbar not built yet, tracker_mode unset")
        return
    appbar.tracker_mode = True


def _refresh(ctx, app) -> None:
    """Push current ctx state into tracker_core, drive the tracker page
    labels, and ask the console to repaint."""
    tracker_core = getattr(ctx, "tracker_core", None)
    if tracker_core is None or tracker_core.multiworld is None or tracker_core.player_id is None:
        return

    tracker_core.set_missing_locations(getattr(ctx, "missing_locations", set()) or set())
    tracker_core.set_items_received(
        list(getattr(ctx, "items_received", []) or []) + _local_items(ctx))
    tracker_core.set_hints({})
    updateTracker_ret = tracker_core.updateTracker()

    _update_tracker_page_labels(ctx, tracker_core, updateTracker_ret)

    console_screen = getattr(app, "console_screen", None)
    update_fn = getattr(console_screen, "update_tracker_locations", None) if console_screen else None
    if update_fn is not None:
        update_fn()

    if app is not None:
        from worlds.tracker.gui import clear_stray_tooltips
        clear_stray_tooltips()


def _update_tracker_page_labels(ctx, tracker_core, updateTracker_ret) -> None:
    """Drive the Tracker page header labels (mirrors TrackerGameContext.updateTracker);
    hasattr guards cover contexts where the tab feature hasn't run."""
    if updateTracker_ret is None or updateTracker_ret.state is None:
        return

    current_world = tracker_core.get_current_world()
    if current_world is None:
        return

    page = getattr(ctx, "tracker_page", None)
    if page is not None:
        page.refresh_from_data()

    from worlds.tracker.TrackerClient import get_ut_color

    if hasattr(ctx, "tracker_total_locs_label"):
        checked = len(getattr(ctx, "checked_locations", []) or [])
        total = getattr(ctx, "total_locations", 0) or 0
        ctx.tracker_total_locs_label.text = f"Locations: {checked}/{total}"
    if hasattr(ctx, "tracker_logic_locs_label"):
        ctx.tracker_logic_locs_label.text = (
            f"In Logic: {len(updateTracker_ret.in_logic_locations)}"
        )
    if hasattr(ctx, "tracker_glitched_locs_label"):
        ctx.tracker_glitched_locs_label.text = (
            f"Glitched: [color={get_ut_color('glitched')}]"
            f"{len(updateTracker_ret.glitched_locations)}[/color]"
        )
    if hasattr(ctx, "tracker_hinted_locs_label"):
        ctx.tracker_hinted_locs_label.text = (
            f"Hinted: [color={get_ut_color('hinted_in_logic')}]"
            f"{len(updateTracker_ret.hinted_locations)}[/color]"
        )
    if hasattr(ctx, "tracker_go_mode_label"):
        multiworld = tracker_core.multiworld
        if multiworld.has_beaten_game(updateTracker_ret.state, current_world.player):
            ctx.tracker_go_mode_label.text = (
                f"Go mode: [color={get_ut_color('in_logic')}]Yes[/color]"
            )
        elif (updateTracker_ret.glitches_state
              and multiworld.has_beaten_game(updateTracker_ret.glitches_state, current_world.player)):
            ctx.tracker_go_mode_label.text = (
                f"Go mode: [color={get_ut_color('glitched')}]Glitched[/color]"
            )
        else:
            ctx.tracker_go_mode_label.text = (
                f"Go mode: [color={get_ut_color('out_of_logic')}]No[/color]"
            )
