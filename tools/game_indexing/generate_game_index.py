import json
from pathlib import Path
from typing import Dict, Set, Any
import os
from re import match

def clean_value(value: Any) -> str:
    """
    Clean a value for indexing, converting null/None to empty string
    and ensuring we have a string value.
    
    Args:
        value: The value to clean
        
    Returns:
        Cleaned string value
    """
    if value is None:
        return ""
    return str(value).lower()

def clean_game_data(games_data: dict, rating_filter: str = "NR") -> dict:
    """
    Clean the game data, ensuring no null values and proper types.
    Preserves original world_name as it's used for identification.
    
    Args:
        games_data: Raw game data dictionary
        
    Returns:
        Cleaned game data dictionary
    """
    age_filter = []
    filter_nr = ["MW","3", "7", "12", "16", "18", "E", "T", "M", "NR"]
    filter_ao = ["MW","3", "7", "12", "16", "18", "E", "T", "M", "NR", "AO"]
    filter_16 = ["MW","3", "7", "12", "16", "E", "T"]
    filter_12 = ["MW","3", "7", "12", "E"]

    if rating_filter == "18_teen":
        age_filter = filter_16
    elif rating_filter == "12_kid":
        age_filter = filter_12
    elif rating_filter == "18plus_adult":
        age_filter = filter_ao
    age_filter = filter_nr

    cleaned_data = {}
    for world_name, game_data in games_data.items():
        if game_data.get("age_rating", "NR") in age_filter:
            cleaned_data[world_name] = game_data
    return cleaned_data

def build_search_index(games_data: dict) -> Dict[str, Set[str]]:
    """
    Build the search index from game data.
    
    Args:
        games_data: Dictionary of game data from game_details.json
        
    Returns:
        Dictionary mapping search terms to sets of game names
        Prepends the "popular" key to the index with a set of popular games
    """
    search_index = {
        "popular": {
        "alttp",
        "sc2",
        "oot",
        "kh2",
        "hk",
        "sm64ex"
    }}
    
    # Fields that should be indexed
    searchable_fields = {
        'igdb_name',
        'platforms',
        'genres',
        'themes',
        'keywords',
        'player_perspectives'
    }
    
    for world_name, game_data in games_data.items():
        # Index game name
        _add_to_index(search_index, game_data["game_name"], world_name)
        
        # Index only searchable fields
        for field, value in game_data.items():
            if field not in searchable_fields:
                continue
                
            if isinstance(value, list):
                # Convert to set to remove duplicates and improve iteration performance
                value_set = set(value) if value else set()
                for item in value_set:
                    if item and not match(r".*[():].*", item):  # Skip items with parentheses or colons
                        # Add both the full term and individual words
                        _add_to_index(search_index, clean_value(item), world_name)
                        for word in clean_value(item).split():
                            _add_to_index(search_index, word, world_name)
            elif isinstance(value, (str, int, float, bool)):
                if value:  # Only index non-empty values
                    value_str = clean_value(value)
                    _add_to_index(search_index, value_str, world_name)
                    # Add individual words for multi-word values
                    for word in value_str.split():
                        _add_to_index(search_index, word, world_name)
    
    return search_index

def _add_to_index(index: Dict[str, Set[str]], term: str, world_name: str) -> None:
    """
    Add a term to the search index.
    
    Args:
        index: The search index dictionary
        term: The term to index
        game_name: The name of the game this term is associated with
    """
    term = clean_value(term)
    if term:  # Only index non-empty terms
        if term not in index:
            index[term] = set()
        index[term].add(world_name)

def validate_generated_index(games_data: dict, search_index: Dict[str, Set[str]]) -> bool:
    """
    Validate the generated index to ensure all games are properly indexed.
    
    Args:
        games_data: The original game data
        search_index: The generated search index
        
    Returns:
        True if validation passes, False otherwise
    """
    # Check that all game names are in the index
    for world_name in games_data:
        game_name = games_data[world_name]["game_name"]
        if game_name not in search_index.get(game_name.lower(), set()):
            print(f"Warning: Game name '{game_name}' not properly indexed")
            return False
    
    # Check that all indexed terms point to valid games
    for term, games in search_index.items():
        for game in games:
            if game not in games_data:
                print(f"Warning: Invalid game reference '{game}' in term '{term}'")
                return False
    
    return True

def generate_index_file(rating_filter: str = "NR"):
    """Generate the game_index.py file with pre-built index."""
    try:
        # Load game data
        with open(os.path.join(os.path.dirname(__file__), 'output', 'game_details.json'), "r", encoding="utf-8") as file:
            games_data = json.load(file)
        
        # Clean the game data
        games_data = clean_game_data(games_data, rating_filter)
        
        # Build search index
        search_index = build_search_index(games_data)
        
        # Build the game names dictionary for fast lookups
        game_names = {name["game_name"]: module for module, name in games_data.items()}
        
        # Validate the generated index
        if not validate_generated_index(games_data, search_index):
            print("Warning: Index validation failed, but continuing with generation")
        
        # Convert sets to lists for JSON serialization
        search_index_json = {k: list(v) for k, v in search_index.items()}
        
        # Generate Python code
        games_data_str = json.dumps(games_data, indent=4)
        game_names_str = json.dumps(game_names, indent=4)
        search_index_str = json.dumps(search_index_json, indent=4).replace("[", "{").replace("]", "}")
        
        # Read template
        template_path = Path.cwd() / 'game_index_template.py'
        with open(template_path, "r") as f:
            template = f.read()
        
        # Fill template with explicit placeholder names
        code = template.replace("GAMES_DATA_PLACEHOLDER", games_data_str)
        code = code.replace("GAMES_NAMES_PLACEHOLDER", game_names_str)
        code = code.replace("SEARCH_INDEX_PLACEHOLDER", search_index_str)
        
        if rating_filter == "12_kid":
            folder = "twelve"
        elif rating_filter == "18_teen":
            folder = "sixteen"
        elif rating_filter == "18plus_adult":
            folder = "ao"
        else:
            folder = "nr"
            
        # Write generated file
        output_path = Path.cwd().parents[1] / 'game_index' / folder/ 'mwgg_igdb.py'
        with open(output_path, "w") as f:
            f.write(code)
        
        print(f"Generated game index with {len(games_data)} games and {len(search_index)} search terms")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find required file: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in game_details.json: {e}")
        return False
    except Exception as e:
        print(f"Error: Unexpected error during index generation: {e}")
        return False
    
    return True

def main():
    success = generate_index_file()
    if not success:
        exit(1) 
    success = generate_index_file(rating_filter="18plus_adult")
    if not success:
        exit(1) 
    success = generate_index_file(rating_filter="12_kid")
    if not success:
        exit(1)
    success = generate_index_file(rating_filter="18_teen")
    if not success:
        exit(1)

if __name__ == "__main__":
    main()