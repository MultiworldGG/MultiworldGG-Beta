import os
from typing import Protocol, runtime_checkable, Any
from multiprocessing import Queue


def resolve_frontend_class() -> "type[FrontendProtocol]":
    """Lazy-import the frontend App class selected by the `MWGG_FRONTEND` env var.

    `MultiWorld.py` sets `MWGG_FRONTEND` from the `--frontend={gui,tui}` arg before any
    frontend is constructed. Both `CommonContext.make_gui()` and the pre-context
    `InitialClient` builder route through this function so dispatch lives in one place.
    """
    frontend = os.environ.get("MWGG_FRONTEND", "gui")
    if frontend == "tui":
        from mwgg_tui.app import MultiTUIApp
        return MultiTUIApp
    if frontend == "gui":
        from mwgg_gui.app import MultiMDApp
        return MultiMDApp
    raise ValueError(f"Unknown MWGG_FRONTEND={frontend!r}; expected 'gui' or 'tui'.")


@runtime_checkable
class FrontendProtocol(Protocol):
    """Contract that every MultiworldGG frontend (Kivy GUI, Textual TUI, ...) must satisfy.

    Tier 1 only: covers what `CommonClient.MultiworldGGContext` itself drives.
    Tracker/manual-client surfaces (`current_map`, `game_bar_text`, ...) are
    intentionally NOT part of this protocol and remain Kivy-only.
    """

    ctx: Any
    text_buffer: Queue
    commandprocessor: Any
    base_title: str
    ui_player_data: dict
    countdown_timer: float

    def __init__(self, ctx: Any) -> None: ...
    def async_run(self) -> Any: ...
    def stop(self) -> None: ...
    def print_json(self, data: list) -> None: ...
    def on_connect(self) -> None: ...
    def update_hints(self) -> None: ...
    def update_mwgg_hints(self) -> None: ...
    def update_timer(self, value: Any) -> None: ...
    def set_new_energy_link_value(self) -> None: ...
    def focus_textinput(self) -> None: ...
    def hide_loading(self) -> None: ...
    def is_on_console_screen(self) -> bool: ...
