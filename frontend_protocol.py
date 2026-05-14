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

    def show_error_dialog(self, title: str, message: str) -> Any:
        """Display a modal error to the user. Returns an opaque handle that
        can later be passed to `dismiss_error_dialog` to close the dialog
        (e.g. when a connection retry succeeds).

        Each frontend chooses its own widget: Kivy uses an MDDialog-based
        MessageBox, Textual uses a ModalScreen. Callers must never assume a
        specific widget type — only the handle round-trip is portable.
        """
        ...

    def dismiss_error_dialog(self, handle: Any) -> None:
        """Dismiss an error dialog previously returned by `show_error_dialog`.
        No-op if the handle has already been dismissed."""
        ...

    # --- NOT-YET-IMPLEMENTED: per-world custom UI surface ---
    #
    # Reserved for future work to fully deprecate `kvui`. The methods below are the
    # Kivy-only hooks that per-world client wrappers (kh2, albw, ...) currently reach for
    # when they subclass `kvui.GameManager` -- they pass a `kivy.uix.widget.Widget` as
    # `content`, which is exactly what locks those worlds to Kivy. A frontend-neutral
    # rewrite would have to:
    #
    #   1. Define a frontend-neutral "content" type (probably a small dataclass: title,
    #      logging-source name, optional structured data, and a renderer callback the
    #      frontend invokes with its own widget toolkit). Right now `content` is just
    #      `Any` so each frontend can decide what it accepts; do NOT take `Widget` here.
    #   2. Implement the methods on both `MultiMDApp` (Kivy) and `MultiTUIApp` (Textual).
    #      Kivy already has working bodies in `kvui.GameManager`; the TUI side needs new
    #      Screen/Tab widgets and a registry that survives takeover.
    #   3. Update per-world client wrappers to call `ctx.ui.add_client_tab(...)` instead
    #      of subclassing `kvui.GameManager`, then drop the `from kvui import GameManager`
    #      import. Once every world is migrated, `kvui.py` (and the stub it contains for
    #      the TUI path) can be deleted.
    #
    # Until that work happens, these are *protocol stubs only* -- `FrontendProtocol` is a
    # `runtime_checkable` Protocol, so adding them here is harmless: frontends that don't
    # implement them simply fail `isinstance(app, FrontendProtocol)`, which nothing in the
    # codebase currently relies on at runtime. Worlds that need custom UI must still go
    # through `kvui.GameManager` for now.

    def add_client_tab(self, title: str, content: Any, index: int = -1) -> Any:
        """Add a per-world tab/panel to the running frontend.

        `content` is frontend-defined (Kivy passes a `Widget`; the TUI would accept a
        Textual `Widget` or a renderable spec). Returns a handle the caller can later
        pass back to `remove_client_tab`.
        """
        ...

    def remove_client_tab(self, tab: Any) -> None:
        """Remove a tab previously returned by `add_client_tab`."""
        ...

    def create_custom_screen(self, title: str, content: Any, index: int = -1) -> Any:
        """Add a full-screen per-world view (one level above `add_client_tab`).

        Used by worlds that want their own top-level screen rather than a tab inside the
        main client view. Returns a handle suitable for `remove_custom_screen`.
        """
        ...

    def remove_custom_screen(self, handle: Any) -> None:
        """Remove a screen previously returned by `create_custom_screen`."""
        ...
