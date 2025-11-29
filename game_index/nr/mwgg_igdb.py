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
GAMES_DATA = {
    "adventure": {
        "igdb_id": "12239",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/qzcqrjruhpuge5egkzgj.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Adventure",
        "igdb_name": "Adventure",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Adventure"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "BBC Microcomputer System",
            "Acorn Electron"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 1983
    },
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
            "PlayStation 4",
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
            "swimming",
            "crowdfunding"
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
    "apgo": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Archipela-Go!",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "apsudoku": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Sudoku",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "aquaria": {
        "igdb_id": "7406",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1r7r.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Aquaria",
        "igdb_name": "Aquaria",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Drama"
        ],
        "platforms": [
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac"
        ],
        "storyline": "The world of Aquaria hides the secrets of creation within its depths. The currents that buffet the many diverse plants and animals that live there also carry with them stories of long lost civilizations; of love and war, change and loss.\n\nFrom lush, green kelp forests to dark caves, exploring will be no easy task. But the splendor of the undersea world awaits Naija... and you.\n\nOpen Waters\nCRYSTALLINE BLUE\n\nThe glassy waters of the open sea let you peer far into the distance, and fish and other creatures play beneath the wide canopies of giant, undersea mushrooms.\n\nHere, ruins serve as a clue to Aquaria's long past. Will they lead Naija to the truth?\n\nThe Kelp Forest\nTHE NATURAL WORLD\n\nThe kelp forest teems with life. As light from above pours across the multitudes of strange plants and animals that live here, one cannot help but marvel at the dynamic landscape.\n\nBut beware, its beauty belies the inherent danger inside. Careful not to lose your way.\n\nThe Abyss\nDARKNESS\n\nAs you swim deeper, to where sight cannot reach, the Abyss begins to swallow you whole. The deeper waters of Aquaria have spawned legends of frightening monstrosities that lurk where few things can survive. Are they true?\n\nBeyond\n???\n\nWhat lies beyond? Are there areas deeper than the Abyss? Or as we swim ever upward, can we find the source of the light?\n\nOnly those with great fortitude will come to know and understand the mysteries of Aquaria.",
        "keywords": [
            "exploration",
            "magic",
            "metroidvania",
            "action-adventure",
            "amnesia",
            "swimming",
            "darkness",
            "alternate costumes",
            "world map",
            "save point",
            "underwater gameplay",
            "shape-shifting",
            "plot twist"
        ],
        "release_date": 2007
    },
    "archipidle": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "ArchipIDLE",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "aus": {
        "igdb_id": "72926",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2nok.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "An Untitled Story",
        "igdb_name": "An Untitled Story",
        "age_rating": "NR",
        "rating": [],
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
            "PC (Microsoft Windows)"
        ],
        "storyline": "You are an egg. Leap out of your nest and begin exploring the world, collecting hearts to increase your life and upgrades that can help you jump higher or give you other abilities.",
        "keywords": [
            "ghosts",
            "minigames",
            "metroidvania",
            "action-adventure",
            "bird"
        ],
        "release_date": 2007
    },
    "balatro": {
        "igdb_id": "251833",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9f4g.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar4m0g.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar4m0c.png",
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
    "bfbb": {
        "igdb_id": "2765",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3iyp.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Battle for Bikini Bottom",
        "igdb_name": "SpongeBob SquarePants: Battle For Bikini Bottom",
        "age_rating": "3",
        "rating": [
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
            "Comedy"
        ],
        "platforms": [
            "Xbox",
            "Nintendo GameCube",
            "PlayStation 2"
        ],
        "storyline": "The game revolves around the theme of robots invading Bikini Bottom, SpongeBob's hometown. The robots were created by Plankton, the evil genius owner of the Chum Bucket, who has built a new machine called the Duplicatotron 3000 to produce an army ofjeremih to take over the world using these robots, but only after he creates them does he realizes that the switch on the Duplicatotron has accidentally been switched to \"Don't Obey\" and the robots quickly kick him out of the Chum Bucket before taking over it.\n\nSpongeBob and Patrick were playing with toy robots and wish they would with real robots. Patrick uses his \"magic wishing shell\" to make their wish come true, hoping they will show up tomorrow. SpongeBob wakes up to find that his house has been trashed after thinking he wants to play with a robot. He wanders through the house for a while and receives a fax from Mr. Krabs, stating that he would give SpongeBob a golden spatula for every certain amount of shiny objects he collects for him. Outside, SpongeBob finds a disappointed Plankton, who weaves a tale of lies to the hero, claiming that the robots showed up out of nowhere and kicked him out. Fooled by the diminutive villain, SpongeBob embarks on a perilous quest to find golden spatulas, get rid of the robots, trading shiny objects to Mr. Krabs for golden spatulas, searching for Patrick's stolen socks (that had been taken by the robots) who will give him golden spatulas if he brings back ten socks, and getting Plankton back into the Chum Bucket, including bungee jumping, bubble blowing, learning new bubble moves from Bubble Buddy, and traveling through dreams amongst others.",
        "keywords": [
            "robots",
            "kid friendly",
            "talking animals",
            "3d platformer",
            "anthropomorphism",
            "voice acting",
            "bink video",
            "moving platforms"
        ],
        "release_date": 2003
    },
    "blasphemous": {
        "igdb_id": "26820",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9yoj.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6zd.png",
        "key_art_url": "",
        "game_name": "Blasphemous",
        "igdb_name": "Blasphemous",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Violence",
            "Nudity"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Hack and slash/Beat 'em up",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Horror"
        ],
        "platforms": [
            "PlayStation 4",
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "A foul curse has fallen upon the land of Cvstodia and all its inhabitants - it is simply known as The Miracle.\n\nPlay as The Penitent One - a sole survivor of the massacre of the \u2018Silent Sorrow\u2019. Trapped in an endless cycle of death and rebirth, it\u2019s down to you to free the world from this terrible fate and reach the origin of your anguish.",
        "keywords": [
            "retro",
            "bloody",
            "2d",
            "metroidvania",
            "difficult",
            "side-scrolling",
            "achievements",
            "pixel art",
            "silent protagonist",
            "great soundtrack",
            "moving platforms",
            "soulslike",
            "you can pet the dog",
            "interconnected-world"
        ],
        "release_date": 2019
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
    "bumpstik": {
        "igdb_id": "271950",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co78k5.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Bumper Stickers",
        "igdb_name": "Bumper Stickers Archipelago Edition",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "Puzzle"
        ],
        "themes": [],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2023
    },
    "candybox2": {
        "igdb_id": "62779",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3tqk.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Candy Box 2",
        "igdb_name": "Candy Box 2",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Text"
        ],
        "genres": [
            "Puzzle",
            "Role-playing (RPG)"
        ],
        "themes": [
            "Historical",
            "Comedy"
        ],
        "platforms": [
            "Web browser"
        ],
        "storyline": "",
        "keywords": [
            "medieval",
            "magic",
            "merchants"
        ],
        "release_date": 2013
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
    "cccharles": {
        "igdb_id": "173432",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co62bw.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1fol.png",
        "key_art_url": "",
        "game_name": "Choo-Choo Charles",
        "igdb_name": "Choo-Choo Charles",
        "age_rating": "16",
        "rating": [
            "Violence",
            "Blood"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Horror",
            "Survival",
            "Open world"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "In Choo-Choo Charles you're given the task of eradicating a monster known by the locals as \"Charles\". Nobody knows where he came from, but they know why; to eat the flesh of puny humans. You have a small yellow train, with a map, mounted machine gun, and an exquisite collection of bobble-heads on the dashboard. You'll use this train to get from place to place, while you complete missions for the townspeople, or loot scraps from around the island. Over time you\u2019ll use your scraps to upgrade your train\u2019s speed, armor, and damage. You\u2019ll grow your arsenal, and (hopefully) become an unstoppable force, ready to take on the great and mighty Charles.",
        "keywords": [
            "forest"
        ],
        "release_date": 2022
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
            "lgbtq+",
            "conversation"
        ],
        "release_date": 2018
    },
    "celeste64": {
        "igdb_id": "284430",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7oz4.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2pw4.png",
        "key_art_url": "",
        "game_name": "Celeste 64",
        "igdb_name": "Celeste 64: Fragments of the Mountain",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Third person"
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
            "Linux",
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [
            "female protagonist",
            "lgbtq+"
        ],
        "release_date": 2024
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
            "lgbtq+",
            "conversation"
        ],
        "release_date": 2018
    },
    "chainedechoes": {
        "igdb_id": "117271",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co544u.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6jp.png",
        "key_art_url": "",
        "game_name": "Chained Echoes",
        "igdb_name": "Chained Echoes",
        "age_rating": "16",
        "rating": [
            "Strong Language",
            "Suggestive Themes",
            "Sexual Themes"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Strategy",
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
        "storyline": "Follow a group of heroes as they explore a land filled to the brim with charming characters, fantastic landscapes and vicious foes. Can you bring peace to a continent where war has been waged for generations and betrayal lurks around every corner?",
        "keywords": [
            "jrpg"
        ],
        "release_date": 2022
    },
    "chatipelago": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Chatipelago",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "checksfinder": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "ChecksFinder",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
            "bink video",
            "loot gathering",
            "ambient music"
        ],
        "release_date": 2005
    },
    "clique": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Clique",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
            "crowdfunding",
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
    "dark_souls_2": {
        "igdb_id": "2368",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2eoo.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/bbekzevyyjzwxxp98wp2.png",
        "key_art_url": "",
        "game_name": "Dark Souls II",
        "igdb_name": "Dark Souls II",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Partial Nudity",
            "Violence",
            "Mild Language"
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
            "PC (Microsoft Windows)",
            "Xbox 360"
        ],
        "storyline": "",
        "keywords": [
            "medieval",
            "magic",
            "3d",
            "metroidvania",
            "death",
            "action-adventure",
            "achievements",
            "undead",
            "traps",
            "sequel",
            "sword & sorcery",
            "spider",
            "customizable characters",
            "leveling up",
            "human",
            "bow and arrow",
            "upgradeable weapons",
            "checkpoints",
            "saving the world",
            "side quests",
            "melee",
            "real-time combat",
            "rpg elements",
            "mercenary",
            "boss assistance",
            "fire manipulation",
            "status effects",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": 2014
    },
    "dark_souls_3": {
        "igdb_id": "11133",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaavt.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar4ko8.png",
        "key_art_url": "",
        "game_name": "Dark Souls III",
        "igdb_name": "Dark Souls III",
        "age_rating": "16",
        "rating": [
            "Blood",
            "Violence"
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
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Xbox One"
        ],
        "storyline": "Set in the Kingdom of Lothric, a bell has rung to signal that the First Flame, responsible for maintaining the Age of Fire, is dying out. As has happened many times before, the coming of the Age of Dark produces the undead: cursed beings that rise after death. The Age of Fire can be prolonged by linking the fire, a ritual in which great lords and heroes sacrifice their souls to rekindle the First Flame. However, Prince Lothric, the chosen linker for this age, abandoned his duty and decided to watch the flame die from afar. The bell is the last hope for the Age of Fire, resurrecting previous Lords of Cinder (heroes who linked the flame in past ages) to attempt to link the fire again; however, all but one Lord shirk their duty. Meanwhile, Sulyvahn, a sorcerer from the Painted World of Ariandel, wrongfully proclaims himself Pontiff and seizes power over Irithyll of the Boreal Valley and the returning Anor Londo cathedral from Dark Souls as a tyrant.\n\nThe Ashen One, an Undead who failed to become a Lord of Cinder and thus called an Unkindled, rises and must link the fire by returning Prince Lothric and the defiant Lords of Cinder to their thrones in Firelink Shrine. The Lords include the Abyss Watchers, a legion of warriors sworn by the Old Wolf's Blood which linked their souls into one to protect the land from the Abyss and ultimately locked in an endless battle between each other; Yhorm the Giant, who sacrificed his life for a nation conquered by his ancestor; and Aldrich, who became a Lord of Cinder despite his ravenous appetite for both men and gods. Lothric was raised to link the First Flame but neglected his duties and chose to watch the fire fade instead.\n\nOnce the Ashen One succeeds in returning Lothric and the Lords of Cinder to their thrones, they travel to the ruins of the Kiln of the First Flame. There, they encounter the Soul of Cinder, an amalgamation of all the former Lords of Cinder. Upon defeat, the player can attempt to link the fire or access three other optional endings unlocked by the player's in-game decisions. These include summoning the Fire Keeper to extinguish the flame and begin an age of Dark or killing her in a sudden change of heart. A fourth ending consists of the Ashen One taking the flame for their own, becoming the Lord of Hollows.",
        "keywords": [
            "medieval",
            "3d",
            "death",
            "action-adventure",
            "sequel",
            "sword & sorcery",
            "customizable characters",
            "bink video",
            "human",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": 2016
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
    "dlcquest": {
        "igdb_id": "3004",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2105.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar249v.png",
        "key_art_url": "",
        "game_name": "DLCQuest",
        "igdb_name": "DLC Quest",
        "age_rating": "NR",
        "rating": [],
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
            "Comedy"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox 360"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "digital distribution",
            "deliberately retro",
            "punctuation mark above head"
        ],
        "release_date": 2011
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
    "doom_1993": {
        "igdb_id": "673",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5rav.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar68f.png",
        "key_art_url": "",
        "game_name": "DOOM 1993",
        "igdb_name": "Doom",
        "age_rating": "16",
        "rating": [
            "Intense Violence",
            "Blood and Gore",
            "Violence",
            "Animated Violence",
            "Animated Blood and Gore"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Horror"
        ],
        "platforms": [
            "Windows Mobile",
            "PC-9800 Series",
            "Linux",
            "DOS"
        ],
        "storyline": "The player takes the role of a marine (unnamed to further represent the person playing), \"one of Earth's toughest, hardened in combat and trained for action\", who has been incarcerated on Mars after assaulting a senior officer when ordered to fire upon civilians. There, he works alongside the Union Aerospace Corporation (UAC), a multi-planetary conglomerate and military contractor performing secret experiments on interdimensional travel. Recently, the teleportation has shown signs of anomalies and instability, but the research continues nonetheless.\n\nSuddenly, something goes wrong and creatures from hell swarm out of the teleportation gates on Deimos and Phobos. A defensive response from base security fails to halt the invasion, and the bases are quickly overrun by monsters; all personnel are killed or turned into zombies\n\nA military detachment from Mars travels to Phobos to investigate the incident. The player is tasked with securing the perimeter, as the assault team and their heavy weapons are brought inside. Radio contact soon ceases and the player realizes that he is the only survivor. Being unable to pilot the shuttle off of Phobos by himself, the only way to escape is to go inside and fight through the complexes of the moon base.",
        "keywords": [
            "2.5d",
            "maze",
            "silent protagonist",
            "melee",
            "real-time combat",
            "invisibility"
        ],
        "release_date": 1993
    },
    "doom_ii": {
        "igdb_id": "312",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6iip.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar68g.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar3nqk.png",
        "game_name": "DOOM II",
        "igdb_name": "Doom II: Hell on Earth",
        "age_rating": "16",
        "rating": [
            "Violence",
            "Blood and Gore"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter",
            "Puzzle"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Horror"
        ],
        "platforms": [
            "PC-9800 Series",
            "Tapwave Zodiac",
            "PC (Microsoft Windows)",
            "Mac",
            "DOS"
        ],
        "storyline": "Immediately following the events in Doom, the player once again assumes the role of the unnamed space marine. After defeating the demon invasion of the Mars moon bases and returning from Hell, Doomguy finds that Earth has also been invaded by the demons, who have killed billions of people.\n\nThe humans who survived the attack have developed a plan to build massive spaceships which will carry the remaining survivors into space. Once the ships are ready, the survivors prepare to evacuate Earth. Unfortunately, Earth's only ground spaceport gets taken over by the demons, who place a flame barrier over it, preventing any ships from leaving.",
        "keywords": [
            "bloody",
            "death",
            "2.5d",
            "achievements",
            "multiple endings",
            "traps",
            "artificial intelligence",
            "easter egg",
            "teleportation",
            "sequel",
            "darkness",
            "explosion",
            "digital distribution",
            "voice acting",
            "human",
            "breaking the fourth wall",
            "pop culture reference",
            "game reference",
            "unstable platforms",
            "melee",
            "real-time combat",
            "stat tracking",
            "secret area",
            "walking through walls",
            "difficulty level",
            "rock music",
            "sequence breaking",
            "temporary invincibility",
            "boss assistance",
            "invisibility"
        ],
        "release_date": 1994
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
    "dsr": {
        "igdb_id": "81085",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2uro.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar9u6.png",
        "key_art_url": "",
        "game_name": "Dark Souls Remastered",
        "igdb_name": "Dark Souls: Remastered",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Partial Nudity",
            "Violence"
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
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "magic",
            "3d",
            "undead",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": 2018
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
            "forest",
            "witches",
            "soulslike",
            "conversation"
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
            "Nintendo Switch 2",
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
    "factorio_saws": {
        "igdb_id": "263344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co91k3.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar3845.png",
        "key_art_url": "",
        "game_name": "Factorio - Space Age Without Space",
        "igdb_name": "Factorio: Space Age",
        "age_rating": "NR",
        "rating": [],
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
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "crafting"
        ],
        "release_date": 2024
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
    "frogmonster": {
        "igdb_id": "187372",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7l4c.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1cq0.png",
        "key_art_url": "",
        "game_name": "Frog Monster",
        "igdb_name": "Frogmonster",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "In a world, existing before and still, built through the powerful and cunning minds of the Creators, a new being emerges. The world, once flourishing with enriching creatures and plants, is changing rapidly and dangerously. Beasts, designed by a wicked and corrupt Creator, tear apart and threaten the creatures that still survive. You, the final hope from Melora, a na\u00efve and endangered creator, will journey though the unraveling, unique lands, battle the mindless beasts, and revive the world that once was.",
        "keywords": [
            "3d",
            "metroidvania",
            "atmospheric"
        ],
        "release_date": 2024
    },
    "generic": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Archipelago",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
    "gzdoom": {
        "igdb_id": "307741",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "gzDoom",
        "igdb_name": "GZDoom SM64",
        "age_rating": "NR",
        "rating": [],
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
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": ""
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
            "forest",
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
    "heretic": {
        "igdb_id": "6362",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mwz.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Heretic",
        "igdb_name": "Heretic",
        "age_rating": "M",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter"
        ],
        "themes": [
            "Fantasy",
            "Historical"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac",
            "DOS"
        ],
        "storyline": "",
        "keywords": [
            "bloody",
            "medieval",
            "magic",
            "death",
            "2.5d",
            "undead",
            "sword & sorcery",
            "digital distribution",
            "skeletons",
            "melee",
            "secret area"
        ],
        "release_date": 1994
    },
    "hitman_woa": {
        "igdb_id": "233571",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co620f.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar307p.png",
        "key_art_url": "",
        "game_name": "HITMAN World of Assasination",
        "igdb_name": "Hitman World of Assassination",
        "age_rating": "18",
        "rating": [
            "Drug Reference",
            "Intense Violence",
            "Sexual Themes",
            "Strong Language",
            "Use of Drugs and Alcohol",
            "Blood"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Shooter",
            "Tactical",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Thriller",
            "Stealth",
            "Sandbox"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PlayStation VR",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2023
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
            "crowdfunding",
            "shielded enemies",
            "merchants",
            "fast traveling",
            "controller support",
            "interconnected-world"
        ],
        "release_date": 2017
    },
    "hylics2": {
        "igdb_id": "98469",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co290q.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arjmn.png",
        "key_art_url": "",
        "game_name": "Hylics 2",
        "igdb_name": "Hylics 2",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "First person",
            "Third person",
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Turn-based strategy (TBS)",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "The tyrant Gibby\u2019s minions seek to reconstitute their long-presumed-annihilated master. It\u2019s up to our crescent headed protagonist Wayne to assemble a crew and put a stop to that sort of thing.",
        "keywords": [
            "exploration",
            "retro",
            "3d",
            "jrpg",
            "flight",
            "side-scrolling",
            "stylized",
            "atmospheric",
            "sequel",
            "story rich",
            "great soundtrack"
        ],
        "release_date": 2020
    },
    "inscryption": {
        "igdb_id": "139090",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co401c.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar123g.png",
        "key_art_url": "",
        "game_name": "Inscryption",
        "igdb_name": "Inscryption",
        "age_rating": "16",
        "rating": [
            "Blood",
            "Strong Language",
            "Violence"
        ],
        "player_perspectives": [
            "First person",
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Strategy",
            "Adventure",
            "Indie",
            "Card & Board Game"
        ],
        "themes": [
            "Horror",
            "Mystery"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "Linux",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "From the creator of Pony Island and The Hex comes the latest mind melting, self-destructing love letter to video games. Inscryption is an inky black card-based odyssey that blends the deckbuilding roguelike, escape-room style puzzles, and psychological horror into a blood-laced smoothie. Darker still are the secrets inscrybed upon the cards...\nIn Inscryption you will...\n\nAcquire a deck of woodland creature cards by draft, surgery, and self mutilation\nUnlock the secrets lurking behind the walls of Leshy's cabin\nEmbark on an unexpected and deeply disturbing odyssey",
        "keywords": [],
        "release_date": 2021
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
    "jigsaw": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Jigsaw",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
            "kid friendly",
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
    "kindergarten_2": {
        "igdb_id": "118637",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2vk4.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arpoz.png",
        "key_art_url": "",
        "game_name": "Kindergarten 2",
        "igdb_name": "Kindergarten 2",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "Adventure",
            "Indie"
        ],
        "themes": [],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2019
    },
    "ladx": {
        "igdb_id": "1027",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4o47.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1kl1.png",
        "key_art_url": "",
        "game_name": "Links Awakening DX Beta",
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
            "kid friendly",
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
    "lethal_company": {
        "igdb_id": "212089",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5ive.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1rug.png",
        "key_art_url": "",
        "game_name": "Lethal Company",
        "igdb_name": "Lethal Company",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Indie"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Horror",
            "Comedy"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "You are a contracted worker for the Company. Your job is to collect scrap from abandoned, industrialized moons to meet the Company's profit quota. You can use the cash you earn to travel to new moons with higher risks and rewards--or you can buy fancy suits and decorations for your ship. Experience nature, scanning any creature you find to add them to your bestiary. Explore the wondrous outdoors and rummage through their derelict, steel and concrete underbellies. Just never miss the quota.",
        "keywords": [
            "aliens",
            "exploration"
        ],
        "release_date": 2023
    },
    "lingo": {
        "igdb_id": "189169",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5iy5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1f1q.png",
        "key_art_url": "",
        "game_name": "Lingo",
        "igdb_name": "Lingo",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Puzzle",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Open world"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "3d"
        ],
        "release_date": 2021
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
    "lunacid": {
        "igdb_id": "192291",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7cdv.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1i8t.png",
        "key_art_url": "",
        "game_name": "Lunacid",
        "igdb_name": "Lunacid",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Indie"
        ],
        "themes": [
            "Fantasy",
            "Horror"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "Long ago a great beast arose from the sea and covered the earth in a poison fog. Now those deemed undesirable are thrown into a great well, which has become a pit of chaos and disease. You awaken in a moonlit subterranean world, having been thrown into the Great Well for crimes unknown. The only way out is to go further down and confront the sleeping old one below. On the way there will be many creatures and secrets to discover.",
        "keywords": [],
        "release_date": 2023
    },
    "madou": {
        "igdb_id": "110397",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co40d9.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Madou Monogatari Hanamaru Daiyouchienji",
        "igdb_name": "Madou Monogatari: Hanamaru Daiyouchienji",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Third person",
            "Side view"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "Satellaview",
            "Super Famicom"
        ],
        "storyline": "Arle Nadja is 5 years old and is attending kindergarten, and it's final exam time. But in order to take her final exam, she needs to locate a Final Exam Certificate... In the meantime, a letter arrives which speaks of eight magical gems. Find all eight and take them to the Wizard's Mountain, and you will be granted one wish. Arle decides to search for the gems and wish for her final exam certificate, and along the way she'll have to fight off a gang of local bullies and other various characters you may recognize from the Puyo Puyo series of games!",
        "keywords": [],
        "release_date": 1995
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
    "meritous": {
        "igdb_id": "78479",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/zkameytcg0na8alfswsp.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Meritous",
        "igdb_name": "Meritous",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)"
        ],
        "themes": [],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2008
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
    "nine_sols": {
        "igdb_id": "194821",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4l2s.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1jha.png",
        "key_art_url": "",
        "game_name": "Nine Sols",
        "igdb_name": "Nine Sols",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Use of Alcohol",
            "Language",
            "Violence",
            "Blood"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Hack and slash/Beat 'em up",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction"
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
        "storyline": "In New Kunlun, hero Yi has awakened the 9 rulers of this forsaken realm. To defeat the 9 Sols in the deserted city.\n\n\u201cBecomes one with the way of Tao\u2026\u201d\n\nNew Kunlun, the Solarian\u2019s last sanctuary, has remained quiet for centuries. Inside this vast realm, the ancient gods left mortals with a promised land that is forever protected by the sacred rituals, yet the truth of this world remains unknown to most. Everything changes when Yi, a long forgotten hero from the past, is awoken by a human child.\n\nFollow Yi on his vengeful quest against the 9 Sols, formidable rulers of this forsaken realm, and obliterate any obstacles blocking your way in Sekiro-lite style combat. Explore in unique \u201cTaopunk\u201d setting that blends cyberpunk elements with Taoism and far eastern mythology. Unravel the mysteries of an ancient alien race and learn about the fate of mankind.",
        "keywords": [
            "2d",
            "metroidvania"
        ],
        "release_date": 2024
    },
    "noita": {
        "igdb_id": "52006",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qp1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar7dm.png",
        "key_art_url": "",
        "game_name": "Noita",
        "igdb_name": "Noita",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Role-playing (RPG)",
            "Simulator",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Sandbox"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [
            "magic",
            "roguelite"
        ],
        "release_date": 2020
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
    "openrct2": {
        "igdb_id": "80720",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ngq.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "OpenRCT2",
        "igdb_name": "OpenRCT2",
        "age_rating": "NR",
        "rating": [],
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
            "Business",
            "4X (explore, expand, exploit, and exterminate)"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "death",
            "maze",
            "kid friendly",
            "easter egg",
            "explosion"
        ],
        "release_date": 2014
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
            "forest",
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
    "osrs": {
        "igdb_id": "79824",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mo1.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6ki.png",
        "key_art_url": "",
        "game_name": "Old School Runescape",
        "igdb_name": "Old School RuneScape",
        "age_rating": "16",
        "rating": [
            "Crude Humor",
            "Fantasy Violence",
            "Use of Alcohol",
            "Users Interact"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Text"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Adventure"
        ],
        "themes": [
            "Fantasy",
            "Sandbox",
            "Open world"
        ],
        "platforms": [
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2013
    },
    "osu": {
        "igdb_id": "3012",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8a4m.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar15xc.png",
        "key_art_url": "",
        "game_name": "osu!",
        "igdb_name": "Osu!",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Auditory"
        ],
        "genres": [
            "Music",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "anime",
            "stat tracking",
            "difficulty level"
        ],
        "release_date": 2007
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coasbb.png",
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
    "paint": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Paint",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
    "peak": {
        "igdb_id": "360757",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "PEAK",
        "igdb_name": "Peak",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [],
        "genres": [],
        "themes": [],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2025
    },
    "peaks_of_yore": {
        "igdb_id": "238690",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8zzc.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2712.png",
        "key_art_url": "",
        "game_name": "Peaks of Yore",
        "igdb_name": "Peaks of Yore",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "Platform",
            "Adventure",
            "Indie"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2023
    },
    "phoa": {
        "igdb_id": "136805",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2n5s.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arc27.png",
        "key_art_url": "",
        "game_name": "Phoenotopia: Awakening",
        "igdb_name": "Phoenotopia: Awakening",
        "age_rating": "7",
        "rating": [
            "Fantasy Violence",
            "Mild Language",
            "Use of Alcohol",
            "Comic Mischief"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
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
            "Fantasy",
            "Open world"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "Mac",
            "Xbox One",
            "Nintendo Switch"
        ],
        "storyline": "The story follows the adventures of a girl named Gale, who sets out into the world to find out what happened to her village after a mysterious object descends from the sky and abducts almost everyone. Gale embarks on an epic quest that takes her to many different locations, solving puzzles, finding friends, and battling ferocious enemies, in order to find answers.",
        "keywords": [
            "metroidvania",
            "fishing",
            "side-scrolling",
            "world map"
        ],
        "release_date": 2020
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
    "poe": {
        "igdb_id": "1911",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1n6w.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arjpc.png",
        "key_art_url": "",
        "game_name": "Path of Exile",
        "igdb_name": "Path of Exile",
        "age_rating": "18",
        "rating": [
            "Intense Violence",
            "Blood and Gore",
            "Sexual Themes",
            "Language",
            "Nudity"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Role-playing (RPG)",
            "Hack and slash/Beat 'em up",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Horror"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation 5",
            "Mac",
            "Xbox One"
        ],
        "storyline": "All exiles are given the same choice: to sink or swim. Those that don't drown will reach the forsaken shores of Wraeclast, where the only welcome is the clinging embrace of undeath. However, a small band of survivors has managed to hold fast in a ruined lighthouse, desperately repelling both the grasping undead and the manic scavengers that stubbornly cling to their last shreds of humanity. Under the commanding gaze of Axiom Prison, snarling goatmen roam the craggy bluffs, always keeping their cloven feet well clear of the rhoa-infested swamps in the lowlands. All along the coast, rotting shipwrecks litter the shoreline, the spirits of the stranded sailors still haunting the wreckages of their ill-fated ships, waiting to take out their sorrow and rage on those who yet live. All the while, the Siren herself continues her sweet, sad song, luring ever more ships to their watery graves.\n\nFarther inland, through the twisting caves and darkened forests, the ruins of civilisation become more apparent. The ravages of time have worn many buildings to rubble, and stripped away decaying flesh, leaving only grotesquely grinning bones. The dark, fetid caves and underground passages are a clattering refuge for these skeletal ranks, while the open forests and riverways brim with monstrous beasts with a taste for blood. Recently, ragtag groups of bloodthirsty bandits have built fortified camps in the forest, openly challenging one another while extorting food and supplies from the small, struggling village that sits between them atop a stone dam. Ignored by the squabbling bandits, strange newcomers clad in black armor have been seen skulking around various large ruins, their purpose both mysterious yet unsettling.\n\nAtop a sheer cliff of ruptured mantle, straddling the river feeding a mighty waterfall, lies the fallen capital of the Eternal Empire. Its former glory rots amid the ruins of a blasted cityscape, the buildings decrepit and mouldering. But Sarn is far from uninhabited. Many of the original citizens still lurk the dark recesses, their humanity washed clean by the cataclysm of centuries past. These Undying monsters roam the city at night and skulk the shadows during the day, for the naked sunlight is anathema to their shrivelled, leathery skin. The sun-scarred days are far from peaceful, however. A legion of soldiers from Oriath has occupied the area to the west of the river, and is fighting an all-out war against the multifarious denizens of the city. Every day their black-clad soldiers battle twisted insects that scuttle and breed, feasting on anything that moves. Every day they throw battalions against the army of floating, red Ribbons that eviscerate all who trespass on their domain. Every day they skirmish against a small group of exiles who have barricaded themselves on a small island in the middle of the river, caught between certain death on both sides.",
        "keywords": [
            "bloody",
            "magic",
            "3d",
            "leveling up",
            "bink video",
            "bow and arrow",
            "potion",
            "fast traveling"
        ],
        "release_date": 2013
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
            "kid friendly",
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
            "kid friendly",
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
    "pseudoregalia": {
        "igdb_id": "259465",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6vcy.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2fmq.png",
        "key_art_url": "",
        "game_name": "Pseudoregalia",
        "igdb_name": "Pseudoregalia: Jam Ver.",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
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
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [
            "metroidvania"
        ],
        "release_date": 2023
    },
    "quake": {
        "igdb_id": "333",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9bg9.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arhee.png",
        "key_art_url": "",
        "game_name": "Quake 1",
        "igdb_name": "Quake",
        "age_rating": "T",
        "rating": [
            "Animated Blood and Gore",
            "Animated Violence"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Horror",
            "Historical",
            "Comedy"
        ],
        "platforms": [
            "Zeebo",
            "Linux",
            "PC (Microsoft Windows)",
            "Mac",
            "DOS",
            "Amiga",
            "Sega Saturn",
            "Legacy Mobile Device"
        ],
        "storyline": "The player takes the role of a protagonist known as Ranger who was sent into a portal in order to stop an enemy code-named \"Quake\". The government had been experimenting with teleportation technology and developed a working prototype called a \"Slipgate\"; the mysterious Quake compromised the Slipgate by connecting it with its own teleportation system, using it to send death squads to the \"Human\" dimension in order to test the martial capabilities of Humanity.",
        "keywords": [
            "aliens",
            "bloody",
            "medieval",
            "death",
            "backtracking",
            "silent protagonist",
            "swimming",
            "explosion",
            "digital distribution",
            "human",
            "polygonal 3d",
            "auto-aim",
            "melee",
            "real-time combat",
            "underwater gameplay",
            "mercenary",
            "moving platforms",
            "temporary invincibility",
            "speedrun",
            "invisibility",
            "retroachievements"
        ],
        "release_date": 1996
    },
    "rabi_ribi": {
        "igdb_id": "28545",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4eck.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arb6h.png",
        "key_art_url": "",
        "game_name": "Rabi-Ribi",
        "igdb_name": "Rabi-Ribi",
        "age_rating": "12",
        "rating": [
            "Fantasy Violence",
            "Suggestive Themes",
            "Partial Nudity"
        ],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Role-playing (RPG)",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Fantasy"
        ],
        "platforms": [
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "PlayStation Vita",
            "Nintendo Switch"
        ],
        "storyline": "The main character is Erina, formerly a normal rabbit who became transformed into a human bunny girl, and awakens in an unknown place. Shortly after she is magically sent back to Rabi Rabi Island, her home island. Lost and confused, searching for her master is the best thing to understand what's going on. Along the way, Erina befriends Ribbon, a fairy seeking freedom and independence and becomes Erina's sidekick.",
        "keywords": [
            "exploration",
            "anime",
            "magic",
            "2d",
            "metroidvania",
            "rabbit",
            "difficult",
            "female protagonist",
            "action-adventure",
            "fairy",
            "cute",
            "crowdfunding",
            "great soundtrack",
            "conversation"
        ],
        "release_date": 2016
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
    "residentevil2remake": {
        "igdb_id": "19686",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ir3.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/qqrtgvipdy3t5xgc5u6q.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar4owg.png",
        "game_name": "Resident Evil 2 Remake",
        "igdb_name": "Resident Evil 2",
        "age_rating": "18",
        "rating": [
            "Strong Language",
            "Intense Violence",
            "Blood and Gore"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Shooter",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror",
            "Survival"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One"
        ],
        "storyline": "Players join rookie police officer Leon Kennedy and college student Claire Redfield, who are thrust together by a disastrous outbreak in Raccoon City that transformed its population into deadly zombies. Both Leon and Claire have their own separate playable campaigns, allowing players to see the story from both characters\u2019 perspectives. The fate of these two fan favorite characters is in the player's hands as they work together to survive and get to the bottom of what is behind the terrifying attack on the city.",
        "keywords": [
            "bloody"
        ],
        "release_date": 2019
    },
    "residentevil3remake": {
        "igdb_id": "115115",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co22l7.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar6e9.png",
        "key_art_url": "",
        "game_name": "Resident Evil 3 Remake",
        "igdb_name": "Resident Evil 3",
        "age_rating": "18",
        "rating": [
            "Intense Violence",
            "Strong Language",
            "Blood and Gore"
        ],
        "player_perspectives": [
            "Third person"
        ],
        "genres": [
            "Shooter",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Horror",
            "Survival"
        ],
        "platforms": [
            "Xbox Series X|S",
            "PlayStation 4",
            "PC (Microsoft Windows)",
            "iOS",
            "PlayStation 5",
            "Mac",
            "Xbox One"
        ],
        "storyline": "A series of strange disappearances have been occurring in the American Midwest within a place called Racoon City. A specialist squad of the police force known as S.T.A.R.S. has been investigating the case, and have determined that the pharmaceutical company Umbrella and their biological weapon, the T-Virus, are behind the incidents. Jill Valentine and the other surviving S.T.A.R.S. members try to make this truth known, but find that the police department itself is under Umbrella's sway and their reports are rejected out of hand. With the viral plague spreading through the town and to her very doorstep, Jill is determined to survive. However, an extremely powerful pursuer has already been dispatched to eliminate her.",
        "keywords": [],
        "release_date": 2020
    },
    "rimworld": {
        "igdb_id": "9789",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaaqj.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ardhk.png",
        "key_art_url": "",
        "game_name": "Rimworld",
        "igdb_name": "RimWorld",
        "age_rating": "16",
        "rating": [
            "Blood",
            "Suggestive Themes",
            "Violence",
            "Use of Drugs and Alcohol"
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
            "Science fiction",
            "Survival"
        ],
        "platforms": [
            "Linux",
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "RimWorld follows three survivors from a crashed space liner as they build a colony on a frontier world at the rim of known space. Inspired by the space western vibe of Firefly, the deep simulation of Dwarf Fortress, and the epic scale of Dune and Warhammer 40,000.\n\nManage colonists' moods, needs, thoughts, individual wounds, and illnesses. Engage in deeply-simulated small-team gunplay. Fashion structures, weapons, and apparel from metal, wood, stone, cloth, or exotic, futuristic materials. Fight pirate raiders, hostile tribes, rampaging animals and ancient killing machines. Discover a new generated world each time you play. Build colonies in biomes ranging from desert to jungle to tundra, each with unique flora and fauna. Manage and develop colonists with unique backstories, traits, and skills. Learn to play easily with the help of an intelligent and unobtrusive AI tutor.",
        "keywords": [],
        "release_date": 2018
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
            "crowdfunding",
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
    "saving_princess": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Saving Princess",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "sc2": {
        "igdb_id": "239",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1tnn.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/hrlspaxbr5en04afvnox.png",
        "key_art_url": "",
        "game_name": "Starcraft 2",
        "igdb_name": "StarCraft II: Wings of Liberty",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Language",
            "Suggestive Themes",
            "Use of Alcohol and Tobacco",
            "Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Real Time Strategy (RTS)",
            "Strategy"
        ],
        "themes": [
            "Action",
            "Science fiction",
            "Warfare"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "human",
            "side quests",
            "mercenary"
        ],
        "release_date": 2010
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
    "shapez": {
        "igdb_id": "134826",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4tfx.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arxzw.png",
        "key_art_url": "",
        "game_name": "shapez",
        "igdb_name": "Shapez",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Puzzle",
            "Simulator",
            "Strategy",
            "Indie"
        ],
        "themes": [
            "Sandbox"
        ],
        "platforms": [
            "Linux",
            "Android",
            "PC (Microsoft Windows)",
            "iOS",
            "Mac"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2020
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
        "artwork_url": "",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar4l4d.png",
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
            "forest",
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
    "simpsonshitnrun": {
        "igdb_id": "2844",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2uk7.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "The Simpsons Hit And Run",
        "igdb_name": "The Simpsons: Hit & Run",
        "age_rating": "T",
        "rating": [
            "Comic Mischief",
            "Mild Language",
            "Violence",
            "Crude Humor",
            "Alcohol Reference",
            "Cartoon Violence"
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
            "Comedy",
            "Open world"
        ],
        "platforms": [
            "Xbox",
            "Nintendo GameCube",
            "PC (Microsoft Windows)",
            "PlayStation 2"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "ghosts",
            "time limit",
            "wall jump",
            "explosion",
            "countdown timer",
            "alternate costumes",
            "voice acting",
            "bink video",
            "human",
            "polygonal 3d",
            "breaking the fourth wall",
            "pop culture reference",
            "stat tracking",
            "punctuation mark above head",
            "been here before",
            "lgbtq+"
        ],
        "release_date": 2003
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
    "smz3": {
        "igdb_id": "210231",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5zep.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "SMZ3",
        "igdb_name": "Super Metroid and A Link to the Past Crossover Randomizer",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Platform",
            "Adventure"
        ],
        "themes": [
            "Action",
            "Open world"
        ],
        "platforms": [
            "Super Nintendo Entertainment System"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2018
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
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar4l4o.png",
        "key_art_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/ar4lch.png",
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
    "spire": {
        "igdb_id": "296831",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co82c5.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar2w86.png",
        "key_art_url": "",
        "game_name": "Slay the Spire",
        "igdb_name": "Slay the Spire II",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Strategy",
            "Indie",
            "Card & Board Game"
        ],
        "themes": [
            "Fantasy"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "",
        "keywords": [
            "roguelike"
        ],
        "release_date": 2026
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
    "tboir": {
        "igdb_id": "310643",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8kxf.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar335q.png",
        "key_art_url": "",
        "game_name": "The Binding of Isaac Repentance",
        "igdb_name": "The Binding of Isaac: Repentance",
        "age_rating": "16",
        "rating": [
            "Blood and Gore",
            "Crude Humor",
            "Violence"
        ],
        "player_perspectives": [
            "Bird view / Isometric"
        ],
        "genres": [
            "Shooter",
            "Indie"
        ],
        "themes": [],
        "platforms": [
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2021
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
            "crowdfunding",
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
    "ttyd": {
        "igdb_id": "328663",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9p1w.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Paper Mario The Thousand Year Door",
        "igdb_name": "Paper Mario: The Thousand-Year Door",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "Puzzle"
        ],
        "themes": [],
        "platforms": [
            "Web browser"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": 2004
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
            "forest",
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
    "ufo50": {
        "igdb_id": "54555",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co24v0.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/ar1udh.png",
        "key_art_url": "",
        "game_name": "UFO 50",
        "igdb_name": "UFO 50",
        "age_rating": "12",
        "rating": [
            "Blood",
            "Violence",
            "Simulated Gambling",
            "Use of Drugs"
        ],
        "player_perspectives": [
            "Bird view / Isometric",
            "Side view"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Puzzle",
            "Role-playing (RPG)",
            "Strategy",
            "Adventure",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Nintendo Switch"
        ],
        "storyline": "",
        "keywords": [
            "digital distribution",
            "deliberately retro"
        ],
        "release_date": 2024
    },
    "ultrakill": {
        "igdb_id": "124333",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co46s3.png",
        "artwork_url": "https://images.igdb.com/igdb/image/upload/t_logo_med/arlq1.png",
        "key_art_url": "",
        "game_name": "ULTRAKILL",
        "igdb_name": "Ultrakill",
        "age_rating": "M",
        "rating": [
            "Violence",
            "Blood and Gore"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Shooter",
            "Platform",
            "Indie",
            "Arcade"
        ],
        "themes": [
            "Action",
            "Fantasy",
            "Science fiction"
        ],
        "platforms": [
            "PC (Microsoft Windows)"
        ],
        "storyline": "Mankind has gone extinct and the only beings left on earth are machines fueled by blood.\nBut now that blood is starting to run out on the surface...\n\nMachines are racing to the depths of Hell in search of more.",
        "keywords": [
            "bloody",
            "robots",
            "stylized",
            "silent protagonist",
            "great soundtrack",
            "rock music"
        ],
        "release_date": 2020
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
            "conversation",
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
            "controller support",
            "conversation"
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
            "bink video",
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
    "wordipelago": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Wordipelago",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
    "yachtdice": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Yacht Dice",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
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
    },
    "zillion": {
        "igdb_id": "18141",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7xxj.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Zillion",
        "igdb_name": "Zillion",
        "age_rating": "NR",
        "rating": [],
        "player_perspectives": [
            "Side view"
        ],
        "genres": [
            "Platform",
            "Puzzle"
        ],
        "themes": [
            "Science fiction"
        ],
        "platforms": [
            "Sega Master System/Mark III"
        ],
        "storyline": "Are you ready for the ultimate danger? You're alone, outnumbered and there's no guarantee you'll make it alive. You're J.J. Your objective: secretly infiltrate the underground labyrinth of The Norsa Empire and steal their plans for domination. Armed with the ultra speed and power of the Zillion Laser, your mission is complex. And sheer strength will not win this one alone. You'll need more brains than brawn in this sophisticated operation. So, how will you think your way to victory? With cunning strategy and memory to guide you successfully through the maze which awaits. Where once inside, you'll find the information needed to destroy the Norsas and restore peace forever.",
        "keywords": [
            "anime",
            "metroidvania",
            "action-adventure"
        ],
        "release_date": 1987
    },
    "zork_grand_inquisitor": {
        "igdb_id": "1955",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kql.png",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Zork Grand Inquisitor",
        "igdb_name": "Zork: Grand Inquisitor",
        "age_rating": "T",
        "rating": [
            "Comic Mischief",
            "Suggestive Themes",
            "Use of Alcohol and Tobacco"
        ],
        "player_perspectives": [
            "First person"
        ],
        "genres": [
            "Point-and-click",
            "Puzzle",
            "Adventure"
        ],
        "themes": [
            "Fantasy",
            "Comedy"
        ],
        "platforms": [
            "PC (Microsoft Windows)",
            "Mac"
        ],
        "storyline": "",
        "keywords": [
            "magic"
        ],
        "release_date": 1997
    },
    "_debug": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "debug",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "_manual": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Manual",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    },
    "_tracker": {
        "igdb_id": "",
        "cover_url": "",
        "artwork_url": "",
        "key_art_url": "",
        "game_name": "Universal Tracker",
        "igdb_name": "",
        "age_rating": "MW",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "Multiplayer"
        ],
        "themes": [],
        "platforms": [
            "Archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": 2025
    }
}  # type: ignore  # noqa: F821

SEARCH_INDEX = {
    "popular": [
        "alttp",
        "sc2",
        "oot",
        "kh2",
        "hk",
        "sm64ex"
    ],
    "adventure": [
        "rabi_ribi",
        "albw",
        "banjo_tooie",
        "stardew_valley",
        "oot",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "seaofthieves",
        "v6",
        "oribf",
        "sly1",
        "dark_souls_3",
        "k64",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "frogmonster",
        "faxanadu",
        "kindergarten_2",
        "jakanddaxter",
        "tmc",
        "witness",
        "ladx",
        "metroidfusion",
        "subnautica",
        "messenger",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "lego_star_wars_tcs",
        "peaks_of_yore",
        "dsr",
        "cv64",
        "alttp",
        "sadx",
        "shivers",
        "pseudoregalia",
        "smo",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "getting_over_it",
        "aquaria",
        "metroidprime",
        "residentevil2remake",
        "sa2b",
        "earthbound",
        "rac2",
        "hitman_woa",
        "pokemon_crystal",
        "terraria",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "monster_sanctuary",
        "sms",
        "sotn",
        "shorthike",
        "sm",
        "pokemon_frlg",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "xenobladex",
        "ff1",
        "luigismansion",
        "dredge",
        "lingo",
        "kh2",
        "crosscode",
        "tloz",
        "zork_grand_inquisitor",
        "bfbb",
        "kh1",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "tww",
        "dark_souls_2",
        "adventure",
        "hcniko",
        "cvcotm",
        "noita",
        "mlss",
        "tloz_ph",
        "pokemon_emerald",
        "dkc3",
        "residentevil3remake",
        "enderlilies",
        "satisfactory",
        "undertale",
        "tloz_oos",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "wl4",
        "gstla",
        "cccharles",
        "chainedechoes",
        "ahit",
        "sm_map_rando",
        "smw",
        "tloz_ooa",
        "mm2",
        "tp",
        "poe",
        "sonic_heroes",
        "zelda2",
        "hk",
        "aus",
        "ff4fe",
        "mzm",
        "dk64",
        "ss",
        "kdl3",
        "spyro3",
        "papermario",
        "dw1"
    ],
    "bird view / isometric": [
        "albw",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "ufo50",
        "openrct2",
        "sc2",
        "alttp",
        "tunic",
        "ff1",
        "undertale",
        "shapez",
        "tloz_oos",
        "mmbn3",
        "hylics2",
        "ctjot",
        "dredge",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "gstla",
        "civ_6",
        "ffta",
        "factorio",
        "diddy_kong_racing",
        "hades",
        "pokemon_rb",
        "crosscode",
        "smz3",
        "tboir",
        "cuphead",
        "tloz",
        "chainedechoes",
        "yugiohddm",
        "placidplasticducksim",
        "yugioh06",
        "landstalker",
        "tloz_ooa",
        "adventure",
        "balatro",
        "shorthike",
        "against_the_storm",
        "overcooked2",
        "earthbound",
        "pmd_eos",
        "ladx",
        "poe",
        "sims4",
        "sonic_heroes",
        "tmc",
        "tyrian",
        "brotato",
        "ff4fe",
        "rimworld",
        "pokemon_crystal",
        "tloz_ph",
        "factorio_saws",
        "osrs",
        "spyro3",
        "wargroove",
        "ffmq",
        "sms",
        "wargroove2",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "bird": [
        "dkc3",
        "albw",
        "banjo_tooie",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "openrct2",
        "ufo50",
        "sc2",
        "alttp",
        "tunic",
        "ff1",
        "undertale",
        "shapez",
        "tloz_oos",
        "mmbn3",
        "pokemon_frlg",
        "hylics2",
        "ctjot",
        "dredge",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "gstla",
        "civ_6",
        "ffta",
        "factorio",
        "diddy_kong_racing",
        "hades",
        "pokemon_rb",
        "crosscode",
        "smz3",
        "tboir",
        "cuphead",
        "tloz",
        "chainedechoes",
        "yugiohddm",
        "placidplasticducksim",
        "yugioh06",
        "landstalker",
        "tloz_ooa",
        "adventure",
        "balatro",
        "shorthike",
        "against_the_storm",
        "overcooked2",
        "earthbound",
        "pmd_eos",
        "ladx",
        "poe",
        "sims4",
        "sonic_heroes",
        "tmc",
        "aus",
        "brotato",
        "ff4fe",
        "rimworld",
        "tyrian",
        "pokemon_crystal",
        "tloz_ph",
        "factorio_saws",
        "osrs",
        "rogue_legacy",
        "spyro3",
        "wargroove",
        "ffmq",
        "sms",
        "wargroove2",
        "dw1",
        "pokemon_emerald",
        "minecraft"
    ],
    "view": [
        "rabi_ribi",
        "albw",
        "meritous",
        "stardew_valley",
        "openrct2",
        "celeste_open_world",
        "tunic",
        "zillion",
        "v6",
        "ctjot",
        "oribf",
        "k64",
        "inscryption",
        "animal_well",
        "hades",
        "ffta",
        "tboir",
        "dkc",
        "faxanadu",
        "tetrisattack",
        "overcooked2",
        "pmd_eos",
        "tmc",
        "ladx",
        "megamix",
        "brotato",
        "metroidfusion",
        "messenger",
        "wl",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "soe",
        "alttp",
        "shapez",
        "mmbn3",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "yugiohddm",
        "mm3",
        "getting_over_it",
        "aquaria",
        "placidplasticducksim",
        "earthbound",
        "pokemon_crystal",
        "terraria",
        "mmx3",
        "monster_sanctuary",
        "ffmq",
        "sms",
        "sotn",
        "shorthike",
        "sm",
        "pokemon_frlg",
        "phoa",
        "ufo50",
        "ff1",
        "musedash",
        "dredge",
        "factorio",
        "diddy_kong_racing",
        "crosscode",
        "tloz",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "landstalker",
        "lufia2ac",
        "adventure",
        "against_the_storm",
        "cvcotm",
        "noita",
        "mlss",
        "factorio_saws",
        "wargroove",
        "tloz_ph",
        "pokemon_emerald",
        "dkc3",
        "madou",
        "sc2",
        "enderlilies",
        "undertale",
        "tloz_oos",
        "celeste",
        "hylics2",
        "wl4",
        "gstla",
        "civ_6",
        "chainedechoes",
        "marioland2",
        "sm_map_rando",
        "smw",
        "tloz_ooa",
        "spire",
        "balatro",
        "mm2",
        "sims4",
        "yugioh06",
        "poe",
        "sonic_heroes",
        "zelda2",
        "hk",
        "tyrian",
        "aus",
        "rimworld",
        "ff4fe",
        "dkc2",
        "mzm",
        "yoshisisland",
        "kdl3",
        "spyro3",
        "papermario",
        "wargroove2",
        "dw1"
    ],
    "/": [
        "albw",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "ufo50",
        "openrct2",
        "sc2",
        "alttp",
        "tunic",
        "ff1",
        "undertale",
        "shapez",
        "tloz_oos",
        "mmbn3",
        "hylics2",
        "ctjot",
        "dredge",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "gstla",
        "civ_6",
        "ffta",
        "factorio",
        "diddy_kong_racing",
        "hades",
        "pokemon_rb",
        "crosscode",
        "smz3",
        "tboir",
        "cuphead",
        "tloz",
        "chainedechoes",
        "yugiohddm",
        "placidplasticducksim",
        "yugioh06",
        "landstalker",
        "tloz_ooa",
        "adventure",
        "balatro",
        "shorthike",
        "against_the_storm",
        "overcooked2",
        "earthbound",
        "pmd_eos",
        "ladx",
        "poe",
        "sims4",
        "sonic_heroes",
        "tmc",
        "tyrian",
        "brotato",
        "ff4fe",
        "rimworld",
        "pokemon_crystal",
        "tloz_ph",
        "factorio_saws",
        "osrs",
        "spyro3",
        "wargroove",
        "ffmq",
        "sms",
        "wargroove2",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "isometric": [
        "albw",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "ufo50",
        "openrct2",
        "sc2",
        "alttp",
        "tunic",
        "ff1",
        "undertale",
        "shapez",
        "tloz_oos",
        "mmbn3",
        "hylics2",
        "ctjot",
        "dredge",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "gstla",
        "civ_6",
        "ffta",
        "factorio",
        "diddy_kong_racing",
        "hades",
        "pokemon_rb",
        "crosscode",
        "smz3",
        "tboir",
        "cuphead",
        "tloz",
        "chainedechoes",
        "yugiohddm",
        "placidplasticducksim",
        "yugioh06",
        "landstalker",
        "tloz_ooa",
        "adventure",
        "balatro",
        "shorthike",
        "against_the_storm",
        "overcooked2",
        "earthbound",
        "pmd_eos",
        "ladx",
        "poe",
        "sims4",
        "sonic_heroes",
        "tmc",
        "tyrian",
        "brotato",
        "ff4fe",
        "rimworld",
        "pokemon_crystal",
        "tloz_ph",
        "factorio_saws",
        "osrs",
        "spyro3",
        "wargroove",
        "ffmq",
        "sms",
        "wargroove2",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "fantasy": [
        "rabi_ribi",
        "albw",
        "banjo_tooie",
        "stardew_valley",
        "lunacid",
        "oot",
        "celeste_open_world",
        "tunic",
        "heretic",
        "seaofthieves",
        "v6",
        "ctjot",
        "oribf",
        "dark_souls_3",
        "hades",
        "ffta",
        "frogmonster",
        "faxanadu",
        "pmd_eos",
        "tmc",
        "ladx",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "dsr",
        "alttp",
        "pseudoregalia",
        "smo",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "pokemon_rb",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "yugiohddm",
        "aquaria",
        "fm",
        "earthbound",
        "pokemon_crystal",
        "terraria",
        "mm_recomp",
        "monster_sanctuary",
        "ffmq",
        "shorthike",
        "pokemon_frlg",
        "phoa",
        "ff1",
        "kh2",
        "tloz",
        "zork_grand_inquisitor",
        "kh1",
        "ror1",
        "tww",
        "landstalker",
        "dark_souls_2",
        "lufia2ac",
        "adventure",
        "against_the_storm",
        "noita",
        "mlss",
        "wargroove",
        "tloz_ph",
        "pokemon_emerald",
        "madou",
        "enderlilies",
        "undertale",
        "tloz_oos",
        "celeste",
        "hylics2",
        "gstla",
        "civ_6",
        "chainedechoes",
        "ahit",
        "smw",
        "spire",
        "sims4",
        "tp",
        "yugioh06",
        "poe",
        "zelda2",
        "hk",
        "ff4fe",
        "dkc2",
        "ss",
        "yoshisisland",
        "papermario",
        "ultrakill",
        "wargroove2"
    ],
    "bbc microcomputer system": [
        "adventure"
    ],
    "bbc": [
        "adventure"
    ],
    "microcomputer": [
        "adventure"
    ],
    "system": [
        "dkc3",
        "soe",
        "xenobladex",
        "alttp",
        "ff1",
        "gstla",
        "ffta",
        "dkc",
        "smz3",
        "tloz",
        "sm",
        "kh1",
        "mm3",
        "sm_map_rando",
        "smw",
        "faxanadu",
        "lufia2ac",
        "adventure",
        "tetrisattack",
        "earthbound",
        "zelda2",
        "ff4fe",
        "dkc2",
        "yoshisisland",
        "pokemon_crystal",
        "kdl3",
        "mlss",
        "papermario",
        "mmx3",
        "ffmq",
        "pokemon_emerald"
    ],
    "acorn electron": [
        "adventure"
    ],
    "acorn": [
        "adventure"
    ],
    "electron": [
        "adventure"
    ],
    "against the storm": [
        "against_the_storm"
    ],
    "against": [
        "against_the_storm"
    ],
    "the": [
        "lego_star_wars_tcs",
        "dkc3",
        "banjo_tooie",
        "albw",
        "simpsonshitnrun",
        "oot",
        "enderlilies",
        "alttp",
        "undertale",
        "tloz_oos",
        "smo",
        "seaofthieves",
        "oribf",
        "sly1",
        "blasphemous",
        "k64",
        "gstla",
        "hades",
        "ffta",
        "tboir",
        "dkc",
        "diddy_kong_racing",
        "smz3",
        "tloz",
        "ttyd",
        "tww",
        "doom_ii",
        "dark_souls_2",
        "spire",
        "lufia2ac",
        "tloz_ooa",
        "sims4",
        "hcniko",
        "against_the_storm",
        "earthbound",
        "jakanddaxter",
        "ladx",
        "cvcotm",
        "overcooked2",
        "tmc",
        "tp",
        "witness",
        "zelda2",
        "dkc2",
        "ss",
        "metroidfusion",
        "messenger",
        "mlss",
        "spyro3",
        "papermario",
        "mm_recomp",
        "rogue_legacy",
        "terraria",
        "sotn",
        "tloz_ph",
        "celeste64"
    ],
    "storm": [
        "against_the_storm"
    ],
    "real time strategy (rts)": [
        "rimworld",
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3"
    ],
    "real": [
        "rimworld",
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3"
    ],
    "time": [
        "simpsonshitnrun",
        "oot",
        "openrct2",
        "outer_wilds",
        "sc2",
        "alttp",
        "tloz_oos",
        "mmbn3",
        "v6",
        "wl4",
        "ctjot",
        "mk64",
        "sly1",
        "ffta",
        "diddy_kong_racing",
        "timespinner",
        "sm",
        "ahit",
        "ror1",
        "metroidprime",
        "sm_map_rando",
        "tloz_ooa",
        "against_the_storm",
        "pmd_eos",
        "jakanddaxter",
        "earthbound",
        "tmc",
        "witness",
        "apeescape",
        "rimworld",
        "pokemon_crystal",
        "metroidfusion",
        "tloz_ph",
        "spyro3",
        "rogue_legacy",
        "mm_recomp",
        "sms",
        "shorthike",
        "pokemon_emerald"
    ],
    "strategy": [
        "ufo50",
        "stardew_valley",
        "openrct2",
        "sc2",
        "satisfactory",
        "undertale",
        "shapez",
        "mmbn3",
        "hylics2",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "civ_6",
        "ffta",
        "factorio",
        "pokemon_rb",
        "chainedechoes",
        "yugiohddm",
        "spire",
        "fm",
        "balatro",
        "overcooked2",
        "against_the_storm",
        "pmd_eos",
        "earthbound",
        "yugioh06",
        "rimworld",
        "factorio_saws",
        "terraria",
        "monster_sanctuary",
        "wargroove",
        "wargroove2",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "(rts)": [
        "rimworld",
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3"
    ],
    "simulator": [
        "stardew_valley",
        "openrct2",
        "outer_wilds",
        "satisfactory",
        "shapez",
        "seaofthieves",
        "dredge",
        "dontstarvetogether",
        "civ_6",
        "raft",
        "factorio",
        "powerwashsimulator",
        "doronko_wanko",
        "getting_over_it",
        "placidplasticducksim",
        "sims4",
        "overcooked2",
        "against_the_storm",
        "noita",
        "rimworld",
        "factorio_saws",
        "terraria",
        "minecraft"
    ],
    "indie": [
        "rabi_ribi",
        "phoa",
        "peaks_of_yore",
        "stardew_valley",
        "lunacid",
        "ufo50",
        "openrct2",
        "outer_wilds",
        "enderlilies",
        "satisfactory",
        "celeste_open_world",
        "tunic",
        "undertale",
        "shivers",
        "pseudoregalia",
        "musedash",
        "shapez",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "osu",
        "v6",
        "lingo",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "inscryption",
        "animal_well",
        "dontstarvetogether",
        "hades",
        "tboir",
        "factorio",
        "raft",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "chainedechoes",
        "lethal_company",
        "dlcquest",
        "ahit",
        "momodoramoonlitfarewell",
        "getting_over_it",
        "ror1",
        "ror2",
        "aquaria",
        "frogmonster",
        "spire",
        "balatro",
        "kindergarten_2",
        "against_the_storm",
        "hcniko",
        "overcooked2",
        "witness",
        "hk",
        "noita",
        "aus",
        "brotato",
        "rimworld",
        "subnautica",
        "messenger",
        "factorio_saws",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "ultrakill",
        "wargroove",
        "wargroove2",
        "shorthike",
        "celeste64"
    ],
    "xbox series x|s": [
        "phoa",
        "residentevil3remake",
        "outer_wilds",
        "enderlilies",
        "satisfactory",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "dredge",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "cccharles",
        "momodoramoonlitfarewell",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "brotato",
        "hitman_woa",
        "subnautica",
        "nine_sols",
        "wargroove2"
    ],
    "xbox": [
        "lego_star_wars_tcs",
        "phoa",
        "simpsonshitnrun",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "satisfactory",
        "celeste_open_world",
        "tunic",
        "sadx",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "seaofthieves",
        "oribf",
        "dredge",
        "dark_souls_3",
        "blasphemous",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "bfbb",
        "chainedechoes",
        "dlcquest",
        "ahit",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "dark_souls_2",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "overcooked2",
        "poe",
        "sa2b",
        "shorthike",
        "hk",
        "sims4",
        "sonic_heroes",
        "witness",
        "brotato",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "wargroove2",
        "sotn",
        "dw1"
    ],
    "series": [
        "phoa",
        "residentevil3remake",
        "outer_wilds",
        "doom_1993",
        "enderlilies",
        "satisfactory",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "dredge",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "cccharles",
        "momodoramoonlitfarewell",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "doom_ii",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "brotato",
        "hitman_woa",
        "subnautica",
        "nine_sols",
        "wargroove2"
    ],
    "x|s": [
        "phoa",
        "residentevil3remake",
        "outer_wilds",
        "enderlilies",
        "satisfactory",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "dredge",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "cccharles",
        "momodoramoonlitfarewell",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "brotato",
        "hitman_woa",
        "subnautica",
        "nine_sols",
        "wargroove2"
    ],
    "playstation 4": [
        "rabi_ribi",
        "phoa",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "v6",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "inscryption",
        "hades",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "chainedechoes",
        "ahit",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "jakanddaxter",
        "overcooked2",
        "poe",
        "sims4",
        "hk",
        "witness",
        "brotato",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "shorthike"
    ],
    "playstation": [
        "lego_star_wars_tcs",
        "rabi_ribi",
        "phoa",
        "simpsonshitnrun",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "satisfactory",
        "celeste_open_world",
        "tunic",
        "sadx",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "seaofthieves",
        "v6",
        "sly1",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "bfbb",
        "chainedechoes",
        "kh1",
        "ahit",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "dark_souls_2",
        "fm",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "jakanddaxter",
        "overcooked2",
        "poe",
        "sa2b",
        "hk",
        "shorthike",
        "sims4",
        "sonic_heroes",
        "witness",
        "apeescape",
        "brotato",
        "rac2",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "spyro3",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "sotn",
        "dw1"
    ],
    "4": [
        "rabi_ribi",
        "phoa",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "v6",
        "wl4",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "inscryption",
        "hades",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "chainedechoes",
        "ahit",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "jakanddaxter",
        "overcooked2",
        "poe",
        "shorthike",
        "hk",
        "sims4",
        "witness",
        "brotato",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "dw1"
    ],
    "pc (microsoft windows)": [
        "rabi_ribi",
        "meritous",
        "stardew_valley",
        "lunacid",
        "openrct2",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "heretic",
        "seaofthieves",
        "v6",
        "osu",
        "oribf",
        "dark_souls_3",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "frogmonster",
        "kindergarten_2",
        "overcooked2",
        "witness",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "lego_star_wars_tcs",
        "peaks_of_yore",
        "dsr",
        "peak",
        "sadx",
        "shivers",
        "pseudoregalia",
        "shapez",
        "quake",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "timespinner",
        "cuphead",
        "getting_over_it",
        "aquaria",
        "placidplasticducksim",
        "residentevil2remake",
        "sa2b",
        "hitman_woa",
        "terraria",
        "monster_sanctuary",
        "shorthike",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "toontown",
        "musedash",
        "dredge",
        "lingo",
        "factorio",
        "crosscode",
        "zork_grand_inquisitor",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "landstalker",
        "dark_souls_2",
        "against_the_storm",
        "hcniko",
        "noita",
        "factorio_saws",
        "wargroove",
        "residentevil3remake",
        "sc2",
        "enderlilies",
        "satisfactory",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "civ_6",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "bumpstik",
        "lethal_company",
        "ahit",
        "gzdoom",
        "trackmania",
        "doom_ii",
        "spire",
        "balatro",
        "sims4",
        "poe",
        "sonic_heroes",
        "hk",
        "tyrian",
        "aus",
        "rimworld",
        "ultrakill",
        "wargroove2"
    ],
    "pc": [
        "rabi_ribi",
        "meritous",
        "stardew_valley",
        "lunacid",
        "openrct2",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "heretic",
        "seaofthieves",
        "v6",
        "osu",
        "oribf",
        "dark_souls_3",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "frogmonster",
        "kindergarten_2",
        "overcooked2",
        "witness",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "lego_star_wars_tcs",
        "peaks_of_yore",
        "dsr",
        "peak",
        "sadx",
        "shivers",
        "pseudoregalia",
        "shapez",
        "quake",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "timespinner",
        "cuphead",
        "getting_over_it",
        "aquaria",
        "placidplasticducksim",
        "residentevil2remake",
        "sa2b",
        "hitman_woa",
        "terraria",
        "monster_sanctuary",
        "shorthike",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "toontown",
        "musedash",
        "dredge",
        "lingo",
        "factorio",
        "crosscode",
        "zork_grand_inquisitor",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "landstalker",
        "dark_souls_2",
        "against_the_storm",
        "hcniko",
        "noita",
        "factorio_saws",
        "wargroove",
        "residentevil3remake",
        "sc2",
        "enderlilies",
        "satisfactory",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "civ_6",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "bumpstik",
        "lethal_company",
        "ahit",
        "gzdoom",
        "trackmania",
        "doom_ii",
        "spire",
        "balatro",
        "sims4",
        "poe",
        "sonic_heroes",
        "hk",
        "tyrian",
        "aus",
        "rimworld",
        "ultrakill",
        "wargroove2"
    ],
    "(microsoft": [
        "rabi_ribi",
        "meritous",
        "stardew_valley",
        "lunacid",
        "openrct2",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "heretic",
        "seaofthieves",
        "v6",
        "osu",
        "oribf",
        "dark_souls_3",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "frogmonster",
        "kindergarten_2",
        "overcooked2",
        "witness",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "lego_star_wars_tcs",
        "peaks_of_yore",
        "dsr",
        "peak",
        "sadx",
        "shivers",
        "pseudoregalia",
        "shapez",
        "quake",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "timespinner",
        "cuphead",
        "getting_over_it",
        "aquaria",
        "placidplasticducksim",
        "residentevil2remake",
        "sa2b",
        "hitman_woa",
        "terraria",
        "monster_sanctuary",
        "shorthike",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "toontown",
        "musedash",
        "dredge",
        "lingo",
        "factorio",
        "crosscode",
        "zork_grand_inquisitor",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "landstalker",
        "dark_souls_2",
        "against_the_storm",
        "hcniko",
        "noita",
        "factorio_saws",
        "wargroove",
        "residentevil3remake",
        "sc2",
        "enderlilies",
        "satisfactory",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "civ_6",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "bumpstik",
        "lethal_company",
        "ahit",
        "gzdoom",
        "trackmania",
        "doom_ii",
        "spire",
        "balatro",
        "sims4",
        "poe",
        "sonic_heroes",
        "hk",
        "tyrian",
        "aus",
        "rimworld",
        "ultrakill",
        "wargroove2"
    ],
    "windows)": [
        "rabi_ribi",
        "meritous",
        "stardew_valley",
        "lunacid",
        "openrct2",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "heretic",
        "seaofthieves",
        "v6",
        "osu",
        "oribf",
        "dark_souls_3",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "powerwashsimulator",
        "frogmonster",
        "kindergarten_2",
        "overcooked2",
        "witness",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "minecraft",
        "lego_star_wars_tcs",
        "peaks_of_yore",
        "dsr",
        "peak",
        "sadx",
        "shivers",
        "pseudoregalia",
        "shapez",
        "quake",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "timespinner",
        "cuphead",
        "getting_over_it",
        "aquaria",
        "placidplasticducksim",
        "residentevil2remake",
        "sa2b",
        "hitman_woa",
        "terraria",
        "monster_sanctuary",
        "shorthike",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "toontown",
        "musedash",
        "dredge",
        "lingo",
        "factorio",
        "crosscode",
        "zork_grand_inquisitor",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "landstalker",
        "dark_souls_2",
        "against_the_storm",
        "hcniko",
        "noita",
        "factorio_saws",
        "wargroove",
        "residentevil3remake",
        "sc2",
        "enderlilies",
        "satisfactory",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "civ_6",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "bumpstik",
        "lethal_company",
        "ahit",
        "gzdoom",
        "trackmania",
        "doom_ii",
        "spire",
        "balatro",
        "sims4",
        "poe",
        "sonic_heroes",
        "hk",
        "tyrian",
        "aus",
        "rimworld",
        "ultrakill",
        "wargroove2"
    ],
    "playstation 5": [
        "residentevil3remake",
        "outer_wilds",
        "satisfactory",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "dredge",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "crosscode",
        "powerwashsimulator",
        "cccharles",
        "momodoramoonlitfarewell",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "poe",
        "brotato",
        "hitman_woa",
        "subnautica",
        "messenger",
        "nine_sols"
    ],
    "5": [
        "residentevil3remake",
        "outer_wilds",
        "satisfactory",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "dredge",
        "inscryption",
        "animal_well",
        "hades",
        "raft",
        "crosscode",
        "powerwashsimulator",
        "cccharles",
        "momodoramoonlitfarewell",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "poe",
        "brotato",
        "hitman_woa",
        "subnautica",
        "messenger",
        "nine_sols"
    ],
    "nintendo switch": [
        "rabi_ribi",
        "phoa",
        "ufo50",
        "stardew_valley",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "musedash",
        "smo",
        "bomb_rush_cyberfunk",
        "celeste",
        "v6",
        "oribf",
        "dredge",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "inscryption",
        "animal_well",
        "dontstarvetogether",
        "hades",
        "tboir",
        "factorio",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "ahit",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "balatro",
        "against_the_storm",
        "hcniko",
        "overcooked2",
        "megamix",
        "hk",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "wargroove2",
        "shorthike"
    ],
    "nintendo": [
        "rabi_ribi",
        "albw",
        "banjo_tooie",
        "stardew_valley",
        "oot",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "v6",
        "ctjot",
        "oribf",
        "k64",
        "inscryption",
        "animal_well",
        "hades",
        "tboir",
        "dkc",
        "powerwashsimulator",
        "mario_kart_double_dash",
        "faxanadu",
        "tetrisattack",
        "overcooked2",
        "pmd_eos",
        "tmc",
        "ladx",
        "megamix",
        "brotato",
        "metroidfusion",
        "subnautica",
        "messenger",
        "swr",
        "wl",
        "rogue_legacy",
        "nine_sols",
        "soe",
        "dsr",
        "cv64",
        "alttp",
        "smo",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "dontstarvetogether",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "placidplasticducksim",
        "metroidprime",
        "earthbound",
        "pokemon_crystal",
        "terraria",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "monster_sanctuary",
        "sms",
        "shorthike",
        "sm",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "ff1",
        "luigismansion",
        "musedash",
        "mk64",
        "dredge",
        "factorio",
        "diddy_kong_racing",
        "crosscode",
        "tloz",
        "bfbb",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "tww",
        "lufia2ac",
        "against_the_storm",
        "hcniko",
        "wargroove",
        "tloz_ph",
        "dkc3",
        "enderlilies",
        "undertale",
        "tloz_oos",
        "bomb_rush_cyberfunk",
        "celeste",
        "wl4",
        "star_fox_64",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "marioland2",
        "ahit",
        "sm_map_rando",
        "smw",
        "tloz_ooa",
        "balatro",
        "mm2",
        "sonic_heroes",
        "zelda2",
        "hk",
        "ff4fe",
        "dkc2",
        "dk64",
        "yoshisisland",
        "kdl3",
        "papermario",
        "wargroove2",
        "dw1"
    ],
    "switch": [
        "rabi_ribi",
        "phoa",
        "ufo50",
        "stardew_valley",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "musedash",
        "smo",
        "bomb_rush_cyberfunk",
        "celeste",
        "v6",
        "oribf",
        "dredge",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "inscryption",
        "animal_well",
        "dontstarvetogether",
        "hades",
        "tboir",
        "factorio",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "ahit",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "balatro",
        "against_the_storm",
        "hcniko",
        "overcooked2",
        "megamix",
        "hk",
        "brotato",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "wargroove2",
        "shorthike"
    ],
    "roguelite": [
        "noita",
        "brotato",
        "ror1",
        "ror2",
        "hades",
        "against_the_storm"
    ],
    "a hat in time": [
        "ahit"
    ],
    "a": [
        "albw",
        "ahit",
        "alttp",
        "smz3",
        "shorthike"
    ],
    "hat": [
        "ahit"
    ],
    "in": [
        "zelda2",
        "albw",
        "kh1",
        "ss",
        "ahit",
        "oot",
        "tloz_ph",
        "metroidprime",
        "alttp",
        "papermario",
        "smw",
        "sm_map_rando",
        "sms",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "sm",
        "earthbound"
    ],
    "first person": [
        "lunacid",
        "outer_wilds",
        "doom_1993",
        "cv64",
        "satisfactory",
        "shivers",
        "quake",
        "heretic",
        "seaofthieves",
        "hylics2",
        "lingo",
        "inscryption",
        "star_fox_64",
        "raft",
        "powerwashsimulator",
        "cccharles",
        "zork_grand_inquisitor",
        "lethal_company",
        "yugiohddm",
        "ahit",
        "trackmania",
        "metroidprime",
        "doom_ii",
        "frogmonster",
        "fm",
        "sims4",
        "earthbound",
        "witness",
        "swr",
        "subnautica",
        "ultrakill",
        "minecraft"
    ],
    "first": [
        "lunacid",
        "outer_wilds",
        "doom_1993",
        "cv64",
        "satisfactory",
        "shivers",
        "quake",
        "heretic",
        "seaofthieves",
        "hylics2",
        "lingo",
        "inscryption",
        "star_fox_64",
        "raft",
        "powerwashsimulator",
        "cccharles",
        "zork_grand_inquisitor",
        "lethal_company",
        "yugiohddm",
        "ahit",
        "trackmania",
        "metroidprime",
        "doom_ii",
        "frogmonster",
        "fm",
        "sims4",
        "earthbound",
        "witness",
        "swr",
        "subnautica",
        "ultrakill",
        "minecraft"
    ],
    "person": [
        "banjo_tooie",
        "albw",
        "lunacid",
        "oot",
        "outer_wilds",
        "heretic",
        "seaofthieves",
        "sly1",
        "dark_souls_3",
        "inscryption",
        "raft",
        "powerwashsimulator",
        "mario_kart_double_dash",
        "frogmonster",
        "jakanddaxter",
        "witness",
        "megamix",
        "swr",
        "subnautica",
        "minecraft",
        "lego_star_wars_tcs",
        "soe",
        "dsr",
        "cv64",
        "sadx",
        "shivers",
        "pseudoregalia",
        "quake",
        "smo",
        "cat_quest",
        "crystal_project",
        "sm64hacks",
        "sm64ex",
        "yugiohddm",
        "getting_over_it",
        "placidplasticducksim",
        "metroidprime",
        "fm",
        "residentevil2remake",
        "sa2b",
        "earthbound",
        "rac2",
        "hitman_woa",
        "mm_recomp",
        "sms",
        "celeste64",
        "simpsonshitnrun",
        "xenobladex",
        "toontown",
        "luigismansion",
        "mk64",
        "lingo",
        "kh2",
        "diddy_kong_racing",
        "zork_grand_inquisitor",
        "bfbb",
        "kh1",
        "ror2",
        "tww",
        "dark_souls_2",
        "hcniko",
        "apeescape",
        "residentevil3remake",
        "madou",
        "doom_1993",
        "satisfactory",
        "bomb_rush_cyberfunk",
        "hylics2",
        "star_fox_64",
        "gstla",
        "cccharles",
        "lethal_company",
        "ahit",
        "gzdoom",
        "trackmania",
        "doom_ii",
        "sims4",
        "tp",
        "sonic_heroes",
        "ss",
        "dk64",
        "spyro3",
        "papermario",
        "ultrakill",
        "dw1"
    ],
    "third person": [
        "lego_star_wars_tcs",
        "banjo_tooie",
        "albw",
        "simpsonshitnrun",
        "soe",
        "residentevil3remake",
        "oot",
        "dsr",
        "madou",
        "xenobladex",
        "cv64",
        "toontown",
        "sadx",
        "pseudoregalia",
        "luigismansion",
        "smo",
        "bomb_rush_cyberfunk",
        "hylics2",
        "mk64",
        "sly1",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "crystal_project",
        "star_fox_64",
        "gstla",
        "raft",
        "diddy_kong_racing",
        "sm64hacks",
        "mario_kart_double_dash",
        "bfbb",
        "kh1",
        "sm64ex",
        "ahit",
        "ror2",
        "getting_over_it",
        "gzdoom",
        "placidplasticducksim",
        "trackmania",
        "tww",
        "dark_souls_2",
        "sims4",
        "residentevil2remake",
        "hcniko",
        "jakanddaxter",
        "sa2b",
        "sonic_heroes",
        "megamix",
        "tp",
        "apeescape",
        "ss",
        "dk64",
        "hitman_woa",
        "rac2",
        "swr",
        "spyro3",
        "papermario",
        "mm_recomp",
        "sms",
        "dw1",
        "minecraft",
        "celeste64"
    ],
    "third": [
        "lego_star_wars_tcs",
        "banjo_tooie",
        "albw",
        "simpsonshitnrun",
        "soe",
        "residentevil3remake",
        "oot",
        "dsr",
        "madou",
        "xenobladex",
        "cv64",
        "toontown",
        "sadx",
        "pseudoregalia",
        "luigismansion",
        "smo",
        "bomb_rush_cyberfunk",
        "hylics2",
        "mk64",
        "sly1",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "crystal_project",
        "star_fox_64",
        "gstla",
        "raft",
        "diddy_kong_racing",
        "sm64hacks",
        "mario_kart_double_dash",
        "bfbb",
        "kh1",
        "sm64ex",
        "ahit",
        "ror2",
        "getting_over_it",
        "gzdoom",
        "placidplasticducksim",
        "trackmania",
        "tww",
        "dark_souls_2",
        "sims4",
        "residentevil2remake",
        "hcniko",
        "jakanddaxter",
        "sa2b",
        "sonic_heroes",
        "megamix",
        "tp",
        "apeescape",
        "ss",
        "dk64",
        "hitman_woa",
        "rac2",
        "swr",
        "spyro3",
        "papermario",
        "mm_recomp",
        "sms",
        "dw1",
        "minecraft",
        "celeste64"
    ],
    "platform": [
        "lego_star_wars_tcs",
        "dkc3",
        "rabi_ribi",
        "banjo_tooie",
        "phoa",
        "peaks_of_yore",
        "simpsonshitnrun",
        "sm64ex",
        "ufo50",
        "cv64",
        "enderlilies",
        "celeste_open_world",
        "sadx",
        "pseudoregalia",
        "zillion",
        "smo",
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "v6",
        "oribf",
        "sly1",
        "wl4",
        "blasphemous",
        "crystal_project",
        "k64",
        "animal_well",
        "dkc",
        "smz3",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "bfbb",
        "marioland2",
        "dlcquest",
        "ahit",
        "mm3",
        "getting_over_it",
        "gzdoom",
        "momodoramoonlitfarewell",
        "ror1",
        "aquaria",
        "metroidprime",
        "smw",
        "sm_map_rando",
        "faxanadu",
        "mm2",
        "hcniko",
        "jakanddaxter",
        "sa2b",
        "sonic_heroes",
        "zelda2",
        "cvcotm",
        "hk",
        "aus",
        "apeescape",
        "mzm",
        "dkc2",
        "dk64",
        "rac2",
        "metroidfusion",
        "yoshisisland",
        "kdl3",
        "messenger",
        "wl",
        "spyro3",
        "rogue_legacy",
        "mmx3",
        "monster_sanctuary",
        "nine_sols",
        "sms",
        "terraria",
        "sotn",
        "ultrakill",
        "sm",
        "celeste64"
    ],
    "action": [
        "rabi_ribi",
        "albw",
        "banjo_tooie",
        "oot",
        "outer_wilds",
        "celeste_open_world",
        "tunic",
        "seaofthieves",
        "v6",
        "osu",
        "ctjot",
        "oribf",
        "sly1",
        "dark_souls_3",
        "k64",
        "animal_well",
        "hades",
        "dkc",
        "mario_kart_double_dash",
        "frogmonster",
        "faxanadu",
        "tetrisattack",
        "overcooked2",
        "jakanddaxter",
        "tmc",
        "ladx",
        "brotato",
        "metroidfusion",
        "swr",
        "messenger",
        "wl",
        "rogue_legacy",
        "nine_sols",
        "lego_star_wars_tcs",
        "soe",
        "peaks_of_yore",
        "dsr",
        "cv64",
        "alttp",
        "sadx",
        "pseudoregalia",
        "quake",
        "mmbn3",
        "smo",
        "cat_quest",
        "blasphemous",
        "dontstarvetogether",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "getting_over_it",
        "metroidprime",
        "residentevil2remake",
        "sa2b",
        "earthbound",
        "rac2",
        "hitman_woa",
        "pokemon_crystal",
        "terraria",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "monster_sanctuary",
        "sms",
        "sotn",
        "sm",
        "pokemon_frlg",
        "celeste64",
        "phoa",
        "simpsonshitnrun",
        "ufo50",
        "xenobladex",
        "ff1",
        "luigismansion",
        "musedash",
        "mk64",
        "dredge",
        "kh2",
        "diddy_kong_racing",
        "crosscode",
        "tloz",
        "bfbb",
        "kh1",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "ror2",
        "tww",
        "landstalker",
        "dark_souls_2",
        "hcniko",
        "cvcotm",
        "noita",
        "apeescape",
        "mlss",
        "tloz_ph",
        "pokemon_emerald",
        "dkc3",
        "residentevil3remake",
        "sc2",
        "doom_1993",
        "enderlilies",
        "tloz_oos",
        "bomb_rush_cyberfunk",
        "celeste",
        "wl4",
        "star_fox_64",
        "gstla",
        "doronko_wanko",
        "cccharles",
        "chainedechoes",
        "lethal_company",
        "marioland2",
        "ahit",
        "gzdoom",
        "trackmania",
        "sm_map_rando",
        "smw",
        "doom_ii",
        "tloz_ooa",
        "sims4",
        "mm2",
        "tp",
        "poe",
        "sonic_heroes",
        "zelda2",
        "hk",
        "tyrian",
        "aus",
        "ff4fe",
        "dkc2",
        "dk64",
        "mzm",
        "ss",
        "yoshisisland",
        "kdl3",
        "spyro3",
        "papermario",
        "ultrakill",
        "dw1"
    ],
    "mac": [
        "lego_star_wars_tcs",
        "phoa",
        "stardew_valley",
        "residentevil3remake",
        "openrct2",
        "sc2",
        "celeste_open_world",
        "toontown",
        "tunic",
        "undertale",
        "shapez",
        "musedash",
        "quake",
        "heretic",
        "celeste",
        "v6",
        "hylics2",
        "osu",
        "dredge",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "civ_6",
        "hades",
        "factorio",
        "crosscode",
        "timespinner",
        "cuphead",
        "chainedechoes",
        "zork_grand_inquisitor",
        "dlcquest",
        "ahit",
        "ror1",
        "getting_over_it",
        "aquaria",
        "landstalker",
        "doom_ii",
        "balatro",
        "residentevil2remake",
        "overcooked2",
        "sims4",
        "poe",
        "witness",
        "hk",
        "tyrian",
        "brotato",
        "rimworld",
        "hitman_woa",
        "swr",
        "subnautica",
        "factorio_saws",
        "osrs",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "shorthike",
        "minecraft"
    ],
    "xbox one": [
        "phoa",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "seaofthieves",
        "oribf",
        "dredge",
        "dark_souls_3",
        "blasphemous",
        "inscryption",
        "hades",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "chainedechoes",
        "ahit",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "overcooked2",
        "sims4",
        "poe",
        "witness",
        "hk",
        "brotato",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "wargroove2",
        "shorthike"
    ],
    "one": [
        "phoa",
        "stardew_valley",
        "residentevil3remake",
        "dsr",
        "outer_wilds",
        "enderlilies",
        "celeste_open_world",
        "tunic",
        "undertale",
        "bomb_rush_cyberfunk",
        "celeste",
        "seaofthieves",
        "oribf",
        "dredge",
        "dark_souls_3",
        "blasphemous",
        "inscryption",
        "hades",
        "crosscode",
        "timespinner",
        "cuphead",
        "powerwashsimulator",
        "cccharles",
        "chainedechoes",
        "ahit",
        "ror1",
        "ror2",
        "placidplasticducksim",
        "trackmania",
        "balatro",
        "residentevil2remake",
        "overcooked2",
        "sims4",
        "poe",
        "witness",
        "hk",
        "brotato",
        "hitman_woa",
        "swr",
        "subnautica",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "terraria",
        "wargroove",
        "wargroove2",
        "shorthike"
    ],
    "time travel": [
        "ctjot",
        "apeescape",
        "ahit",
        "oot",
        "outer_wilds",
        "mm_recomp",
        "tloz_ooa",
        "tloz_oos",
        "timespinner",
        "pmd_eos",
        "earthbound"
    ],
    "travel": [
        "ctjot",
        "apeescape",
        "ahit",
        "oot",
        "outer_wilds",
        "mm_recomp",
        "tloz_ooa",
        "tloz_oos",
        "timespinner",
        "pmd_eos",
        "earthbound"
    ],
    "spaceship": [
        "v6",
        "mzm",
        "ahit",
        "metroidfusion",
        "star_fox_64",
        "metroidprime",
        "civ_6"
    ],
    "female protagonist": [
        "dkc3",
        "rabi_ribi",
        "cv64",
        "enderlilies",
        "celeste_open_world",
        "undertale",
        "celeste",
        "timespinner",
        "ahit",
        "metroidprime",
        "sm_map_rando",
        "hcniko",
        "earthbound",
        "mzm",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "shorthike",
        "sm",
        "celeste64"
    ],
    "female": [
        "dkc3",
        "rabi_ribi",
        "cv64",
        "enderlilies",
        "celeste_open_world",
        "undertale",
        "celeste",
        "timespinner",
        "ahit",
        "metroidprime",
        "sm_map_rando",
        "hcniko",
        "earthbound",
        "mzm",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "shorthike",
        "sm",
        "celeste64"
    ],
    "protagonist": [
        "dkc3",
        "rabi_ribi",
        "oot",
        "doom_1993",
        "cv64",
        "enderlilies",
        "alttp",
        "celeste_open_world",
        "undertale",
        "tloz_oos",
        "quake",
        "celeste",
        "blasphemous",
        "k64",
        "gstla",
        "dkc",
        "timespinner",
        "sm",
        "ahit",
        "metroidprime",
        "sm_map_rando",
        "tloz_ooa",
        "hcniko",
        "jakanddaxter",
        "earthbound",
        "tmc",
        "ladx",
        "hk",
        "zelda2",
        "mzm",
        "dkc2",
        "ss",
        "metroidfusion",
        "mlss",
        "tloz_ph",
        "papermario",
        "rogue_legacy",
        "ultrakill",
        "shorthike",
        "pokemon_emerald",
        "celeste64"
    ],
    "action-adventure": [
        "rabi_ribi",
        "albw",
        "banjo_tooie",
        "oot",
        "xenobladex",
        "cv64",
        "alttp",
        "tloz_oos",
        "luigismansion",
        "zillion",
        "seaofthieves",
        "dark_souls_3",
        "dontstarvetogether",
        "crosscode",
        "timespinner",
        "kh1",
        "ahit",
        "aquaria",
        "tww",
        "landstalker",
        "metroidprime",
        "sm_map_rando",
        "dark_souls_2",
        "tloz_ooa",
        "tmc",
        "ladx",
        "cvcotm",
        "hk",
        "zelda2",
        "aus",
        "ss",
        "metroidfusion",
        "rogue_legacy",
        "mm_recomp",
        "terraria",
        "sms",
        "sotn",
        "tloz_ph",
        "sm",
        "minecraft"
    ],
    "cute": [
        "celeste",
        "rabi_ribi",
        "sims4",
        "ahit",
        "animal_well",
        "celeste_open_world",
        "tunic",
        "undertale",
        "shorthike",
        "musedash",
        "hcniko"
    ],
    "snow": [
        "celeste",
        "dkc3",
        "lego_star_wars_tcs",
        "albw",
        "mk64",
        "stardew_valley",
        "ahit",
        "metroidprime",
        "celeste_open_world",
        "gstla",
        "terraria",
        "ffta",
        "diddy_kong_racing",
        "shorthike",
        "hcniko",
        "jakanddaxter",
        "minecraft",
        "dkc"
    ],
    "wall jump": [
        "cvcotm",
        "oribf",
        "simpsonshitnrun",
        "mzm",
        "ahit",
        "metroidfusion",
        "sm_map_rando",
        "mmx3",
        "sms",
        "sm",
        "smo"
    ],
    "wall": [
        "banjo_tooie",
        "simpsonshitnrun",
        "undertale",
        "smo",
        "oribf",
        "ffta",
        "dkc",
        "ahit",
        "sm_map_rando",
        "doom_ii",
        "jakanddaxter",
        "tmc",
        "ladx",
        "cvcotm",
        "mzm",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "mmx3",
        "rogue_legacy",
        "sms",
        "sm"
    ],
    "jump": [
        "cvcotm",
        "oribf",
        "simpsonshitnrun",
        "mzm",
        "ahit",
        "metroidfusion",
        "sm_map_rando",
        "mmx3",
        "sms",
        "sm",
        "smo"
    ],
    "3d platformer": [
        "bomb_rush_cyberfunk",
        "bfbb",
        "sm64ex",
        "ahit",
        "sonic_heroes",
        "sms",
        "shorthike",
        "hcniko",
        "smo",
        "sm64hacks"
    ],
    "3d": [
        "lego_star_wars_tcs",
        "albw",
        "simpsonshitnrun",
        "oot",
        "dsr",
        "xenobladex",
        "cv64",
        "tunic",
        "luigismansion",
        "quake",
        "smo",
        "bomb_rush_cyberfunk",
        "hylics2",
        "mk64",
        "dredge",
        "lingo",
        "dark_souls_3",
        "sly1",
        "crystal_project",
        "k64",
        "star_fox_64",
        "sm64hacks",
        "powerwashsimulator",
        "bfbb",
        "kh1",
        "sm64ex",
        "ahit",
        "metroidprime",
        "frogmonster",
        "dark_souls_2",
        "shorthike",
        "hcniko",
        "jakanddaxter",
        "poe",
        "sonic_heroes",
        "witness",
        "apeescape",
        "ss",
        "dk64",
        "tloz_ph",
        "spyro3",
        "sms",
        "sotn",
        "dw1",
        "minecraft"
    ],
    "platformer": [
        "bomb_rush_cyberfunk",
        "bfbb",
        "sm64ex",
        "ahit",
        "sonic_heroes",
        "sms",
        "shorthike",
        "hcniko",
        "smo",
        "sm64hacks"
    ],
    "swimming": [
        "dkc3",
        "banjo_tooie",
        "albw",
        "oot",
        "alttp",
        "quake",
        "smo",
        "wl4",
        "dkc",
        "sm64hacks",
        "kh1",
        "sm64ex",
        "ahit",
        "aquaria",
        "tloz_ooa",
        "hcniko",
        "jakanddaxter",
        "tmc",
        "dkc2",
        "subnautica",
        "spyro3",
        "terraria",
        "sms",
        "minecraft"
    ],
    "crowdfunding": [
        "hk",
        "rabi_ribi",
        "timespinner",
        "ror1",
        "ahit",
        "crosscode"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "ladx",
        "albw",
        "ss",
        "oot",
        "tp",
        "tloz_ph",
        "tww",
        "alttp",
        "mm_recomp",
        "tloz_ooa",
        "tloz_oos",
        "tloz",
        "tmc"
    ],
    "of": [
        "dkc3",
        "albw",
        "soe",
        "peaks_of_yore",
        "oot",
        "sc2",
        "cv64",
        "enderlilies",
        "alttp",
        "tloz_oos",
        "luigismansion",
        "seaofthieves",
        "oribf",
        "sly1",
        "star_fox_64",
        "ffta",
        "tboir",
        "dkc",
        "tloz",
        "ror1",
        "ror2",
        "tww",
        "tloz_ooa",
        "lufia2ac",
        "tp",
        "jakanddaxter",
        "earthbound",
        "pmd_eos",
        "ladx",
        "cvcotm",
        "poe",
        "tmc",
        "zelda2",
        "dkc2",
        "dk64",
        "hitman_woa",
        "pokemon_crystal",
        "ss",
        "spyro3",
        "rogue_legacy",
        "mm_recomp",
        "sms",
        "sotn",
        "tloz_ph",
        "pokemon_emerald",
        "celeste64"
    ],
    "zelda:": [
        "ladx",
        "albw",
        "ss",
        "oot",
        "tloz_ph",
        "tww",
        "alttp",
        "mm_recomp",
        "tloz_ooa",
        "tloz_oos",
        "tp",
        "tmc"
    ],
    "link": [
        "zelda2",
        "smz3",
        "albw",
        "alttp"
    ],
    "between": [
        "albw"
    ],
    "worlds": [
        "albw"
    ],
    "puzzle": [
        "albw",
        "ufo50",
        "oot",
        "outer_wilds",
        "cv64",
        "candybox2",
        "alttp",
        "tunic",
        "undertale",
        "shivers",
        "shapez",
        "tloz_oos",
        "zillion",
        "v6",
        "wl4",
        "oribf",
        "lingo",
        "inscryption",
        "animal_well",
        "crosscode",
        "zork_grand_inquisitor",
        "bumpstik",
        "yugiohddm",
        "ttyd",
        "placidplasticducksim",
        "tww",
        "doom_ii",
        "tloz_ooa",
        "lufia2ac",
        "tetrisattack",
        "hcniko",
        "tp",
        "tmc",
        "witness",
        "ladx",
        "ss",
        "metroidfusion",
        "spyro3",
        "rogue_legacy",
        "mm_recomp",
        "tloz_ph"
    ],
    "historical": [
        "albw",
        "soe",
        "ss",
        "candybox2",
        "civ_6",
        "fm",
        "quake",
        "heretic"
    ],
    "sandbox": [
        "albw",
        "stardew_valley",
        "oot",
        "xenobladex",
        "satisfactory",
        "shapez",
        "smo",
        "dontstarvetogether",
        "factorio",
        "powerwashsimulator",
        "placidplasticducksim",
        "landstalker",
        "faxanadu",
        "sims4",
        "zelda2",
        "noita",
        "hitman_woa",
        "factorio_saws",
        "osrs",
        "terraria",
        "sms",
        "minecraft"
    ],
    "open world": [
        "albw",
        "phoa",
        "simpsonshitnrun",
        "oot",
        "outer_wilds",
        "xenobladex",
        "satisfactory",
        "toontown",
        "smo",
        "seaofthieves",
        "dredge",
        "lingo",
        "dontstarvetogether",
        "gstla",
        "pokemon_rb",
        "smz3",
        "tloz",
        "sm64hacks",
        "cccharles",
        "sm64ex",
        "metroidprime",
        "frogmonster",
        "jakanddaxter",
        "witness",
        "mzm",
        "ss",
        "subnautica",
        "osrs",
        "terraria",
        "mm_recomp",
        "sotn",
        "shorthike",
        "minecraft"
    ],
    "open": [
        "albw",
        "phoa",
        "simpsonshitnrun",
        "oot",
        "outer_wilds",
        "xenobladex",
        "satisfactory",
        "toontown",
        "smo",
        "seaofthieves",
        "dredge",
        "lingo",
        "dontstarvetogether",
        "gstla",
        "pokemon_rb",
        "smz3",
        "tloz",
        "sm64hacks",
        "cccharles",
        "sm64ex",
        "metroidprime",
        "frogmonster",
        "jakanddaxter",
        "witness",
        "mzm",
        "ss",
        "subnautica",
        "osrs",
        "terraria",
        "mm_recomp",
        "sotn",
        "shorthike",
        "minecraft"
    ],
    "world": [
        "dkc3",
        "albw",
        "phoa",
        "simpsonshitnrun",
        "oot",
        "outer_wilds",
        "xenobladex",
        "satisfactory",
        "alttp",
        "toontown",
        "tloz_oos",
        "smo",
        "seaofthieves",
        "v6",
        "dredge",
        "lingo",
        "dontstarvetogether",
        "gstla",
        "dkc",
        "pokemon_rb",
        "smz3",
        "tloz",
        "sm64hacks",
        "cccharles",
        "sm64ex",
        "aquaria",
        "metroidprime",
        "smw",
        "frogmonster",
        "dark_souls_2",
        "shorthike",
        "jakanddaxter",
        "earthbound",
        "tmc",
        "ladx",
        "witness",
        "yugioh06",
        "zelda2",
        "mzm",
        "dkc2",
        "ss",
        "hitman_woa",
        "pokemon_crystal",
        "subnautica",
        "yoshisisland",
        "tloz_ph",
        "osrs",
        "terraria",
        "mm_recomp",
        "sotn",
        "dw1",
        "minecraft"
    ],
    "nintendo 3ds": [
        "ladx",
        "v6",
        "wl4",
        "albw",
        "zelda2",
        "marioland2",
        "mm3",
        "metroidfusion",
        "pokemon_crystal",
        "wl",
        "terraria",
        "tloz_ooa",
        "ff1",
        "pokemon_rb",
        "tloz_oos",
        "mm2",
        "tloz",
        "tmc"
    ],
    "3ds": [
        "dkc3",
        "albw",
        "alttp",
        "ff1",
        "tloz_oos",
        "v6",
        "wl4",
        "pokemon_rb",
        "dkc",
        "tloz",
        "marioland2",
        "mm3",
        "sm_map_rando",
        "smw",
        "tloz_ooa",
        "mm2",
        "earthbound",
        "tmc",
        "ladx",
        "zelda2",
        "dkc2",
        "pokemon_crystal",
        "metroidfusion",
        "wl",
        "terraria",
        "mmx3",
        "sm"
    ],
    "medieval": [
        "albw",
        "soe",
        "dark_souls_3",
        "ss",
        "candybox2",
        "rogue_legacy",
        "dark_souls_2",
        "quake",
        "heretic"
    ],
    "magic": [
        "rabi_ribi",
        "albw",
        "dsr",
        "cv64",
        "candybox2",
        "alttp",
        "tloz_oos",
        "heretic",
        "ctjot",
        "gstla",
        "ffta",
        "cuphead",
        "zork_grand_inquisitor",
        "aquaria",
        "dark_souls_2",
        "faxanadu",
        "poe",
        "tmc",
        "ladx",
        "cvcotm",
        "noita",
        "zelda2",
        "rogue_legacy",
        "terraria",
        "sotn"
    ],
    "minigames": [
        "dkc3",
        "albw",
        "stardew_valley",
        "oot",
        "toontown",
        "wl4",
        "k64",
        "gstla",
        "kh1",
        "tloz_ooa",
        "hcniko",
        "aus",
        "apeescape",
        "dk64",
        "pokemon_crystal",
        "spyro3",
        "rogue_legacy",
        "tloz_ph",
        "pokemon_emerald"
    ],
    "2.5d": [
        "dkc3",
        "albw",
        "k64",
        "doom_1993",
        "doom_ii",
        "dkc",
        "heretic"
    ],
    "archery": [
        "albw",
        "ss",
        "oot",
        "tww",
        "alttp",
        "mm_recomp",
        "minecraft"
    ],
    "fairy": [
        "ladx",
        "rabi_ribi",
        "zelda2",
        "albw",
        "stardew_valley",
        "dk64",
        "oot",
        "k64",
        "tloz_ph",
        "tww",
        "landstalker",
        "alttp",
        "mm_recomp",
        "terraria",
        "tloz_ooa",
        "tloz_oos",
        "tloz",
        "tmc"
    ],
    "princess": [
        "ladx",
        "lego_star_wars_tcs",
        "albw",
        "mk64",
        "kh1",
        "ss",
        "oot",
        "mlss",
        "tloz_ph",
        "alttp",
        "papermario",
        "smw",
        "tloz_ooa",
        "tloz_oos",
        "tp",
        "tmc"
    ],
    "sequel": [
        "banjo_tooie",
        "albw",
        "oot",
        "alttp",
        "smo",
        "hylics2",
        "wl4",
        "mk64",
        "dark_souls_3",
        "dontstarvetogether",
        "gstla",
        "civ_6",
        "ffta",
        "mm3",
        "doom_ii",
        "dark_souls_2",
        "mm2",
        "zelda2",
        "dkc2",
        "mmx3",
        "mm_recomp",
        "sms",
        "dw1"
    ],
    "sword & sorcery": [
        "ladx",
        "albw",
        "kh1",
        "dark_souls_3",
        "ss",
        "oot",
        "tww",
        "spyro3",
        "terraria",
        "mm_recomp",
        "dark_souls_2",
        "ffmq",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "heretic"
    ],
    "sword": [
        "ladx",
        "albw",
        "kh1",
        "dark_souls_3",
        "ss",
        "oot",
        "tww",
        "spyro3",
        "terraria",
        "mm_recomp",
        "dark_souls_2",
        "ffmq",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "heretic"
    ],
    "&": [
        "albw",
        "simpsonshitnrun",
        "oot",
        "tloz_oos",
        "heretic",
        "dark_souls_3",
        "inscryption",
        "kh1",
        "yugiohddm",
        "tww",
        "tloz_ooa",
        "dark_souls_2",
        "spire",
        "fm",
        "balatro",
        "yugioh06",
        "tmc",
        "ladx",
        "ss",
        "rac2",
        "mlss",
        "spyro3",
        "terraria",
        "mm_recomp",
        "ffmq"
    ],
    "sorcery": [
        "ladx",
        "albw",
        "kh1",
        "dark_souls_3",
        "ss",
        "oot",
        "tww",
        "spyro3",
        "terraria",
        "mm_recomp",
        "dark_souls_2",
        "ffmq",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "heretic"
    ],
    "darkness": [
        "dkc3",
        "albw",
        "alttp",
        "luigismansion",
        "dkc",
        "mm3",
        "aquaria",
        "sm_map_rando",
        "doom_ii",
        "tmc",
        "witness",
        "ladx",
        "earthbound",
        "zelda2",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "terraria",
        "sm",
        "minecraft"
    ],
    "digital distribution": [
        "banjo_tooie",
        "albw",
        "ufo50",
        "oot",
        "celeste_open_world",
        "tunic",
        "tloz_oos",
        "musedash",
        "quake",
        "heretic",
        "celeste",
        "seaofthieves",
        "v6",
        "wl4",
        "oribf",
        "dredge",
        "dontstarvetogether",
        "civ_6",
        "factorio",
        "dkc",
        "crosscode",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "dlcquest",
        "getting_over_it",
        "smw",
        "doom_ii",
        "tmc",
        "witness",
        "ladx",
        "apeescape",
        "yoshisisland",
        "dkc2",
        "dk64",
        "mlss",
        "rogue_legacy",
        "terraria",
        "sotn",
        "minecraft"
    ],
    "digital": [
        "banjo_tooie",
        "albw",
        "ufo50",
        "oot",
        "celeste_open_world",
        "tunic",
        "tloz_oos",
        "musedash",
        "quake",
        "heretic",
        "celeste",
        "seaofthieves",
        "v6",
        "wl4",
        "oribf",
        "dredge",
        "dontstarvetogether",
        "civ_6",
        "factorio",
        "dkc",
        "crosscode",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "dlcquest",
        "getting_over_it",
        "smw",
        "doom_ii",
        "tmc",
        "witness",
        "ladx",
        "apeescape",
        "yoshisisland",
        "dkc2",
        "dk64",
        "mlss",
        "rogue_legacy",
        "terraria",
        "sotn",
        "minecraft"
    ],
    "distribution": [
        "banjo_tooie",
        "albw",
        "ufo50",
        "oot",
        "celeste_open_world",
        "tunic",
        "tloz_oos",
        "musedash",
        "quake",
        "heretic",
        "celeste",
        "seaofthieves",
        "v6",
        "wl4",
        "oribf",
        "dredge",
        "dontstarvetogether",
        "civ_6",
        "factorio",
        "dkc",
        "crosscode",
        "timespinner",
        "cuphead",
        "sm64hacks",
        "sm64ex",
        "dlcquest",
        "getting_over_it",
        "smw",
        "doom_ii",
        "tmc",
        "witness",
        "ladx",
        "apeescape",
        "yoshisisland",
        "dkc2",
        "dk64",
        "mlss",
        "rogue_legacy",
        "terraria",
        "sotn",
        "minecraft"
    ],
    "anthropomorphism": [
        "dkc3",
        "banjo_tooie",
        "albw",
        "cv64",
        "tunic",
        "undertale",
        "tloz_oos",
        "mk64",
        "sly1",
        "k64",
        "star_fox_64",
        "dkc",
        "diddy_kong_racing",
        "cuphead",
        "bfbb",
        "kh1",
        "tloz_ooa",
        "hcniko",
        "jakanddaxter",
        "tmc",
        "sonic_heroes",
        "apeescape",
        "dkc2",
        "dk64",
        "mlss",
        "spyro3",
        "papermario",
        "sms",
        "shorthike"
    ],
    "polygonal 3d": [
        "lego_star_wars_tcs",
        "albw",
        "simpsonshitnrun",
        "oot",
        "xenobladex",
        "cv64",
        "luigismansion",
        "quake",
        "mk64",
        "sly1",
        "k64",
        "star_fox_64",
        "kh1",
        "metroidprime",
        "jakanddaxter",
        "witness",
        "apeescape",
        "ss",
        "dk64",
        "tloz_ph",
        "spyro3",
        "sms",
        "sotn",
        "dw1",
        "minecraft"
    ],
    "polygonal": [
        "lego_star_wars_tcs",
        "albw",
        "simpsonshitnrun",
        "oot",
        "xenobladex",
        "cv64",
        "luigismansion",
        "quake",
        "mk64",
        "sly1",
        "k64",
        "star_fox_64",
        "kh1",
        "metroidprime",
        "jakanddaxter",
        "witness",
        "apeescape",
        "ss",
        "dk64",
        "tloz_ph",
        "spyro3",
        "sms",
        "sotn",
        "dw1",
        "minecraft"
    ],
    "bow and arrow": [
        "ladx",
        "albw",
        "ss",
        "oot",
        "ror1",
        "tloz_ph",
        "alttp",
        "rogue_legacy",
        "dark_souls_2",
        "poe",
        "ffta",
        "terraria",
        "tmc",
        "tloz_oos",
        "minecraft",
        "cuphead"
    ],
    "bow": [
        "ladx",
        "albw",
        "ss",
        "oot",
        "ror1",
        "tloz_ph",
        "alttp",
        "rogue_legacy",
        "dark_souls_2",
        "poe",
        "ffta",
        "terraria",
        "tmc",
        "tloz_oos",
        "minecraft",
        "cuphead"
    ],
    "and": [
        "albw",
        "oot",
        "openrct2",
        "cv64",
        "alttp",
        "tloz_oos",
        "oribf",
        "sly1",
        "blasphemous",
        "civ_6",
        "ffta",
        "hades",
        "smz3",
        "cuphead",
        "ror1",
        "dark_souls_2",
        "jakanddaxter",
        "poe",
        "tmc",
        "ladx",
        "ss",
        "rogue_legacy",
        "nine_sols",
        "terraria",
        "tloz_ph",
        "minecraft"
    ],
    "arrow": [
        "ladx",
        "albw",
        "ss",
        "oot",
        "ror1",
        "tloz_ph",
        "alttp",
        "rogue_legacy",
        "dark_souls_2",
        "poe",
        "ffta",
        "terraria",
        "tmc",
        "tloz_oos",
        "minecraft",
        "cuphead"
    ],
    "damsel in distress": [
        "zelda2",
        "albw",
        "kh1",
        "ss",
        "oot",
        "tloz_ph",
        "metroidprime",
        "alttp",
        "papermario",
        "smw",
        "sm_map_rando",
        "sms",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "sm",
        "earthbound"
    ],
    "damsel": [
        "zelda2",
        "albw",
        "kh1",
        "ss",
        "oot",
        "tloz_ph",
        "metroidprime",
        "alttp",
        "papermario",
        "smw",
        "sm_map_rando",
        "sms",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "sm",
        "earthbound"
    ],
    "distress": [
        "zelda2",
        "albw",
        "kh1",
        "ss",
        "oot",
        "tloz_ph",
        "metroidprime",
        "alttp",
        "papermario",
        "smw",
        "sm_map_rando",
        "sms",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "sm",
        "earthbound"
    ],
    "upgradeable weapons": [
        "albw",
        "mzm",
        "dk64",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "mmx3",
        "dark_souls_2",
        "mm2",
        "tmc"
    ],
    "upgradeable": [
        "albw",
        "mzm",
        "dk64",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "mmx3",
        "dark_souls_2",
        "mm2",
        "tmc"
    ],
    "weapons": [
        "albw",
        "mzm",
        "dk64",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "mmx3",
        "dark_souls_2",
        "mm2",
        "tmc"
    ],
    "disorientation zone": [
        "ladx",
        "albw",
        "oot",
        "alttp",
        "tloz_ooa",
        "tloz_oos",
        "tmc"
    ],
    "disorientation": [
        "ladx",
        "albw",
        "oot",
        "alttp",
        "tloz_ooa",
        "tloz_oos",
        "tmc"
    ],
    "zone": [
        "ladx",
        "albw",
        "oot",
        "alttp",
        "tloz_ooa",
        "tloz_oos",
        "tmc"
    ],
    "descendants of other characters": [
        "dkc3",
        "albw",
        "sly1",
        "dkc2",
        "dk64",
        "oot",
        "tmc",
        "star_fox_64",
        "cv64",
        "rogue_legacy",
        "mm_recomp",
        "sotn",
        "tloz_ooa",
        "sms",
        "dkc",
        "luigismansion",
        "jakanddaxter",
        "earthbound"
    ],
    "descendants": [
        "dkc3",
        "albw",
        "sly1",
        "dkc2",
        "dk64",
        "oot",
        "tmc",
        "star_fox_64",
        "cv64",
        "rogue_legacy",
        "mm_recomp",
        "sotn",
        "tloz_ooa",
        "sms",
        "dkc",
        "luigismansion",
        "jakanddaxter",
        "earthbound"
    ],
    "other": [
        "dkc3",
        "albw",
        "sly1",
        "dkc2",
        "dk64",
        "oot",
        "tmc",
        "star_fox_64",
        "cv64",
        "rogue_legacy",
        "mm_recomp",
        "sotn",
        "tloz_ooa",
        "sms",
        "dkc",
        "luigismansion",
        "jakanddaxter",
        "earthbound"
    ],
    "characters": [
        "lego_star_wars_tcs",
        "dkc3",
        "albw",
        "stardew_valley",
        "oot",
        "xenobladex",
        "cv64",
        "luigismansion",
        "sly1",
        "dark_souls_3",
        "star_fox_64",
        "dkc",
        "tloz_ooa",
        "dark_souls_2",
        "jakanddaxter",
        "earthbound",
        "tmc",
        "dkc2",
        "dk64",
        "rogue_legacy",
        "mm_recomp",
        "terraria",
        "sms",
        "sotn"
    ],
    "save point": [
        "dkc3",
        "albw",
        "cv64",
        "luigismansion",
        "v6",
        "gstla",
        "dkc",
        "kh1",
        "aquaria",
        "metroidprime",
        "sm_map_rando",
        "faxanadu",
        "jakanddaxter",
        "earthbound",
        "cvcotm",
        "mzm",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "sotn",
        "sm"
    ],
    "save": [
        "dkc3",
        "albw",
        "cv64",
        "luigismansion",
        "v6",
        "gstla",
        "dkc",
        "kh1",
        "aquaria",
        "metroidprime",
        "sm_map_rando",
        "faxanadu",
        "jakanddaxter",
        "earthbound",
        "cvcotm",
        "mzm",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "sotn",
        "sm"
    ],
    "point": [
        "dkc3",
        "albw",
        "cv64",
        "luigismansion",
        "v6",
        "gstla",
        "dkc",
        "kh1",
        "aquaria",
        "metroidprime",
        "sm_map_rando",
        "faxanadu",
        "jakanddaxter",
        "earthbound",
        "cvcotm",
        "mzm",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "sotn",
        "sm"
    ],
    "side quests": [
        "ladx",
        "albw",
        "oot",
        "pokemon_crystal",
        "sc2",
        "xenobladex",
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "dark_souls_2",
        "tloz_oos",
        "pokemon_emerald",
        "tmc"
    ],
    "side": [
        "rabi_ribi",
        "albw",
        "oot",
        "celeste_open_world",
        "zillion",
        "v6",
        "oribf",
        "k64",
        "animal_well",
        "dkc",
        "faxanadu",
        "tetrisattack",
        "tmc",
        "ladx",
        "megamix",
        "metroidfusion",
        "messenger",
        "wl",
        "rogue_legacy",
        "nine_sols",
        "alttp",
        "blasphemous",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "mm3",
        "getting_over_it",
        "aquaria",
        "pokemon_crystal",
        "terraria",
        "mmx3",
        "monster_sanctuary",
        "ffmq",
        "sotn",
        "sm",
        "pokemon_frlg",
        "phoa",
        "ufo50",
        "xenobladex",
        "ff1",
        "musedash",
        "dlcquest",
        "momodoramoonlitfarewell",
        "ror1",
        "dark_souls_2",
        "lufia2ac",
        "cvcotm",
        "noita",
        "mlss",
        "wargroove",
        "tloz_ph",
        "pokemon_emerald",
        "dkc3",
        "madou",
        "sc2",
        "enderlilies",
        "tloz_oos",
        "celeste",
        "hylics2",
        "wl4",
        "marioland2",
        "sm_map_rando",
        "smw",
        "tloz_ooa",
        "spire",
        "mm2",
        "zelda2",
        "hk",
        "aus",
        "ff4fe",
        "dkc2",
        "mzm",
        "yoshisisland",
        "kdl3",
        "papermario",
        "wargroove2"
    ],
    "quests": [
        "ladx",
        "zelda2",
        "albw",
        "oot",
        "pokemon_crystal",
        "sc2",
        "xenobladex",
        "tloz_ph",
        "metroidprime",
        "alttp",
        "tloz_ooa",
        "dark_souls_2",
        "tloz_oos",
        "pokemon_emerald",
        "tmc"
    ],
    "potion": [
        "ladx",
        "zelda2",
        "albw",
        "kh1",
        "ss",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "gstla",
        "poe",
        "rogue_legacy",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "minecraft"
    ],
    "real-time combat": [
        "albw",
        "oot",
        "xenobladex",
        "doom_1993",
        "cv64",
        "alttp",
        "tloz_oos",
        "quake",
        "dkc",
        "sm64hacks",
        "kh1",
        "sm64ex",
        "landstalker",
        "metroidprime",
        "doom_ii",
        "dark_souls_2",
        "sm_map_rando",
        "tloz_ooa",
        "tmc",
        "ladx",
        "zelda2",
        "ss",
        "dk64",
        "spyro3",
        "sms",
        "sotn",
        "tloz_ph",
        "sm",
        "minecraft"
    ],
    "real-time": [
        "albw",
        "oot",
        "xenobladex",
        "doom_1993",
        "cv64",
        "alttp",
        "tloz_oos",
        "quake",
        "dkc",
        "sm64hacks",
        "kh1",
        "sm64ex",
        "landstalker",
        "metroidprime",
        "doom_ii",
        "dark_souls_2",
        "sm_map_rando",
        "tloz_ooa",
        "tmc",
        "ladx",
        "zelda2",
        "ss",
        "dk64",
        "spyro3",
        "sms",
        "sotn",
        "tloz_ph",
        "sm",
        "minecraft"
    ],
    "combat": [
        "albw",
        "oot",
        "xenobladex",
        "doom_1993",
        "cv64",
        "alttp",
        "tloz_oos",
        "quake",
        "dkc",
        "sm64hacks",
        "kh1",
        "sm64ex",
        "landstalker",
        "metroidprime",
        "doom_ii",
        "dark_souls_2",
        "sm_map_rando",
        "tloz_ooa",
        "tmc",
        "ladx",
        "zelda2",
        "ss",
        "dk64",
        "spyro3",
        "sms",
        "sotn",
        "tloz_ph",
        "sm",
        "minecraft"
    ],
    "self-referential humor": [
        "albw",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "earthbound"
    ],
    "self-referential": [
        "albw",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "earthbound"
    ],
    "humor": [
        "albw",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "earthbound"
    ],
    "rpg elements": [
        "lego_star_wars_tcs",
        "zelda2",
        "banjo_tooie",
        "albw",
        "oribf",
        "mzm",
        "metroidfusion",
        "mlss",
        "dark_souls_2",
        "sotn",
        "minecraft"
    ],
    "rpg": [
        "lego_star_wars_tcs",
        "zelda2",
        "banjo_tooie",
        "albw",
        "oribf",
        "mzm",
        "metroidfusion",
        "mlss",
        "dark_souls_2",
        "sotn",
        "minecraft"
    ],
    "elements": [
        "lego_star_wars_tcs",
        "zelda2",
        "banjo_tooie",
        "albw",
        "oribf",
        "mzm",
        "metroidfusion",
        "mlss",
        "dark_souls_2",
        "sotn",
        "minecraft"
    ],
    "mercenary": [
        "albw",
        "ss",
        "oot",
        "sc2",
        "metroidprime",
        "alttp",
        "sm_map_rando",
        "dark_souls_2",
        "sm",
        "quake"
    ],
    "coming of age": [
        "albw",
        "oribf",
        "oot",
        "pokemon_crystal",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "coming": [
        "albw",
        "oribf",
        "oot",
        "pokemon_crystal",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "age": [
        "albw",
        "oribf",
        "oot",
        "pokemon_crystal",
        "factorio_saws",
        "alttp",
        "gstla",
        "ffta",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "androgyny": [
        "albw",
        "ss",
        "oot",
        "gstla",
        "ffta",
        "sotn"
    ],
    "fast traveling": [
        "hk",
        "albw",
        "oot",
        "alttp",
        "undertale",
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "poe"
    ],
    "fast": [
        "hk",
        "albw",
        "oot",
        "alttp",
        "undertale",
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "poe"
    ],
    "traveling": [
        "hk",
        "albw",
        "oot",
        "alttp",
        "undertale",
        "tmc",
        "tloz_ph",
        "pokemon_emerald",
        "poe"
    ],
    "context sensitive": [
        "albw",
        "ss",
        "oot",
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "tloz_oos"
    ],
    "context": [
        "albw",
        "ss",
        "oot",
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "tloz_oos"
    ],
    "sensitive": [
        "albw",
        "ss",
        "oot",
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "tloz_oos"
    ],
    "living inventory": [
        "albw",
        "ss",
        "oot",
        "tww",
        "alttp",
        "mm_recomp",
        "tmc"
    ],
    "living": [
        "albw",
        "ss",
        "oot",
        "tww",
        "alttp",
        "mm_recomp",
        "tmc"
    ],
    "inventory": [
        "albw",
        "ss",
        "oot",
        "tww",
        "alttp",
        "mm_recomp",
        "tmc"
    ],
    "bees": [
        "albw",
        "dontstarvetogether",
        "alttp",
        "terraria",
        "raft",
        "tloz_ph",
        "minecraft"
    ],
    "a link to the past": [
        "alttp"
    ],
    "the legend of zelda: a link to the past": [
        "alttp"
    ],
    "to": [
        "smz3",
        "alttp"
    ],
    "past": [
        "smz3",
        "alttp"
    ],
    "satellaview": [
        "alttp",
        "madou",
        "yoshisisland"
    ],
    "super nintendo entertainment system": [
        "dkc3",
        "smz3",
        "soe",
        "ff4fe",
        "dkc2",
        "yoshisisland",
        "kdl3",
        "sm_map_rando",
        "alttp",
        "mmx3",
        "smw",
        "ffmq",
        "lufia2ac",
        "tetrisattack",
        "dkc",
        "sm",
        "earthbound"
    ],
    "super": [
        "dkc3",
        "soe",
        "madou",
        "alttp",
        "smo",
        "smz3",
        "dkc",
        "sm64hacks",
        "sm64ex",
        "marioland2",
        "sm_map_rando",
        "smw",
        "lufia2ac",
        "tetrisattack",
        "earthbound",
        "ff4fe",
        "dkc2",
        "yoshisisland",
        "kdl3",
        "wl",
        "mmx3",
        "ffmq",
        "sms",
        "sm"
    ],
    "entertainment": [
        "dkc3",
        "soe",
        "alttp",
        "ff1",
        "smz3",
        "dkc",
        "tloz",
        "mm3",
        "sm_map_rando",
        "smw",
        "faxanadu",
        "lufia2ac",
        "tetrisattack",
        "earthbound",
        "zelda2",
        "ff4fe",
        "dkc2",
        "yoshisisland",
        "kdl3",
        "mmx3",
        "ffmq",
        "sm"
    ],
    "wii": [
        "lego_star_wars_tcs",
        "dkc3",
        "stardew_valley",
        "oot",
        "xenobladex",
        "alttp",
        "ff1",
        "wl4",
        "mk64",
        "k64",
        "star_fox_64",
        "gstla",
        "ffta",
        "dkc",
        "tloz",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "landstalker",
        "smw",
        "sm_map_rando",
        "faxanadu",
        "tp",
        "pmd_eos",
        "earthbound",
        "tmc",
        "zelda2",
        "cvcotm",
        "hk",
        "ff4fe",
        "dkc2",
        "dk64",
        "mzm",
        "metroidfusion",
        "ss",
        "kdl3",
        "mlss",
        "papermario",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "terraria",
        "tloz_ph",
        "sm"
    ],
    "wii u": [
        "dkc3",
        "stardew_valley",
        "oot",
        "xenobladex",
        "alttp",
        "ff1",
        "wl4",
        "mk64",
        "k64",
        "star_fox_64",
        "gstla",
        "ffta",
        "dkc",
        "tloz",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "sm_map_rando",
        "smw",
        "pmd_eos",
        "earthbound",
        "tmc",
        "zelda2",
        "cvcotm",
        "hk",
        "mzm",
        "dkc2",
        "dk64",
        "ss",
        "metroidfusion",
        "kdl3",
        "mlss",
        "papermario",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "terraria",
        "tloz_ph",
        "sm"
    ],
    "u": [
        "dkc3",
        "stardew_valley",
        "oot",
        "xenobladex",
        "alttp",
        "ff1",
        "wl4",
        "mk64",
        "k64",
        "star_fox_64",
        "gstla",
        "ffta",
        "dkc",
        "tloz",
        "sm64hacks",
        "sm64ex",
        "mm3",
        "sm_map_rando",
        "smw",
        "pmd_eos",
        "earthbound",
        "tmc",
        "zelda2",
        "cvcotm",
        "hk",
        "mzm",
        "dkc2",
        "dk64",
        "ss",
        "metroidfusion",
        "kdl3",
        "mlss",
        "papermario",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "terraria",
        "tloz_ph",
        "sm"
    ],
    "new nintendo 3ds": [
        "dkc3",
        "dkc2",
        "sm_map_rando",
        "alttp",
        "mmx3",
        "smw",
        "dkc",
        "sm",
        "earthbound"
    ],
    "new": [
        "dkc3",
        "dkc2",
        "sm_map_rando",
        "alttp",
        "mmx3",
        "smw",
        "dkc",
        "sm",
        "earthbound"
    ],
    "super famicom": [
        "dkc3",
        "yoshisisland",
        "dkc2",
        "madou",
        "kdl3",
        "sm_map_rando",
        "alttp",
        "mmx3",
        "smw",
        "ffmq",
        "lufia2ac",
        "dkc",
        "sm",
        "earthbound"
    ],
    "famicom": [
        "dkc3",
        "yoshisisland",
        "dkc2",
        "madou",
        "kdl3",
        "sm_map_rando",
        "alttp",
        "mmx3",
        "smw",
        "ffmq",
        "lufia2ac",
        "dkc",
        "sm",
        "earthbound"
    ],
    "ghosts": [
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "cv64",
        "alttp",
        "luigismansion",
        "v6",
        "wl4",
        "sly1",
        "cuphead",
        "metroidprime",
        "tloz_ooa",
        "tmc",
        "earthbound",
        "aus",
        "dkc2",
        "mlss",
        "papermario",
        "rogue_legacy",
        "ffmq",
        "sms",
        "sotn"
    ],
    "mascot": [
        "ladx",
        "sly1",
        "mm3",
        "k64",
        "kdl3",
        "tloz_ph",
        "spyro3",
        "alttp",
        "papermario",
        "tloz_oos",
        "mm2",
        "jakanddaxter",
        "tmc"
    ],
    "death": [
        "oot",
        "openrct2",
        "cv64",
        "alttp",
        "tloz_oos",
        "luigismansion",
        "quake",
        "heretic",
        "v6",
        "sly1",
        "dark_souls_3",
        "star_fox_64",
        "gstla",
        "ffta",
        "dkc",
        "kh1",
        "mm3",
        "metroidprime",
        "doom_ii",
        "dark_souls_2",
        "tloz_ooa",
        "mm2",
        "tmc",
        "ladx",
        "cvcotm",
        "zelda2",
        "mzm",
        "dk64",
        "metroidfusion",
        "papermario",
        "mmx3",
        "rogue_legacy",
        "terraria",
        "sms",
        "sotn",
        "tloz_ph",
        "minecraft"
    ],
    "maze": [
        "ladx",
        "mzm",
        "openrct2",
        "doom_1993",
        "cv64",
        "alttp",
        "papermario",
        "witness",
        "tmc"
    ],
    "backtracking": [
        "banjo_tooie",
        "oot",
        "cv64",
        "alttp",
        "undertale",
        "tloz_oos",
        "quake",
        "ffta",
        "kh1",
        "metroidprime",
        "faxanadu",
        "jakanddaxter",
        "tmc",
        "witness",
        "ladx",
        "cvcotm",
        "mzm",
        "metroidfusion",
        "sotn",
        "tloz_ph"
    ],
    "undead": [
        "ladx",
        "tmc",
        "oot",
        "dsr",
        "mlss",
        "cv64",
        "alttp",
        "papermario",
        "dark_souls_2",
        "ffmq",
        "terraria",
        "tloz_ooa",
        "sotn",
        "tloz_oos",
        "heretic"
    ],
    "campaign": [
        "ladx",
        "zelda2",
        "ss",
        "oot",
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "tloz_oos",
        "tmc"
    ],
    "pixel art": [
        "stardew_valley",
        "alttp",
        "celeste_open_world",
        "undertale",
        "tloz_oos",
        "celeste",
        "v6",
        "wl4",
        "blasphemous",
        "animal_well",
        "crosscode",
        "timespinner",
        "ror1",
        "mm3",
        "sm_map_rando",
        "mm2",
        "hcniko",
        "tmc",
        "ladx",
        "zelda2",
        "tyrian",
        "mzm",
        "metroidfusion",
        "rogue_legacy",
        "terraria",
        "wargroove",
        "sotn",
        "sm"
    ],
    "pixel": [
        "stardew_valley",
        "alttp",
        "celeste_open_world",
        "undertale",
        "tloz_oos",
        "celeste",
        "v6",
        "wl4",
        "blasphemous",
        "animal_well",
        "crosscode",
        "timespinner",
        "ror1",
        "mm3",
        "sm_map_rando",
        "mm2",
        "hcniko",
        "tmc",
        "ladx",
        "zelda2",
        "tyrian",
        "mzm",
        "metroidfusion",
        "rogue_legacy",
        "terraria",
        "wargroove",
        "sotn",
        "sm"
    ],
    "art": [
        "stardew_valley",
        "alttp",
        "celeste_open_world",
        "undertale",
        "tloz_oos",
        "celeste",
        "v6",
        "wl4",
        "blasphemous",
        "animal_well",
        "crosscode",
        "timespinner",
        "ror1",
        "mm3",
        "sm_map_rando",
        "mm2",
        "hcniko",
        "tmc",
        "ladx",
        "zelda2",
        "tyrian",
        "mzm",
        "metroidfusion",
        "rogue_legacy",
        "terraria",
        "wargroove",
        "sotn",
        "sm"
    ],
    "easter egg": [
        "ladx",
        "banjo_tooie",
        "apeescape",
        "openrct2",
        "metroidfusion",
        "alttp",
        "doom_ii",
        "papermario",
        "rogue_legacy"
    ],
    "easter": [
        "ladx",
        "banjo_tooie",
        "apeescape",
        "openrct2",
        "metroidfusion",
        "alttp",
        "doom_ii",
        "papermario",
        "rogue_legacy"
    ],
    "egg": [
        "ladx",
        "banjo_tooie",
        "apeescape",
        "openrct2",
        "metroidfusion",
        "alttp",
        "doom_ii",
        "papermario",
        "rogue_legacy"
    ],
    "teleportation": [
        "v6",
        "pokemon_crystal",
        "cv64",
        "alttp",
        "doom_ii",
        "rogue_legacy",
        "terraria",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "jakanddaxter",
        "earthbound"
    ],
    "giant insects": [
        "dkc3",
        "hk",
        "soe",
        "dkc2",
        "dk64",
        "mlss",
        "alttp",
        "sms",
        "dkc",
        "pokemon_emerald"
    ],
    "giant": [
        "dkc3",
        "hk",
        "soe",
        "dkc2",
        "dk64",
        "mlss",
        "alttp",
        "sms",
        "dkc",
        "pokemon_emerald"
    ],
    "insects": [
        "dkc3",
        "hk",
        "soe",
        "dkc2",
        "dk64",
        "mlss",
        "alttp",
        "sms",
        "dkc",
        "pokemon_emerald"
    ],
    "silent protagonist": [
        "oot",
        "doom_1993",
        "alttp",
        "tloz_oos",
        "quake",
        "blasphemous",
        "k64",
        "gstla",
        "dkc",
        "tloz_ooa",
        "jakanddaxter",
        "tmc",
        "ladx",
        "hk",
        "zelda2",
        "dkc2",
        "ss",
        "mlss",
        "papermario",
        "ultrakill",
        "tloz_ph",
        "pokemon_emerald"
    ],
    "silent": [
        "oot",
        "doom_1993",
        "alttp",
        "tloz_oos",
        "quake",
        "blasphemous",
        "k64",
        "gstla",
        "dkc",
        "tloz_ooa",
        "jakanddaxter",
        "tmc",
        "ladx",
        "hk",
        "zelda2",
        "dkc2",
        "ss",
        "mlss",
        "papermario",
        "ultrakill",
        "tloz_ph",
        "pokemon_emerald"
    ],
    "explosion": [
        "lego_star_wars_tcs",
        "dkc3",
        "simpsonshitnrun",
        "openrct2",
        "cv64",
        "alttp",
        "quake",
        "mk64",
        "ffta",
        "cuphead",
        "mm3",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "tloz_ooa",
        "mm2",
        "tmc",
        "sonic_heroes",
        "zelda2",
        "mzm",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "mmx3",
        "terraria",
        "ffmq",
        "sms",
        "sotn",
        "sm",
        "minecraft"
    ],
    "monkey": [
        "ladx",
        "dkc3",
        "mk64",
        "apeescape",
        "dkc2",
        "dk64",
        "alttp",
        "diddy_kong_racing",
        "dkc"
    ],
    "nintendo power": [
        "dkc3",
        "dkc2",
        "sm_map_rando",
        "alttp",
        "dkc",
        "sm",
        "earthbound"
    ],
    "power": [
        "dkc3",
        "dkc2",
        "sm_map_rando",
        "alttp",
        "dkc",
        "sm",
        "earthbound"
    ],
    "world map": [
        "ladx",
        "dkc3",
        "v6",
        "phoa",
        "dkc2",
        "oot",
        "pokemon_crystal",
        "tloz_ph",
        "aquaria",
        "metroidprime",
        "alttp",
        "dkc",
        "tloz_oos",
        "jakanddaxter",
        "tmc"
    ],
    "map": [
        "ladx",
        "dkc3",
        "v6",
        "phoa",
        "dkc2",
        "oot",
        "pokemon_crystal",
        "tloz_ph",
        "aquaria",
        "metroidprime",
        "alttp",
        "dkc",
        "tloz_oos",
        "jakanddaxter",
        "tmc"
    ],
    "human": [
        "simpsonshitnrun",
        "sc2",
        "cv64",
        "alttp",
        "quake",
        "dark_souls_3",
        "gstla",
        "doom_ii",
        "dark_souls_2",
        "ladx",
        "zelda2",
        "apeescape",
        "ss",
        "metroidfusion",
        "papermario",
        "terraria",
        "sms",
        "sotn",
        "tloz_ph"
    ],
    "shopping": [
        "lego_star_wars_tcs",
        "yugiohddm",
        "pokemon_crystal",
        "mlss",
        "tloz_ph",
        "cv64",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "tmc",
        "cuphead"
    ],
    "ice stage": [
        "dkc3",
        "wl4",
        "banjo_tooie",
        "mk64",
        "dkc2",
        "oot",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "alttp",
        "terraria",
        "dkc",
        "jakanddaxter",
        "tmc"
    ],
    "ice": [
        "dkc3",
        "wl4",
        "banjo_tooie",
        "mk64",
        "dkc2",
        "oot",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "alttp",
        "terraria",
        "dkc",
        "jakanddaxter",
        "tmc"
    ],
    "stage": [
        "dkc3",
        "wl4",
        "banjo_tooie",
        "mk64",
        "dkc2",
        "oot",
        "metroidfusion",
        "cv64",
        "spyro3",
        "metroidprime",
        "alttp",
        "smw",
        "terraria",
        "dkc",
        "jakanddaxter",
        "tmc",
        "sonic_heroes"
    ],
    "saving the world": [
        "zelda2",
        "alttp",
        "dark_souls_2",
        "tloz_ph",
        "earthbound",
        "tmc"
    ],
    "saving": [
        "zelda2",
        "alttp",
        "dark_souls_2",
        "tloz_ph",
        "earthbound",
        "tmc"
    ],
    "grapple": [
        "lego_star_wars_tcs",
        "oot",
        "metroidprime",
        "alttp",
        "tloz_ph",
        "tmc"
    ],
    "secret area": [
        "dkc3",
        "alttp",
        "tunic",
        "tloz_oos",
        "heretic",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "sm_map_rando",
        "doom_ii",
        "hcniko",
        "tmc",
        "witness",
        "zelda2",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "sotn",
        "sm"
    ],
    "secret": [
        "dkc3",
        "soe",
        "alttp",
        "tunic",
        "tloz_oos",
        "heretic",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "sm_map_rando",
        "doom_ii",
        "hcniko",
        "tmc",
        "witness",
        "zelda2",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "sotn",
        "sm"
    ],
    "area": [
        "dkc3",
        "alttp",
        "tunic",
        "tloz_oos",
        "heretic",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "sm_map_rando",
        "doom_ii",
        "hcniko",
        "tmc",
        "witness",
        "zelda2",
        "dkc2",
        "metroidfusion",
        "rogue_legacy",
        "sotn",
        "sm"
    ],
    "shielded enemies": [
        "dkc3",
        "hk",
        "rogue_legacy",
        "alttp",
        "tloz_ooa",
        "tmc"
    ],
    "shielded": [
        "dkc3",
        "hk",
        "rogue_legacy",
        "alttp",
        "tloz_ooa",
        "tmc"
    ],
    "enemies": [
        "dkc3",
        "hk",
        "rogue_legacy",
        "alttp",
        "tloz_ooa",
        "tmc"
    ],
    "walking through walls": [
        "ladx",
        "oot",
        "alttp",
        "doom_ii",
        "tloz_ooa",
        "tloz_oos"
    ],
    "walking": [
        "ladx",
        "oot",
        "alttp",
        "doom_ii",
        "tloz_ooa",
        "tloz_oos"
    ],
    "through": [
        "ladx",
        "oot",
        "alttp",
        "doom_ii",
        "tloz_ooa",
        "tloz_oos"
    ],
    "walls": [
        "ladx",
        "oot",
        "alttp",
        "doom_ii",
        "tloz_ooa",
        "tloz_oos"
    ],
    "villain": [
        "lego_star_wars_tcs",
        "cvcotm",
        "zelda2",
        "banjo_tooie",
        "kh1",
        "oot",
        "mm3",
        "metroidfusion",
        "star_fox_64",
        "alttp",
        "papermario",
        "tloz_ooa",
        "sotn",
        "tloz_oos",
        "mm2",
        "tmc"
    ],
    "recurring boss": [
        "dkc3",
        "banjo_tooie",
        "kh1",
        "dkc2",
        "dk64",
        "mm3",
        "metroidfusion",
        "alttp",
        "papermario",
        "dkc",
        "pokemon_emerald"
    ],
    "recurring": [
        "dkc3",
        "banjo_tooie",
        "kh1",
        "dkc2",
        "dk64",
        "mm3",
        "metroidfusion",
        "alttp",
        "papermario",
        "dkc",
        "pokemon_emerald"
    ],
    "boss": [
        "dkc3",
        "banjo_tooie",
        "oot",
        "alttp",
        "dkc",
        "cuphead",
        "kh1",
        "mm3",
        "metroidprime",
        "doom_ii",
        "dark_souls_2",
        "tmc",
        "dkc2",
        "dk64",
        "metroidfusion",
        "papermario",
        "mm_recomp",
        "rogue_legacy",
        "sms",
        "tloz_ph",
        "pokemon_emerald"
    ],
    "been here before": [
        "simpsonshitnrun",
        "oot",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "ffta",
        "tloz_ph",
        "sms",
        "tmc"
    ],
    "been": [
        "simpsonshitnrun",
        "oot",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "ffta",
        "tloz_ph",
        "sms",
        "tmc"
    ],
    "here": [
        "simpsonshitnrun",
        "oot",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "ffta",
        "tloz_ph",
        "sms",
        "hcniko",
        "tmc"
    ],
    "before": [
        "simpsonshitnrun",
        "oot",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "ffta",
        "tloz_ph",
        "sms",
        "tmc"
    ],
    "sleeping": [
        "pokemon_crystal",
        "alttp",
        "gstla",
        "papermario",
        "sms",
        "tmc",
        "minecraft"
    ],
    "merchants": [
        "hk",
        "yugiohddm",
        "candybox2",
        "alttp",
        "terraria",
        "faxanadu",
        "timespinner"
    ],
    "fetch quests": [
        "ladx",
        "zelda2",
        "tloz_oos",
        "metroidprime",
        "alttp",
        "tloz_ph",
        "tmc"
    ],
    "fetch": [
        "ladx",
        "zelda2",
        "tloz_oos",
        "metroidprime",
        "alttp",
        "tloz_ph",
        "tmc"
    ],
    "poisoning": [
        "pokemon_crystal",
        "cv64",
        "papermario",
        "alttp",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "minecraft"
    ],
    "status effects": [
        "ladx",
        "zelda2",
        "pokemon_crystal",
        "alttp",
        "tloz_ooa",
        "dark_souls_2",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "status": [
        "ladx",
        "zelda2",
        "pokemon_crystal",
        "alttp",
        "tloz_ooa",
        "dark_souls_2",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "effects": [
        "ladx",
        "zelda2",
        "pokemon_crystal",
        "alttp",
        "tloz_ooa",
        "dark_souls_2",
        "tmc",
        "tloz_oos",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "damage over time": [
        "oot",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "ffta",
        "tloz_oos",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "damage": [
        "oot",
        "pokemon_crystal",
        "tloz_ph",
        "alttp",
        "ffta",
        "tloz_oos",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "over": [
        "oot",
        "pokemon_crystal",
        "getting_over_it",
        "tloz_ph",
        "alttp",
        "ffta",
        "tloz_oos",
        "pokemon_emerald",
        "jakanddaxter",
        "tmc"
    ],
    "monomyth": [
        "zelda2",
        "ss",
        "mm3",
        "alttp",
        "tloz_ph",
        "mm2",
        "tmc"
    ],
    "retroachievements": [
        "dkc3",
        "banjo_tooie",
        "oot",
        "cv64",
        "alttp",
        "quake",
        "mk64",
        "k64",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "tloz",
        "sm64hacks",
        "sm64ex",
        "tww",
        "metroidprime",
        "smw",
        "lufia2ac",
        "tetrisattack",
        "pmd_eos",
        "earthbound",
        "sonic_heroes",
        "ff4fe",
        "dkc2",
        "dk64",
        "swr",
        "kdl3",
        "papermario",
        "mmx3",
        "mm_recomp",
        "ffmq",
        "sms"
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
        "dkc3",
        "rabi_ribi",
        "phoa",
        "ufo50",
        "madou",
        "enderlilies",
        "celeste_open_world",
        "ff1",
        "musedash",
        "zillion",
        "celeste",
        "v6",
        "hylics2",
        "wl4",
        "oribf",
        "blasphemous",
        "k64",
        "animal_well",
        "dkc",
        "pokemon_rb",
        "smz3",
        "timespinner",
        "cuphead",
        "sm",
        "marioland2",
        "dlcquest",
        "momodoramoonlitfarewell",
        "mm3",
        "getting_over_it",
        "ror1",
        "aquaria",
        "sm_map_rando",
        "smw",
        "faxanadu",
        "lufia2ac",
        "spire",
        "tetrisattack",
        "mm2",
        "ladx",
        "cvcotm",
        "hk",
        "megamix",
        "noita",
        "aus",
        "zelda2",
        "ff4fe",
        "dkc2",
        "mzm",
        "pokemon_crystal",
        "metroidfusion",
        "yoshisisland",
        "kdl3",
        "messenger",
        "mlss",
        "wl",
        "papermario",
        "mmx3",
        "monster_sanctuary",
        "ffmq",
        "nine_sols",
        "rogue_legacy",
        "sotn",
        "terraria",
        "wargroove",
        "pokemon_emerald",
        "wargroove2",
        "pokemon_frlg"
    ],
    "horror": [
        "lunacid",
        "residentevil3remake",
        "doom_1993",
        "cv64",
        "undertale",
        "shivers",
        "luigismansion",
        "quake",
        "dredge",
        "blasphemous",
        "inscryption",
        "animal_well",
        "dontstarvetogether",
        "cccharles",
        "lethal_company",
        "getting_over_it",
        "doom_ii",
        "residentevil2remake",
        "poe",
        "cvcotm",
        "terraria",
        "mm_recomp",
        "sotn"
    ],
    "survival": [
        "cccharles",
        "rimworld",
        "residentevil3remake",
        "ror1",
        "raft",
        "ror2",
        "subnautica",
        "animal_well",
        "dontstarvetogether",
        "factorio_saws",
        "terraria",
        "factorio",
        "residentevil2remake",
        "yugioh06",
        "minecraft"
    ],
    "mystery": [
        "dredge",
        "crystal_project",
        "outer_wilds",
        "inscryption",
        "animal_well",
        "pmd_eos",
        "witness"
    ],
    "exploration": [
        "rabi_ribi",
        "outer_wilds",
        "cv64",
        "celeste_open_world",
        "tunic",
        "celeste",
        "seaofthieves",
        "hylics2",
        "v6",
        "dredge",
        "lingo",
        "animal_well",
        "sm",
        "lethal_company",
        "dlcquest",
        "aquaria",
        "metroidprime",
        "sm_map_rando",
        "hcniko",
        "jakanddaxter",
        "witness",
        "pokemon_crystal",
        "metroidfusion",
        "subnautica",
        "tloz_ph",
        "rogue_legacy",
        "terraria",
        "shorthike",
        "pokemon_emerald"
    ],
    "retro": [
        "celeste",
        "v6",
        "hylics2",
        "ufo50",
        "stardew_valley",
        "dlcquest",
        "blasphemous",
        "messenger",
        "animal_well",
        "celeste_open_world",
        "terraria",
        "undertale",
        "smo",
        "timespinner",
        "minecraft",
        "cuphead"
    ],
    "2d": [
        "rabi_ribi",
        "stardew_valley",
        "celeste_open_world",
        "undertale",
        "musedash",
        "celeste",
        "v6",
        "blasphemous",
        "animal_well",
        "dontstarvetogether",
        "cuphead",
        "sm_map_rando",
        "earthbound",
        "zelda2",
        "hk",
        "messenger",
        "terraria",
        "nine_sols",
        "sotn",
        "sm"
    ],
    "metroidvania": [
        "rabi_ribi",
        "phoa",
        "enderlilies",
        "pseudoregalia",
        "zillion",
        "v6",
        "oribf",
        "crystal_project",
        "blasphemous",
        "animal_well",
        "timespinner",
        "momodoramoonlitfarewell",
        "aquaria",
        "metroidprime",
        "sm_map_rando",
        "frogmonster",
        "dark_souls_2",
        "faxanadu",
        "zelda2",
        "cvcotm",
        "hk",
        "aus",
        "mzm",
        "metroidfusion",
        "messenger",
        "rogue_legacy",
        "nine_sols",
        "monster_sanctuary",
        "sotn",
        "sm"
    ],
    "atmospheric": [
        "celeste",
        "hk",
        "hylics2",
        "powerwashsimulator",
        "crystal_project",
        "animal_well",
        "dontstarvetogether",
        "celeste_open_world",
        "frogmonster",
        "tunic",
        "shorthike"
    ],
    "relaxing": [
        "powerwashsimulator",
        "stardew_valley",
        "animal_well",
        "sims4",
        "hcniko",
        "shorthike"
    ],
    "controller support": [
        "v6",
        "hk",
        "stardew_valley",
        "animal_well",
        "tunic",
        "shorthike",
        "hcniko"
    ],
    "controller": [
        "v6",
        "hk",
        "stardew_valley",
        "animal_well",
        "tunic",
        "shorthike",
        "hcniko"
    ],
    "support": [
        "v6",
        "hk",
        "stardew_valley",
        "animal_well",
        "tunic",
        "shorthike",
        "hcniko"
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
        "lego_star_wars_tcs",
        "apeescape",
        "kh2",
        "spyro3",
        "rogue_legacy",
        "terraria",
        "dark_souls_2",
        "sadx",
        "sotn",
        "sa2b",
        "sonic_heroes"
    ],
    "3": [
        "lego_star_wars_tcs",
        "apeescape",
        "kh2",
        "residentevil3remake",
        "mm3",
        "kdl3",
        "wl",
        "spyro3",
        "rogue_legacy",
        "terraria",
        "dark_souls_2",
        "sadx",
        "sotn",
        "sa2b",
        "mmbn3",
        "sonic_heroes"
    ],
    "playstation portable": [
        "sotn",
        "spyro3",
        "apeescape"
    ],
    "portable": [
        "sotn",
        "spyro3",
        "apeescape"
    ],
    "anime": [
        "rabi_ribi",
        "wl4",
        "osu",
        "apeescape",
        "yugiohddm",
        "pokemon_crystal",
        "zillion",
        "gstla",
        "fm",
        "dw1",
        "musedash",
        "pokemon_emerald"
    ],
    "dinosaurs": [
        "banjo_tooie",
        "apeescape",
        "yoshisisland",
        "smw",
        "sms",
        "earthbound",
        "smo"
    ],
    "collecting": [
        "zelda2",
        "banjo_tooie",
        "apeescape",
        "mzm",
        "pokemon_crystal",
        "pokemon_rb",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "multiple endings": [
        "wl4",
        "apeescape",
        "kh1",
        "dkc2",
        "dk64",
        "mzm",
        "k64",
        "star_fox_64",
        "cv64",
        "metroidprime",
        "doom_ii",
        "mmx3",
        "civ_6",
        "undertale",
        "sotn",
        "tloz_oos",
        "witness",
        "cuphead"
    ],
    "multiple": [
        "lego_star_wars_tcs",
        "dkc3",
        "cv64",
        "undertale",
        "tloz_oos",
        "wl4",
        "k64",
        "star_fox_64",
        "civ_6",
        "dkc",
        "cuphead",
        "kh1",
        "metroidprime",
        "doom_ii",
        "earthbound",
        "sonic_heroes",
        "witness",
        "apeescape",
        "mzm",
        "dkc2",
        "dk64",
        "mlss",
        "spyro3",
        "rogue_legacy",
        "mmx3",
        "sotn"
    ],
    "endings": [
        "wl4",
        "apeescape",
        "kh1",
        "dkc2",
        "dk64",
        "mzm",
        "k64",
        "star_fox_64",
        "cv64",
        "metroidprime",
        "doom_ii",
        "mmx3",
        "civ_6",
        "undertale",
        "sotn",
        "tloz_oos",
        "witness",
        "cuphead"
    ],
    "amnesia": [
        "apeescape",
        "xenobladex",
        "aquaria",
        "tloz_ph",
        "witness",
        "sonic_heroes"
    ],
    "voice acting": [
        "sly1",
        "simpsonshitnrun",
        "bfbb",
        "apeescape",
        "kh1",
        "sonic_heroes",
        "star_fox_64",
        "xenobladex",
        "cv64",
        "doom_ii",
        "civ_6",
        "sms",
        "dw1",
        "jakanddaxter",
        "witness",
        "cuphead"
    ],
    "voice": [
        "sly1",
        "simpsonshitnrun",
        "bfbb",
        "apeescape",
        "kh1",
        "sonic_heroes",
        "star_fox_64",
        "xenobladex",
        "cv64",
        "doom_ii",
        "civ_6",
        "sms",
        "dw1",
        "jakanddaxter",
        "witness",
        "cuphead"
    ],
    "acting": [
        "sly1",
        "simpsonshitnrun",
        "bfbb",
        "apeescape",
        "kh1",
        "sonic_heroes",
        "star_fox_64",
        "xenobladex",
        "cv64",
        "doom_ii",
        "civ_6",
        "sms",
        "dw1",
        "jakanddaxter",
        "witness",
        "cuphead"
    ],
    "moving platforms": [
        "dkc3",
        "cv64",
        "quake",
        "v6",
        "wl4",
        "sly1",
        "blasphemous",
        "k64",
        "dkc",
        "bfbb",
        "mm3",
        "metroidprime",
        "mm2",
        "jakanddaxter",
        "tmc",
        "sonic_heroes",
        "ladx",
        "cvcotm",
        "apeescape",
        "dk64",
        "spyro3",
        "papermario",
        "mmx3",
        "sms",
        "sotn",
        "tloz_ph"
    ],
    "moving": [
        "dkc3",
        "cv64",
        "quake",
        "v6",
        "wl4",
        "sly1",
        "blasphemous",
        "k64",
        "dkc",
        "bfbb",
        "mm3",
        "metroidprime",
        "mm2",
        "jakanddaxter",
        "tmc",
        "sonic_heroes",
        "ladx",
        "cvcotm",
        "apeescape",
        "dk64",
        "spyro3",
        "papermario",
        "mmx3",
        "sms",
        "sotn",
        "tloz_ph"
    ],
    "platforms": [
        "dkc3",
        "cv64",
        "quake",
        "v6",
        "wl4",
        "oribf",
        "sly1",
        "blasphemous",
        "k64",
        "dkc",
        "bfbb",
        "mm3",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "mm2",
        "jakanddaxter",
        "tmc",
        "sonic_heroes",
        "ladx",
        "cvcotm",
        "zelda2",
        "apeescape",
        "dk64",
        "spyro3",
        "papermario",
        "mmx3",
        "sms",
        "sotn",
        "tloz_ph",
        "sm"
    ],
    "time trials": [
        "v6",
        "sly1",
        "mk64",
        "apeescape",
        "spyro3",
        "diddy_kong_racing"
    ],
    "trials": [
        "v6",
        "sly1",
        "mk64",
        "apeescape",
        "spyro3",
        "diddy_kong_racing"
    ],
    "archipela-go!": [
        "apgo"
    ],
    "multiplayer": [
        "jigsaw",
        "archipidle",
        "chatipelago",
        "_tracker",
        "generic",
        "yachtdice",
        "wordipelago",
        "checksfinder",
        "_debug",
        "_manual",
        "apgo",
        "apsudoku",
        "saving_princess",
        "clique",
        "paint"
    ],
    "archipelago": [
        "jigsaw",
        "archipidle",
        "chatipelago",
        "_tracker",
        "bumpstik",
        "generic",
        "yachtdice",
        "wordipelago",
        "checksfinder",
        "_debug",
        "_manual",
        "apgo",
        "apsudoku",
        "saving_princess",
        "clique",
        "paint"
    ],
    "hints": [
        "jigsaw",
        "archipidle",
        "chatipelago",
        "_tracker",
        "generic",
        "yachtdice",
        "wordipelago",
        "checksfinder",
        "_debug",
        "_manual",
        "apgo",
        "apsudoku",
        "saving_princess",
        "clique",
        "paint"
    ],
    "multiworld": [
        "jigsaw",
        "archipidle",
        "chatipelago",
        "_tracker",
        "generic",
        "yachtdice",
        "wordipelago",
        "checksfinder",
        "_debug",
        "_manual",
        "apgo",
        "apsudoku",
        "saving_princess",
        "clique",
        "paint"
    ],
    "sudoku": [
        "apsudoku"
    ],
    "aquaria": [
        "aquaria"
    ],
    "drama": [
        "hades",
        "undertale",
        "earthbound",
        "aquaria"
    ],
    "linux": [
        "stardew_valley",
        "openrct2",
        "doom_1993",
        "celeste_open_world",
        "undertale",
        "shapez",
        "quake",
        "celeste",
        "v6",
        "osu",
        "cat_quest",
        "blasphemous",
        "crystal_project",
        "inscryption",
        "dontstarvetogether",
        "factorio",
        "crosscode",
        "timespinner",
        "chainedechoes",
        "bumpstik",
        "ror1",
        "getting_over_it",
        "aquaria",
        "landstalker",
        "overcooked2",
        "hk",
        "rimworld",
        "factorio_saws",
        "rogue_legacy",
        "terraria",
        "monster_sanctuary",
        "shorthike",
        "minecraft",
        "celeste64"
    ],
    "android": [
        "lego_star_wars_tcs",
        "v6",
        "osu",
        "dredge",
        "cat_quest",
        "brotato",
        "shapez",
        "stardew_valley",
        "blasphemous",
        "getting_over_it",
        "subnautica",
        "aquaria",
        "osrs",
        "terraria",
        "wargroove2",
        "balatro",
        "musedash"
    ],
    "ios": [
        "lego_star_wars_tcs",
        "stardew_valley",
        "residentevil3remake",
        "shapez",
        "musedash",
        "v6",
        "osu",
        "dredge",
        "cat_quest",
        "blasphemous",
        "hades",
        "getting_over_it",
        "aquaria",
        "balatro",
        "residentevil2remake",
        "witness",
        "brotato",
        "hitman_woa",
        "subnautica",
        "osrs",
        "terraria",
        "wargroove2"
    ],
    "alternate costumes": [
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "kh1",
        "metroidfusion",
        "cv64",
        "aquaria",
        "sms",
        "smo"
    ],
    "alternate": [
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "kh1",
        "metroidfusion",
        "cv64",
        "aquaria",
        "sms",
        "smo"
    ],
    "costumes": [
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "kh1",
        "metroidfusion",
        "cv64",
        "aquaria",
        "sms",
        "smo"
    ],
    "underwater gameplay": [
        "banjo_tooie",
        "kh1",
        "sm64ex",
        "dkc2",
        "oot",
        "mm3",
        "metroidfusion",
        "subnautica",
        "aquaria",
        "metroidprime",
        "terraria",
        "mmx3",
        "sms",
        "dkc",
        "mm2",
        "quake",
        "smo",
        "sm64hacks"
    ],
    "underwater": [
        "banjo_tooie",
        "kh1",
        "sm64ex",
        "dkc2",
        "oot",
        "mm3",
        "metroidfusion",
        "subnautica",
        "aquaria",
        "metroidprime",
        "terraria",
        "mmx3",
        "sms",
        "dkc",
        "mm2",
        "quake",
        "smo",
        "sm64hacks"
    ],
    "gameplay": [
        "banjo_tooie",
        "kh1",
        "sm64ex",
        "dkc2",
        "oot",
        "mm3",
        "metroidfusion",
        "subnautica",
        "aquaria",
        "metroidprime",
        "terraria",
        "mmx3",
        "sms",
        "dkc",
        "mm2",
        "quake",
        "smo",
        "sm64hacks"
    ],
    "shape-shifting": [
        "banjo_tooie",
        "k64",
        "kdl3",
        "aquaria",
        "metroidprime",
        "mm_recomp",
        "sotn"
    ],
    "plot twist": [
        "kh1",
        "oot",
        "metroidfusion",
        "cv64",
        "aquaria",
        "undertale"
    ],
    "plot": [
        "kh1",
        "oot",
        "metroidfusion",
        "cv64",
        "aquaria",
        "undertale"
    ],
    "twist": [
        "kh1",
        "oot",
        "metroidfusion",
        "cv64",
        "aquaria",
        "undertale"
    ],
    "archipidle": [
        "archipidle"
    ],
    "an untitled story": [
        "aus"
    ],
    "an": [
        "aus"
    ],
    "untitled": [
        "aus"
    ],
    "story": [
        "celeste",
        "powerwashsimulator",
        "hylics2",
        "aus",
        "dredge",
        "getting_over_it",
        "celeste_open_world",
        "hades",
        "undertale"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "hylics2",
        "pokemon_rb",
        "yugiohddm",
        "wargroove2",
        "crystal_project",
        "yugioh06",
        "pokemon_frlg",
        "monster_sanctuary",
        "civ_6",
        "ffta",
        "undertale",
        "fm",
        "balatro",
        "wargroove",
        "pokemon_emerald",
        "pmd_eos",
        "earthbound"
    ],
    "turn-based": [
        "undertale",
        "hylics2",
        "crystal_project",
        "gstla",
        "civ_6",
        "ffta",
        "pokemon_rb",
        "yugiohddm",
        "fm",
        "balatro",
        "pmd_eos",
        "earthbound",
        "yugioh06",
        "pokemon_crystal",
        "mlss",
        "papermario",
        "wargroove",
        "ffmq",
        "monster_sanctuary",
        "wargroove2",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "(tbs)": [
        "hylics2",
        "pokemon_rb",
        "yugiohddm",
        "wargroove2",
        "crystal_project",
        "yugioh06",
        "pokemon_frlg",
        "monster_sanctuary",
        "civ_6",
        "ffta",
        "undertale",
        "fm",
        "balatro",
        "wargroove",
        "pokemon_emerald",
        "pmd_eos",
        "earthbound"
    ],
    "card & board game": [
        "yugiohddm",
        "inscryption",
        "spire",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "card": [
        "yugiohddm",
        "inscryption",
        "spire",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "board": [
        "yugiohddm",
        "inscryption",
        "spire",
        "fm",
        "balatro",
        "yugioh06"
    ],
    "game": [
        "oot",
        "tloz_oos",
        "mmbn3",
        "wl4",
        "inscryption",
        "gstla",
        "ffta",
        "pokemon_rb",
        "marioland2",
        "yugiohddm",
        "doom_ii",
        "tloz_ooa",
        "spire",
        "fm",
        "balatro",
        "mm2",
        "hcniko",
        "yugioh06",
        "earthbound",
        "tmc",
        "ladx",
        "cvcotm",
        "witness",
        "mzm",
        "dkc2",
        "pokemon_crystal",
        "metroidfusion",
        "mlss",
        "wl",
        "spyro3",
        "rogue_legacy",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "roguelike": [
        "ror1",
        "rogue_legacy",
        "hades",
        "spire",
        "balatro",
        "pmd_eos"
    ],
    "banjo-tooie": [
        "banjo_tooie"
    ],
    "quiz/trivia": [
        "banjo_tooie"
    ],
    "comedy": [
        "lego_star_wars_tcs",
        "banjo_tooie",
        "simpsonshitnrun",
        "candybox2",
        "toontown",
        "undertale",
        "luigismansion",
        "musedash",
        "quake",
        "sly1",
        "diddy_kong_racing",
        "cuphead",
        "doronko_wanko",
        "zork_grand_inquisitor",
        "bfbb",
        "kh1",
        "dlcquest",
        "lethal_company",
        "getting_over_it",
        "placidplasticducksim",
        "sims4",
        "hcniko",
        "jakanddaxter",
        "overcooked2",
        "dkc2",
        "dk64",
        "rac2",
        "messenger",
        "mlss",
        "spyro3",
        "papermario",
        "rogue_legacy",
        "dw1"
    ],
    "nintendo 64": [
        "banjo_tooie",
        "mk64",
        "sm64ex",
        "dk64",
        "oot",
        "k64",
        "star_fox_64",
        "swr",
        "cv64",
        "papermario",
        "mm_recomp",
        "diddy_kong_racing",
        "sm64hacks"
    ],
    "64": [
        "banjo_tooie",
        "mk64",
        "sm64ex",
        "dk64",
        "oot",
        "k64",
        "star_fox_64",
        "swr",
        "cv64",
        "papermario",
        "mm_recomp",
        "diddy_kong_racing",
        "sm64hacks"
    ],
    "aliens": [
        "lego_star_wars_tcs",
        "banjo_tooie",
        "sm",
        "simpsonshitnrun",
        "lethal_company",
        "mzm",
        "metroidfusion",
        "sc2",
        "xenobladex",
        "factorio_saws",
        "metroidprime",
        "sm_map_rando",
        "factorio",
        "hcniko",
        "quake",
        "earthbound"
    ],
    "flight": [
        "lego_star_wars_tcs",
        "hylics2",
        "banjo_tooie",
        "wl4",
        "mm3",
        "star_fox_64",
        "xenobladex",
        "spyro3",
        "rogue_legacy",
        "terraria",
        "diddy_kong_racing",
        "shorthike",
        "mm2",
        "dkc"
    ],
    "witches": [
        "banjo_tooie",
        "cv64",
        "enderlilies",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "minecraft"
    ],
    "achievements": [
        "lego_star_wars_tcs",
        "hk",
        "v6",
        "banjo_tooie",
        "oribf",
        "stardew_valley",
        "blasphemous",
        "sonic_heroes",
        "tunic",
        "doom_ii",
        "dark_souls_2",
        "sotn",
        "shorthike",
        "musedash",
        "hcniko",
        "minecraft",
        "cuphead"
    ],
    "talking animals": [
        "dkc3",
        "banjo_tooie",
        "sly1",
        "bfbb",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "hcniko",
        "dkc"
    ],
    "talking": [
        "dkc3",
        "banjo_tooie",
        "sly1",
        "bfbb",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "hcniko",
        "dkc"
    ],
    "animals": [
        "dkc3",
        "banjo_tooie",
        "sly1",
        "bfbb",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "hcniko",
        "dkc"
    ],
    "breaking the fourth wall": [
        "ladx",
        "banjo_tooie",
        "simpsonshitnrun",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "doom_ii",
        "rogue_legacy",
        "undertale",
        "ffta",
        "dkc",
        "jakanddaxter",
        "tmc"
    ],
    "breaking": [
        "banjo_tooie",
        "simpsonshitnrun",
        "oot",
        "undertale",
        "wl4",
        "ffta",
        "dkc",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "tloz_ooa",
        "jakanddaxter",
        "tmc",
        "ladx",
        "mzm",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "rogue_legacy",
        "sotn",
        "sm"
    ],
    "fourth": [
        "ladx",
        "banjo_tooie",
        "simpsonshitnrun",
        "dkc2",
        "metroidfusion",
        "mlss",
        "papermario",
        "doom_ii",
        "rogue_legacy",
        "undertale",
        "ffta",
        "dkc",
        "jakanddaxter",
        "tmc"
    ],
    "temporary invincibility": [
        "banjo_tooie",
        "mk64",
        "dkc2",
        "sonic_heroes",
        "papermario",
        "doom_ii",
        "rogue_legacy",
        "faxanadu",
        "quake",
        "jakanddaxter",
        "cuphead"
    ],
    "temporary": [
        "banjo_tooie",
        "mk64",
        "dkc2",
        "sonic_heroes",
        "papermario",
        "doom_ii",
        "rogue_legacy",
        "faxanadu",
        "quake",
        "jakanddaxter",
        "cuphead"
    ],
    "invincibility": [
        "banjo_tooie",
        "mk64",
        "dkc2",
        "sonic_heroes",
        "papermario",
        "doom_ii",
        "rogue_legacy",
        "faxanadu",
        "quake",
        "jakanddaxter",
        "cuphead"
    ],
    "gliding": [
        "banjo_tooie",
        "sly1",
        "kh1",
        "spyro3",
        "sms",
        "shorthike",
        "tmc"
    ],
    "lgbtq+": [
        "celeste",
        "banjo_tooie",
        "simpsonshitnrun",
        "celeste_open_world",
        "rogue_legacy",
        "sims4",
        "timespinner",
        "celeste64"
    ],
    "battle for bikini bottom": [
        "bfbb"
    ],
    "spongebob squarepants: battle for bikini bottom": [
        "bfbb"
    ],
    "spongebob": [
        "bfbb"
    ],
    "squarepants:": [
        "bfbb"
    ],
    "battle": [
        "mmbn3",
        "sa2b",
        "bfbb"
    ],
    "for": [
        "bfbb"
    ],
    "bikini": [
        "bfbb"
    ],
    "bottom": [
        "bfbb"
    ],
    "nintendo gamecube": [
        "mario_kart_double_dash",
        "simpsonshitnrun",
        "bfbb",
        "tww",
        "metroidprime",
        "sms",
        "dw1",
        "luigismansion",
        "sonic_heroes"
    ],
    "gamecube": [
        "mario_kart_double_dash",
        "simpsonshitnrun",
        "bfbb",
        "tww",
        "metroidprime",
        "sms",
        "dw1",
        "luigismansion",
        "sonic_heroes"
    ],
    "playstation 2": [
        "sly1",
        "simpsonshitnrun",
        "kh1",
        "bfbb",
        "kh2",
        "rac2",
        "dw1",
        "jakanddaxter",
        "sonic_heroes"
    ],
    "2": [
        "simpsonshitnrun",
        "stardew_valley",
        "candybox2",
        "smo",
        "hylics2",
        "sly1",
        "kh2",
        "factorio",
        "bfbb",
        "kh1",
        "ror2",
        "residentevil2remake",
        "kindergarten_2",
        "overcooked2",
        "jakanddaxter",
        "sonic_heroes",
        "rac2",
        "wargroove2",
        "dw1"
    ],
    "robots": [
        "lego_star_wars_tcs",
        "bfbb",
        "mm3",
        "metroidfusion",
        "sonic_heroes",
        "star_fox_64",
        "swr",
        "xenobladex",
        "mmx3",
        "ultrakill",
        "sms",
        "mm2",
        "earthbound",
        "cuphead"
    ],
    "kid friendly": [
        "lego_star_wars_tcs",
        "bfbb",
        "openrct2",
        "pokemon_crystal",
        "k64",
        "pokemon_emerald"
    ],
    "kid": [
        "lego_star_wars_tcs",
        "bfbb",
        "openrct2",
        "pokemon_crystal",
        "k64",
        "pokemon_emerald"
    ],
    "friendly": [
        "lego_star_wars_tcs",
        "bfbb",
        "openrct2",
        "pokemon_crystal",
        "k64",
        "pokemon_emerald"
    ],
    "bink video": [
        "simpsonshitnrun",
        "bfbb",
        "dark_souls_3",
        "civ_6",
        "witness",
        "poe"
    ],
    "bink": [
        "simpsonshitnrun",
        "bfbb",
        "dark_souls_3",
        "civ_6",
        "witness",
        "poe"
    ],
    "video": [
        "simpsonshitnrun",
        "bfbb",
        "dark_souls_3",
        "civ_6",
        "witness",
        "poe"
    ],
    "blasphemous": [
        "blasphemous"
    ],
    "role-playing (rpg)": [
        "rabi_ribi",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "lunacid",
        "ufo50",
        "dsr",
        "madou",
        "xenobladex",
        "enderlilies",
        "candybox2",
        "tunic",
        "toontown",
        "ff1",
        "undertale",
        "tloz_oos",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "hylics2",
        "ctjot",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "crystal_project",
        "gstla",
        "hades",
        "ffta",
        "pokemon_rb",
        "crosscode",
        "timespinner",
        "chainedechoes",
        "kh1",
        "ror1",
        "landstalker",
        "tloz_ooa",
        "dark_souls_2",
        "faxanadu",
        "lufia2ac",
        "sims4",
        "pmd_eos",
        "earthbound",
        "poe",
        "zelda2",
        "cvcotm",
        "noita",
        "brotato",
        "ff4fe",
        "pokemon_crystal",
        "mlss",
        "osrs",
        "papermario",
        "rogue_legacy",
        "monster_sanctuary",
        "ffmq",
        "terraria",
        "wargroove2",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "role-playing": [
        "rabi_ribi",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "lunacid",
        "ufo50",
        "dsr",
        "madou",
        "xenobladex",
        "enderlilies",
        "candybox2",
        "tunic",
        "toontown",
        "ff1",
        "undertale",
        "tloz_oos",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "hylics2",
        "ctjot",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "crystal_project",
        "gstla",
        "hades",
        "ffta",
        "pokemon_rb",
        "crosscode",
        "timespinner",
        "chainedechoes",
        "kh1",
        "ror1",
        "landstalker",
        "tloz_ooa",
        "dark_souls_2",
        "faxanadu",
        "lufia2ac",
        "sims4",
        "pmd_eos",
        "earthbound",
        "poe",
        "zelda2",
        "cvcotm",
        "noita",
        "brotato",
        "ff4fe",
        "pokemon_crystal",
        "mlss",
        "osrs",
        "papermario",
        "rogue_legacy",
        "monster_sanctuary",
        "ffmq",
        "terraria",
        "wargroove2",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "(rpg)": [
        "rabi_ribi",
        "meritous",
        "phoa",
        "soe",
        "stardew_valley",
        "lunacid",
        "ufo50",
        "dsr",
        "madou",
        "xenobladex",
        "enderlilies",
        "candybox2",
        "tunic",
        "toontown",
        "ff1",
        "undertale",
        "tloz_oos",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "hylics2",
        "ctjot",
        "dredge",
        "cat_quest",
        "dark_souls_3",
        "kh2",
        "blasphemous",
        "crystal_project",
        "gstla",
        "hades",
        "ffta",
        "pokemon_rb",
        "crosscode",
        "timespinner",
        "chainedechoes",
        "kh1",
        "ror1",
        "landstalker",
        "tloz_ooa",
        "dark_souls_2",
        "faxanadu",
        "lufia2ac",
        "sims4",
        "pmd_eos",
        "earthbound",
        "poe",
        "zelda2",
        "cvcotm",
        "noita",
        "brotato",
        "ff4fe",
        "pokemon_crystal",
        "mlss",
        "osrs",
        "papermario",
        "rogue_legacy",
        "monster_sanctuary",
        "ffmq",
        "terraria",
        "wargroove2",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "hack and slash/beat 'em up": [
        "ror1",
        "blasphemous",
        "cv64",
        "nine_sols",
        "hades",
        "poe"
    ],
    "hack": [
        "ror1",
        "blasphemous",
        "cv64",
        "nine_sols",
        "hades",
        "poe"
    ],
    "slash/beat": [
        "ror1",
        "blasphemous",
        "cv64",
        "nine_sols",
        "hades",
        "poe"
    ],
    "'em": [
        "ror1",
        "blasphemous",
        "cv64",
        "nine_sols",
        "hades",
        "poe"
    ],
    "up": [
        "cv64",
        "undertale",
        "blasphemous",
        "gstla",
        "hades",
        "kh1",
        "ror1",
        "landstalker",
        "dark_souls_2",
        "poe",
        "earthbound",
        "zelda2",
        "cvcotm",
        "pokemon_crystal",
        "papermario",
        "nine_sols",
        "sotn",
        "dw1",
        "pokemon_emerald"
    ],
    "bloody": [
        "blasphemous",
        "cv64",
        "metroidprime",
        "doom_ii",
        "poe",
        "ultrakill",
        "sotn",
        "residentevil2remake",
        "quake",
        "heretic"
    ],
    "difficult": [
        "celeste",
        "rabi_ribi",
        "zelda2",
        "ror1",
        "blasphemous",
        "getting_over_it",
        "messenger",
        "dontstarvetogether",
        "celeste_open_world",
        "tunic",
        "hades"
    ],
    "side-scrolling": [
        "dkc3",
        "phoa",
        "musedash",
        "hylics2",
        "blasphemous",
        "k64",
        "dkc",
        "cuphead",
        "mm3",
        "sm_map_rando",
        "mm2",
        "zelda2",
        "mzm",
        "dkc2",
        "yoshisisland",
        "metroidfusion",
        "kdl3",
        "rogue_legacy",
        "mmx3",
        "sotn",
        "sm"
    ],
    "great soundtrack": [
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "rabi_ribi",
        "blasphemous",
        "getting_over_it",
        "celeste_open_world",
        "tunic",
        "ultrakill",
        "undertale",
        "shorthike"
    ],
    "great": [
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "rabi_ribi",
        "blasphemous",
        "getting_over_it",
        "celeste_open_world",
        "tunic",
        "ultrakill",
        "undertale",
        "shorthike"
    ],
    "soundtrack": [
        "bomb_rush_cyberfunk",
        "celeste",
        "hylics2",
        "rabi_ribi",
        "blasphemous",
        "getting_over_it",
        "celeste_open_world",
        "tunic",
        "ultrakill",
        "undertale",
        "shorthike"
    ],
    "soulslike": [
        "dark_souls_3",
        "blasphemous",
        "dsr",
        "enderlilies",
        "tunic",
        "dark_souls_2"
    ],
    "you can pet the dog": [
        "seaofthieves",
        "blasphemous",
        "terraria",
        "hades",
        "undertale",
        "sims4",
        "overcooked2"
    ],
    "you": [
        "seaofthieves",
        "blasphemous",
        "terraria",
        "hades",
        "undertale",
        "sims4",
        "overcooked2"
    ],
    "can": [
        "seaofthieves",
        "blasphemous",
        "terraria",
        "hades",
        "undertale",
        "sims4",
        "overcooked2"
    ],
    "pet": [
        "seaofthieves",
        "blasphemous",
        "terraria",
        "hades",
        "undertale",
        "sims4",
        "overcooked2"
    ],
    "dog": [
        "seaofthieves",
        "doronko_wanko",
        "sly1",
        "soe",
        "oot",
        "blasphemous",
        "star_fox_64",
        "cv64",
        "overcooked2",
        "tloz_oos",
        "terraria",
        "hades",
        "undertale",
        "tmc",
        "sims4",
        "smo",
        "hcniko",
        "minecraft"
    ],
    "interconnected-world": [
        "hk",
        "dark_souls_3",
        "mzm",
        "blasphemous",
        "dsr",
        "sm_map_rando",
        "dark_souls_2",
        "sotn",
        "luigismansion",
        "sm"
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
    "sport": [
        "bomb_rush_cyberfunk",
        "trackmania"
    ],
    "science fiction": [
        "lego_star_wars_tcs",
        "soe",
        "outer_wilds",
        "sc2",
        "xenobladex",
        "doom_1993",
        "satisfactory",
        "zillion",
        "quake",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "v6",
        "ctjot",
        "star_fox_64",
        "factorio",
        "crosscode",
        "lethal_company",
        "ror1",
        "mm3",
        "ror2",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "mm2",
        "jakanddaxter",
        "earthbound",
        "witness",
        "tyrian",
        "brotato",
        "mzm",
        "rimworld",
        "rac2",
        "metroidfusion",
        "subnautica",
        "swr",
        "factorio_saws",
        "terraria",
        "mmx3",
        "nine_sols",
        "ultrakill",
        "sm",
        "pokemon_frlg"
    ],
    "science": [
        "lego_star_wars_tcs",
        "soe",
        "outer_wilds",
        "sc2",
        "xenobladex",
        "doom_1993",
        "satisfactory",
        "zillion",
        "quake",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "v6",
        "ctjot",
        "star_fox_64",
        "factorio",
        "crosscode",
        "lethal_company",
        "ror1",
        "mm3",
        "ror2",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "mm2",
        "jakanddaxter",
        "earthbound",
        "witness",
        "tyrian",
        "brotato",
        "mzm",
        "rimworld",
        "rac2",
        "metroidfusion",
        "subnautica",
        "swr",
        "factorio_saws",
        "terraria",
        "mmx3",
        "nine_sols",
        "ultrakill",
        "sm",
        "pokemon_frlg"
    ],
    "fiction": [
        "lego_star_wars_tcs",
        "soe",
        "outer_wilds",
        "sc2",
        "xenobladex",
        "doom_1993",
        "satisfactory",
        "zillion",
        "quake",
        "mmbn3",
        "bomb_rush_cyberfunk",
        "v6",
        "ctjot",
        "star_fox_64",
        "factorio",
        "crosscode",
        "lethal_company",
        "ror1",
        "mm3",
        "ror2",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "mm2",
        "jakanddaxter",
        "earthbound",
        "witness",
        "tyrian",
        "brotato",
        "mzm",
        "rimworld",
        "rac2",
        "metroidfusion",
        "subnautica",
        "swr",
        "factorio_saws",
        "terraria",
        "mmx3",
        "nine_sols",
        "ultrakill",
        "sm",
        "pokemon_frlg"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "ufo50",
        "residentevil3remake",
        "doom_1993",
        "quake",
        "heretic",
        "star_fox_64",
        "tboir",
        "crosscode",
        "cuphead",
        "cccharles",
        "ror1",
        "ror2",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "frogmonster",
        "residentevil2remake",
        "noita",
        "tyrian",
        "brotato",
        "mzm",
        "rac2",
        "hitman_woa",
        "metroidfusion",
        "mmx3",
        "ultrakill",
        "sm"
    ],
    "arcade": [
        "megamix",
        "mario_kart_double_dash",
        "noita",
        "osu",
        "mk64",
        "rabi_ribi",
        "brotato",
        "tyrian",
        "ufo50",
        "v6",
        "mm3",
        "messenger",
        "trackmania",
        "smw",
        "ultrakill",
        "overcooked2",
        "cuphead"
    ],
    "bumper stickers": [
        "bumpstik"
    ],
    "bumper stickers archipelago edition": [
        "bumpstik"
    ],
    "bumper": [
        "bumpstik"
    ],
    "stickers": [
        "bumpstik"
    ],
    "edition": [
        "minecraft",
        "bumpstik"
    ],
    "candy box 2": [
        "candybox2"
    ],
    "candy": [
        "candybox2"
    ],
    "box": [
        "candybox2"
    ],
    "text": [
        "candybox2",
        "yugioh06",
        "osrs"
    ],
    "web browser": [
        "candybox2",
        "ttyd"
    ],
    "web": [
        "candybox2",
        "ttyd"
    ],
    "browser": [
        "candybox2",
        "ttyd"
    ],
    "cat quest": [
        "cat_quest"
    ],
    "cat": [
        "wl4",
        "kh1",
        "cat_quest",
        "dkc2",
        "tmc",
        "tloz_oos",
        "minecraft",
        "cuphead"
    ],
    "quest": [
        "dkc2",
        "ffmq",
        "dlcquest",
        "cat_quest"
    ],
    "choo-choo charles": [
        "cccharles"
    ],
    "choo-choo": [
        "cccharles"
    ],
    "charles": [
        "cccharles"
    ],
    "forest": [
        "oribf",
        "cccharles",
        "enderlilies",
        "tunic",
        "shorthike",
        "hcniko"
    ],
    "celeste": [
        "celeste",
        "celeste_open_world",
        "celeste64"
    ],
    "google stadia": [
        "celeste",
        "ror2",
        "celeste_open_world",
        "terraria"
    ],
    "google": [
        "celeste",
        "ror2",
        "celeste_open_world",
        "terraria"
    ],
    "stadia": [
        "celeste",
        "ror2",
        "celeste_open_world",
        "terraria"
    ],
    "story rich": [
        "celeste",
        "powerwashsimulator",
        "hylics2",
        "dredge",
        "getting_over_it",
        "celeste_open_world",
        "hades",
        "undertale"
    ],
    "rich": [
        "celeste",
        "powerwashsimulator",
        "hylics2",
        "dredge",
        "getting_over_it",
        "celeste_open_world",
        "hades",
        "undertale"
    ],
    "conversation": [
        "celeste",
        "rabi_ribi",
        "v6",
        "enderlilies",
        "celeste_open_world",
        "undertale"
    ],
    "celeste 64": [
        "celeste64"
    ],
    "celeste 64: fragments of the mountain": [
        "celeste64"
    ],
    "64:": [
        "k64",
        "celeste64"
    ],
    "fragments": [
        "celeste64"
    ],
    "mountain": [
        "celeste64"
    ],
    "celeste (open world)": [
        "celeste_open_world"
    ],
    "chained echoes": [
        "chainedechoes"
    ],
    "chained": [
        "chainedechoes"
    ],
    "echoes": [
        "chainedechoes"
    ],
    "jrpg": [
        "hylics2",
        "chainedechoes",
        "ff4fe",
        "crystal_project",
        "ffta",
        "ffmq",
        "ff1",
        "pmd_eos"
    ],
    "chatipelago": [
        "chatipelago"
    ],
    "checksfinder": [
        "checksfinder"
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
        "openrct2",
        "civ_6"
    ],
    "4x": [
        "openrct2",
        "civ_6"
    ],
    "(explore,": [
        "openrct2",
        "civ_6"
    ],
    "expand,": [
        "openrct2",
        "civ_6"
    ],
    "exploit,": [
        "openrct2",
        "civ_6"
    ],
    "exterminate)": [
        "openrct2",
        "civ_6"
    ],
    "loot gathering": [
        "dk64",
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "minecraft"
    ],
    "loot": [
        "dk64",
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "minecraft"
    ],
    "gathering": [
        "dk64",
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "minecraft"
    ],
    "ambient music": [
        "dkc3",
        "soe",
        "mzm",
        "dkc2",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "civ_6",
        "dkc"
    ],
    "ambient": [
        "dkc3",
        "soe",
        "mzm",
        "dkc2",
        "metroidfusion",
        "cv64",
        "metroidprime",
        "civ_6",
        "dkc"
    ],
    "music": [
        "dkc3",
        "soe",
        "cv64",
        "musedash",
        "osu",
        "gstla",
        "civ_6",
        "ffta",
        "dkc",
        "placidplasticducksim",
        "metroidprime",
        "doom_ii",
        "sonic_heroes",
        "megamix",
        "mzm",
        "dkc2",
        "metroidfusion",
        "ultrakill",
        "ffmq",
        "sotn"
    ],
    "clique": [
        "clique"
    ],
    "crosscode": [
        "crosscode"
    ],
    "crystal project": [
        "crystal_project"
    ],
    "crystal": [
        "crystal_project",
        "k64",
        "pokemon_crystal"
    ],
    "project": [
        "megamix",
        "crystal_project"
    ],
    "tactical": [
        "hitman_woa",
        "crystal_project",
        "wargroove",
        "ffta",
        "overcooked2",
        "mmbn3"
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
        "ctjot",
        "pmd_eos"
    ],
    "ds": [
        "tloz_ph",
        "ctjot",
        "pmd_eos"
    ],
    "cuphead": [
        "cuphead"
    ],
    "pirates": [
        "seaofthieves",
        "kh1",
        "mzm",
        "dkc2",
        "metroidfusion",
        "tloz_ph",
        "metroidprime",
        "tloz_ooa",
        "wargroove2",
        "tloz_oos",
        "cuphead"
    ],
    "violent plants": [
        "ss",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "terraria",
        "sms",
        "cuphead"
    ],
    "violent": [
        "ss",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "terraria",
        "sms",
        "cuphead"
    ],
    "plants": [
        "ss",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "terraria",
        "sms",
        "cuphead"
    ],
    "auto-scrolling levels": [
        "v6",
        "dkc3",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc",
        "cuphead"
    ],
    "auto-scrolling": [
        "v6",
        "dkc3",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc",
        "cuphead"
    ],
    "levels": [
        "v6",
        "dkc3",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc",
        "cuphead"
    ],
    "boss assistance": [
        "dkc2",
        "oot",
        "metroidprime",
        "papermario",
        "doom_ii",
        "dark_souls_2",
        "mm_recomp",
        "rogue_legacy",
        "dkc",
        "tloz_ph",
        "sms",
        "tmc",
        "cuphead"
    ],
    "assistance": [
        "dkc2",
        "oot",
        "metroidprime",
        "papermario",
        "doom_ii",
        "dark_souls_2",
        "mm_recomp",
        "rogue_legacy",
        "dkc",
        "tloz_ph",
        "sms",
        "tmc",
        "cuphead"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "horse": [
        "cvcotm",
        "oot",
        "cv64",
        "rogue_legacy",
        "sotn",
        "minecraft"
    ],
    "multiple protagonists": [
        "lego_star_wars_tcs",
        "dkc3",
        "dkc2",
        "dk64",
        "mlss",
        "cv64",
        "spyro3",
        "rogue_legacy",
        "mmx3",
        "sotn",
        "dkc",
        "earthbound",
        "sonic_heroes"
    ],
    "protagonists": [
        "lego_star_wars_tcs",
        "dkc3",
        "dkc2",
        "dk64",
        "mlss",
        "cv64",
        "spyro3",
        "rogue_legacy",
        "mmx3",
        "sotn",
        "dkc",
        "earthbound",
        "sonic_heroes"
    ],
    "traps": [
        "metroidfusion",
        "cv64",
        "rogue_legacy",
        "doom_ii",
        "dark_souls_2",
        "tmc",
        "minecraft"
    ],
    "bats": [
        "zelda2",
        "cvcotm",
        "mk64",
        "pokemon_crystal",
        "cv64",
        "terraria",
        "sotn"
    ],
    "day/night cycle": [
        "stardew_valley",
        "ss",
        "dk64",
        "oot",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "tww",
        "terraria",
        "mm_recomp",
        "sotn",
        "jakanddaxter",
        "minecraft"
    ],
    "day/night": [
        "stardew_valley",
        "ss",
        "dk64",
        "oot",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "tww",
        "terraria",
        "mm_recomp",
        "sotn",
        "jakanddaxter",
        "minecraft"
    ],
    "cycle": [
        "stardew_valley",
        "ss",
        "dk64",
        "oot",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "tww",
        "terraria",
        "mm_recomp",
        "sotn",
        "jakanddaxter",
        "minecraft"
    ],
    "skeletons": [
        "seaofthieves",
        "cvcotm",
        "sly1",
        "heretic",
        "cv64",
        "terraria",
        "undertale",
        "sotn",
        "minecraft"
    ],
    "unstable platforms": [
        "v6",
        "cvcotm",
        "zelda2",
        "oribf",
        "sly1",
        "cv64",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "sms",
        "dkc",
        "sm",
        "tmc"
    ],
    "unstable": [
        "v6",
        "cvcotm",
        "zelda2",
        "oribf",
        "sly1",
        "cv64",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "sms",
        "dkc",
        "sm",
        "tmc"
    ],
    "melee": [
        "lego_star_wars_tcs",
        "doom_1993",
        "cv64",
        "tunic",
        "quake",
        "heretic",
        "wl4",
        "sly1",
        "k64",
        "gstla",
        "ffta",
        "kh1",
        "doom_ii",
        "dark_souls_2",
        "tmc",
        "cvcotm",
        "pokemon_crystal",
        "metroidfusion",
        "kdl3",
        "papermario",
        "terraria",
        "sotn",
        "pokemon_emerald"
    ],
    "instant kill": [
        "v6",
        "dkc2",
        "metroidfusion",
        "cv64",
        "dkc",
        "mm2"
    ],
    "instant": [
        "v6",
        "dkc2",
        "metroidfusion",
        "cv64",
        "dkc",
        "mm2"
    ],
    "kill": [
        "v6",
        "dkc2",
        "metroidfusion",
        "cv64",
        "dkc",
        "mm2"
    ],
    "difficulty level": [
        "osu",
        "mk64",
        "mzm",
        "star_fox_64",
        "cv64",
        "musedash",
        "metroidprime",
        "doom_ii",
        "mm2",
        "minecraft"
    ],
    "difficulty": [
        "osu",
        "mk64",
        "mzm",
        "star_fox_64",
        "cv64",
        "musedash",
        "metroidprime",
        "doom_ii",
        "mm2",
        "minecraft"
    ],
    "level": [
        "osu",
        "mk64",
        "kh1",
        "mzm",
        "dkc2",
        "oot",
        "star_fox_64",
        "cv64",
        "musedash",
        "metroidprime",
        "doom_ii",
        "sms",
        "dkc",
        "mm2",
        "minecraft"
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
        "wl4",
        "mzm",
        "yugiohddm",
        "metroidfusion",
        "mlss",
        "gstla",
        "pokemon_frlg",
        "ffta",
        "tmc",
        "mmbn3",
        "pokemon_emerald",
        "yugioh06",
        "earthbound"
    ],
    "boy": [
        "tloz_oos",
        "mmbn3",
        "wl4",
        "gstla",
        "ffta",
        "pokemon_rb",
        "marioland2",
        "yugiohddm",
        "tloz_ooa",
        "mm2",
        "yugioh06",
        "tmc",
        "earthbound",
        "ladx",
        "cvcotm",
        "mzm",
        "pokemon_crystal",
        "metroidfusion",
        "mlss",
        "wl",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "advance": [
        "cvcotm",
        "wl4",
        "mzm",
        "yugiohddm",
        "metroidfusion",
        "mlss",
        "gstla",
        "pokemon_frlg",
        "ffta",
        "tmc",
        "mmbn3",
        "pokemon_emerald",
        "yugioh06",
        "earthbound"
    ],
    "gravity": [
        "lego_star_wars_tcs",
        "cvcotm",
        "dkc3",
        "v6",
        "mzm",
        "dkc2",
        "dk64",
        "oot",
        "metroidfusion",
        "star_fox_64",
        "metroidprime",
        "papermario",
        "sotn",
        "dkc"
    ],
    "leveling up": [
        "zelda2",
        "cvcotm",
        "kh1",
        "pokemon_crystal",
        "landstalker",
        "papermario",
        "gstla",
        "dark_souls_2",
        "poe",
        "undertale",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "earthbound"
    ],
    "leveling": [
        "zelda2",
        "cvcotm",
        "kh1",
        "pokemon_crystal",
        "landstalker",
        "papermario",
        "gstla",
        "dark_souls_2",
        "poe",
        "undertale",
        "sotn",
        "dw1",
        "pokemon_emerald",
        "earthbound"
    ],
    "dark souls ii": [
        "dark_souls_2"
    ],
    "dark": [
        "dsr",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "souls": [
        "dark_souls_2",
        "dark_souls_3"
    ],
    "ii": [
        "ff4fe",
        "kh2",
        "dark_souls_2",
        "spire",
        "mm2"
    ],
    "xbox 360": [
        "lego_star_wars_tcs",
        "dlcquest",
        "terraria",
        "dark_souls_2",
        "sadx",
        "sotn",
        "sa2b"
    ],
    "360": [
        "lego_star_wars_tcs",
        "dlcquest",
        "terraria",
        "dark_souls_2",
        "sadx",
        "sotn",
        "sa2b"
    ],
    "spider": [
        "zelda2",
        "sly1",
        "oribf",
        "dkc2",
        "dark_souls_2",
        "minecraft"
    ],
    "customizable characters": [
        "lego_star_wars_tcs",
        "stardew_valley",
        "dark_souls_3",
        "xenobladex",
        "terraria",
        "dark_souls_2"
    ],
    "customizable": [
        "lego_star_wars_tcs",
        "stardew_valley",
        "dark_souls_3",
        "xenobladex",
        "terraria",
        "dark_souls_2"
    ],
    "checkpoints": [
        "v6",
        "dkc3",
        "sly1",
        "dkc2",
        "mm3",
        "mmx3",
        "dark_souls_2",
        "dkc",
        "mm2",
        "jakanddaxter",
        "smo",
        "sonic_heroes"
    ],
    "fire manipulation": [
        "pokemon_crystal",
        "papermario",
        "gstla",
        "dark_souls_2",
        "rogue_legacy",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "fire": [
        "pokemon_crystal",
        "papermario",
        "gstla",
        "dark_souls_2",
        "rogue_legacy",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "manipulation": [
        "pokemon_crystal",
        "papermario",
        "gstla",
        "dark_souls_2",
        "rogue_legacy",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "dark souls iii": [
        "dark_souls_3"
    ],
    "iii": [
        "zillion",
        "dark_souls_3"
    ],
    "diddy kong racing": [
        "diddy_kong_racing"
    ],
    "diddy": [
        "diddy_kong_racing"
    ],
    "kong": [
        "dkc3",
        "dkc2",
        "dk64",
        "diddy_kong_racing",
        "dkc"
    ],
    "racing": [
        "mario_kart_double_dash",
        "mk64",
        "simpsonshitnrun",
        "swr",
        "trackmania",
        "diddy_kong_racing",
        "jakanddaxter"
    ],
    "behind the waterfall": [
        "dkc3",
        "ss",
        "tmc",
        "gstla",
        "sotn",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "smo"
    ],
    "behind": [
        "dkc3",
        "ss",
        "tmc",
        "gstla",
        "sotn",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "smo"
    ],
    "waterfall": [
        "dkc3",
        "ss",
        "tmc",
        "gstla",
        "sotn",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "smo"
    ],
    "donkey kong 64": [
        "dk64"
    ],
    "donkey": [
        "dkc2",
        "dk64",
        "dkc3",
        "dkc"
    ],
    "artificial intelligence": [
        "mk64",
        "sly1",
        "dk64",
        "star_fox_64",
        "metroidprime",
        "doom_ii",
        "jakanddaxter"
    ],
    "artificial": [
        "mk64",
        "sly1",
        "dk64",
        "star_fox_64",
        "metroidprime",
        "doom_ii",
        "jakanddaxter"
    ],
    "intelligence": [
        "mk64",
        "sly1",
        "dk64",
        "star_fox_64",
        "metroidprime",
        "doom_ii",
        "jakanddaxter"
    ],
    "completion percentage": [
        "mzm",
        "dkc2",
        "dk64",
        "metroidfusion",
        "metroidprime",
        "sotn"
    ],
    "completion": [
        "mzm",
        "dkc2",
        "dk64",
        "metroidfusion",
        "metroidprime",
        "sotn"
    ],
    "percentage": [
        "mzm",
        "dkc2",
        "dk64",
        "metroidfusion",
        "metroidprime",
        "sotn"
    ],
    "invisibility": [
        "sly1",
        "dk64",
        "doom_1993",
        "papermario",
        "doom_ii",
        "quake"
    ],
    "foreshadowing": [
        "mzm",
        "dk64",
        "metroidfusion",
        "metroidprime",
        "sms",
        "tmc"
    ],
    "donkey kong country": [
        "dkc"
    ],
    "country": [
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "overworld": [
        "zelda2",
        "dkc3",
        "dkc2",
        "gstla",
        "ffmq",
        "ffta",
        "dkc",
        "tloz"
    ],
    "bonus stage": [
        "dkc3",
        "dkc2",
        "spyro3",
        "smw",
        "dkc",
        "sonic_heroes"
    ],
    "bonus": [
        "dkc3",
        "dkc2",
        "spyro3",
        "smw",
        "dkc",
        "sonic_heroes"
    ],
    "water level": [
        "kh1",
        "dkc2",
        "oot",
        "sms",
        "dkc",
        "mm2"
    ],
    "water": [
        "kh1",
        "dkc2",
        "oot",
        "sms",
        "dkc",
        "mm2"
    ],
    "speedrun": [
        "sm64ex",
        "metroidfusion",
        "metroidprime",
        "sotn",
        "dkc",
        "quake",
        "sm64hacks"
    ],
    "donkey kong country 2": [
        "dkc2"
    ],
    "donkey kong country 2: diddy's kong quest": [
        "dkc2"
    ],
    "2:": [
        "dkc2",
        "yoshisisland",
        "sa2b",
        "marioland2"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "sly1",
        "dkc2",
        "tloz_oos",
        "terraria",
        "tloz_ooa",
        "sms",
        "shorthike",
        "jakanddaxter",
        "tmc"
    ],
    "game reference": [
        "dkc2",
        "oot",
        "spyro3",
        "rogue_legacy",
        "doom_ii",
        "witness",
        "hcniko",
        "tmc"
    ],
    "reference": [
        "simpsonshitnrun",
        "dkc2",
        "oot",
        "placidplasticducksim",
        "spyro3",
        "rogue_legacy",
        "doom_ii",
        "witness",
        "hcniko",
        "tmc"
    ],
    "sprinting mechanics": [
        "wl4",
        "soe",
        "sm64ex",
        "dkc2",
        "oot",
        "pokemon_crystal",
        "mm_recomp",
        "sms",
        "pokemon_emerald",
        "sm64hacks"
    ],
    "sprinting": [
        "wl4",
        "soe",
        "sm64ex",
        "dkc2",
        "oot",
        "pokemon_crystal",
        "mm_recomp",
        "sms",
        "pokemon_emerald",
        "sm64hacks"
    ],
    "mechanics": [
        "wl4",
        "soe",
        "sm64ex",
        "dkc2",
        "oot",
        "pokemon_crystal",
        "mm_recomp",
        "sms",
        "pokemon_emerald",
        "sm64hacks"
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
        "mario_kart_double_dash",
        "dkc3"
    ],
    "trouble!": [
        "dkc3"
    ],
    "dlcquest": [
        "dlcquest"
    ],
    "dlc quest": [
        "dlcquest"
    ],
    "dlc": [
        "dlcquest"
    ],
    "deliberately retro": [
        "v6",
        "ufo50",
        "stardew_valley",
        "dlcquest",
        "minecraft",
        "terraria",
        "timespinner",
        "smo"
    ],
    "deliberately": [
        "v6",
        "ufo50",
        "stardew_valley",
        "dlcquest",
        "minecraft",
        "terraria",
        "timespinner",
        "smo"
    ],
    "punctuation mark above head": [
        "simpsonshitnrun",
        "dlcquest",
        "pokemon_crystal",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald",
        "tmc"
    ],
    "punctuation": [
        "simpsonshitnrun",
        "dlcquest",
        "pokemon_crystal",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald",
        "tmc"
    ],
    "mark": [
        "simpsonshitnrun",
        "dlcquest",
        "pokemon_crystal",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald",
        "tmc"
    ],
    "above": [
        "simpsonshitnrun",
        "dlcquest",
        "pokemon_crystal",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald",
        "tmc"
    ],
    "head": [
        "simpsonshitnrun",
        "dlcquest",
        "pokemon_crystal",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald",
        "tmc"
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
        "raft",
        "dontstarvetogether",
        "factorio_saws",
        "satisfactory",
        "terraria",
        "factorio",
        "minecraft"
    ],
    "funny": [
        "powerwashsimulator",
        "sims4",
        "getting_over_it",
        "dontstarvetogether",
        "undertale",
        "shorthike"
    ],
    "doom 1993": [
        "doom_1993"
    ],
    "doom": [
        "doom_ii",
        "doom_1993"
    ],
    "windows mobile": [
        "doom_1993"
    ],
    "windows": [
        "terraria",
        "doom_1993"
    ],
    "mobile": [
        "mmx3",
        "quake",
        "doom_1993"
    ],
    "pc-9800 series": [
        "doom_ii",
        "doom_1993"
    ],
    "pc-9800": [
        "doom_ii",
        "doom_1993"
    ],
    "dos": [
        "tyrian",
        "doom_1993",
        "doom_ii",
        "quake",
        "heretic"
    ],
    "doom ii": [
        "doom_ii"
    ],
    "doom ii: hell on earth": [
        "doom_ii"
    ],
    "ii:": [
        "zelda2",
        "sc2",
        "doom_ii",
        "lufia2ac"
    ],
    "hell": [
        "doom_ii"
    ],
    "on": [
        "doom_ii"
    ],
    "earth": [
        "doom_ii"
    ],
    "tapwave zodiac": [
        "doom_ii"
    ],
    "tapwave": [
        "doom_ii"
    ],
    "zodiac": [
        "doom_ii"
    ],
    "pop culture reference": [
        "simpsonshitnrun",
        "placidplasticducksim",
        "rogue_legacy",
        "doom_ii",
        "witness",
        "tmc"
    ],
    "pop": [
        "simpsonshitnrun",
        "placidplasticducksim",
        "rogue_legacy",
        "doom_ii",
        "witness",
        "tmc"
    ],
    "culture": [
        "simpsonshitnrun",
        "placidplasticducksim",
        "rogue_legacy",
        "doom_ii",
        "witness",
        "tmc"
    ],
    "stat tracking": [
        "osu",
        "simpsonshitnrun",
        "kh1",
        "rogue_legacy",
        "doom_ii",
        "ffta",
        "witness"
    ],
    "stat": [
        "osu",
        "simpsonshitnrun",
        "kh1",
        "rogue_legacy",
        "doom_ii",
        "ffta",
        "witness"
    ],
    "tracking": [
        "osu",
        "simpsonshitnrun",
        "kh1",
        "rogue_legacy",
        "doom_ii",
        "ffta",
        "witness"
    ],
    "rock music": [
        "gstla",
        "doom_ii",
        "ffmq",
        "ffta",
        "ultrakill",
        "sotn",
        "sonic_heroes"
    ],
    "rock": [
        "gstla",
        "doom_ii",
        "ffmq",
        "ffta",
        "ultrakill",
        "sotn",
        "sonic_heroes"
    ],
    "sequence breaking": [
        "wl4",
        "mzm",
        "oot",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "tloz_ooa",
        "sotn",
        "sm",
        "tmc"
    ],
    "sequence": [
        "wl4",
        "mzm",
        "oot",
        "metroidprime",
        "sm_map_rando",
        "doom_ii",
        "tloz_ooa",
        "sotn",
        "sm",
        "tmc"
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
        "phoa",
        "dredge",
        "stardew_valley",
        "terraria",
        "shorthike",
        "hcniko",
        "minecraft"
    ],
    "stylized": [
        "hylics2",
        "dredge",
        "tunic",
        "ultrakill",
        "hades",
        "shorthike",
        "hcniko"
    ],
    "dark souls remastered": [
        "dsr"
    ],
    "dark souls: remastered": [
        "dsr"
    ],
    "souls:": [
        "dsr"
    ],
    "remastered": [
        "dsr"
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
    "earthbound": [
        "earthbound"
    ],
    "party system": [
        "kh1",
        "pokemon_crystal",
        "mlss",
        "xenobladex",
        "papermario",
        "gstla",
        "ffmq",
        "ffta",
        "pokemon_emerald",
        "earthbound"
    ],
    "party": [
        "mk64",
        "kh1",
        "pokemon_crystal",
        "mlss",
        "xenobladex",
        "placidplasticducksim",
        "papermario",
        "gstla",
        "ffmq",
        "ffta",
        "pokemon_emerald",
        "overcooked2",
        "earthbound"
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
    "factorio": [
        "factorio"
    ],
    "nintendo switch 2": [
        "factorio",
        "overcooked2",
        "smo",
        "stardew_valley"
    ],
    "factorio - space age without space": [
        "factorio_saws"
    ],
    "factorio: space age": [
        "factorio_saws"
    ],
    "factorio:": [
        "factorio_saws"
    ],
    "space": [
        "factorio_saws"
    ],
    "faxanadu": [
        "faxanadu"
    ],
    "family computer": [
        "mm3",
        "tloz",
        "faxanadu",
        "ff1"
    ],
    "family": [
        "zelda2",
        "mm3",
        "faxanadu",
        "ff1",
        "tloz"
    ],
    "computer": [
        "zelda2",
        "mm3",
        "faxanadu",
        "ff1",
        "tloz"
    ],
    "nintendo entertainment system": [
        "zelda2",
        "mm3",
        "faxanadu",
        "ff1",
        "tloz"
    ],
    "final fantasy": [
        "ff1"
    ],
    "final": [
        "ffmq",
        "ffta",
        "ff1",
        "ff4fe"
    ],
    "kids": [
        "lego_star_wars_tcs",
        "mario_kart_double_dash",
        "mk64",
        "yoshisisland",
        "pokemon_crystal",
        "placidplasticducksim",
        "pokemon_frlg",
        "ff1",
        "pokemon_emerald",
        "pokemon_rb",
        "tetrisattack",
        "overcooked2",
        "pmd_eos",
        "minecraft"
    ],
    "final fantasy iv free enterprise": [
        "ff4fe"
    ],
    "final fantasy ii": [
        "ff4fe"
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
        "sims4",
        "getting_over_it",
        "placidplasticducksim",
        "ffmq",
        "shorthike",
        "musedash"
    ],
    "final fantasy tactics advance": [
        "ffta"
    ],
    "tactics": [
        "ffta"
    ],
    "yu-gi-oh! forbidden memories": [
        "fm"
    ],
    "yu-gi-oh!": [
        "fm",
        "yugioh06",
        "yugiohddm"
    ],
    "forbidden": [
        "fm"
    ],
    "memories": [
        "fm"
    ],
    "frog monster": [
        "frogmonster"
    ],
    "frogmonster": [
        "frogmonster"
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
        "gstla",
        "marioland2"
    ],
    "sun:": [
        "gstla"
    ],
    "lost": [
        "gstla"
    ],
    "gzdoom": [
        "gzdoom"
    ],
    "gzdoom sm64": [
        "gzdoom"
    ],
    "sm64": [
        "gzdoom"
    ],
    "hades": [
        "hades"
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
    "heretic": [
        "heretic"
    ],
    "hitman world of assasination": [
        "hitman_woa"
    ],
    "hitman world of assassination": [
        "hitman_woa"
    ],
    "hitman": [
        "hitman_woa"
    ],
    "assassination": [
        "hitman_woa"
    ],
    "thriller": [
        "sm_map_rando",
        "hitman_woa",
        "sm",
        "oribf"
    ],
    "stealth": [
        "hitman_woa",
        "sly1"
    ],
    "playstation vr": [
        "hitman_woa"
    ],
    "vr": [
        "hitman_woa"
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
    "hylics 2": [
        "hylics2"
    ],
    "hylics": [
        "hylics2"
    ],
    "inscryption": [
        "inscryption"
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
        "mmx3",
        "jakanddaxter",
        "quake"
    ],
    "jigsaw": [
        "jigsaw"
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
        "wl",
        "wl4",
        "kdl3",
        "marioland2"
    ],
    "kingdom hearts": [
        "kh1"
    ],
    "kingdom": [
        "kh2",
        "kh1"
    ],
    "hearts": [
        "kh2",
        "kh1"
    ],
    "kingdom hearts 2": [
        "kh2"
    ],
    "kingdom hearts ii": [
        "kh2"
    ],
    "kindergarten 2": [
        "kindergarten_2"
    ],
    "kindergarten": [
        "kindergarten_2"
    ],
    "links awakening dx beta": [
        "ladx"
    ],
    "the legend of zelda: link's awakening dx": [
        "ladx"
    ],
    "link's": [
        "ladx"
    ],
    "awakening": [
        "ladx",
        "phoa"
    ],
    "dx": [
        "ladx",
        "sadx"
    ],
    "game boy color": [
        "ladx",
        "pokemon_crystal",
        "tloz_ooa",
        "tloz_oos"
    ],
    "color": [
        "ladx",
        "pokemon_crystal",
        "tloz_ooa",
        "tloz_oos"
    ],
    "tentacles": [
        "ladx",
        "pokemon_crystal",
        "mlss",
        "metroidprime",
        "papermario",
        "sms",
        "pokemon_emerald"
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
        "landstalker",
        "zillion",
        "quake"
    ],
    "mega": [
        "megamix",
        "mm3",
        "landstalker",
        "mmx3",
        "mm2",
        "mmbn3"
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
        "swr",
        "star_fox_64"
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
    "lethal company": [
        "lethal_company"
    ],
    "lethal": [
        "lethal_company"
    ],
    "company": [
        "lethal_company"
    ],
    "lingo": [
        "lingo"
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
    "lunacid": [
        "lunacid"
    ],
    "madou monogatari hanamaru daiyouchienji": [
        "madou"
    ],
    "madou monogatari: hanamaru daiyouchienji": [
        "madou"
    ],
    "madou": [
        "madou"
    ],
    "monogatari:": [
        "madou"
    ],
    "hanamaru": [
        "madou"
    ],
    "daiyouchienji": [
        "madou"
    ],
    "super mario land 2": [
        "marioland2"
    ],
    "super mario land 2: 6 golden coins": [
        "marioland2"
    ],
    "mario": [
        "mario_kart_double_dash",
        "mk64",
        "sm64ex",
        "marioland2",
        "yoshisisland",
        "mlss",
        "wl",
        "papermario",
        "smw",
        "sms",
        "smo",
        "sm64hacks"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "wl",
        "pokemon_rb",
        "mm2",
        "marioland2"
    ],
    "turtle": [
        "mk64",
        "sly1",
        "marioland2",
        "mlss",
        "papermario",
        "sms"
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
    "meritous": [
        "meritous"
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
        "metroidfusion",
        "metroidprime",
        "sm_map_rando",
        "smz3",
        "sm"
    ],
    "fusion": [
        "metroidfusion"
    ],
    "time limit": [
        "wl4",
        "simpsonshitnrun",
        "ror1",
        "metroidfusion",
        "tloz_ph",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "sms",
        "witness",
        "shorthike",
        "sm",
        "tmc"
    ],
    "limit": [
        "wl4",
        "simpsonshitnrun",
        "ror1",
        "metroidfusion",
        "tloz_ph",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "sms",
        "witness",
        "shorthike",
        "sm",
        "tmc"
    ],
    "countdown timer": [
        "wl4",
        "simpsonshitnrun",
        "mzm",
        "oot",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "tmc"
    ],
    "countdown": [
        "wl4",
        "simpsonshitnrun",
        "mzm",
        "oot",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "tmc"
    ],
    "timer": [
        "wl4",
        "simpsonshitnrun",
        "mzm",
        "oot",
        "metroidfusion",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "tmc"
    ],
    "isolation": [
        "mzm",
        "metroidfusion",
        "sm_map_rando",
        "metroidprime",
        "sotn",
        "sm"
    ],
    "metroid prime": [
        "metroidprime"
    ],
    "prime": [
        "metroidprime"
    ],
    "auto-aim": [
        "ss",
        "oot",
        "tww",
        "metroidprime",
        "mm_recomp",
        "quake"
    ],
    "meme origin": [
        "zelda2",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "tloz",
        "minecraft"
    ],
    "meme": [
        "zelda2",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "tloz",
        "minecraft"
    ],
    "origin": [
        "zelda2",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "tloz",
        "minecraft"
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
    "virtual reality": [
        "subnautica",
        "minecraft"
    ],
    "virtual": [
        "subnautica",
        "minecraft"
    ],
    "reality": [
        "subnautica",
        "minecraft"
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
        "mm3",
        "mm2",
        "mmx3",
        "mmbn3"
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
        "mmx3",
        "quake"
    ],
    "device": [
        "mmx3",
        "quake"
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
        "oot",
        "mm_recomp"
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
    "nine sols": [
        "nine_sols"
    ],
    "nine": [
        "nine_sols"
    ],
    "sols": [
        "nine_sols"
    ],
    "noita": [
        "noita"
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
    "openrct2": [
        "openrct2"
    ],
    "business": [
        "powerwashsimulator",
        "openrct2",
        "stardew_valley"
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
    "old school runescape": [
        "osrs"
    ],
    "old": [
        "osrs"
    ],
    "school": [
        "osrs"
    ],
    "runescape": [
        "osrs"
    ],
    "osu!": [
        "osu"
    ],
    "auditory": [
        "osu"
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
    "paint": [
        "paint"
    ],
    "paper mario": [
        "papermario"
    ],
    "paper": [
        "papermario",
        "ttyd"
    ],
    "peak": [
        "peak"
    ],
    "peaks of yore": [
        "peaks_of_yore"
    ],
    "peaks": [
        "peaks_of_yore"
    ],
    "yore": [
        "peaks_of_yore"
    ],
    "phoenotopia: awakening": [
        "phoa"
    ],
    "phoenotopia:": [
        "phoa"
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
    "pokemon mystery dungeon explorers of sky": [
        "pmd_eos"
    ],
    "pok\u00e9mon mystery dungeon: explorers of sky": [
        "pmd_eos"
    ],
    "pok\u00e9mon": [
        "pokemon_crystal",
        "pokemon_rb",
        "pokemon_emerald",
        "pmd_eos",
        "pokemon_frlg"
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
    "path of exile": [
        "poe"
    ],
    "path": [
        "poe"
    ],
    "exile": [
        "poe"
    ],
    "pokemon crystal": [
        "pokemon_crystal"
    ],
    "pok\u00e9mon crystal version": [
        "pokemon_crystal"
    ],
    "version": [
        "pokemon_rb",
        "pokemon_crystal",
        "pokemon_emerald",
        "pokemon_frlg"
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
    "pseudoregalia": [
        "pseudoregalia"
    ],
    "pseudoregalia: jam ver.": [
        "pseudoregalia"
    ],
    "pseudoregalia:": [
        "pseudoregalia"
    ],
    "jam": [
        "pseudoregalia"
    ],
    "ver.": [
        "pseudoregalia"
    ],
    "quake 1": [
        "quake"
    ],
    "quake": [
        "quake"
    ],
    "zeebo": [
        "quake"
    ],
    "amiga": [
        "quake"
    ],
    "sega saturn": [
        "quake"
    ],
    "saturn": [
        "quake"
    ],
    "rabi-ribi": [
        "rabi_ribi"
    ],
    "playstation vita": [
        "v6",
        "rabi_ribi",
        "stardew_valley",
        "ror1",
        "rogue_legacy",
        "terraria",
        "undertale",
        "timespinner"
    ],
    "vita": [
        "v6",
        "rabi_ribi",
        "stardew_valley",
        "ror1",
        "rogue_legacy",
        "terraria",
        "undertale",
        "timespinner"
    ],
    "rabbit": [
        "rabi_ribi",
        "sm64ex",
        "sm64hacks",
        "terraria",
        "tloz_ooa",
        "smo",
        "sonic_heroes"
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
    "resident evil 2 remake": [
        "residentevil2remake"
    ],
    "resident evil 2": [
        "residentevil2remake"
    ],
    "resident": [
        "residentevil3remake",
        "residentevil2remake"
    ],
    "evil": [
        "residentevil3remake",
        "residentevil2remake"
    ],
    "resident evil 3 remake": [
        "residentevil3remake"
    ],
    "resident evil 3": [
        "residentevil3remake"
    ],
    "rimworld": [
        "rimworld"
    ],
    "rogue legacy": [
        "rogue_legacy"
    ],
    "rogue": [
        "rogue_legacy"
    ],
    "risk of rain": [
        "ror1"
    ],
    "risk": [
        "ror2",
        "ror1"
    ],
    "rain": [
        "ror2",
        "ror1"
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
    "saving princess": [
        "saving_princess"
    ],
    "starcraft 2": [
        "sc2"
    ],
    "starcraft ii: wings of liberty": [
        "sc2"
    ],
    "starcraft": [
        "sc2"
    ],
    "wings": [
        "sc2"
    ],
    "liberty": [
        "sc2"
    ],
    "warfare": [
        "wargroove2",
        "sc2",
        "wargroove"
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
    "shapez": [
        "shapez"
    ],
    "shivers": [
        "shivers"
    ],
    "point-and-click": [
        "shivers",
        "zork_grand_inquisitor"
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
    "the simpsons hit and run": [
        "simpsonshitnrun"
    ],
    "the simpsons: hit & run": [
        "simpsonshitnrun"
    ],
    "simpsons:": [
        "simpsonshitnrun"
    ],
    "hit": [
        "simpsonshitnrun"
    ],
    "run": [
        "simpsonshitnrun"
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
    "super metroid": [
        "sm_map_rando",
        "sm"
    ],
    "super mario 64": [
        "sm64ex",
        "sm64hacks"
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
    "smz3": [
        "smz3"
    ],
    "super metroid and a link to the past crossover randomizer": [
        "smz3"
    ],
    "crossover": [
        "smz3"
    ],
    "randomizer": [
        "smz3"
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
    "slay the spire": [
        "spire"
    ],
    "slay the spire ii": [
        "spire"
    ],
    "slay": [
        "spire"
    ],
    "spire": [
        "spire"
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
    "the binding of isaac repentance": [
        "tboir"
    ],
    "the binding of isaac: repentance": [
        "tboir"
    ],
    "binding": [
        "tboir"
    ],
    "isaac:": [
        "tboir"
    ],
    "repentance": [
        "tboir"
    ],
    "terraria": [
        "terraria"
    ],
    "windows phone": [
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
        "zelda2",
        "tloz"
    ],
    "family computer disk system": [
        "zelda2",
        "tloz"
    ],
    "disk": [
        "zelda2",
        "tloz"
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
    "paper mario the thousand year door": [
        "ttyd"
    ],
    "paper mario: the thousand-year door": [
        "ttyd"
    ],
    "mario:": [
        "ttyd"
    ],
    "thousand-year": [
        "ttyd"
    ],
    "door": [
        "ttyd"
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
    "ufo 50": [
        "ufo50"
    ],
    "ufo": [
        "ufo50"
    ],
    "50": [
        "ufo50"
    ],
    "ultrakill": [
        "ultrakill"
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
    "wordipelago": [
        "wordipelago"
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
    "yacht dice": [
        "yachtdice"
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
    ],
    "zillion": [
        "zillion"
    ],
    "sega master system/mark iii": [
        "zillion"
    ],
    "master": [
        "zillion"
    ],
    "system/mark": [
        "zillion"
    ],
    "zork grand inquisitor": [
        "zork_grand_inquisitor"
    ],
    "zork: grand inquisitor": [
        "zork_grand_inquisitor"
    ],
    "zork:": [
        "zork_grand_inquisitor"
    ],
    "grand": [
        "zork_grand_inquisitor"
    ],
    "inquisitor": [
        "zork_grand_inquisitor"
    ],
    "debug": [
        "_debug"
    ],
    "manual": [
        "_manual"
    ],
    "universal tracker": [
        "_tracker"
    ]
}  # type: ignore  # noqa: F821