"""Universal Tracker overlay for game-specific clients.

When the launcher's "Universal Tracker" checkbox is set alongside a game
module, ``CommonClient.CommonContext.__init__`` calls ``attach_tracker_overlay``
on the just-built context. That:

1. Instantiates a ``TrackerCore`` and stashes it on ``ctx.tracker_core`` so
   the GUI's ``TrackerLocationRecycleView.populate_from_ctx`` (in
   ``mwgg-gui``) can render regions and missing locations.
2. Patches ``ctx.on_package`` so the first ``Connected`` packet drives
   ``tracker_core.initalize_tracker_core(connected_cls, slot_data)`` -- the
   only event we *must* intercept synchronously, since everything else is
   handled by the periodic refresh below.
3. Registers overlay features on ``ctx.client.features`` so
   ``ExtrasBuilder`` activates them after the per-game UI is wired up.
   Today: ``register_tracker_page_tab`` (adds the Tracker tab to the
   launcher's screen menu, wires tracker_core's display callbacks to it)
   and ``start_overlay_ui_refresh`` (schedules a 10-second Kivy interval
   which pushes current ``ctx.missing_locations`` / ``ctx.items_received``
   into ``tracker_core``, drives the Tracker page header labels, and asks
   the console to repaint). New overlay surfaces (e.g. the Map page)
   register here following the same pattern.

The standalone ``TrackerGameContext`` already owns its own ``tracker_core``
and the on_package interception lives in ``TrackerClient.py`` directly, so
``attach_tracker_overlay`` no-ops when called on a context that already has
one.
"""

from __future__ import annotations

import functools
import logging
import os

logger = logging.getLogger("Client")


def attach_tracker_overlay(ctx) -> None:
    """Phase 1: install ``tracker_core`` and patch ``on_package`` on ``ctx``.

    Called from ``CommonContext.__init__`` before the world's ``launch()``
    schedules ``server_task`` -- guarantees the patch is in place before any
    server packet can arrive.
    """
    if getattr(ctx, "tracker_core", None) is not None:
        # Standalone TrackerGameContext owns its own tracker_core and routes
        # on_package through TrackerClient. Nothing to do.
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
    """On the first ``Connected`` packet, populate ``tracker_core`` with the
    slot params and trigger multiworld generation. Mirrors the equivalent
    block in ``TrackerClient.TrackerGameContext.on_package`` (Connected
    branch), minus the map / deferred-entrance / scout plumbing that lives
    in the standalone tracker."""
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

    # Worlds that can't reconstruct themselves from slot_data need a real
    # generation against the user's YAML so launch_multiworld is populated
    # before initalize_tracker_core's slot-lookup branch runs. Standalone
    # TrackerClient.main does this at startup; the overlay defers it to
    # Connected so the picker only fires for games actually being tracked.
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


def start_overlay_ui_refresh(ctx, app) -> None:
    """Phase 2: schedule the periodic GUI refresh tick.

    Invoked by ``ExtrasBuilder.build()`` after the per-game UI is wired up.
    For non-Kivy frontends (TUI / headless), no-ops cleanly -- the overlay is
    GUI-only in v1. When the tracker migrates off legacy kvui this detection
    moves to a polymorphic refresh dispatcher.
    """
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

    # Expose a manual-refresh hook so the console refresh button (and any
    # future caller) can drive the full tracker pipeline -- not just the
    # UI repaint -- without importing wrap internals.
    ctx.tracker_overlay_refresh = lambda: _refresh(ctx, app)

    Clock.schedule_once(_tick, 0)
    Clock.schedule_interval(_tick, 60)


def _enable_console_tracker_mode(app) -> None:
    """Flip the console sliver appbar's tracker_mode so the Players/Logic
    toggle (and its initial recycleview seed) become available. The launcher's
    client_type-based detection in ConsoleSliverAppbar.__init__ isn't reliable
    for the overlay path -- explicit signal here is the single source of truth."""
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
    tracker_core.set_items_received(getattr(ctx, "items_received", []) or [])
    tracker_core.set_hints({})
    updateTracker_ret = tracker_core.updateTracker()

    _update_tracker_page_labels(ctx, tracker_core, updateTracker_ret)

    console_screen = getattr(app, "console_screen", None)
    update_fn = getattr(console_screen, "update_tracker_locations", None) if console_screen else None
    if update_fn is not None:
        update_fn()


def _update_tracker_page_labels(ctx, tracker_core, updateTracker_ret) -> None:
    """Drive the five Tracker page header labels (Locations / In Logic /
    Glitched / Hinted / Go Mode) from the latest tracker state.

    Mirrors TrackerGameContext.updateTracker (TrackerClient.py:534-548). The
    labels only exist after register_tracker_page_tab has attached them to
    ctx; hasattr guards make this safe when the tab feature hasn't run
    (e.g. headless / non-Kivy)."""
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
