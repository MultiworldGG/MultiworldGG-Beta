from __future__ import annotations
"""
Dictionary of constants for the MultiWorld GUI application

Contains the actions for the console and launcher.
"""

__all__ = (
    "CONSOLE_ACTIONS",
    "LAUNCHER_ACTIONS",
)

CONSOLE_ACTIONS = [
{
    "id":           "console",
    "buttonicon":   "chat-outline",
    "icon":         "chat-outline",
    "prefill":      "!countdown",
    "label":        "Console",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "hint",
    "buttonicon":   "map-search",
    "icon":         "map-search",
    "prefill":      "!hint",
    "label":        "Hint",
    "indicator":    "widgets",
    "type":         "assist",
},
{
    "id":           "admin",
    "buttonicon":   "account-lock-outline",
    "icon":         "wrench",
    "prefill":      "password",
    "label":        "Host Administration",
    "indicator":    "server-network",
    "type":         "assist",
}]


LAUNCHER_ACTIONS = [
{
    "id":           "connect",
    "buttonicon":   "lan-connect",
    "icon":         "lan-connect",
    "prefill":      "",
    "label":        "Connect",
    "indicator":    "blank",
    "type":         "assist",
},
]
