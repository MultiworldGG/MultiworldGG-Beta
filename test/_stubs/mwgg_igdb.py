"""Test-only stub for `mwgg_igdb`.

The real package is a ~50k-line generated module installed from the Index
repo's orphan branch. Tests don't need its game-name->slug data — worlds that
are physically present in the repo are loaded by `worlds/__init__.py` and
register themselves on `AutoWorldRegister` at import time. This stub provides
the same `GameIndex` singleton with the same API surface, backed by empty
dicts, so callers (`test/__init__.py`, `Utils.set_game_names`,
`Generate.roll_settings`, `BaseUtils.get_archipelago_constants`, etc.) can
import and call methods without crashing.

`src/conftest.py` prepends this directory to `sys.path` at pytest startup so
this module is found before any real `mwgg_igdb` installed in the venv.
"""


class _GameIndexClass:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._initialized:
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._game_names: dict[str, str] = {}
        self._search_index: dict[str, set] = {}
        self._games: dict[str, dict] = {}
        self._module_to_name: dict[str, str] = {}

    @property
    def game_names(self) -> dict:
        return self._game_names

    @game_names.setter
    def game_names(self, item) -> None:
        key, value = item
        self._game_names[key] = value

    @property
    def search_index(self) -> dict:
        return self._search_index

    @search_index.setter
    def search_index(self, item) -> None:
        key, value = item
        if key in self._search_index:
            self._search_index[key].add(value)
        else:
            self._search_index[key] = {value}

    @property
    def games(self) -> dict:
        return self._games

    @games.setter
    def games(self, item) -> None:
        key, value = item
        self._games[key] = value

    def search(self, query: str) -> dict:
        return {}

    def get_game(self, game_module: str) -> dict:
        return self._games.get(game_module, {})

    def add_game(self, game_module: str, game_data: dict) -> None:
        self._games[game_module] = game_data
        name = game_data.get("game_name")
        if name:
            self._game_names[name] = game_module
            self._module_to_name[game_module] = name
        for term in game_module.lower().split():
            if term in self._search_index:
                self._search_index[term].add(game_module)
            else:
                self._search_index[term] = {game_module}

    def get_module_for_game(self, game_name: str, worlds: bool = False):
        module = self._game_names.get(game_name)
        if module and worlds:
            return f"worlds.{module}"
        return module

    def get_game_name_for_module(self, module_name: str):
        if module_name.startswith("worlds."):
            module_name = module_name[len("worlds."):]
        return self._module_to_name.get(module_name)

    def get_all_games(self) -> dict:
        return self._games

    def get_all_game_names(self) -> list:
        return list(self._game_names.keys())


GameIndex = _GameIndexClass()

GAMES_DATA: dict[str, dict] = {}
GAMES_NAMES: dict[str, str] = {}
SEARCH_INDEX: dict[str, set] = {}
