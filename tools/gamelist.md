# Game Search Implementation Design

## Overview
The current implementation loads all games immediately into the UI. We need to modify this to only show games that match the search criteria entered in the search field. The search should be comprehensive, matching against multiple fields in the game data.

## Architecture

### 1. Game Index Module (`data/game_index.py`)
This module will contain the pre-generated search index for games. The index will be generated during the build process and included in the final executable.

```python
# This file will be generated during build
from typing import Dict, Set

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
        
        # Get initial set of matching games
        for term in query_terms:
            for indexed_term, games in self.search_index.items():
                if term in indexed_term:
                    if not matching_games:
                        matching_games = games.copy()
                    else:
                        matching_games &= games
        
        # Return only matching games
        return {name: self.games[name] for name in matching_games}

# These constants will be generated during build
GAMES_DATA = {
    # Generated from game_details.json
}

SEARCH_INDEX = {
    # Generated inverted index
}
```

### 2. Index Generation Script (`tools/generate_game_index.py`)
This script will be run during the build process to generate the search index.

```python
import json
from pathlib import Path
from typing import Dict, Set

def build_search_index(games_data: dict) -> Dict[str, Set[str]]:
    """
    Build the search index from game data.
    
    Args:
        games_data: Dictionary of game data from game_details.json
        
    Returns:
        Dictionary mapping search terms to sets of game names
    """
    search_index = {}
    
    for game_name, game_data in games_data.items():
        # Index game name
        _add_to_index(search_index, game_name, game_data)
        
        # Index all fields
        for field, value in game_data:
            _add_to_index(search_index, value.lower(), game_name)
    
    return search_index

def _add_to_index(index: Dict[str, Set[str]], term: str, game_name: str) -> None:
    """Add a term to the search index."""
    term = term.lower()
    if term not in index:
        index[term] = set()
    index[term].add(game_name)

def generate_index_file():
    """Generate the game_index.py file with pre-built index."""
    # Load game data
    with open("game_details.json", "r", encoding="utf-8") as file:
        games_data = json.load(file)
    
    # Build search index
    search_index = build_search_index(games_data)
    
    # Generate Python code
    games_data_str = json.dumps(games_data, indent=4)
    search_index_str = json.dumps({k: list(v) for k, v in search_index.items()}, indent=4)
    
    # Read template
    template_path = Path("tools/game_index_template.py")
    with open(template_path, "r") as f:
        template = f.read()
    
    # Fill template
    code = template.format(
        games_data=games_data_str,
        search_index=search_index_str
    )
    
    # Write generated file
    output_path = Path("data/game_index.py")
    with open(output_path, "w") as f:
        f.write(code)

if __name__ == "__main__":
    generate_index_file()
```

### 3. Build Process Integration
The index generation will be integrated into the build process:

```python
# In your build script
def build_client():
    # Generate game index
    subprocess.run(["python", "tools/generate_game_index.py"])
    
    # Build executable
    # ...
```

### 4. Launcher Screen Integration (`gui/launcher.py`)
The launcher screen will use the pre-generated GameIndex.

```python
from mwgg_gui.game_index import GameIndex

class LauncherScreen(MDScreen, ThemableBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games_mdlist = MDList(width=260)
        
        # Get the pre-generated game index
        self.game_index = GameIndex()
        
        # Bind search field to search function
        self.important_appbar.ids.search_bar.ids.game_tag_filter.bind(
            text=self.on_search_text
        )
    
    def on_search_text(self, instance, value):
        """Handle search text changes"""
        matching_games = self.game_index.search(value)
        self.update_game_list(matching_games)
    
    def update_game_list(self, games):
        """Update the UI with matching games"""
        self.games_mdlist.clear_widgets()
        for game_tag, tag_type in games.items():
            game = GameListPanel(game_tag=game_tag, tag_type=tag_type)
            self.games_mdlist.add_widget(game)
```

## Performance Considerations

1. **Build-time Index Generation**
   - Index is generated once during build
   - No runtime index building required
   - Smaller memory footprint as index is optimized
   - Faster client startup

2. **Search Optimization**
   - Use case-insensitive search
   - Split search terms to match partial words
   - Use set intersection for combining multiple search terms
   - Consider implementing fuzzy search for better matching
   - Add debouncing to prevent too frequent searches

3. **UI Updates**
   - Use async loading for game panels
   - Implement virtual scrolling if the list gets too long
   NO - Add loading indicators during search #I have a loading module already.  Indicate with comments where to start/stop loading animations.
   - Show empty state when no search is entered

## Implementation Steps

1. Create the index generation script
2. Create the game index template
3. Integrate index generation into build process
4. Update `LauncherScreen` to use the pre-generated index
5. Add loading and empty states to the UI
6. Implement search debouncing
7. Add error handling

## Testing Plan

1. Unit Tests (`tests/test_game_index.py`):
   ```python
   def test_search_functionality():
       """Test search returns correct results"""
       game_index = GameIndex()  # Uses pre-generated index
       results = game_index.search("action")
       assert len(results) > 0
       # Add more specific assertions based on known data
   ```

2. Build Process Tests:
   - Test index generation
   - Test generated file format
   - Test index completeness
   - Test build process integration

3. Integration Tests:
   - Test UI updates with search results
   - Test search performance
   - Test error handling

4. User Testing:
   - Test search usability
   - Test search performance
   - Test UI responsiveness

## Future Improvements

1. **Advanced Search Features**
   - Add filters for specific fields (genre, theme, etc.)
   - Implement fuzzy search for better matching
   - Add search history
   - Add search suggestions

2. **Performance Optimizations**
   - Implement caching for frequent searches
   - Add pagination for large result sets
   - Optimize index structure for faster searches

3. **UI Enhancements**
   - Add search filters UI
   - Show search result counts
   - Add sorting options
   - Implement keyboard shortcuts

4. **Build Process Improvements**
   - Add index validation during build
   - Add index optimization options
   - Add index compression
   - Add incremental index updates 