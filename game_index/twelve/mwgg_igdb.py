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

# These constants will be generated during build
GAMES_DATA = {
    "against_the_storm": {
        "igdb_id": "147519",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaazl.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/aru5g.png",
        "key_art_url": "",
        "game_name": "Against the Storm",
        "igdb_name": "Against the Storm",
        "age_rating": "12",
        "rating": [
            "Mild Blood",
            "Alcohol Reference",
            "Use of Tobacco",
            "Language",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Real Time Strategy (RTS)",
            "Simulator",
            "Strategy",
            "Indie"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Nintendo Switch"
        ],
        "storyline": "The rain is your ally and the greatest enemy. It cycles in three seasons requiring you to stay flexible and adapt to changing conditions. In Drizzle, the season of regrowth, natural resources replenish themselves, and it\u2019s time for construction and planting crops. The Clearance is the season of harvest, expansion, and preparations for the last, most unforgiving season of them all. A true test of your city\u2019s strength comes with the Storm when bolts of lightning tear the sky, nothing grows and resources are scarce.",
        "keywords": [
            "roguelite"
        ],
        "release_date": 2023
    },
    "ahit": {
        "igdb_id": "6705",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pl5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar75x.png",
        "key_art_url": "",
        "game_name": "A Hat in Time",
        "igdb_name": "A Hat in Time",
        "age_rating": "7",
        "rating": [
            "Blood",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "time travel",
            "spaceship",
            "female protagonist",
            "action-adventure",
            "cute",
            "snow",
            "wall jump",
            "3d platformer",
            "swimming"
        ],
        "release_date": 2017
    },
    "albw": {
        "igdb_id": "2909",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3p0j.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/wh4w8shdd0oiikmdelth.png",
        "key_art_url": "",
        "game_name": "A Link Between Worlds",
        "igdb_name": "The Legend of Zelda: A Link Between Worlds",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Historical",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Nintendo 3DS"
        ],
        "storyline": "After capturing Princess Zelda and escaping through a rift into the parallel world of Lorule, the evil sorcerer Yuga plan to use the power of the Seven Mages to resurrect the demon king Ganon. The young adventurer Link is called out to restore peace to the kingdom of Hyrule and is granted the ability to merge into walls after obtaining a magic bracelet from the eccentric merchant Ravio, which allows him to reach previously inaccessible areas and travel between the worlds of Hyrule and Lorule.",
        "keywords": [
            "medieval",
            "magic",
            "minigames",
            "2.5d",
            "archery",
            "action-adventure",
            "fairy",
            "bird",
            "princess",
            "snow",
            "sequel",
            "swimming",
            "sword & sorcery",
            "darkness",
            "digital distribution",
            "anthropomorphism",
            "polygonal 3d",
            "bow and arrow",
            "damsel in distress",
            "upgradeable weapons",
            "disorientation zone",
            "descendants of other characters",
            "save point",
            "side quests",
            "potion",
            "real-time combat",
            "self-referential humor",
            "rpg elements",
            "mercenary",
            "coming of age",
            "androgyny",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "bees"
        ],
        "release_date": 2013
    },
    "alttp": {
        "igdb_id": "1026",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3vzn.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14lb.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p2x.png",
        "game_name": "A Link to the Past",
        "igdb_name": "The Legend of Zelda: A Link to the Past",
        "age_rating": "7",
        "rating": [
            "Mild Violence",
            "Mild Animated Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Satellaview",
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "The wizard Agahnim has been abducting descendants of the seven sages, intent on using their power to obliterate the barrier leading to the Dark World. One of the descendants happens to be Princess Zelda, who informs Link of her plight. Armed with a trusty sword and shield, Link begins a journey that will take him through treacherous territory.",
        "keywords": [
            "ghosts",
            "magic",
            "mascot",
            "death",
            "maze",
            "archery",
            "action-adventure",
            "fairy",
            "backtracking",
            "undead",
            "campaign",
            "princess",
            "pixel art",
            "easter egg",
            "teleportation",
            "sequel",
            "giant insects",
            "silent protagonist",
            "swimming",
            "darkness",
            "explosion",
            "monkey",
            "nintendo power",
            "world map",
            "human",
            "shopping",
            "bow and arrow",
            "damsel in distress",
            "disorientation zone",
            "ice stage",
            "saving the world",
            "side quests",
            "potion",
            "grapple",
            "real-time combat",
            "secret area",
            "shielded enemies",
            "walking through walls",
            "mercenary",
            "coming of age",
            "villain",
            "recurring boss",
            "been here before",
            "sleeping",
            "merchants",
            "fetch quests",
            "poisoning",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "status effects",
            "damage over time",
            "monomyth",
            "retroachievements",
            "bees"
        ],
        "release_date": 1991
    },
    "animal_well": {
        "igdb_id": "191435",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4hdh.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1gce.png",
        "key_art_url": "",
        "game_name": "ANIMAL WELL",
        "igdb_name": "Animal Well",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Horror",
            "Survival",
            "Mystery"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Nintendo Switch"
        ],
        "storyline": "It is dark. It is lonely. You don't belong in this world. It's not that it\u2019s a hostile world... it's just... not yours. As you uncover its secrets, the world grows on you. It takes on a feel of familiarity, yet you know that you've only probed the surface. The more you discover, the more you realize how much more there is to discover. Secrets leading to more secrets. You recall the feeling of zooming closer and closer in on a very high-resolution photo. As you hone your focus, the world betrays its secrets.",
        "keywords": [
            "exploration",
            "retro",
            "2d",
            "metroidvania",
            "cute",
            "atmospheric",
            "pixel art",
            "relaxing",
            "controller support"
        ],
        "release_date": 2024
    },
    "apeescape": {
        "igdb_id": "3762",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2gzc.png",
        "artwork_url": "",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3scq.png",
        "game_name": "Ape Escape",
        "igdb_name": "Ape Escape",
        "age_rating": "E",
        "rating": [
            "Mild Animated Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "PlayStation 3",
            "PlayStation",
            "PlayStation Portable"
        ],
        "storyline": "The doctors trustfull test apes have escaped and it's up to you to get out there and retrieve all of them.",
        "keywords": [
            "anime",
            "dinosaurs",
            "time travel",
            "collecting",
            "minigames",
            "multiple endings",
            "amnesia",
            "easter egg",
            "digital distribution",
            "anthropomorphism",
            "monkey",
            "voice acting",
            "human",
            "polygonal 3d",
            "moving platforms",
            "time trials"
        ],
        "release_date": 1999
    },
    "balatro": {
        "igdb_id": "251833",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9f4g.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2c5g.png",
        "key_art_url": "",
        "game_name": "Balatro",
        "igdb_name": "Balatro",
        "age_rating": "12",
        "rating": [
            "Simulated Gambling"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Strategy",
            "Turn-based strategy (TBS)",
            "Indie",
            "Card & Board Game"
        ],
        "themes": [],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "roguelike"
        ],
        "release_date": 2024
    },
    "banjo_tooie": {
        "igdb_id": "3418",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6c1w.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar7us.png",
        "key_art_url": "",
        "game_name": "Banjo-Tooie",
        "igdb_name": "Banjo-Tooie",
        "age_rating": "3",
        "rating": [
            "Crude Humor",
            "Animated Violence",
            "Comic Mischief",
            "Cartoon Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Quiz/Trivia",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "Nintendo 64"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "dinosaurs",
            "collecting",
            "flight",
            "action-adventure",
            "witches",
            "bird",
            "backtracking",
            "achievements",
            "easter egg",
            "sequel",
            "talking animals",
            "swimming",
            "digital distribution",
            "anthropomorphism",
            "breaking the fourth wall",
            "ice stage",
            "underwater gameplay",
            "rpg elements",
            "villain",
            "recurring boss",
            "shape-shifting",
            "temporary invincibility",
            "gliding",
            "lgbtq+",
            "retroachievements"
        ],
        "release_date": 2000
    },
    "bomb_rush_cyberfunk": {
        "igdb_id": "135940",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6ya8.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arzj0.png",
        "key_art_url": "",
        "game_name": "Bomb Rush Cyberfunk",
        "igdb_name": "Bomb Rush Cyberfunk",
        "age_rating": "12",
        "rating": [
            "Language",
            "Violence",
            "Suggestive Themes",
            "Blood"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Sport",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Start your own cypher and dance, paint, trick, face off with the cops and stake your claim to the extrusions and cavities of a sprawling metropolis in an alternate future set to the musical brainwaves of Hideki Naganuma.",
        "keywords": [
            "3d platformer",
            "great soundtrack"
        ],
        "release_date": 2023
    },
    "brotato": {
        "igdb_id": "199116",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaauv.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1m88.png",
        "key_art_url": "",
        "game_name": "Brotato",
        "igdb_name": "Brotato",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Mild Blood"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Fighting",
            "Shooter",
            "Role-playing (RPG)",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "A spaceship from Potato World crashes onto an alien planet. The sole survivor: Brotato, the only potato capable of handling 6 weapons at the same time. Waiting to be rescued by his mates, Brotato must survive in this hostile environment.",
        "keywords": [
            "roguelite"
        ],
        "release_date": 2023
    },
    "cat_quest": {
        "igdb_id": "36597",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qlq.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arab6.png",
        "key_art_url": "",
        "game_name": "Cat Quest",
        "igdb_name": "Cat Quest",
        "age_rating": "3",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2017
    },
    "celeste": {
        "igdb_id": "26226",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3byy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar7u5.png",
        "key_art_url": "",
        "game_name": "Celeste",
        "igdb_name": "Celeste",
        "age_rating": "7",
        "rating": [
            "Alcohol Reference",
            "Fantasy Violence",
            "Mild Language"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Google Stadia",
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Set on a fictional version of Mount Celeste, it follows a young woman named Madeline who attempts to climb the mountain, and must face her inner demons in her quest to reach the summit.",
        "keywords": [
            "exploration",
            "retro",
            "2d",
            "difficult",
            "female protagonist",
            "cute",
            "atmospheric",
            "pixel art",
            "snow",
            "story rich",
            "great soundtrack",
            "digital distribution",
            "lgbtq+"
        ],
        "release_date": 2018
    },
    "celeste_open_world": {
        "igdb_id": "26226",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3byy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar7u5.png",
        "key_art_url": "",
        "game_name": "Celeste (Open World)",
        "igdb_name": "Celeste",
        "age_rating": "7",
        "rating": [
            "Alcohol Reference",
            "Fantasy Violence",
            "Mild Language"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Google Stadia",
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Set on a fictional version of Mount Celeste, it follows a young woman named Madeline who attempts to climb the mountain, and must face her inner demons in her quest to reach the summit.",
        "keywords": [
            "exploration",
            "retro",
            "2d",
            "difficult",
            "female protagonist",
            "cute",
            "atmospheric",
            "pixel art",
            "snow",
            "story rich",
            "great soundtrack",
            "digital distribution",
            "lgbtq+"
        ],
        "release_date": 2018
    },
    "civ_6": {
        "igdb_id": "293",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1rjp.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6uy.png",
        "key_art_url": "",
        "game_name": "Civilization VI",
        "igdb_name": "Sid Meier's Civilization IV",
        "age_rating": "12",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Simulator",
            "Strategy",
            "Turn-based strategy (TBS)"
        ],
        "themes": [
            "Fantasy",
            "Historical",
            "Educational",
            "4X (explore, expand, exploit, and exterminate)"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "turn-based",
            "spaceship",
            "multiple endings",
            "sequel",
            "digital distribution",
            "voice acting",
            "loot gathering",
            "ambient music"
        ],
        "release_date": 2005
    },
    "crosscode": {
        "igdb_id": "35282",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co28wy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar7wo.png",
        "key_art_url": "",
        "game_name": "CrossCode",
        "igdb_name": "CrossCode",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Language"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Shooter",
            "Puzzle",
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "action-adventure",
            "pixel art",
            "digital distribution"
        ],
        "release_date": 2018
    },
    "crystal_project": {
        "igdb_id": "181444",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co48fv.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar19k4.png",
        "key_art_url": "",
        "game_name": "Crystal Project",
        "igdb_name": "Crystal Project",
        "age_rating": "7",
        "rating": [
            "Mild Language",
            "Fantasy Violence",
            "Mild Blood"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Strategy",
            "Turn-based strategy (TBS)",
            "Tactical",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Mystery"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Nintendo Switch"
        ],
        "storyline": "Explore the world, find Crystals, and fulfill the prophecy to bring balance to the land of Sequoia.\n\n...Or maybe you'd rather spend your time collecting neat equipment and artifacts? Or tame strange creatures and fill out all the entries in your archive? Or perhaps you'd rather hunt down every monster and conquer the world's toughest bosses. Or maybe you'd rather travel to the farthest reaches of the land and uncover the world's greatest mysteries.\n\nThe choice is yours, as it should be! Or is it? They say that those who stray out of line will be punished, killed, or worse. Maybe it's for your own good that you stick to collecting Crystals, just like everyone else. But where would the adventure be in that?",
        "keywords": [
            "3d",
            "metroidvania",
            "jrpg",
            "atmospheric"
        ],
        "release_date": 2022
    },
    "ctjot": {
        "igdb_id": "20398",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co54iw.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Chrono Trigger Jets of Time",
        "igdb_name": "Chrono Trigger",
        "age_rating": "12",
        "rating": [
            "Animated Blood",
            "Mild Fantasy Violence",
            "Suggestive Themes",
            "Use of Alcohol"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction"
        ],
        "platforms": [
            "Nintendo DS"
        ],
        "storyline": "",
        "keywords": [
            "time travel",
            "magic"
        ],
        "release_date": 2008
    },
    "cuphead": {
        "igdb_id": "9061",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co62ao.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6yl.png",
        "key_art_url": "",
        "game_name": "Cuphead",
        "igdb_name": "Cuphead",
        "age_rating": "7",
        "rating": [
            "Use of Alcohol and Tobacco",
            "Mild Language",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "pirates",
            "ghosts",
            "retro",
            "magic",
            "2d",
            "robots",
            "side-scrolling",
            "bird",
            "achievements",
            "multiple endings",
            "explosion",
            "digital distribution",
            "anthropomorphism",
            "voice acting",
            "cat",
            "shopping",
            "bow and arrow",
            "violent plants",
            "auto-scrolling levels",
            "temporary invincibility",
            "boss assistance"
        ],
        "release_date": 2017
    },
    "cv64": {
        "igdb_id": "1130",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5geb.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Castlevania 64",
        "igdb_name": "Castlevania",
        "age_rating": "12",
        "rating": [
            "Animated Blood",
            "Animated Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Hack and slash/Beat 'em up",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror"
        ],
        "platforms": [
            "Nintendo 64"
        ],
        "storyline": "Castlevania games debut on the N64 this is the first Castlevania game in 3D. However, the goal of the game remains the same: defeat Dracula and his monsters. The player can choose to be Reinhardt Schneider with traditional whip or Carrie Fernandez who uses magic. A new feature is the presence of an in-game clock that switches time from day to night.",
        "keywords": [
            "ghosts",
            "exploration",
            "bloody",
            "magic",
            "death",
            "horse",
            "maze",
            "female protagonist",
            "action-adventure",
            "witches",
            "multiple protagonists",
            "backtracking",
            "multiple endings",
            "undead",
            "traps",
            "dog",
            "teleportation",
            "bats",
            "day/night cycle",
            "explosion",
            "anthropomorphism",
            "alternate costumes",
            "voice acting",
            "human",
            "polygonal 3d",
            "shopping",
            "upgradeable weapons",
            "loot gathering",
            "skeletons",
            "descendants of other characters",
            "save point",
            "ice stage",
            "unstable platforms",
            "melee",
            "real-time combat",
            "instant kill",
            "difficulty level",
            "moving platforms",
            "plot twist",
            "ambient music",
            "poisoning",
            "retroachievements"
        ],
        "release_date": 1999
    },
    "cvcotm": {
        "igdb_id": "1132",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2zq1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vgm.png",
        "key_art_url": "",
        "game_name": "Castlevania - Circle of the Moon",
        "igdb_name": "Castlevania: Circle of the Moon",
        "age_rating": "12",
        "rating": [
            "Mild Violence",
            "Animated Blood"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror"
        ],
        "platforms": [
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "Taking place in 1830, Circle of the Moon is set in one of the fictional universes of the Castlevania series. The premise of the original series is the eternal conflict between the vampire hunters of the Belmont clan and the immortal vampire Dracula. Circle of the Moon's protagonist, however, is Nathan Graves, whose parents died a decade ago to banish Dracula. Morris Baldwin, who helped in Dracula's banishment, trained him to defeat Dracula and the monsters; Morris ultimately chose him as his successor and gave him the \"Hunter Whip\", to the displeasure of Hugh, Morris' son who trained alongside him.\n\nAt an old castle, Camilla, a minion of Dracula, revives him, only to be interrupted by the arrival of Morris, Nathan, and Hugh. Before they are able to banish him again, Dracula destroys the floor under Nathan and Hugh, causing them to plummet down a long tunnel. Surviving the fall and wishing to find his father, Hugh leaves Nathan behind. Nathan proceeds to search the castle for his mentor. Along the way, he learns that at the next full moon, Morris' soul will be used to return Dracula to full power. He also periodically encounters Hugh, who becomes more hostile as the game progresses. Eventually, Nathan encounters Camilla, who hints that she and Dracula are responsible for the changes in his personality. Nathan vanquishes Camilla in her true form and meets up with Hugh once more. Upon seeing him, Hugh immediately attacks him with the goal of proving himself to his father through Nathan's defeat; Nathan, however, realizes that Dracula is controlling Hugh. Nathan defeats him, and Dracula's control over Hugh breaks. Confessing that he doubted his self-worth when Nathan was chosen as successor, Hugh tasks him with Morris' rescue.\n\nArriving at the ceremonial room, Nathan confronts Dracula, who confirms that he had tampered with Hugh's soul to cause the changes in his personality. They begin to fight and halfway through, Dracula teleports away to gain his full power. Hugh then frees his father and tasks Nathan with Dracula's banishment. Nathan continues the battle and defeats Dracula; escaping the collapsing castle, he reunites with Morris and Hugh. Nathan is declared a master vampire hunter by Morris. Hugh vows to retrain under Morris due to his failure.",
        "keywords": [
            "gravity",
            "magic",
            "metroidvania",
            "death",
            "horse",
            "action-adventure",
            "backtracking",
            "wall jump",
            "bats",
            "leveling up",
            "skeletons",
            "save point",
            "unstable platforms",
            "melee",
            "moving platforms",
            "villain"
        ],
        "release_date": 2001
    },
    "diddy_kong_racing": {
        "igdb_id": "2723",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wgj.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar21yi.png",
        "key_art_url": "",
        "game_name": "Diddy Kong Racing",
        "igdb_name": "Diddy Kong Racing",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Racing"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "Nintendo 64"
        ],
        "storyline": "Timber the Tiger's parents picked a fine time to go on vacation. When they come back they're going to be faced with an island trashed by the spiteful space bully Wizpig - unless the local animals can do something about it! So join Diddy Kong as he teams up with Timber the Tiger Pipsy the Mouse and Taj the Genie in an epic racing adventure unlike anything you've ever experienced before! This unique game blends adventure and racing like no other game! Roam anywhere you want on the island by car plane or hovercraft! An enormous amount of single-player and multi-player modes! Feel the action when you use the N64 Rumble Pak and save your times on the N64 Controller Pak!",
        "keywords": [
            "flight",
            "snow",
            "talking animals",
            "anthropomorphism",
            "monkey",
            "secret area",
            "time trials",
            "behind the waterfall",
            "retroachievements"
        ],
        "release_date": 1997
    },
    "dk64": {
        "igdb_id": "1096",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co289i.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kpl.png",
        "key_art_url": "",
        "game_name": "Donkey Kong 64",
        "igdb_name": "Donkey Kong 64",
        "age_rating": "7",
        "rating": [
            "Mild Animated Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "",
        "keywords": [
            "gravity",
            "minigames",
            "death",
            "fairy",
            "multiple protagonists",
            "multiple endings",
            "artificial intelligence",
            "giant insects",
            "day/night cycle",
            "digital distribution",
            "anthropomorphism",
            "monkey",
            "polygonal 3d",
            "upgradeable weapons",
            "loot gathering",
            "descendants of other characters",
            "real-time combat",
            "moving platforms",
            "recurring boss",
            "completion percentage",
            "invisibility",
            "foreshadowing",
            "retroachievements"
        ],
        "release_date": 1999
    },
    "dkc": {
        "igdb_id": "1090",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co70qn.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar407r.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar407t.png",
        "game_name": "Donkey Kong Country",
        "igdb_name": "Donkey Kong Country",
        "age_rating": "7",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "On a dark and stormy night in Donkey Kong Island, Diddy Kong, Donkey Kong's nephew has taken the weighty responsibility of guarding DK's precious banana hoard for one night, as a part of his \"hero training\". DK entrusts Diddy with protecting the hoard until midnight, when he would be relieved, while DK himself goes to sleep as he is tired.\n\nEverything seems to go smoothly in the hoard until Diddy hears some noises. Diddy hears some voices outside and gets scared, asking who's there. King K. Rool, who had commanded his Kremling minions to steal the bananas. Two ropes drop from above and suddenly two Kritters appear. Diddy cartwheels them both easily, but then a Krusha (Klump in the instruction booklet) comes in as backup. As Diddy is not strong enough to defeat Krusha by himself, he is overpowered and defeated by the Kremling. The lizars seal Diddy inside a barrel and then throw it in the bushes.\nDonkey's grandfather, Cranky Kong, rushes inside the treehouse to tell Donkey Kong to wake up so he may tell him what happened. He then tells Donkey to check his Banana Cave. Donkey Kong is infuriated, exclaiming that the Kremlings will pay for stealing his banana hoard and kidnapping his little buddy. Donkey goes on to say that he will hunt every corner of the island for his bananas back.",
        "keywords": [
            "gravity",
            "death",
            "2.5d",
            "flight",
            "side-scrolling",
            "multiple protagonists",
            "overworld",
            "snow",
            "giant insects",
            "talking animals",
            "silent protagonist",
            "swimming",
            "darkness",
            "digital distribution",
            "anthropomorphism",
            "bonus stage",
            "monkey",
            "nintendo power",
            "world map",
            "breaking the fourth wall",
            "descendants of other characters",
            "save point",
            "ice stage",
            "checkpoints",
            "unstable platforms",
            "real-time combat",
            "underwater gameplay",
            "instant kill",
            "secret area",
            "moving platforms",
            "recurring boss",
            "water level",
            "auto-scrolling levels",
            "speedrun",
            "boss assistance",
            "ambient music",
            "retroachievements"
        ],
        "release_date": 1994
    },
    "dkc2": {
        "igdb_id": "1092",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co217m.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar4088.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3okv.png",
        "game_name": "Donkey Kong Country 2",
        "igdb_name": "Donkey Kong Country 2: Diddy's Kong Quest",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "It was a relaxing, sunny day on Donkey Kong Island. Funky Kong is seen surfing and then falling off his board. He asked for Donkey Kong to join him, but the hero simply continues lounging. Cranky Kong goes up to him and complains how he never took breaks, \"whisking off maidens and throwing barrels seven days a week\", but Donkey ignores him, confident that he is a hero and that King K. Rool is gone for good. Cranky soon leaves.\n\nMeanwhile, above, Kaptain K. Rool, aboard his vessel, The Flying Krock, commands his minions to invade the island and take Donkey captive so that his next attempt at stealing the banana hoard will not be a failure and the hero will never mess with his plans again. Donkey, still lounging, did not notice the attack until Kutlasses ambushed him and took him prisoner. Kaptain K. Rool assures Donkey Kong that he will never see his precious island or his friends again.\n\nLater and back on the island, Diddy, Dixie and Cranky Kong find Donkey missing, along with a note. It reads:\nHah-arrrrh! We have got the big monkey! If you want him back, you scurvy dogs, you'll have to hand over the banana hoard!\nKaptain K. Rool\nAt this point, Wrinkly, Funky and Swanky Kong come to the scene. Cranky suggests to give up the hoard, but Diddy insists that Donkey Kong would be furious if he lost his bananas after all trouble recovering them at the last time. Diddy and Dixie Kong ride to Crocodile Isle via Enguarde the Swordfish, and then start their quest.",
        "keywords": [
            "pirates",
            "ghosts",
            "gravity",
            "female protagonist",
            "side-scrolling",
            "multiple protagonists",
            "overworld",
            "multiple endings",
            "sequel",
            "giant insects",
            "talking animals",
            "silent protagonist",
            "climbing",
            "swimming",
            "darkness",
            "explosion",
            "digital distribution",
            "anthropomorphism",
            "bonus stage",
            "monkey",
            "spider",
            "nintendo power",
            "world map",
            "cat",
            "breaking the fourth wall",
            "game reference",
            "descendants of other characters",
            "save point",
            "sprinting mechanics",
            "ice stage",
            "checkpoints",
            "underwater gameplay",
            "instant kill",
            "secret area",
            "self-referential humor",
            "recurring boss",
            "water level",
            "auto-scrolling levels",
            "temporary invincibility",
            "boss assistance",
            "completion percentage",
            "ambient music",
            "retroachievements"
        ],
        "release_date": 1995
    },
    "dkc3": {
        "igdb_id": "1094",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co217n.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3ozm.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3ozn.png",
        "game_name": "Donkey Kong Country 3",
        "igdb_name": "Donkey Kong Country 3: Dixie Kong's Double Trouble!",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "Months after the Kongs' second triumph over the Kremling Krew, they continue to celebrate. One day, DK and Diddy suddenly disappear, and a letter from Diddy says they were out exploring the island again.\n\nHowever, several days pass without their return, and Dixie knows something is up. She takes matters into her own hands, and made her way to the southern shores of Donkey Kong Island, to the Northern Kremisphere, a Canadian and northern European-inspired landmass. There she meets Wrinkly Kong, and Wrinkly confirmed that the Kongs had passed by. Dixie then makes her way to Funky's Rentals. Funky suggests her to take her baby cousin Kiddy Kong along with her in the search. Funky lends them a boat and the two venture off to find Donkey and Diddy Kong.",
        "keywords": [
            "gravity",
            "minigames",
            "2.5d",
            "female protagonist",
            "side-scrolling",
            "multiple protagonists",
            "overworld",
            "bird",
            "snow",
            "giant insects",
            "talking animals",
            "swimming",
            "darkness",
            "explosion",
            "anthropomorphism",
            "bonus stage",
            "monkey",
            "nintendo power",
            "world map",
            "descendants of other characters",
            "save point",
            "ice stage",
            "checkpoints",
            "secret area",
            "shielded enemies",
            "moving platforms",
            "recurring boss",
            "auto-scrolling levels",
            "ambient music",
            "behind the waterfall",
            "retroachievements"
        ],
        "release_date": 1996
    },
    "dontstarvetogether": {
        "igdb_id": "17832",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaaqp.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar5m2.png",
        "key_art_url": "",
        "game_name": "Don't Starve Together",
        "igdb_name": "Don't Starve Together",
        "age_rating": "12",
        "rating": [
            "Crude Humor",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Simulator",
            "Strategy",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Horror",
            "Survival",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Nintendo Switch"
        ],
        "storyline": "Discover and explore a massive procedurally generated and biome-rich world with countless resources and threats. Whether you stick to the surface world, go spelunking in the caves, dive deeper into the Ancient Archive, or set sail for the Lunar islands, it will be a long time before you run out of things to do.\n\nSeasonal bosses, wandering menaces, lurking shadow creatures, and plenty of flora and fauna ready to turn you into a spooky ghost.\n\nPlow fields and sow seeds to grow the farm of your dreams. Tend to your crops to help your fellow survivors stay fed and ready for the challenges to come.\n\nProtect yourself, your friends, and everything you have managed to gather, because you can be sure, somebody or something is going to want it back.\n\nEnter a strange and unexplored world full of odd creatures, hidden dangers, and ancient secrets. Gather resources to craft items and build structures that match your survival style. Play your way as you unravel the mysteries of \"The Constant\".\n\nCooperate with your friends in a private game, or find new friends online. Work with other players to survive the harsh environment, or strike out on your own.\n\nDo whatever it takes, but most importantly, Don't Starve.",
        "keywords": [
            "2d",
            "crafting",
            "difficult",
            "action-adventure",
            "funny",
            "atmospheric",
            "sequel",
            "digital distribution",
            "bees"
        ],
        "release_date": 2016
    },
    "doronko_wanko": {
        "igdb_id": "290647",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7zj5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2t55.png",
        "key_art_url": "",
        "game_name": "DORONKO WANKO",
        "igdb_name": "Doronko Wanko",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "Simulator"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "dog"
        ],
        "release_date": 2024
    },
    "dredge": {
        "igdb_id": "164867",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9kyk.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar10y5.png",
        "key_art_url": "",
        "game_name": "Dredge",
        "igdb_name": "Dredge",
        "age_rating": "12",
        "rating": [
            "Mild Violence",
            "Use of Tobacco"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Simulator",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror",
            "Open world",
            "Mystery"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "3d",
            "fishing",
            "stylized",
            "story rich",
            "digital distribution"
        ],
        "release_date": 2023
    },
    "dw1": {
        "igdb_id": "3878",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2dyy.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Digimon World",
        "igdb_name": "Digimon World 4",
        "age_rating": "E",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "Xbox",
            "Nintendo GameCube",
            "PlayStation 2"
        ],
        "storyline": "The Yamato Server disappears after the X-Virus attacks, and the Doom Server has taken it's place. It's up to the you and up to 3 of your friends, the Digital Security Guard (D.S.G.) to venture into the Doom Server, discover the source of the virus and deal with the infection before it can infect the Home server.\n\nYou will venture into the Dry Lands stop the virus from spreading, into the Venom Jungle to stop the Dread Note from launching and then the Machine Pit to destroy the final boss.\n\nAfter finishing the game for the first time, you unlock Hard mode, where the enemies are stronger, but you keep all of your levels, equipment and digivolutions. Do it again, and you unlock the hardest difficulty, Very Hard.",
        "keywords": [
            "anime",
            "sequel",
            "leveling up",
            "voice acting",
            "polygonal 3d",
            "shopping"
        ],
        "release_date": 2005
    },
    "earthbound": {
        "igdb_id": "2899",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6v07.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1gd3.png",
        "key_art_url": "",
        "game_name": "EarthBound",
        "igdb_name": "EarthBound",
        "age_rating": "12",
        "rating": [],
        "player_perspectives": [
            "First person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction",
            "Drama"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii U",
            "New Nintendo 3DS",
            "Game Boy Advance",
            "Super Famicom"
        ],
        "storyline": "The story begins when Ness is awakened by a meteor that has plummeted to the earth near his home, whereupon he proceeds to investigate the crash site. When Ness gets to the crash site he discovers a police roadblock and Pokey Minch, his friend and neighbor, who tells him to go home. Later, Ness is woken up again by Pokey knocking at his door, demanding help to find his brother Picky.\n\nThey find him near the meteor sleeping behind a tree and wake him up. Then the three encounter an insect from the meteor named Buzz Buzz who informs Ness that he is from the future where the \"universal cosmic destroyer\", Giygas, dominates the planet. Buzz Buzz senses great potential in Ness and instructs him to embark on a journey to seek out and record the melodies of eight \"sanctuaries,\" unite his own powers with the Earth's and gain the strength required to confront Giygas.",
        "keywords": [
            "aliens",
            "ghosts",
            "dinosaurs",
            "time travel",
            "2d",
            "turn-based",
            "robots",
            "female protagonist",
            "multiple protagonists",
            "teleportation",
            "darkness",
            "nintendo power",
            "leveling up",
            "damsel in distress",
            "party system",
            "descendants of other characters",
            "save point",
            "saving the world",
            "self-referential humor",
            "fire manipulation",
            "status effects",
            "retroachievements"
        ],
        "release_date": 1994
    },
    "enderlilies": {
        "igdb_id": "138858",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9s9e.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar96z.png",
        "key_art_url": "",
        "game_name": "Ender Lilies",
        "igdb_name": "Ender Lilies: Quietus of the Knights",
        "age_rating": "12",
        "rating": [
            "Violence",
            "Blood"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Once upon a time, in the End's Kingdom, the Dying Rain suddenly started to fall, transforming all living things it touched into bloodthirsty corpses. Following this tragedy, the kingdom quickly fell into chaos and soon, no one remained. The rain, as if cursed, would never stop falling on the land. In the depths of a forsaken church, Lily opens her eyes...",
        "keywords": [
            "metroidvania",
            "female protagonist",
            "witches",
            "soulslike"
        ],
        "release_date": 2021
    },
    "factorio": {
        "igdb_id": "7046",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1tfy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vdh.png",
        "key_art_url": "",
        "game_name": "Factorio",
        "igdb_name": "Factorio",
        "age_rating": "7",
        "rating": [
            "Blood",
            "Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Simulator",
            "Strategy",
            "Indie"
        ],
        "themes": [
            "Science fiction",
            "Survival",
            "Sandbox"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Nintendo Switch"
        ],
        "storyline": "You crash land on an alien planet and must research a way to get yourself a rocket out of the planet. Defend yourself from the natives who dislike the pollution your production generates.",
        "keywords": [
            "aliens",
            "crafting",
            "digital distribution"
        ],
        "release_date": 2020
    },
    "faxanadu": {
        "igdb_id": "1974",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5jif.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vkf.png",
        "key_art_url": "",
        "game_name": "Faxanadu",
        "igdb_name": "Faxanadu",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence",
            "Use of Tobacco"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox"
        ],
        "platforms": [
            "Wii",
            "Family Computer",
            "Nintendo Entertainment System"
        ],
        "storyline": "The player-controlled protagonist of is an unidentified wanderer. He has no name, though the Japanese version allows the player to choose one. The game begins when he approaches Eolis, his hometown, after an absence to find it in disrepair and virtually abandoned. Worse still, the town is under attack by Dwarves.The Elven king explains that the Elf fountain water, their life source, has stopped and provides the protagonist with 1500 golds, the games currency, to prepare for his journey to uncover the cause.As the story unfolds, it is revealed that Elves and Dwarfs lived in harmony among the World Tree until The Evil One emerged from a fallen meteorite. The Evil One then transformed the Dwarves into monsters against their will and set them against the Elves. The Dwarf King, Grieve, swallowed his magical sword before he was transformed, hiding it in his own body to prevent The Evil One from acquiring it. It is only with this sword that The Evil One can be destroyed.His journey takes him to four overworld areas: The tree's buttress, the inside of the trunk, the tree's branches and finally the Dwarves' mountain stronghold.",
        "keywords": [
            "magic",
            "metroidvania",
            "backtracking",
            "save point",
            "temporary invincibility",
            "merchants"
        ],
        "release_date": 1987
    },
    "ff1": {
        "igdb_id": "385",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2xv8.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vi4.png",
        "key_art_url": "",
        "game_name": "Final Fantasy",
        "igdb_name": "Final Fantasy",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Kids"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Wii",
            "Family Computer",
            "Wii U",
            "Nintendo Entertainment System"
        ],
        "storyline": "The story follows four youths called the Light Warriors, who each carry one of their world's four elemental orbs which have been darkened by the four Elemental Fiends. Together, they quest to defeat these evil forces, restore light to the orbs, and save their world.",
        "keywords": [
            "jrpg"
        ],
        "release_date": 1987
    },
    "ff4fe": {
        "igdb_id": "387",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2y6s.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vks.png",
        "key_art_url": "",
        "game_name": "Final Fantasy IV Free Enterprise",
        "igdb_name": "Final Fantasy II",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence",
            "Mild Suggestive Themes"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii"
        ],
        "storyline": "",
        "keywords": [
            "jrpg",
            "retroachievements"
        ],
        "release_date": 1991
    },
    "ffmq": {
        "igdb_id": "415",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2y0b.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar21za.png",
        "key_art_url": "",
        "game_name": "Final Fantasy Mystic Quest",
        "igdb_name": "Final Fantasy: Mystic Quest",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "Super Famicom"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "casual",
            "turn-based",
            "jrpg",
            "overworld",
            "undead",
            "sword & sorcery",
            "explosion",
            "party system",
            "rock music",
            "retroachievements"
        ],
        "release_date": 1992
    },
    "ffta": {
        "igdb_id": "414",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wyp.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kju.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3on9.png",
        "game_name": "Final Fantasy Tactics Advance",
        "igdb_name": "Final Fantasy Tactics Advance",
        "age_rating": "7",
        "rating": [
            "Mild Violence",
            "Alcohol Reference"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Strategy",
            "Turn-based strategy (TBS)",
            "Tactical"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [
            "magic",
            "turn-based",
            "jrpg",
            "death",
            "overworld",
            "backtracking",
            "snow",
            "sequel",
            "explosion",
            "bow and arrow",
            "breaking the fourth wall",
            "party system",
            "melee",
            "stat tracking",
            "rock music",
            "coming of age",
            "been here before",
            "androgyny",
            "damage over time"
        ],
        "release_date": 2003
    },
    "fm": {
        "igdb_id": "4108",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ui5.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Yu-Gi-Oh! Forbidden Memories",
        "igdb_name": "Yu-Gi-Oh! Forbidden Memories",
        "age_rating": "E",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Strategy",
            "Turn-based strategy (TBS)",
            "Card & Board Game"
        ],
        "themes": [
            "Fantasy",
            "Historical"
        ],
        "platforms": [
            "PlayStation"
        ],
        "storyline": "The game begins in ancient Egypt, with Prince Atem sneaking out of the palace to see his friends, Jono and Teana, at the dueling grounds. While there, they witness a ceremony performed by the mages, which is darker than the ceremonies that they normally perform. After the ceremony, Atem duels one of the priests, named Seto, and defeats him.\n\nWhen Atem returns to the palace, he is quickly sent to bed by Simon Muran, his tutor and advisor. As Simon walks away, he is informed by a guard that the high priest Heishin has invaded the palace, using a strange magic. Muran searches for Heishin. When Muran finds him, Heishin tells Muran that he has found the Dark Power, then uses the Millennium Rod to blast Muran. When Heishin finds Atem, he threatens to kill the Egyptian king and queen if he does not hand over the Millennium Puzzle. Muran appears behind Heishin and tells Atem to smash the puzzle. Atem obeys, and Muran seals himself and Atem inside the puzzle, to wait for someone to reassemble it.\n\nFive thousand years later, Yugi Mutou reassembles the puzzle. He speaks to Atem in the puzzle, and Atem gives Yugi six blank cards. Not sure what they are for, he carries them into a Dueling Tournament. After he defeats one of the duelists, one of the cards is filled with a Millennium item. Realizing what the cards are for, Yugi completes the tournament and fills all six cards with Millennium items. This allows Atem to return to his time.\n\nOnce in his own time, Muran tells Atem of what has happened since he was sealed away. Heishin and the mages have taken control of the kingdom with the Millennium items, and that the only way to free the kingdom is to recover the items from the mages guarding them. After passing this on, Muran dies.\n\nAfter he catches up with Jono and Teana, he goes to the destroyed palace and searches it. He finds Seto, who gives him a map with the locations of the mages and the Millennium items, and asks him to defeat the mages.\n\nAfter Atem recovers all of the Millennium items but one, Seto leads him to Heishin, who holds the Millennium Rod. Atem defeats Heishin, but discovers that Seto has the Millennium Rod, and merely wanted to use Atem to gather the items in one place. Atem duels Seto for the items and defeats him, but after the duel, Heishin grabs the items and uses them to summon the DarkNite. Hoping to use the DarkNite to destroy his enemies, he doesn't have the item to prove his authority and as a result, the DarkNite instead turns Heishin into a card. Heishin now turned into a playing card, DarkNite now mocks Heishin before incinerating the card. After Atem shows that he had the Millennium Items, DarkNite challenges him to a duel. Atem defeats him, and he transforms into Nitemare, who challenges Atem again. Atem defeats him again, and Nitemare begrudgingly returns from where he came. Atem then is able to take the throne and lead his people in peace.",
        "keywords": [
            "anime",
            "turn-based"
        ],
        "release_date": 1999
    },
    "getting_over_it": {
        "igdb_id": "72373",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3wl5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6y0.png",
        "key_art_url": "",
        "game_name": "Getting Over It",
        "igdb_name": "Getting Over It with Bennett Foddy",
        "age_rating": "E",
        "rating": [],
        "player_perspectives": [
            "Third person",
            "Side view"
        ],
        "genres": [
            "Platform",
            "Simulator",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Horror",
            "Comedy"
        ],
        "platforms": [
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac"
        ],
        "storyline": "Climb up an enormous mountain with nothing but a hammer and a pot.",
        "keywords": [
            "casual",
            "difficult",
            "funny",
            "story rich",
            "great soundtrack",
            "digital distribution"
        ],
        "release_date": 2017
    },
    "gstla": {
        "igdb_id": "1173",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co25rt.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kpa.png",
        "key_art_url": "",
        "game_name": "Golden Sun The Lost Age",
        "igdb_name": "Golden Sun: The Lost Age",
        "age_rating": "7",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "\"It is the dawn of a new age...And the heroes of Golden Sun have been abandoned. Now, the world is falling into darkness. A new band of adventurers is the world's final hope...but they may also be its doom. Pursued by the heroes of the original Golden Sun, they must race to complete their quest before the world becomes lost to the ages.\"",
        "keywords": [
            "anime",
            "magic",
            "minigames",
            "turn-based",
            "death",
            "overworld",
            "snow",
            "sequel",
            "silent protagonist",
            "leveling up",
            "human",
            "party system",
            "save point",
            "potion",
            "melee",
            "rock music",
            "been here before",
            "sleeping",
            "androgyny",
            "fire manipulation",
            "behind the waterfall"
        ],
        "release_date": 2002
    },
    "hades": {
        "igdb_id": "113112",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co39vc.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar17uy.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3m4s.png",
        "game_name": "Hades",
        "igdb_name": "Hades",
        "age_rating": "12",
        "rating": [
            "Mild Language",
            "Alcohol Reference",
            "Violence",
            "Suggestive Themes",
            "Blood"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Hack and slash/Beat 'em up",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Drama"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Zagreus, the son of Hades, has discovered that his mother, which he was led to believe was Nyx, Night Incarnate, is actually someone else, and is outside Hell. He is now attempting to escape his father's domain, with the help of the other gods of Olympus, in an attempt to find his real mother.",
        "keywords": [
            "roguelike",
            "difficult",
            "stylized",
            "story rich",
            "roguelite",
            "you can pet the dog"
        ],
        "release_date": 2020
    },
    "hcniko": {
        "igdb_id": "142405",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2o6i.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arz25.png",
        "key_art_url": "",
        "game_name": "Here Comes Niko!",
        "igdb_name": "Here Comes Niko!",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "exploration",
            "3d",
            "minigames",
            "fishing",
            "female protagonist",
            "stylized",
            "achievements",
            "cute",
            "pixel art",
            "snow",
            "dog",
            "relaxing",
            "talking animals",
            "3d platformer",
            "swimming",
            "anthropomorphism",
            "game reference",
            "secret area",
            "behind the waterfall",
            "controller support"
        ],
        "release_date": 2021
    },
    "hk": {
        "igdb_id": "14593",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co93cr.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ylrp6zuf9e7tcu1nvuir.png",
        "key_art_url": "",
        "game_name": "Hollow Knight",
        "igdb_name": "Hollow Knight",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Mild Blood"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Wii U",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "2d",
            "metroidvania",
            "action-adventure",
            "achievements",
            "atmospheric",
            "giant insects",
            "silent protagonist",
            "shielded enemies",
            "merchants",
            "fast traveling",
            "controller support",
            "interconnected-world"
        ],
        "release_date": 2017
    },
    "jakanddaxter": {
        "igdb_id": "1528",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1w7q.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/yvqffc6igxmvpzokkkf2.png",
        "key_art_url": "",
        "game_name": "Jak and Daxter: The Precursor Legacy",
        "igdb_name": "Jak and Daxter: The Precursor Legacy",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Mild Suggestive Themes"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Racing",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Comedy",
            "Open world"
        ],
        "platforms": [
            "PlayStation 4",
            "PlayStation 2"
        ],
        "storyline": "The opening sequence of the game features Jak and Daxter in a speedboat headed for Misty Island, an area prohibited by their watch over Samos. Upon arriving to the island, Daxter had second thoughts about straying from the village. The two perch on a large skeleton to observe a legion of lurkers crowded around two dark figures, Gol and Maia, who were commanding the lurkers to \"deal harshly with anyone who strays from the village,\" and to search for any precursor artifacts and eco near Sandover Village.[4] After the secret observation, Jak and Daxter continue searching the island. Daxter trips on a dark eco canister which he tosses to Jak after expressing his dislike for the item, and as Jak caught the object it lit up. Shortly afterwards a bone armor lurker suddenly confronted the two, where Jak threw the dark eco canister at the lurker, killing it, but inadvertently knocked Daxter into a dark eco silo behind him. When Daxter reemerged, he was in the form of an ottsel, and upon realizing the transformation he began to panic.",
        "keywords": [
            "exploration",
            "mascot",
            "backtracking",
            "artificial intelligence",
            "snow",
            "teleportation",
            "silent protagonist",
            "climbing",
            "swimming",
            "day/night cycle",
            "anthropomorphism",
            "world map",
            "voice acting",
            "polygonal 3d",
            "breaking the fourth wall",
            "descendants of other characters",
            "save point",
            "ice stage",
            "checkpoints",
            "coming of age",
            "moving platforms",
            "temporary invincibility",
            "damage over time"
        ],
        "release_date": 2001
    },
    "k64": {
        "igdb_id": "2713",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wcz.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1krk.png",
        "key_art_url": "",
        "game_name": "Kirby 64 - The Crystal Shards",
        "igdb_name": "Kirby 64: The Crystal Shards",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "On the planet of Ripple Star, lives a group of kind and peaceful fairies. The planet itself is protected from danger by the power of the great Crystal, which watches over Ripple Star. This power, however, draws the attention of Dark Matter, who wishes to use the great Crystal for its own evil agenda. Its gigantic mass attacks and searches for the Crystal, blackening the sky and sending the fairies into panic. In response to the threat Dark Matter presents, the queen of Ripple Star orders a fairy named Ribbon to take the Crystal to a safe place. Ribbon tries to fly away with the Crystal in tow, but is stopped by three orbs sent by Dark Matter. The Crystal shatters into 74 shards, scattered throughout several planets, and Ribbon crashes onto Planet Popstar. Kirby finds one shard and gives it to Ribbon, whereupon the two set out to find the others. Once Kirby and his friends collect every Crystal Shard and defeat Miracle Matter, Dark Matter flees Ripple Star and explodes. The victory is cut short, however, as the Crystal detects a powerful presence of Dark Matter energy within the Fairy Queen and expels it from her, manifesting over the planet to create Dark Star. Kirby and his friends infiltrate Dark Star, and King Dedede launches them up to challenge 02. Kirby and Ribbon, armed with their Shard Gun, destroyed 02 and the Dark Star.",
        "keywords": [
            "minigames",
            "mascot",
            "2.5d",
            "side-scrolling",
            "fairy",
            "multiple endings",
            "silent protagonist",
            "anthropomorphism",
            "polygonal 3d",
            "melee",
            "moving platforms",
            "shape-shifting",
            "auto-scrolling levels",
            "retroachievements"
        ],
        "release_date": 2000
    },
    "kdl3": {
        "igdb_id": "3720",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co25su.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kr4.png",
        "key_art_url": "",
        "game_name": "Kirby's Dream Land 3",
        "igdb_name": "Kirby's Dream Land 3",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "Super Famicom"
        ],
        "storyline": "",
        "keywords": [
            "mascot",
            "side-scrolling",
            "melee",
            "shape-shifting",
            "retroachievements"
        ],
        "release_date": 1997
    },
    "kh1": {
        "igdb_id": "1219",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co30zf.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/xsqeggrjy7tzab4gtab9.png",
        "key_art_url": "",
        "game_name": "Kingdom Hearts",
        "igdb_name": "Kingdom Hearts",
        "age_rating": "7",
        "rating": [
            "Violence",
            "Cartoon Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 2"
        ],
        "storyline": "When his world is destroyed and his friends mysteriously disappear, a young boy named Sora is thrust into a quest to find his missing friends and prevent the armies of darkness from destroying many other worlds. During his quest, he meets many characters from classic Disney films and a handful from the Final Fantasy video game series.",
        "keywords": [
            "pirates",
            "minigames",
            "death",
            "action-adventure",
            "backtracking",
            "multiple endings",
            "princess",
            "swimming",
            "sword & sorcery",
            "anthropomorphism",
            "alternate costumes",
            "leveling up",
            "voice acting",
            "cat",
            "polygonal 3d",
            "damsel in distress",
            "party system",
            "save point",
            "potion",
            "melee",
            "real-time combat",
            "underwater gameplay",
            "stat tracking",
            "villain",
            "recurring boss",
            "water level",
            "plot twist",
            "gliding"
        ],
        "release_date": 2002
    },
    "kh2": {
        "igdb_id": "1221",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co30t1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/quibnp6vdu6lmwsulsdi.png",
        "key_art_url": "",
        "game_name": "Kingdom Hearts 2",
        "igdb_name": "Kingdom Hearts II",
        "age_rating": "12",
        "rating": [
            "Mild Blood",
            "Violence",
            "Use of Alcohol"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 3",
            "PlayStation 4",
            "PlayStation 2"
        ],
        "storyline": "One year after the events of Kingdom Hearts: Chain of Memories, Sora, Donald and Goofy awaken in Twilight Town. Bent on the quest to find Riku and King Mickey Mouse, the three begin their journey. However, they soon discover that while they have been asleep, the Heartless are back. Not only that, but new enemies also showed up during their absence. Sora, Donald and Goofy set off on a quest to rid the world of the Heartless once more, uncovering the many secrets that linger about Ansem and the mysterious Organization XIII.",
        "keywords": [],
        "release_date": 2005
    },
    "ladx": {
        "igdb_id": "1027",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4o47.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kl1.png",
        "key_art_url": "",
        "game_name": "Link's Awakening DX Beta",
        "igdb_name": "The Legend of Zelda: Link's Awakening DX",
        "age_rating": "7",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Game Boy Color",
            "Nintendo 3DS"
        ],
        "storyline": "After the events of A Link to the Past, the hero Link travels by ship to other countries to train for further threats. After being attacked at sea, Link's ship sinks and he finds himself stranded on Koholint Island. He awakens to see a beautiful woman looking down at him and soon learns the island has a giant egg on top of a mountain that the Wind Fish inhabits deep inside. Link is told to awaken the wind fish and all will be answered, so he sets out on another quest.",
        "keywords": [
            "magic",
            "mascot",
            "fishing",
            "death",
            "maze",
            "action-adventure",
            "fairy",
            "backtracking",
            "undead",
            "campaign",
            "princess",
            "pixel art",
            "easter egg",
            "silent protagonist",
            "sword & sorcery",
            "darkness",
            "digital distribution",
            "monkey",
            "world map",
            "human",
            "bow and arrow",
            "breaking the fourth wall",
            "disorientation zone",
            "side quests",
            "potion",
            "real-time combat",
            "walking through walls",
            "moving platforms",
            "tentacles",
            "fetch quests",
            "status effects"
        ],
        "release_date": 1998
    },
    "landstalker": {
        "igdb_id": "15072",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kb9.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar30jm.png",
        "key_art_url": "",
        "game_name": "Landstalker - The Treasures of King Nole",
        "igdb_name": "Landstalker",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox"
        ],
        "platforms": [
            "Linux",
            "Wii",
            "Sega Mega Drive/Genesis",
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "action-adventure",
            "fairy",
            "leveling up",
            "real-time combat"
        ],
        "release_date": 1992
    },
    "lego_star_wars_tcs": {
        "igdb_id": "2682",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qrr.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arp30.png",
        "key_art_url": "",
        "game_name": "Lego Star Wars: The Complete Saga",
        "igdb_name": "LEGO Star Wars: The Complete Saga",
        "age_rating": "3",
        "rating": [
            "Fantasy Violence",
            "Crude Humor",
            "Cartoon Violence",
            "Animated Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Comedy",
            "Kids"
        ],
        "platforms": [
            "PlayStation 3",
            "Wii",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Xbox 360"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "ghosts",
            "gravity",
            "robots",
            "flight",
            "multiple protagonists",
            "achievements",
            "princess",
            "snow",
            "explosion",
            "alternate costumes",
            "customizable characters",
            "polygonal 3d",
            "shopping",
            "melee",
            "grapple",
            "rpg elements",
            "villain"
        ],
        "release_date": 2007
    },
    "lufia2ac": {
        "igdb_id": "1178",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9mg3.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Lufia II: Ancient Cave",
        "igdb_name": "Lufia II: Rise of the Sinistrals",
        "age_rating": "E",
        "rating": [
            "Mild Animated Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Super Famicom"
        ],
        "storyline": "",
        "keywords": [
            "retroachievements"
        ],
        "release_date": 1995
    },
    "luigismansion": {
        "igdb_id": "2485",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wr1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3fnc.png",
        "key_art_url": "",
        "game_name": "Luigi's Mansion",
        "igdb_name": "Luigi's Mansion",
        "age_rating": "E",
        "rating": [],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror",
            "Comedy"
        ],
        "platforms": [
            "Nintendo GameCube"
        ],
        "storyline": "One day, Luigi received an unexpected message: You've won a huge mansion! Naturally, He[sic] got very excited and called his brother, Mario. \"Mario? It's me, Luigi. I won myself a big mansion! Meet me there and we'll celebrate, what do you say?\"\n\nLuigi tried to follow the map to his new mansion, but the night was dark, and he became hopelessly lost in an eerie forest along the way. Finally, he came upon a gloomy mansion on the edge of the woods. According to the map, this mansion seemed to be the one Luigi was looking for. As soon as Luigi set foot in the mansion, he started to feel nervous. Mario, who should have arrived first, was nowhere to be seen. Not only that, but there were ghosts in the mansion!\n\nSuddenly, a ghost lunged at Luigi! \"Mario! Help meee!\" That's when a strange old man with a vacuum cleaner on his back appeared out of nowhere! This strange fellow managed to rescue Luigi from the ghosts, then the two of them escaped...\n\nIt just so happened that the old man, Professor Elvin Gadd, who lived near the house, was researching his favorite subject, ghosts. Luigi told Professor E. Gadd that his brother Mario was missing, so the Professor decided to give Luigi two inventions that would help him search for his brother.\n\nLuigi's not exactly known for his bravery. Can he get rid of all the prank-loving ghosts and find Mario?",
        "keywords": [
            "ghosts",
            "3d",
            "death",
            "action-adventure",
            "darkness",
            "polygonal 3d",
            "descendants of other characters",
            "save point",
            "interconnected-world"
        ],
        "release_date": 2001
    },
    "marioland2": {
        "igdb_id": "1071",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7gxg.png",
        "artwork_url": "",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar4079.png",
        "game_name": "Super Mario Land 2",
        "igdb_name": "Super Mario Land 2: 6 Golden Coins",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Game Boy"
        ],
        "storyline": "Danger! Danger!\n\nWhile I was away crusading against the mystery alien Tatanga in Sarasa Land, an evil creep took over my castle and put the people of Mario Land under his control with a magic spell. This intruder goes by the name of Wario. He mimics my appearance, and has tried to steal my castle many times. It seems he has succeeded this time.\n\nWario has scattered the 6 Golden Coins from my castle all over Mario Land. These Golden Coins are guarded by those under Wario's spell. Without these coins, we can't get into the castle to deal with Wario. We must collect the 6 coins, attack Wario in the castle, and save everybody!\n\nIt\u2019s time to set out on our mission!!",
        "keywords": [
            "turtle"
        ],
        "release_date": 1992
    },
    "mario_kart_double_dash": {
        "igdb_id": "2344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7ndu.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3k93.png",
        "key_art_url": "",
        "game_name": "Mario Kart Double Dash",
        "igdb_name": "Mario Kart: Double Dash!!",
        "age_rating": "3",
        "rating": [
            "Mild Cartoon Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Racing",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Kids"
        ],
        "platforms": [
            "Nintendo GameCube"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2003
    },
    "megamix": {
        "igdb_id": "120278",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa4vr.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/araan.png",
        "key_art_url": "",
        "game_name": "Hatsune Miku Project Diva Mega Mix+",
        "igdb_name": "Hatsune Miku: Project Diva Mega Mix",
        "age_rating": "12",
        "rating": [
            "Blood",
            "Sexual Themes",
            "Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Side view"
        ],
        "genres": [
            "Music",
            "Arcade"
        ],
        "themes": [],
        "platforms": [
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2020
    },
    "messenger": {
        "igdb_id": "71628",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2hr9.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6u0.png",
        "key_art_url": "",
        "game_name": "The Messenger",
        "igdb_name": "The Messenger",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Language",
            "Crude Humor"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "retro",
            "2d",
            "metroidvania",
            "difficult"
        ],
        "release_date": 2018
    },
    "metroidfusion": {
        "igdb_id": "1104",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w49.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14ar.png",
        "key_art_url": "",
        "game_name": "Metroid Fusion",
        "igdb_name": "Metroid Fusion",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence",
            "Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "The game begins with Samus Aran acting as a bodyguard for the Biologic's research team on planet SR388. Eventually, a Hornoad confronts them and is killed by Samus. However, a globular yellow organism (an X) emerges from the Hornoad as it is destroyed and enters Samus's body.\nFeeling no initial effects, Samus continues escorting the researchers and completes the assignment. On the way back to the laboratory, however, Samus loses consciousness, and her gunship crashes into an asteroid belt. The ship's emergency systems automatically ejected Samus' escape pod, saving her from the crash, but her gunship is completely destroyed. Samus is quickly attended to by a medical crew, who discover that the creature that entered her body on SR388 was actually a parasitic organism that they soon named X.\n\nSamus Infected 2\nSamus, infected by the X Parasites.\nThe organic components of Samus's Power Suit had become so integrated with her system that it could not be removed while she was unconscious. Large portions of her infected suit had to be surgically removed, dramatically altering its appearance. However, the X in Samus's central nervous system were too embedded to be removed safely; Samus's chances of survival were lower than one percent.\nMetroids are the only known predator of the X; however, since Samus destroyed all the Metroids on SR388 in a previous mission, the X were able to multiply unchecked. Seeing this as the key to curing her, doctors proposed using a Metroid cell from Samus' dead Baby Metroid to make an anti-X vaccine. Apparently, the Federation had managed to preserve a cell culture from the Baby that saved Samus while she was on Zebes a second time. The serum was prepared and injected without delay, completely eradicating the X. There were, however, two side effects: Samus could no longer be hurt by normal X and could even absorb them to replenish health and ammunition, but she also inherited the Metroids' vulnerability to cold.\n\nUpon recovering, Samus is sent to investigate an explosion on the Biologic Space Laboratories research station, where the specimens from SR388 and the infected pieces of her Power Suit are being held. Once she arrives at the station, Samus immediately heads to the Quarantine Bay, where she encounters and kills a Hornoad that has been infected by an X parasite. Samus speaks with her new gunship's computer (whom she has named \"Adam\", as it reminds her of a former CO) and learns that the specimens brought back by the field team have become infected by the X. The computer also reveals that the X can use the DNA of its prey to create a perfect copy, meaning any organic life on the station may also be infected.\n\nSA-X 1\nThe SA-X.\nAs she continues to explore the station, Samus discovers that the X have used the infected portions of her Power Suit to create a copy of Samus herself, dubbed the SA-X (or Samus Aran-X). Since the SA-X arose from Samus's fully-upgraded Power Suit, it has all of her powered-up abilities, as evidenced by it using a Power Bomb to escape the Quarantine Bay. By exploding the bomb, the SA-X also destroyed the capsules holding the X specimens, releasing them all into the station. Well into her investigation of the station, Samus stumbles upon the facility's Restricted Lab. Here, she finds dozens of infant Metroids and several more Metroids in various stages of maturity, all in stasis; these were the results of a cloning project of which Samus was not previously aware. Shortly after Samus discovers them, the SA-X attempts to destroy its predators, but its plan backfires: the Metroids break free and the emergency fail-safes are activated as a result. Samus barely escapes before the lab locks down completely and is jettisoned from the station, exploding over SR388.\nAfter the incident at the Restricted Lab, Samus speaks with her ship's computer, who is angry about the discovery and subsequent destruction of the Metroids. The computer explains that the Federation had been secretly working on a Metroid breeding program, for \"peaceful applications\". The computer reveals that the station's SRX environment, a replica of the SR388 ecosystem, was ideal for raising Alpha, Gamma, Zeta, and even Omega Metroids. The research uncovered techniques for rapid growth, allowing an infant grow into an Omega Metroid in mere days. Unfortunately, the SA-X had been tracking Samus down and followed her to the lab's location. Much to Samus's surprise, the computer also mentions that the SA-X has been reproducing asexually and there are no fewer than 10 aboard the station.\n\nLater, the computer tells Samus that she has caused enough damage and instructs her to leave the rest of the investigation to the Federation. Apparently, the Federation has taken an interest in the X and SA-X and believe that this life-form has endless applications. Samus, having seen the SA-X's destructive capabilities firsthand, is strongly against this. She is convinced that the X will overwhelm the Federation troops as soon as they land, absorbing their powers and knowledge in the process. If this happens, they could easily spread throughout the galaxy and \"galactic civilization will end.\"\n\nAs an alternative, Samus decides to activate the station's self-destruct mechanism in order to destroy the X, risking her own life in the process. However, her ship's computer has locked Samus in a Navigation Room, as the Federation has ordered it to keep her confined until their arrival. Desperate, Samus yells at the computer: \"Don't let them do this. Can't you see what will happen, Adam?\" Puzzled at the use of the name, the computer inquires as to who this Adam was. Samus reveals that he had been her previous commanding officer and had died saving her life. Apparently moved by Samus's revelation, the computer agrees with the plan, and suggests that if Samus were to alter the station's orbit, then she might be able to include the planet in the explosion, thus ensuring the destruction of the X on planet SR388 as well as those on the station. At this point, Samus realizes that her ship's computer truly is Adam Malkovich, whose personality had been uploaded to a computer prior to his death.\n\nSamus hurries to the Operations Room, where she is confronted by an SA-X. She manages to defeat it, but its Core-X escapes before she can absorb it. Ignoring its escape, Samus initiates the self-destruct sequence and hurries back to her ship. However, she finds the docking bay in ruins and her ship gone. Before she can react to the situation, an Omega Metroid appears, apparently having escaped from the Restricted Lab before its destruction and grown to full size in record time. Samus possesses no weapon capable of damaging the Metroid, and a single swipe of its claw reduces her energy reserves to one unit. As the Omega Metroid prepares to finish her off, the SA-X returns, and attacks the Metroid with its Ice Beam, injuring it. However, it was greatly weakened from its fight with Samus and is quickly defeated by the Metroid. This time, the Core-X hovers over Samus, allowing her to absorb it and obtain the \"Unnamed Suit\" as well as the Ice Beam and restoring her genetic condition to its pre-vaccine state. Using her regained abilities, Samus fights and kills the Omega Metroid after a fierce struggle. After the battle, Samus's ship reenters the bay, having been piloted by the computer, Adam, and the same Etecoons and Dachoras she saved on the previous mission to Zebes and later on the Habitation Deck.\n\nAs Samus leaves the station, it is shown crashing into SR388, destroying both the station and the planet, ridding the universe of the X forever.\n\nReflecting on her actions, Samus doubts people will understand why she destroyed the X, nor will they realize the danger that was barely averted. Samus believes she will be held responsible for defying the Federation, but Adam comforts her, telling her: \"Do not worry. One of them will understand. One of them must.\" A final reflection, Samus goes on to say: \"we are all bound by our experiences. They are the limits of our consciousness. But in the end, the human soul will ever reach for the truth... This is what Adam taught me.\"",
        "keywords": [
            "aliens",
            "pirates",
            "exploration",
            "gravity",
            "metroidvania",
            "death",
            "robots",
            "spaceship",
            "female protagonist",
            "action-adventure",
            "side-scrolling",
            "backtracking",
            "time limit",
            "traps",
            "pixel art",
            "easter egg",
            "wall jump",
            "darkness",
            "explosion",
            "countdown timer",
            "alternate costumes",
            "human",
            "upgradeable weapons",
            "breaking the fourth wall",
            "save point",
            "ice stage",
            "melee",
            "underwater gameplay",
            "instant kill",
            "secret area",
            "self-referential humor",
            "rpg elements",
            "violent plants",
            "villain",
            "recurring boss",
            "speedrun",
            "plot twist",
            "completion percentage",
            "ambient music",
            "foreshadowing",
            "isolation"
        ],
        "release_date": 2002
    },
    "metroidprime": {
        "igdb_id": "1105",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w4w.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/a0lmffyqmm3wqgzdistt.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3qxy.png",
        "game_name": "Metroid Prime",
        "igdb_name": "Metroid Prime",
        "age_rating": "12",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Open world"
        ],
        "platforms": [
            "Nintendo GameCube"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "pirates",
            "ghosts",
            "exploration",
            "bloody",
            "gravity",
            "metroidvania",
            "death",
            "spaceship",
            "female protagonist",
            "action-adventure",
            "backtracking",
            "time limit",
            "multiple endings",
            "artificial intelligence",
            "snow",
            "explosion",
            "countdown timer",
            "world map",
            "polygonal 3d",
            "damsel in distress",
            "upgradeable weapons",
            "save point",
            "ice stage",
            "unstable platforms",
            "auto-aim",
            "grapple",
            "real-time combat",
            "underwater gameplay",
            "difficulty level",
            "mercenary",
            "violent plants",
            "moving platforms",
            "sequence breaking",
            "shape-shifting",
            "tentacles",
            "speedrun",
            "boss assistance",
            "fetch quests",
            "completion percentage",
            "meme origin",
            "ambient music",
            "foreshadowing",
            "isolation",
            "retroachievements"
        ],
        "release_date": 2002
    },
    "minecraft": {
        "igdb_id": "121",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa77e.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar30cw.png",
        "key_art_url": "",
        "game_name": "Minecraft",
        "igdb_name": "Minecraft: Java Edition",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person",
            "Virtual Reality"
        ],
        "genres": [
            "Simulator",
            "Adventure"
        ],
        "themes": [
            "Fantasy",
            "Survival",
            "Sandbox",
            "Kids",
            "Open world"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "Minecraft: Java Edition (previously known as Minecraft) is the original version of Minecraft, developed by Mojang Studios for Windows, macOS, and Linux. Notch began development on May 10, 2009, publicly releasing Minecraft on May 17, 2009. The full release of the game was on November 18, 2011, at MINECON 2011.",
        "keywords": [
            "3d",
            "fishing",
            "crafting",
            "death",
            "horse",
            "archery",
            "action-adventure",
            "witches",
            "bird",
            "achievements",
            "traps",
            "snow",
            "dog",
            "swimming",
            "day/night cycle",
            "darkness",
            "explosion",
            "digital distribution",
            "spider",
            "cat",
            "polygonal 3d",
            "bow and arrow",
            "loot gathering",
            "skeletons",
            "deliberately retro",
            "potion",
            "real-time combat",
            "difficulty level",
            "rpg elements",
            "sleeping",
            "meme origin",
            "poisoning",
            "fire manipulation",
            "status effects",
            "bees"
        ],
        "release_date": 2011
    },
    "mk64": {
        "igdb_id": "2342",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co67hm.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar406h.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar406i.png",
        "game_name": "Mario Kart 64",
        "igdb_name": "Mario Kart 64",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Racing",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Kids",
            "Party"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "",
        "keywords": [
            "princess",
            "artificial intelligence",
            "snow",
            "sequel",
            "bats",
            "turtle",
            "explosion",
            "anthropomorphism",
            "monkey",
            "polygonal 3d",
            "ice stage",
            "difficulty level",
            "temporary invincibility",
            "time trials",
            "retroachievements"
        ],
        "release_date": 1996
    },
    "mlss": {
        "igdb_id": "3351",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co21rg.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/knx4ne4pefgjivuylmii.png",
        "key_art_url": "",
        "game_name": "Mario & Luigi Superstar Saga",
        "igdb_name": "Mario & Luigi: Superstar Saga",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "turn-based",
            "multiple protagonists",
            "undead",
            "princess",
            "giant insects",
            "silent protagonist",
            "turtle",
            "digital distribution",
            "anthropomorphism",
            "shopping",
            "breaking the fourth wall",
            "party system",
            "save point",
            "self-referential humor",
            "rpg elements",
            "tentacles"
        ],
        "release_date": 2003
    },
    "mm2": {
        "igdb_id": "1734",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5572.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar8mv.png",
        "key_art_url": "",
        "game_name": "Mega Man 2",
        "igdb_name": "Mega Man II",
        "age_rating": "7",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Game Boy"
        ],
        "storyline": "Even after his crushing defeat at the hands of Mega Man during the events of Mega Man: Dr. Wily's Revenge, Dr. Wily was already planning his next scheme. If he could get his hands on the time machine (named Time Skimmer in the American manual) that was being developed at the Time-Space Research Laboratory (named Chronos Institute in the American manual), he thought he just might be able to change the past.\n\nAfter stealing the time machine, Wily had wanted to set out immediately on a trip across time, but had to put an emergency brake down on his plans when he discovered that the time machine had a serious flaw.\n\nMeanwhile, Dr. Light had been dispatched to the time-space laboratory to investigate. With the help of Rush\u2019s super-sense of smell, he was able to deduce that it was none other than Dr. Wily behind the theft. Having a bad feeling about the incident, Dr. Light quickly called upon Mega Man and Rush to search out Dr. Wily\u2019s whereabouts.",
        "keywords": [
            "mascot",
            "death",
            "robots",
            "flight",
            "side-scrolling",
            "pixel art",
            "sequel",
            "explosion",
            "upgradeable weapons",
            "checkpoints",
            "underwater gameplay",
            "instant kill",
            "difficulty level",
            "moving platforms",
            "villain",
            "water level",
            "monomyth"
        ],
        "release_date": 1991
    },
    "mm3": {
        "igdb_id": "1716",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co55ce.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3p52.png",
        "key_art_url": "",
        "game_name": "Mega Man 3",
        "igdb_name": "Mega Man 3",
        "age_rating": "7",
        "rating": [
            "Mild Cartoon Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Arcade",
            "Nintendo 3DS",
            "Wii",
            "Family Computer",
            "Wii U",
            "Nintendo Entertainment System"
        ],
        "storyline": "",
        "keywords": [
            "mascot",
            "death",
            "robots",
            "flight",
            "side-scrolling",
            "pixel art",
            "sequel",
            "darkness",
            "explosion",
            "checkpoints",
            "underwater gameplay",
            "moving platforms",
            "villain",
            "recurring boss",
            "monomyth"
        ],
        "release_date": 1990
    },
    "mmbn3": {
        "igdb_id": "1758",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co203k.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kmf.png",
        "key_art_url": "",
        "game_name": "MegaMan Battle Network 3",
        "igdb_name": "Mega Man Battle Network 3 Blue",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Real Time Strategy (RTS)",
            "Role-playing (RPG)",
            "Tactical"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2002
    },
    "mmx3": {
        "igdb_id": "1743",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co55pa.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2oxu.png",
        "key_art_url": "",
        "game_name": "Mega Man X3",
        "igdb_name": "Mega Man X3",
        "age_rating": "7",
        "rating": [
            "Animated Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii U",
            "New Nintendo 3DS",
            "Legacy Mobile Device",
            "Super Famicom"
        ],
        "storyline": "Zero, who had returned as an irregular hunter, became the commander of the Zero Special Forces Unit and continued to sweep up irregulars together with X, who was active as the commander of the 17th Elite Unit, and other hunters in the unit.\nAt the same time, Dr. Doppler, a scientist-type repliloid, conducted research that revealed the fact that the computer virus \"Sigma Virus\" was the cause of irregularities, developed a special antibody virus, and proposed that it be injected into repliloids. As a result, the number of irregularities decreased. Furthermore, Dr. Doppler declared that he would build \"Doppeltown,\" a peaceful city where humans and replicants could coexist, and he gained the support of both humans and replicants.\nA few months later, however, Doppler and his Repliroids, who had been exposed to the antibody virus mentioned above, rebelled. The Irregular Hunters recognized Doppler and the participants in the rebellion as irregulars, and X and Zero were ordered to go into action.",
        "keywords": [
            "death",
            "robots",
            "side-scrolling",
            "multiple protagonists",
            "multiple endings",
            "sequel",
            "wall jump",
            "explosion",
            "upgradeable weapons",
            "checkpoints",
            "underwater gameplay",
            "moving platforms",
            "retroachievements"
        ],
        "release_date": 1995
    },
    "mm_recomp": {
        "igdb_id": "1030",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3pah.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/jkiwacooqfrtotvqlxba.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p8l.png",
        "game_name": "Majora's Mask Recompiled",
        "igdb_name": "The Legend of Zelda: Majora's Mask",
        "age_rating": "12",
        "rating": [
            "Animated Violence",
            "Cartoon Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Horror",
            "Open world"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "64DD",
            "Wii U"
        ],
        "storyline": "After the events of The Legend of Zelda: Ocarina of Time, Link departs on his horse Epona in the Lost Woods and is assaulted by an imp named Skull Kid who dons a mysterious mask, accompanied by the fairies Tael and Tatl. Skull Kid turns Link into a small plant-like creature known as Deku Scrub and takes away his horse and his magical ocarina. Shortly afterward, Tatl joins Link and agrees to help him revert to his native form. A meeting with a wandering mask salesman reveals that the Skull Kid is wearing Majora's Mask, an ancient item used in hexing rituals, which calls forth a menacing moon hovering over the land of Termina. Link has exactly three days to find a way to prevent this from happening.",
        "keywords": [
            "time travel",
            "archery",
            "action-adventure",
            "fairy",
            "sequel",
            "day/night cycle",
            "sword & sorcery",
            "descendants of other characters",
            "sprinting mechanics",
            "auto-aim",
            "shape-shifting",
            "boss assistance",
            "meme origin",
            "living inventory",
            "retroachievements"
        ],
        "release_date": 2000
    },
    "momodoramoonlitfarewell": {
        "igdb_id": "188088",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7mxs.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1rhx.png",
        "key_art_url": "",
        "game_name": "Momodora Moonlit Farewell",
        "igdb_name": "Momodora: Moonlit Farewell",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Blood",
            "Suggestive Themes"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Nintendo Switch"
        ],
        "storyline": "Momodora: Moonlit Farewell presents the account of the greatest calamity to befall the village of Koho, five years after the events of Momodora III. Once the toll of an ominous bell is heard, the village is soon threatened by a demon invasion.\n\nThe village's matriarch sends Momo Reinol, their most capable priestess, to investigate the bell and find the bellringer responsible for summoning demons. It is their hope that by finding the culprit, they will also be able to secure the village's safety, and most importantly, the sacred Lun Tree's, a source of life and healing for Koho...",
        "keywords": [
            "metroidvania"
        ],
        "release_date": 2024
    },
    "monster_sanctuary": {
        "igdb_id": "89594",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1q3q.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar88x.png",
        "key_art_url": "",
        "game_name": "Monster Sanctuary",
        "igdb_name": "Monster Sanctuary",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Mild Blood",
            "Tobacco Reference"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Strategy",
            "Turn-based strategy (TBS)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "metroidvania"
        ],
        "release_date": 2020
    },
    "musedash": {
        "igdb_id": "86316",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6h43.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar5ul.png",
        "key_art_url": "",
        "game_name": "Muse Dash",
        "igdb_name": "Muse Dash",
        "age_rating": "12",
        "rating": [
            "Sexual Themes",
            "Mild Blood",
            "Mild Lyrics",
            "Fantasy Violence",
            "Suggestive Themes"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Music",
            "Indie"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "anime",
            "casual",
            "2d",
            "side-scrolling",
            "achievements",
            "cute",
            "digital distribution",
            "difficulty level"
        ],
        "release_date": 2018
    },
    "mzm": {
        "igdb_id": "1107",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1vci.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vh5.png",
        "key_art_url": "",
        "game_name": "Metroid Zero Mission",
        "igdb_name": "Metroid: Zero Mission",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Open world"
        ],
        "platforms": [
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "pirates",
            "gravity",
            "collecting",
            "metroidvania",
            "death",
            "maze",
            "spaceship",
            "female protagonist",
            "side-scrolling",
            "backtracking",
            "multiple endings",
            "pixel art",
            "wall jump",
            "explosion",
            "countdown timer",
            "upgradeable weapons",
            "save point",
            "difficulty level",
            "rpg elements",
            "sequence breaking",
            "completion percentage",
            "ambient music",
            "foreshadowing",
            "isolation",
            "interconnected-world"
        ],
        "release_date": 2004
    },
    "oot": {
        "igdb_id": "1029",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3nnx.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3p2v.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p2s.png",
        "game_name": "Ocarina of Time",
        "igdb_name": "The Legend of Zelda: Ocarina of Time",
        "age_rating": "12",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "64DD",
            "Wii U"
        ],
        "storyline": "A young boy named Link was raised in the village of the elf-like Kokiri people. One day a fairy named Navi introduces him to the village's guardian, the Great Deku Tree. It appears that a mysterious man has cursed the tree, and Link is sent to the Hyrule Castle to find out more. Princess Zelda tells Link that Ganondorf, the leader of the Gerudo tribe, seeks to obtain the Triforce, a holy relic that grants immense power to the one who possesses it. Link must do everything in his power to obtain the Triforce before Ganondorf does, and save Hyrule.",
        "keywords": [
            "gravity",
            "time travel",
            "minigames",
            "death",
            "horse",
            "archery",
            "action-adventure",
            "fairy",
            "backtracking",
            "undead",
            "campaign",
            "princess",
            "dog",
            "sequel",
            "silent protagonist",
            "swimming",
            "day/night cycle",
            "sword & sorcery",
            "digital distribution",
            "countdown timer",
            "world map",
            "polygonal 3d",
            "bow and arrow",
            "damsel in distress",
            "game reference",
            "disorientation zone",
            "descendants of other characters",
            "sprinting mechanics",
            "ice stage",
            "side quests",
            "auto-aim",
            "grapple",
            "real-time combat",
            "underwater gameplay",
            "walking through walls",
            "mercenary",
            "coming of age",
            "sequence breaking",
            "villain",
            "been here before",
            "water level",
            "plot twist",
            "boss assistance",
            "androgyny",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "damage over time",
            "retroachievements"
        ],
        "release_date": 1998
    },
    "oribf": {
        "igdb_id": "7344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1y41.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/argmx.png",
        "key_art_url": "",
        "game_name": "Ori and the Blind Forest",
        "igdb_name": "Ori and the Blind Forest",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Thriller"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Ori, the protagonist of the game, falls from the Spirit Tree and is adopted by Naru, who raises Ori as her own. When a disastrous event occurs causing the forest to wither and Naru to die, Ori is left to explore the forest. Ori eventually encounters Sein, who begins to guide Ori on an adventure to restore the forest through the recovery of the light of three main elements supporting the balance of the forest: waters, winds and warmth.",
        "keywords": [
            "metroidvania",
            "achievements",
            "wall jump",
            "digital distribution",
            "spider",
            "unstable platforms",
            "rpg elements",
            "coming of age"
        ],
        "release_date": 2015
    },
    "outer_wilds": {
        "igdb_id": "11737",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co65ac.png",
        "artwork_url": "",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3nua.png",
        "game_name": "Outer Wilds",
        "igdb_name": "Outer Wilds",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Alcohol Reference"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Puzzle",
            "Simulator",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Open world",
            "Mystery"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Welcome to the Space Program! You're the newest recruit of Outer Wilds Ventures, a fledgling space program searching for answers in a strange, constantly evolving solar system. What lurks in the heart of the ominous Dark Bramble? Who built the alien ruins on the Moon? Can the endless time loop be stopped? Answers await you in the most dangerous reaches of space.\n\nThe planets of Outer Wilds are packed with hidden locations that change with the passage of time. Visit an underground city of before it's swallowed by sand, or explore the surface of a planet as it crumbles beneath your feet. Every secret is guarded by hazardous environments and natural catastrophes.\n\nStrap on your hiking boots, check your oxygen levels, and get ready to venture into space. Use a variety of unique gadgets to probe your surroundings, track down mysterious signals, decipher ancient alien writing, and roast the perfect marshmallow.",
        "keywords": [
            "exploration",
            "time travel"
        ],
        "release_date": 2019
    },
    "overcooked2": {
        "igdb_id": "103341",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1usu.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar89w.png",
        "key_art_url": "",
        "game_name": "Overcooked! 2",
        "igdb_name": "Overcooked! 2",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Simulator",
            "Strategy",
            "Tactical",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Comedy",
            "Kids",
            "Party"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "Nintendo Switch 2",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "you can pet the dog"
        ],
        "release_date": 2018
    },
    "papermario": {
        "igdb_id": "3340",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qda.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Paper Mario",
        "igdb_name": "Paper Mario",
        "age_rating": "3",
        "rating": [
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "gravity",
            "mascot",
            "turn-based",
            "death",
            "maze",
            "undead",
            "princess",
            "easter egg",
            "silent protagonist",
            "turtle",
            "anthropomorphism",
            "leveling up",
            "human",
            "damsel in distress",
            "breaking the fourth wall",
            "party system",
            "save point",
            "melee",
            "self-referential humor",
            "moving platforms",
            "villain",
            "recurring boss",
            "sleeping",
            "tentacles",
            "temporary invincibility",
            "boss assistance",
            "poisoning",
            "invisibility",
            "fire manipulation",
            "retroachievements"
        ],
        "release_date": 2000
    },
    "placidplasticducksim": {
        "igdb_id": "204122",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4yq5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1oc8.png",
        "key_art_url": "",
        "game_name": "Placid Plastic Duck Simulator",
        "igdb_name": "Placid Plastic Duck Simulator",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Music",
            "Puzzle",
            "Simulator"
        ],
        "themes": [
            "Comedy",
            "Sandbox",
            "Kids",
            "Party"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "casual",
            "pop culture reference"
        ],
        "release_date": 2022
    },
    "pmd_eos": {
        "igdb_id": "2323",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7ovf.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kc2.png",
        "key_art_url": "",
        "game_name": "Pokemon Mystery Dungeon Explorers of Sky",
        "igdb_name": "Pok\u00e9mon Mystery Dungeon: Explorers of Sky",
        "age_rating": "3",
        "rating": [
            "Mild Cartoon Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)"
        ],
        "themes": [
            "Fantasy",
            "Kids"
        ],
        "platforms": [
            "Wii U",
            "Nintendo DS"
        ],
        "storyline": "",
        "keywords": [
            "time travel",
            "roguelike",
            "jrpg",
            "retroachievements"
        ],
        "release_date": 2009
    },
    "pokemon_crystal": {
        "igdb_id": "1514",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pil.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1ox6.png",
        "key_art_url": "",
        "game_name": "Pokemon Crystal",
        "igdb_name": "Pok\u00e9mon Crystal Version",
        "age_rating": "12",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Kids"
        ],
        "platforms": [
            "Game Boy Color",
            "Nintendo 3DS"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "anime",
            "collecting",
            "minigames",
            "turn-based",
            "teleportation",
            "bats",
            "day/night cycle",
            "leveling up",
            "world map",
            "shopping",
            "party system",
            "sprinting mechanics",
            "side quests",
            "potion",
            "melee",
            "coming of age",
            "punctuation mark above head",
            "been here before",
            "sleeping",
            "tentacles",
            "poisoning",
            "fire manipulation",
            "status effects",
            "damage over time"
        ],
        "release_date": 2000
    },
    "pokemon_emerald": {
        "igdb_id": "1517",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1zhr.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar21y7.png",
        "key_art_url": "",
        "game_name": "Pokemon Emerald",
        "igdb_name": "Pok\u00e9mon Emerald Version",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Kids"
        ],
        "platforms": [
            "Game Boy Advance"
        ],
        "storyline": "Both Team Magma and Team Aqua are featured as the villainous teams, each stirring trouble at different stages in the game. The objective of each team, to awaken Groudon and Kyogre, respectively, is eventually fulfilled.\nRayquaza is prominent plot-wise, awakened in order to stop the destructive battle between Groudon and Kyogre. It is now the one out of the three ancient Pok\u00e9mon that can be caught prior to the Elite Four challenge, while still at the same place and at the same high level as in Ruby and Sapphire.",
        "keywords": [
            "exploration",
            "anime",
            "collecting",
            "minigames",
            "turn-based",
            "bird",
            "teleportation",
            "giant insects",
            "silent protagonist",
            "leveling up",
            "shopping",
            "party system",
            "sprinting mechanics",
            "side quests",
            "potion",
            "melee",
            "coming of age",
            "punctuation mark above head",
            "recurring boss",
            "tentacles",
            "poisoning",
            "fire manipulation",
            "fast traveling",
            "status effects",
            "damage over time"
        ],
        "release_date": 2004
    },
    "pokemon_frlg": {
        "igdb_id": "1516",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1zip.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Pokemon FireRed and LeafGreen",
        "igdb_name": "Pok\u00e9mon LeafGreen Version",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction",
            "Kids"
        ],
        "platforms": [
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [
            "collecting"
        ],
        "release_date": 2004
    },
    "pokemon_rb": {
        "igdb_id": "1561",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pi4.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1krw.png",
        "key_art_url": "",
        "game_name": "Pokemon Red and Blue",
        "igdb_name": "Pok\u00e9mon Red Version",
        "age_rating": "12",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Kids",
            "Open world"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Game Boy"
        ],
        "storyline": "The player character starts out in Pallet Town. When the player character tries to leave the town without a Pok\u00e9mon of their own, they are stopped in the nick of time by Professor Oak, who invites them to his lab. There, he gives them a Pok\u00e9mon of their own and a Pok\u00e9dex, telling them about his dream to make a complete guide on every Pok\u00e9mon in the world. After the player character battles their rival and leaves the lab, they are entitled to win every Gym Badge, compete in the Pok\u00e9mon League, and fulfill Oak's dream by catching every Pok\u00e9mon.",
        "keywords": [
            "collecting"
        ],
        "release_date": 1996
    },
    "powerwashsimulator": {
        "igdb_id": "138590",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7gek.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ardhg.png",
        "key_art_url": "",
        "game_name": "Powerwash Simulator",
        "igdb_name": "PowerWash Simulator",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Simulator",
            "Indie"
        ],
        "themes": [
            "Business",
            "Sandbox"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "You're looking to start a business \u2013 but what? You decide power washing is super satisfying and you'd like to turn it into a full time gig. You put your good friend Harper Shaw, a bargain hunter and auction lot buyer up to the task of finding you the perfect vehicle for your new enterprise.\n\nThrough completing various jobs, you get to know the citizens of Muckingham, the small town in which the game is set, helping wash away their various problems. Figuratively... and literally!\n\nThe first client you are introduced to is Cal, Harper Shaw's new disgruntled neighbour. They are a volcanologist, who\u2019s moved back into town to study Mount Rushless, the local volcano, and to help look after his ageing parents. He's so worked up as he bought a house without even looking at a picture of the back garden. He thinks the previous owners might have even owned rhinos it's that dirty...",
        "keywords": [
            "3d",
            "funny",
            "atmospheric",
            "relaxing",
            "story rich"
        ],
        "release_date": 2022
    },
    "rac2": {
        "igdb_id": "1770",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co230n.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Ratchet & Clank 2",
        "igdb_name": "Ratchet & Clank: Going Commando",
        "age_rating": "7",
        "rating": [
            "Animated Blood",
            "Comic Mischief",
            "Fantasy Violence",
            "Mild Language"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 2"
        ],
        "storyline": "Having defeated Chairman Drek in their last intergalactic adventure, Ratchet and Clank find themselves returning to a more sedate lifestyle. That is, until they are approached by Abercrombie Fizzwidget, the CRO of Megacorp, who needs the duo to track down the company\u2019s most promising experimental project, which has been stolen by a mysterious masked figure. Initially, the mission seemed like a Sunday stroll in the park, but we soon find our heroes entangled in a colossal struggle for control of the galaxy. Along the way, the duo unleashes some of the coolest weapons and gadgets ever invented upon the most dangerous foes they have ever faced. Ratchet and Clanks set out to destroy anything and anyone who stands in their way of discovering the secrets that lie behind \u201cThe Experiment.\u201d",
        "keywords": [],
        "release_date": 2003
    },
    "raft": {
        "igdb_id": "27082",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1xdc.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ardgp.png",
        "key_art_url": "",
        "game_name": "Raft",
        "igdb_name": "Raft",
        "age_rating": "12",
        "rating": [
            "Violence",
            "Blood"
        ],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Simulator",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Survival"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5"
        ],
        "storyline": "Trapped on a small raft with nothing but a hook made of old plastic, players awake on a vast, blue ocean totally alone and with no land in sight! With a dry throat and an empty stomach, survival will not be easy!\n\nResources are tough to come by at sea: Players will have to make sure to catch whatever debris floats by using their trusty hook and when possible, scavenge the reefs beneath the waves and the islands above. However, thirst and hunger is not the only danger in the ocean\u2026 watch out for the man-eating shark determined to end your voyage!",
        "keywords": [
            "crafting",
            "bees"
        ],
        "release_date": 2022
    },
    "rogue_legacy": {
        "igdb_id": "3221",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co27fi.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ard4c.png",
        "key_art_url": "",
        "game_name": "Rogue Legacy",
        "igdb_name": "Rogue Legacy",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Crude Humor"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 3",
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "PlayStation Vita",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "exploration",
            "medieval",
            "magic",
            "minigames",
            "roguelike",
            "metroidvania",
            "death",
            "horse",
            "female protagonist",
            "flight",
            "action-adventure",
            "side-scrolling",
            "multiple protagonists",
            "bird",
            "time limit",
            "traps",
            "pixel art",
            "easter egg",
            "teleportation",
            "darkness",
            "explosion",
            "digital distribution",
            "countdown timer",
            "bow and arrow",
            "breaking the fourth wall",
            "pop culture reference",
            "game reference",
            "descendants of other characters",
            "potion",
            "stat tracking",
            "secret area",
            "shielded enemies",
            "violent plants",
            "punctuation mark above head",
            "temporary invincibility",
            "boss assistance",
            "fire manipulation",
            "lgbtq+"
        ],
        "release_date": 2013
    },
    "ror1": {
        "igdb_id": "3173",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2k2z.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ard5n.png",
        "key_art_url": "",
        "game_name": "Risk of Rain",
        "igdb_name": "Risk of Rain",
        "age_rating": "7",
        "rating": [
            "Alcohol Reference",
            "Fantasy Violence",
            "Mild Blood",
            "Mild Language"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Role-playing (RPG)",
            "Hack and slash/Beat 'em up",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction",
            "Survival"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "PlayStation Vita",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "roguelike",
            "difficult",
            "time limit",
            "pixel art",
            "bow and arrow",
            "roguelite"
        ],
        "release_date": 2013
    },
    "ror2": {
        "igdb_id": "28512",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaavb.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar758.png",
        "key_art_url": "",
        "game_name": "Risk of Rain 2",
        "igdb_name": "Risk of Rain 2",
        "age_rating": "12",
        "rating": [
            "Blood",
            "Drug Reference",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Shooter",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Survival"
        ],
        "platforms": [
            "Google Stadia",
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Risk of Rain 2 follows the crew of UES: Safe Travels as they try to find UES: Contact Light and any survivors along their path. They have to try and survive the hostile wildlife and environment as difficulty increases over time, navigating Petrichor V via the teleporters strewn across the entire planet. The crew loop endlessly through many distinct environments, but end upon the moon to defeat the final boss.\n\nWith each run, you\u2019ll learn the patterns of your foes, and even the longest odds can be overcome with enough skill. A unique scaling system means both you and your foes limitlessly increase in power over the course of a game\u2013what once was a bossfight will in time become a common enemy.\n\nMyriad survivors, items, enemies, and bosses return to Risk 2, and many new ones are joining the fight. Brand new survivors like the Artificer and MUL-T debut alongside classic survivors such as the Engineer, Huntress, and\u2013of course\u2013the Commando. With over 75 items to unlock and exploit, each run will keep you cleverly strategizing your way out of sticky situations.",
        "keywords": [
            "roguelite"
        ],
        "release_date": 2020
    },
    "sa2b": {
        "igdb_id": "192194",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5p3o.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1h09.png",
        "key_art_url": "",
        "game_name": "Sonic Adventure 2 Battle",
        "igdb_name": "Sonic Adventure 2: Battle",
        "age_rating": "E",
        "rating": [
            "Mild Lyrics",
            "Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "PlayStation 3",
            "PC (Microsoft Windows)",
            "Xbox 360"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2012
    },
    "sadx": {
        "igdb_id": "192114",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4iln.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1nly.png",
        "key_art_url": "",
        "game_name": "Sonic Adventure DX",
        "igdb_name": "Sonic Adventure: Sonic Adventure DX Upgrade",
        "age_rating": "E",
        "rating": [
            "Animated Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "PlayStation 3",
            "PC (Microsoft Windows)",
            "Xbox 360"
        ],
        "storyline": "Doctor Robotnik seeks a new way to defeat his longtime nemesis Sonic and conquer the world. During his research, he learns about an entity called Chaos\u2014a creature that, thousands of years ago, helped to protect the Chao and the all-powerful Master Emerald, which balances the power of the seven Chaos Emeralds. When a tribe of echidnas sought to steal the power of the Emeralds, breaking the harmony they had with the Chao, Chaos retaliated by using the Emeralds' power to transform into a monstrous beast, Perfect Chaos, and wipe them out. Before it could destroy the world, Tikal, a young echidna who befriended Chaos, imprisoned it in the Master Emerald along with herself. Eggman releases Chaos and Sonic and his friends must act against Eggman's plans and prevent the monster from becoming more powerful.",
        "keywords": [],
        "release_date": 2010
    },
    "satisfactory": {
        "igdb_id": "90558",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8tfy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar57j.png",
        "key_art_url": "",
        "game_name": "Satisfactory",
        "igdb_name": "Satisfactory",
        "age_rating": "3",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Simulator",
            "Strategy",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Science fiction",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5"
        ],
        "storyline": "",
        "keywords": [
            "crafting"
        ],
        "release_date": 2024
    },
    "seaofthieves": {
        "igdb_id": "11137",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2558.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6pg.png",
        "key_art_url": "",
        "game_name": "Sea of Thieves",
        "igdb_name": "Sea of Thieves",
        "age_rating": "12",
        "rating": [
            "Crude Humor",
            "Use of Alcohol",
            "Violence"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Simulator",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One"
        ],
        "storyline": "",
        "keywords": [
            "pirates",
            "exploration",
            "crafting",
            "action-adventure",
            "digital distribution",
            "skeletons",
            "you can pet the dog"
        ],
        "release_date": 2018
    },
    "shivers": {
        "igdb_id": "12477",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7a5z.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/aruss.png",
        "key_art_url": "",
        "game_name": "Shivers",
        "igdb_name": "Shivers",
        "age_rating": "7",
        "rating": [
            "Realistic Blood and Gore",
            "Realistic Blood"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Point-and-click",
            "Puzzle",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Horror"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 1995
    },
    "shorthike": {
        "igdb_id": "116753",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6e83.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arcrm.png",
        "key_art_url": "",
        "game_name": "A Short Hike",
        "igdb_name": "A Short Hike",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "The main character is Claire, a young anthropomorphic bird who travels to Hawk Peak Provincial Park, where her Aunt May works as a ranger, to spend days off. However, Claire cannot get cellphone reception unless she reaches the top of the peak, and is expecting an important call. For this reason, she decides to reach the highest point in the park.",
        "keywords": [
            "exploration",
            "casual",
            "3d",
            "fishing",
            "female protagonist",
            "flight",
            "stylized",
            "bird",
            "achievements",
            "time limit",
            "cute",
            "funny",
            "atmospheric",
            "snow",
            "relaxing",
            "3d platformer",
            "climbing",
            "great soundtrack",
            "anthropomorphism",
            "gliding",
            "controller support"
        ],
        "release_date": 2019
    },
    "sims4": {
        "igdb_id": "3212",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3h3l.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ary47.png",
        "key_art_url": "",
        "game_name": "The Sims 4",
        "igdb_name": "The Sims 4",
        "age_rating": "12",
        "rating": [
            "Sexual Themes",
            "Crude Humor",
            "Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Simulator"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Comedy",
            "Sandbox",
            "Romance"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One"
        ],
        "storyline": "Choose how Sims look, act, and dress. Determine how they\u2019ll live out each day. Design and build incredible homes for every family, then decorate with your favorite furnishings and d\u00e9cor. Travel to different neighborhoods where you can meet other Sims and learn about their lives. Discover beautiful locations with distinctive environments, and go on spontaneous adventures. Manage the ups and downs of Sims\u2019 everyday lives and see what happens when you play out realistic or fantastical scenarios. Tell your stories your way while developing relationships, pursuing careers and life aspirations, and immersing yourself in an extraordinary game where the possibilities are endless.",
        "keywords": [
            "casual",
            "cute",
            "funny",
            "relaxing",
            "lgbtq+",
            "you can pet the dog"
        ],
        "release_date": 2014
    },
    "sly1": {
        "igdb_id": "1798",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1p0r.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Sly Cooper and the Thievius Raccoonus",
        "igdb_name": "Sly Cooper and the Thievius Raccoonus",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Stealth",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 2"
        ],
        "storyline": "Sly Cooper comes from a long line of master thieves (the Cooper Clan) who only steal from other criminals, thus making them vigilantes. The Cooper family's heirloom, an ancient book by the name The Thievius Raccoonus, records all the secret moves and techniques from every member in the clan. On his 8th birthday, Sly was supposed to inherit the book and learn all of his family's ancient secrets which was supposed to help him become a master thief, however, a group of thugs by the name \"The Fiendish Five\" (led by Clockwerk, who is the arch-nemesis of the family clan) attack the Cooper household and kills Sly's parents and stole all of the pages from the Thievius Raccoonus. After that, the ruthless gang go their separate ways to commit dastardly crimes around the world. Sly is sent to an orphanage where he meets and teams up and forms a gang with two guys who become his lifelong best friends, Bentley, a technician, inventor and a talented mathematical hacker with encyclopedic knowledge who plays the role as the brains of the gang, and Murray, a huge husky cowardly guy with a ginormous appetite who plays the role as the brawns and the getaway driver of the gang. The three leave the orphanage together at age 16 to start their lives becoming international vigilante criminals together, naming themselves \"The Cooper Gang\". Sly swears one day to avenge his family and track down the Fiendish Five and steal back the Thievius Raccoonus. Two years later, the Cooper Gang head to Paris, France, to infiltrate Itnerpol (a police headquarters) in order to find the secret police file which stores details and information about the Fiendish Five but during the heist they are ambushed by Inspector Carmelita Fox (towards whom Sly develops a romantic attraction), a police officer who is affiliated with Interpol and is after the Cooper Gang. The gang manage to steal the police file and successfully escapes from her and the rest of the cops. With the secret police file finally in their hands, the Cooper Gang manage to track down the Fiendish Five.",
        "keywords": [
            "ghosts",
            "mascot",
            "death",
            "artificial intelligence",
            "dog",
            "talking animals",
            "climbing",
            "turtle",
            "anthropomorphism",
            "spider",
            "voice acting",
            "polygonal 3d",
            "skeletons",
            "descendants of other characters",
            "checkpoints",
            "unstable platforms",
            "melee",
            "moving platforms",
            "gliding",
            "invisibility",
            "time trials"
        ],
        "release_date": 2002
    },
    "sm": {
        "igdb_id": "1103",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5osy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14az.png",
        "key_art_url": "",
        "game_name": "Super Metroid",
        "igdb_name": "Super Metroid",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Thriller"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "After Samus completed her mission and eradicated the entire Metroid population on SR388 as commanded by the Galactic Federation (sans the Metroid Hatchling, which she nicknamed \"Baby\"), she brought the Hatchling to the Ceres Space Colony for research. However, shortly after she left, she received a distress signal from the Station and returned to investigate.\n\nWhen Samus arrives at the Space Science Academy where the Baby was being studied, she finds all the scientists slaughtered and the containment unit that held the Baby missing. Upon further exploration of the Station, she finds the Baby in a small capsule. As she approaches, Ridley appears and grabs the capsule. After a brief battle, Samus repels Ridley, and he activates a self-destruct sequence to destroy Ceres.\n\nAfter escaping the explosion, Ridley flees to Zebes, and Samus goes after him.",
        "keywords": [
            "aliens",
            "exploration",
            "2d",
            "metroidvania",
            "female protagonist",
            "action-adventure",
            "side-scrolling",
            "time limit",
            "pixel art",
            "wall jump",
            "darkness",
            "explosion",
            "countdown timer",
            "nintendo power",
            "damsel in distress",
            "save point",
            "unstable platforms",
            "real-time combat",
            "secret area",
            "mercenary",
            "sequence breaking",
            "isolation",
            "interconnected-world"
        ],
        "release_date": 1994
    },
    "sm64ex": {
        "igdb_id": "1074",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co721v.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14k6.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3na7.png",
        "game_name": "Super Mario 64",
        "igdb_name": "Super Mario 64",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "\u201cMario, please come to the castle. I've baked a cake for you. Yours truly, Princess Toadstool.\u201d\n\n\u201cWow, an invitation from Peach! I'll head out right away. I hope she can wait for me!\u201d\n\nMario is so excited to receive the invitation from the princess, who lives in the Mushroom Castle that he quickly dresses in his best and leaves right away.\n\n\u201cHmmm, something's not quite right here... It's so quiet...\u201d\n\nShaking off his uneasy premonition, Mario steps into the silent castle, where he is greeted by the gruff words, \u201cNo one's home! Now scram! Bwa, ha, ha.\u201d\n\nThe sound seems to come from everywhere.\n\n\u201cWho's there?! I've heard that voice somewhere before...\u201d\n\nMario begins searching all over the castle. Most of the doors are locked, but finding one open, he peeks inside. Hanging on the wall is the largest painting he has ever seen, and from behind the painting comes the strangest sound that he has ever heard...\n\n\u201cI think I hear someone calling. What secrets does this painting hold?\u201d\n\nWithout a second thought, Mario jumps at the painting. As he is drawn into it, another world opens before his very eyes.\n\nOnce inside the painting, Mario finds himself in the midst of battling Bob-ombs. According to the Bob-omb Buddies, someone...or something...has suddenly attacked the castle and stolen the \u201cPower Stars.\u201d These stars protect the castle. With the stars in his control, the beast plans to take over the Mushroom Castle.\n\nTo help him accomplish this, he plans to convert the residents of the painting world into monsters as well. If nothing is done, all those monsters will soon begin to overflow from inside the painting.\n\n\u201cA plan this maniacal, this cunning...this must be the work of Bowser!\u201d\n\nPrincess Toadstool and Toad are missing, too. Bowser must have taken them and sealed them inside the painting. Unless Mario recovers the Power Stars immediately, the inhabitants of this world will become Bowser's army.\n\n\u201cWell, Bowser's not going to get away with it, not as long as I'm around!\u201d\n\nStolen Power Stars are hidden throughout the painting world. Use your wisdom and strength to recover the Power Stars and restore peace to the Mushroom Castle.\n\n\u201cMario! You are the only one we can count on.\u201d",
        "keywords": [
            "rabbit",
            "3d platformer",
            "swimming",
            "digital distribution",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "retroachievements"
        ],
        "release_date": 1996
    },
    "sm64hacks": {
        "igdb_id": "1074",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co721v.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14k6.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3na7.png",
        "game_name": "SM64 Romhack",
        "igdb_name": "Super Mario 64",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "\u201cMario, please come to the castle. I've baked a cake for you. Yours truly, Princess Toadstool.\u201d\n\n\u201cWow, an invitation from Peach! I'll head out right away. I hope she can wait for me!\u201d\n\nMario is so excited to receive the invitation from the princess, who lives in the Mushroom Castle that he quickly dresses in his best and leaves right away.\n\n\u201cHmmm, something's not quite right here... It's so quiet...\u201d\n\nShaking off his uneasy premonition, Mario steps into the silent castle, where he is greeted by the gruff words, \u201cNo one's home! Now scram! Bwa, ha, ha.\u201d\n\nThe sound seems to come from everywhere.\n\n\u201cWho's there?! I've heard that voice somewhere before...\u201d\n\nMario begins searching all over the castle. Most of the doors are locked, but finding one open, he peeks inside. Hanging on the wall is the largest painting he has ever seen, and from behind the painting comes the strangest sound that he has ever heard...\n\n\u201cI think I hear someone calling. What secrets does this painting hold?\u201d\n\nWithout a second thought, Mario jumps at the painting. As he is drawn into it, another world opens before his very eyes.\n\nOnce inside the painting, Mario finds himself in the midst of battling Bob-ombs. According to the Bob-omb Buddies, someone...or something...has suddenly attacked the castle and stolen the \u201cPower Stars.\u201d These stars protect the castle. With the stars in his control, the beast plans to take over the Mushroom Castle.\n\nTo help him accomplish this, he plans to convert the residents of the painting world into monsters as well. If nothing is done, all those monsters will soon begin to overflow from inside the painting.\n\n\u201cA plan this maniacal, this cunning...this must be the work of Bowser!\u201d\n\nPrincess Toadstool and Toad are missing, too. Bowser must have taken them and sealed them inside the painting. Unless Mario recovers the Power Stars immediately, the inhabitants of this world will become Bowser's army.\n\n\u201cWell, Bowser's not going to get away with it, not as long as I'm around!\u201d\n\nStolen Power Stars are hidden throughout the painting world. Use your wisdom and strength to recover the Power Stars and restore peace to the Mushroom Castle.\n\n\u201cMario! You are the only one we can count on.\u201d",
        "keywords": [
            "rabbit",
            "3d platformer",
            "swimming",
            "digital distribution",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "retroachievements"
        ],
        "release_date": 1996
    },
    "smo": {
        "igdb_id": "26758",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mxf.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/lymumhy07tlqyprs0zrn.png",
        "key_art_url": "",
        "game_name": "Super Mario Odyssey",
        "igdb_name": "Super Mario Odyssey",
        "age_rating": "7",
        "rating": [
            "Cartoon Violence",
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Nintendo Switch 2",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "dinosaurs",
            "3d",
            "rabbit",
            "dog",
            "sequel",
            "wall jump",
            "3d platformer",
            "swimming",
            "alternate costumes",
            "deliberately retro",
            "checkpoints",
            "underwater gameplay",
            "behind the waterfall"
        ],
        "release_date": 2017
    },
    "sms": {
        "igdb_id": "1075",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co21rh.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14lj.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3nb8.png",
        "game_name": "Super Mario Sunshine",
        "igdb_name": "Super Mario Sunshine",
        "age_rating": "3",
        "rating": [
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Sandbox"
        ],
        "platforms": [
            "Nintendo GameCube"
        ],
        "storyline": "Close your eyes and imagine\u2026soothing sunshine accompanied by the sound of waves gently breaking on the shore. High above, seagulls turn lazy circles in a clear blue sky. This is Isle Delfino.\n\nFar from the hustle and bustle of the Mushroom Kingdom, this island resort glitters like a gem in the waters of a southern sea.\n\nMario, Peach, and an entourage of Toads have come to Isle Delfino to relax and unwind. At least, that\u2019s their plan\u2026but when they arrive, they find things have gone horribly wrong...\n\nAccording to the island inhabitants, the person responsible for the mess has a round nose, a thick mustache, and a cap\u2026\n\nWhat? But\u2026that sounds like Mario!!\n\nThe islanders are saying that Mario's mess has polluted the island and caused their energy source, the Shine Sprites, to vanish.\n\nNow the falsely accused Mario has promised to clean up the island, but...how?\n\nNever fear! FLUDD, the latest invention from Gadd Science, Inc., can help Mario tidy up the island, take on baddies, and lend a nozzle in all kinds of sticky situations.\n\nCan Mario clean the island, capture the villain, and clear his good name? It\u2019s time for another Mario adventure to get started!",
        "keywords": [
            "ghosts",
            "dinosaurs",
            "3d",
            "death",
            "robots",
            "action-adventure",
            "time limit",
            "sequel",
            "giant insects",
            "wall jump",
            "3d platformer",
            "climbing",
            "swimming",
            "turtle",
            "explosion",
            "anthropomorphism",
            "alternate costumes",
            "voice acting",
            "human",
            "polygonal 3d",
            "damsel in distress",
            "descendants of other characters",
            "sprinting mechanics",
            "unstable platforms",
            "real-time combat",
            "underwater gameplay",
            "violent plants",
            "moving platforms",
            "been here before",
            "water level",
            "sleeping",
            "tentacles",
            "boss assistance",
            "gliding",
            "foreshadowing",
            "retroachievements"
        ],
        "release_date": 2002
    },
    "smw": {
        "igdb_id": "1070",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8lo8.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1ge5.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3nae.png",
        "game_name": "Super Mario World",
        "igdb_name": "Super Mario World",
        "age_rating": "7",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Arcade",
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "Mario is having a vacation in Dinosaur Land when he learns that Princess Peach Toadstool has been kidnapped by the evil King Koopa Bowser. When Mario starts searching for her he finds a giant egg with a dinosaur named Yoshi hatching out of it. Yoshi tells Mario that his fellow dinosaurs have been imprisoned in eggs by Bowser's underlings. The intrepid plumber has to travel to their castles, rescue the dinosaurs, and eventually face King Koopa himself, forcing him to release the princess.",
        "keywords": [
            "dinosaurs",
            "princess",
            "digital distribution",
            "bonus stage",
            "damsel in distress",
            "retroachievements"
        ],
        "release_date": 1990
    },
    "sm_map_rando": {
        "igdb_id": "1103",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5osy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14az.png",
        "key_art_url": "",
        "game_name": "Super Metroid Map Rando",
        "igdb_name": "Super Metroid",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Thriller"
        ],
        "platforms": [
            "Super Nintendo Entertainment System",
            "Wii",
            "Wii U",
            "New Nintendo 3DS",
            "Super Famicom"
        ],
        "storyline": "After Samus completed her mission and eradicated the entire Metroid population on SR388 as commanded by the Galactic Federation (sans the Metroid Hatchling, which she nicknamed \"Baby\"), she brought the Hatchling to the Ceres Space Colony for research. However, shortly after she left, she received a distress signal from the Station and returned to investigate.\n\nWhen Samus arrives at the Space Science Academy where the Baby was being studied, she finds all the scientists slaughtered and the containment unit that held the Baby missing. Upon further exploration of the Station, she finds the Baby in a small capsule. As she approaches, Ridley appears and grabs the capsule. After a brief battle, Samus repels Ridley, and he activates a self-destruct sequence to destroy Ceres.\n\nAfter escaping the explosion, Ridley flees to Zebes, and Samus goes after him.",
        "keywords": [
            "aliens",
            "exploration",
            "2d",
            "metroidvania",
            "female protagonist",
            "action-adventure",
            "side-scrolling",
            "time limit",
            "pixel art",
            "wall jump",
            "darkness",
            "explosion",
            "countdown timer",
            "nintendo power",
            "damsel in distress",
            "save point",
            "unstable platforms",
            "real-time combat",
            "secret area",
            "mercenary",
            "sequence breaking",
            "isolation",
            "interconnected-world"
        ],
        "release_date": 1994
    },
    "soe": {
        "igdb_id": "1359",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8kz6.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Secret of Evermore",
        "igdb_name": "Secret of Evermore",
        "age_rating": "E",
        "rating": [
            "Mild Animated Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Historical"
        ],
        "platforms": [
            "Super Nintendo Entertainment System"
        ],
        "storyline": "In Dr. Sidney Ruffleberg's old, decaying mansion, a boy and his dog stumble upon a mysterious machine. By sheer accident they are propelled into Evermore, a one-time utopia that now has become a confounding and deadly world. A world of prehistoric jungles, ancient civilizations, medieval kingdoms and futuristic cities. During his odyssey, the boy must master a variety of weapons, learn to harness the forces of alchemy, and make powerful allies to battle Evermore's diabolical monsters. What's more, his dog masters shape-changing to aid the quest. But even if they can muster enough skill and courage, even if they can uncover the mysterious clues, they can only find their way home by discovering the Secret of Evermore.",
        "keywords": [
            "medieval",
            "dog",
            "giant insects",
            "sprinting mechanics",
            "ambient music"
        ],
        "release_date": 1995
    },
    "sonic_heroes": {
        "igdb_id": "4156",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9olx.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Sonic Heroes",
        "igdb_name": "Sonic Heroes",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Xbox",
            "PlayStation 3",
            "Nintendo GameCube",
            "PC (Microsoft Windows)",
            "PlayStation 2"
        ],
        "storyline": "Dr. Eggman has come back to challenge Sonic and crew again to defeat his new scheme. Sonic the Hedgehog, Miles \"Tails\" Prower, and Knuckles the Echidna gladly accept and race off to tackle the doctor's latest plan. Meanwhile, Rouge the Bat swings in on one of Eggman's old fortresses and discovers Shadow the Hedgehog encapsuled. After an odd encounter, Rouge, Shadow, and E-123 Omega join up to find out what happened to Shadow and to get revenge on Eggman.\nAt a resort, Amy Rose looks at an ad that shows Sonic in it with Chocola and Froggy, Cheese's and Big's best friends respectively. After getting over boredom, Amy, Cream the Rabbit, and Big the Cat decide to find Sonic and get what they want back. Elsewhere, in a run down building, the Chaotix Detective Agency receive a package that contains a walkie-talkie. Tempting them, Vector the Crocodile, Espio the Chameleon and Charmy Bee decide to work for this mysterious person, so they can earn some money.",
        "keywords": [
            "3d",
            "robots",
            "rabbit",
            "multiple protagonists",
            "achievements",
            "amnesia",
            "3d platformer",
            "explosion",
            "anthropomorphism",
            "bonus stage",
            "voice acting",
            "checkpoints",
            "rock music",
            "moving platforms",
            "temporary invincibility",
            "retroachievements"
        ],
        "release_date": 2003
    },
    "sotn": {
        "igdb_id": "1128",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co53m8.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1nj6.png",
        "key_art_url": "",
        "game_name": "Symphony of the Night",
        "igdb_name": "Castlevania: Symphony of the Night",
        "age_rating": "12",
        "rating": [
            "Animated Blood and Gore",
            "Animated Violence",
            "Violence",
            "Blood and Gore",
            "Cartoon Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror",
            "Open world"
        ],
        "platforms": [
            "PlayStation 3",
            "PlayStation",
            "PlayStation Portable",
            "Xbox 360"
        ],
        "storyline": "The game's story takes place during the year 1797, 5 years after the events of Rondo of Blood and begins with Richter Belmont's defeat of Count Dracula, mirroring the end of the former game. However, despite Dracula being defeated, Richter vanishes without a trace. Castlevania rises again five years later, and while there are no Belmonts to storm the castle, Alucard, the son of Dracula, awakens from his self-induced sleep, and decides to investigate what transpired during his slumber.\n\nMeanwhile, Maria Renard, Richter's sister-in-law, enters Castlevania herself to search for the missing Richter. She assists Alucard multiple times throughout the game.",
        "keywords": [
            "ghosts",
            "bloody",
            "gravity",
            "magic",
            "2d",
            "metroidvania",
            "death",
            "horse",
            "action-adventure",
            "side-scrolling",
            "multiple protagonists",
            "backtracking",
            "achievements",
            "multiple endings",
            "undead",
            "pixel art",
            "bats",
            "day/night cycle",
            "explosion",
            "digital distribution",
            "leveling up",
            "human",
            "polygonal 3d",
            "shopping",
            "skeletons",
            "descendants of other characters",
            "save point",
            "melee",
            "real-time combat",
            "secret area",
            "rock music",
            "rpg elements",
            "moving platforms",
            "sequence breaking",
            "villain",
            "shape-shifting",
            "speedrun",
            "completion percentage",
            "meme origin",
            "androgyny",
            "behind the waterfall",
            "isolation",
            "interconnected-world"
        ],
        "release_date": 1997
    },
    "spyro3": {
        "igdb_id": "1578",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7t4m.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Spyro 3",
        "igdb_name": "Spyro: Year of the Dragon",
        "age_rating": "7",
        "rating": [
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Comedy"
        ],
        "platforms": [
            "PlayStation 3",
            "PlayStation",
            "PlayStation Portable"
        ],
        "storyline": "The game follows the titular purple dragon Spyro as he travels to the Forgotten Worlds after 150 magical dragon eggs are stolen from the land of the dragons by an evil sorceress.",
        "keywords": [
            "minigames",
            "mascot",
            "flight",
            "multiple protagonists",
            "swimming",
            "sword & sorcery",
            "anthropomorphism",
            "bonus stage",
            "polygonal 3d",
            "game reference",
            "real-time combat",
            "moving platforms",
            "gliding",
            "time trials"
        ],
        "release_date": 2000
    },
    "ss": {
        "igdb_id": "534",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5wrj.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/o7kzk0l7wrtw3gfv4dgb.png",
        "key_art_url": "",
        "game_name": "Skyward Sword",
        "igdb_name": "The Legend of Zelda: Skyward Sword",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Animated Blood",
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Historical",
            "Open world"
        ],
        "platforms": [
            "Wii",
            "Wii U"
        ],
        "storyline": "Born on an island suspended in the sky, a young man called Link accepts his destiny to venture to the world below to save his childhood friend Zelda after being kidnapped and brought to an abandoned land.",
        "keywords": [
            "medieval",
            "archery",
            "action-adventure",
            "campaign",
            "princess",
            "silent protagonist",
            "day/night cycle",
            "sword & sorcery",
            "human",
            "polygonal 3d",
            "bow and arrow",
            "damsel in distress",
            "potion",
            "auto-aim",
            "real-time combat",
            "mercenary",
            "violent plants",
            "androgyny",
            "context sensitive",
            "living inventory",
            "behind the waterfall",
            "monomyth"
        ],
        "release_date": 2011
    },
    "stardew_valley": {
        "igdb_id": "17000",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa93h.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar5l8.png",
        "key_art_url": "",
        "game_name": "Stardew Valley",
        "igdb_name": "Stardew Valley",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Mild Blood",
            "Mild Language",
            "Simulated Gambling",
            "Use of Tobacco",
            "Use of Alcohol",
            "Use of Alcohol and Tobacco"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Simulator",
            "Strategy",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Business",
            "Sandbox",
            "Romance"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "Nintendo Switch 2",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Wii U",
            "PlayStation Vita",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "You\u2019ve inherited your grandfather\u2019s old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home? It won\u2019t be easy. Ever since Joja Corporation came to town, the old ways of life have all but disappeared. The community center, once the town\u2019s most vibrant hub of activity, now lies in shambles. But the valley seems full of opportunity. With a little dedication, you might just be the one to restore Stardew Valley to greatness!",
        "keywords": [
            "minigames",
            "2d",
            "fishing",
            "crafting",
            "fairy",
            "achievements",
            "pixel art",
            "snow",
            "relaxing",
            "day/night cycle",
            "customizable characters",
            "deliberately retro",
            "controller support"
        ],
        "release_date": 2016
    },
    "star_fox_64": {
        "igdb_id": "2591",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2e4k.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1vrq.png",
        "key_art_url": "",
        "game_name": "Star Fox 64",
        "igdb_name": "Star Fox 64",
        "age_rating": "7",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Shooter"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "Wii",
            "Nintendo 64",
            "Wii U"
        ],
        "storyline": "Mad scientist Andross arises as the emperor of Venom and declares war on the entire Lylat System, starting with Corneria. General Pepper sends in the Star Fox team to protect the key planets of the Lylat System and stop Dr. Andross.",
        "keywords": [
            "gravity",
            "death",
            "robots",
            "spaceship",
            "flight",
            "multiple endings",
            "artificial intelligence",
            "dog",
            "talking animals",
            "anthropomorphism",
            "voice acting",
            "polygonal 3d",
            "descendants of other characters",
            "secret area",
            "difficulty level",
            "villain",
            "auto-scrolling levels",
            "meme origin",
            "retroachievements"
        ],
        "release_date": 1997
    },
    "subnautica": {
        "igdb_id": "9254",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa938.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar56g.png",
        "key_art_url": "",
        "game_name": "Subnautica",
        "igdb_name": "Subnautica",
        "age_rating": "7",
        "rating": [
            "Mild Language",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "First person",
            "Virtual Reality"
        ],
        "genres": [
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Science fiction",
            "Survival",
            "Open world"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "SteamVR",
            "PlayStation 5",
            "Mac",
            "Oculus Rift",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "You have crash-landed on an alien ocean world, and the only way to go is down. Subnautica's oceans range from sun drenched shallow coral reefs to treacherous deep-sea trenches, lava fields, and bio-luminescent underwater rivers. Manage your oxygen supply as you explore kelp forests, plateaus, reefs, and winding cave systems. The water teems with life: Some of it helpful, much of it harmful.\n\nAfter crash landing in your Life Pod, the clock is ticking to find water, food, and to develop the equipment you need to explore. Collect resources from the ocean around you. Craft diving gear, lights, habitat modules, and submersibles. Venture deeper and further form to find rarer resources, allowing you to craft more advanced items.",
        "keywords": [
            "exploration",
            "swimming",
            "underwater gameplay"
        ],
        "release_date": 2018
    },
    "swr": {
        "igdb_id": "154",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3wj7.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar8f0.png",
        "key_art_url": "",
        "game_name": "Star Wars Episode I Racer",
        "igdb_name": "Star Wars: Episode I - Racer",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Racing"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "PlayStation 4",
            "Nintendo 64",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch",
            "Dreamcast"
        ],
        "storyline": "",
        "keywords": [
            "robots",
            "retroachievements"
        ],
        "release_date": 1999
    },
    "terraria": {
        "igdb_id": "1879",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaamg.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar5kn.png",
        "key_art_url": "",
        "game_name": "Terraria",
        "igdb_name": "Terraria",
        "age_rating": "12",
        "rating": [
            "Mild Suggestive Themes",
            "Blood and Gore",
            "Use of Alcohol",
            "Cartoon Violence",
            "Suggestive Themes",
            "Violence",
            "Blood",
            "Alcohol Reference"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Simulator",
            "Strategy",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction",
            "Horror",
            "Survival",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Google Stadia",
            "PlayStation 3",
            "PlayStation 4",
            "Linux",
            "Nintendo 3DS",
            "Windows Phone",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Wii U",
            "PlayStation Vita",
            "Xbox 360",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "magic",
            "2d",
            "fishing",
            "crafting",
            "death",
            "rabbit",
            "flight",
            "action-adventure",
            "fairy",
            "undead",
            "pixel art",
            "snow",
            "teleportation",
            "climbing",
            "swimming",
            "bats",
            "day/night cycle",
            "sword & sorcery",
            "darkness",
            "explosion",
            "digital distribution",
            "customizable characters",
            "human",
            "bow and arrow",
            "loot gathering",
            "skeletons",
            "deliberately retro",
            "ice stage",
            "melee",
            "underwater gameplay",
            "violent plants",
            "merchants",
            "you can pet the dog",
            "bees"
        ],
        "release_date": 2011
    },
    "tetrisattack": {
        "igdb_id": "2739",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2w6k.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Tetris Attack",
        "igdb_name": "Tetris Attack",
        "age_rating": "E",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Puzzle"
        ],
        "themes": [
            "Action",
            "Kids"
        ],
        "platforms": [
            "Super Nintendo Entertainment System"
        ],
        "storyline": "The story mode takes place in the world of Yoshi's Island, where Bowser and his minions have cursed all of Yoshi's friends. Playing as Yoshi, the player must defeat each of his friends in order to remove the curse. Once all friends have been freed, the game proceeds to a series of Bowser's minions, and then to Bowser himself. During these final matches, the player can select Yoshi or any of his friends to play out the stage.",
        "keywords": [
            "retroachievements"
        ],
        "release_date": 1996
    },
    "timespinner": {
        "igdb_id": "28952",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co24ag.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar9y3.png",
        "key_art_url": "",
        "game_name": "Timespinner",
        "igdb_name": "Timespinner",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Sexual Themes",
            "Mild Language"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "PlayStation Vita",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "With her family murdered in front of her and the ancient Timespinner device destroyed, Lunais is suddenly transported into a unknown world, stranded with seemingly no hope of return. Using her power to control time, Lunais vows to take her revenge on the evil Lachiem Empire, but sometimes the course of history isn\u2019t quite as black and white as it seems...",
        "keywords": [
            "time travel",
            "metroidvania",
            "female protagonist",
            "action-adventure",
            "pixel art",
            "digital distribution",
            "deliberately retro",
            "merchants",
            "lgbtq+"
        ],
        "release_date": 2018
    },
    "tloz": {
        "igdb_id": "1022",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1uii.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14l0.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p2o.png",
        "game_name": "The Legend of Zelda",
        "igdb_name": "The Legend of Zelda",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Family Computer Disk System",
            "Nintendo 3DS",
            "Wii",
            "Family Computer",
            "Wii U",
            "Nintendo Entertainment System"
        ],
        "storyline": "In one of the darkest times in the Kingdom of Hyrule, a young boy named Link takes on an epic quest to restore the fragmented Triforce of Wisdom and save the Princess Zelda from the clutches of the evil Ganon.",
        "keywords": [
            "fairy",
            "overworld",
            "meme origin",
            "retroachievements"
        ],
        "release_date": 1986
    },
    "tloz_ooa": {
        "igdb_id": "1041",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2tw1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar31pi.png",
        "key_art_url": "",
        "game_name": "The Legend of Zelda - Oracle of Ages",
        "igdb_name": "The Legend of Zelda: Oracle of Ages",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Game Boy Color",
            "Nintendo 3DS"
        ],
        "storyline": "A pall of Darkness has fallen over the land of Labrynna. The Sorceress of Shadows has captured the Oracle of Ages and is using her power to do evil. Link has been summoned to help and must travel back and forth in time to stop the Sorceress of Shadows and return Labrynna to its former glory.",
        "keywords": [
            "pirates",
            "ghosts",
            "time travel",
            "minigames",
            "death",
            "rabbit",
            "action-adventure",
            "witches",
            "fairy",
            "undead",
            "campaign",
            "princess",
            "silent protagonist",
            "climbing",
            "swimming",
            "sword & sorcery",
            "explosion",
            "anthropomorphism",
            "shopping",
            "damsel in distress",
            "disorientation zone",
            "descendants of other characters",
            "side quests",
            "real-time combat",
            "shielded enemies",
            "walking through walls",
            "punctuation mark above head",
            "sequence breaking",
            "villain",
            "context sensitive",
            "status effects",
            "behind the waterfall"
        ],
        "release_date": 2001
    },
    "tloz_oos": {
        "igdb_id": "1032",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2tw0.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar31pl.png",
        "key_art_url": "",
        "game_name": "The Legend of Zelda - Oracle of Seasons",
        "igdb_name": "The Legend of Zelda: Oracle of Seasons",
        "age_rating": "7",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Game Boy Color",
            "Nintendo 3DS"
        ],
        "storyline": "The land of Holodrum is slowly withering. Onox, the General of Darkness, has imprisoned the Oracle of Seasons and is draining the very life out of the land. With the seasons in tumult and the forces of evil running rampant, the world looks for a hero... and finds Link. His quest won't be easy - he'll have to master the seasons themselves if he's to turn back the evil tide.",
        "keywords": [
            "pirates",
            "time travel",
            "magic",
            "mascot",
            "death",
            "action-adventure",
            "witches",
            "fairy",
            "backtracking",
            "multiple endings",
            "undead",
            "campaign",
            "princess",
            "pixel art",
            "dog",
            "teleportation",
            "silent protagonist",
            "climbing",
            "sword & sorcery",
            "digital distribution",
            "anthropomorphism",
            "world map",
            "cat",
            "shopping",
            "bow and arrow",
            "damsel in distress",
            "disorientation zone",
            "side quests",
            "potion",
            "real-time combat",
            "secret area",
            "walking through walls",
            "villain",
            "fetch quests",
            "poisoning",
            "context sensitive",
            "status effects",
            "damage over time"
        ],
        "release_date": 2001
    },
    "tloz_ph": {
        "igdb_id": "1037",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3ocu.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/atulchizv5c4ezn2gjob.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p2i.png",
        "game_name": "The Legend of Zelda - Phantom Hourglass",
        "igdb_name": "The Legend of Zelda: Phantom Hourglass",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Wii U",
            "Nintendo DS"
        ],
        "storyline": "Many months have passed since the events of The Legend of Zelda: The Wind Waker, and Link, Tetra and Tetra\u2019s band of pirates have set sail in search of new lands. They come across a patch of ocean covered in a dense fog, in which they discover an abandoned ship. Tetra falls into danger when she explores the ship alone, and Link falls into the ocean when he attempts to rescue her. When he washes up unconscious on the shores of a mysterious island, he is awakened by the sound of a fairy\u2019s voice. With the aid of this fairy, he sets off to find Tetra \u2013 and his way back to the seas he once knew.",
        "keywords": [
            "pirates",
            "exploration",
            "minigames",
            "mascot",
            "death",
            "action-adventure",
            "fairy",
            "backtracking",
            "time limit",
            "campaign",
            "princess",
            "amnesia",
            "silent protagonist",
            "countdown timer",
            "world map",
            "human",
            "polygonal 3d",
            "shopping",
            "bow and arrow",
            "damsel in distress",
            "saving the world",
            "side quests",
            "potion",
            "grapple",
            "real-time combat",
            "moving platforms",
            "been here before",
            "boss assistance",
            "fetch quests",
            "fast traveling",
            "context sensitive",
            "damage over time",
            "monomyth",
            "bees"
        ],
        "release_date": 2007
    },
    "tmc": {
        "igdb_id": "1035",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3nsk.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/shsfsrmdduhlknr5piky.png",
        "key_art_url": "",
        "game_name": "The Minish Cap",
        "igdb_name": "The Legend of Zelda: The Minish Cap",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "While at a festival with Princess Zelda, Link encounters a mysterious mage called Vaati who turns the princess to stone. Helpless to stop them, Link is asked by the king to meet with a race of tiny people known as the Minish, who may be able to help with their predicament. On his travels, Link teams up with a talking cap called Ezlo, who is able to shrink Link to the size of a Minish so that he can meet with them. With his newfound abilities, Link must save the kingdom from Vaati's menace.",
        "keywords": [
            "ghosts",
            "magic",
            "mascot",
            "death",
            "maze",
            "action-adventure",
            "witches",
            "fairy",
            "bird",
            "backtracking",
            "time limit",
            "undead",
            "traps",
            "campaign",
            "princess",
            "pixel art",
            "dog",
            "teleportation",
            "silent protagonist",
            "climbing",
            "swimming",
            "sword & sorcery",
            "darkness",
            "explosion",
            "digital distribution",
            "anthropomorphism",
            "countdown timer",
            "world map",
            "cat",
            "shopping",
            "bow and arrow",
            "damsel in distress",
            "upgradeable weapons",
            "breaking the fourth wall",
            "pop culture reference",
            "game reference",
            "disorientation zone",
            "descendants of other characters",
            "ice stage",
            "unstable platforms",
            "saving the world",
            "side quests",
            "potion",
            "melee",
            "grapple",
            "real-time combat",
            "secret area",
            "shielded enemies",
            "coming of age",
            "moving platforms",
            "punctuation mark above head",
            "sequence breaking",
            "villain",
            "been here before",
            "sleeping",
            "boss assistance",
            "fetch quests",
            "gliding",
            "poisoning",
            "fast traveling",
            "living inventory",
            "status effects",
            "behind the waterfall",
            "foreshadowing",
            "damage over time",
            "monomyth"
        ],
        "release_date": 2004
    },
    "toontown": {
        "igdb_id": "25326",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co28yv.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Toontown",
        "igdb_name": "Toontown Online",
        "age_rating": "3",
        "rating": [
            "Cartoon Violence",
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [
            "Comedy",
            "Open world"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "Toontown Online's story centers on an ongoing battle between a population of cartoon animals known as the Toons and a collection of business-minded robots known as the Cogs who are trying to take over the town. Players would choose and customize their own toon and go on to complete Toontasks, play mini-games, and fight the Cogs.",
        "keywords": [
            "minigames"
        ],
        "release_date": 2003
    },
    "tp": {
        "igdb_id": "134014",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w1h.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar21yd.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p34.png",
        "game_name": "Twilight Princess",
        "igdb_name": "The Legend of Zelda: Twilight Princess",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Animated Blood"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Wii"
        ],
        "storyline": "Link, a young farm boy whose tasks consist of herding goats to watching children in Ordon village, is asked by the mayor to run an errand in Castle Town. But things went strange that day: the land becomes dark and strange creatures appear from another world called the Twilight Realm which turns most people into ghosts. Unlike the others, Link transforms into a wolf but is captured. A mysterious figure named Midna helps him break free, and with the aid of her magic, they set off to free the land from the shadows. Link must explore the vast land of Hyrule and uncover the mystery behind its plunge into darkness.",
        "keywords": [],
        "release_date": 2006
    },
    "trackmania": {
        "igdb_id": "133807",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2fe9.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar8jb.png",
        "key_art_url": "",
        "game_name": "Trackmania",
        "igdb_name": "Trackmania",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "First person",
            "Third person"
        ],
        "genres": [
            "Racing",
            "Sport",
            "Arcade"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2020
    },
    "tunic": {
        "igdb_id": "23733",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/td1t8kb33gyo8mvhl2pc.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arklp.png",
        "key_art_url": "",
        "game_name": "TUNIC",
        "igdb_name": "Tunic",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Tunic is an action adventure game about a small fox in a big world, who must explore the countryside, fight monsters, and discover secrets. Crafted to evoke feelings of classic action adventure games, Tunic will challenge the player with unique items, skillful combat techniques, and arcane mysteries as our hero forges their way through an intriguing new world.",
        "keywords": [
            "exploration",
            "3d",
            "difficult",
            "stylized",
            "achievements",
            "cute",
            "atmospheric",
            "great soundtrack",
            "digital distribution",
            "anthropomorphism",
            "melee",
            "secret area",
            "controller support",
            "soulslike"
        ],
        "release_date": 2022
    },
    "tww": {
        "igdb_id": "1033",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3ohz.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/nqujfvlda7lg7bhk7xrq.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3p3f.png",
        "game_name": "The Wind Waker",
        "igdb_name": "The Legend of Zelda: The Wind Waker",
        "age_rating": "7",
        "rating": [
            "Violence"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "Nintendo GameCube"
        ],
        "storyline": "Set hundreds of years after the events of Ocarina of Time, The Wind Waker finds the hero Link living with his grandmother on the Outset Island, one of the many small islands lost amidst the waters of the Great Sea. On his tenth birthday, Link encounters a giant bird carrying a girl. He rescues the girl, but as a result his own sister is taken away by the bird. The girl is a pirate captain named Tetra, who agrees to help Link find and rescue his sister. During the course of their journey, the two of them realize that a powerful, legendary evil is active again, and must find a way to stop him.",
        "keywords": [
            "archery",
            "action-adventure",
            "fairy",
            "day/night cycle",
            "sword & sorcery",
            "auto-aim",
            "living inventory",
            "retroachievements"
        ],
        "release_date": 2002
    },
    "tyrian": {
        "igdb_id": "14432",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2zg1.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Tyrian",
        "igdb_name": "Tyrian 2000",
        "age_rating": "E",
        "rating": [
            "Animated Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Shooter",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Science fiction"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac",
            "DOS"
        ],
        "storyline": "",
        "keywords": [
            "pixel art"
        ],
        "release_date": 1999
    },
    "undertale": {
        "igdb_id": "12517",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2855.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar4vc.png",
        "key_art_url": "",
        "game_name": "Undertale",
        "igdb_name": "Undertale",
        "age_rating": "12",
        "rating": [
            "Mild Blood",
            "Mild Language",
            "Use of Tobacco",
            "Simulated Gambling",
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Horror",
            "Comedy",
            "Drama"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "PlayStation Vita",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "\"A long time ago, two races ruled peacefully over the Earth: HUMANS and MONSTERS. One day, a terrible war broke out between the two races. After a long battle, the humans were victorious. They sealed the monsters underground with a magical spell.\n\nIn the year 201X, a small child scales Mt. Ebott. It is said that those who climb the mountain never return.\n\nSeeking refuge from the rainy weather, the child enters a cave and discovers an enormous hole.\n\nMoving closer to get a better look... the child falls in.\n\nNow, our story begins.\"",
        "keywords": [
            "retro",
            "2d",
            "turn-based",
            "female protagonist",
            "backtracking",
            "multiple endings",
            "cute",
            "funny",
            "pixel art",
            "story rich",
            "great soundtrack",
            "anthropomorphism",
            "leveling up",
            "breaking the fourth wall",
            "skeletons",
            "plot twist",
            "fast traveling",
            "you can pet the dog"
        ],
        "release_date": 2015
    },
    "v6": {
        "igdb_id": "1990",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4ieg.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arct2.png",
        "key_art_url": "",
        "game_name": "VVVVVV",
        "igdb_name": "VVVVVV",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence",
            "Mild Language"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction"
        ],
        "platforms": [
            "PlayStation 4",
            "Ouya",
            "Linux",
            "Nintendo 3DS",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "PlayStation Vita",
            "Nintendo Switch"
        ],
        "storyline": "A spaceship with six crew members - Viridian, Victoria, Vitellary, Vermillion, Verdigris, and Violet - suddenly encountered mysterious trouble while underway.\nThe group escapes by means of a teleportation device, but for some reason all the crew members are sent to different places.\nViridian, the protagonist, must find the other crew members and escape from this mysterious labyrinth...",
        "keywords": [
            "ghosts",
            "exploration",
            "retro",
            "gravity",
            "2d",
            "metroidvania",
            "death",
            "spaceship",
            "achievements",
            "pixel art",
            "teleportation",
            "digital distribution",
            "world map",
            "deliberately retro",
            "save point",
            "checkpoints",
            "unstable platforms",
            "instant kill",
            "moving platforms",
            "auto-scrolling levels",
            "time trials",
            "controller support"
        ],
        "release_date": 2010
    },
    "wargroove": {
        "igdb_id": "27441",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4hgb.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar9ii.png",
        "key_art_url": "",
        "game_name": "Wargroove",
        "igdb_name": "Wargroove",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Strategy",
            "Turn-based strategy (TBS)",
            "Tactical",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Warfare"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Wargroove is a modern take on the simple yet deep turn-based tactical gameplay popularised in the 2000s by handheld games such as Advance Wars. As big fans of those games we were disappointed to find that nothing in this genre was available on current generation platforms and set out to fill the gap ourselves. Wargroove aims to recreate the charm and accessibility of the titles that inspired it whilst bringing modern technology into the formula. This modern focus allows for higher resolution pixel art, robust online play and deep modding capability, ultimately creating the most complete experience for Advance Wars and TBS fans.",
        "keywords": [
            "pixel art"
        ],
        "release_date": 2019
    },
    "wargroove2": {
        "igdb_id": "241149",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co731u.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar28cx.png",
        "key_art_url": "",
        "game_name": "Wargroove 2",
        "igdb_name": "Wargroove 2",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Strategy",
            "Turn-based strategy (TBS)",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Warfare"
        ],
        "platforms": [
            "Xbox Series X|S",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "Three years have passed since Queen Mercia and her allies defeated the ancient adversaries and restored peace to Aurania. Now, an ambitious foreign faction is unearthing forbidden technologies that could have catastrophic consequences for the land and its people. Battle your way through 3 Campaigns following 1 interweaving story. Only bold decisions, smart resourcing, and tactical know-how can repair a fractured realm\u2026",
        "keywords": [
            "pirates"
        ],
        "release_date": 2023
    },
    "witness": {
        "igdb_id": "5601",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3hih.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1cly.png",
        "key_art_url": "",
        "game_name": "The Witness",
        "igdb_name": "The Witness",
        "age_rating": "3",
        "rating": [
            "Alcohol Reference"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Puzzle",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Science fiction",
            "Open world",
            "Mystery"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Xbox One"
        ],
        "storyline": "You wake up, alone, on a strange island full of puzzles that will challenge and surprise you.\n\nYou don't remember who you are, and you don't remember how you got here, but there's one thing you can do: explore the island in hope of discovering clues, regaining your memory, and somehow finding your way home.",
        "keywords": [
            "exploration",
            "maze",
            "backtracking",
            "time limit",
            "multiple endings",
            "amnesia",
            "darkness",
            "digital distribution",
            "voice acting",
            "polygonal 3d",
            "pop culture reference",
            "game reference",
            "stat tracking",
            "secret area"
        ],
        "release_date": 2016
    },
    "wl": {
        "igdb_id": "1072",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co216h.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kik.png",
        "key_art_url": "",
        "game_name": "Wario Land",
        "igdb_name": "Wario Land: Super Mario Land 3",
        "age_rating": "3",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Game Boy"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 1994
    },
    "wl4": {
        "igdb_id": "1699",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wpx.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kt5.png",
        "key_art_url": "",
        "game_name": "Wario Land 4",
        "igdb_name": "Wario Land 4",
        "age_rating": "3",
        "rating": [
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Nintendo 3DS",
            "Wii U",
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "anime",
            "minigames",
            "flight",
            "time limit",
            "multiple endings",
            "pixel art",
            "sequel",
            "swimming",
            "digital distribution",
            "countdown timer",
            "cat",
            "sprinting mechanics",
            "ice stage",
            "melee",
            "moving platforms",
            "sequence breaking"
        ],
        "release_date": 2001
    },
    "xenobladex": {
        "igdb_id": "2366",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1nwh.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar37uu.png",
        "key_art_url": "",
        "game_name": "Xenoblade X",
        "igdb_name": "Xenoblade Chronicles X",
        "age_rating": "12",
        "rating": [
            "Suggestive Themes",
            "Use of Alcohol",
            "Language",
            "Violence",
            "Animated Blood"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Wii U"
        ],
        "storyline": "Xenoblade Chronicles X opens as humanity, warned of its impending destruction in the crossfire between two warring alien races, constructs interstellar arks to escape Earth. However, only a few arks escape the destruction, including the White Whale ark. Two years after launching, the White Whale is attacked and transported to Mira. During the crash-landing, the Lifehold\u2014a device containing the majority of the human colonists\u2014is separated from the White Whale, with lifepods containing colonists being scattered across Mira. The avatar is awoken from a lifepod by Elma and brought back to New Los Angeles. While suffering from amnesia, the avatar joins BLADE, working with Elma and Lin to recover more lifepods and search for the Lifehold. During their missions across Mira, BLADE encounters multiple alien races, learning that those attacking them are part of the Ganglion coalition, an alliance of races led by the Ganglion race, who are intent on destroying humanity.",
        "keywords": [
            "aliens",
            "robots",
            "flight",
            "action-adventure",
            "amnesia",
            "day/night cycle",
            "customizable characters",
            "voice acting",
            "polygonal 3d",
            "loot gathering",
            "party system",
            "side quests",
            "real-time combat"
        ],
        "release_date": 2015
    },
    "yoshisisland": {
        "igdb_id": "1073",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kn9.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1gep.png",
        "key_art_url": "",
        "game_name": "Yoshi's Island",
        "igdb_name": "Super Mario World 2: Yoshi's Island",
        "age_rating": "E",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Kids"
        ],
        "platforms": [
            "Satellaview",
            "Super Nintendo Entertainment System",
            "Super Famicom"
        ],
        "storyline": "A stork carrying the infant Mario Brothers is attacked by Kamek the Magikoopa, who steals Baby Luigi and knocks Baby Mario out of the sky. Baby Mario lands on Yoshi's Island on the back of Yoshi himself. With the help of his seven other Yoshi friends, Yoshi must traverse the island to safely reunite Baby Mario with his brother and get the babies to their parents.",
        "keywords": [
            "dinosaurs",
            "side-scrolling",
            "digital distribution"
        ],
        "release_date": 1995
    },
    "yugioh06": {
        "igdb_id": "49377",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7yau.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Yu-Gi-Oh! 2006",
        "igdb_name": "Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006",
        "age_rating": "3",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Text"
        ],
        "genres": [
            "Strategy",
            "Turn-based strategy (TBS)",
            "Card & Board Game"
        ],
        "themes": [
            "Fantasy",
            "Survival"
        ],
        "platforms": [
            "Game Boy Advance"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2006
    },
    "yugiohddm": {
        "igdb_id": "49211",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5ztw.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Yu-Gi-Oh! Dungeon Dice Monsters",
        "igdb_name": "Yu-Gi-Oh! Dungeon Dice Monsters",
        "age_rating": "3",
        "rating": [
            "Mild Violence"
        ],
        "player_perspectives": [
            "First person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Strategy",
            "Turn-based strategy (TBS)",
            "Card & Board Game"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "Game Boy Advance"
        ],
        "storyline": "Dungeon Dice Monsters is the newest addition to the Yu-Gi-Oh! universe. As featured in the Dungeon Dice Monsters story arc in the animated television series, players collect and fight with dice inscribed with mystical powers and magic in order to defeat their opponents. Enter a dozen different tournaments and ultimately faceoff against the scheming creator of Dungeon Dice Monsters, Duke Devlin.",
        "keywords": [
            "anime",
            "shopping",
            "merchants"
        ],
        "release_date": 2001
    },
    "zelda2": {
        "igdb_id": "1025",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1uje.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar14l5.png",
        "key_art_url": "",
        "game_name": "Zelda II: The Adventure of Link",
        "igdb_name": "Zelda II: The Adventure of Link",
        "age_rating": "7",
        "rating": [
            "Mild Fantasy Violence"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox"
        ],
        "platforms": [
            "Family Computer Disk System",
            "Nintendo 3DS",
            "Wii",
            "Wii U",
            "Nintendo Entertainment System"
        ],
        "storyline": "Several years after the events of The Legend of Zelda, Link has just turned sixteen and discovers a strange birthmark on his hand. With the help of Impa, Zelda's nursemaid, Link learns that this mark is the key to unlock a secret room where Princess Zelda lies sleeping. When young, Princess Zelda was given knowledge of the Triforce of power which was used to rule the kingdom of Hyrule, but when a magician unsuccessfully tried to find out about the Triforce from Zelda, he put her into an eternal sleep. In his grief, the prince placed Zelda in this room hoping she may wake some day. He ordered all female children in the royal household to be named Zelda from this point on, so the tragedy would not be forgotten. Now, to bring Princess Zelda back, Link must locate all the pieces of the Triforce which have been hidden throughout the land.",
        "keywords": [
            "magic",
            "collecting",
            "2d",
            "metroidvania",
            "death",
            "difficult",
            "action-adventure",
            "side-scrolling",
            "fairy",
            "overworld",
            "campaign",
            "pixel art",
            "sequel",
            "silent protagonist",
            "bats",
            "darkness",
            "explosion",
            "spider",
            "leveling up",
            "human",
            "damsel in distress",
            "unstable platforms",
            "saving the world",
            "potion",
            "real-time combat",
            "secret area",
            "rpg elements",
            "villain",
            "fetch quests",
            "meme origin",
            "status effects",
            "monomyth"
        ],
        "release_date": 1987
    }
} # type: ignore

SEARCH_INDEX = {
    "popular": [
        "alttp",
        "sc2",
        "oot",
        "kh2",
        "hk",
        "sm64ex"
    ],
    "against the storm": [
        "against_the_storm"
    ],
    "against": [
        "against_the_storm"
    ],
    "the": [
        "seaofthieves",
        "k64",
        "tloz_ph",
        "alttp",
        "witness",
        "zelda2",
        "metroidfusion",
        "undertale",
        "oot",
        "terraria",
        "hades",
        "banjo_tooie",
        "albw",
        "dkc2",
        "against_the_storm",
        "tp",
        "diddy_kong_racing",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "rogue_legacy",
        "jakanddaxter",
        "messenger",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "smo",
        "spyro3",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ladx",
        "mlss",
        "tmc",
        "lego_star_wars_tcs",
        "lufia2ac",
        "overcooked2",
        "earthbound",
        "gstla",
        "hcniko",
        "sly1",
        "ffta",
        "tloz",
        "sims4",
        "oribf",
        "papermario"
    ],
    "storm": [
        "against_the_storm"
    ],
    "bird view / isometric": [
        "tunic",
        "crystal_project",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "ctjot",
        "balatro",
        "undertale",
        "yugioh06",
        "wargroove2",
        "ff4fe",
        "factorio",
        "shorthike",
        "tyrian",
        "pokemon_rb",
        "dw1",
        "soe",
        "hades",
        "yugiohddm",
        "pokemon_crystal",
        "sms",
        "albw",
        "dredge",
        "brotato",
        "against_the_storm",
        "mmbn3",
        "diddy_kong_racing",
        "civ_6",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "tloz_oos",
        "cuphead",
        "sims4",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "ff1",
        "ladx",
        "pmd_eos",
        "stardew_valley",
        "wargroove",
        "tmc",
        "overcooked2",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "placidplasticducksim"
    ],
    "bird": [
        "tunic",
        "crystal_project",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "ctjot",
        "balatro",
        "undertale",
        "yugioh06",
        "wargroove2",
        "ff4fe",
        "factorio",
        "shorthike",
        "tyrian",
        "pokemon_rb",
        "dw1",
        "soe",
        "hades",
        "yugiohddm",
        "pokemon_crystal",
        "banjo_tooie",
        "sms",
        "albw",
        "dredge",
        "brotato",
        "against_the_storm",
        "mmbn3",
        "diddy_kong_racing",
        "civ_6",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "tloz_oos",
        "rogue_legacy",
        "cuphead",
        "sims4",
        "tloz_ooa",
        "dkc3",
        "pokemon_frlg",
        "spyro3",
        "ff1",
        "ladx",
        "pmd_eos",
        "stardew_valley",
        "wargroove",
        "tmc",
        "overcooked2",
        "earthbound",
        "gstla",
        "minecraft",
        "ffta",
        "tloz",
        "ffmq",
        "placidplasticducksim"
    ],
    "view": [
        "momodoramoonlitfarewell",
        "ctjot",
        "undertale",
        "wl",
        "monster_sanctuary",
        "ff4fe",
        "terraria",
        "mzm",
        "smw",
        "against_the_storm",
        "mm2",
        "mmbn3",
        "megamix",
        "animal_well",
        "cuphead",
        "faxanadu",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "sotn",
        "ff1",
        "ladx",
        "oribf",
        "papermario",
        "tunic",
        "mm3",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "timespinner",
        "tyrian",
        "dw1",
        "yoshisisland",
        "sm_map_rando",
        "soe",
        "sms",
        "albw",
        "dkc2",
        "tetrisattack",
        "crosscode",
        "rogue_legacy",
        "dkc3",
        "wargroove",
        "stardew_valley",
        "tmc",
        "overcooked2",
        "ffta",
        "tloz",
        "crystal_project",
        "k64",
        "zelda2",
        "v6",
        "yugioh06",
        "metroidfusion",
        "wargroove2",
        "musedash",
        "factorio",
        "shorthike",
        "kdl3",
        "pokemon_rb",
        "mmx3",
        "yugiohddm",
        "pokemon_crystal",
        "dredge",
        "brotato",
        "ror1",
        "getting_over_it",
        "diddy_kong_racing",
        "civ_6",
        "landstalker",
        "sm",
        "tloz_oos",
        "messenger",
        "dkc",
        "pmd_eos",
        "lufia2ac",
        "wl4",
        "earthbound",
        "gstla",
        "celeste_open_world",
        "tloz_ph",
        "balatro",
        "hades",
        "marioland2",
        "hk",
        "dontstarvetogether",
        "cvcotm",
        "enderlilies",
        "ffmq",
        "mlss",
        "celeste",
        "sims4",
        "placidplasticducksim"
    ],
    "/": [
        "tunic",
        "crystal_project",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "ctjot",
        "balatro",
        "undertale",
        "yugioh06",
        "wargroove2",
        "ff4fe",
        "factorio",
        "shorthike",
        "tyrian",
        "pokemon_rb",
        "dw1",
        "soe",
        "hades",
        "yugiohddm",
        "pokemon_crystal",
        "sms",
        "albw",
        "dredge",
        "brotato",
        "against_the_storm",
        "mmbn3",
        "diddy_kong_racing",
        "civ_6",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "tloz_oos",
        "cuphead",
        "sims4",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "ff1",
        "ladx",
        "pmd_eos",
        "stardew_valley",
        "wargroove",
        "tmc",
        "overcooked2",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "placidplasticducksim"
    ],
    "isometric": [
        "tunic",
        "crystal_project",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "ctjot",
        "balatro",
        "undertale",
        "yugioh06",
        "wargroove2",
        "ff4fe",
        "factorio",
        "shorthike",
        "tyrian",
        "pokemon_rb",
        "dw1",
        "soe",
        "hades",
        "yugiohddm",
        "pokemon_crystal",
        "sms",
        "albw",
        "dredge",
        "brotato",
        "against_the_storm",
        "mmbn3",
        "diddy_kong_racing",
        "civ_6",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "tloz_oos",
        "cuphead",
        "sims4",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "ff1",
        "ladx",
        "pmd_eos",
        "stardew_valley",
        "wargroove",
        "tmc",
        "overcooked2",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "placidplasticducksim"
    ],
    "real time strategy (rts)": [
        "mmbn3",
        "against_the_storm"
    ],
    "real": [
        "mmbn3",
        "against_the_storm"
    ],
    "time": [
        "apeescape",
        "pokemon_emerald",
        "timespinner",
        "alttp",
        "tloz_ph",
        "ctjot",
        "witness",
        "metroidprime",
        "v6",
        "metroidfusion",
        "ahit",
        "shorthike",
        "oot",
        "sm_map_rando",
        "outer_wilds",
        "pokemon_crystal",
        "sms",
        "against_the_storm",
        "ror1",
        "mmbn3",
        "diddy_kong_racing",
        "sm",
        "tloz_oos",
        "mm_recomp",
        "rogue_legacy",
        "jakanddaxter",
        "tloz_ooa",
        "spyro3",
        "pmd_eos",
        "tmc",
        "mk64",
        "wl4",
        "earthbound",
        "sly1",
        "ffta"
    ],
    "strategy": [
        "fm",
        "crystal_project",
        "pokemon_emerald",
        "balatro",
        "undertale",
        "yugioh06",
        "monster_sanctuary",
        "wargroove2",
        "factorio",
        "terraria",
        "pokemon_rb",
        "satisfactory",
        "yugiohddm",
        "against_the_storm",
        "mmbn3",
        "civ_6",
        "dontstarvetogether",
        "pokemon_frlg",
        "pmd_eos",
        "wargroove",
        "stardew_valley",
        "overcooked2",
        "earthbound",
        "ffta"
    ],
    "(rts)": [
        "mmbn3",
        "against_the_storm"
    ],
    "simulator": [
        "seaofthieves",
        "stardew_valley",
        "getting_over_it",
        "satisfactory",
        "civ_6",
        "outer_wilds",
        "doronko_wanko",
        "dontstarvetogether",
        "overcooked2",
        "raft",
        "minecraft",
        "sims4",
        "powerwashsimulator",
        "dredge",
        "factorio",
        "against_the_storm",
        "placidplasticducksim",
        "terraria"
    ],
    "indie": [
        "shivers",
        "tunic",
        "crystal_project",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "getting_over_it",
        "crosscode",
        "dontstarvetogether",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "hcniko",
        "cat_quest",
        "celeste_open_world"
    ],
    "fantasy": [
        "tunic",
        "fm",
        "crystal_project",
        "seaofthieves",
        "sm64hacks",
        "tloz_ph",
        "pokemon_emerald",
        "timespinner",
        "alttp",
        "ctjot",
        "zelda2",
        "v6",
        "yugioh06",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "ff4fe",
        "shorthike",
        "wargroove2",
        "oot",
        "pokemon_rb",
        "terraria",
        "yoshisisland",
        "hades",
        "yugiohddm",
        "pokemon_crystal",
        "banjo_tooie",
        "albw",
        "smw",
        "dkc2",
        "hk",
        "against_the_storm",
        "kh1",
        "tp",
        "ror1",
        "civ_6",
        "landstalker",
        "tloz_oos",
        "mm_recomp",
        "tww",
        "ss",
        "rogue_legacy",
        "cuphead",
        "kh2",
        "sims4",
        "faxanadu",
        "oribf",
        "smo",
        "pokemon_frlg",
        "enderlilies",
        "ff1",
        "ladx",
        "mlss",
        "celeste",
        "pmd_eos",
        "sm64ex",
        "stardew_valley",
        "tmc",
        "lufia2ac",
        "wargroove",
        "earthbound",
        "gstla",
        "minecraft",
        "cat_quest",
        "ffta",
        "tloz",
        "ffmq",
        "celeste_open_world",
        "papermario"
    ],
    "xbox series x|s": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "balatro",
        "wargroove2",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "against_the_storm",
        "animal_well",
        "enderlilies",
        "ror2",
        "placidplasticducksim"
    ],
    "xbox": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "sonic_heroes",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "wargroove2",
        "terraria",
        "dw1",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "crosscode",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "sadx",
        "oribf",
        "messenger",
        "enderlilies",
        "sotn",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "swr",
        "sa2b",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "series": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "balatro",
        "wargroove2",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "against_the_storm",
        "animal_well",
        "enderlilies",
        "ror2",
        "placidplasticducksim"
    ],
    "x|s": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "balatro",
        "wargroove2",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "against_the_storm",
        "animal_well",
        "enderlilies",
        "ror2",
        "placidplasticducksim"
    ],
    "pc (microsoft windows)": [
        "shivers",
        "tunic",
        "crystal_project",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "sonic_heroes",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "tyrian",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "doronko_wanko",
        "dontstarvetogether",
        "landstalker",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "sadx",
        "oribf",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "hcniko",
        "minecraft",
        "cat_quest",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "pc": [
        "shivers",
        "tunic",
        "crystal_project",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "sonic_heroes",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "tyrian",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "doronko_wanko",
        "dontstarvetogether",
        "landstalker",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "sadx",
        "oribf",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "hcniko",
        "minecraft",
        "cat_quest",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "(microsoft": [
        "shivers",
        "tunic",
        "crystal_project",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "sonic_heroes",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "tyrian",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "doronko_wanko",
        "dontstarvetogether",
        "landstalker",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "sadx",
        "oribf",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "hcniko",
        "minecraft",
        "cat_quest",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "windows)": [
        "shivers",
        "tunic",
        "crystal_project",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "timespinner",
        "witness",
        "sonic_heroes",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "tyrian",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "doronko_wanko",
        "dontstarvetogether",
        "landstalker",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "sadx",
        "oribf",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "hcniko",
        "minecraft",
        "cat_quest",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "playstation 5": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "balatro",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "against_the_storm",
        "crosscode",
        "animal_well",
        "messenger",
        "ror2",
        "placidplasticducksim"
    ],
    "playstation": [
        "tunic",
        "fm",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "apeescape",
        "timespinner",
        "witness",
        "sonic_heroes",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "terraria",
        "dw1",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "rac2",
        "brotato",
        "hk",
        "against_the_storm",
        "kh1",
        "ror1",
        "crosscode",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "kh2",
        "sadx",
        "messenger",
        "spyro3",
        "enderlilies",
        "sotn",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "lego_star_wars_tcs",
        "overcooked2",
        "cat_quest",
        "sly1",
        "swr",
        "sa2b",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "5": [
        "tunic",
        "seaofthieves",
        "momodoramoonlitfarewell",
        "balatro",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "trackmania",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "against_the_storm",
        "crosscode",
        "animal_well",
        "messenger",
        "ror2",
        "placidplasticducksim"
    ],
    "nintendo switch": [
        "tunic",
        "crystal_project",
        "momodoramoonlitfarewell",
        "timespinner",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "crosscode",
        "megamix",
        "doronko_wanko",
        "dontstarvetogether",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "oribf",
        "messenger",
        "smo",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "hcniko",
        "cat_quest",
        "swr",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "nintendo": [
        "sm64hacks",
        "momodoramoonlitfarewell",
        "ctjot",
        "metroidprime",
        "undertale",
        "wl",
        "monster_sanctuary",
        "ff4fe",
        "terraria",
        "smw",
        "against_the_storm",
        "mm2",
        "megamix",
        "mm_recomp",
        "animal_well",
        "cuphead",
        "dk64",
        "cv64",
        "faxanadu",
        "tloz_ooa",
        "ff1",
        "ladx",
        "ror2",
        "mk64",
        "cat_quest",
        "swr",
        "oribf",
        "papermario",
        "tunic",
        "mm3",
        "timespinner",
        "alttp",
        "sonic_heroes",
        "ahit",
        "oot",
        "dw1",
        "yoshisisland",
        "sm_map_rando",
        "soe",
        "outer_wilds",
        "sms",
        "albw",
        "dkc2",
        "tetrisattack",
        "crosscode",
        "tww",
        "doronko_wanko",
        "rogue_legacy",
        "dkc3",
        "smo",
        "wargroove",
        "stardew_valley",
        "tmc",
        "overcooked2",
        "tloz",
        "star_fox_64",
        "crystal_project",
        "k64",
        "zelda2",
        "v6",
        "metroidfusion",
        "wargroove2",
        "musedash",
        "factorio",
        "shorthike",
        "kdl3",
        "pokemon_rb",
        "mmx3",
        "pokemon_crystal",
        "banjo_tooie",
        "luigismansion",
        "dredge",
        "mario_kart_double_dash",
        "brotato",
        "ror1",
        "diddy_kong_racing",
        "sm",
        "tloz_oos",
        "messenger",
        "dkc",
        "pmd_eos",
        "lufia2ac",
        "wl4",
        "earthbound",
        "hcniko",
        "celeste_open_world",
        "tloz_ph",
        "balatro",
        "bomb_rush_cyberfunk",
        "hades",
        "subnautica",
        "powerwashsimulator",
        "marioland2",
        "hk",
        "dontstarvetogether",
        "enderlilies",
        "celeste",
        "sm64ex",
        "ffmq",
        "placidplasticducksim"
    ],
    "switch": [
        "tunic",
        "crystal_project",
        "momodoramoonlitfarewell",
        "timespinner",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "against_the_storm",
        "ror1",
        "crosscode",
        "megamix",
        "doronko_wanko",
        "dontstarvetogether",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "oribf",
        "messenger",
        "smo",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "hcniko",
        "cat_quest",
        "swr",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "roguelite": [
        "ror1",
        "hades",
        "ror2",
        "brotato",
        "against_the_storm"
    ],
    "a hat in time": [
        "ahit"
    ],
    "a": [
        "albw",
        "alttp",
        "shorthike",
        "ahit"
    ],
    "hat": [
        "ahit"
    ],
    "in": [
        "sm_map_rando",
        "sm",
        "tloz_oos",
        "tloz_ph",
        "tmc",
        "alttp",
        "ss",
        "earthbound",
        "sms",
        "albw",
        "metroidprime",
        "smw",
        "zelda2",
        "ahit",
        "tloz_ooa",
        "kh1",
        "oot",
        "papermario"
    ],
    "first person": [
        "shivers",
        "fm",
        "seaofthieves",
        "witness",
        "metroidprime",
        "ahit",
        "trackmania",
        "satisfactory",
        "yugiohddm",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "sims4",
        "cv64",
        "earthbound",
        "minecraft",
        "swr",
        "star_fox_64"
    ],
    "first": [
        "shivers",
        "fm",
        "seaofthieves",
        "witness",
        "metroidprime",
        "ahit",
        "trackmania",
        "satisfactory",
        "yugiohddm",
        "outer_wilds",
        "raft",
        "subnautica",
        "powerwashsimulator",
        "sims4",
        "cv64",
        "earthbound",
        "minecraft",
        "swr",
        "star_fox_64"
    ],
    "person": [
        "shivers",
        "fm",
        "crystal_project",
        "seaofthieves",
        "sm64hacks",
        "apeescape",
        "witness",
        "sonic_heroes",
        "metroidprime",
        "ahit",
        "oot",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "trackmania",
        "satisfactory",
        "yugiohddm",
        "xenobladex",
        "outer_wilds",
        "banjo_tooie",
        "raft",
        "subnautica",
        "luigismansion",
        "sms",
        "albw",
        "powerwashsimulator",
        "rac2",
        "mario_kart_double_dash",
        "kh1",
        "tp",
        "getting_over_it",
        "diddy_kong_racing",
        "megamix",
        "tww",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "kh2",
        "dk64",
        "cv64",
        "sadx",
        "smo",
        "spyro3",
        "sm64ex",
        "ror2",
        "lego_star_wars_tcs",
        "mk64",
        "earthbound",
        "gstla",
        "hcniko",
        "cat_quest",
        "minecraft",
        "sly1",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "star_fox_64",
        "placidplasticducksim",
        "papermario"
    ],
    "third person": [
        "crystal_project",
        "sm64hacks",
        "apeescape",
        "sonic_heroes",
        "ahit",
        "oot",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "trackmania",
        "xenobladex",
        "banjo_tooie",
        "raft",
        "luigismansion",
        "sms",
        "albw",
        "rac2",
        "mario_kart_double_dash",
        "kh1",
        "tp",
        "getting_over_it",
        "diddy_kong_racing",
        "megamix",
        "tww",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "kh2",
        "dk64",
        "cv64",
        "sadx",
        "smo",
        "spyro3",
        "sm64ex",
        "ror2",
        "lego_star_wars_tcs",
        "mk64",
        "gstla",
        "hcniko",
        "minecraft",
        "cat_quest",
        "sly1",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "star_fox_64",
        "placidplasticducksim",
        "papermario"
    ],
    "third": [
        "crystal_project",
        "sm64hacks",
        "apeescape",
        "sonic_heroes",
        "ahit",
        "oot",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "trackmania",
        "xenobladex",
        "banjo_tooie",
        "raft",
        "luigismansion",
        "sms",
        "albw",
        "rac2",
        "mario_kart_double_dash",
        "kh1",
        "tp",
        "getting_over_it",
        "diddy_kong_racing",
        "megamix",
        "tww",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "kh2",
        "dk64",
        "cv64",
        "sadx",
        "smo",
        "spyro3",
        "sm64ex",
        "ror2",
        "lego_star_wars_tcs",
        "mk64",
        "gstla",
        "hcniko",
        "minecraft",
        "cat_quest",
        "sly1",
        "swr",
        "sa2b",
        "toontown",
        "sims4",
        "star_fox_64",
        "placidplasticducksim",
        "papermario"
    ],
    "platform": [
        "crystal_project",
        "sm64hacks",
        "k64",
        "apeescape",
        "mm3",
        "momodoramoonlitfarewell",
        "timespinner",
        "sonic_heroes",
        "zelda2",
        "metroidprime",
        "v6",
        "metroidfusion",
        "wl",
        "ahit",
        "monster_sanctuary",
        "kdl3",
        "terraria",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "mzm",
        "banjo_tooie",
        "sms",
        "smw",
        "rac2",
        "dkc2",
        "marioland2",
        "hk",
        "mm2",
        "ror1",
        "getting_over_it",
        "sm",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "dk64",
        "cv64",
        "faxanadu",
        "messenger",
        "oribf",
        "sadx",
        "dkc",
        "dkc3",
        "smo",
        "spyro3",
        "cvcotm",
        "enderlilies",
        "sotn",
        "celeste",
        "sm64ex",
        "lego_star_wars_tcs",
        "wl4",
        "hcniko",
        "sly1",
        "sa2b",
        "celeste_open_world"
    ],
    "adventure": [
        "seaofthieves",
        "sm64hacks",
        "momodoramoonlitfarewell",
        "witness",
        "metroidprime",
        "undertale",
        "monster_sanctuary",
        "ff4fe",
        "terraria",
        "mzm",
        "smw",
        "rac2",
        "mm2",
        "mm_recomp",
        "animal_well",
        "cuphead",
        "jakanddaxter",
        "dk64",
        "cv64",
        "faxanadu",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "sotn",
        "ff1",
        "ladx",
        "ror2",
        "cat_quest",
        "oribf",
        "papermario",
        "tunic",
        "mm3",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "timespinner",
        "ahit",
        "oot",
        "dw1",
        "sm_map_rando",
        "outer_wilds",
        "raft",
        "sms",
        "albw",
        "tp",
        "crosscode",
        "tww",
        "rogue_legacy",
        "kh2",
        "dkc3",
        "smo",
        "stardew_valley",
        "tmc",
        "tloz",
        "shivers",
        "crystal_project",
        "k64",
        "zelda2",
        "v6",
        "metroidfusion",
        "shorthike",
        "kdl3",
        "pokemon_rb",
        "mmx3",
        "xenobladex",
        "pokemon_crystal",
        "banjo_tooie",
        "luigismansion",
        "dredge",
        "ror1",
        "getting_over_it",
        "sm",
        "tloz_oos",
        "ss",
        "messenger",
        "wl4",
        "earthbound",
        "gstla",
        "hcniko",
        "minecraft",
        "sly1",
        "celeste_open_world",
        "tloz_ph",
        "bomb_rush_cyberfunk",
        "hades",
        "satisfactory",
        "subnautica",
        "hk",
        "kh1",
        "dontstarvetogether",
        "sadx",
        "cvcotm",
        "enderlilies",
        "mlss",
        "celeste",
        "sm64ex",
        "lego_star_wars_tcs",
        "sa2b",
        "ffmq"
    ],
    "action": [
        "seaofthieves",
        "sm64hacks",
        "momodoramoonlitfarewell",
        "apeescape",
        "ctjot",
        "metroidprime",
        "wl",
        "monster_sanctuary",
        "ff4fe",
        "terraria",
        "mzm",
        "smw",
        "rac2",
        "mm2",
        "mmbn3",
        "mm_recomp",
        "animal_well",
        "cuphead",
        "jakanddaxter",
        "dk64",
        "cv64",
        "faxanadu",
        "sims4",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "sotn",
        "ff1",
        "ladx",
        "ror2",
        "mk64",
        "cat_quest",
        "swr",
        "oribf",
        "papermario",
        "tunic",
        "mm3",
        "pokemon_emerald",
        "alttp",
        "sonic_heroes",
        "timespinner",
        "ahit",
        "tyrian",
        "oot",
        "dw1",
        "yoshisisland",
        "sm_map_rando",
        "soe",
        "trackmania",
        "outer_wilds",
        "sms",
        "albw",
        "dkc2",
        "tetrisattack",
        "tp",
        "crosscode",
        "tww",
        "doronko_wanko",
        "rogue_legacy",
        "kh2",
        "dkc3",
        "smo",
        "tmc",
        "overcooked2",
        "tloz",
        "star_fox_64",
        "k64",
        "zelda2",
        "v6",
        "metroidfusion",
        "musedash",
        "kdl3",
        "pokemon_rb",
        "mmx3",
        "xenobladex",
        "pokemon_crystal",
        "banjo_tooie",
        "luigismansion",
        "dredge",
        "mario_kart_double_dash",
        "brotato",
        "ror1",
        "getting_over_it",
        "diddy_kong_racing",
        "landstalker",
        "sm",
        "tloz_oos",
        "ss",
        "messenger",
        "dkc",
        "wl4",
        "earthbound",
        "gstla",
        "hcniko",
        "sly1",
        "celeste_open_world",
        "tloz_ph",
        "bomb_rush_cyberfunk",
        "hades",
        "marioland2",
        "hk",
        "kh1",
        "dontstarvetogether",
        "sadx",
        "cvcotm",
        "enderlilies",
        "mlss",
        "celeste",
        "sm64ex",
        "lego_star_wars_tcs",
        "sa2b",
        "ffmq"
    ],
    "playstation 4": [
        "tunic",
        "timespinner",
        "witness",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "trackmania",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "ror1",
        "crosscode",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "kh2",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "cat_quest",
        "swr",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "4": [
        "tunic",
        "timespinner",
        "witness",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "terraria",
        "dw1",
        "bomb_rush_cyberfunk",
        "hades",
        "trackmania",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "ror1",
        "crosscode",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "kh2",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "wl4",
        "cat_quest",
        "swr",
        "sims4",
        "placidplasticducksim",
        "celeste_open_world"
    ],
    "mac": [
        "tunic",
        "crystal_project",
        "timespinner",
        "witness",
        "v6",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "musedash",
        "factorio",
        "shorthike",
        "tyrian",
        "terraria",
        "hades",
        "subnautica",
        "dredge",
        "brotato",
        "hk",
        "ror1",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "rogue_legacy",
        "cuphead",
        "celeste",
        "stardew_valley",
        "lego_star_wars_tcs",
        "overcooked2",
        "minecraft",
        "cat_quest",
        "swr",
        "toontown",
        "sims4",
        "celeste_open_world"
    ],
    "xbox one": [
        "tunic",
        "seaofthieves",
        "timespinner",
        "celeste_open_world",
        "witness",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "trackmania",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "ror1",
        "crosscode",
        "rogue_legacy",
        "cuphead",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "swr",
        "sims4",
        "placidplasticducksim",
        "oribf"
    ],
    "one": [
        "tunic",
        "seaofthieves",
        "timespinner",
        "celeste_open_world",
        "witness",
        "balatro",
        "undertale",
        "ahit",
        "monster_sanctuary",
        "shorthike",
        "wargroove2",
        "terraria",
        "bomb_rush_cyberfunk",
        "hades",
        "trackmania",
        "outer_wilds",
        "subnautica",
        "powerwashsimulator",
        "dredge",
        "brotato",
        "hk",
        "ror1",
        "crosscode",
        "rogue_legacy",
        "cuphead",
        "messenger",
        "enderlilies",
        "wargroove",
        "celeste",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "swr",
        "sims4",
        "placidplasticducksim",
        "oribf"
    ],
    "time travel": [
        "pmd_eos",
        "tloz_oos",
        "apeescape",
        "outer_wilds",
        "mm_recomp",
        "timespinner",
        "earthbound",
        "ctjot",
        "ahit",
        "tloz_ooa",
        "oot"
    ],
    "travel": [
        "pmd_eos",
        "tloz_oos",
        "apeescape",
        "outer_wilds",
        "mm_recomp",
        "timespinner",
        "earthbound",
        "ctjot",
        "ahit",
        "tloz_ooa",
        "oot"
    ],
    "spaceship": [
        "mzm",
        "civ_6",
        "metroidprime",
        "v6",
        "metroidfusion",
        "ahit",
        "star_fox_64"
    ],
    "female protagonist": [
        "enderlilies",
        "sm_map_rando",
        "mzm",
        "celeste",
        "sm",
        "timespinner",
        "earthbound",
        "hcniko",
        "rogue_legacy",
        "metroidprime",
        "dkc2",
        "cv64",
        "ahit",
        "metroidfusion",
        "shorthike",
        "undertale",
        "dkc3",
        "celeste_open_world"
    ],
    "female": [
        "enderlilies",
        "sm_map_rando",
        "mzm",
        "celeste",
        "sm",
        "timespinner",
        "earthbound",
        "hcniko",
        "rogue_legacy",
        "metroidprime",
        "dkc2",
        "cv64",
        "ahit",
        "metroidfusion",
        "shorthike",
        "undertale",
        "dkc3",
        "celeste_open_world"
    ],
    "protagonist": [
        "k64",
        "tloz_ph",
        "pokemon_emerald",
        "timespinner",
        "alttp",
        "zelda2",
        "metroidprime",
        "metroidfusion",
        "undertale",
        "ahit",
        "shorthike",
        "oot",
        "sm_map_rando",
        "mzm",
        "dkc2",
        "hk",
        "sm",
        "tloz_oos",
        "ss",
        "rogue_legacy",
        "jakanddaxter",
        "cv64",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "enderlilies",
        "ladx",
        "mlss",
        "celeste",
        "tmc",
        "earthbound",
        "gstla",
        "hcniko",
        "celeste_open_world",
        "papermario"
    ],
    "action-adventure": [
        "seaofthieves",
        "tloz_ph",
        "timespinner",
        "alttp",
        "zelda2",
        "metroidprime",
        "metroidfusion",
        "ahit",
        "oot",
        "terraria",
        "sm_map_rando",
        "xenobladex",
        "banjo_tooie",
        "luigismansion",
        "sms",
        "albw",
        "kh1",
        "hk",
        "sm",
        "crosscode",
        "landstalker",
        "tloz_oos",
        "dontstarvetogether",
        "mm_recomp",
        "ss",
        "tww",
        "rogue_legacy",
        "cv64",
        "tloz_ooa",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "minecraft"
    ],
    "cute": [
        "tunic",
        "celeste",
        "shorthike",
        "animal_well",
        "hcniko",
        "undertale",
        "ahit",
        "musedash",
        "sims4",
        "celeste_open_world"
    ],
    "snow": [
        "celeste",
        "stardew_valley",
        "diddy_kong_racing",
        "lego_star_wars_tcs",
        "mk64",
        "gstla",
        "hcniko",
        "albw",
        "jakanddaxter",
        "metroidprime",
        "minecraft",
        "ffta",
        "ahit",
        "shorthike",
        "dkc",
        "dkc3",
        "celeste_open_world",
        "terraria"
    ],
    "wall jump": [
        "cvcotm",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "sm",
        "sms",
        "metroidfusion",
        "ahit",
        "smo",
        "oribf"
    ],
    "wall": [
        "metroidfusion",
        "undertale",
        "ahit",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "banjo_tooie",
        "sms",
        "dkc2",
        "sm",
        "rogue_legacy",
        "jakanddaxter",
        "dkc",
        "smo",
        "cvcotm",
        "ladx",
        "mlss",
        "tmc",
        "ffta",
        "oribf",
        "papermario"
    ],
    "jump": [
        "cvcotm",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "sm",
        "sms",
        "metroidfusion",
        "ahit",
        "smo",
        "oribf"
    ],
    "3d platformer": [
        "bomb_rush_cyberfunk",
        "sm64ex",
        "sm64hacks",
        "sonic_heroes",
        "hcniko",
        "sms",
        "ahit",
        "shorthike",
        "smo"
    ],
    "3d": [
        "tunic",
        "crystal_project",
        "sm64hacks",
        "k64",
        "apeescape",
        "tloz_ph",
        "witness",
        "sonic_heroes",
        "metroidprime",
        "ahit",
        "shorthike",
        "oot",
        "dw1",
        "bomb_rush_cyberfunk",
        "xenobladex",
        "luigismansion",
        "sms",
        "albw",
        "powerwashsimulator",
        "dredge",
        "kh1",
        "ss",
        "jakanddaxter",
        "dk64",
        "cv64",
        "smo",
        "spyro3",
        "sotn",
        "sm64ex",
        "lego_star_wars_tcs",
        "mk64",
        "hcniko",
        "minecraft",
        "sly1",
        "star_fox_64"
    ],
    "platformer": [
        "bomb_rush_cyberfunk",
        "sm64ex",
        "sm64hacks",
        "sonic_heroes",
        "hcniko",
        "sms",
        "ahit",
        "shorthike",
        "smo"
    ],
    "swimming": [
        "sm64hacks",
        "alttp",
        "ahit",
        "terraria",
        "oot",
        "banjo_tooie",
        "subnautica",
        "sms",
        "albw",
        "dkc2",
        "kh1",
        "jakanddaxter",
        "tloz_ooa",
        "dkc",
        "smo",
        "dkc3",
        "spyro3",
        "sm64ex",
        "tmc",
        "wl4",
        "hcniko",
        "minecraft"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "ladx",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "tloz",
        "tloz_ooa",
        "tp",
        "oot"
    ],
    "of": [
        "seaofthieves",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "zelda2",
        "oot",
        "soe",
        "pokemon_crystal",
        "luigismansion",
        "sms",
        "albw",
        "dkc2",
        "tp",
        "ror1",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "rogue_legacy",
        "jakanddaxter",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "spyro3",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ladx",
        "pmd_eos",
        "ror2",
        "tmc",
        "lufia2ac",
        "earthbound",
        "sly1",
        "ffta",
        "tloz",
        "star_fox_64",
        "oribf"
    ],
    "zelda:": [
        "ladx",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "tloz_ooa",
        "tp",
        "oot"
    ],
    "link": [
        "albw",
        "alttp",
        "zelda2"
    ],
    "between": [
        "albw"
    ],
    "worlds": [
        "albw"
    ],
    "puzzle": [
        "shivers",
        "tunic",
        "tloz_ph",
        "alttp",
        "witness",
        "v6",
        "metroidfusion",
        "undertale",
        "oot",
        "yugiohddm",
        "outer_wilds",
        "albw",
        "tetrisattack",
        "tp",
        "crosscode",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "animal_well",
        "ss",
        "rogue_legacy",
        "cv64",
        "tloz_ooa",
        "spyro3",
        "ladx",
        "tmc",
        "lufia2ac",
        "wl4",
        "hcniko",
        "placidplasticducksim",
        "oribf"
    ],
    "historical": [
        "fm",
        "soe",
        "civ_6",
        "ss",
        "albw"
    ],
    "sandbox": [
        "smo",
        "stardew_valley",
        "satisfactory",
        "terraria",
        "landstalker",
        "xenobladex",
        "dontstarvetogether",
        "zelda2",
        "sms",
        "albw",
        "minecraft",
        "powerwashsimulator",
        "sims4",
        "faxanadu",
        "factorio",
        "placidplasticducksim",
        "oot"
    ],
    "open world": [
        "seaofthieves",
        "sm64hacks",
        "witness",
        "metroidprime",
        "shorthike",
        "oot",
        "pokemon_rb",
        "terraria",
        "mzm",
        "satisfactory",
        "xenobladex",
        "outer_wilds",
        "subnautica",
        "albw",
        "dredge",
        "dontstarvetogether",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "smo",
        "sotn",
        "sm64ex",
        "gstla",
        "minecraft",
        "tloz",
        "toontown"
    ],
    "open": [
        "seaofthieves",
        "sm64hacks",
        "witness",
        "metroidprime",
        "shorthike",
        "oot",
        "pokemon_rb",
        "terraria",
        "mzm",
        "satisfactory",
        "xenobladex",
        "outer_wilds",
        "subnautica",
        "albw",
        "dredge",
        "dontstarvetogether",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "smo",
        "sotn",
        "sm64ex",
        "gstla",
        "minecraft",
        "tloz",
        "toontown"
    ],
    "world": [
        "seaofthieves",
        "sm64hacks",
        "tloz_ph",
        "alttp",
        "witness",
        "zelda2",
        "metroidprime",
        "v6",
        "yugioh06",
        "shorthike",
        "oot",
        "pokemon_rb",
        "dw1",
        "terraria",
        "yoshisisland",
        "mzm",
        "satisfactory",
        "xenobladex",
        "outer_wilds",
        "pokemon_crystal",
        "subnautica",
        "albw",
        "smw",
        "dredge",
        "dkc2",
        "tloz_oos",
        "dontstarvetogether",
        "mm_recomp",
        "ss",
        "jakanddaxter",
        "dkc",
        "dkc3",
        "smo",
        "sotn",
        "ladx",
        "sm64ex",
        "tmc",
        "earthbound",
        "gstla",
        "minecraft",
        "tloz",
        "toontown"
    ],
    "nintendo 3ds": [
        "tloz_ooa",
        "ff1",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "mm3",
        "wl4",
        "zelda2",
        "albw",
        "v6",
        "metroidfusion",
        "wl",
        "tloz",
        "marioland2",
        "pokemon_rb",
        "mm2"
    ],
    "3ds": [
        "mm3",
        "alttp",
        "zelda2",
        "v6",
        "metroidfusion",
        "wl",
        "terraria",
        "pokemon_rb",
        "mmx3",
        "sm_map_rando",
        "pokemon_crystal",
        "albw",
        "smw",
        "dkc2",
        "marioland2",
        "mm2",
        "sm",
        "tloz_oos",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "ff1",
        "ladx",
        "tmc",
        "wl4",
        "earthbound",
        "tloz"
    ],
    "medieval": [
        "albw",
        "soe",
        "rogue_legacy",
        "ss"
    ],
    "magic": [
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "tloz_oos",
        "alttp",
        "ctjot",
        "gstla",
        "albw",
        "cuphead",
        "rogue_legacy",
        "zelda2",
        "cv64",
        "faxanadu",
        "ffta",
        "terraria"
    ],
    "minigames": [
        "toontown",
        "stardew_valley",
        "k64",
        "apeescape",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "wl4",
        "gstla",
        "hcniko",
        "albw",
        "rogue_legacy",
        "dk64",
        "tloz_ooa",
        "kh1",
        "dkc3",
        "spyro3",
        "oot"
    ],
    "2.5d": [
        "albw",
        "dkc",
        "dkc3",
        "k64"
    ],
    "archery": [
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "minecraft",
        "oot"
    ],
    "fairy": [
        "ladx",
        "stardew_valley",
        "terraria",
        "tmc",
        "k64",
        "landstalker",
        "tloz_oos",
        "mm_recomp",
        "alttp",
        "tloz_ph",
        "tww",
        "zelda2",
        "albw",
        "dk64",
        "tloz",
        "tloz_ooa",
        "oot"
    ],
    "princess": [
        "ladx",
        "mlss",
        "tmc",
        "tloz_oos",
        "lego_star_wars_tcs",
        "tloz_ph",
        "mk64",
        "alttp",
        "ss",
        "albw",
        "smw",
        "tloz_ooa",
        "kh1",
        "tp",
        "oot",
        "papermario"
    ],
    "sequel": [
        "mm3",
        "alttp",
        "zelda2",
        "oot",
        "dw1",
        "mmx3",
        "banjo_tooie",
        "sms",
        "albw",
        "dkc2",
        "mm2",
        "civ_6",
        "dontstarvetogether",
        "mm_recomp",
        "smo",
        "mk64",
        "wl4",
        "gstla",
        "ffta"
    ],
    "sword & sorcery": [
        "ffmq",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "albw",
        "tloz_ooa",
        "kh1",
        "spyro3",
        "oot"
    ],
    "sword": [
        "ffmq",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "albw",
        "tloz_ooa",
        "kh1",
        "spyro3",
        "oot"
    ],
    "&": [
        "fm",
        "balatro",
        "yugioh06",
        "terraria",
        "oot",
        "yugiohddm",
        "albw",
        "rac2",
        "kh1",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "tloz_ooa",
        "spyro3",
        "ladx",
        "mlss",
        "tmc",
        "ffmq"
    ],
    "sorcery": [
        "ffmq",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tww",
        "mm_recomp",
        "ss",
        "albw",
        "tloz_ooa",
        "kh1",
        "spyro3",
        "oot"
    ],
    "darkness": [
        "ladx",
        "sm_map_rando",
        "sm",
        "tmc",
        "mm3",
        "alttp",
        "witness",
        "earthbound",
        "luigismansion",
        "albw",
        "minecraft",
        "rogue_legacy",
        "zelda2",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "terraria"
    ],
    "digital distribution": [
        "tunic",
        "seaofthieves",
        "sm64hacks",
        "apeescape",
        "timespinner",
        "witness",
        "v6",
        "musedash",
        "factorio",
        "oot",
        "terraria",
        "yoshisisland",
        "banjo_tooie",
        "albw",
        "smw",
        "dredge",
        "dkc2",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "tloz_oos",
        "dontstarvetogether",
        "rogue_legacy",
        "cuphead",
        "dk64",
        "oribf",
        "dkc",
        "sotn",
        "ladx",
        "mlss",
        "celeste",
        "sm64ex",
        "tmc",
        "wl4",
        "minecraft",
        "celeste_open_world"
    ],
    "digital": [
        "tunic",
        "seaofthieves",
        "sm64hacks",
        "apeescape",
        "timespinner",
        "witness",
        "v6",
        "musedash",
        "factorio",
        "oot",
        "terraria",
        "yoshisisland",
        "banjo_tooie",
        "albw",
        "smw",
        "dredge",
        "dkc2",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "tloz_oos",
        "dontstarvetogether",
        "rogue_legacy",
        "cuphead",
        "dk64",
        "oribf",
        "dkc",
        "sotn",
        "ladx",
        "mlss",
        "celeste",
        "sm64ex",
        "tmc",
        "wl4",
        "minecraft",
        "celeste_open_world"
    ],
    "distribution": [
        "tunic",
        "seaofthieves",
        "sm64hacks",
        "apeescape",
        "timespinner",
        "witness",
        "v6",
        "musedash",
        "factorio",
        "oot",
        "terraria",
        "yoshisisland",
        "banjo_tooie",
        "albw",
        "smw",
        "dredge",
        "dkc2",
        "getting_over_it",
        "civ_6",
        "crosscode",
        "tloz_oos",
        "dontstarvetogether",
        "rogue_legacy",
        "cuphead",
        "dk64",
        "oribf",
        "dkc",
        "sotn",
        "ladx",
        "mlss",
        "celeste",
        "sm64ex",
        "tmc",
        "wl4",
        "minecraft",
        "celeste_open_world"
    ],
    "anthropomorphism": [
        "tunic",
        "k64",
        "apeescape",
        "sonic_heroes",
        "undertale",
        "shorthike",
        "banjo_tooie",
        "sms",
        "albw",
        "dkc2",
        "kh1",
        "diddy_kong_racing",
        "tloz_oos",
        "cuphead",
        "jakanddaxter",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "spyro3",
        "mlss",
        "tmc",
        "mk64",
        "hcniko",
        "sly1",
        "star_fox_64",
        "papermario"
    ],
    "polygonal 3d": [
        "k64",
        "apeescape",
        "tloz_ph",
        "witness",
        "metroidprime",
        "oot",
        "dw1",
        "xenobladex",
        "luigismansion",
        "sms",
        "albw",
        "kh1",
        "ss",
        "jakanddaxter",
        "dk64",
        "cv64",
        "spyro3",
        "sotn",
        "lego_star_wars_tcs",
        "mk64",
        "minecraft",
        "sly1",
        "star_fox_64"
    ],
    "polygonal": [
        "k64",
        "apeescape",
        "tloz_ph",
        "witness",
        "metroidprime",
        "oot",
        "dw1",
        "xenobladex",
        "luigismansion",
        "sms",
        "albw",
        "kh1",
        "ss",
        "jakanddaxter",
        "dk64",
        "cv64",
        "spyro3",
        "sotn",
        "lego_star_wars_tcs",
        "mk64",
        "minecraft",
        "sly1",
        "star_fox_64"
    ],
    "bow and arrow": [
        "ror1",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "cuphead",
        "minecraft",
        "rogue_legacy",
        "ffta",
        "oot"
    ],
    "bow": [
        "ror1",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "cuphead",
        "minecraft",
        "rogue_legacy",
        "ffta",
        "oot"
    ],
    "and": [
        "tloz_ph",
        "alttp",
        "terraria",
        "oot",
        "hades",
        "albw",
        "ror1",
        "civ_6",
        "tloz_oos",
        "ss",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "cv64",
        "ladx",
        "tmc",
        "minecraft",
        "sly1",
        "ffta",
        "oribf"
    ],
    "arrow": [
        "ror1",
        "ladx",
        "terraria",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "cuphead",
        "minecraft",
        "rogue_legacy",
        "ffta",
        "oot"
    ],
    "damsel in distress": [
        "sm_map_rando",
        "sm",
        "tloz_oos",
        "tloz_ph",
        "tmc",
        "alttp",
        "ss",
        "earthbound",
        "sms",
        "albw",
        "metroidprime",
        "smw",
        "zelda2",
        "tloz_ooa",
        "kh1",
        "oot",
        "papermario"
    ],
    "damsel": [
        "sm_map_rando",
        "sm",
        "tloz_oos",
        "tloz_ph",
        "tmc",
        "alttp",
        "ss",
        "earthbound",
        "sms",
        "albw",
        "metroidprime",
        "smw",
        "zelda2",
        "tloz_ooa",
        "kh1",
        "oot",
        "papermario"
    ],
    "distress": [
        "sm_map_rando",
        "sm",
        "tloz_oos",
        "tloz_ph",
        "tmc",
        "alttp",
        "ss",
        "earthbound",
        "sms",
        "albw",
        "metroidprime",
        "smw",
        "zelda2",
        "tloz_ooa",
        "kh1",
        "oot",
        "papermario"
    ],
    "upgradeable weapons": [
        "mmx3",
        "mzm",
        "tmc",
        "albw",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "cv64",
        "mm2"
    ],
    "upgradeable": [
        "mmx3",
        "mzm",
        "tmc",
        "albw",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "cv64",
        "mm2"
    ],
    "weapons": [
        "mmx3",
        "mzm",
        "tmc",
        "albw",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "cv64",
        "mm2"
    ],
    "disorientation zone": [
        "ladx",
        "tmc",
        "tloz_oos",
        "alttp",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "disorientation": [
        "ladx",
        "tmc",
        "tloz_oos",
        "alttp",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "zone": [
        "ladx",
        "tmc",
        "tloz_oos",
        "alttp",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "descendants of other characters": [
        "sotn",
        "tmc",
        "mm_recomp",
        "earthbound",
        "luigismansion",
        "albw",
        "jakanddaxter",
        "rogue_legacy",
        "dk64",
        "cv64",
        "dkc2",
        "sly1",
        "sms",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "oot",
        "star_fox_64"
    ],
    "descendants": [
        "sotn",
        "tmc",
        "mm_recomp",
        "earthbound",
        "luigismansion",
        "albw",
        "jakanddaxter",
        "rogue_legacy",
        "dk64",
        "cv64",
        "dkc2",
        "sly1",
        "sms",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "oot",
        "star_fox_64"
    ],
    "other": [
        "sotn",
        "tmc",
        "mm_recomp",
        "earthbound",
        "luigismansion",
        "albw",
        "jakanddaxter",
        "rogue_legacy",
        "dk64",
        "cv64",
        "dkc2",
        "sly1",
        "sms",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "oot",
        "star_fox_64"
    ],
    "characters": [
        "terraria",
        "oot",
        "xenobladex",
        "luigismansion",
        "sms",
        "albw",
        "dkc2",
        "mm_recomp",
        "rogue_legacy",
        "jakanddaxter",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "sotn",
        "stardew_valley",
        "tmc",
        "lego_star_wars_tcs",
        "earthbound",
        "sly1",
        "star_fox_64"
    ],
    "save point": [
        "metroidprime",
        "v6",
        "metroidfusion",
        "sm_map_rando",
        "mzm",
        "luigismansion",
        "albw",
        "dkc2",
        "kh1",
        "sm",
        "jakanddaxter",
        "cv64",
        "faxanadu",
        "dkc",
        "dkc3",
        "cvcotm",
        "sotn",
        "mlss",
        "earthbound",
        "gstla",
        "papermario"
    ],
    "save": [
        "metroidprime",
        "v6",
        "metroidfusion",
        "sm_map_rando",
        "mzm",
        "luigismansion",
        "albw",
        "dkc2",
        "kh1",
        "sm",
        "jakanddaxter",
        "cv64",
        "faxanadu",
        "dkc",
        "dkc3",
        "cvcotm",
        "sotn",
        "mlss",
        "earthbound",
        "gstla",
        "papermario"
    ],
    "point": [
        "metroidprime",
        "v6",
        "metroidfusion",
        "sm_map_rando",
        "mzm",
        "luigismansion",
        "albw",
        "dkc2",
        "kh1",
        "sm",
        "jakanddaxter",
        "cv64",
        "faxanadu",
        "dkc",
        "dkc3",
        "cvcotm",
        "sotn",
        "mlss",
        "earthbound",
        "gstla",
        "papermario"
    ],
    "side quests": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "xenobladex",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "side": [
        "k64",
        "momodoramoonlitfarewell",
        "mm3",
        "pokemon_emerald",
        "alttp",
        "timespinner",
        "tloz_ph",
        "zelda2",
        "v6",
        "metroidfusion",
        "wl",
        "monster_sanctuary",
        "ff4fe",
        "musedash",
        "wargroove2",
        "kdl3",
        "oot",
        "pokemon_rb",
        "terraria",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "xenobladex",
        "pokemon_crystal",
        "albw",
        "smw",
        "dkc2",
        "marioland2",
        "hk",
        "tetrisattack",
        "mm2",
        "ror1",
        "getting_over_it",
        "sm",
        "tloz_oos",
        "megamix",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "faxanadu",
        "oribf",
        "messenger",
        "tloz_ooa",
        "dkc",
        "dkc3",
        "pokemon_frlg",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ff1",
        "ladx",
        "mlss",
        "celeste",
        "wargroove",
        "tmc",
        "lufia2ac",
        "wl4",
        "ffmq",
        "celeste_open_world",
        "papermario"
    ],
    "quests": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "xenobladex",
        "zelda2",
        "albw",
        "metroidprime",
        "tloz_ooa",
        "oot"
    ],
    "potion": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "ss",
        "gstla",
        "zelda2",
        "albw",
        "minecraft",
        "rogue_legacy",
        "kh1"
    ],
    "real-time combat": [
        "sm64hacks",
        "tloz_ph",
        "alttp",
        "zelda2",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "xenobladex",
        "sms",
        "albw",
        "kh1",
        "sm",
        "landstalker",
        "tloz_oos",
        "ss",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "spyro3",
        "sotn",
        "ladx",
        "sm64ex",
        "tmc",
        "minecraft"
    ],
    "real-time": [
        "sm64hacks",
        "tloz_ph",
        "alttp",
        "zelda2",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "xenobladex",
        "sms",
        "albw",
        "kh1",
        "sm",
        "landstalker",
        "tloz_oos",
        "ss",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "spyro3",
        "sotn",
        "ladx",
        "sm64ex",
        "tmc",
        "minecraft"
    ],
    "combat": [
        "sm64hacks",
        "tloz_ph",
        "alttp",
        "zelda2",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "xenobladex",
        "sms",
        "albw",
        "kh1",
        "sm",
        "landstalker",
        "tloz_oos",
        "ss",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "spyro3",
        "sotn",
        "ladx",
        "sm64ex",
        "tmc",
        "minecraft"
    ],
    "self-referential humor": [
        "mlss",
        "earthbound",
        "albw",
        "metroidfusion",
        "dkc2",
        "papermario"
    ],
    "self-referential": [
        "mlss",
        "earthbound",
        "albw",
        "metroidfusion",
        "dkc2",
        "papermario"
    ],
    "humor": [
        "mlss",
        "earthbound",
        "albw",
        "metroidfusion",
        "dkc2",
        "papermario"
    ],
    "rpg elements": [
        "sotn",
        "mlss",
        "mzm",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "zelda2",
        "albw",
        "minecraft",
        "metroidfusion",
        "oribf"
    ],
    "rpg": [
        "sotn",
        "mlss",
        "mzm",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "zelda2",
        "albw",
        "minecraft",
        "metroidfusion",
        "oribf"
    ],
    "elements": [
        "sotn",
        "mlss",
        "mzm",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "zelda2",
        "albw",
        "minecraft",
        "metroidfusion",
        "oribf"
    ],
    "mercenary": [
        "sm_map_rando",
        "sm",
        "alttp",
        "ss",
        "albw",
        "metroidprime",
        "oot"
    ],
    "coming of age": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "albw",
        "jakanddaxter",
        "ffta",
        "oribf",
        "oot"
    ],
    "coming": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "albw",
        "jakanddaxter",
        "ffta",
        "oribf",
        "oot"
    ],
    "age": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "gstla",
        "albw",
        "jakanddaxter",
        "ffta",
        "oribf",
        "oot"
    ],
    "androgyny": [
        "sotn",
        "ss",
        "gstla",
        "albw",
        "ffta",
        "oot"
    ],
    "fast traveling": [
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "albw",
        "undertale",
        "hk",
        "oot"
    ],
    "fast": [
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "albw",
        "undertale",
        "hk",
        "oot"
    ],
    "traveling": [
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "alttp",
        "albw",
        "undertale",
        "hk",
        "oot"
    ],
    "context sensitive": [
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "context": [
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "sensitive": [
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "albw",
        "tloz_ooa",
        "oot"
    ],
    "living inventory": [
        "tmc",
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "oot"
    ],
    "living": [
        "tmc",
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "oot"
    ],
    "inventory": [
        "tmc",
        "tww",
        "mm_recomp",
        "alttp",
        "ss",
        "albw",
        "oot"
    ],
    "bees": [
        "tloz_ph",
        "raft",
        "dontstarvetogether",
        "alttp",
        "albw",
        "minecraft",
        "terraria"
    ],
    "a link to the past": [
        "alttp"
    ],
    "the legend of zelda: a link to the past": [
        "alttp"
    ],
    "to": [
        "alttp"
    ],
    "past": [
        "alttp"
    ],
    "satellaview": [
        "yoshisisland",
        "alttp"
    ],
    "super nintendo entertainment system": [
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "soe",
        "sm",
        "lufia2ac",
        "alttp",
        "earthbound",
        "smw",
        "dkc2",
        "ff4fe",
        "ffmq",
        "dkc",
        "dkc3",
        "tetrisattack",
        "kdl3"
    ],
    "super": [
        "sm64hacks",
        "alttp",
        "wl",
        "ff4fe",
        "kdl3",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "soe",
        "sms",
        "smw",
        "dkc2",
        "marioland2",
        "tetrisattack",
        "sm",
        "dkc",
        "smo",
        "dkc3",
        "sm64ex",
        "lufia2ac",
        "earthbound",
        "ffmq"
    ],
    "entertainment": [
        "mm3",
        "alttp",
        "zelda2",
        "ff4fe",
        "kdl3",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "soe",
        "smw",
        "dkc2",
        "tetrisattack",
        "sm",
        "faxanadu",
        "dkc",
        "dkc3",
        "ff1",
        "lufia2ac",
        "earthbound",
        "tloz",
        "ffmq"
    ],
    "system": [
        "mm3",
        "pokemon_emerald",
        "alttp",
        "zelda2",
        "ff4fe",
        "kdl3",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "soe",
        "xenobladex",
        "pokemon_crystal",
        "smw",
        "dkc2",
        "kh1",
        "tetrisattack",
        "sm",
        "faxanadu",
        "dkc",
        "dkc3",
        "ff1",
        "mlss",
        "lufia2ac",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "papermario"
    ],
    "wii": [
        "sm64hacks",
        "k64",
        "tloz_ph",
        "mm3",
        "alttp",
        "zelda2",
        "metroidfusion",
        "ff4fe",
        "kdl3",
        "oot",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "xenobladex",
        "smw",
        "dkc2",
        "hk",
        "tp",
        "sm",
        "landstalker",
        "mm_recomp",
        "ss",
        "dk64",
        "faxanadu",
        "dkc",
        "dkc3",
        "cvcotm",
        "ff1",
        "mlss",
        "pmd_eos",
        "sm64ex",
        "stardew_valley",
        "tmc",
        "lego_star_wars_tcs",
        "mk64",
        "wl4",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "star_fox_64",
        "papermario"
    ],
    "wii u": [
        "sm64hacks",
        "k64",
        "tloz_ph",
        "mm3",
        "alttp",
        "zelda2",
        "metroidfusion",
        "kdl3",
        "oot",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "xenobladex",
        "smw",
        "dkc2",
        "hk",
        "sm",
        "mm_recomp",
        "ss",
        "dk64",
        "dkc",
        "dkc3",
        "cvcotm",
        "ff1",
        "mlss",
        "pmd_eos",
        "sm64ex",
        "stardew_valley",
        "tmc",
        "mk64",
        "wl4",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "star_fox_64",
        "papermario"
    ],
    "u": [
        "sm64hacks",
        "k64",
        "tloz_ph",
        "mm3",
        "alttp",
        "zelda2",
        "metroidfusion",
        "kdl3",
        "oot",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "xenobladex",
        "smw",
        "dkc2",
        "hk",
        "sm",
        "mm_recomp",
        "ss",
        "dk64",
        "dkc",
        "dkc3",
        "cvcotm",
        "ff1",
        "mlss",
        "pmd_eos",
        "sm64ex",
        "stardew_valley",
        "tmc",
        "mk64",
        "wl4",
        "earthbound",
        "gstla",
        "ffta",
        "tloz",
        "ffmq",
        "star_fox_64",
        "papermario"
    ],
    "new nintendo 3ds": [
        "mmx3",
        "sm_map_rando",
        "sm",
        "alttp",
        "earthbound",
        "smw",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "new": [
        "mmx3",
        "sm_map_rando",
        "sm",
        "alttp",
        "earthbound",
        "smw",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "super famicom": [
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "sm",
        "lufia2ac",
        "alttp",
        "earthbound",
        "smw",
        "dkc2",
        "ffmq",
        "dkc",
        "dkc3",
        "kdl3"
    ],
    "famicom": [
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "sm",
        "lufia2ac",
        "alttp",
        "earthbound",
        "smw",
        "dkc2",
        "ffmq",
        "dkc",
        "dkc3",
        "kdl3"
    ],
    "ghosts": [
        "alttp",
        "metroidprime",
        "v6",
        "luigismansion",
        "sms",
        "dkc2",
        "rogue_legacy",
        "cuphead",
        "cv64",
        "tloz_ooa",
        "sotn",
        "mlss",
        "tmc",
        "lego_star_wars_tcs",
        "wl4",
        "earthbound",
        "sly1",
        "ffmq",
        "papermario"
    ],
    "mascot": [
        "ladx",
        "tmc",
        "k64",
        "tloz_oos",
        "mm3",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "sly1",
        "papermario",
        "spyro3",
        "kdl3",
        "mm2"
    ],
    "death": [
        "tloz_ph",
        "mm3",
        "alttp",
        "zelda2",
        "metroidprime",
        "v6",
        "metroidfusion",
        "oot",
        "terraria",
        "mmx3",
        "mzm",
        "luigismansion",
        "sms",
        "kh1",
        "mm2",
        "tloz_oos",
        "rogue_legacy",
        "dk64",
        "cv64",
        "tloz_ooa",
        "dkc",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "gstla",
        "minecraft",
        "sly1",
        "ffta",
        "star_fox_64",
        "papermario"
    ],
    "maze": [
        "ladx",
        "mzm",
        "tmc",
        "alttp",
        "witness",
        "cv64",
        "papermario"
    ],
    "backtracking": [
        "tloz_ph",
        "alttp",
        "witness",
        "metroidprime",
        "metroidfusion",
        "undertale",
        "oot",
        "mzm",
        "banjo_tooie",
        "kh1",
        "tloz_oos",
        "jakanddaxter",
        "cv64",
        "faxanadu",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "ffta"
    ],
    "undead": [
        "sotn",
        "ladx",
        "mlss",
        "terraria",
        "tmc",
        "tloz_oos",
        "alttp",
        "cv64",
        "tloz_ooa",
        "ffmq",
        "oot",
        "papermario"
    ],
    "campaign": [
        "ladx",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "ss",
        "zelda2",
        "tloz_ooa",
        "oot"
    ],
    "pixel art": [
        "mm3",
        "timespinner",
        "alttp",
        "zelda2",
        "v6",
        "metroidfusion",
        "undertale",
        "tyrian",
        "terraria",
        "sm_map_rando",
        "mzm",
        "mm2",
        "ror1",
        "sm",
        "crosscode",
        "tloz_oos",
        "animal_well",
        "rogue_legacy",
        "sotn",
        "ladx",
        "wargroove",
        "celeste",
        "stardew_valley",
        "tmc",
        "wl4",
        "hcniko",
        "celeste_open_world"
    ],
    "pixel": [
        "mm3",
        "timespinner",
        "alttp",
        "zelda2",
        "v6",
        "metroidfusion",
        "undertale",
        "tyrian",
        "terraria",
        "sm_map_rando",
        "mzm",
        "mm2",
        "ror1",
        "sm",
        "crosscode",
        "tloz_oos",
        "animal_well",
        "rogue_legacy",
        "sotn",
        "ladx",
        "wargroove",
        "celeste",
        "stardew_valley",
        "tmc",
        "wl4",
        "hcniko",
        "celeste_open_world"
    ],
    "art": [
        "mm3",
        "timespinner",
        "alttp",
        "zelda2",
        "v6",
        "metroidfusion",
        "undertale",
        "tyrian",
        "terraria",
        "sm_map_rando",
        "mzm",
        "mm2",
        "ror1",
        "sm",
        "crosscode",
        "tloz_oos",
        "animal_well",
        "rogue_legacy",
        "sotn",
        "ladx",
        "wargroove",
        "celeste",
        "stardew_valley",
        "tmc",
        "wl4",
        "hcniko",
        "celeste_open_world"
    ],
    "easter egg": [
        "ladx",
        "apeescape",
        "banjo_tooie",
        "alttp",
        "rogue_legacy",
        "metroidfusion",
        "papermario"
    ],
    "easter": [
        "ladx",
        "apeescape",
        "banjo_tooie",
        "alttp",
        "rogue_legacy",
        "metroidfusion",
        "papermario"
    ],
    "egg": [
        "ladx",
        "apeescape",
        "banjo_tooie",
        "alttp",
        "rogue_legacy",
        "metroidfusion",
        "papermario"
    ],
    "teleportation": [
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "earthbound",
        "rogue_legacy",
        "jakanddaxter",
        "v6",
        "cv64",
        "terraria"
    ],
    "giant insects": [
        "soe",
        "mlss",
        "pokemon_emerald",
        "alttp",
        "sms",
        "dk64",
        "dkc2",
        "hk",
        "dkc",
        "dkc3"
    ],
    "giant": [
        "soe",
        "mlss",
        "pokemon_emerald",
        "alttp",
        "sms",
        "dk64",
        "dkc2",
        "hk",
        "dkc",
        "dkc3"
    ],
    "insects": [
        "soe",
        "mlss",
        "pokemon_emerald",
        "alttp",
        "sms",
        "dk64",
        "dkc2",
        "hk",
        "dkc",
        "dkc3"
    ],
    "silent protagonist": [
        "ladx",
        "mlss",
        "tmc",
        "k64",
        "tloz_oos",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "ss",
        "gstla",
        "zelda2",
        "jakanddaxter",
        "dkc2",
        "tloz_ooa",
        "hk",
        "dkc",
        "oot",
        "papermario"
    ],
    "silent": [
        "ladx",
        "mlss",
        "tmc",
        "k64",
        "tloz_oos",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "ss",
        "gstla",
        "zelda2",
        "jakanddaxter",
        "dkc2",
        "tloz_ooa",
        "hk",
        "dkc",
        "oot",
        "papermario"
    ],
    "explosion": [
        "mm3",
        "alttp",
        "sonic_heroes",
        "zelda2",
        "metroidprime",
        "metroidfusion",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "sms",
        "dkc2",
        "mm2",
        "sm",
        "rogue_legacy",
        "cuphead",
        "cv64",
        "tloz_ooa",
        "dkc3",
        "sotn",
        "tmc",
        "lego_star_wars_tcs",
        "mk64",
        "minecraft",
        "ffta",
        "ffmq"
    ],
    "monkey": [
        "ladx",
        "diddy_kong_racing",
        "apeescape",
        "mk64",
        "alttp",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "nintendo power": [
        "sm_map_rando",
        "sm",
        "alttp",
        "earthbound",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "power": [
        "sm_map_rando",
        "sm",
        "alttp",
        "earthbound",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "world map": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "metroidprime",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "oot"
    ],
    "map": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "metroidprime",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "oot"
    ],
    "human": [
        "sotn",
        "ladx",
        "apeescape",
        "tloz_ph",
        "alttp",
        "ss",
        "gstla",
        "sms",
        "zelda2",
        "cv64",
        "metroidfusion",
        "terraria",
        "papermario"
    ],
    "shopping": [
        "dw1",
        "sotn",
        "mlss",
        "tmc",
        "tloz_oos",
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "tloz_ph",
        "yugiohddm",
        "cuphead",
        "cv64",
        "tloz_ooa"
    ],
    "ice stage": [
        "terraria",
        "tmc",
        "banjo_tooie",
        "mk64",
        "alttp",
        "wl4",
        "jakanddaxter",
        "metroidprime",
        "cv64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "oot"
    ],
    "ice": [
        "terraria",
        "tmc",
        "banjo_tooie",
        "mk64",
        "alttp",
        "wl4",
        "jakanddaxter",
        "metroidprime",
        "cv64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "oot"
    ],
    "stage": [
        "terraria",
        "tmc",
        "banjo_tooie",
        "mk64",
        "alttp",
        "sonic_heroes",
        "wl4",
        "jakanddaxter",
        "metroidprime",
        "smw",
        "cv64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "spyro3",
        "oot"
    ],
    "saving the world": [
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "earthbound"
    ],
    "saving": [
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "earthbound"
    ],
    "grapple": [
        "tmc",
        "lego_star_wars_tcs",
        "tloz_ph",
        "alttp",
        "metroidprime",
        "oot"
    ],
    "secret area": [
        "tunic",
        "sotn",
        "sm_map_rando",
        "diddy_kong_racing",
        "sm",
        "tloz_oos",
        "tmc",
        "alttp",
        "witness",
        "hcniko",
        "zelda2",
        "rogue_legacy",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "secret": [
        "tunic",
        "sotn",
        "sm_map_rando",
        "soe",
        "diddy_kong_racing",
        "sm",
        "tloz_oos",
        "tmc",
        "alttp",
        "witness",
        "hcniko",
        "zelda2",
        "rogue_legacy",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "area": [
        "tunic",
        "sotn",
        "sm_map_rando",
        "diddy_kong_racing",
        "sm",
        "tloz_oos",
        "tmc",
        "alttp",
        "witness",
        "hcniko",
        "zelda2",
        "rogue_legacy",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "shielded enemies": [
        "tmc",
        "alttp",
        "rogue_legacy",
        "tloz_ooa",
        "hk",
        "dkc3"
    ],
    "shielded": [
        "tmc",
        "alttp",
        "rogue_legacy",
        "tloz_ooa",
        "hk",
        "dkc3"
    ],
    "enemies": [
        "tmc",
        "alttp",
        "rogue_legacy",
        "tloz_ooa",
        "hk",
        "dkc3"
    ],
    "walking through walls": [
        "ladx",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "oot"
    ],
    "walking": [
        "ladx",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "oot"
    ],
    "through": [
        "ladx",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "oot"
    ],
    "walls": [
        "ladx",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "oot"
    ],
    "villain": [
        "cvcotm",
        "sotn",
        "tmc",
        "tloz_oos",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "mm3",
        "alttp",
        "zelda2",
        "metroidfusion",
        "papermario",
        "tloz_ooa",
        "kh1",
        "star_fox_64",
        "oot",
        "mm2"
    ],
    "recurring boss": [
        "banjo_tooie",
        "mm3",
        "alttp",
        "pokemon_emerald",
        "dk64",
        "dkc2",
        "metroidfusion",
        "kh1",
        "dkc",
        "dkc3",
        "papermario"
    ],
    "recurring": [
        "banjo_tooie",
        "mm3",
        "alttp",
        "pokemon_emerald",
        "dk64",
        "dkc2",
        "metroidfusion",
        "kh1",
        "dkc",
        "dkc3",
        "papermario"
    ],
    "boss": [
        "tloz_ph",
        "mm3",
        "pokemon_emerald",
        "alttp",
        "metroidprime",
        "metroidfusion",
        "oot",
        "banjo_tooie",
        "sms",
        "dkc2",
        "kh1",
        "mm_recomp",
        "rogue_legacy",
        "cuphead",
        "dk64",
        "dkc",
        "dkc3",
        "tmc",
        "papermario"
    ],
    "been here before": [
        "tmc",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "gstla",
        "sms",
        "ffta",
        "oot"
    ],
    "been": [
        "tmc",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "gstla",
        "sms",
        "ffta",
        "oot"
    ],
    "here": [
        "tmc",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "hcniko",
        "gstla",
        "sms",
        "ffta",
        "oot"
    ],
    "before": [
        "tmc",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "gstla",
        "sms",
        "ffta",
        "oot"
    ],
    "sleeping": [
        "tmc",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "sms",
        "minecraft",
        "papermario"
    ],
    "merchants": [
        "yugiohddm",
        "timespinner",
        "alttp",
        "faxanadu",
        "hk",
        "terraria"
    ],
    "fetch quests": [
        "ladx",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "zelda2",
        "metroidprime"
    ],
    "fetch": [
        "ladx",
        "tmc",
        "tloz_oos",
        "tloz_ph",
        "alttp",
        "zelda2",
        "metroidprime"
    ],
    "poisoning": [
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "minecraft",
        "cv64",
        "papermario"
    ],
    "status effects": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "earthbound",
        "zelda2",
        "minecraft",
        "tloz_ooa"
    ],
    "status": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "earthbound",
        "zelda2",
        "minecraft",
        "tloz_ooa"
    ],
    "effects": [
        "ladx",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "alttp",
        "earthbound",
        "zelda2",
        "minecraft",
        "tloz_ooa"
    ],
    "damage over time": [
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "ffta",
        "oot"
    ],
    "damage": [
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "ffta",
        "oot"
    ],
    "over": [
        "getting_over_it",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "pokemon_emerald",
        "tloz_ph",
        "alttp",
        "jakanddaxter",
        "ffta",
        "oot"
    ],
    "monomyth": [
        "tmc",
        "tloz_ph",
        "mm3",
        "alttp",
        "ss",
        "zelda2",
        "mm2"
    ],
    "retroachievements": [
        "sm64hacks",
        "k64",
        "alttp",
        "sonic_heroes",
        "metroidprime",
        "ff4fe",
        "oot",
        "kdl3",
        "mmx3",
        "banjo_tooie",
        "sms",
        "smw",
        "dkc2",
        "tetrisattack",
        "diddy_kong_racing",
        "tww",
        "mm_recomp",
        "dk64",
        "cv64",
        "dkc",
        "dkc3",
        "pmd_eos",
        "sm64ex",
        "lufia2ac",
        "mk64",
        "earthbound",
        "swr",
        "tloz",
        "ffmq",
        "star_fox_64",
        "papermario"
    ],
    "animal well": [
        "animal_well"
    ],
    "animal": [
        "animal_well"
    ],
    "well": [
        "animal_well"
    ],
    "side view": [
        "k64",
        "momodoramoonlitfarewell",
        "mm3",
        "pokemon_emerald",
        "timespinner",
        "zelda2",
        "v6",
        "metroidfusion",
        "wl",
        "monster_sanctuary",
        "ff4fe",
        "musedash",
        "wargroove2",
        "kdl3",
        "pokemon_rb",
        "terraria",
        "yoshisisland",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "pokemon_crystal",
        "smw",
        "dkc2",
        "marioland2",
        "hk",
        "tetrisattack",
        "mm2",
        "ror1",
        "getting_over_it",
        "sm",
        "megamix",
        "animal_well",
        "rogue_legacy",
        "cuphead",
        "faxanadu",
        "oribf",
        "messenger",
        "dkc",
        "dkc3",
        "pokemon_frlg",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ff1",
        "ladx",
        "mlss",
        "celeste",
        "wargroove",
        "lufia2ac",
        "wl4",
        "ffmq",
        "celeste_open_world",
        "papermario"
    ],
    "horror": [
        "cvcotm",
        "shivers",
        "sotn",
        "getting_over_it",
        "dontstarvetogether",
        "mm_recomp",
        "animal_well",
        "luigismansion",
        "dredge",
        "cv64",
        "undertale",
        "terraria"
    ],
    "survival": [
        "ror1",
        "ror2",
        "raft",
        "dontstarvetogether",
        "subnautica",
        "animal_well",
        "minecraft",
        "yugioh06",
        "factorio",
        "terraria"
    ],
    "mystery": [
        "pmd_eos",
        "crystal_project",
        "outer_wilds",
        "witness",
        "animal_well",
        "dredge"
    ],
    "exploration": [
        "tunic",
        "seaofthieves",
        "tloz_ph",
        "pokemon_emerald",
        "witness",
        "metroidprime",
        "v6",
        "metroidfusion",
        "shorthike",
        "terraria",
        "sm_map_rando",
        "outer_wilds",
        "pokemon_crystal",
        "subnautica",
        "dredge",
        "sm",
        "animal_well",
        "rogue_legacy",
        "jakanddaxter",
        "cv64",
        "celeste",
        "hcniko",
        "celeste_open_world"
    ],
    "retro": [
        "celeste",
        "stardew_valley",
        "timespinner",
        "animal_well",
        "minecraft",
        "cuphead",
        "v6",
        "undertale",
        "messenger",
        "smo",
        "celeste_open_world",
        "terraria"
    ],
    "2d": [
        "sotn",
        "sm_map_rando",
        "celeste",
        "stardew_valley",
        "sm",
        "dontstarvetogether",
        "animal_well",
        "earthbound",
        "zelda2",
        "cuphead",
        "v6",
        "undertale",
        "messenger",
        "musedash",
        "hk",
        "celeste_open_world",
        "terraria"
    ],
    "metroidvania": [
        "crystal_project",
        "momodoramoonlitfarewell",
        "timespinner",
        "zelda2",
        "metroidprime",
        "v6",
        "metroidfusion",
        "monster_sanctuary",
        "sm_map_rando",
        "mzm",
        "hk",
        "sm",
        "animal_well",
        "rogue_legacy",
        "faxanadu",
        "messenger",
        "cvcotm",
        "enderlilies",
        "sotn",
        "oribf"
    ],
    "atmospheric": [
        "tunic",
        "crystal_project",
        "celeste",
        "dontstarvetogether",
        "animal_well",
        "powerwashsimulator",
        "shorthike",
        "hk",
        "celeste_open_world"
    ],
    "relaxing": [
        "stardew_valley",
        "animal_well",
        "hcniko",
        "powerwashsimulator",
        "shorthike",
        "sims4"
    ],
    "controller support": [
        "tunic",
        "stardew_valley",
        "animal_well",
        "hcniko",
        "v6",
        "shorthike",
        "hk"
    ],
    "controller": [
        "tunic",
        "stardew_valley",
        "animal_well",
        "hcniko",
        "v6",
        "shorthike",
        "hk"
    ],
    "support": [
        "tunic",
        "stardew_valley",
        "animal_well",
        "hcniko",
        "v6",
        "shorthike",
        "hk"
    ],
    "ape escape": [
        "apeescape"
    ],
    "ape": [
        "apeescape"
    ],
    "escape": [
        "apeescape"
    ],
    "playstation 3": [
        "sotn",
        "apeescape",
        "lego_star_wars_tcs",
        "sonic_heroes",
        "rogue_legacy",
        "sadx",
        "kh2",
        "sa2b",
        "spyro3",
        "terraria"
    ],
    "3": [
        "mmbn3",
        "sotn",
        "terraria",
        "apeescape",
        "lego_star_wars_tcs",
        "mm3",
        "sonic_heroes",
        "rogue_legacy",
        "sadx",
        "kh2",
        "wl",
        "sa2b",
        "spyro3",
        "kdl3"
    ],
    "playstation portable": [
        "apeescape",
        "spyro3",
        "sotn"
    ],
    "portable": [
        "apeescape",
        "spyro3",
        "sotn"
    ],
    "anime": [
        "dw1",
        "fm",
        "yugiohddm",
        "apeescape",
        "pokemon_crystal",
        "pokemon_emerald",
        "wl4",
        "gstla",
        "musedash"
    ],
    "dinosaurs": [
        "yoshisisland",
        "apeescape",
        "banjo_tooie",
        "earthbound",
        "sms",
        "smw",
        "smo"
    ],
    "collecting": [
        "mzm",
        "apeescape",
        "banjo_tooie",
        "pokemon_crystal",
        "pokemon_emerald",
        "zelda2",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "multiple endings": [
        "sotn",
        "mmx3",
        "mzm",
        "civ_6",
        "apeescape",
        "k64",
        "tloz_oos",
        "witness",
        "wl4",
        "cuphead",
        "metroidprime",
        "dk64",
        "cv64",
        "dkc2",
        "undertale",
        "kh1",
        "star_fox_64"
    ],
    "multiple": [
        "k64",
        "apeescape",
        "witness",
        "sonic_heroes",
        "metroidprime",
        "undertale",
        "mmx3",
        "mzm",
        "dkc2",
        "kh1",
        "civ_6",
        "tloz_oos",
        "rogue_legacy",
        "cuphead",
        "dk64",
        "cv64",
        "dkc",
        "dkc3",
        "spyro3",
        "sotn",
        "mlss",
        "lego_star_wars_tcs",
        "wl4",
        "earthbound",
        "star_fox_64"
    ],
    "endings": [
        "sotn",
        "mmx3",
        "mzm",
        "civ_6",
        "apeescape",
        "k64",
        "tloz_oos",
        "witness",
        "wl4",
        "cuphead",
        "metroidprime",
        "dk64",
        "cv64",
        "dkc2",
        "undertale",
        "kh1",
        "star_fox_64"
    ],
    "amnesia": [
        "xenobladex",
        "apeescape",
        "tloz_ph",
        "witness",
        "sonic_heroes"
    ],
    "voice acting": [
        "dw1",
        "civ_6",
        "apeescape",
        "xenobladex",
        "witness",
        "sonic_heroes",
        "sms",
        "cuphead",
        "jakanddaxter",
        "sly1",
        "cv64",
        "kh1",
        "star_fox_64"
    ],
    "voice": [
        "dw1",
        "civ_6",
        "apeescape",
        "xenobladex",
        "witness",
        "sonic_heroes",
        "sms",
        "cuphead",
        "jakanddaxter",
        "sly1",
        "cv64",
        "kh1",
        "star_fox_64"
    ],
    "acting": [
        "dw1",
        "civ_6",
        "apeescape",
        "xenobladex",
        "witness",
        "sonic_heroes",
        "sms",
        "cuphead",
        "jakanddaxter",
        "sly1",
        "cv64",
        "kh1",
        "star_fox_64"
    ],
    "moving platforms": [
        "k64",
        "apeescape",
        "mm3",
        "tloz_ph",
        "sonic_heroes",
        "metroidprime",
        "v6",
        "mmx3",
        "sms",
        "mm2",
        "jakanddaxter",
        "dk64",
        "cv64",
        "dkc",
        "dkc3",
        "spyro3",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "wl4",
        "sly1",
        "papermario"
    ],
    "moving": [
        "k64",
        "apeescape",
        "mm3",
        "tloz_ph",
        "sonic_heroes",
        "metroidprime",
        "v6",
        "mmx3",
        "sms",
        "mm2",
        "jakanddaxter",
        "dk64",
        "cv64",
        "dkc",
        "dkc3",
        "spyro3",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "wl4",
        "sly1",
        "papermario"
    ],
    "platforms": [
        "k64",
        "apeescape",
        "mm3",
        "tloz_ph",
        "sonic_heroes",
        "zelda2",
        "metroidprime",
        "v6",
        "mmx3",
        "sm_map_rando",
        "sms",
        "mm2",
        "sm",
        "jakanddaxter",
        "dk64",
        "cv64",
        "dkc",
        "dkc3",
        "spyro3",
        "cvcotm",
        "sotn",
        "ladx",
        "tmc",
        "wl4",
        "sly1",
        "oribf",
        "papermario"
    ],
    "time trials": [
        "diddy_kong_racing",
        "apeescape",
        "mk64",
        "sly1",
        "v6",
        "spyro3"
    ],
    "trials": [
        "diddy_kong_racing",
        "apeescape",
        "mk64",
        "sly1",
        "v6",
        "spyro3"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "fm",
        "crystal_project",
        "pmd_eos",
        "wargroove",
        "yugiohddm",
        "civ_6",
        "pokemon_emerald",
        "earthbound",
        "wargroove2",
        "balatro",
        "ffta",
        "undertale",
        "yugioh06",
        "monster_sanctuary",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "turn-based": [
        "fm",
        "crystal_project",
        "pokemon_emerald",
        "balatro",
        "undertale",
        "yugioh06",
        "wargroove2",
        "monster_sanctuary",
        "pokemon_rb",
        "yugiohddm",
        "pokemon_crystal",
        "civ_6",
        "pokemon_frlg",
        "mlss",
        "pmd_eos",
        "wargroove",
        "earthbound",
        "gstla",
        "ffta",
        "ffmq",
        "papermario"
    ],
    "(tbs)": [
        "fm",
        "crystal_project",
        "pmd_eos",
        "wargroove",
        "yugiohddm",
        "civ_6",
        "pokemon_emerald",
        "earthbound",
        "wargroove2",
        "balatro",
        "ffta",
        "undertale",
        "yugioh06",
        "monster_sanctuary",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "card & board game": [
        "yugiohddm",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "card": [
        "yugiohddm",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "board": [
        "yugiohddm",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "game": [
        "fm",
        "pokemon_emerald",
        "witness",
        "balatro",
        "metroidfusion",
        "wl",
        "yugioh06",
        "oot",
        "pokemon_rb",
        "mzm",
        "yugiohddm",
        "pokemon_crystal",
        "dkc2",
        "marioland2",
        "mm2",
        "mmbn3",
        "tloz_oos",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_frlg",
        "spyro3",
        "cvcotm",
        "ladx",
        "mlss",
        "tmc",
        "wl4",
        "earthbound",
        "gstla",
        "hcniko",
        "ffta"
    ],
    "android": [
        "stardew_valley",
        "getting_over_it",
        "lego_star_wars_tcs",
        "subnautica",
        "wargroove2",
        "cat_quest",
        "v6",
        "balatro",
        "dredge",
        "brotato",
        "musedash",
        "terraria"
    ],
    "ios": [
        "hades",
        "getting_over_it",
        "stardew_valley",
        "lego_star_wars_tcs",
        "subnautica",
        "witness",
        "wargroove2",
        "cat_quest",
        "v6",
        "balatro",
        "dredge",
        "brotato",
        "musedash",
        "terraria"
    ],
    "roguelike": [
        "ror1",
        "pmd_eos",
        "hades",
        "rogue_legacy",
        "balatro"
    ],
    "banjo-tooie": [
        "banjo_tooie"
    ],
    "quiz/trivia": [
        "banjo_tooie"
    ],
    "comedy": [
        "undertale",
        "musedash",
        "dw1",
        "banjo_tooie",
        "luigismansion",
        "rac2",
        "dkc2",
        "kh1",
        "getting_over_it",
        "diddy_kong_racing",
        "doronko_wanko",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "dk64",
        "messenger",
        "spyro3",
        "mlss",
        "lego_star_wars_tcs",
        "overcooked2",
        "hcniko",
        "sly1",
        "toontown",
        "sims4",
        "placidplasticducksim",
        "papermario"
    ],
    "nintendo 64": [
        "sm64ex",
        "sm64hacks",
        "diddy_kong_racing",
        "k64",
        "banjo_tooie",
        "mk64",
        "mm_recomp",
        "dk64",
        "cv64",
        "swr",
        "star_fox_64",
        "oot",
        "papermario"
    ],
    "64": [
        "sm64ex",
        "sm64hacks",
        "diddy_kong_racing",
        "k64",
        "banjo_tooie",
        "mk64",
        "mm_recomp",
        "dk64",
        "cv64",
        "swr",
        "star_fox_64",
        "oot",
        "papermario"
    ],
    "aliens": [
        "sm_map_rando",
        "mzm",
        "sm",
        "xenobladex",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "hcniko",
        "earthbound",
        "metroidprime",
        "metroidfusion",
        "factorio"
    ],
    "flight": [
        "diddy_kong_racing",
        "xenobladex",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "mm3",
        "wl4",
        "rogue_legacy",
        "shorthike",
        "dkc",
        "star_fox_64",
        "spyro3",
        "terraria",
        "mm2"
    ],
    "witches": [
        "enderlilies",
        "tmc",
        "tloz_oos",
        "banjo_tooie",
        "minecraft",
        "cv64",
        "tloz_ooa"
    ],
    "achievements": [
        "tunic",
        "sotn",
        "shorthike",
        "stardew_valley",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "sonic_heroes",
        "hcniko",
        "minecraft",
        "cuphead",
        "v6",
        "musedash",
        "hk",
        "oribf"
    ],
    "talking animals": [
        "diddy_kong_racing",
        "banjo_tooie",
        "hcniko",
        "sly1",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "talking": [
        "diddy_kong_racing",
        "banjo_tooie",
        "hcniko",
        "sly1",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "animals": [
        "diddy_kong_racing",
        "banjo_tooie",
        "hcniko",
        "sly1",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "breaking the fourth wall": [
        "ladx",
        "mlss",
        "tmc",
        "banjo_tooie",
        "rogue_legacy",
        "jakanddaxter",
        "ffta",
        "dkc2",
        "metroidfusion",
        "undertale",
        "dkc",
        "papermario"
    ],
    "breaking": [
        "metroidprime",
        "metroidfusion",
        "undertale",
        "oot",
        "sm_map_rando",
        "mzm",
        "banjo_tooie",
        "dkc2",
        "sm",
        "rogue_legacy",
        "jakanddaxter",
        "tloz_ooa",
        "dkc",
        "sotn",
        "ladx",
        "mlss",
        "tmc",
        "wl4",
        "ffta",
        "papermario"
    ],
    "fourth": [
        "ladx",
        "mlss",
        "tmc",
        "banjo_tooie",
        "rogue_legacy",
        "jakanddaxter",
        "ffta",
        "dkc2",
        "metroidfusion",
        "undertale",
        "dkc",
        "papermario"
    ],
    "underwater gameplay": [
        "mmx3",
        "sm64ex",
        "sm64hacks",
        "terraria",
        "banjo_tooie",
        "mm3",
        "subnautica",
        "sms",
        "metroidprime",
        "metroidfusion",
        "dkc2",
        "kh1",
        "dkc",
        "smo",
        "oot",
        "mm2"
    ],
    "underwater": [
        "mmx3",
        "sm64ex",
        "sm64hacks",
        "terraria",
        "banjo_tooie",
        "mm3",
        "subnautica",
        "sms",
        "metroidprime",
        "metroidfusion",
        "dkc2",
        "kh1",
        "dkc",
        "smo",
        "oot",
        "mm2"
    ],
    "gameplay": [
        "mmx3",
        "sm64ex",
        "sm64hacks",
        "terraria",
        "banjo_tooie",
        "mm3",
        "subnautica",
        "sms",
        "metroidprime",
        "metroidfusion",
        "dkc2",
        "kh1",
        "dkc",
        "smo",
        "oot",
        "mm2"
    ],
    "shape-shifting": [
        "sotn",
        "k64",
        "banjo_tooie",
        "mm_recomp",
        "metroidprime",
        "kdl3"
    ],
    "temporary invincibility": [
        "banjo_tooie",
        "mk64",
        "sonic_heroes",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "faxanadu",
        "dkc2",
        "papermario"
    ],
    "temporary": [
        "banjo_tooie",
        "mk64",
        "sonic_heroes",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "faxanadu",
        "dkc2",
        "papermario"
    ],
    "invincibility": [
        "banjo_tooie",
        "mk64",
        "sonic_heroes",
        "rogue_legacy",
        "cuphead",
        "jakanddaxter",
        "faxanadu",
        "dkc2",
        "papermario"
    ],
    "gliding": [
        "tmc",
        "banjo_tooie",
        "sms",
        "sly1",
        "shorthike",
        "kh1",
        "spyro3"
    ],
    "lgbtq+": [
        "celeste",
        "banjo_tooie",
        "timespinner",
        "rogue_legacy",
        "sims4",
        "celeste_open_world"
    ],
    "bomb rush cyberfunk": [
        "bomb_rush_cyberfunk"
    ],
    "bomb": [
        "bomb_rush_cyberfunk"
    ],
    "rush": [
        "bomb_rush_cyberfunk"
    ],
    "cyberfunk": [
        "bomb_rush_cyberfunk"
    ],
    "role-playing (rpg)": [
        "tunic",
        "crystal_project",
        "pokemon_emerald",
        "timespinner",
        "ctjot",
        "zelda2",
        "undertale",
        "monster_sanctuary",
        "ff4fe",
        "wargroove2",
        "pokemon_rb",
        "terraria",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "hades",
        "xenobladex",
        "pokemon_crystal",
        "dredge",
        "brotato",
        "kh1",
        "ror1",
        "mmbn3",
        "crosscode",
        "landstalker",
        "tloz_oos",
        "rogue_legacy",
        "sims4",
        "kh2",
        "faxanadu",
        "tloz_ooa",
        "pokemon_frlg",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ff1",
        "mlss",
        "pmd_eos",
        "stardew_valley",
        "lufia2ac",
        "earthbound",
        "gstla",
        "cat_quest",
        "ffta",
        "toontown",
        "ffmq",
        "papermario"
    ],
    "role-playing": [
        "tunic",
        "crystal_project",
        "pokemon_emerald",
        "timespinner",
        "ctjot",
        "zelda2",
        "undertale",
        "monster_sanctuary",
        "ff4fe",
        "wargroove2",
        "pokemon_rb",
        "terraria",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "hades",
        "xenobladex",
        "pokemon_crystal",
        "dredge",
        "brotato",
        "kh1",
        "ror1",
        "mmbn3",
        "crosscode",
        "landstalker",
        "tloz_oos",
        "rogue_legacy",
        "sims4",
        "kh2",
        "faxanadu",
        "tloz_ooa",
        "pokemon_frlg",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ff1",
        "mlss",
        "pmd_eos",
        "stardew_valley",
        "lufia2ac",
        "earthbound",
        "gstla",
        "cat_quest",
        "ffta",
        "toontown",
        "ffmq",
        "papermario"
    ],
    "(rpg)": [
        "tunic",
        "crystal_project",
        "pokemon_emerald",
        "timespinner",
        "ctjot",
        "zelda2",
        "undertale",
        "monster_sanctuary",
        "ff4fe",
        "wargroove2",
        "pokemon_rb",
        "terraria",
        "dw1",
        "soe",
        "bomb_rush_cyberfunk",
        "hades",
        "xenobladex",
        "pokemon_crystal",
        "dredge",
        "brotato",
        "kh1",
        "ror1",
        "mmbn3",
        "crosscode",
        "landstalker",
        "tloz_oos",
        "rogue_legacy",
        "sims4",
        "kh2",
        "faxanadu",
        "tloz_ooa",
        "pokemon_frlg",
        "cvcotm",
        "enderlilies",
        "sotn",
        "ff1",
        "mlss",
        "pmd_eos",
        "stardew_valley",
        "lufia2ac",
        "earthbound",
        "gstla",
        "cat_quest",
        "ffta",
        "toontown",
        "ffmq",
        "papermario"
    ],
    "sport": [
        "bomb_rush_cyberfunk",
        "trackmania"
    ],
    "science fiction": [
        "mm3",
        "witness",
        "ctjot",
        "metroidprime",
        "v6",
        "metroidfusion",
        "tyrian",
        "factorio",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "mzm",
        "satisfactory",
        "soe",
        "xenobladex",
        "outer_wilds",
        "subnautica",
        "rac2",
        "brotato",
        "mm2",
        "ror1",
        "mmbn3",
        "sm",
        "crosscode",
        "jakanddaxter",
        "pokemon_frlg",
        "ror2",
        "lego_star_wars_tcs",
        "earthbound",
        "swr",
        "star_fox_64"
    ],
    "science": [
        "mm3",
        "witness",
        "ctjot",
        "metroidprime",
        "v6",
        "metroidfusion",
        "tyrian",
        "factorio",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "mzm",
        "satisfactory",
        "soe",
        "xenobladex",
        "outer_wilds",
        "subnautica",
        "rac2",
        "brotato",
        "mm2",
        "ror1",
        "mmbn3",
        "sm",
        "crosscode",
        "jakanddaxter",
        "pokemon_frlg",
        "ror2",
        "lego_star_wars_tcs",
        "earthbound",
        "swr",
        "star_fox_64"
    ],
    "fiction": [
        "mm3",
        "witness",
        "ctjot",
        "metroidprime",
        "v6",
        "metroidfusion",
        "tyrian",
        "factorio",
        "terraria",
        "mmx3",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "mzm",
        "satisfactory",
        "soe",
        "xenobladex",
        "outer_wilds",
        "subnautica",
        "rac2",
        "brotato",
        "mm2",
        "ror1",
        "mmbn3",
        "sm",
        "crosscode",
        "jakanddaxter",
        "pokemon_frlg",
        "ror2",
        "lego_star_wars_tcs",
        "earthbound",
        "swr",
        "star_fox_64"
    ],
    "great soundtrack": [
        "tunic",
        "bomb_rush_cyberfunk",
        "celeste",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste_open_world"
    ],
    "great": [
        "tunic",
        "bomb_rush_cyberfunk",
        "celeste",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste_open_world"
    ],
    "soundtrack": [
        "tunic",
        "bomb_rush_cyberfunk",
        "celeste",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste_open_world"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "ror1",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "ror2",
        "crosscode",
        "sm",
        "cuphead",
        "metroidprime",
        "rac2",
        "metroidfusion",
        "brotato",
        "tyrian",
        "star_fox_64"
    ],
    "arcade": [
        "trackmania",
        "megamix",
        "mm3",
        "mk64",
        "overcooked2",
        "cuphead",
        "smw",
        "v6",
        "mario_kart_double_dash",
        "messenger",
        "brotato",
        "tyrian"
    ],
    "cat quest": [
        "cat_quest"
    ],
    "cat": [
        "tmc",
        "tloz_oos",
        "wl4",
        "minecraft",
        "cat_quest",
        "cuphead",
        "dkc2",
        "kh1"
    ],
    "quest": [
        "cat_quest",
        "dkc2",
        "ffmq"
    ],
    "linux": [
        "crystal_project",
        "timespinner",
        "v6",
        "undertale",
        "monster_sanctuary",
        "shorthike",
        "factorio",
        "terraria",
        "hk",
        "ror1",
        "getting_over_it",
        "crosscode",
        "landstalker",
        "dontstarvetogether",
        "rogue_legacy",
        "celeste",
        "stardew_valley",
        "overcooked2",
        "minecraft",
        "cat_quest",
        "celeste_open_world"
    ],
    "celeste": [
        "celeste_open_world",
        "celeste"
    ],
    "google stadia": [
        "ror2",
        "celeste_open_world",
        "celeste",
        "terraria"
    ],
    "google": [
        "ror2",
        "celeste_open_world",
        "celeste",
        "terraria"
    ],
    "stadia": [
        "ror2",
        "celeste_open_world",
        "celeste",
        "terraria"
    ],
    "difficult": [
        "ror1",
        "tunic",
        "hades",
        "celeste",
        "getting_over_it",
        "dontstarvetogether",
        "zelda2",
        "messenger",
        "celeste_open_world"
    ],
    "story rich": [
        "hades",
        "celeste",
        "getting_over_it",
        "powerwashsimulator",
        "dredge",
        "undertale",
        "celeste_open_world"
    ],
    "story": [
        "hades",
        "celeste",
        "getting_over_it",
        "powerwashsimulator",
        "dredge",
        "undertale",
        "celeste_open_world"
    ],
    "rich": [
        "hades",
        "celeste",
        "getting_over_it",
        "powerwashsimulator",
        "dredge",
        "undertale",
        "celeste_open_world"
    ],
    "celeste (open world)": [
        "celeste_open_world"
    ],
    "civilization vi": [
        "civ_6"
    ],
    "sid meier's civilization iv": [
        "civ_6"
    ],
    "sid": [
        "civ_6"
    ],
    "meier's": [
        "civ_6"
    ],
    "civilization": [
        "civ_6"
    ],
    "iv": [
        "civ_6"
    ],
    "educational": [
        "civ_6"
    ],
    "4x (explore, expand, exploit, and exterminate)": [
        "civ_6"
    ],
    "4x": [
        "civ_6"
    ],
    "(explore,": [
        "civ_6"
    ],
    "expand,": [
        "civ_6"
    ],
    "exploit,": [
        "civ_6"
    ],
    "exterminate)": [
        "civ_6"
    ],
    "loot gathering": [
        "civ_6",
        "xenobladex",
        "minecraft",
        "dk64",
        "cv64",
        "terraria"
    ],
    "loot": [
        "civ_6",
        "xenobladex",
        "minecraft",
        "dk64",
        "cv64",
        "terraria"
    ],
    "gathering": [
        "civ_6",
        "xenobladex",
        "minecraft",
        "dk64",
        "cv64",
        "terraria"
    ],
    "ambient music": [
        "soe",
        "mzm",
        "civ_6",
        "metroidprime",
        "cv64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3"
    ],
    "ambient": [
        "soe",
        "mzm",
        "civ_6",
        "metroidprime",
        "cv64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3"
    ],
    "music": [
        "sotn",
        "soe",
        "mzm",
        "civ_6",
        "megamix",
        "placidplasticducksim",
        "sonic_heroes",
        "gstla",
        "metroidprime",
        "cv64",
        "dkc2",
        "ffta",
        "metroidfusion",
        "musedash",
        "ffmq",
        "dkc",
        "dkc3"
    ],
    "crosscode": [
        "crosscode"
    ],
    "crystal project": [
        "crystal_project"
    ],
    "crystal": [
        "k64",
        "pokemon_crystal",
        "crystal_project"
    ],
    "project": [
        "megamix",
        "crystal_project"
    ],
    "tactical": [
        "mmbn3",
        "crystal_project",
        "wargroove",
        "overcooked2",
        "ffta"
    ],
    "jrpg": [
        "ff1",
        "crystal_project",
        "pmd_eos",
        "ffta",
        "ff4fe",
        "ffmq"
    ],
    "chrono trigger jets of time": [
        "ctjot"
    ],
    "chrono trigger": [
        "ctjot"
    ],
    "chrono": [
        "ctjot"
    ],
    "trigger": [
        "ctjot"
    ],
    "nintendo ds": [
        "tloz_ph",
        "pmd_eos",
        "ctjot"
    ],
    "ds": [
        "tloz_ph",
        "pmd_eos",
        "ctjot"
    ],
    "cuphead": [
        "cuphead"
    ],
    "pirates": [
        "mzm",
        "seaofthieves",
        "tloz_oos",
        "tloz_ph",
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "dkc2",
        "wargroove2",
        "tloz_ooa",
        "kh1"
    ],
    "robots": [
        "mmx3",
        "xenobladex",
        "lego_star_wars_tcs",
        "mm3",
        "sonic_heroes",
        "earthbound",
        "sms",
        "cuphead",
        "metroidfusion",
        "swr",
        "star_fox_64",
        "mm2"
    ],
    "side-scrolling": [
        "sotn",
        "mmx3",
        "sm_map_rando",
        "mzm",
        "yoshisisland",
        "sm",
        "k64",
        "mm3",
        "zelda2",
        "rogue_legacy",
        "cuphead",
        "dkc2",
        "metroidfusion",
        "musedash",
        "dkc",
        "dkc3",
        "kdl3",
        "mm2"
    ],
    "violent plants": [
        "ss",
        "sms",
        "rogue_legacy",
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "terraria"
    ],
    "violent": [
        "ss",
        "sms",
        "rogue_legacy",
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "terraria"
    ],
    "plants": [
        "ss",
        "sms",
        "rogue_legacy",
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "terraria"
    ],
    "auto-scrolling levels": [
        "k64",
        "cuphead",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "auto-scrolling": [
        "k64",
        "cuphead",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "levels": [
        "k64",
        "cuphead",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "star_fox_64"
    ],
    "boss assistance": [
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "sms",
        "rogue_legacy",
        "cuphead",
        "metroidprime",
        "dkc2",
        "dkc",
        "oot",
        "papermario"
    ],
    "assistance": [
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "sms",
        "rogue_legacy",
        "cuphead",
        "metroidprime",
        "dkc2",
        "dkc",
        "oot",
        "papermario"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "hack and slash/beat 'em up": [
        "ror1",
        "cv64",
        "hades"
    ],
    "hack": [
        "ror1",
        "cv64",
        "hades"
    ],
    "slash/beat": [
        "ror1",
        "cv64",
        "hades"
    ],
    "'em": [
        "ror1",
        "cv64",
        "hades"
    ],
    "up": [
        "cvcotm",
        "dw1",
        "ror1",
        "sotn",
        "hades",
        "landstalker",
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "zelda2",
        "cv64",
        "undertale",
        "kh1",
        "papermario"
    ],
    "bloody": [
        "metroidprime",
        "cv64",
        "sotn"
    ],
    "horse": [
        "cvcotm",
        "sotn",
        "minecraft",
        "rogue_legacy",
        "cv64",
        "oot"
    ],
    "multiple protagonists": [
        "sotn",
        "mmx3",
        "mlss",
        "lego_star_wars_tcs",
        "sonic_heroes",
        "earthbound",
        "rogue_legacy",
        "dk64",
        "cv64",
        "dkc2",
        "dkc",
        "dkc3",
        "spyro3"
    ],
    "protagonists": [
        "sotn",
        "mmx3",
        "mlss",
        "lego_star_wars_tcs",
        "sonic_heroes",
        "earthbound",
        "rogue_legacy",
        "dk64",
        "cv64",
        "dkc2",
        "dkc",
        "dkc3",
        "spyro3"
    ],
    "traps": [
        "tmc",
        "minecraft",
        "rogue_legacy",
        "metroidfusion",
        "cv64"
    ],
    "dog": [
        "soe",
        "seaofthieves",
        "hades",
        "terraria",
        "tmc",
        "tloz_oos",
        "doronko_wanko",
        "overcooked2",
        "hcniko",
        "minecraft",
        "sly1",
        "cv64",
        "undertale",
        "sims4",
        "star_fox_64",
        "smo",
        "oot"
    ],
    "bats": [
        "cvcotm",
        "sotn",
        "pokemon_crystal",
        "mk64",
        "zelda2",
        "cv64",
        "terraria"
    ],
    "day/night cycle": [
        "sotn",
        "stardew_valley",
        "terraria",
        "xenobladex",
        "pokemon_crystal",
        "tww",
        "mm_recomp",
        "ss",
        "minecraft",
        "jakanddaxter",
        "dk64",
        "cv64",
        "oot"
    ],
    "day/night": [
        "sotn",
        "stardew_valley",
        "terraria",
        "xenobladex",
        "pokemon_crystal",
        "tww",
        "mm_recomp",
        "ss",
        "minecraft",
        "jakanddaxter",
        "dk64",
        "cv64",
        "oot"
    ],
    "cycle": [
        "sotn",
        "stardew_valley",
        "terraria",
        "xenobladex",
        "pokemon_crystal",
        "tww",
        "mm_recomp",
        "ss",
        "minecraft",
        "jakanddaxter",
        "dk64",
        "cv64",
        "oot"
    ],
    "alternate costumes": [
        "lego_star_wars_tcs",
        "sms",
        "metroidfusion",
        "cv64",
        "kh1",
        "smo"
    ],
    "alternate": [
        "lego_star_wars_tcs",
        "sms",
        "metroidfusion",
        "cv64",
        "kh1",
        "smo"
    ],
    "costumes": [
        "lego_star_wars_tcs",
        "sms",
        "metroidfusion",
        "cv64",
        "kh1",
        "smo"
    ],
    "skeletons": [
        "cvcotm",
        "sotn",
        "seaofthieves",
        "minecraft",
        "sly1",
        "cv64",
        "undertale",
        "terraria"
    ],
    "unstable platforms": [
        "cvcotm",
        "sm_map_rando",
        "sm",
        "tmc",
        "zelda2",
        "sms",
        "metroidprime",
        "sly1",
        "v6",
        "cv64",
        "dkc",
        "oribf"
    ],
    "unstable": [
        "cvcotm",
        "sm_map_rando",
        "sm",
        "tmc",
        "zelda2",
        "sms",
        "metroidprime",
        "sly1",
        "v6",
        "cv64",
        "dkc",
        "oribf"
    ],
    "melee": [
        "cvcotm",
        "tunic",
        "sotn",
        "terraria",
        "tmc",
        "k64",
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "pokemon_emerald",
        "wl4",
        "gstla",
        "sly1",
        "ffta",
        "cv64",
        "metroidfusion",
        "kh1",
        "kdl3",
        "papermario"
    ],
    "instant kill": [
        "v6",
        "metroidfusion",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "instant": [
        "v6",
        "metroidfusion",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "kill": [
        "v6",
        "metroidfusion",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "difficulty level": [
        "mzm",
        "mk64",
        "minecraft",
        "metroidprime",
        "cv64",
        "musedash",
        "star_fox_64",
        "mm2"
    ],
    "difficulty": [
        "mzm",
        "mk64",
        "minecraft",
        "metroidprime",
        "cv64",
        "musedash",
        "star_fox_64",
        "mm2"
    ],
    "level": [
        "mzm",
        "mk64",
        "sms",
        "minecraft",
        "metroidprime",
        "cv64",
        "dkc2",
        "musedash",
        "kh1",
        "dkc",
        "star_fox_64",
        "oot",
        "mm2"
    ],
    "plot twist": [
        "metroidfusion",
        "cv64",
        "undertale",
        "kh1",
        "oot"
    ],
    "plot": [
        "metroidfusion",
        "cv64",
        "undertale",
        "kh1",
        "oot"
    ],
    "twist": [
        "metroidfusion",
        "cv64",
        "undertale",
        "kh1",
        "oot"
    ],
    "castlevania - circle of the moon": [
        "cvcotm"
    ],
    "castlevania: circle of the moon": [
        "cvcotm"
    ],
    "castlevania:": [
        "cvcotm",
        "sotn"
    ],
    "circle": [
        "cvcotm"
    ],
    "moon": [
        "cvcotm"
    ],
    "game boy advance": [
        "cvcotm",
        "mmbn3",
        "mlss",
        "mzm",
        "tmc",
        "yugiohddm",
        "pokemon_emerald",
        "wl4",
        "gstla",
        "earthbound",
        "yugioh06",
        "metroidfusion",
        "ffta",
        "pokemon_frlg"
    ],
    "boy": [
        "pokemon_emerald",
        "yugioh06",
        "metroidfusion",
        "wl",
        "pokemon_rb",
        "mzm",
        "yugiohddm",
        "pokemon_crystal",
        "marioland2",
        "mm2",
        "mmbn3",
        "tloz_oos",
        "tloz_ooa",
        "pokemon_frlg",
        "cvcotm",
        "ladx",
        "mlss",
        "tmc",
        "wl4",
        "gstla",
        "earthbound",
        "ffta"
    ],
    "advance": [
        "cvcotm",
        "mmbn3",
        "mlss",
        "mzm",
        "tmc",
        "yugiohddm",
        "pokemon_emerald",
        "wl4",
        "gstla",
        "earthbound",
        "yugioh06",
        "metroidfusion",
        "ffta",
        "pokemon_frlg"
    ],
    "gravity": [
        "cvcotm",
        "sotn",
        "mzm",
        "star_fox_64",
        "lego_star_wars_tcs",
        "metroidprime",
        "v6",
        "dk64",
        "dkc2",
        "metroidfusion",
        "dkc",
        "dkc3",
        "oot",
        "papermario"
    ],
    "leveling up": [
        "cvcotm",
        "dw1",
        "sotn",
        "landstalker",
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "zelda2",
        "undertale",
        "kh1",
        "papermario"
    ],
    "leveling": [
        "cvcotm",
        "dw1",
        "sotn",
        "landstalker",
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "zelda2",
        "undertale",
        "kh1",
        "papermario"
    ],
    "diddy kong racing": [
        "diddy_kong_racing"
    ],
    "diddy": [
        "diddy_kong_racing"
    ],
    "kong": [
        "diddy_kong_racing",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "racing": [
        "trackmania",
        "diddy_kong_racing",
        "mk64",
        "jakanddaxter",
        "mario_kart_double_dash",
        "swr"
    ],
    "behind the waterfall": [
        "sotn",
        "smo",
        "diddy_kong_racing",
        "tmc",
        "ss",
        "hcniko",
        "gstla",
        "tloz_ooa",
        "dkc3"
    ],
    "behind": [
        "sotn",
        "smo",
        "diddy_kong_racing",
        "tmc",
        "ss",
        "hcniko",
        "gstla",
        "tloz_ooa",
        "dkc3"
    ],
    "waterfall": [
        "sotn",
        "smo",
        "diddy_kong_racing",
        "tmc",
        "ss",
        "hcniko",
        "gstla",
        "tloz_ooa",
        "dkc3"
    ],
    "donkey kong 64": [
        "dk64"
    ],
    "donkey": [
        "dkc3",
        "dkc",
        "dk64",
        "dkc2"
    ],
    "artificial intelligence": [
        "mk64",
        "jakanddaxter",
        "metroidprime",
        "dk64",
        "sly1",
        "star_fox_64"
    ],
    "artificial": [
        "mk64",
        "jakanddaxter",
        "metroidprime",
        "dk64",
        "sly1",
        "star_fox_64"
    ],
    "intelligence": [
        "mk64",
        "jakanddaxter",
        "metroidprime",
        "dk64",
        "sly1",
        "star_fox_64"
    ],
    "completion percentage": [
        "sotn",
        "mzm",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "dkc2"
    ],
    "completion": [
        "sotn",
        "mzm",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "dkc2"
    ],
    "percentage": [
        "sotn",
        "mzm",
        "metroidprime",
        "dk64",
        "metroidfusion",
        "dkc2"
    ],
    "invisibility": [
        "sly1",
        "dk64",
        "papermario"
    ],
    "foreshadowing": [
        "mzm",
        "tmc",
        "sms",
        "metroidprime",
        "dk64",
        "metroidfusion"
    ],
    "donkey kong country": [
        "dkc"
    ],
    "country": [
        "dkc",
        "dkc3",
        "dkc2"
    ],
    "overworld": [
        "gstla",
        "zelda2",
        "ffta",
        "dkc2",
        "tloz",
        "ffmq",
        "dkc",
        "dkc3"
    ],
    "bonus stage": [
        "sonic_heroes",
        "smw",
        "dkc2",
        "dkc",
        "dkc3",
        "spyro3"
    ],
    "bonus": [
        "sonic_heroes",
        "smw",
        "dkc2",
        "dkc",
        "dkc3",
        "spyro3"
    ],
    "checkpoints": [
        "mmx3",
        "smo",
        "mm3",
        "sonic_heroes",
        "jakanddaxter",
        "sly1",
        "v6",
        "dkc2",
        "dkc",
        "dkc3",
        "mm2"
    ],
    "water level": [
        "sms",
        "dkc2",
        "kh1",
        "dkc",
        "oot",
        "mm2"
    ],
    "water": [
        "sms",
        "dkc2",
        "kh1",
        "dkc",
        "oot",
        "mm2"
    ],
    "speedrun": [
        "sotn",
        "sm64ex",
        "sm64hacks",
        "metroidprime",
        "metroidfusion",
        "dkc"
    ],
    "donkey kong country 2": [
        "dkc2"
    ],
    "donkey kong country 2: diddy's kong quest": [
        "dkc2"
    ],
    "2:": [
        "sa2b",
        "marioland2",
        "yoshisisland",
        "dkc2"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "sms",
        "jakanddaxter",
        "sly1",
        "dkc2",
        "shorthike",
        "terraria"
    ],
    "spider": [
        "zelda2",
        "minecraft",
        "sly1",
        "dkc2",
        "oribf"
    ],
    "game reference": [
        "tmc",
        "witness",
        "hcniko",
        "rogue_legacy",
        "dkc2",
        "spyro3",
        "oot"
    ],
    "reference": [
        "tmc",
        "witness",
        "hcniko",
        "rogue_legacy",
        "dkc2",
        "placidplasticducksim",
        "spyro3",
        "oot"
    ],
    "sprinting mechanics": [
        "soe",
        "sm64ex",
        "sm64hacks",
        "pokemon_crystal",
        "pokemon_emerald",
        "mm_recomp",
        "wl4",
        "sms",
        "dkc2",
        "oot"
    ],
    "sprinting": [
        "soe",
        "sm64ex",
        "sm64hacks",
        "pokemon_crystal",
        "pokemon_emerald",
        "mm_recomp",
        "wl4",
        "sms",
        "dkc2",
        "oot"
    ],
    "mechanics": [
        "soe",
        "sm64ex",
        "sm64hacks",
        "pokemon_crystal",
        "pokemon_emerald",
        "mm_recomp",
        "wl4",
        "sms",
        "dkc2",
        "oot"
    ],
    "donkey kong country 3": [
        "dkc3"
    ],
    "donkey kong country 3: dixie kong's double trouble!": [
        "dkc3"
    ],
    "3:": [
        "dkc3"
    ],
    "dixie": [
        "dkc3"
    ],
    "kong's": [
        "dkc3"
    ],
    "double": [
        "dkc3",
        "mario_kart_double_dash"
    ],
    "trouble!": [
        "dkc3"
    ],
    "don't starve together": [
        "dontstarvetogether"
    ],
    "don't": [
        "dontstarvetogether"
    ],
    "starve": [
        "dontstarvetogether"
    ],
    "together": [
        "dontstarvetogether"
    ],
    "crafting": [
        "seaofthieves",
        "stardew_valley",
        "satisfactory",
        "raft",
        "dontstarvetogether",
        "minecraft",
        "factorio",
        "terraria"
    ],
    "funny": [
        "getting_over_it",
        "dontstarvetogether",
        "powerwashsimulator",
        "undertale",
        "shorthike",
        "sims4"
    ],
    "doronko wanko": [
        "doronko_wanko"
    ],
    "doronko": [
        "doronko_wanko"
    ],
    "wanko": [
        "doronko_wanko"
    ],
    "dredge": [
        "dredge"
    ],
    "fishing": [
        "ladx",
        "stardew_valley",
        "hcniko",
        "minecraft",
        "dredge",
        "shorthike",
        "terraria"
    ],
    "stylized": [
        "tunic",
        "hades",
        "hcniko",
        "dredge",
        "shorthike"
    ],
    "digimon world": [
        "dw1"
    ],
    "digimon world 4": [
        "dw1"
    ],
    "digimon": [
        "dw1"
    ],
    "nintendo gamecube": [
        "dw1",
        "tww",
        "sonic_heroes",
        "luigismansion",
        "sms",
        "metroidprime",
        "mario_kart_double_dash"
    ],
    "gamecube": [
        "dw1",
        "tww",
        "sonic_heroes",
        "luigismansion",
        "sms",
        "metroidprime",
        "mario_kart_double_dash"
    ],
    "playstation 2": [
        "dw1",
        "sonic_heroes",
        "jakanddaxter",
        "kh2",
        "rac2",
        "sly1",
        "kh1"
    ],
    "2": [
        "dw1",
        "stardew_valley",
        "ror2",
        "overcooked2",
        "sonic_heroes",
        "jakanddaxter",
        "kh2",
        "rac2",
        "sly1",
        "wargroove2",
        "kh1",
        "smo"
    ],
    "earthbound": [
        "earthbound"
    ],
    "drama": [
        "undertale",
        "hades",
        "earthbound"
    ],
    "party system": [
        "ffmq",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "ffta",
        "kh1",
        "papermario"
    ],
    "party": [
        "ffmq",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "pokemon_emerald",
        "mk64",
        "overcooked2",
        "gstla",
        "earthbound",
        "ffta",
        "kh1",
        "placidplasticducksim",
        "papermario"
    ],
    "fire manipulation": [
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "minecraft",
        "rogue_legacy",
        "papermario"
    ],
    "fire": [
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "minecraft",
        "rogue_legacy",
        "papermario"
    ],
    "manipulation": [
        "pokemon_crystal",
        "pokemon_emerald",
        "gstla",
        "earthbound",
        "minecraft",
        "rogue_legacy",
        "papermario"
    ],
    "ender lilies": [
        "enderlilies"
    ],
    "ender lilies: quietus of the knights": [
        "enderlilies"
    ],
    "ender": [
        "enderlilies"
    ],
    "lilies:": [
        "enderlilies"
    ],
    "quietus": [
        "enderlilies"
    ],
    "knights": [
        "enderlilies"
    ],
    "soulslike": [
        "enderlilies",
        "tunic"
    ],
    "factorio": [
        "factorio"
    ],
    "faxanadu": [
        "faxanadu"
    ],
    "family computer": [
        "tloz",
        "ff1",
        "mm3",
        "faxanadu"
    ],
    "family": [
        "ff1",
        "mm3",
        "zelda2",
        "faxanadu",
        "tloz"
    ],
    "computer": [
        "ff1",
        "mm3",
        "zelda2",
        "faxanadu",
        "tloz"
    ],
    "nintendo entertainment system": [
        "ff1",
        "mm3",
        "zelda2",
        "faxanadu",
        "tloz"
    ],
    "final fantasy": [
        "ff1"
    ],
    "final": [
        "ff4fe",
        "ffmq",
        "ff1",
        "ffta"
    ],
    "kids": [
        "yoshisisland",
        "ff1",
        "pmd_eos",
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "mk64",
        "overcooked2",
        "pokemon_emerald",
        "minecraft",
        "mario_kart_double_dash",
        "tetrisattack",
        "placidplasticducksim",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "final fantasy iv free enterprise": [
        "ff4fe"
    ],
    "final fantasy ii": [
        "ff4fe"
    ],
    "ii": [
        "ff4fe",
        "kh2",
        "mm2"
    ],
    "final fantasy mystic quest": [
        "ffmq"
    ],
    "final fantasy: mystic quest": [
        "ffmq"
    ],
    "fantasy:": [
        "ffmq"
    ],
    "mystic": [
        "ffmq"
    ],
    "casual": [
        "shorthike",
        "getting_over_it",
        "sims4",
        "musedash",
        "ffmq",
        "placidplasticducksim"
    ],
    "rock music": [
        "sotn",
        "sonic_heroes",
        "gstla",
        "ffta",
        "ffmq"
    ],
    "rock": [
        "sotn",
        "sonic_heroes",
        "gstla",
        "ffta",
        "ffmq"
    ],
    "final fantasy tactics advance": [
        "ffta"
    ],
    "tactics": [
        "ffta"
    ],
    "stat tracking": [
        "rogue_legacy",
        "kh1",
        "witness",
        "ffta"
    ],
    "stat": [
        "rogue_legacy",
        "kh1",
        "witness",
        "ffta"
    ],
    "tracking": [
        "rogue_legacy",
        "kh1",
        "witness",
        "ffta"
    ],
    "yu-gi-oh! forbidden memories": [
        "fm"
    ],
    "yu-gi-oh!": [
        "yugiohddm",
        "fm",
        "yugioh06"
    ],
    "forbidden": [
        "fm"
    ],
    "memories": [
        "fm"
    ],
    "getting over it": [
        "getting_over_it"
    ],
    "getting over it with bennett foddy": [
        "getting_over_it"
    ],
    "getting": [
        "getting_over_it"
    ],
    "it": [
        "getting_over_it"
    ],
    "with": [
        "getting_over_it"
    ],
    "bennett": [
        "getting_over_it"
    ],
    "foddy": [
        "getting_over_it"
    ],
    "golden sun the lost age": [
        "gstla"
    ],
    "golden sun: the lost age": [
        "gstla"
    ],
    "golden": [
        "marioland2",
        "gstla"
    ],
    "sun:": [
        "gstla"
    ],
    "lost": [
        "gstla"
    ],
    "hades": [
        "hades"
    ],
    "you can pet the dog": [
        "seaofthieves",
        "hades",
        "overcooked2",
        "undertale",
        "sims4",
        "terraria"
    ],
    "you": [
        "seaofthieves",
        "hades",
        "overcooked2",
        "undertale",
        "sims4",
        "terraria"
    ],
    "can": [
        "seaofthieves",
        "hades",
        "overcooked2",
        "undertale",
        "sims4",
        "terraria"
    ],
    "pet": [
        "seaofthieves",
        "hades",
        "overcooked2",
        "undertale",
        "sims4",
        "terraria"
    ],
    "here comes niko!": [
        "hcniko"
    ],
    "comes": [
        "hcniko"
    ],
    "niko!": [
        "hcniko"
    ],
    "hollow knight": [
        "hk"
    ],
    "hollow": [
        "hk"
    ],
    "knight": [
        "hk"
    ],
    "interconnected-world": [
        "sotn",
        "sm_map_rando",
        "mzm",
        "sm",
        "luigismansion",
        "hk"
    ],
    "jak and daxter: the precursor legacy": [
        "jakanddaxter"
    ],
    "jak": [
        "jakanddaxter"
    ],
    "daxter:": [
        "jakanddaxter"
    ],
    "precursor": [
        "jakanddaxter"
    ],
    "legacy": [
        "rogue_legacy",
        "jakanddaxter",
        "mmx3"
    ],
    "kirby 64 - the crystal shards": [
        "k64"
    ],
    "kirby 64: the crystal shards": [
        "k64"
    ],
    "kirby": [
        "k64"
    ],
    "64:": [
        "k64"
    ],
    "shards": [
        "k64"
    ],
    "kirby's dream land 3": [
        "kdl3"
    ],
    "kirby's": [
        "kdl3"
    ],
    "dream": [
        "kdl3"
    ],
    "land": [
        "marioland2",
        "wl",
        "kdl3",
        "wl4"
    ],
    "kingdom hearts": [
        "kh1"
    ],
    "kingdom": [
        "kh1",
        "kh2"
    ],
    "hearts": [
        "kh1",
        "kh2"
    ],
    "kingdom hearts 2": [
        "kh2"
    ],
    "kingdom hearts ii": [
        "kh2"
    ],
    "link's awakening dx beta": [
        "ladx"
    ],
    "the legend of zelda: link's awakening dx": [
        "ladx"
    ],
    "link's": [
        "ladx"
    ],
    "awakening": [
        "ladx"
    ],
    "dx": [
        "sadx",
        "ladx"
    ],
    "game boy color": [
        "tloz_oos",
        "tloz_ooa",
        "pokemon_crystal",
        "ladx"
    ],
    "color": [
        "tloz_oos",
        "tloz_ooa",
        "pokemon_crystal",
        "ladx"
    ],
    "tentacles": [
        "ladx",
        "mlss",
        "pokemon_crystal",
        "pokemon_emerald",
        "sms",
        "metroidprime",
        "papermario"
    ],
    "landstalker - the treasures of king nole": [
        "landstalker"
    ],
    "landstalker": [
        "landstalker"
    ],
    "sega mega drive/genesis": [
        "landstalker"
    ],
    "sega": [
        "landstalker"
    ],
    "mega": [
        "mmbn3",
        "mmx3",
        "landstalker",
        "megamix",
        "mm3",
        "mm2"
    ],
    "drive/genesis": [
        "landstalker"
    ],
    "lego star wars: the complete saga": [
        "lego_star_wars_tcs"
    ],
    "lego": [
        "lego_star_wars_tcs"
    ],
    "star": [
        "lego_star_wars_tcs",
        "star_fox_64",
        "swr"
    ],
    "wars:": [
        "lego_star_wars_tcs",
        "swr"
    ],
    "complete": [
        "lego_star_wars_tcs"
    ],
    "saga": [
        "lego_star_wars_tcs",
        "mlss"
    ],
    "xbox 360": [
        "sotn",
        "lego_star_wars_tcs",
        "sadx",
        "sa2b",
        "terraria"
    ],
    "360": [
        "sotn",
        "lego_star_wars_tcs",
        "sadx",
        "sa2b",
        "terraria"
    ],
    "customizable characters": [
        "xenobladex",
        "lego_star_wars_tcs",
        "stardew_valley",
        "terraria"
    ],
    "customizable": [
        "xenobladex",
        "lego_star_wars_tcs",
        "stardew_valley",
        "terraria"
    ],
    "lufia ii: ancient cave": [
        "lufia2ac"
    ],
    "lufia ii: rise of the sinistrals": [
        "lufia2ac"
    ],
    "lufia": [
        "lufia2ac"
    ],
    "ii:": [
        "lufia2ac",
        "zelda2"
    ],
    "rise": [
        "lufia2ac"
    ],
    "sinistrals": [
        "lufia2ac"
    ],
    "luigi's mansion": [
        "luigismansion"
    ],
    "luigi's": [
        "luigismansion"
    ],
    "mansion": [
        "luigismansion"
    ],
    "super mario land 2": [
        "marioland2"
    ],
    "super mario land 2: 6 golden coins": [
        "marioland2"
    ],
    "mario": [
        "yoshisisland",
        "mlss",
        "sm64ex",
        "sm64hacks",
        "mk64",
        "sms",
        "smw",
        "mario_kart_double_dash",
        "wl",
        "marioland2",
        "smo",
        "papermario"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "marioland2",
        "wl",
        "pokemon_rb",
        "mm2"
    ],
    "turtle": [
        "mlss",
        "mk64",
        "sms",
        "sly1",
        "marioland2",
        "papermario"
    ],
    "mario kart double dash": [
        "mario_kart_double_dash"
    ],
    "mario kart: double dash!!": [
        "mario_kart_double_dash"
    ],
    "kart:": [
        "mario_kart_double_dash"
    ],
    "dash!!": [
        "mario_kart_double_dash"
    ],
    "hatsune miku project diva mega mix+": [
        "megamix"
    ],
    "hatsune miku: project diva mega mix": [
        "megamix"
    ],
    "hatsune": [
        "megamix"
    ],
    "miku:": [
        "megamix"
    ],
    "diva": [
        "megamix"
    ],
    "mix": [
        "megamix"
    ],
    "the messenger": [
        "messenger"
    ],
    "messenger": [
        "messenger"
    ],
    "metroid fusion": [
        "metroidfusion"
    ],
    "metroid": [
        "sm",
        "metroidprime",
        "sm_map_rando",
        "metroidfusion"
    ],
    "fusion": [
        "metroidfusion"
    ],
    "time limit": [
        "ror1",
        "sm_map_rando",
        "sm",
        "tmc",
        "tloz_ph",
        "witness",
        "wl4",
        "sms",
        "rogue_legacy",
        "metroidprime",
        "metroidfusion",
        "shorthike"
    ],
    "limit": [
        "ror1",
        "sm_map_rando",
        "sm",
        "tmc",
        "tloz_ph",
        "witness",
        "wl4",
        "sms",
        "rogue_legacy",
        "metroidprime",
        "metroidfusion",
        "shorthike"
    ],
    "countdown timer": [
        "sm_map_rando",
        "mzm",
        "sm",
        "tmc",
        "tloz_ph",
        "wl4",
        "rogue_legacy",
        "metroidprime",
        "metroidfusion",
        "oot"
    ],
    "countdown": [
        "sm_map_rando",
        "mzm",
        "sm",
        "tmc",
        "tloz_ph",
        "wl4",
        "rogue_legacy",
        "metroidprime",
        "metroidfusion",
        "oot"
    ],
    "timer": [
        "sm_map_rando",
        "mzm",
        "sm",
        "tmc",
        "tloz_ph",
        "wl4",
        "rogue_legacy",
        "metroidprime",
        "metroidfusion",
        "oot"
    ],
    "isolation": [
        "sotn",
        "sm_map_rando",
        "mzm",
        "sm",
        "metroidprime",
        "metroidfusion"
    ],
    "metroid prime": [
        "metroidprime"
    ],
    "prime": [
        "metroidprime"
    ],
    "auto-aim": [
        "tww",
        "mm_recomp",
        "ss",
        "metroidprime",
        "oot"
    ],
    "sequence breaking": [
        "sotn",
        "sm_map_rando",
        "mzm",
        "sm",
        "tmc",
        "wl4",
        "metroidprime",
        "tloz_ooa",
        "oot"
    ],
    "sequence": [
        "sotn",
        "sm_map_rando",
        "mzm",
        "sm",
        "tmc",
        "wl4",
        "metroidprime",
        "tloz_ooa",
        "oot"
    ],
    "meme origin": [
        "sotn",
        "mm_recomp",
        "zelda2",
        "minecraft",
        "metroidprime",
        "tloz",
        "star_fox_64"
    ],
    "meme": [
        "sotn",
        "mm_recomp",
        "zelda2",
        "minecraft",
        "metroidprime",
        "tloz",
        "star_fox_64"
    ],
    "origin": [
        "sotn",
        "mm_recomp",
        "zelda2",
        "minecraft",
        "metroidprime",
        "tloz",
        "star_fox_64"
    ],
    "minecraft": [
        "minecraft"
    ],
    "minecraft: java edition": [
        "minecraft"
    ],
    "minecraft:": [
        "minecraft"
    ],
    "java": [
        "minecraft"
    ],
    "edition": [
        "minecraft"
    ],
    "virtual reality": [
        "minecraft",
        "subnautica"
    ],
    "virtual": [
        "minecraft",
        "subnautica"
    ],
    "reality": [
        "minecraft",
        "subnautica"
    ],
    "deliberately retro": [
        "stardew_valley",
        "timespinner",
        "minecraft",
        "v6",
        "smo",
        "terraria"
    ],
    "deliberately": [
        "stardew_valley",
        "timespinner",
        "minecraft",
        "v6",
        "smo",
        "terraria"
    ],
    "mario kart 64": [
        "mk64"
    ],
    "kart": [
        "mk64"
    ],
    "mario & luigi superstar saga": [
        "mlss"
    ],
    "mario & luigi: superstar saga": [
        "mlss"
    ],
    "luigi:": [
        "mlss"
    ],
    "superstar": [
        "mlss"
    ],
    "mega man 2": [
        "mm2"
    ],
    "mega man ii": [
        "mm2"
    ],
    "man": [
        "mmx3",
        "mmbn3",
        "mm3",
        "mm2"
    ],
    "mega man 3": [
        "mm3"
    ],
    "megaman battle network 3": [
        "mmbn3"
    ],
    "mega man battle network 3 blue": [
        "mmbn3"
    ],
    "battle": [
        "sa2b",
        "mmbn3"
    ],
    "network": [
        "mmbn3"
    ],
    "blue": [
        "mmbn3"
    ],
    "mega man x3": [
        "mmx3"
    ],
    "x3": [
        "mmx3"
    ],
    "legacy mobile device": [
        "mmx3"
    ],
    "mobile": [
        "mmx3"
    ],
    "device": [
        "mmx3"
    ],
    "majora's mask recompiled": [
        "mm_recomp"
    ],
    "the legend of zelda: majora's mask": [
        "mm_recomp"
    ],
    "majora's": [
        "mm_recomp"
    ],
    "mask": [
        "mm_recomp"
    ],
    "64dd": [
        "mm_recomp",
        "oot"
    ],
    "momodora moonlit farewell": [
        "momodoramoonlitfarewell"
    ],
    "momodora: moonlit farewell": [
        "momodoramoonlitfarewell"
    ],
    "momodora:": [
        "momodoramoonlitfarewell"
    ],
    "moonlit": [
        "momodoramoonlitfarewell"
    ],
    "farewell": [
        "momodoramoonlitfarewell"
    ],
    "monster sanctuary": [
        "monster_sanctuary"
    ],
    "monster": [
        "monster_sanctuary"
    ],
    "sanctuary": [
        "monster_sanctuary"
    ],
    "muse dash": [
        "musedash"
    ],
    "muse": [
        "musedash"
    ],
    "dash": [
        "musedash"
    ],
    "metroid zero mission": [
        "mzm"
    ],
    "metroid: zero mission": [
        "mzm"
    ],
    "metroid:": [
        "mzm"
    ],
    "zero": [
        "mzm"
    ],
    "mission": [
        "mzm"
    ],
    "ocarina of time": [
        "oot"
    ],
    "the legend of zelda: ocarina of time": [
        "oot"
    ],
    "ocarina": [
        "oot"
    ],
    "ori and the blind forest": [
        "oribf"
    ],
    "ori": [
        "oribf"
    ],
    "blind": [
        "oribf"
    ],
    "forest": [
        "oribf"
    ],
    "thriller": [
        "sm",
        "sm_map_rando",
        "oribf"
    ],
    "outer wilds": [
        "outer_wilds"
    ],
    "outer": [
        "outer_wilds"
    ],
    "wilds": [
        "outer_wilds"
    ],
    "overcooked! 2": [
        "overcooked2"
    ],
    "overcooked!": [
        "overcooked2"
    ],
    "nintendo switch 2": [
        "smo",
        "overcooked2",
        "stardew_valley"
    ],
    "paper mario": [
        "papermario"
    ],
    "paper": [
        "papermario"
    ],
    "placid plastic duck simulator": [
        "placidplasticducksim"
    ],
    "placid": [
        "placidplasticducksim"
    ],
    "plastic": [
        "placidplasticducksim"
    ],
    "duck": [
        "placidplasticducksim"
    ],
    "pop culture reference": [
        "tmc",
        "rogue_legacy",
        "placidplasticducksim",
        "witness"
    ],
    "pop": [
        "tmc",
        "rogue_legacy",
        "placidplasticducksim",
        "witness"
    ],
    "culture": [
        "tmc",
        "rogue_legacy",
        "placidplasticducksim",
        "witness"
    ],
    "pokemon mystery dungeon explorers of sky": [
        "pmd_eos"
    ],
    "pok\u00e9mon mystery dungeon: explorers of sky": [
        "pmd_eos"
    ],
    "pok\u00e9mon": [
        "pmd_eos",
        "pokemon_crystal",
        "pokemon_emerald",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "dungeon:": [
        "pmd_eos"
    ],
    "explorers": [
        "pmd_eos"
    ],
    "sky": [
        "pmd_eos"
    ],
    "pokemon crystal": [
        "pokemon_crystal"
    ],
    "pok\u00e9mon crystal version": [
        "pokemon_crystal"
    ],
    "version": [
        "pokemon_crystal",
        "pokemon_emerald",
        "pokemon_frlg",
        "pokemon_rb"
    ],
    "punctuation mark above head": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy",
        "tloz_ooa"
    ],
    "punctuation": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy",
        "tloz_ooa"
    ],
    "mark": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy",
        "tloz_ooa"
    ],
    "above": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy",
        "tloz_ooa"
    ],
    "head": [
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy",
        "tloz_ooa"
    ],
    "pokemon emerald": [
        "pokemon_emerald"
    ],
    "pok\u00e9mon emerald version": [
        "pokemon_emerald"
    ],
    "emerald": [
        "pokemon_emerald"
    ],
    "pokemon firered and leafgreen": [
        "pokemon_frlg"
    ],
    "pok\u00e9mon leafgreen version": [
        "pokemon_frlg"
    ],
    "leafgreen": [
        "pokemon_frlg"
    ],
    "pokemon red and blue": [
        "pokemon_rb"
    ],
    "pok\u00e9mon red version": [
        "pokemon_rb"
    ],
    "red": [
        "pokemon_rb"
    ],
    "powerwash simulator": [
        "powerwashsimulator"
    ],
    "powerwash": [
        "powerwashsimulator"
    ],
    "business": [
        "powerwashsimulator",
        "stardew_valley"
    ],
    "ratchet & clank 2": [
        "rac2"
    ],
    "ratchet & clank: going commando": [
        "rac2"
    ],
    "ratchet": [
        "rac2"
    ],
    "clank:": [
        "rac2"
    ],
    "going": [
        "rac2"
    ],
    "commando": [
        "rac2"
    ],
    "raft": [
        "raft"
    ],
    "rogue legacy": [
        "rogue_legacy"
    ],
    "rogue": [
        "rogue_legacy"
    ],
    "playstation vita": [
        "ror1",
        "stardew_valley",
        "timespinner",
        "rogue_legacy",
        "v6",
        "undertale",
        "terraria"
    ],
    "vita": [
        "ror1",
        "stardew_valley",
        "timespinner",
        "rogue_legacy",
        "v6",
        "undertale",
        "terraria"
    ],
    "risk of rain": [
        "ror1"
    ],
    "risk": [
        "ror1",
        "ror2"
    ],
    "rain": [
        "ror1",
        "ror2"
    ],
    "risk of rain 2": [
        "ror2"
    ],
    "sonic adventure 2 battle": [
        "sa2b"
    ],
    "sonic adventure 2: battle": [
        "sa2b"
    ],
    "sonic": [
        "sa2b",
        "sadx",
        "sonic_heroes"
    ],
    "sonic adventure dx": [
        "sadx"
    ],
    "sonic adventure: sonic adventure dx upgrade": [
        "sadx"
    ],
    "adventure:": [
        "sadx"
    ],
    "upgrade": [
        "sadx"
    ],
    "satisfactory": [
        "satisfactory"
    ],
    "sea of thieves": [
        "seaofthieves"
    ],
    "sea": [
        "seaofthieves"
    ],
    "thieves": [
        "seaofthieves"
    ],
    "shivers": [
        "shivers"
    ],
    "point-and-click": [
        "shivers"
    ],
    "a short hike": [
        "shorthike"
    ],
    "short": [
        "shorthike"
    ],
    "hike": [
        "shorthike"
    ],
    "the sims 4": [
        "sims4"
    ],
    "sims": [
        "sims4"
    ],
    "romance": [
        "sims4",
        "stardew_valley"
    ],
    "sly cooper and the thievius raccoonus": [
        "sly1"
    ],
    "sly": [
        "sly1"
    ],
    "cooper": [
        "sly1"
    ],
    "thievius": [
        "sly1"
    ],
    "raccoonus": [
        "sly1"
    ],
    "stealth": [
        "sly1"
    ],
    "super metroid": [
        "sm",
        "sm_map_rando"
    ],
    "super mario 64": [
        "sm64ex",
        "sm64hacks"
    ],
    "rabbit": [
        "sm64ex",
        "sm64hacks",
        "sonic_heroes",
        "tloz_ooa",
        "smo",
        "terraria"
    ],
    "sm64 romhack": [
        "sm64hacks"
    ],
    "super mario odyssey": [
        "smo"
    ],
    "odyssey": [
        "smo"
    ],
    "super mario sunshine": [
        "sms"
    ],
    "sunshine": [
        "sms"
    ],
    "super mario world": [
        "smw"
    ],
    "super metroid map rando": [
        "sm_map_rando"
    ],
    "secret of evermore": [
        "soe"
    ],
    "evermore": [
        "soe"
    ],
    "sonic heroes": [
        "sonic_heroes"
    ],
    "heroes": [
        "sonic_heroes"
    ],
    "symphony of the night": [
        "sotn"
    ],
    "castlevania: symphony of the night": [
        "sotn"
    ],
    "symphony": [
        "sotn"
    ],
    "night": [
        "sotn"
    ],
    "spyro 3": [
        "spyro3"
    ],
    "spyro: year of the dragon": [
        "spyro3"
    ],
    "spyro:": [
        "spyro3"
    ],
    "year": [
        "spyro3"
    ],
    "dragon": [
        "spyro3"
    ],
    "skyward sword": [
        "ss"
    ],
    "the legend of zelda: skyward sword": [
        "ss"
    ],
    "skyward": [
        "ss"
    ],
    "stardew valley": [
        "stardew_valley"
    ],
    "stardew": [
        "stardew_valley"
    ],
    "valley": [
        "stardew_valley"
    ],
    "star fox 64": [
        "star_fox_64"
    ],
    "fox": [
        "star_fox_64"
    ],
    "subnautica": [
        "subnautica"
    ],
    "steamvr": [
        "subnautica"
    ],
    "oculus rift": [
        "subnautica"
    ],
    "oculus": [
        "subnautica"
    ],
    "rift": [
        "subnautica"
    ],
    "star wars episode i racer": [
        "swr"
    ],
    "star wars: episode i - racer": [
        "swr"
    ],
    "episode": [
        "swr"
    ],
    "i": [
        "swr"
    ],
    "-": [
        "swr"
    ],
    "racer": [
        "swr"
    ],
    "dreamcast": [
        "swr"
    ],
    "terraria": [
        "terraria"
    ],
    "windows phone": [
        "terraria"
    ],
    "windows": [
        "terraria"
    ],
    "phone": [
        "terraria"
    ],
    "tetris attack": [
        "tetrisattack"
    ],
    "tetris": [
        "tetrisattack"
    ],
    "attack": [
        "tetrisattack"
    ],
    "timespinner": [
        "timespinner"
    ],
    "the legend of zelda": [
        "tloz"
    ],
    "zelda": [
        "tloz",
        "zelda2"
    ],
    "family computer disk system": [
        "tloz",
        "zelda2"
    ],
    "disk": [
        "tloz",
        "zelda2"
    ],
    "the legend of zelda - oracle of ages": [
        "tloz_ooa"
    ],
    "the legend of zelda: oracle of ages": [
        "tloz_ooa"
    ],
    "oracle": [
        "tloz_oos",
        "tloz_ooa"
    ],
    "ages": [
        "tloz_ooa"
    ],
    "the legend of zelda - oracle of seasons": [
        "tloz_oos"
    ],
    "the legend of zelda: oracle of seasons": [
        "tloz_oos"
    ],
    "seasons": [
        "tloz_oos"
    ],
    "the legend of zelda - phantom hourglass": [
        "tloz_ph"
    ],
    "the legend of zelda: phantom hourglass": [
        "tloz_ph"
    ],
    "phantom": [
        "tloz_ph"
    ],
    "hourglass": [
        "tloz_ph"
    ],
    "the minish cap": [
        "tmc"
    ],
    "the legend of zelda: the minish cap": [
        "tmc"
    ],
    "minish": [
        "tmc"
    ],
    "cap": [
        "tmc"
    ],
    "toontown": [
        "toontown"
    ],
    "toontown online": [
        "toontown"
    ],
    "online": [
        "toontown"
    ],
    "twilight princess": [
        "tp"
    ],
    "the legend of zelda: twilight princess": [
        "tp"
    ],
    "twilight": [
        "tp"
    ],
    "trackmania": [
        "trackmania"
    ],
    "tunic": [
        "tunic"
    ],
    "the wind waker": [
        "tww"
    ],
    "the legend of zelda: the wind waker": [
        "tww"
    ],
    "wind": [
        "tww"
    ],
    "waker": [
        "tww"
    ],
    "tyrian": [
        "tyrian"
    ],
    "tyrian 2000": [
        "tyrian"
    ],
    "2000": [
        "tyrian"
    ],
    "dos": [
        "tyrian"
    ],
    "undertale": [
        "undertale"
    ],
    "vvvvvv": [
        "v6"
    ],
    "ouya": [
        "v6"
    ],
    "wargroove": [
        "wargroove2",
        "wargroove"
    ],
    "warfare": [
        "wargroove2",
        "wargroove"
    ],
    "wargroove 2": [
        "wargroove2"
    ],
    "the witness": [
        "witness"
    ],
    "witness": [
        "witness"
    ],
    "wario land": [
        "wl"
    ],
    "wario land: super mario land 3": [
        "wl"
    ],
    "wario": [
        "wl",
        "wl4"
    ],
    "land:": [
        "wl"
    ],
    "wario land 4": [
        "wl4"
    ],
    "xenoblade x": [
        "xenobladex"
    ],
    "xenoblade chronicles x": [
        "xenobladex"
    ],
    "xenoblade": [
        "xenobladex"
    ],
    "chronicles": [
        "xenobladex"
    ],
    "x": [
        "xenobladex"
    ],
    "yoshi's island": [
        "yoshisisland"
    ],
    "super mario world 2: yoshi's island": [
        "yoshisisland"
    ],
    "yoshi's": [
        "yoshisisland"
    ],
    "island": [
        "yoshisisland"
    ],
    "yu-gi-oh! 2006": [
        "yugioh06"
    ],
    "yu-gi-oh! ultimate masters: world championship tournament 2006": [
        "yugioh06"
    ],
    "ultimate": [
        "yugioh06"
    ],
    "masters:": [
        "yugioh06"
    ],
    "championship": [
        "yugioh06"
    ],
    "tournament": [
        "yugioh06"
    ],
    "2006": [
        "yugioh06"
    ],
    "text": [
        "yugioh06"
    ],
    "yu-gi-oh! dungeon dice monsters": [
        "yugiohddm"
    ],
    "dungeon": [
        "yugiohddm"
    ],
    "dice": [
        "yugiohddm"
    ],
    "monsters": [
        "yugiohddm"
    ],
    "zelda ii: the adventure of link": [
        "zelda2"
    ]
} # type: ignore