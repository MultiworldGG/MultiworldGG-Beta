"""Loading-overlay narration for the tracker's Connected work (yaml search, generation, map pack).

Both tracker paths, the standalone ``TrackerGameContext`` and the game-client overlay in
``wrap.py``, keep the frontend's loading overlay up from ``before_package`` until the tracker is
ready; a frontend without ``show_loading_status`` (the TUI) only gets the log lines.
"""
from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger("Client")


def status_reporter(ctx) -> Callable[[str], Awaitable[None]] | None:
    """The frontend's ``show_loading_status``, for ``TrackerCore.prepare_generation``."""
    return getattr(getattr(ctx, "ui", None), "show_loading_status", None)


async def show_status(ctx, message: str) -> None:
    logger.info(message)
    report = status_reporter(ctx)
    if report is not None:
        await report(message)


def finish_loading(ctx) -> None:
    """Drop the overlay once the Connected work is done; the map controller drops it itself
    while its narrated pack load is still pending."""
    if getattr(ctx, "_map_activation_pending", False):
        return
    hide = getattr(getattr(ctx, "ui", None), "hide_loading", None)
    if hide is not None:
        hide()
