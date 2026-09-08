"""Re-export shim for the upstream SNES client surface.

Upstream SNES worlds do `from SNIClient import snes_read, ...` inside their
validate_rom/game_watcher bodies; the implementation lives in worlds._sni
(bridge) and worlds._sni.context (SNIContext). Client processes only: importing
this loads the worlds package.
"""

from worlds._sni import (
    SNESRequest, SNESState, get_snes_devices, launch_sni, snes_autoreconnect, snes_buffered_write,
    snes_connect, snes_disconnect, snes_flush_writes, snes_logger, snes_read, snes_recv_loop,
    snes_write, task_alive, verify_snes_app,
)
from worlds._sni.context import (
    DeathState, SNIClientCommandProcessor, SNIContext, deathlink_kill_player, game_watcher, launch,
    main, run_game,
)

__all__ = [
    "SNESRequest", "SNESState", "get_snes_devices", "launch_sni", "snes_autoreconnect",
    "snes_buffered_write", "snes_connect", "snes_disconnect", "snes_flush_writes", "snes_logger",
    "snes_read", "snes_recv_loop", "snes_write", "task_alive", "verify_snes_app",
    "DeathState", "SNIClientCommandProcessor", "SNIContext", "deathlink_kill_player", "game_watcher",
    "launch", "main", "run_game",
]
