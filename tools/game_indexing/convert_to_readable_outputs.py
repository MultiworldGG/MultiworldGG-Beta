import json
from datetime import datetime
from collections import Counter
import os

def fix_cover_url(cover_url):
    if cover_url:
        return cover_url.replace("//", "https://")
    return None

def convert_timestamp_to_year(timestamp):
    """Convert Unix timestamp to year, or None if invalid. Leave as is if already a year or None."""
    if timestamp in (None, "", []):
        return None
    try:
        if isinstance(timestamp, str):
            timestamp = int(timestamp)
        # If it's already a year (e.g., 4-digit and < 3000), leave as is
        if isinstance(timestamp, int) and 1000 <= timestamp <= 3000:
            return timestamp
        return datetime.fromtimestamp(timestamp).year
    except (ValueError, OSError, OverflowError, TypeError):
        return None

def remove_infrequent_keywords(data, min_count=6):
    # First pass: collect all keywords and their counts
    keyword_counts = Counter()
    for game in data.values():
        if 'keywords' in game and isinstance(game['keywords'], list):
            for kw in game['keywords']:
                if kw:  # Skip empty strings
                    keyword_counts[kw] += 1
    
    # Debugging output
    print(f"\nTotal unique keywords: {len(keyword_counts)}")
    print(f"Total keyword occurrences: {sum(keyword_counts.values())}")
    print(f"Removing keywords with {min_count} or fewer occurrences...")
    
    # Second pass: remove infrequent keywords
    removed_count = 0
    for game in data.values():
        if 'keywords' in game and isinstance(game['keywords'], list):
            original_length = len(game['keywords'])
            game['keywords'] = [kw for kw in game['keywords'] if keyword_counts[kw] > min_count]
            removed_count += original_length - len(game['keywords'])
    
    print(f"\nTotal keywords removed: {removed_count}")

def process_game_details():
    # Read the JSON file
    with open(os.path.join(os.path.dirname(__file__), 'output', 'game_details.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Convert all release dates to years or None
    for game in data.values():
        if 'cover_url' in game:
            game['cover_url'] = fix_cover_url(game['cover_url'])
        if 'release_date' in game:
            game['release_date'] = convert_timestamp_to_year(game['release_date'])
    
    # Remove infrequent keywords (<= 4 times)
    remove_infrequent_keywords(data, min_count=5)

    # Write the updated data back to the file
    with open(os.path.join(os.path.dirname(__file__), 'output', 'game_details.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    process_game_details() 