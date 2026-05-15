import asyncio
import logging
import os
import ssl
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Any, Optional
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


# --- Pre-flight slot/game verification ---------------------------------------
#
# Used by launcher frontends (Kivy GUI, Textual TUI) to validate a slot/game
# pairing against a live MultiServer BEFORE flipping the launcher into a per-game
# client. The slot/game mismatch is the bug this guards against: users who pick
# the wrong game from the launcher list have no way back to the launcher once
# the client takes over the window.
#
# The MultiServer Connect handler (off-limits to edit) rejects with
# {"cmd": "ConnectionRefused", "errors": [...]} containing one or more of:
# "InvalidPassword", "InvalidSlot", "InvalidGame", "IncompatibleVersion",
# "InvalidItemsHandling". We close the socket immediately after the verdict
# (success or refusal) — the real per-game client opens a fresh connection.


_verify_logger = logging.getLogger("frontend_protocol.verify_slot")


@dataclass
class SlotVerifyResult:
    """Outcome of a pre-flight Connect handshake.

    `ok=True` means the server accepted the slot/game pairing. The socket was
    closed immediately; the caller still needs to launch the real client.

    `ok=False` with `errors` populated means the server returned
    `ConnectionRefused` — `errors` is the verbatim list from that packet.

    `ok=False` with `transport_error` populated means the handshake never
    completed (DNS failure, refused TCP, TLS error, timeout, ...). `errors` is
    empty in that case.
    """
    ok: bool
    errors: list[str] = field(default_factory=list)
    transport_error: Optional[str] = None


def _build_addresses(server: str) -> list[str]:
    """Normalize a user-entered server address into one or two ws URLs to try.

    Mirrors `CommonClient.server_loop`: if the user typed a bare host[:port] or
    an `archipelago://` / `mwgg://` URL, treat it as `ws://` and add a `wss://`
    fallback. If the user typed an explicit scheme, honour it and don't fall
    back.
    """
    if "://" not in server:
        return [f"ws://{server}", f"wss://{server}"]
    normalized = server.replace("archipelago://", "ws://").replace("mwgg://", "ws://")
    if normalized.startswith("ws://"):
        return [normalized, "wss://" + normalized[len("ws://"):]]
    return [normalized]


def _build_connect_packet(slot_name: str, password: Optional[str], game: str) -> dict:
    """Construct a Connect packet identical in shape to `CommonContext.send_connect`.

    Tags are deliberately a single-element list `["AP"]` to match the live
    client's wire format (its set serializes to a JSON array of the same
    contents). The server's `ignore_game` path requires both an empty `game`
    AND a tag in `_non_game_messages` (HintGame/Tracker/TextOnly), so a
    non-empty `game` here guarantees the validation runs as intended.
    """
    from Utils import version_tuple, get_unique_identifier  # local import: keep module load light
    return {
        "cmd": "Connect",
        "password": password,
        "name": slot_name,
        "version": version_tuple,
        "tags": ["AP"],
        "items_handling": 0b000,
        "uuid": get_unique_identifier(),
        "game": game,
        "slot_data": False,
    }


async def _attempt_verify(address: str, packet: dict) -> SlotVerifyResult:
    """Single websocket attempt against one URL. Caller handles fallback."""
    import websockets  # local import: launcher startup avoids ws import until needed
    from NetUtils import encode, decode

    ssl_context: Optional[ssl.SSLContext] = None
    if address.startswith("wss://"):
        import certifi
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

    socket = await websockets.connect(
        address, ping_timeout=None, ping_interval=None, ssl=ssl_context,
    )
    try:
        await socket.send(encode([packet]))
        # The server unconditionally sends RoomInfo on open. Drain frames until
        # we see the verdict (Connected or ConnectionRefused) — anything else
        # (RoomInfo, PrintJSON) is ignored.
        async for raw in socket:
            for msg in decode(raw):
                cmd = msg.get("cmd") if isinstance(msg, dict) else None
                if cmd == "Connected":
                    return SlotVerifyResult(ok=True)
                if cmd == "ConnectionRefused":
                    errors = list(msg.get("errors") or [])
                    return SlotVerifyResult(ok=False, errors=errors)
                if cmd == "InvalidPacket":
                    return SlotVerifyResult(
                        ok=False, transport_error=f"Server rejected Connect: {msg.get('text', 'InvalidPacket')}",
                    )
        return SlotVerifyResult(ok=False, transport_error="Server closed the connection without a verdict.")
    finally:
        try:
            await socket.close()
        except Exception:
            pass


async def verify_slot(
    server: str,
    slot_name: str,
    password: Optional[str],
    game: str,
    *,
    timeout: float = 10.0,
) -> SlotVerifyResult:
    """Pre-flight a Connect handshake against `server` and return the verdict.

    `server` is host[:port] or a full URL (archipelago://, mwgg://, ws://, wss://).
    `slot_name`, `password`, `game` are passed straight through to the server's
    Connect validation. Returns as soon as the server sends Connected or
    ConnectionRefused; the socket is always closed before returning.

    Network/TLS failures surface as `ok=False, transport_error=<msg>` so the
    caller can show a single uniform error dialog instead of catching
    exceptions.
    """
    import websockets

    packet = _build_connect_packet(slot_name, password, game)
    addresses = _build_addresses(server)
    last_error: Optional[str] = None

    async def _run() -> SlotVerifyResult:
        nonlocal last_error
        for address in addresses:
            try:
                return await _attempt_verify(address, packet)
            except websockets.InvalidMessage:
                # Probably a TLS mismatch — try the next address (ws → wss).
                last_error = "Server speaks a different protocol on that port (TLS mismatch?)."
                continue
            except websockets.InvalidURI as exc:
                return SlotVerifyResult(ok=False, transport_error=f"Invalid server address: {exc}")
            except ConnectionRefusedError:
                last_error = "Connection refused — is the server running on that address and port?"
                continue
            except ssl.SSLError as exc:
                last_error = f"TLS error: {exc}"
                continue
            except OSError as exc:
                last_error = f"Network error: {exc}"
                continue
        return SlotVerifyResult(ok=False, transport_error=last_error or "Could not reach the server.")

    try:
        return await asyncio.wait_for(_run(), timeout=timeout)
    except asyncio.TimeoutError:
        return SlotVerifyResult(ok=False, transport_error=f"Timed out after {timeout:.0f}s waiting for the server.")
    except Exception as exc:  # defensive — never let the launcher see a raw exception
        _verify_logger.exception("verify_slot crashed")
        return SlotVerifyResult(ok=False, transport_error=f"Unexpected error: {exc}")
