import asyncio
import logging
import os
import ssl
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Any, Callable, Optional, TYPE_CHECKING
from multiprocessing import Queue

if TYPE_CHECKING:
    import ModuleUpdate


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

    async def show_loading_status(self, message: str) -> None:
        """Put the loading overlay up with `message` under the animation and return once a
        frame has drawn it, so a blocking step announced this way is on screen before it
        starts; `hide_loading` ends the sequence. The tracker narrates its Connected work
        (yaml search, generation, map pack) through it. Feature-detected with getattr, so
        frontends may omit it.
        """
        ...

    def show_error_dialog(self, title: str, message: str) -> Any:
        """Display a modal error to the user. Returns an opaque handle that
        can later be passed to `dismiss_error_dialog` to close the dialog
        (e.g. when a connection retry succeeds).

        Each frontend chooses its own widget: Kivy uses an MDDialog-based
        MessageBox, Textual uses a ModalScreen. Callers must never assume a
        specific widget type; only the handle round-trip is portable.
        """
        ...

    def dismiss_error_dialog(self, handle: Any) -> None:
        """Dismiss an error dialog previously returned by `show_error_dialog`.
        No-op if the handle has already been dismissed."""
        ...

    def show_confirm_dialog(self, title: str, message: str, callback: Callable[[bool], None],
                            ok_text: str = "OK", cancel_text: str = "Cancel") -> Any:
        """Display a modal confirm/cancel prompt (e.g. the launcher's offer to install
        a room's pinned world version).

        `callback` is invoked exactly once on the UI thread with True (confirm) or
        False (cancel). Returns an opaque dialog handle, or None if the frontend
        could not show it. Feature-detected with getattr, so frontends may omit it.
        """
        ...

    def open_connect_dialog(self) -> None:
        """Open the connect dialog prefilled from `ctx` (hostname, port, username,
        password); confirming sets `ctx.username` and calls `ctx.connect`. Used after
        a module launch without a server address and after an InvalidGame/InvalidSlot
        refusal. Feature-detected with getattr: the TUI has none and those callers
        fall back to the console prompt.
        """
        ...

    def patch_client_type(self) -> str:
        """The user's choice of client for a routed patch file when the command line
        named none: "universal_tracker" attaches the tracker overlay to the game's
        client, "text" launches it plain. Feature-detected with getattr; without it
        (or on a falsy return) the patch launches plain.
        """
        ...

    def before_module_launch(self, module_name: str, **launch_kwargs) -> Any:
        """Notice that `module_name`'s client is about to launch with `launch_kwargs`
        (`patch_file`, `server_address`, `client_type`, ...). May return an awaitable, which
        `MultiWorld._route_module_when_ui_ready` awaits before launching so the
        frontend can put status on screen first. Feature-detected with getattr,
        so frontends may omit it.
        """
        ...

    def on_module_launch_failed(self, module_name: str) -> None:
        """The routed client launch for `module_name` failed after the frontend came
        up. Dismiss any loading state and give the user a way out. Feature-detected
        with getattr, so frontends may omit it.
        """
        ...

    def on_admin_command_result(self, args: dict) -> None:
        """Receive the full PrintJSON packet of a remote-admin reply (`type == "AdminCommandResult"`).

        Structured payloads ride along as top-level keys next to `data`: `players` for
        `/players`, `options` for `/options` and a successful `/option`. The text has
        already been routed through `print_json`. CommonClient feature-detects this
        method with getattr, so frontends may omit it.
        """
        ...

    # --- NOT-YET-IMPLEMENTED: per-world custom UI surface ---
    # Protocol stubs reserved for deprecating kvui.GameManager. `content` stays `Any`,
    # never a kivy Widget; nothing checks isinstance(app, FrontendProtocol) at runtime,
    # so frontends may omit these. Worlds still go through kvui.GameManager for now.

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
# Launcher frontends validate a slot/game pairing against a live MultiServer
# BEFORE the client takes over the window (there is no way back to the launcher),
# and install the room's pinned world version before the client imports the world.
# The socket is closed right after the verdict; the real client reconnects fresh.


_verify_logger = logging.getLogger("frontend_protocol.verify_slot")


@dataclass
class SlotVerifyResult:
    """Outcome of a pre-flight Connect handshake.

    `ok=True` means the server accepted the slot/game pairing. The socket was
    closed immediately; the caller still needs to launch the real client.

    `ok=False` with `errors` populated means the server returned
    `ConnectionRefused`; `errors` is the verbatim list from that packet.

    `ok=False` with `transport_error` populated means the handshake never
    completed (DNS failure, refused TCP, TLS error, timeout, ...). `errors` is
    empty in that case.

    `world_pin` is set on `ok=True` when the room pins this game's world at a
    version other than the installed one; `install_pinned_world` installs it.
    """
    ok: bool
    errors: list[str] = field(default_factory=list)
    transport_error: Optional[str] = None
    world_pin: Optional["ModuleUpdate.WorldPinCheck"] = None


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


def _mismatched_world_pin(game: str, room_info: dict) -> "Optional[ModuleUpdate.WorldPinCheck]":
    """The room's pin for `game` when it differs from the installed world; a pin that
    cannot be resolved never fails the verification."""
    import ModuleUpdate
    try:
        pin = ModuleUpdate.check_world_pin(game, (room_info.get("world_versions") or {}).get(game),
                                           room_info.get("mwgg_index_tag"))
    except Exception:
        _verify_logger.exception(f"Could not check the room's world version pin for {game}")
        return None
    return None if pin is None or pin.matches else pin


def install_pinned_world(pin: "ModuleUpdate.WorldPinCheck") -> bool:
    """Blocking install of the room's pinned world version from its index tag; True once
    installed. Must run before the client imports the world: a client holding the world's
    modules and native libraries cannot replace them."""
    import ModuleUpdate
    _verify_logger.info(f"Installing {pin.game} world version {pin.want} from index tag {pin.tag}...")
    try:
        return pin.slug not in ModuleUpdate.install_worlds_from_tag([pin.slug], pin.tag)
    except Exception:
        _verify_logger.exception(f"Install of worlds.{pin.slug} from index tag {pin.tag} failed")
        return False


def _ssl_context(address: str) -> Optional[ssl.SSLContext]:
    if not address.startswith("wss://"):
        return None
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


async def _attempt_verify(address: str, packet: dict) -> SlotVerifyResult:
    """Single websocket attempt against one URL. Caller handles fallback."""
    import websockets  # local import: launcher startup avoids ws import until needed
    from NetUtils import encode, decode

    socket = await websockets.connect(
        address, ping_timeout=None, ping_interval=None, ssl=_ssl_context(address),
    )
    try:
        await socket.send(encode([packet]))
        # The server unconditionally sends RoomInfo on open; keep it for the world
        # pin and drain frames until the verdict (Connected or ConnectionRefused).
        room_info: dict = {}
        async for raw in socket:
            for msg in decode(raw):
                cmd = msg.get("cmd") if isinstance(msg, dict) else None
                if cmd == "RoomInfo":
                    room_info = msg
                if cmd == "Connected":
                    return SlotVerifyResult(ok=True, world_pin=_mismatched_world_pin(packet["game"], room_info))
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
                # Probably a TLS mismatch; try the next address (ws → wss).
                last_error = "Server speaks a different protocol on that port (TLS mismatch?)."
                continue
            except websockets.InvalidURI as exc:
                return SlotVerifyResult(ok=False, transport_error=f"Invalid server address: {exc}")
            except ConnectionRefusedError:
                last_error = "Connection refused - is the server running on that address and port?"
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
    except Exception as exc:  # defensive: never let the launcher see a raw exception
        _verify_logger.exception("verify_slot crashed")
        return SlotVerifyResult(ok=False, transport_error=f"Unexpected error: {exc}")


async def read_room_info(server: str, *, timeout: float = 10.0) -> Optional[dict]:
    """Read the RoomInfo packet the server sends on open, without a Connect, so no
    slot name or password is needed. Returns None when no address answers with one
    within `timeout`; the socket is always closed before returning."""
    import websockets
    from NetUtils import decode

    async def _read(address: str) -> Optional[dict]:
        socket = await websockets.connect(
            address, ping_timeout=None, ping_interval=None, ssl=_ssl_context(address),
        )
        try:
            async for raw in socket:
                for msg in decode(raw):
                    if isinstance(msg, dict) and msg.get("cmd") == "RoomInfo":
                        return msg
            return None
        finally:
            try:
                await socket.close()
            except Exception:
                pass

    async def _run() -> Optional[dict]:
        for address in _build_addresses(server):
            try:
                return await _read(address)
            except (websockets.InvalidMessage, OSError):  # TLS mismatch, refused TCP, TLS error
                continue
        return None

    try:
        return await asyncio.wait_for(_run(), timeout=timeout)
    except Exception as exc:
        _verify_logger.info(f"Could not read RoomInfo from {server}: {exc!r}")
        return None
