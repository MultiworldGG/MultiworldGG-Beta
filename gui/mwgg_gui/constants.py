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
    "id":           "generate",
    "buttonicon":   "creation-outline",
    "icon":         "creation-outline",
    "prefill":      "",
    "label":        "Generate",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "host",
    "buttonicon":   "hand-extended",
    "icon":         "hand-extended",
    "prefill":      "",
    "label":        "Host",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "patch",
    "buttonicon":   "auto-fix",
    "icon":         "auto-fix",
    "prefill":      "",
    "label":        "Patch",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "yaml",
    "buttonicon":   "code-brackets",
    "icon":         "code-brackets",
    "prefill":      "",
    "label":        "YAML",
    "indicator":    "blank",
    "type":         "assist",
},
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
