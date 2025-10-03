from flask import Flask, request, jsonify
import os
import requests  # Changed from request to requests
import json
import importlib.util
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import sys
import re

# Get the user's home directory and convert to forward slashes
home_dir = Path.home()
client_id_path = Path(home_dir) / ".igdb" / "clientid"
key_path = Path(home_dir) / ".igdb" / "key"

with open(client_id_path, 'r') as file:
    igdb_client_id = file.readline().strip()
with open(key_path, 'r') as file:
    igdb_key = file.readline().strip()

igdb_token = ""

if os.path.exists(Path(home_dir) / "access_token"):
    modified_time = datetime.fromtimestamp(os.path.getmtime(Path(home_dir) / "access_token"))
    if datetime.now() - modified_time > timedelta(days=60):
        print("Access token file is older than 60 days, generating new token")
        url = f"https://id.twitch.tv/oauth2/token?client_id={igdb_client_id}&client_secret={igdb_key}&grant_type=client_credentials"
        response = requests.post(url)
        igdb_token = response.json()['access_token']
        with open(Path(home_dir) / "access_token", "w") as file:
            file.write(igdb_token)
    else:
        with open(Path(home_dir) / "access_token", "r") as file:
            igdb_token = file.readline().strip()
else:
    print("Access token file not found, generating new token")
    url = f"https://id.twitch.tv/oauth2/token?client_id={igdb_client_id}&client_secret={igdb_key}&grant_type=client_credentials"
    response = requests.post(url)
    igdb_token = response.json()['access_token']
    with open(Path(home_dir) / "access_token", "w") as file:
        file.write(igdb_token)

def get_igdb_game_keywords(game_id: int) -> list:
    """
    Fetches game keywords from IGDB API using the provided game name.
    """
    url = "https://api.igdb.com/v4/keywords"
    headers = {
        'Client-ID': igdb_client_id,
        'Authorization': f'Bearer {igdb_token}',
        'Content-Type': 'application/json'
    }
    data = f'fields name; search "{game_id}"; limit 10;'
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return [keyword['name'] for keyword in response.json()]
    else:
        return []

def get_igdb_game_cover(game_id: int) -> str:
    """
    Fetches game cover image URL from IGDB API using the provided game name.
    """
    url = "https://api.igdb.com/v4/covers"
    headers = {
        'Client-ID': igdb_client_id,
        'Authorization': f'Bearer {igdb_token}',
        'Content-Type': 'application/json'
    }
    data = f'fields url; search "{game_id}"; limit 1;'
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()[0]['url']
    else:
        return None

def get_game_and_igdb_id_from_world(init_path: str) -> Optional[Tuple[str, int]]:
    """
    Gets the game name and IGDB ID from a world's __init__.py file.
    Returns a tuple of (game_name, igdb_id) or None if not found.
    """
    if not os.path.exists(init_path):
        return None
    
    try:
        # Read the file content
        with open(init_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        # Look for game name with type annotation - handle apostrophes properly
        game_name = content["game"]
        if not game_name:
            return None
        
        # Look for igdb_id with type annotation
        igdb_id = content["igdb_id"]
        if not igdb_id:
            return None
            
        return game_name, igdb_id
                
    except Exception as e:
        print(f"Error loading {init_path}: {e}")
        return None

def get_game_ids_from_worlds() -> dict:
    """
    Gets IGDB game IDs for all games in the worlds directory.
    Returns a dictionary mapping game names to their IGDB IDs.
    """
    # Get all world directories from base_world_inits.txt
    world_dirs = Path.cwd().parents[1] / "worlds"
    worlds = [world_dirs / world for world in world_dirs.iterdir() if world.is_dir()]
    
    game_ids = {}

    for world in worlds:
        init_file = world / "archipelago.json"
            
        # Get game name and IGDB ID from the constants file
        result = get_game_and_igdb_id_from_world(init_file)
        if not result:
            print(f"Could not find game_name and and igdb_id constants in {init_file}")
            continue
            
        game_name, igdb_id = result
        game_ids[world.name] = {"igdb_id": igdb_id, "game_name": game_name}
    return game_ids

def get_igdb_game_details(game_id: int) -> dict:
    """
    Fetches detailed game information from IGDB API including name, rating, themes, and keywords.
    """
    url = "https://api.igdb.com/v4/games"
    headers = {
        'Client-ID': igdb_client_id,
        'Authorization': f'Bearer {igdb_token}',
        'Content-Type': 'application/json'
    }
    data = f'''
    fields name, cover.url, age_ratings.organization.name, age_ratings.rating_category.rating, age_ratings.rating_content_descriptions.description, first_release_date, player_perspectives.name,genres.name, themes.name, keywords.name, platforms.name, storyline;
    where id = {game_id};
    '''

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200 or not response.json():
        return {}
        
    game_data = response.json()[0]

    # Extract content descriptions from age ratings
    content_descriptions = []
    age_rating = "NR"
    for rating in game_data.get('age_ratings', []):
        if 'organization' in rating:
            if rating['organization']['name'] == 'PEGI':
                if 'rating_category' in rating:
                    age_rating = rating['rating_category']['rating']
            if rating['organization']['name'] == 'ESRB':
                if 'rating_content_descriptions' in rating:
                    for desc in rating['rating_content_descriptions']:
                        if 'description' in desc:
                            content_descriptions.append(desc['description'])
                if age_rating == "NR":
                    age_rating = rating['rating_category']['rating']

    return {
        'igdb_name': game_data.get('name', ''),
        'cover_url': game_data.get('cover', {}).get('url', ''),
        'age_rating': age_rating,
        'rating': content_descriptions,
        'themes': [theme['name'] for theme in game_data.get('themes', [])],
        'player_perspectives': [perspective['name'] for perspective in game_data.get('player_perspectives', [])],
        'genres': [genre['name'] for genre in game_data.get('genres', [])],
        'platforms': [platform['name'] for platform in game_data.get('platforms', [])],
        'storyline': game_data.get('storyline', ''),
        'release_date': game_data.get('first_release_date', ''),
        'keywords': [keyword['name'] for keyword in game_data.get('keywords', [])]
    }

def generate_game_details_json() -> dict:
    """
    Generates a JSON structure containing game details from both the world files and IGDB.
    For worlds without IGDB IDs, creates an empty entry with just the world name.
    """
    # Get all directory names from worlds folder
    game_ids = get_game_ids_from_worlds()

    result = {}
    
    for world, data in game_ids.items():
        if data["igdb_id"]:
            # Get IGDB details for worlds with IGDB IDs
            igdb_details = get_igdb_game_details(data["igdb_id"])
            
            # Create the game entry with IGDB data
            result[world] = {
                'igdb_id': str(data["igdb_id"]),
                'cover_url': igdb_details.get('cover_url', ''),
                'game_name': data["game_name"],
                'igdb_name': igdb_details.get('igdb_name', ''),
                'age_rating': igdb_details.get('age_rating', ''),
                'rating': igdb_details.get('rating', ''),
                'player_perspectives': igdb_details.get('player_perspectives', []),
                'genres': igdb_details.get('genres', []),
                'themes': igdb_details.get('themes', []),
                'platforms': igdb_details.get('platforms', []),
                'storyline': igdb_details.get('storyline', ''),
                'keywords': igdb_details.get('keywords', []),
                'release_date': igdb_details.get('release_date', '')
            }
        else:
            # Create empty entry for worlds without IGDB IDs
            result[world] = {
                'igdb_id': '',
                'cover_url': '',
                'game_name': data["game_name"],
                'igdb_name': '',
                'age_rating': 'E', # Defaulting to "everyone" for original worlds/hint worlds
                'rating': '',
                'player_perspectives': [],
                'genres': ["Multiplayer"],
                'themes': [],
                'platforms': ["Archipelago"],
                'storyline': '',
                'keywords': ["hints","archipelago","multiworld"],
                'release_date': ''
            }
            print(f"Created empty entry for {world} (no IGDB ID)")
    
    return result

def get_single_game_details(igdb_id: int) -> dict:
    """
    Gets details for a single game by its IGDB ID.
    Returns a dictionary with the same structure as the full JSON output.
    """
    # Get IGDB details
    igdb_details = get_igdb_game_details(igdb_id)
    
    if not igdb_details:
        return {
            'igdb_id': str(igdb_id),
            'cover_url': '',
            'game_name': '',  # We don't know the world name for a single ID lookup
            'igdb_name': '',
            'age_rating': '',
            'rating': '',
            'player_perspectives': [],
            'genres': [],
            'themes': [],
            'platforms': [],
            'storyline': '',
            'keywords': [],
            'release_date': ''
        }
    
    return {
        'igdb_id': str(igdb_id),
        'cover_url': igdb_details.get('cover_url', ''),
        'game_name': '',  # We don't know the world name for a single ID lookup
        'igdb_name': igdb_details.get('igdb_name', ''),
        'age_rating': igdb_details.get('age_rating', ''),
        'rating': igdb_details.get('rating', ''),
        'player_perspectives': igdb_details.get('player_perspectives', []),
        'genres': igdb_details.get('genres', []),
        'themes': igdb_details.get('themes', []),
        'platforms': igdb_details.get('platforms', []),
        'storyline': igdb_details.get('storyline', ''),
        'keywords': igdb_details.get('keywords', []),
        'release_date': igdb_details.get('release_date', '')
    }

def save_game_details_to_json(single_id: Optional[int] = None):
    """
    Saves the game details to a JSON file.
    If single_id is provided, only saves details for that specific game.
    """
    if single_id is not None:
        game_details = get_single_game_details(single_id)
    else:
        game_details = generate_game_details_json()
        
    output_path = Path.cwd() / 'output' / 'game_details.json'
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(game_details, f, indent=4)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate game details JSON from IGDB')
    parser.add_argument('--id', type=int, help='Get details for a single game by IGDB ID')
    args = parser.parse_args()
    
    save_game_details_to_json(args.id)
    if not args.id:
        from convert_to_readable_outputs import process_game_details
        process_game_details()
        from remove_specific_keywords import process_game_keywords
        process_game_keywords()
        from generate_game_index import main
        main()