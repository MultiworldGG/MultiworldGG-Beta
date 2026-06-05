"""Type stub for the generated ``mwgg_igdb`` package (Index repo orphan branch).

The real package is a ~50k-line generated module baking in the game index; only
its stable public surface is modeled here: the ``GameIndex`` singleton, the
``__variant__`` marker, and the raw data dicts. Game-data dict values are
heterogeneous (strings, lists, nested dicts) and read positionally by callers,
so they are typed ``Any`` rather than ``object`` to match unguarded ``.get(...)``
access sites in ModuleUpdate.
"""
from typing import Any

__variant__: str

class _GameIndexClass:
    @property
    def game_names(self) -> dict[str, str]: ...
    @property
    def search_index(self) -> dict[str, set[str]]: ...
    @property
    def games(self) -> dict[str, dict[str, Any]]: ...
    def search(self, query: str) -> dict[str, dict[str, Any]]: ...
    def get_game(self, game_module: str) -> dict[str, Any]: ...
    def add_game(self, game_module: str, game_data: dict[str, Any]) -> None: ...
    def get_module_for_game(self, game_name: str, worlds: bool = ...) -> str | None: ...
    def get_game_name_for_module(self, module_name: str) -> str | None: ...
    def get_all_games(self) -> dict[str, dict[str, Any]]: ...
    def get_all_game_names(self) -> list[str]: ...

# Module-level singleton instance, not the class (see `GameIndex = _GameIndexClass()`).
GameIndex: _GameIndexClass

GAMES_DATA: dict[str, dict[str, Any]]
GAMES_NAMES: dict[str, str]
SEARCH_INDEX: dict[str, set[str]]
