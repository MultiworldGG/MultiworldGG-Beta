"""Overlay features for game-specific clients with the Universal Tracker
attached.

Each feature is a ``feature(ctx, app)`` callable registered into
``ctx.client.features`` by ``attach_tracker_overlay`` (see wrap.py) and
invoked by ``ClientBuilder.ExtrasBuilder.build`` after the per-game UI is
wired up. Features are the Builder Pattern hook for adding overlay surfaces
without each new surface needing its own bespoke plumbing.

Today: the Tracker page tab. The Map page tab follows the same pattern and
will land here once the pack-loading port is ready.
"""

from __future__ import annotations

import logging
from collections import deque
from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType

if TYPE_CHECKING:
    from .TrackerCore import TrackerCore

logger = logging.getLogger("Client")

_UNREACHABLE_BRANCH = "(Unreachable)"
_MIN_BRANCHES = 4

# Categories matching TrackerLogLineGroup values, so the same string can
# be fed straight into tracker_core.get_ut_color() for the colour hex.
CATEGORY_DEFAULT = "default"
CATEGORY_HINTED = "hinted"
CATEGORY_EXCLUDED = "excluded"
CATEGORY_GLITCHED = "glitched"
CATEGORY_HINTED_GLITCHED = "hinted_glitched"
CATEGORY_EXCLUDED_GLITCHED = "excluded_glitched"

# Plain in-logic first, then glitched variants, then excluded last.
_CATEGORY_SORT_ORDER = {
    CATEGORY_DEFAULT: 0,
    CATEGORY_HINTED: 1,
    CATEGORY_GLITCHED: 2,
    CATEGORY_HINTED_GLITCHED: 3,
    CATEGORY_EXCLUDED: 4,
    CATEGORY_EXCLUDED_GLITCHED: 5,
}


def _select_branch_seeds(menu, min_count: int = _MIN_BRANCHES) -> list:
    """Pick the seed regions used as top-level branches.

    MultiworldGG's world-building contract requires Menu to have exactly
    one exit (the world's root region), so starting from Menu's direct
    exits always gives a single branch — useless as a tracker grouping.
    This descends one level at a time, replacing each branch with its
    own exit targets, until we have at least ``min_count`` distinct
    branches or no further descent is possible.
    """
    def fresh_exits(region, exclude: set) -> list:
        result = []
        seen_local = set()
        for ex in region.exits:
            target = ex.connected_region
            if target is None or target is menu or target is region:
                continue
            if target in exclude or target in seen_local:
                continue
            seen_local.add(target)
            result.append(target)
        return result

    branches = fresh_exits(menu, exclude=set())
    expanded: set = set()
    while len(branches) < min_count:
        next_branches: list = []
        next_seen: set = set()
        any_expanded = False
        for b in branches:
            if b in expanded:
                children = []
            else:
                children = fresh_exits(b, exclude=set(branches) | next_seen)
            if children:
                expanded.add(b)
                any_expanded = True
                for c in children:
                    if c not in next_seen:
                        next_seen.add(c)
                        next_branches.append(c)
            else:
                if b not in next_seen:
                    next_seen.add(b)
                    next_branches.append(b)
        if not any_expanded:
            break
        branches = next_branches
    return branches


def group_reachable_by_top_level_branch(
    tracker_core: "TrackerCore",
    *,
    include_glitched: bool = True,
    min_branches: int = _MIN_BRANCHES,
) -> list[tuple[str, list[tuple[str, str]]]]:
    """Group a player's reachable missing locations under top-level branches.

    Only locations the player can currently reach are included: those in
    ``tracker_core.locations_available`` and, when ``include_glitched`` is
    True, ``tracker_core.glitched_locations``. Out-of-logic missing
    locations are dropped.

    Each location is classified into one of the ``CATEGORY_*`` strings,
    which double as ``tracker_core.get_ut_color`` keys so the view can
    look up the matching hex without knowing the category semantics.

    Seed branches come from ``_select_branch_seeds`` (descending past
    Menu's single exit). Regions that don't connect back to Menu fall
    into ``(Unreachable)``.

    Returns ``[(branch_name, [(location_name, category), ...]), ...]``
    sorted alphabetically by branch (``(Unreachable)`` last); each
    branch's locations sort by category (in-logic before glitched,
    plain before hinted before excluded) then alphabetically.
    """
    multiworld = getattr(tracker_core, "multiworld", None)
    player_id = getattr(tracker_core, "player_id", None)
    if multiworld is None or player_id is None:
        return []

    in_logic = set(getattr(tracker_core, "locations_available", []) or [])
    glitched = set(getattr(tracker_core, "glitched_locations", []) or [])
    hints_map = getattr(tracker_core, "hints", {}) or {}
    hinted = set(hints_map.keys()) if isinstance(hints_map, dict) else set(hints_map)
    # Mirror TrackerCore.updateTracker (TrackerCore.py:478, 535): the
    # ``hide_excluded_locations`` tracker setting drops EXCLUDED locations
    # from the page entirely. Honour the same toggle so this view stays
    # in sync with the rest of the tracker.
    hide_excluded = bool(getattr(tracker_core, "hide_excluded", False))

    if not include_glitched:
        glitched = set()

    try:
        menu = multiworld.get_region("Menu", player_id)
    except KeyError:
        return []

    seeds = _select_branch_seeds(menu, min_count=min_branches)

    region_to_branch: dict[object, str] = {}
    queue: deque = deque()
    for seed in seeds:
        if seed in region_to_branch:
            continue
        region_to_branch[seed] = seed.name
        queue.append(seed)

    while queue:
        region = queue.popleft()
        branch = region_to_branch[region]
        for ex in region.exits:
            target = ex.connected_region
            if target is None or target is menu or target in region_to_branch:
                continue
            region_to_branch[target] = branch
            queue.append(target)

    grouped: dict[str, list[tuple[str, str]]] = {}
    for region in multiworld.get_regions(player_id):
        if region is menu:
            continue
        branch_name = region_to_branch.get(region, _UNREACHABLE_BRANCH)
        for loc in region.locations or []:
            addr = loc.address
            if addr is None:
                continue
            is_excluded = loc.progress_type == LocationProgressType.EXCLUDED
            if is_excluded and hide_excluded:
                continue
            is_hinted = addr in hinted
            if addr in in_logic:
                category = (
                    CATEGORY_EXCLUDED if is_excluded
                    else CATEGORY_HINTED if is_hinted
                    else CATEGORY_DEFAULT
                )
            elif addr in glitched:
                category = (
                    CATEGORY_EXCLUDED_GLITCHED if is_excluded
                    else CATEGORY_HINTED_GLITCHED if is_hinted
                    else CATEGORY_GLITCHED
                )
            else:
                continue
            grouped.setdefault(branch_name, []).append((loc.name, category))

    for items in grouped.values():
        items.sort(key=lambda t: (_CATEGORY_SORT_ORDER.get(t[1], 99), t[0]))

    result = [(name, items) for name, items in grouped.items() if items]
    result.sort(key=lambda t: (t[0] == _UNREACHABLE_BRANCH, t[0]))
    return result


def register_tracker_page_tab(ctx, app) -> None:
    """Build the Tracker page widget, replace the tracker_core display
    no-op callbacks with real ones, and add the page as a 'tracker' tab on
    the live launcher app.

    Idempotent: re-entry is a no-op once the tab exists.
    """
    if getattr(ctx, "tracker_page", None) is not None:
        return

    from worlds.tracker.gui import build_tracker_view, install_app_surface

    # build_tracker_view reads ctx.gen_error unconditionally; the standalone
    # TrackerGameContext defaults it to None at class scope. ALBWContext (and
    # any game-specific ctx) has no such default, so seed it here.
    if not hasattr(ctx, "gen_error"):
        ctx.gen_error = None

    # install_app_surface injects the kivy properties referenced from
    # Tracker.kv (app.source, app.loc_size, ...) onto the live launcher app
    # and contributes the Tracker section to the launcher's SettingsScreen.
    # Idempotent.
    install_app_surface(ctx, app)

    try:
        tracker = build_tracker_view(ctx)
    except Exception:
        logger.exception("Tracker overlay: build_tracker_view failed; tab not added")
        return

    tracker_core = getattr(ctx, "tracker_core", None)
    tracker_page = getattr(ctx, "tracker_page", None)
    if tracker_core is not None and tracker_page is not None:
        # Mirror the standalone TGC's log_to_tab / set_page / clear_page bodies
        # (TrackerClient.py:876-886) so tracker_core's lines reach the page.
        def _set_page(line: str) -> None:
            tracker_page.data = [{"text": line}]

        def _log_to_tab(line: str, sort: bool = False) -> None:
            tracker_page.addLine(line, sort)

        def _clear_page() -> None:
            tracker_page.resetData()

        tracker_core.set_set_page(_set_page)
        tracker_core.set_log_to_tab(_log_to_tab)
        tracker_core.set_clear_page(_clear_page)

    try:
        handle = app.add_client_tab("tracker", tracker)
    except Exception:
        logger.exception("Tracker overlay: add_client_tab('tracker', ...) failed")
        return

    if handle is None:
        logger.info(
            "Tracker overlay: 'tracker' screen already registered, skipping tab add"
        )
    else:
        logger.info("Tracker overlay: 'tracker' tab registered")
