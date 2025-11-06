from typing import Dict, Set, Any

class GameIndex:
    """
    Pre-generated search index for games. This index is built during the build process
    and included in the final executable.
    """
    def __init__(self):
        # The search index is pre-populated during build
        self.games: Dict[str, dict] = GAMES_DATA  # Generated during build
        self.search_index: Dict[str, Set[str]] = SEARCH_INDEX  # Generated during build
    
    def search(self, query: str) -> dict:
        """
        Search for games matching the query.
        
        Args:
            query: The search query string
            
        Returns:
            Dictionary of matching games
        """
        if not query:
            return {}
            
        query_terms = query.lower().split()
        matching_games = set()
        
        # First try exact matches from the search index
        for term in query_terms:
            if term in self.search_index:
                if not matching_games:
                    matching_games = set(self.search_index[term])
                else:
                    matching_games &= set(self.search_index[term])
        
        # If no exact matches found, try partial matches
        if not matching_games:
            for game_name, game_data in self.games.items():
                # First check if any query term is in the game title
                if any(term in game_name.lower() for term in query_terms):
                    matching_games.add(game_name)
                    continue
                
                # Then check other searchable fields
                searchable_fields = {
                    'genres': game_data.get('genres', []),
                    'themes': game_data.get('themes', []),
                    'keywords': game_data.get('keywords', []),
                    'player_perspectives': game_data.get('player_perspectives', []),
                    'rating': [game_data.get('rating', '')],
                    'release_date': [str(game_data.get('release_date', ''))]
                }
                
                # Check if any query term is contained in any searchable field
                for field_values in searchable_fields.values():
                    if isinstance(field_values, list):
                        for value in field_values:
                            if isinstance(value, str) and any(term in value.lower() for term in query_terms):
                                matching_games.add(game_name)
                                break
                    elif isinstance(field_values, str) and any(term in field_values.lower() for term in query_terms):
                        matching_games.add(game_name)
                        break
                    
                    if game_name in matching_games:
                        break
        
        # Return only matching games
        return {name: self.games[name] for name in matching_games}
    
    def get_game(self, game_module: str) -> dict:
        """
        Get full game data for a specific game.
        
        Args:
            game_module: The module name of the game to retrieve
            
        Returns:
            Dictionary containing all game data
        """
        return self.games.get(game_module, {})
    
    def get_all_games(self) -> dict:
        """
        Get all game data.
        
        Returns:
            Dictionary containing all games and their data
        """
        return self.games.copy()

    @staticmethod
    def get_all_game_names() -> list[str]:
        """
        Get all game names.
        
        Returns:
            List of all game names
        """
        return [game_data['game_name'] for game_data in GAMES_DATA.values()]

    @staticmethod
    def get_module_for_game(game_name: str, worlds: bool = False) -> str:
        """Get the module name for a given game name
        
        Args:
            game_name: The name of the game to get the module name for
            worlds: Whether to return the full module name or the folder name
            
        Returns:
            The module name for the given game name
        """
        for module, game_data in GAMES_DATA.items():
            if game_data['game_name'] == game_name:
                return "worlds.{}".format(module) if worlds else module
        return None

    @staticmethod
    def get_game_name_for_module(module_name: str) -> str:
        """Get the game name for a given module name"""
        for module, game_data in GAMES_DATA.items():
            if module == module_name:
                return game_data['game_name']
        return None

    @staticmethod
    def add_game(game_module: str, game_data: dict):
        """Add a game to the game index"""
        GAMES_DATA[game_module] = game_data
        SEARCH_INDEX[game_module] = set()
        for term in game_module.lower().split():
            SEARCH_INDEX[term].add(game_module)

# These constants will be generated during build
GAMES_DATA = GAMES_DATA_PLACEHOLDER  # type: ignore  # noqa: F821

SEARCH_INDEX = SEARCH_INDEX_PLACEHOLDER  # type: ignore  # noqa: F821