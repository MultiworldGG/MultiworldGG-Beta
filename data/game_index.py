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
    def get_module_for_game(game_name: str) -> str:
        """Get the module name for a given game name"""
        for module, game_data in GAMES_DATA.items():
            if game_data['game_name'] == game_name:
                return module
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
    "adventure": {
        "igdb_id": "12239",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/qzcqrjruhpuge5egkzgj.jpg",
        "game_name": "Adventure",
        "igdb_name": "adventure",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "adventure"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "bbc microcomputer system",
            "acorn electron"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "1983"
    },
    "against_the_storm": {
        "igdb_id": "147519",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7j13.jpg",
        "game_name": "Against the Storm",
        "igdb_name": "against the storm",
        "rating": [
            "mild blood",
            "alcohol reference",
            "use of tobacco",
            "language",
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "real time strategy (rts)",
            "simulator",
            "strategy",
            "indie"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5",
            "nintendo switch"
        ],
        "storyline": "the rain is your ally and the greatest enemy. it cycles in three seasons requiring you to stay flexible and adapt to changing conditions. in drizzle, the season of regrowth, natural resources replenish themselves, and it\u2019s time for construction and planting crops. the clearance is the season of harvest, expansion, and preparations for the last, most unforgiving season of them all. a true test of your city\u2019s strength comes with the storm when bolts of lightning tear the sky, nothing grows and resources are scarce.",
        "keywords": [
            "base building",
            "roguelite"
        ],
        "release_date": "2023"
    },
    "ahit": {
        "igdb_id": "6705",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pl5.jpg",
        "game_name": "A Hat in Time",
        "igdb_name": "a hat in time",
        "rating": [
            "blood",
            "fantasy violence"
        ],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
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
            "steam greenlight",
            "crowdfunding",
            "crowd funded",
            "collection marathon"
        ],
        "release_date": "2017"
    },
    "albw": {
        "igdb_id": "2909",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3p0j.jpg",
        "game_name": "A Link Between Worlds",
        "igdb_name": "the legend of zelda: a link between worlds",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "historical",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "nintendo 3ds"
        ],
        "storyline": "after capturing princess zelda and escaping through a rift into the parallel world of lorule, the evil sorcerer yuga plan to use the power of the seven mages to resurrect the demon king ganon. the young adventurer link is called out to restore peace to the kingdom of hyrule and is granted the ability to merge into walls after obtaining a magic bracelet from the eccentric merchant ravio, which allows him to reach previously inaccessible areas and travel between the worlds of hyrule and lorule.",
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
            "stereoscopic 3d",
            "side quests",
            "potion",
            "real-time combat",
            "self-referential humor",
            "multiple gameplay perspectives",
            "rpg elements",
            "mercenary",
            "coming of age",
            "dimension travel",
            "androgyny",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "bees"
        ],
        "release_date": "2013"
    },
    "alttp": {
        "igdb_id": "1026",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3vzn.jpg",
        "game_name": "A Link to the Past",
        "igdb_name": "the legend of zelda: a link to the past",
        "rating": [
            "mild violence",
            "mild animated violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "satellaview",
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "the wizard agahnim has been abducting descendants of the seven sages, intent on using their power to obliterate the barrier leading to the dark world. one of the descendants happens to be princess zelda, who informs link of her plight. armed with a trusty sword and shield, link begins a journey that will take him through treacherous territory.",
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
            "portals",
            "pixel art",
            "easter egg",
            "teleportation",
            "sequel",
            "giant insects",
            "silent protagonist",
            "swimming",
            "darkness",
            "explosion",
            "block puzzle",
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
            "liberation",
            "mercenary",
            "coming of age",
            "conveyor belt",
            "villain",
            "recurring boss",
            "been here before",
            "sleeping",
            "merchants",
            "multiple enemy boss fights",
            "dimension travel",
            "fetch quests",
            "kidnapping",
            "poisoning",
            "time paradox",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "falling object",
            "status effects",
            "hidden room",
            "another world",
            "plane shifting",
            "damage over time",
            "monomyth",
            "buddy system",
            "retroachievements",
            "bees"
        ],
        "release_date": "1991"
    },
    "animal_well": {
        "igdb_id": "191435",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4hdh.jpg",
        "game_name": "ANIMAL WELL",
        "igdb_name": "animal well",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "horror",
            "survival",
            "mystery"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5",
            "nintendo switch"
        ],
        "storyline": "it is dark. it is lonely. you don't belong in this world. it's not that it\u2019s a hostile world... it's just... not yours. as you uncover its secrets, the world grows on you. it takes on a feel of familiarity, yet you know that you've only probed the surface. the more you discover, the more you realize how much more there is to discover. secrets leading to more secrets. you recall the feeling of zooming closer and closer in on a very high-resolution photo. as you hone your focus, the world betrays its secrets.",
        "keywords": [
            "exploration",
            "retro",
            "dark",
            "2d",
            "metroidvania",
            "cute",
            "atmospheric",
            "pixel art",
            "relaxing",
            "controller support"
        ],
        "release_date": "2024"
    },
    "apeescape": {
        "igdb_id": "3762",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2gzc.jpg",
        "game_name": "Ape Escape",
        "igdb_name": "ape escape",
        "rating": [
            "mild animated violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "playstation 3",
            "playstation",
            "playstation portable"
        ],
        "storyline": "the doctors trustfull test apes have escaped and it's up to you to get out there and retrieve all of them.",
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
            "psone classics",
            "moving platforms",
            "spiky-haired protagonist",
            "time trials"
        ],
        "release_date": "1999"
    },
    "apsudoku": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Sudoku",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "aquaria": {
        "igdb_id": "7406",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1r7r.jpg",
        "game_name": "Aquaria",
        "igdb_name": "aquaria",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy",
            "drama"
        ],
        "platforms": [
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "the world of aquaria hides the secrets of creation within its depths. the currents that buffet the many diverse plants and animals that live there also carry with them stories of long lost civilizations; of love and war, change and loss.\n\nfrom lush, green kelp forests to dark caves, exploring will be no easy task. but the splendor of the undersea world awaits naija... and you.\n\nopen waters\ncrystalline blue\n\nthe glassy waters of the open sea let you peer far into the distance, and fish and other creatures play beneath the wide canopies of giant, undersea mushrooms.\n\nhere, ruins serve as a clue to aquaria's long past. will they lead naija to the truth?\n\nthe kelp forest\nthe natural world\n\nthe kelp forest teems with life. as light from above pours across the multitudes of strange plants and animals that live here, one cannot help but marvel at the dynamic landscape.\n\nbut beware, its beauty belies the inherent danger inside. careful not to lose your way.\n\nthe abyss\ndarkness\n\nas you swim deeper, to where sight cannot reach, the abyss begins to swallow you whole. the deeper waters of aquaria have spawned legends of frightening monstrosities that lurk where few things can survive. are they true?\n\nbeyond\n???\n\nwhat lies beyond? are there areas deeper than the abyss? or as we swim ever upward, can we find the source of the light?\n\nonly those with great fortitude will come to know and understand the mysteries of aquaria.",
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
        "release_date": "2007"
    },
    "archipidle": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "ArchipIDLE",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "aus": {
        "igdb_id": "72926",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2nok.jpg",
        "game_name": "An Untitled Story",
        "igdb_name": "an untitled story",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "metroidvania",
            "action-adventure",
            "bird"
        ],
        "release_date": "2007"
    },
    "balatro": {
        "igdb_id": "251833",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9f4g.jpg",
        "game_name": "Balatro",
        "igdb_name": "balatro",
        "rating": [
            "simulated gambling"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "strategy",
            "turn-based strategy (tbs)",
            "indie",
            "card & board game"
        ],
        "themes": [],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "android",
            "pc (microsoft windows)",
            "ios",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "roguelike"
        ],
        "release_date": "2024"
    },
    "banjo_tooie": {
        "igdb_id": "3418",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6c1w.jpg",
        "game_name": "Banjo-Tooie",
        "igdb_name": "banjo-tooie",
        "rating": [
            "crude humor",
            "animated violence",
            "comic mischief",
            "cartoon violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "quiz/trivia",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "nintendo 64"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "dinosaurs",
            "animals",
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
            "cameo appearance",
            "ice stage",
            "character growth",
            "underwater gameplay",
            "rpg elements",
            "villain",
            "recurring boss",
            "invisible wall",
            "shape-shifting",
            "temporary invincibility",
            "gliding",
            "collection marathon",
            "lgbtq+",
            "retroachievements"
        ],
        "release_date": "2000"
    },
    "blasphemous": {
        "igdb_id": "26820",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9yoj.jpg",
        "game_name": "Blasphemous",
        "igdb_name": "blasphemous",
        "rating": [
            "blood and gore",
            "violence",
            "nudity"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "hack and slash/beat 'em up",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "horror"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "a foul curse has fallen upon the land of cvstodia and all its inhabitants - it is simply known as the miracle.\n\nplay as the penitent one - a sole survivor of the massacre of the \u2018silent sorrow\u2019. trapped in an endless cycle of death and rebirth, it\u2019s down to you to free the world from this terrible fate and reach the origin of your anguish.",
        "keywords": [
            "retro",
            "bloody",
            "2d",
            "metroidvania",
            "difficult",
            "side-scrolling",
            "crossover",
            "religion",
            "achievements",
            "pixel art",
            "nudity",
            "silent protagonist",
            "2d platformer",
            "great soundtrack",
            "parrying",
            "moving platforms",
            "soulslike",
            "you can pet the dog",
            "interconnected-world"
        ],
        "release_date": "2019"
    },
    "bomb_rush_cyberfunk": {
        "igdb_id": "135940",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6ya8.jpg",
        "game_name": "Bomb Rush Cyberfunk",
        "igdb_name": "bomb rush cyberfunk",
        "rating": [
            "language",
            "violence",
            "suggestive themes",
            "blood"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "sport",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "start your own cypher and dance, paint, trick, face off with the cops and stake your claim to the extrusions and cavities of a sprawling metropolis in an alternate future set to the musical brainwaves of hideki naganuma.",
        "keywords": [
            "3d platformer",
            "great soundtrack",
            "spiritual successor"
        ],
        "release_date": "2023"
    },
    "brotato": {
        "igdb_id": "199116",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaauv.jpg",
        "game_name": "Brotato",
        "igdb_name": "brotato",
        "rating": [
            "fantasy violence",
            "mild blood"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "fighting",
            "shooter",
            "role-playing (rpg)",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "android",
            "pc (microsoft windows)",
            "ios",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "a spaceship from potato world crashes onto an alien planet. the sole survivor: brotato, the only potato capable of handling 6 weapons at the same time. waiting to be rescued by his mates, brotato must survive in this hostile environment.",
        "keywords": [
            "roguelite"
        ],
        "release_date": "2023"
    },
    "bumpstik": {
        "igdb_id": "271950",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co78k5.jpg",
        "game_name": "Bumper Stickers",
        "igdb_name": "bumper stickers archipelago edition",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "puzzle"
        ],
        "themes": [],
        "platforms": [
            "linux",
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2023"
    },
    "candybox2": {
        "igdb_id": "62779",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3tqk.jpg",
        "game_name": "Candy Box 2",
        "igdb_name": "candy box 2",
        "rating": [],
        "player_perspectives": [
            "text"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)"
        ],
        "themes": [
            "historical",
            "comedy"
        ],
        "platforms": [
            "web browser"
        ],
        "storyline": "",
        "keywords": [
            "medieval",
            "magic",
            "management",
            "merchants"
        ],
        "release_date": "2013"
    },
    "cat_quest": {
        "igdb_id": "36597",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qlq.jpg",
        "game_name": "Cat Quest",
        "igdb_name": "cat quest",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2017"
    },
    "celeste": {
        "igdb_id": "26226",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3byy.jpg",
        "game_name": "Celeste",
        "igdb_name": "celeste",
        "rating": [
            "alcohol reference",
            "fantasy violence",
            "mild language"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "google stadia",
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "set on a fictional version of mount celeste, it follows a young woman named madeline who attempts to climb the mountain, and must face her inner demons in her quest to reach the summit.",
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
        "release_date": "2018"
    },
    "celeste64": {
        "igdb_id": "284430",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7oz4.jpg",
        "game_name": "Celeste 64",
        "igdb_name": "celeste 64: fragments of the mountain",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "female protagonist",
            "lgbtq+"
        ],
        "release_date": "2024"
    },
    "chainedechoes": {
        "igdb_id": "117271",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co544u.jpg",
        "game_name": "Chained Echoes",
        "igdb_name": "chained echoes",
        "rating": [
            "strong language",
            "suggestive themes",
            "sexual themes"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "strategy",
            "turn-based strategy (tbs)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "follow a group of heroes as they explore a land filled to the brim with charming characters, fantastic landscapes and vicious foes. can you bring peace to a continent where war has been waged for generations and betrayal lurks around every corner?",
        "keywords": [
            "jrpg"
        ],
        "release_date": "2022"
    },
    "chatipelago": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Chatipelago",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "checksfinder": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "ChecksFinder",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "civ_6": {
        "igdb_id": "293",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1rjp.jpg",
        "game_name": "Civilization VI",
        "igdb_name": "sid meier's civilization iv",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "simulator",
            "strategy",
            "turn-based strategy (tbs)"
        ],
        "themes": [
            "fantasy",
            "historical",
            "educational",
            "4x (explore, expand, exploit, and exterminate)"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "construction",
            "turn-based",
            "spaceship",
            "management",
            "religion",
            "multiple endings",
            "sequel",
            "mining",
            "digital distribution",
            "voice acting",
            "bink video",
            "loot gathering",
            "royalty",
            "ambient music"
        ],
        "release_date": "2005"
    },
    "clique": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Clique",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "crosscode": {
        "igdb_id": "35282",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co28wy.jpg",
        "game_name": "CrossCode",
        "igdb_name": "crosscode",
        "rating": [
            "fantasy violence",
            "language"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "shooter",
            "puzzle",
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "16-bit",
            "action-adventure",
            "pixel art",
            "crowdfunding",
            "digital distribution",
            "a.i. companion",
            "crowd funded"
        ],
        "release_date": "2018"
    },
    "ctjot": {
        "igdb_id": "20398",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co54iw.jpg",
        "game_name": "Chrono Trigger Jets of Time",
        "igdb_name": "chrono trigger",
        "rating": [
            "animated blood",
            "mild fantasy violence",
            "suggestive themes",
            "use of alcohol"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction"
        ],
        "platforms": [
            "nintendo ds"
        ],
        "storyline": "",
        "keywords": [
            "time travel",
            "magic"
        ],
        "release_date": "2008"
    },
    "cuphead": {
        "igdb_id": "9061",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co62ao.jpg",
        "game_name": "Cuphead",
        "igdb_name": "cuphead",
        "rating": [
            "use of alcohol and tobacco",
            "mild language",
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "pirates",
            "ghosts",
            "retro",
            "magic",
            "2d",
            "shark",
            "robots",
            "run and gun",
            "side-scrolling",
            "bird",
            "achievements",
            "multiple endings",
            "dancing",
            "explosion",
            "digital distribution",
            "anthropomorphism",
            "voice acting",
            "cat",
            "shopping",
            "bow and arrow",
            "parrying",
            "violent plants",
            "conveyor belt",
            "auto-scrolling levels",
            "temporary invincibility",
            "multiple enemy boss fights",
            "boss assistance"
        ],
        "release_date": "2017"
    },
    "cv64": {
        "igdb_id": "1130",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5geb.jpg",
        "game_name": "Castlevania 64",
        "igdb_name": "castlevania",
        "rating": [
            "animated blood",
            "animated violence"
        ],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "platform",
            "puzzle",
            "hack and slash/beat 'em up",
            "adventure"
        ],
        "themes": [
            "action",
            "horror"
        ],
        "platforms": [
            "nintendo 64"
        ],
        "storyline": "castlevania games debut on the n64 this is the first castlevania game in 3d. however, the goal of the game remains the same: defeat dracula and his monsters. the player can choose to be reinhardt schneider with traditional whip or carrie fernandez who uses magic. a new feature is the presence of an in-game clock that switches time from day to night.",
        "keywords": [
            "ghosts",
            "exploration",
            "bloody",
            "magic",
            "summoning support",
            "death",
            "horse",
            "maze",
            "female protagonist",
            "action-adventure",
            "religion",
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
            "character select screen",
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
            "falling damage",
            "unstable platforms",
            "melee",
            "real-time combat",
            "male antagonist",
            "instant kill",
            "difficulty level",
            "moving platforms",
            "plot twist",
            "ambient music",
            "poisoning",
            "drawbridge",
            "time paradox",
            "retroachievements"
        ],
        "release_date": "1999"
    },
    "cvcotm": {
        "igdb_id": "1132",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2zq1.jpg",
        "game_name": "Castlevania - Circle of the Moon",
        "igdb_name": "castlevania: circle of the moon",
        "rating": [
            "mild violence",
            "animated blood"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "horror"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
        ],
        "storyline": "taking place in 1830, circle of the moon is set in one of the fictional universes of the castlevania series. the premise of the original series is the eternal conflict between the vampire hunters of the belmont clan and the immortal vampire dracula. circle of the moon's protagonist, however, is nathan graves, whose parents died a decade ago to banish dracula. morris baldwin, who helped in dracula's banishment, trained him to defeat dracula and the monsters; morris ultimately chose him as his successor and gave him the \"hunter whip\", to the displeasure of hugh, morris' son who trained alongside him.\n\nat an old castle, camilla, a minion of dracula, revives him, only to be interrupted by the arrival of morris, nathan, and hugh. before they are able to banish him again, dracula destroys the floor under nathan and hugh, causing them to plummet down a long tunnel. surviving the fall and wishing to find his father, hugh leaves nathan behind. nathan proceeds to search the castle for his mentor. along the way, he learns that at the next full moon, morris' soul will be used to return dracula to full power. he also periodically encounters hugh, who becomes more hostile as the game progresses. eventually, nathan encounters camilla, who hints that she and dracula are responsible for the changes in his personality. nathan vanquishes camilla in her true form and meets up with hugh once more. upon seeing him, hugh immediately attacks him with the goal of proving himself to his father through nathan's defeat; nathan, however, realizes that dracula is controlling hugh. nathan defeats him, and dracula's control over hugh breaks. confessing that he doubted his self-worth when nathan was chosen as successor, hugh tasks him with morris' rescue.\n\narriving at the ceremonial room, nathan confronts dracula, who confirms that he had tampered with hugh's soul to cause the changes in his personality. they begin to fight and halfway through, dracula teleports away to gain his full power. hugh then frees his father and tasks nathan with dracula's banishment. nathan continues the battle and defeats dracula; escaping the collapsing castle, he reunites with morris and hugh. nathan is declared a master vampire hunter by morris. hugh vows to retrain under morris due to his failure.",
        "keywords": [
            "gravity",
            "magic",
            "metroidvania",
            "death",
            "horse",
            "action-adventure",
            "backtracking",
            "wolf",
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
        "release_date": "2001"
    },
    "dark_souls_2": {
        "igdb_id": "2368",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2eoo.jpg",
        "game_name": "Dark Souls II",
        "igdb_name": "dark souls ii",
        "rating": [
            "blood and gore",
            "partial nudity",
            "violence",
            "mild language"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 3",
            "pc (microsoft windows)",
            "xbox 360"
        ],
        "storyline": "",
        "keywords": [
            "medieval",
            "dark",
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
            "parrying",
            "rpg elements",
            "mercenary",
            "multiple enemy boss fights",
            "boss assistance",
            "sliding down ladders",
            "fire manipulation",
            "status effects",
            "hidden room",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": "2014"
    },
    "dark_souls_3": {
        "igdb_id": "11133",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1vcf.jpg",
        "game_name": "Dark Souls III",
        "igdb_name": "dark souls iii",
        "rating": [
            "blood",
            "violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "xbox one"
        ],
        "storyline": "set in the kingdom of lothric, a bell has rung to signal that the first flame, responsible for maintaining the age of fire, is dying out. as has happened many times before, the coming of the age of dark produces the undead: cursed beings that rise after death. the age of fire can be prolonged by linking the fire, a ritual in which great lords and heroes sacrifice their souls to rekindle the first flame. however, prince lothric, the chosen linker for this age, abandoned his duty and decided to watch the flame die from afar. the bell is the last hope for the age of fire, resurrecting previous lords of cinder (heroes who linked the flame in past ages) to attempt to link the fire again; however, all but one lord shirk their duty. meanwhile, sulyvahn, a sorcerer from the painted world of ariandel, wrongfully proclaims himself pontiff and seizes power over irithyll of the boreal valley and the returning anor londo cathedral from dark souls as a tyrant.\n\nthe ashen one, an undead who failed to become a lord of cinder and thus called an unkindled, rises and must link the fire by returning prince lothric and the defiant lords of cinder to their thrones in firelink shrine. the lords include the abyss watchers, a legion of warriors sworn by the old wolf's blood which linked their souls into one to protect the land from the abyss and ultimately locked in an endless battle between each other; yhorm the giant, who sacrificed his life for a nation conquered by his ancestor; and aldrich, who became a lord of cinder despite his ravenous appetite for both men and gods. lothric was raised to link the first flame but neglected his duties and chose to watch the fire fade instead.\n\nonce the ashen one succeeds in returning lothric and the lords of cinder to their thrones, they travel to the ruins of the kiln of the first flame. there, they encounter the soul of cinder, an amalgamation of all the former lords of cinder. upon defeat, the player can attempt to link the fire or access three other optional endings unlocked by the player's in-game decisions. these include summoning the fire keeper to extinguish the flame and begin an age of dark or killing her in a sudden change of heart. a fourth ending consists of the ashen one taking the flame for their own, becoming the lord of hollows.",
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
            "pick your gender",
            "parrying",
            "sliding down ladders",
            "entering world in a painting",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": "2016"
    },
    "debug": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "debug",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "diddy_kong_racing": {
        "igdb_id": "2723",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wgj.jpg",
        "game_name": "Diddy Kong Racing",
        "igdb_name": "diddy kong racing",
        "rating": [],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "racing"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "nintendo 64"
        ],
        "storyline": "timber the tiger's parents picked a fine time to go on vacation. when they come back they're going to be faced with an island trashed by the spiteful space bully wizpig - unless the local animals can do something about it! so join diddy kong as he teams up with timber the tiger pipsy the mouse and taj the genie in an epic racing adventure unlike anything you've ever experienced before! this unique game blends adventure and racing like no other game! roam anywhere you want on the island by car plane or hovercraft! an enormous amount of single-player and multi-player modes! feel the action when you use the n64 rumble pak and save your times on the n64 controller pak!",
        "keywords": [
            "go-kart",
            "flight",
            "crossover",
            "snow",
            "talking animals",
            "anthropomorphism",
            "monkey",
            "secret area",
            "time trials",
            "behind the waterfall",
            "retroachievements"
        ],
        "release_date": "1997"
    },
    "dk64": {
        "igdb_id": "1096",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co289i.jpg",
        "game_name": "Donkey Kong 64",
        "igdb_name": "donkey kong 64",
        "rating": [
            "mild animated violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "nintendo 64",
            "wii u"
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
            "death match",
            "digital distribution",
            "anthropomorphism",
            "monkey",
            "character select screen",
            "gorilla",
            "polygonal 3d",
            "upgradeable weapons",
            "loot gathering",
            "descendants of other characters",
            "character growth",
            "real-time combat",
            "moving platforms",
            "recurring boss",
            "invisible wall",
            "franchise reboot",
            "western games based on japanese ips",
            "over 100% completion",
            "completion percentage",
            "mine cart sequence",
            "invisibility",
            "foreshadowing",
            "ape",
            "collection marathon",
            "retroachievements"
        ],
        "release_date": "1999"
    },
    "dkc": {
        "igdb_id": "1090",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co70qn.jpg",
        "game_name": "Donkey Kong Country",
        "igdb_name": "donkey kong country",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "on a dark and stormy night in donkey kong island, diddy kong, donkey kong's nephew has taken the weighty responsibility of guarding dk's precious banana hoard for one night, as a part of his \"hero training\". dk entrusts diddy with protecting the hoard until midnight, when he would be relieved, while dk himself goes to sleep as he is tired.\n\neverything seems to go smoothly in the hoard until diddy hears some noises. diddy hears some voices outside and gets scared, asking who's there. king k. rool, who had commanded his kremling minions to steal the bananas. two ropes drop from above and suddenly two kritters appear. diddy cartwheels them both easily, but then a krusha (klump in the instruction booklet) comes in as backup. as diddy is not strong enough to defeat krusha by himself, he is overpowered and defeated by the kremling. the lizars seal diddy inside a barrel and then throw it in the bushes.\ndonkey's grandfather, cranky kong, rushes inside the treehouse to tell donkey kong to wake up so he may tell him what happened. he then tells donkey to check his banana cave. donkey kong is infuriated, exclaiming that the kremlings will pay for stealing his banana hoard and kidnapping his little buddy. donkey goes on to say that he will hunt every corner of the island for his bananas back.",
        "keywords": [
            "gravity",
            "shark",
            "death",
            "2.5d",
            "frog",
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
            "rhinoceros",
            "nintendo power",
            "world map",
            "gorilla",
            "crocodile",
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
            "franchise reboot",
            "auto-scrolling levels",
            "western games based on japanese ips",
            "speedrun",
            "boss assistance",
            "villain turned good",
            "over 100% completion",
            "mine cart sequence",
            "ambient music",
            "resized enemy",
            "on-the-fly character switching",
            "ape",
            "secret areas within secret areas",
            "buddy system",
            "retroachievements"
        ],
        "release_date": "1994"
    },
    "dkc2": {
        "igdb_id": "1092",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co217m.jpg",
        "game_name": "Donkey Kong Country 2",
        "igdb_name": "donkey kong country 2: diddy's kong quest",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "it was a relaxing, sunny day on donkey kong island. funky kong is seen surfing and then falling off his board. he asked for donkey kong to join him, but the hero simply continues lounging. cranky kong goes up to him and complains how he never took breaks, \"whisking off maidens and throwing barrels seven days a week\", but donkey ignores him, confident that he is a hero and that king k. rool is gone for good. cranky soon leaves.\n\nmeanwhile, above, kaptain k. rool, aboard his vessel, the flying krock, commands his minions to invade the island and take donkey captive so that his next attempt at stealing the banana hoard will not be a failure and the hero will never mess with his plans again. donkey, still lounging, did not notice the attack until kutlasses ambushed him and took him prisoner. kaptain k. rool assures donkey kong that he will never see his precious island or his friends again.\n\nlater and back on the island, diddy, dixie and cranky kong find donkey missing, along with a note. it reads:\nhah-arrrrh! we have got the big monkey! if you want him back, you scurvy dogs, you'll have to hand over the banana hoard!\nkaptain k. rool\nat this point, wrinkly, funky and swanky kong come to the scene. cranky suggests to give up the hoard, but diddy insists that donkey kong would be furious if he lost his bananas after all trouble recovering them at the last time. diddy and dixie kong ride to crocodile isle via enguarde the swordfish, and then start their quest.",
        "keywords": [
            "pirates",
            "ghosts",
            "gravity",
            "frog",
            "female protagonist",
            "side-scrolling",
            "multiple protagonists",
            "overworld",
            "multiple endings",
            "dancing",
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
            "rhinoceros",
            "spider",
            "nintendo power",
            "world map",
            "gorilla",
            "crocodile",
            "cat",
            "breaking the fourth wall",
            "game reference",
            "cameo appearance",
            "descendants of other characters",
            "save point",
            "sprinting mechanics",
            "ice stage",
            "checkpoints",
            "underwater gameplay",
            "instant kill",
            "secret area",
            "self-referential humor",
            "liberation",
            "recurring boss",
            "water level",
            "auto-scrolling levels",
            "temporary invincibility",
            "western games based on japanese ips",
            "boss assistance",
            "completion percentage",
            "mine cart sequence",
            "ambient music",
            "resized enemy",
            "fireworks",
            "on-the-fly character switching",
            "ape",
            "buddy system",
            "retroachievements"
        ],
        "release_date": "1995"
    },
    "dkc3": {
        "igdb_id": "1094",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co217n.jpg",
        "game_name": "Donkey Kong Country 3",
        "igdb_name": "donkey kong country 3: dixie kong's double trouble!",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "months after the kongs' second triumph over the kremling krew, they continue to celebrate. one day, dk and diddy suddenly disappear, and a letter from diddy says they were out exploring the island again.\n\nhowever, several days pass without their return, and dixie knows something is up. she takes matters into her own hands, and made her way to the southern shores of donkey kong island, to the northern kremisphere, a canadian and northern european-inspired landmass. there she meets wrinkly kong, and wrinkly confirmed that the kongs had passed by. dixie then makes her way to funky's rentals. funky suggests her to take her baby cousin kiddy kong along with her in the search. funky lends them a boat and the two venture off to find donkey and diddy kong.",
        "keywords": [
            "gravity",
            "minigames",
            "2.5d",
            "female protagonist",
            "side-scrolling",
            "multiple protagonists",
            "overworld",
            "bird",
            "dancing",
            "snow",
            "giant insects",
            "talking animals",
            "swimming",
            "darkness",
            "snowman",
            "explosion",
            "anthropomorphism",
            "bonus stage",
            "monkey",
            "rhinoceros",
            "nintendo power",
            "world map",
            "gorilla",
            "crocodile",
            "descendants of other characters",
            "save point",
            "ice stage",
            "checkpoints",
            "secret area",
            "shielded enemies",
            "moving platforms",
            "recurring boss",
            "auto-scrolling levels",
            "western games based on japanese ips",
            "over 100% completion",
            "ambient music",
            "on-the-fly character switching",
            "behind the waterfall",
            "ape",
            "buddy system",
            "retroachievements"
        ],
        "release_date": "1996"
    },
    "dlcquest": {
        "igdb_id": "3004",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2105.jpg",
        "game_name": "DLCQuest",
        "igdb_name": "dlc quest",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac",
            "xbox 360"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "steam greenlight",
            "digital distribution",
            "deliberately retro",
            "punctuation mark above head"
        ],
        "release_date": "2011"
    },
    "dontstarvetogether": {
        "igdb_id": "17832",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6la0.jpg",
        "game_name": "Dont Starve Together",
        "igdb_name": "don't starve together",
        "rating": [
            "crude humor",
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "simulator",
            "strategy",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "horror",
            "survival",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac",
            "nintendo switch"
        ],
        "storyline": "discover and explore a massive procedurally generated and biome-rich world with countless resources and threats. whether you stick to the surface world, go spelunking in the caves, dive deeper into the ancient archive, or set sail for the lunar islands, it will be a long time before you run out of things to do.\n\nseasonal bosses, wandering menaces, lurking shadow creatures, and plenty of flora and fauna ready to turn you into a spooky ghost.\n\nplow fields and sow seeds to grow the farm of your dreams. tend to your crops to help your fellow survivors stay fed and ready for the challenges to come.\n\nprotect yourself, your friends, and everything you have managed to gather, because you can be sure, somebody or something is going to want it back.\n\nenter a strange and unexplored world full of odd creatures, hidden dangers, and ancient secrets. gather resources to craft items and build structures that match your survival style. play your way as you unravel the mysteries of \"the constant\".\n\ncooperate with your friends in a private game, or find new friends online. work with other players to survive the harsh environment, or strike out on your own.\n\ndo whatever it takes, but most importantly, don't starve.",
        "keywords": [
            "2d",
            "crafting",
            "difficult",
            "action-adventure",
            "funny",
            "atmospheric",
            "survival horror",
            "sequel",
            "digital distribution",
            "bees"
        ],
        "release_date": "2016"
    },
    "doom_1993": {
        "igdb_id": "673",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5rav.jpg",
        "game_name": "DOOM 1993",
        "igdb_name": "doom",
        "rating": [
            "intense violence",
            "blood and gore",
            "violence",
            "animated violence",
            "animated blood and gore"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter"
        ],
        "themes": [
            "action",
            "science fiction",
            "horror"
        ],
        "platforms": [
            "windows mobile",
            "pc-9800 series",
            "linux",
            "dos"
        ],
        "storyline": "the player takes the role of a marine (unnamed to further represent the person playing), \"one of earth's toughest, hardened in combat and trained for action\", who has been incarcerated on mars after assaulting a senior officer when ordered to fire upon civilians. there, he works alongside the union aerospace corporation (uac), a multi-planetary conglomerate and military contractor performing secret experiments on interdimensional travel. recently, the teleportation has shown signs of anomalies and instability, but the research continues nonetheless.\n\nsuddenly, something goes wrong and creatures from hell swarm out of the teleportation gates on deimos and phobos. a defensive response from base security fails to halt the invasion, and the bases are quickly overrun by monsters; all personnel are killed or turned into zombies\n\na military detachment from mars travels to phobos to investigate the incident. the player is tasked with securing the perimeter, as the assault team and their heavy weapons are brought inside. radio contact soon ceases and the player realizes that he is the only survivor. being unable to pilot the shuttle off of phobos by himself, the only way to escape is to go inside and fight through the complexes of the moon base.",
        "keywords": [
            "2.5d",
            "maze",
            "futuristic",
            "silent protagonist",
            "melee",
            "real-time combat",
            "invisibility"
        ],
        "release_date": "1993"
    },
    "doom_ii": {
        "igdb_id": "312",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6iip.jpg",
        "game_name": "DOOM II",
        "igdb_name": "doom ii: hell on earth",
        "rating": [
            "violence",
            "blood and gore"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter",
            "puzzle"
        ],
        "themes": [
            "action",
            "science fiction",
            "horror"
        ],
        "platforms": [
            "pc-9800 series",
            "tapwave zodiac",
            "pc (microsoft windows)",
            "mac",
            "dos"
        ],
        "storyline": "immediately following the events in doom, the player once again assumes the role of the unnamed space marine. after defeating the demon invasion of the mars moon bases and returning from hell, doomguy finds that earth has also been invaded by the demons, who have killed billions of people.\n\nthe humans who survived the attack have developed a plan to build massive spaceships which will carry the remaining survivors into space. once the ships are ready, the survivors prepare to evacuate earth. unfortunately, earth's only ground spaceport gets taken over by the demons, who place a flame barrier over it, preventing any ships from leaving.",
        "keywords": [
            "bloody",
            "death",
            "2.5d",
            "run and gun",
            "achievements",
            "multiple endings",
            "traps",
            "artificial intelligence",
            "easter egg",
            "teleportation",
            "sequel",
            "darkness",
            "explosion",
            "death match",
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
            "dimension travel",
            "boss assistance",
            "over 100% completion",
            "invisibility",
            "jumping puzzle",
            "hidden room",
            "secret areas within secret areas",
            "another world"
        ],
        "release_date": "1994"
    },
    "doronko_wanko": {
        "igdb_id": "290647",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7zj5.jpg",
        "game_name": "DORONKO WANKO",
        "igdb_name": "doronko wanko",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "simulator"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "dog"
        ],
        "release_date": "2024"
    },
    "dsr": {
        "igdb_id": "81085",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2uro.jpg",
        "game_name": "Dark Souls Remastered",
        "igdb_name": "dark souls: remastered",
        "rating": [
            "blood and gore",
            "partial nudity",
            "violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "magic",
            "3d",
            "undead",
            "secret areas within secret areas",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": "2018"
    },
    "dungeon_clawler": {
        "igdb_id": "290897",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7ygu.jpg",
        "game_name": "Dungeon Clawler",
        "igdb_name": "dungeon clawler",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "simulator",
            "strategy",
            "turn-based strategy (tbs)",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "fantasy",
            "survival"
        ],
        "platforms": [
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "roguelike",
            "roguelite"
        ],
        "release_date": "2024"
    },
    "dw1": {
        "igdb_id": "3878",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2dyy.jpg",
        "game_name": "Digimon World",
        "igdb_name": "digimon world 4",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "xbox",
            "nintendo gamecube",
            "playstation 2"
        ],
        "storyline": "the yamato server disappears after the x-virus attacks, and the doom server has taken it's place. it's up to the you and up to 3 of your friends, the digital security guard (d.s.g.) to venture into the doom server, discover the source of the virus and deal with the infection before it can infect the home server.\n\nyou will venture into the dry lands stop the virus from spreading, into the venom jungle to stop the dread note from launching and then the machine pit to destroy the final boss.\n\nafter finishing the game for the first time, you unlock hard mode, where the enemies are stronger, but you keep all of your levels, equipment and digivolutions. do it again, and you unlock the hardest difficulty, very hard.",
        "keywords": [
            "anime",
            "sequel",
            "leveling up",
            "voice acting",
            "polygonal 3d",
            "shopping",
            "tie-in"
        ],
        "release_date": "2005"
    },
    "earthbound": {
        "igdb_id": "2899",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6v07.jpg",
        "game_name": "EarthBound",
        "igdb_name": "earthbound",
        "rating": [],
        "player_perspectives": [
            "first person",
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction",
            "drama"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii u",
            "new nintendo 3ds",
            "game boy advance",
            "super famicom"
        ],
        "storyline": "the story begins when ness is awakened by a meteor that has plummeted to the earth near his home, whereupon he proceeds to investigate the crash site. when ness gets to the crash site he discovers a police roadblock and pokey minch, his friend and neighbor, who tells him to go home. later, ness is woken up again by pokey knocking at his door, demanding help to find his brother picky.\n\nthey find him near the meteor sleeping behind a tree and wake him up. then the three encounter an insect from the meteor named buzz buzz who informs ness that he is from the future where the \"universal cosmic destroyer\", giygas, dominates the planet. buzz buzz senses great potential in ness and instructs him to embark on a journey to seek out and record the melodies of eight \"sanctuaries,\" unite his own powers with the earth's and gain the strength required to confront giygas.",
        "keywords": [
            "aliens",
            "ghosts",
            "dinosaurs",
            "time travel",
            "2d",
            "16-bit",
            "turn-based",
            "robots",
            "mummy",
            "female protagonist",
            "religion",
            "multiple protagonists",
            "teleportation",
            "darkness",
            "nintendo power",
            "leveling up",
            "damsel in distress",
            "party system",
            "descendants of other characters",
            "save point",
            "robot protagonist",
            "saving the world",
            "royalty",
            "male antagonist",
            "self-referential humor",
            "kidnapping",
            "fire manipulation",
            "censored version",
            "status effects",
            "retroachievements"
        ],
        "release_date": "1994"
    },
    "enderlilies": {
        "igdb_id": "138858",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9s9e.jpg",
        "game_name": "Ender Lilies",
        "igdb_name": "ender lilies: quietus of the knights",
        "rating": [
            "violence",
            "blood"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "once upon a time, in the end's kingdom, the dying rain suddenly started to fall, transforming all living things it touched into bloodthirsty corpses. following this tragedy, the kingdom quickly fell into chaos and soon, no one remained. the rain, as if cursed, would never stop falling on the land. in the depths of a forsaken church, lily opens her eyes...",
        "keywords": [
            "metroidvania",
            "female protagonist",
            "forest",
            "witches",
            "soulslike",
            "conversation"
        ],
        "release_date": "2021"
    },
    "factorio": {
        "igdb_id": "7046",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1tfy.jpg",
        "game_name": "Factorio",
        "igdb_name": "factorio",
        "rating": [
            "blood",
            "violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "simulator",
            "strategy",
            "indie"
        ],
        "themes": [
            "science fiction",
            "survival",
            "sandbox"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac",
            "nintendo switch"
        ],
        "storyline": "you crash land on an alien planet and must research a way to get yourself a rocket out of the planet. defend yourself from the natives who dislike the pollution your production generates.",
        "keywords": [
            "aliens",
            "crafting",
            "digital distribution"
        ],
        "release_date": "2020"
    },
    "factorio_saws": {
        "igdb_id": "263344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co91k3.jpg",
        "game_name": "Factorio Space Age Without Space",
        "igdb_name": "factorio: space age",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "simulator",
            "strategy",
            "indie"
        ],
        "themes": [
            "science fiction",
            "survival",
            "sandbox"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "crafting"
        ],
        "release_date": "2024"
    },
    "faxanadu": {
        "igdb_id": "1974",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5jif.jpg",
        "game_name": "Faxanadu",
        "igdb_name": "faxanadu",
        "rating": [
            "mild fantasy violence",
            "use of tobacco"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox"
        ],
        "platforms": [
            "wii",
            "family computer",
            "nintendo entertainment system"
        ],
        "storyline": "the player-controlled protagonist of is an unidentified wanderer. he has no name, though the japanese version allows the player to choose one. the game begins when he approaches eolis, his hometown, after an absence to find it in disrepair and virtually abandoned. worse still, the town is under attack by dwarves.the elven king explains that the elf fountain water, their life source, has stopped and provides the protagonist with 1500 golds, the games currency, to prepare for his journey to uncover the cause.as the story unfolds, it is revealed that elves and dwarfs lived in harmony among the world tree until the evil one emerged from a fallen meteorite. the evil one then transformed the dwarves into monsters against their will and set them against the elves. the dwarf king, grieve, swallowed his magical sword before he was transformed, hiding it in his own body to prevent the evil one from acquiring it. it is only with this sword that the evil one can be destroyed.his journey takes him to four overworld areas: the tree's buttress, the inside of the trunk, the tree's branches and finally the dwarves' mountain stronghold.",
        "keywords": [
            "magic",
            "metroidvania",
            "backtracking",
            "save point",
            "temporary invincibility",
            "merchants",
            "nameless protagonist"
        ],
        "release_date": "1987"
    },
    "ff1": {
        "igdb_id": "385",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2xv8.jpg",
        "game_name": "Final Fantasy",
        "igdb_name": "final fantasy",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "kids"
        ],
        "platforms": [
            "nintendo 3ds",
            "wii",
            "family computer",
            "wii u",
            "nintendo entertainment system"
        ],
        "storyline": "the story follows four youths called the light warriors, who each carry one of their world's four elemental orbs which have been darkened by the four elemental fiends. together, they quest to defeat these evil forces, restore light to the orbs, and save their world.",
        "keywords": [
            "jrpg"
        ],
        "release_date": "1987"
    },
    "ff4fe": {
        "igdb_id": "387",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2y6s.jpg",
        "game_name": "Final Fantasy IV Free Enterprise",
        "igdb_name": "final fantasy ii",
        "rating": [
            "mild fantasy violence",
            "mild suggestive themes"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii"
        ],
        "storyline": "",
        "keywords": [
            "jrpg",
            "retroachievements"
        ],
        "release_date": "1991"
    },
    "ffmq": {
        "igdb_id": "415",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2y0b.jpg",
        "game_name": "Final Fantasy Mystic Quest",
        "igdb_name": "final fantasy: mystic quest",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "super famicom"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "casual",
            "ninja",
            "turn-based",
            "jrpg",
            "mummy",
            "overworld",
            "undead",
            "sword & sorcery",
            "explosion",
            "party system",
            "rock music",
            "franchise reboot",
            "retroachievements"
        ],
        "release_date": "1992"
    },
    "ffta": {
        "igdb_id": "414",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wyp.jpg",
        "game_name": "Final Fantasy Tactics Advance",
        "igdb_name": "final fantasy tactics advance",
        "rating": [
            "mild violence",
            "alcohol reference"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "strategy",
            "turn-based strategy (tbs)",
            "tactical"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [
            "ninja",
            "magic",
            "grinding",
            "turn-based",
            "summoning support",
            "jrpg",
            "death",
            "permadeath",
            "management",
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
            "franchise reboot",
            "mana",
            "androgyny",
            "random encounter",
            "damage over time"
        ],
        "release_date": "2003"
    },
    "fm": {
        "igdb_id": "4108",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ui5.jpg",
        "game_name": "Yu-Gi-Oh! Forbidden Memories",
        "igdb_name": "yu-gi-oh! forbidden memories",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "strategy",
            "turn-based strategy (tbs)",
            "card & board game"
        ],
        "themes": [
            "fantasy",
            "historical"
        ],
        "platforms": [
            "playstation"
        ],
        "storyline": "the game begins in ancient egypt, with prince atem sneaking out of the palace to see his friends, jono and teana, at the dueling grounds. while there, they witness a ceremony performed by the mages, which is darker than the ceremonies that they normally perform. after the ceremony, atem duels one of the priests, named seto, and defeats him.\n\nwhen atem returns to the palace, he is quickly sent to bed by simon muran, his tutor and advisor. as simon walks away, he is informed by a guard that the high priest heishin has invaded the palace, using a strange magic. muran searches for heishin. when muran finds him, heishin tells muran that he has found the dark power, then uses the millennium rod to blast muran. when heishin finds atem, he threatens to kill the egyptian king and queen if he does not hand over the millennium puzzle. muran appears behind heishin and tells atem to smash the puzzle. atem obeys, and muran seals himself and atem inside the puzzle, to wait for someone to reassemble it.\n\nfive thousand years later, yugi mutou reassembles the puzzle. he speaks to atem in the puzzle, and atem gives yugi six blank cards. not sure what they are for, he carries them into a dueling tournament. after he defeats one of the duelists, one of the cards is filled with a millennium item. realizing what the cards are for, yugi completes the tournament and fills all six cards with millennium items. this allows atem to return to his time.\n\nonce in his own time, muran tells atem of what has happened since he was sealed away. heishin and the mages have taken control of the kingdom with the millennium items, and that the only way to free the kingdom is to recover the items from the mages guarding them. after passing this on, muran dies.\n\nafter he catches up with jono and teana, he goes to the destroyed palace and searches it. he finds seto, who gives him a map with the locations of the mages and the millennium items, and asks him to defeat the mages.\n\nafter atem recovers all of the millennium items but one, seto leads him to heishin, who holds the millennium rod. atem defeats heishin, but discovers that seto has the millennium rod, and merely wanted to use atem to gather the items in one place. atem duels seto for the items and defeats him, but after the duel, heishin grabs the items and uses them to summon the darknite. hoping to use the darknite to destroy his enemies, he doesn't have the item to prove his authority and as a result, the darknite instead turns heishin into a card. heishin now turned into a playing card, darknite now mocks heishin before incinerating the card. after atem shows that he had the millennium items, darknite challenges him to a duel. atem defeats him, and he transforms into nitemare, who challenges atem again. atem defeats him again, and nitemare begrudgingly returns from where he came. atem then is able to take the throne and lead his people in peace.",
        "keywords": [
            "anime",
            "turn-based",
            "summoning support",
            "tie-in"
        ],
        "release_date": "1999"
    },
    "generic": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Archipelago",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "getting_over_it": {
        "igdb_id": "72373",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3wl5.jpg",
        "game_name": "Getting Over It",
        "igdb_name": "getting over it with bennett foddy",
        "rating": [],
        "player_perspectives": [
            "third person",
            "side view"
        ],
        "genres": [
            "platform",
            "simulator",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "horror",
            "comedy"
        ],
        "platforms": [
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "climb up an enormous mountain with nothing but a hammer and a pot.",
        "keywords": [
            "casual",
            "psychological horror",
            "difficult",
            "space",
            "funny",
            "story rich",
            "great soundtrack",
            "digital distribution"
        ],
        "release_date": "2017"
    },
    "gstla": {
        "igdb_id": "1173",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co25rt.jpg",
        "game_name": "Golden Sun The Lost Age",
        "igdb_name": "golden sun: the lost age",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
        ],
        "storyline": "\"it is the dawn of a new age...and the heroes of golden sun have been abandoned. now, the world is falling into darkness. a new band of adventurers is the world's final hope...but they may also be its doom. pursued by the heroes of the original golden sun, they must race to complete their quest before the world becomes lost to the ages.\"",
        "keywords": [
            "anime",
            "magic",
            "minigames",
            "turn-based",
            "summoning support",
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
            "villain turned good",
            "androgyny",
            "ancient advanced civilization technology",
            "random encounter",
            "fire manipulation",
            "battle screen",
            "behind the waterfall"
        ],
        "release_date": "2002"
    },
    "gzdoom": {
        "igdb_id": "307741",
        "cover_url": "",
        "game_name": "gzDoom",
        "igdb_name": "gzdoom sm64",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": ""
    },
    "hades": {
        "igdb_id": "113112",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co39vc.jpg",
        "game_name": "Hades",
        "igdb_name": "hades",
        "rating": [
            "mild language",
            "alcohol reference",
            "violence",
            "suggestive themes",
            "blood"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "hack and slash/beat 'em up",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "drama"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "ios",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "zagreus, the son of hades, has discovered that his mother, which he was led to believe was nyx, night incarnate, is actually someone else, and is outside hell. he is now attempting to escape his father's domain, with the help of the other gods of olympus, in an attempt to find his real mother.",
        "keywords": [
            "roguelike",
            "difficult",
            "stylized",
            "story rich",
            "roguelite",
            "you can pet the dog"
        ],
        "release_date": "2020"
    },
    "hcniko": {
        "igdb_id": "142405",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2o6i.jpg",
        "game_name": "Here Comes Niko!",
        "igdb_name": "here comes niko!",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "exploration",
            "animals",
            "3d",
            "minigames",
            "fishing",
            "frog",
            "female protagonist",
            "crossover",
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
            "controller support",
            "beach"
        ],
        "release_date": "2021"
    },
    "heretic": {
        "igdb_id": "6362",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mwz.jpg",
        "game_name": "Heretic",
        "igdb_name": "heretic",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter"
        ],
        "themes": [
            "fantasy",
            "historical"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac",
            "dos"
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
            "death match",
            "digital distribution",
            "skeletons",
            "melee",
            "secret area",
            "hidden room"
        ],
        "release_date": "1994"
    },
    "hk": {
        "igdb_id": "14593",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co93cr.jpg",
        "game_name": "Hollow Knight",
        "igdb_name": "hollow knight",
        "rating": [
            "fantasy violence",
            "mild blood"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "wii u",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "dark",
            "sword",
            "2d",
            "metroidvania",
            "action-adventure",
            "achievements",
            "atmospheric",
            "giant insects",
            "silent protagonist",
            "crowdfunding",
            "2d platformer",
            "crowd funded",
            "shielded enemies",
            "parrying",
            "merchants",
            "fast traveling",
            "creature compendium",
            "controller support",
            "interconnected-world"
        ],
        "release_date": "2017"
    },
    "huniepop": {
        "igdb_id": "9655",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2sor.jpg",
        "game_name": "Hunie Pop",
        "igdb_name": "huniepop",
        "rating": [],
        "player_perspectives": [
            "first person",
            "text"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)",
            "simulator",
            "strategy",
            "indie",
            "visual novel"
        ],
        "themes": [
            "fantasy",
            "comedy",
            "erotic",
            "romance"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "anime",
            "nudity"
        ],
        "release_date": "2015"
    },
    "huniepop2": {
        "igdb_id": "72472",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5x87.jpg",
        "game_name": "Hunie Pop 2",
        "igdb_name": "huniepop 2: double date",
        "rating": [],
        "player_perspectives": [
            "first person",
            "text"
        ],
        "genres": [
            "puzzle",
            "simulator",
            "strategy",
            "indie",
            "visual novel"
        ],
        "themes": [
            "erotic",
            "romance"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "an era of darkness and destruction draws near as an ancient evil of limitless lechery, the nymphojinn, will soon be awoken by a cosmic super-period of unspeakable pms. reunite with kyu, your old love fairy sidekick, and travel to the island of inna de poona to develop your double dating prowess and overcome the insatiable lust of the demonic pair.",
        "keywords": [
            "anime",
            "fairy",
            "achievements",
            "funny",
            "nudity",
            "digital distribution",
            "voice acting"
        ],
        "release_date": "2021"
    },
    "hylics2": {
        "igdb_id": "98469",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co290q.jpg",
        "game_name": "Hylics 2",
        "igdb_name": "hylics 2",
        "rating": [],
        "player_perspectives": [
            "first person",
            "third person",
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "the tyrant gibby\u2019s minions seek to reconstitute their long-presumed-annihilated master. it\u2019s up to our crescent headed protagonist wayne to assemble a crew and put a stop to that sort of thing.",
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
            "2d platformer",
            "great soundtrack"
        ],
        "release_date": "2020"
    },
    "inscryption": {
        "igdb_id": "139090",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co401c.jpg",
        "game_name": "Inscryption",
        "igdb_name": "inscryption",
        "rating": [
            "blood",
            "strong language",
            "violence"
        ],
        "player_perspectives": [
            "first person",
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "strategy",
            "adventure",
            "indie",
            "card & board game"
        ],
        "themes": [
            "horror",
            "mystery"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "from the creator of pony island and the hex comes the latest mind melting, self-destructing love letter to video games. inscryption is an inky black card-based odyssey that blends the deckbuilding roguelike, escape-room style puzzles, and psychological horror into a blood-laced smoothie. darker still are the secrets inscrybed upon the cards...\nin inscryption you will...\n\nacquire a deck of woodland creature cards by draft, surgery, and self mutilation\nunlock the secrets lurking behind the walls of leshy's cabin\nembark on an unexpected and deeply disturbing odyssey",
        "keywords": [],
        "release_date": "2021"
    },
    "jakanddaxter": {
        "igdb_id": "1528",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1w7q.jpg",
        "game_name": "Jak and Daxter: The Precursor Legacy",
        "igdb_name": "jak and daxter: the precursor legacy",
        "rating": [
            "fantasy violence",
            "mild suggestive themes"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "racing",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "comedy",
            "open world"
        ],
        "platforms": [
            "playstation 4",
            "playstation 2"
        ],
        "storyline": "the opening sequence of the game features jak and daxter in a speedboat headed for misty island, an area prohibited by their watch over samos. upon arriving to the island, daxter had second thoughts about straying from the village. the two perch on a large skeleton to observe a legion of lurkers crowded around two dark figures, gol and maia, who were commanding the lurkers to \"deal harshly with anyone who strays from the village,\" and to search for any precursor artifacts and eco near sandover village.[4] after the secret observation, jak and daxter continue searching the island. daxter trips on a dark eco canister which he tosses to jak after expressing his dislike for the item, and as jak caught the object it lit up. shortly afterwards a bone armor lurker suddenly confronted the two, where jak threw the dark eco canister at the lurker, killing it, but inadvertently knocked daxter into a dark eco silo behind him. when daxter reemerged, he was in the form of an ottsel, and upon realizing the transformation he began to panic.",
        "keywords": [
            "exploration",
            "mascot",
            "shark",
            "frog",
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
            "language selection",
            "polygonal 3d",
            "breaking the fourth wall",
            "cameo appearance",
            "descendants of other characters",
            "save point",
            "ice stage",
            "checkpoints",
            "auto-saving",
            "useable vehicles",
            "coming of age",
            "moving platforms",
            "destructible environment",
            "temporary invincibility",
            "spiky-haired protagonist",
            "ancient advanced civilization technology",
            "time paradox",
            "comic relief",
            "damage over time"
        ],
        "release_date": "2001"
    },
    "jigsaw": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Jigsaw",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "k64": {
        "igdb_id": "2713",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wcz.jpg",
        "game_name": "Kirby 64 - The Crystal Shards",
        "igdb_name": "kirby 64: the crystal shards",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "on the planet of ripple star, lives a group of kind and peaceful fairies. the planet itself is protected from danger by the power of the great crystal, which watches over ripple star. this power, however, draws the attention of dark matter, who wishes to use the great crystal for its own evil agenda. its gigantic mass attacks and searches for the crystal, blackening the sky and sending the fairies into panic. in response to the threat dark matter presents, the queen of ripple star orders a fairy named ribbon to take the crystal to a safe place. ribbon tries to fly away with the crystal in tow, but is stopped by three orbs sent by dark matter. the crystal shatters into 74 shards, scattered throughout several planets, and ribbon crashes onto planet popstar. kirby finds one shard and gives it to ribbon, whereupon the two set out to find the others. once kirby and his friends collect every crystal shard and defeat miracle matter, dark matter flees ripple star and explodes. the victory is cut short, however, as the crystal detects a powerful presence of dark matter energy within the fairy queen and expels it from her, manifesting over the planet to create dark star. kirby and his friends infiltrate dark star, and king dedede launches them up to challenge 02. kirby and ribbon, armed with their shard gun, destroyed 02 and the dark star.",
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
            "sliding down ladders",
            "whale",
            "fireworks",
            "collection marathon",
            "retroachievements"
        ],
        "release_date": "2000"
    },
    "kdl3": {
        "igdb_id": "3720",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co25su.jpg",
        "game_name": "Kirby's Dream Land 3",
        "igdb_name": "kirby's dream land 3",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "super famicom"
        ],
        "storyline": "",
        "keywords": [
            "mascot",
            "side-scrolling",
            "melee",
            "shape-shifting",
            "whale",
            "retroachievements"
        ],
        "release_date": "1997"
    },
    "kh1": {
        "igdb_id": "1219",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co30zf.jpg",
        "game_name": "Kingdom Hearts",
        "igdb_name": "kingdom hearts",
        "rating": [
            "violence",
            "cartoon violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "playstation 2"
        ],
        "storyline": "when his world is destroyed and his friends mysteriously disappear, a young boy named sora is thrust into a quest to find his missing friends and prevent the armies of darkness from destroying many other worlds. during his quest, he meets many characters from classic disney films and a handful from the final fantasy video game series.",
        "keywords": [
            "pirates",
            "grinding",
            "minigames",
            "summoning support",
            "death",
            "action-adventure",
            "crossover",
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
            "a.i. companion",
            "stat tracking",
            "unbeatable enemies",
            "destructible environment",
            "villain",
            "recurring boss",
            "water level",
            "invisible wall",
            "plot twist",
            "villain turned good",
            "spiky-haired protagonist",
            "gliding",
            "random encounter",
            "whale",
            "comic relief"
        ],
        "release_date": "2002"
    },
    "kh2": {
        "igdb_id": "1221",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co30t1.jpg",
        "game_name": "Kingdom Hearts 2",
        "igdb_name": "kingdom hearts ii",
        "rating": [
            "mild blood",
            "violence",
            "use of alcohol"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 3",
            "playstation 4",
            "playstation 2"
        ],
        "storyline": "one year after the events of kingdom hearts: chain of memories, sora, donald and goofy awaken in twilight town. bent on the quest to find riku and king mickey mouse, the three begin their journey. however, they soon discover that while they have been asleep, the heartless are back. not only that, but new enemies also showed up during their absence. sora, donald and goofy set off on a quest to rid the world of the heartless once more, uncovering the many secrets that linger about ansem and the mysterious organization xiii.",
        "keywords": [],
        "release_date": "2005"
    },
    "ladx": {
        "igdb_id": "1027",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4o47.jpg",
        "game_name": "Link's Awakening DX Beta",
        "igdb_name": "the legend of zelda: link's awakening dx",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "game boy color",
            "nintendo 3ds"
        ],
        "storyline": "after the events of a link to the past, the hero link travels by ship to other countries to train for further threats. after being attacked at sea, link's ship sinks and he finds himself stranded on koholint island. he awakens to see a beautiful woman looking down at him and soon learns the island has a giant egg on top of a mountain that the wind fish inhabits deep inside. link is told to awaken the wind fish and all will be answered, so he sets out on another quest.",
        "keywords": [
            "magic",
            "mascot",
            "fishing",
            "death",
            "maze",
            "chicken",
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
            "animal cruelty",
            "status effects",
            "another world",
            "comic relief"
        ],
        "release_date": "1998"
    },
    "landstalker": {
        "igdb_id": "15072",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kb9.jpg",
        "game_name": "Landstalker - The Treasures of King Nole",
        "igdb_name": "landstalker",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox"
        ],
        "platforms": [
            "linux",
            "wii",
            "sega mega drive/genesis",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "action-adventure",
            "fairy",
            "leveling up",
            "real-time combat"
        ],
        "release_date": "1992"
    },
    "lego_star_wars_tcs": {
        "igdb_id": "2682",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qrr.jpg",
        "game_name": "Lego Star Wars: The Complete Saga",
        "igdb_name": "lego star wars: the complete saga",
        "rating": [
            "fantasy violence",
            "crude humor",
            "cartoon violence",
            "animated violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "comedy",
            "kids"
        ],
        "platforms": [
            "playstation 3",
            "wii",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "xbox 360"
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
            "character select screen",
            "polygonal 3d",
            "shopping",
            "motion control",
            "character creation",
            "melee",
            "grapple",
            "liberation",
            "rpg elements",
            "destructible environment",
            "villain",
            "tie-in",
            "on-the-fly character switching"
        ],
        "release_date": "2007"
    },
    "lethal_company": {
        "igdb_id": "212089",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5ive.jpg",
        "game_name": "Lethal Company",
        "igdb_name": "lethal company",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "indie"
        ],
        "themes": [
            "action",
            "science fiction",
            "horror",
            "comedy"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "you are a contracted worker for the company. your job is to collect scrap from abandoned, industrialized moons to meet the company's profit quota. you can use the cash you earn to travel to new moons with higher risks and rewards--or you can buy fancy suits and decorations for your ship. experience nature, scanning any creature you find to add them to your bestiary. explore the wondrous outdoors and rummage through their derelict, steel and concrete underbellies. just never miss the quota.",
        "keywords": [
            "aliens",
            "exploration",
            "monsters",
            "psychological horror",
            "survival horror"
        ],
        "release_date": "2023"
    },
    "lingo": {
        "igdb_id": "189169",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5iy5.jpg",
        "game_name": "Lingo",
        "igdb_name": "lingo",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "open world"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "3d"
        ],
        "release_date": "2021"
    },
    "lufia2ac": {
        "igdb_id": "1178",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9mg3.jpg",
        "game_name": "Lufia II: Ancient Cave",
        "igdb_name": "lufia ii: rise of the sinistrals",
        "rating": [
            "mild animated violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "super famicom"
        ],
        "storyline": "",
        "keywords": [
            "retroachievements"
        ],
        "release_date": "1995"
    },
    "luigismansion": {
        "igdb_id": "2485",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wr1.jpg",
        "game_name": "Luigi's Mansion",
        "igdb_name": "luigi's mansion",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "adventure"
        ],
        "themes": [
            "action",
            "horror",
            "comedy"
        ],
        "platforms": [
            "nintendo gamecube"
        ],
        "storyline": "one day, luigi received an unexpected message: you've won a huge mansion! naturally, he[sic] got very excited and called his brother, mario. \"mario? it's me, luigi. i won myself a big mansion! meet me there and we'll celebrate, what do you say?\"\n\nluigi tried to follow the map to his new mansion, but the night was dark, and he became hopelessly lost in an eerie forest along the way. finally, he came upon a gloomy mansion on the edge of the woods. according to the map, this mansion seemed to be the one luigi was looking for. as soon as luigi set foot in the mansion, he started to feel nervous. mario, who should have arrived first, was nowhere to be seen. not only that, but there were ghosts in the mansion!\n\nsuddenly, a ghost lunged at luigi! \"mario! help meee!\" that's when a strange old man with a vacuum cleaner on his back appeared out of nowhere! this strange fellow managed to rescue luigi from the ghosts, then the two of them escaped...\n\nit just so happened that the old man, professor elvin gadd, who lived near the house, was researching his favorite subject, ghosts. luigi told professor e. gadd that his brother mario was missing, so the professor decided to give luigi two inventions that would help him search for his brother.\n\nluigi's not exactly known for his bravery. can he get rid of all the prank-loving ghosts and find mario?",
        "keywords": [
            "ghosts",
            "3d",
            "death",
            "action-adventure",
            "darkness",
            "polygonal 3d",
            "descendants of other characters",
            "save point",
            "stereoscopic 3d",
            "italian accent",
            "interconnected-world"
        ],
        "release_date": "2001"
    },
    "marioland2": {
        "igdb_id": "1071",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7gxg.jpg",
        "game_name": "Super Mario Land 2",
        "igdb_name": "super mario land 2: 6 golden coins",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "nintendo 3ds",
            "game boy"
        ],
        "storyline": "danger! danger!\n\nwhile i was away crusading against the mystery alien tatanga in sarasa land, an evil creep took over my castle and put the people of mario land under his control with a magic spell. this intruder goes by the name of wario. he mimics my appearance, and has tried to steal my castle many times. it seems he has succeeded this time.\n\nwario has scattered the 6 golden coins from my castle all over mario land. these golden coins are guarded by those under wario's spell. without these coins, we can't get into the castle to deal with wario. we must collect the 6 coins, attack wario in the castle, and save everybody!\n\nit\u2019s time to set out on our mission!!",
        "keywords": [
            "space",
            "mario",
            "turtle",
            "whale"
        ],
        "release_date": "1992"
    },
    "mario_kart_double_dash": {
        "igdb_id": "2344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7ndu.jpg",
        "game_name": "Mario Kart Double Dash",
        "igdb_name": "mario kart: double dash!!",
        "rating": [
            "mild cartoon violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "racing",
            "arcade"
        ],
        "themes": [
            "action",
            "kids"
        ],
        "platforms": [
            "nintendo gamecube"
        ],
        "storyline": "",
        "keywords": [
            "go-kart",
            "yoshi",
            "mario",
            "princess peach"
        ],
        "release_date": "2003"
    },
    "megamix": {
        "igdb_id": "120278",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa4vr.jpg",
        "game_name": "Hatsune Miku Project Diva Mega Mix+",
        "igdb_name": "hatsune miku: project diva mega mix",
        "rating": [
            "blood",
            "sexual themes",
            "violence"
        ],
        "player_perspectives": [
            "third person",
            "side view"
        ],
        "genres": [
            "music",
            "arcade"
        ],
        "themes": [],
        "platforms": [
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2020"
    },
    "meritous": {
        "igdb_id": "78479",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/zkameytcg0na8alfswsp.jpg",
        "game_name": "Meritous",
        "igdb_name": "meritous",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)"
        ],
        "themes": [],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2008"
    },
    "messenger": {
        "igdb_id": "71628",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2hr9.jpg",
        "game_name": "The Messenger",
        "igdb_name": "the messenger",
        "rating": [
            "fantasy violence",
            "language",
            "crude humor"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "retro",
            "ninja",
            "2d",
            "metroidvania",
            "difficult",
            "8-bit"
        ],
        "release_date": "2018"
    },
    "metroidprime": {
        "igdb_id": "1105",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w4w.jpg",
        "game_name": "Metroid Prime",
        "igdb_name": "metroid prime",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter",
            "platform",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "open world"
        ],
        "platforms": [
            "nintendo gamecube"
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
            "falling damage",
            "unstable platforms",
            "auto-aim",
            "grapple",
            "real-time combat",
            "underwater gameplay",
            "difficulty level",
            "multiple gameplay perspectives",
            "mercenary",
            "violent plants",
            "moving platforms",
            "sequence breaking",
            "shape-shifting",
            "tentacles",
            "western games based on japanese ips",
            "speedrun",
            "boss assistance",
            "fetch quests",
            "completion percentage",
            "linear gameplay",
            "meme origin",
            "ancient advanced civilization technology",
            "ambient music",
            "creature compendium",
            "foreshadowing",
            "isolation"
        ],
        "release_date": "2002"
    },
    "minecraft": {
        "igdb_id": "121",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa77e.jpg",
        "game_name": "Minecraft",
        "igdb_name": "minecraft: java edition",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "first person",
            "third person",
            "virtual reality"
        ],
        "genres": [
            "simulator",
            "adventure"
        ],
        "themes": [
            "fantasy",
            "survival",
            "sandbox",
            "kids",
            "open world"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "minecraft: java edition (previously known as minecraft) is the original version of minecraft, developed by mojang studios for windows, macos, and linux. notch began development on may 10, 2009, publicly releasing minecraft on may 17, 2009. the full release of the game was on november 18, 2011, at minecon 2011.",
        "keywords": [
            "monsters",
            "animals",
            "sword",
            "3d",
            "construction",
            "fishing",
            "crafting",
            "death",
            "procedural generation",
            "permadeath",
            "horse",
            "archery",
            "chicken",
            "action-adventure",
            "witches",
            "bird",
            "achievements",
            "traps",
            "snow",
            "wolf",
            "dog",
            "mining",
            "swimming",
            "day/night cycle",
            "darkness",
            "snowman",
            "explosion",
            "digital distribution",
            "spider",
            "cat",
            "language selection",
            "polygonal 3d",
            "bow and arrow",
            "loot gathering",
            "skeletons",
            "deliberately retro",
            "falling damage",
            "character creation",
            "stereoscopic 3d",
            "potion",
            "auto-saving",
            "real-time combat",
            "difficulty level",
            "multiple gameplay perspectives",
            "rpg elements",
            "sleeping",
            "meme origin",
            "poisoning",
            "fire manipulation",
            "status effects",
            "beach",
            "bees"
        ],
        "release_date": "2011"
    },
    "mk64": {
        "igdb_id": "2342",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co67hm.jpg",
        "game_name": "Mario Kart 64",
        "igdb_name": "mario kart 64",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "racing",
            "arcade"
        ],
        "themes": [
            "action",
            "kids",
            "party"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "",
        "keywords": [
            "go-kart",
            "crossover",
            "princess",
            "artificial intelligence",
            "snow",
            "sequel",
            "bats",
            "turtle",
            "explosion",
            "death match",
            "anthropomorphism",
            "monkey",
            "character select screen",
            "polygonal 3d",
            "ice stage",
            "difficulty level",
            "invisible wall",
            "temporary invincibility",
            "time trials",
            "italian accent",
            "falling object",
            "ape",
            "retroachievements"
        ],
        "release_date": "1996"
    },
    "mlss": {
        "igdb_id": "3351",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co21rg.jpg",
        "game_name": "Mario & Luigi Superstar Saga",
        "igdb_name": "mario & luigi: superstar saga",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
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
            "mario",
            "easy",
            "turtle",
            "spiritual successor",
            "digital distribution",
            "anthropomorphism",
            "super-ness",
            "shopping",
            "breaking the fourth wall",
            "party system",
            "save point",
            "royalty",
            "self-referential humor",
            "rpg elements",
            "tentacles",
            "fireworks",
            "italian accent",
            "battle screen",
            "wiggler",
            "princess peach"
        ],
        "release_date": "2003"
    },
    "mm2": {
        "igdb_id": "1734",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5572.jpg",
        "game_name": "Mega Man 2",
        "igdb_name": "mega man ii",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "nintendo 3ds",
            "game boy"
        ],
        "storyline": "even after his crushing defeat at the hands of mega man during the events of mega man: dr. wily's revenge, dr. wily was already planning his next scheme. if he could get his hands on the time machine (named time skimmer in the american manual) that was being developed at the time-space research laboratory (named chronos institute in the american manual), he thought he just might be able to change the past.\n\nafter stealing the time machine, wily had wanted to set out immediately on a trip across time, but had to put an emergency brake down on his plans when he discovered that the time machine had a serious flaw.\n\nmeanwhile, dr. light had been dispatched to the time-space laboratory to investigate. with the help of rush\u2019s super-sense of smell, he was able to deduce that it was none other than dr. wily behind the theft. having a bad feeling about the incident, dr. light quickly called upon mega man and rush to search out dr. wily\u2019s whereabouts.",
        "keywords": [
            "mascot",
            "death",
            "robots",
            "flight",
            "side-scrolling",
            "pixel art",
            "sequel",
            "8-bit",
            "explosion",
            "psone classics",
            "upgradeable weapons",
            "checkpoints",
            "robot protagonist",
            "underwater gameplay",
            "male antagonist",
            "instant kill",
            "difficulty level",
            "moving platforms",
            "conveyor belt",
            "villain",
            "water level",
            "monomyth"
        ],
        "release_date": "1991"
    },
    "mm3": {
        "igdb_id": "1716",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co55ce.jpg",
        "game_name": "Mega Man 3",
        "igdb_name": "mega man 3",
        "rating": [
            "mild cartoon violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "arcade",
            "nintendo 3ds",
            "wii",
            "family computer",
            "wii u",
            "nintendo entertainment system"
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
            "8-bit",
            "darkness",
            "explosion",
            "psone classics",
            "checkpoints",
            "robot protagonist",
            "underwater gameplay",
            "moving platforms",
            "villain",
            "recurring boss",
            "multiple enemy boss fights",
            "jumping puzzle",
            "falling object",
            "monomyth"
        ],
        "release_date": "1990"
    },
    "mmbn3": {
        "igdb_id": "1758",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co203k.jpg",
        "game_name": "MegaMan Battle Network 3",
        "igdb_name": "mega man battle network 3 blue",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "real time strategy (rts)",
            "role-playing (rpg)",
            "tactical"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [
            "futuristic"
        ],
        "release_date": "2002"
    },
    "mmx3": {
        "igdb_id": "1743",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co55pa.jpg",
        "game_name": "Mega Man X3",
        "igdb_name": "mega man x3",
        "rating": [
            "animated violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii u",
            "new nintendo 3ds",
            "legacy mobile device",
            "super famicom"
        ],
        "storyline": "zero, who had returned as an irregular hunter, became the commander of the zero special forces unit and continued to sweep up irregulars together with x, who was active as the commander of the 17th elite unit, and other hunters in the unit.\nat the same time, dr. doppler, a scientist-type repliloid, conducted research that revealed the fact that the computer virus \"sigma virus\" was the cause of irregularities, developed a special antibody virus, and proposed that it be injected into repliloids. as a result, the number of irregularities decreased. furthermore, dr. doppler declared that he would build \"doppeltown,\" a peaceful city where humans and replicants could coexist, and he gained the support of both humans and replicants.\na few months later, however, doppler and his repliroids, who had been exposed to the antibody virus mentioned above, rebelled. the irregular hunters recognized doppler and the participants in the rebellion as irregulars, and x and zero were ordered to go into action.",
        "keywords": [
            "death",
            "robots",
            "run and gun",
            "futuristic",
            "side-scrolling",
            "multiple protagonists",
            "multiple endings",
            "sequel",
            "wall jump",
            "explosion",
            "rhinoceros",
            "upgradeable weapons",
            "checkpoints",
            "robot protagonist",
            "underwater gameplay",
            "moving platforms",
            "retroachievements"
        ],
        "release_date": "1995"
    },
    "mm_recomp": {
        "igdb_id": "1030",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3pah.jpg",
        "game_name": "Majora's Mask Recompiled",
        "igdb_name": "the legend of zelda: majora's mask",
        "rating": [
            "animated violence",
            "cartoon violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "horror",
            "open world"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "64dd",
            "wii u"
        ],
        "storyline": "after the events of the legend of zelda: ocarina of time, link departs on his horse epona in the lost woods and is assaulted by an imp named skull kid who dons a mysterious mask, accompanied by the fairies tael and tatl. skull kid turns link into a small plant-like creature known as deku scrub and takes away his horse and his magical ocarina. shortly afterward, tatl joins link and agrees to help him revert to his native form. a meeting with a wandering mask salesman reveals that the skull kid is wearing majora's mask, an ancient item used in hexing rituals, which calls forth a menacing moon hovering over the land of termina. link has exactly three days to find a way to prevent this from happening.",
        "keywords": [
            "psychological horror",
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
            "dimension travel",
            "boss assistance",
            "meme origin",
            "living inventory",
            "another world",
            "retroachievements"
        ],
        "release_date": "2000"
    },
    "momodoramoonlitfarewell": {
        "igdb_id": "188088",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7mxs.jpg",
        "game_name": "Momodora Moonlit Farewell",
        "igdb_name": "momodora: moonlit farewell",
        "rating": [
            "fantasy violence",
            "blood",
            "suggestive themes"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5",
            "nintendo switch"
        ],
        "storyline": "momodora: moonlit farewell presents the account of the greatest calamity to befall the village of koho, five years after the events of momodora iii. once the toll of an ominous bell is heard, the village is soon threatened by a demon invasion.\n\nthe village's matriarch sends momo reinol, their most capable priestess, to investigate the bell and find the bellringer responsible for summoning demons. it is their hope that by finding the culprit, they will also be able to secure the village's safety, and most importantly, the sacred lun tree's, a source of life and healing for koho...",
        "keywords": [
            "metroidvania"
        ],
        "release_date": "2024"
    },
    "monster_sanctuary": {
        "igdb_id": "89594",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1q3q.jpg",
        "game_name": "Monster Sanctuary",
        "igdb_name": "monster sanctuary",
        "rating": [
            "fantasy violence",
            "mild blood",
            "tobacco reference"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "strategy",
            "turn-based strategy (tbs)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "metroidvania"
        ],
        "release_date": "2020"
    },
    "musedash": {
        "igdb_id": "86316",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6h43.jpg",
        "game_name": "Muse Dash",
        "igdb_name": "muse dash",
        "rating": [
            "sexual themes",
            "mild blood",
            "mild lyrics",
            "fantasy violence",
            "suggestive themes"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "music",
            "indie"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "anime",
            "casual",
            "2d",
            "side-scrolling",
            "achievements",
            "cute",
            "nudity",
            "digital distribution",
            "difficulty level"
        ],
        "release_date": "2018"
    },
    "mzm": {
        "igdb_id": "1107",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1vci.jpg",
        "game_name": "Metroid Zero Mission",
        "igdb_name": "metroid: zero mission",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "open world"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
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
        "release_date": "2004"
    },
    "noita": {
        "igdb_id": "52006",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qp1.jpg",
        "game_name": "Noita",
        "igdb_name": "noita",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "role-playing (rpg)",
            "simulator",
            "adventure",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "magic",
            "roguelite"
        ],
        "release_date": "2020"
    },
    "oot": {
        "igdb_id": "1029",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3nnx.jpg",
        "game_name": "Ocarina of Time",
        "igdb_name": "the legend of zelda: ocarina of time",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "64dd",
            "wii u"
        ],
        "storyline": "a young boy named link was raised in the village of the elf-like kokiri people. one day a fairy named navi introduces him to the village's guardian, the great deku tree. it appears that a mysterious man has cursed the tree, and link is sent to the hyrule castle to find out more. princess zelda tells link that ganondorf, the leader of the gerudo tribe, seeks to obtain the triforce, a holy relic that grants immense power to the one who possesses it. link must do everything in his power to obtain the triforce before ganondorf does, and save hyrule.",
        "keywords": [
            "gravity",
            "time travel",
            "minigames",
            "death",
            "horse",
            "archery",
            "chicken",
            "time manipulation",
            "action-adventure",
            "religion",
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
            "easy",
            "block puzzle",
            "digital distribution",
            "countdown timer",
            "world map",
            "polygonal 3d",
            "bow and arrow",
            "damsel in distress",
            "game reference",
            "cameo appearance",
            "disorientation zone",
            "descendants of other characters",
            "sprinting mechanics",
            "ice stage",
            "falling damage",
            "character growth",
            "side quests",
            "auto-aim",
            "grapple",
            "real-time combat",
            "underwater gameplay",
            "a.i. companion",
            "walking through walls",
            "mercenary",
            "coming of age",
            "sequence breaking",
            "villain",
            "been here before",
            "water level",
            "invisible wall",
            "plot twist",
            "boss assistance",
            "androgyny",
            "animal cruelty",
            "resized enemy",
            "drawbridge",
            "time paradox",
            "fast traveling",
            "censored version",
            "context sensitive",
            "living inventory",
            "damage over time",
            "retroachievements"
        ],
        "release_date": "1998"
    },
    "openrct2": {
        "igdb_id": "80720",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ngq.jpg",
        "game_name": "OpenRCT2",
        "igdb_name": "openrct2",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "real time strategy (rts)",
            "simulator",
            "strategy"
        ],
        "themes": [
            "business",
            "4x (explore, expand, exploit, and exterminate)"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "death",
            "maze",
            "kid friendly",
            "easter egg",
            "explosion",
            "kidnapping"
        ],
        "release_date": "2014"
    },
    "oribf": {
        "igdb_id": "7344",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1y41.jpg",
        "game_name": "Ori and the Blind Forest",
        "igdb_name": "ori and the blind forest",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "thriller"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "ori, the protagonist of the game, falls from the spirit tree and is adopted by naru, who raises ori as her own. when a disastrous event occurs causing the forest to wither and naru to die, ori is left to explore the forest. ori eventually encounters sein, who begins to guide ori on an adventure to restore the forest through the recovery of the light of three main elements supporting the balance of the forest: waters, winds and warmth.",
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
        "release_date": "2015"
    },
    "osrs": {
        "igdb_id": "79824",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mo1.jpg",
        "game_name": "Old School Runescape",
        "igdb_name": "old school runescape",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "text"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "fantasy",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "grinding"
        ],
        "release_date": "2013"
    },
    "osu": {
        "igdb_id": "3012",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8a4m.jpg",
        "game_name": "osu!",
        "igdb_name": "osu!",
        "rating": [],
        "player_perspectives": [
            "auditory"
        ],
        "genres": [
            "music",
            "indie",
            "arcade"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "anime",
            "stat tracking",
            "difficulty level"
        ],
        "release_date": "2007"
    },
    "outer_wilds": {
        "igdb_id": "11737",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co65ac.jpg",
        "game_name": "Outer Wilds",
        "igdb_name": "outer wilds",
        "rating": [
            "fantasy violence",
            "alcohol reference"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "puzzle",
            "simulator",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "science fiction",
            "open world",
            "mystery"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "welcome to the space program! you're the newest recruit of outer wilds ventures, a fledgling space program searching for answers in a strange, constantly evolving solar system. what lurks in the heart of the ominous dark bramble? who built the alien ruins on the moon? can the endless time loop be stopped? answers await you in the most dangerous reaches of space.\n\nthe planets of outer wilds are packed with hidden locations that change with the passage of time. visit an underground city of before it's swallowed by sand, or explore the surface of a planet as it crumbles beneath your feet. every secret is guarded by hazardous environments and natural catastrophes.\n\nstrap on your hiking boots, check your oxygen levels, and get ready to venture into space. use a variety of unique gadgets to probe your surroundings, track down mysterious signals, decipher ancient alien writing, and roast the perfect marshmallow.",
        "keywords": [
            "exploration",
            "time travel"
        ],
        "release_date": "2019"
    },
    "overcooked2": {
        "igdb_id": "103341",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1usu.jpg",
        "game_name": "Overcooked! 2",
        "igdb_name": "overcooked! 2",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "simulator",
            "strategy",
            "tactical",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "comedy",
            "kids",
            "party"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "you can pet the dog"
        ],
        "release_date": "2018"
    },
    "paint": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Paint",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "papermario": {
        "igdb_id": "3340",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1qda.jpg",
        "game_name": "Paper Mario",
        "igdb_name": "paper mario",
        "rating": [
            "comic mischief"
        ],
        "player_perspectives": [
            "third person",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "gravity",
            "mascot",
            "turn-based",
            "death",
            "maze",
            "gambling",
            "undead",
            "princess",
            "easter egg",
            "silent protagonist",
            "turtle",
            "snowman",
            "spiritual successor",
            "anthropomorphism",
            "leveling up",
            "human",
            "damsel in distress",
            "breaking the fourth wall",
            "party system",
            "save point",
            "melee",
            "unbeatable enemies",
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
            "battle screen",
            "retroachievements"
        ],
        "release_date": "2000"
    },
    "peaks_of_yore": {
        "igdb_id": "238690",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8zzc.jpg",
        "game_name": "Peaks of Yore",
        "igdb_name": "peaks of yore",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2023"
    },
    "placidplasticducksim": {
        "igdb_id": "204122",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4yq5.jpg",
        "game_name": "Placid Plastic Duck Simulator",
        "igdb_name": "placid plastic duck simulator",
        "rating": [],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "music",
            "puzzle",
            "simulator"
        ],
        "themes": [
            "comedy",
            "sandbox",
            "kids",
            "party"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "casual",
            "pop culture reference"
        ],
        "release_date": "2022"
    },
    "pmd_eos": {
        "igdb_id": "2323",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7ovf.jpg",
        "game_name": "Pokemon Mystery Dungeon Explorers of Sky",
        "igdb_name": "pok\u00e9mon mystery dungeon: explorers of sky",
        "rating": [
            "mild cartoon violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)"
        ],
        "themes": [
            "fantasy",
            "kids"
        ],
        "platforms": [
            "wii u",
            "nintendo ds"
        ],
        "storyline": "",
        "keywords": [
            "time travel",
            "roguelike",
            "jrpg"
        ],
        "release_date": "2009"
    },
    "poe": {
        "igdb_id": "1911",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1n6w.jpg",
        "game_name": "Path of Exile",
        "igdb_name": "path of exile",
        "rating": [
            "intense violence",
            "blood and gore",
            "sexual themes",
            "language",
            "nudity"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "hack and slash/beat 'em up",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "horror"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "mac",
            "xbox one"
        ],
        "storyline": "all exiles are given the same choice: to sink or swim. those that don't drown will reach the forsaken shores of wraeclast, where the only welcome is the clinging embrace of undeath. however, a small band of survivors has managed to hold fast in a ruined lighthouse, desperately repelling both the grasping undead and the manic scavengers that stubbornly cling to their last shreds of humanity. under the commanding gaze of axiom prison, snarling goatmen roam the craggy bluffs, always keeping their cloven feet well clear of the rhoa-infested swamps in the lowlands. all along the coast, rotting shipwrecks litter the shoreline, the spirits of the stranded sailors still haunting the wreckages of their ill-fated ships, waiting to take out their sorrow and rage on those who yet live. all the while, the siren herself continues her sweet, sad song, luring ever more ships to their watery graves.\n\nfarther inland, through the twisting caves and darkened forests, the ruins of civilisation become more apparent. the ravages of time have worn many buildings to rubble, and stripped away decaying flesh, leaving only grotesquely grinning bones. the dark, fetid caves and underground passages are a clattering refuge for these skeletal ranks, while the open forests and riverways brim with monstrous beasts with a taste for blood. recently, ragtag groups of bloodthirsty bandits have built fortified camps in the forest, openly challenging one another while extorting food and supplies from the small, struggling village that sits between them atop a stone dam. ignored by the squabbling bandits, strange newcomers clad in black armor have been seen skulking around various large ruins, their purpose both mysterious yet unsettling.\n\natop a sheer cliff of ruptured mantle, straddling the river feeding a mighty waterfall, lies the fallen capital of the eternal empire. its former glory rots amid the ruins of a blasted cityscape, the buildings decrepit and mouldering. but sarn is far from uninhabited. many of the original citizens still lurk the dark recesses, their humanity washed clean by the cataclysm of centuries past. these undying monsters roam the city at night and skulk the shadows during the day, for the naked sunlight is anathema to their shrivelled, leathery skin. the sun-scarred days are far from peaceful, however. a legion of soldiers from oriath has occupied the area to the west of the river, and is fighting an all-out war against the multifarious denizens of the city. every day their black-clad soldiers battle twisted insects that scuttle and breed, feasting on anything that moves. every day they throw battalions against the army of floating, red ribbons that eviscerate all who trespass on their domain. every day they skirmish against a small group of exiles who have barricaded themselves on a small island in the middle of the river, caught between certain death on both sides.",
        "keywords": [
            "bloody",
            "magic",
            "3d",
            "leveling up",
            "bink video",
            "bow and arrow",
            "potion",
            "mana",
            "fast traveling"
        ],
        "release_date": "2013"
    },
    "pokemon_crystal": {
        "igdb_id": "1514",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pil.jpg",
        "game_name": "Pokemon Crystal",
        "igdb_name": "pok\u00e9mon crystal version",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "kids"
        ],
        "platforms": [
            "game boy color",
            "nintendo 3ds"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "anime",
            "collecting",
            "minigames",
            "turn-based",
            "gambling",
            "kid friendly",
            "teleportation",
            "bats",
            "day/night cycle",
            "leveling up",
            "world map",
            "shopping",
            "party system",
            "sprinting mechanics",
            "character growth",
            "character creation",
            "side quests",
            "pick your gender",
            "potion",
            "melee",
            "coming of age",
            "punctuation mark above head",
            "been here before",
            "sleeping",
            "tentacles",
            "animal cruelty",
            "poisoning",
            "random encounter",
            "fire manipulation",
            "battle screen",
            "nameless protagonist",
            "status effects",
            "damage over time"
        ],
        "release_date": "2000"
    },
    "pokemon_emerald": {
        "igdb_id": "1517",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1zhr.jpg",
        "game_name": "Pokemon Emerald",
        "igdb_name": "pok\u00e9mon emerald version",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "kids"
        ],
        "platforms": [
            "game boy advance"
        ],
        "storyline": "both team magma and team aqua are featured as the villainous teams, each stirring trouble at different stages in the game. the objective of each team, to awaken groudon and kyogre, respectively, is eventually fulfilled.\nrayquaza is prominent plot-wise, awakened in order to stop the destructive battle between groudon and kyogre. it is now the one out of the three ancient pok\u00e9mon that can be caught prior to the elite four challenge, while still at the same place and at the same high level as in ruby and sapphire.",
        "keywords": [
            "exploration",
            "anime",
            "collecting",
            "minigames",
            "turn-based",
            "gambling",
            "bird",
            "kid friendly",
            "teleportation",
            "giant insects",
            "silent protagonist",
            "leveling up",
            "shopping",
            "party system",
            "sprinting mechanics",
            "character creation",
            "side quests",
            "pick your gender",
            "potion",
            "melee",
            "coming of age",
            "punctuation mark above head",
            "recurring boss",
            "tentacles",
            "animal cruelty",
            "poisoning",
            "random encounter",
            "fire manipulation",
            "fast traveling",
            "battle screen",
            "nameless protagonist",
            "creature compendium",
            "status effects",
            "damage over time"
        ],
        "release_date": "2004"
    },
    "pokemon_frlg": {
        "igdb_id": "1516",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1zip.jpg",
        "game_name": "Pokemon FireRed and LeafGreen",
        "igdb_name": "pok\u00e9mon leafgreen version",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction",
            "kids"
        ],
        "platforms": [
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [
            "monsters",
            "collecting"
        ],
        "release_date": "2004"
    },
    "pokemon_rb": {
        "igdb_id": "1561",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5pi4.jpg",
        "game_name": "Pokemon Red and Blue",
        "igdb_name": "pok\u00e9mon red version",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "kids",
            "open world"
        ],
        "platforms": [
            "nintendo 3ds",
            "game boy"
        ],
        "storyline": "the player character starts out in pallet town. when the player character tries to leave the town without a pok\u00e9mon of their own, they are stopped in the nick of time by professor oak, who invites them to his lab. there, he gives them a pok\u00e9mon of their own and a pok\u00e9dex, telling them about his dream to make a complete guide on every pok\u00e9mon in the world. after the player character battles their rival and leaves the lab, they are entitled to win every gym badge, compete in the pok\u00e9mon league, and fulfill oak's dream by catching every pok\u00e9mon.",
        "keywords": [
            "collecting"
        ],
        "release_date": "1996"
    },
    "powerwashsimulator": {
        "igdb_id": "138590",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7gek.jpg",
        "game_name": "Powerwash Simulator",
        "igdb_name": "powerwash simulator",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "simulator",
            "indie"
        ],
        "themes": [
            "business",
            "sandbox"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "you're looking to start a business \u2013 but what? you decide power washing is super satisfying and you'd like to turn it into a full time gig. you put your good friend harper shaw, a bargain hunter and auction lot buyer up to the task of finding you the perfect vehicle for your new enterprise.\n\nthrough completing various jobs, you get to know the citizens of muckingham, the small town in which the game is set, helping wash away their various problems. figuratively... and literally!\n\nthe first client you are introduced to is cal, harper shaw's new disgruntled neighbour. they are a volcanologist, who\u2019s moved back into town to study mount rushless, the local volcano, and to help look after his ageing parents. he's so worked up as he bought a house without even looking at a picture of the back garden. he thinks the previous owners might have even owned rhinos it's that dirty...",
        "keywords": [
            "3d",
            "funny",
            "atmospheric",
            "relaxing",
            "story rich",
            "family friendly"
        ],
        "release_date": "2022"
    },
    "pseudoregalia": {
        "igdb_id": "259465",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6vcy.jpg",
        "game_name": "Pseudoregalia",
        "igdb_name": "pseudoregalia: jam ver.",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "metroidvania"
        ],
        "release_date": "2023"
    },
    "quake": {
        "igdb_id": "333",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9bg9.jpg",
        "game_name": "Quake 1",
        "igdb_name": "quake",
        "rating": [
            "animated blood and gore",
            "animated violence"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter"
        ],
        "themes": [
            "action",
            "science fiction",
            "horror",
            "historical",
            "comedy"
        ],
        "platforms": [
            "zeebo",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "dos",
            "amiga",
            "sega saturn",
            "legacy mobile device"
        ],
        "storyline": "the player takes the role of a protagonist known as ranger who was sent into a portal in order to stop an enemy code-named \"quake\". the government had been experimenting with teleportation technology and developed a working prototype called a \"slipgate\"; the mysterious quake compromised the slipgate by connecting it with its own teleportation system, using it to send death squads to the \"human\" dimension in order to test the martial capabilities of humanity.",
        "keywords": [
            "aliens",
            "bloody",
            "medieval",
            "death",
            "run and gun",
            "backtracking",
            "portals",
            "silent protagonist",
            "swimming",
            "explosion",
            "spiritual successor",
            "death match",
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
            "secret areas within secret areas",
            "retroachievements"
        ],
        "release_date": "1996"
    },
    "rac2": {
        "igdb_id": "1770",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co230n.jpg",
        "game_name": "Ratchet & Clank 2",
        "igdb_name": "ratchet & clank: going commando",
        "rating": [
            "animated blood",
            "comic mischief",
            "fantasy violence",
            "mild language"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "comedy"
        ],
        "platforms": [
            "playstation 2"
        ],
        "storyline": "having defeated chairman drek in their last intergalactic adventure, ratchet and clank find themselves returning to a more sedate lifestyle. that is, until they are approached by abercrombie fizzwidget, the cro of megacorp, who needs the duo to track down the company\u2019s most promising experimental project, which has been stolen by a mysterious masked figure. initially, the mission seemed like a sunday stroll in the park, but we soon find our heroes entangled in a colossal struggle for control of the galaxy. along the way, the duo unleashes some of the coolest weapons and gadgets ever invented upon the most dangerous foes they have ever faced. ratchet and clanks set out to destroy anything and anyone who stands in their way of discovering the secrets that lie behind \u201cthe experiment.\u201d",
        "keywords": [],
        "release_date": "2003"
    },
    "raft": {
        "igdb_id": "27082",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1xdc.jpg",
        "game_name": "Raft",
        "igdb_name": "raft",
        "rating": [
            "violence",
            "blood"
        ],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "simulator",
            "adventure",
            "indie"
        ],
        "themes": [
            "survival"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5"
        ],
        "storyline": "trapped on a small raft with nothing but a hook made of old plastic, players awake on a vast, blue ocean totally alone and with no land in sight! with a dry throat and an empty stomach, survival will not be easy!\n\nresources are tough to come by at sea: players will have to make sure to catch whatever debris floats by using their trusty hook and when possible, scavenge the reefs beneath the waves and the islands above. however, thirst and hunger is not the only danger in the ocean\u2026 watch out for the man-eating shark determined to end your voyage!",
        "keywords": [
            "shark",
            "crafting",
            "bees"
        ],
        "release_date": "2022"
    },
    "residentevil2remake": {
        "igdb_id": "19686",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1ir3.jpg",
        "game_name": "Resident Evil 2 Remake",
        "igdb_name": "resident evil 2",
        "rating": [
            "strong language",
            "intense violence",
            "blood and gore"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "shooter",
            "adventure"
        ],
        "themes": [
            "action",
            "horror",
            "survival"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "ios",
            "playstation 5",
            "mac",
            "xbox one"
        ],
        "storyline": "players join rookie police officer leon kennedy and college student claire redfield, who are thrust together by a disastrous outbreak in raccoon city that transformed its population into deadly zombies. both leon and claire have their own separate playable campaigns, allowing players to see the story from both characters\u2019 perspectives. the fate of these two fan favorite characters is in the player's hands as they work together to survive and get to the bottom of what is behind the terrifying attack on the city.",
        "keywords": [
            "bloody",
            "survival horror",
            "censored version"
        ],
        "release_date": "2019"
    },
    "residentevil3remake": {
        "igdb_id": "115115",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co22l7.jpg",
        "game_name": "Resident Evil 3 Remake",
        "igdb_name": "resident evil 3",
        "rating": [
            "intense violence",
            "strong language",
            "blood and gore"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "shooter",
            "adventure"
        ],
        "themes": [
            "action",
            "horror",
            "survival"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "ios",
            "playstation 5",
            "mac",
            "xbox one"
        ],
        "storyline": "a series of strange disappearances have been occurring in the american midwest within a place called racoon city. a specialist squad of the police force known as s.t.a.r.s. has been investigating the case, and have determined that the pharmaceutical company umbrella and their biological weapon, the t-virus, are behind the incidents. jill valentine and the other surviving s.t.a.r.s. members try to make this truth known, but find that the police department itself is under umbrella's sway and their reports are rejected out of hand. with the viral plague spreading through the town and to her very doorstep, jill is determined to survive. however, an extremely powerful pursuer has already been dispatched to eliminate her.",
        "keywords": [
            "survival horror"
        ],
        "release_date": "2020"
    },
    "rimworld": {
        "igdb_id": "9789",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaaqj.jpg",
        "game_name": "Rimworld",
        "igdb_name": "rimworld",
        "rating": [
            "blood",
            "suggestive themes",
            "violence",
            "use of drugs and alcohol"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "real time strategy (rts)",
            "simulator",
            "strategy",
            "indie"
        ],
        "themes": [
            "science fiction",
            "survival"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "rimworld follows three survivors from a crashed space liner as they build a colony on a frontier world at the rim of known space. inspired by the space western vibe of firefly, the deep simulation of dwarf fortress, and the epic scale of dune and warhammer 40,000.\n\nmanage colonists' moods, needs, thoughts, individual wounds, and illnesses. engage in deeply-simulated small-team gunplay. fashion structures, weapons, and apparel from metal, wood, stone, cloth, or exotic, futuristic materials. fight pirate raiders, hostile tribes, rampaging animals and ancient killing machines. discover a new generated world each time you play. build colonies in biomes ranging from desert to jungle to tundra, each with unique flora and fauna. manage and develop colonists with unique backstories, traits, and skills. learn to play easily with the help of an intelligent and unobtrusive ai tutor.",
        "keywords": [
            "management",
            "base building"
        ],
        "release_date": "2018"
    },
    "rogue_legacy": {
        "igdb_id": "3221",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co27fi.jpg",
        "game_name": "Rogue Legacy",
        "igdb_name": "rogue legacy",
        "rating": [
            "fantasy violence",
            "crude humor"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle",
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "playstation 3",
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "playstation vita",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "exploration",
            "medieval",
            "ninja",
            "magic",
            "minigames",
            "16-bit",
            "roguelike",
            "metroidvania",
            "death",
            "procedural generation",
            "permadeath",
            "horse",
            "gambling",
            "time manipulation",
            "female protagonist",
            "flight",
            "action-adventure",
            "side-scrolling",
            "multiple protagonists",
            "bird",
            "time limit",
            "traps",
            "pixel art",
            "wolf",
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
            "royalty",
            "potion",
            "stat tracking",
            "secret area",
            "shielded enemies",
            "violent plants",
            "punctuation mark above head",
            "temporary invincibility",
            "boss assistance",
            "fire manipulation",
            "jumping puzzle",
            "resized enemy",
            "drawbridge",
            "lgbtq+"
        ],
        "release_date": "2013"
    },
    "ror1": {
        "igdb_id": "3173",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2k2z.jpg",
        "game_name": "Risk of Rain",
        "igdb_name": "risk of rain",
        "rating": [
            "alcohol reference",
            "fantasy violence",
            "mild blood",
            "mild language"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "role-playing (rpg)",
            "hack and slash/beat 'em up",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction",
            "survival"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "playstation vita",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "roguelike",
            "permadeath",
            "difficult",
            "time limit",
            "pixel art",
            "steam greenlight",
            "crowdfunding",
            "bow and arrow",
            "crowd funded",
            "roguelite"
        ],
        "release_date": "2013"
    },
    "ror2": {
        "igdb_id": "28512",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2eu7.jpg",
        "game_name": "Risk of Rain 2",
        "igdb_name": "risk of rain 2",
        "rating": [
            "blood",
            "drug reference",
            "fantasy violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "shooter",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "science fiction",
            "survival"
        ],
        "platforms": [
            "google stadia",
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "risk of rain 2 follows the crew of ues: safe travels as they try to find ues: contact light and any survivors along their path. they have to try and survive the hostile wildlife and environment as difficulty increases over time, navigating petrichor v via the teleporters strewn across the entire planet. the crew loop endlessly through many distinct environments, but end upon the moon to defeat the final boss.\n\nwith each run, you\u2019ll learn the patterns of your foes, and even the longest odds can be overcome with enough skill. a unique scaling system means both you and your foes limitlessly increase in power over the course of a game\u2013what once was a bossfight will in time become a common enemy.\n\nmyriad survivors, items, enemies, and bosses return to risk 2, and many new ones are joining the fight. brand new survivors like the artificer and mul-t debut alongside classic survivors such as the engineer, huntress, and\u2013of course\u2013the commando. with over 75 items to unlock and exploit, each run will keep you cleverly strategizing your way out of sticky situations.",
        "keywords": [
            "roguelite"
        ],
        "release_date": "2020"
    },
    "sa2b": {
        "igdb_id": "192194",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5p3o.jpg",
        "game_name": "Sonic Adventure 2 Battle",
        "igdb_name": "sonic adventure 2: battle",
        "rating": [
            "mild lyrics",
            "violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "playstation 3",
            "pc (microsoft windows)",
            "xbox 360"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2012"
    },
    "sadx": {
        "igdb_id": "192114",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4iln.jpg",
        "game_name": "Sonic Adventure DX",
        "igdb_name": "sonic adventure: sonic adventure dx upgrade",
        "rating": [
            "animated violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "playstation 3",
            "pc (microsoft windows)",
            "xbox 360"
        ],
        "storyline": "doctor robotnik seeks a new way to defeat his longtime nemesis sonic and conquer the world. during his research, he learns about an entity called chaos\u2014a creature that, thousands of years ago, helped to protect the chao and the all-powerful master emerald, which balances the power of the seven chaos emeralds. when a tribe of echidnas sought to steal the power of the emeralds, breaking the harmony they had with the chao, chaos retaliated by using the emeralds' power to transform into a monstrous beast, perfect chaos, and wipe them out. before it could destroy the world, tikal, a young echidna who befriended chaos, imprisoned it in the master emerald along with herself. eggman releases chaos and sonic and his friends must act against eggman's plans and prevent the monster from becoming more powerful.",
        "keywords": [],
        "release_date": "2010"
    },
    "satisfactory": {
        "igdb_id": "90558",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8tfy.jpg",
        "game_name": "Satisfactory",
        "igdb_name": "satisfactory",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "simulator",
            "strategy",
            "adventure",
            "indie"
        ],
        "themes": [
            "science fiction",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5"
        ],
        "storyline": "",
        "keywords": [
            "crafting",
            "base building"
        ],
        "release_date": "2024"
    },
    "saving_princess": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Saving Princess",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "sc2": {
        "igdb_id": "239",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1tnn.jpg",
        "game_name": "Starcraft 2",
        "igdb_name": "starcraft ii: wings of liberty",
        "rating": [
            "blood and gore",
            "language",
            "suggestive themes",
            "use of alcohol and tobacco",
            "violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "real time strategy (rts)",
            "strategy"
        ],
        "themes": [
            "action",
            "science fiction",
            "warfare"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "aliens",
            "space",
            "human",
            "side quests",
            "mercenary"
        ],
        "release_date": "2010"
    },
    "seaofthieves": {
        "igdb_id": "11137",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2558.jpg",
        "game_name": "Sea of Thieves",
        "igdb_name": "sea of thieves",
        "rating": [
            "crude humor",
            "use of alcohol",
            "violence"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "simulator",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one"
        ],
        "storyline": "",
        "keywords": [
            "pirates",
            "exploration",
            "grinding",
            "crafting",
            "action-adventure",
            "digital distribution",
            "skeletons",
            "you can pet the dog"
        ],
        "release_date": "2018"
    },
    "shapez": {
        "igdb_id": "134826",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4tfx.jpg",
        "game_name": "shapez",
        "igdb_name": "shapez",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "simulator",
            "strategy",
            "indie"
        ],
        "themes": [
            "sandbox"
        ],
        "platforms": [
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "base building"
        ],
        "release_date": "2020"
    },
    "shivers": {
        "igdb_id": "12477",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7a5z.jpg",
        "game_name": "Shivers",
        "igdb_name": "shivers",
        "rating": [
            "realistic blood and gore",
            "realistic blood"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "point-and-click",
            "puzzle",
            "adventure",
            "indie"
        ],
        "themes": [
            "horror"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "1995"
    },
    "shorthike": {
        "igdb_id": "116753",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co6e83.jpg",
        "game_name": "A Short Hike",
        "igdb_name": "a short hike",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy",
            "open world"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "the main character is claire, a young anthropomorphic bird who travels to hawk peak provincial park, where her aunt may works as a ranger, to spend days off. however, claire cannot get cellphone reception unless she reaches the top of the peak, and is expecting an important call. for this reason, she decides to reach the highest point in the park.",
        "keywords": [
            "exploration",
            "casual",
            "fishing",
            "female protagonist",
            "flight",
            "bird",
            "cute",
            "funny",
            "relaxing",
            "3d platformer",
            "family friendly",
            "great soundtrack"
        ],
        "release_date": "2019"
    },
    "simpsonshitnrun": {
        "igdb_id": "2844",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2uk7.jpg",
        "game_name": "The Simpsons Hit And Run",
        "igdb_name": "the simpsons: hit & run",
        "rating": [
            "comic mischief",
            "mild language",
            "violence",
            "crude humor",
            "alcohol reference",
            "cartoon violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "racing",
            "adventure"
        ],
        "themes": [
            "action",
            "comedy",
            "open world"
        ],
        "platforms": [
            "xbox",
            "nintendo gamecube",
            "pc (microsoft windows)",
            "playstation 2"
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
            "useable vehicles",
            "stat tracking",
            "destructible environment",
            "punctuation mark above head",
            "been here before",
            "tie-in",
            "spiky-haired protagonist",
            "fireworks",
            "lgbtq+"
        ],
        "release_date": "2003"
    },
    "sims4": {
        "igdb_id": "3212",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3h3l.jpg",
        "game_name": "The Sims 4",
        "igdb_name": "the sims 4",
        "rating": [
            "sexual themes",
            "crude humor",
            "violence"
        ],
        "player_perspectives": [
            "first person",
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "simulator"
        ],
        "themes": [
            "action",
            "fantasy",
            "comedy",
            "sandbox",
            "romance"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "mac",
            "xbox one"
        ],
        "storyline": "choose how sims look, act, and dress. determine how they\u2019ll live out each day. design and build incredible homes for every family, then decorate with your favorite furnishings and d\u00e9cor. travel to different neighborhoods where you can meet other sims and learn about their lives. discover beautiful locations with distinctive environments, and go on spontaneous adventures. manage the ups and downs of sims\u2019 everyday lives and see what happens when you play out realistic or fantastical scenarios. tell your stories your way while developing relationships, pursuing careers and life aspirations, and immersing yourself in an extraordinary game where the possibilities are endless.",
        "keywords": [
            "casual",
            "management",
            "cute",
            "funny",
            "relaxing",
            "family friendly",
            "lgbtq+",
            "you can pet the dog"
        ],
        "release_date": "2014"
    },
    "sly1": {
        "igdb_id": "1798",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1p0r.jpg",
        "game_name": "Sly Cooper and the Thievius Raccoonus",
        "igdb_name": "sly cooper and the thievius raccoonus",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "stealth",
            "comedy"
        ],
        "platforms": [
            "playstation 2"
        ],
        "storyline": "sly cooper comes from a long line of master thieves (the cooper clan) who only steal from other criminals, thus making them vigilantes. the cooper family's heirloom, an ancient book by the name the thievius raccoonus, records all the secret moves and techniques from every member in the clan. on his 8th birthday, sly was supposed to inherit the book and learn all of his family's ancient secrets which was supposed to help him become a master thief, however, a group of thugs by the name \"the fiendish five\" (led by clockwerk, who is the arch-nemesis of the family clan) attack the cooper household and kills sly's parents and stole all of the pages from the thievius raccoonus. after that, the ruthless gang go their separate ways to commit dastardly crimes around the world. sly is sent to an orphanage where he meets and teams up and forms a gang with two guys who become his lifelong best friends, bentley, a technician, inventor and a talented mathematical hacker with encyclopedic knowledge who plays the role as the brains of the gang, and murray, a huge husky cowardly guy with a ginormous appetite who plays the role as the brawns and the getaway driver of the gang. the three leave the orphanage together at age 16 to start their lives becoming international vigilante criminals together, naming themselves \"the cooper gang\". sly swears one day to avenge his family and track down the fiendish five and steal back the thievius raccoonus. two years later, the cooper gang head to paris, france, to infiltrate itnerpol (a police headquarters) in order to find the secret police file which stores details and information about the fiendish five but during the heist they are ambushed by inspector carmelita fox (towards whom sly develops a romantic attraction), a police officer who is affiliated with interpol and is after the cooper gang. the gang manage to steal the police file and successfully escapes from her and the rest of the cops. with the secret police file finally in their hands, the cooper gang manage to track down the fiendish five.",
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
            "crocodile",
            "language selection",
            "polygonal 3d",
            "skeletons",
            "descendants of other characters",
            "checkpoints",
            "unstable platforms",
            "stereoscopic 3d",
            "melee",
            "moving platforms",
            "destructible environment",
            "gliding",
            "invisibility",
            "time trials",
            "fireworks"
        ],
        "release_date": "2002"
    },
    "sm": {
        "igdb_id": "1103",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5osy.jpg",
        "game_name": "Super Metroid",
        "igdb_name": "super metroid",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "thriller"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "after samus completed her mission and eradicated the entire metroid population on sr388 as commanded by the galactic federation (sans the metroid hatchling, which she nicknamed \"baby\"), she brought the hatchling to the ceres space colony for research. however, shortly after she left, she received a distress signal from the station and returned to investigate.\n\nwhen samus arrives at the space science academy where the baby was being studied, she finds all the scientists slaughtered and the containment unit that held the baby missing. upon further exploration of the station, she finds the baby in a small capsule. as she approaches, ridley appears and grabs the capsule. after a brief battle, samus repels ridley, and he activates a self-destruct sequence to destroy ceres.\n\nafter escaping the explosion, ridley flees to zebes, and samus goes after him.",
        "keywords": [
            "aliens",
            "exploration",
            "2d",
            "16-bit",
            "metroidvania",
            "time manipulation",
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
            "liberation",
            "mercenary",
            "sequence breaking",
            "isolation",
            "interconnected-world"
        ],
        "release_date": "1994"
    },
    "sm64ex": {
        "igdb_id": "1074",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co721v.jpg",
        "game_name": "Super Mario 64",
        "igdb_name": "super mario 64",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "\u201cmario, please come to the castle. i've baked a cake for you. yours truly, princess toadstool.\u201d\n\n\u201cwow, an invitation from peach! i'll head out right away. i hope she can wait for me!\u201d\n\nmario is so excited to receive the invitation from the princess, who lives in the mushroom castle that he quickly dresses in his best and leaves right away.\n\n\u201chmmm, something's not quite right here... it's so quiet...\u201d\n\nshaking off his uneasy premonition, mario steps into the silent castle, where he is greeted by the gruff words, \u201cno one's home! now scram! bwa, ha, ha.\u201d\n\nthe sound seems to come from everywhere.\n\n\u201cwho's there?! i've heard that voice somewhere before...\u201d\n\nmario begins searching all over the castle. most of the doors are locked, but finding one open, he peeks inside. hanging on the wall is the largest painting he has ever seen, and from behind the painting comes the strangest sound that he has ever heard...\n\n\u201ci think i hear someone calling. what secrets does this painting hold?\u201d\n\nwithout a second thought, mario jumps at the painting. as he is drawn into it, another world opens before his very eyes.\n\nonce inside the painting, mario finds himself in the midst of battling bob-ombs. according to the bob-omb buddies, someone...or something...has suddenly attacked the castle and stolen the \u201cpower stars.\u201d these stars protect the castle. with the stars in his control, the beast plans to take over the mushroom castle.\n\nto help him accomplish this, he plans to convert the residents of the painting world into monsters as well. if nothing is done, all those monsters will soon begin to overflow from inside the painting.\n\n\u201ca plan this maniacal, this cunning...this must be the work of bowser!\u201d\n\nprincess toadstool and toad are missing, too. bowser must have taken them and sealed them inside the painting. unless mario recovers the power stars immediately, the inhabitants of this world will become bowser's army.\n\n\u201cwell, bowser's not going to get away with it, not as long as i'm around!\u201d\n\nstolen power stars are hidden throughout the painting world. use your wisdom and strength to recover the power stars and restore peace to the mushroom castle.\n\n\u201cmario! you are the only one we can count on.\u201d",
        "keywords": [
            "rabbit",
            "3d platformer",
            "swimming",
            "snowman",
            "digital distribution",
            "super-ness",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "linear gameplay",
            "wiggler",
            "entering world in a painting",
            "retroachievements",
            "princess peach"
        ],
        "release_date": "1996"
    },
    "sm64hacks": {
        "igdb_id": "1074",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co721v.jpg",
        "game_name": "SM64 Romhack",
        "igdb_name": "super mario 64",
        "rating": [],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "\u201cmario, please come to the castle. i've baked a cake for you. yours truly, princess toadstool.\u201d\n\n\u201cwow, an invitation from peach! i'll head out right away. i hope she can wait for me!\u201d\n\nmario is so excited to receive the invitation from the princess, who lives in the mushroom castle that he quickly dresses in his best and leaves right away.\n\n\u201chmmm, something's not quite right here... it's so quiet...\u201d\n\nshaking off his uneasy premonition, mario steps into the silent castle, where he is greeted by the gruff words, \u201cno one's home! now scram! bwa, ha, ha.\u201d\n\nthe sound seems to come from everywhere.\n\n\u201cwho's there?! i've heard that voice somewhere before...\u201d\n\nmario begins searching all over the castle. most of the doors are locked, but finding one open, he peeks inside. hanging on the wall is the largest painting he has ever seen, and from behind the painting comes the strangest sound that he has ever heard...\n\n\u201ci think i hear someone calling. what secrets does this painting hold?\u201d\n\nwithout a second thought, mario jumps at the painting. as he is drawn into it, another world opens before his very eyes.\n\nonce inside the painting, mario finds himself in the midst of battling bob-ombs. according to the bob-omb buddies, someone...or something...has suddenly attacked the castle and stolen the \u201cpower stars.\u201d these stars protect the castle. with the stars in his control, the beast plans to take over the mushroom castle.\n\nto help him accomplish this, he plans to convert the residents of the painting world into monsters as well. if nothing is done, all those monsters will soon begin to overflow from inside the painting.\n\n\u201ca plan this maniacal, this cunning...this must be the work of bowser!\u201d\n\nprincess toadstool and toad are missing, too. bowser must have taken them and sealed them inside the painting. unless mario recovers the power stars immediately, the inhabitants of this world will become bowser's army.\n\n\u201cwell, bowser's not going to get away with it, not as long as i'm around!\u201d\n\nstolen power stars are hidden throughout the painting world. use your wisdom and strength to recover the power stars and restore peace to the mushroom castle.\n\n\u201cmario! you are the only one we can count on.\u201d",
        "keywords": [
            "rabbit",
            "3d platformer",
            "swimming",
            "snowman",
            "digital distribution",
            "super-ness",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "linear gameplay",
            "wiggler",
            "entering world in a painting",
            "retroachievements",
            "princess peach"
        ],
        "release_date": "1996"
    },
    "smo": {
        "igdb_id": "26758",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1mxf.jpg",
        "game_name": "Super Mario Odyssey",
        "igdb_name": "super mario odyssey",
        "rating": [
            "cartoon violence",
            "comic mischief"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "nintendo switch 2",
            "nintendo switch"
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
            "2d platformer",
            "alternate costumes",
            "motion control",
            "deliberately retro",
            "checkpoints",
            "underwater gameplay",
            "wiggler",
            "behind the waterfall",
            "entering world in a painting",
            "beach"
        ],
        "release_date": "2017"
    },
    "sms": {
        "igdb_id": "1075",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co21rh.jpg",
        "game_name": "Super Mario Sunshine",
        "igdb_name": "super mario sunshine",
        "rating": [
            "comic mischief"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "sandbox"
        ],
        "platforms": [
            "nintendo gamecube"
        ],
        "storyline": "close your eyes and imagine\u2026soothing sunshine accompanied by the sound of waves gently breaking on the shore. high above, seagulls turn lazy circles in a clear blue sky. this is isle delfino.\n\nfar from the hustle and bustle of the mushroom kingdom, this island resort glitters like a gem in the waters of a southern sea.\n\nmario, peach, and an entourage of toads have come to isle delfino to relax and unwind. at least, that\u2019s their plan\u2026but when they arrive, they find things have gone horribly wrong...\n\naccording to the island inhabitants, the person responsible for the mess has a round nose, a thick mustache, and a cap\u2026\n\nwhat? but\u2026that sounds like mario!!\n\nthe islanders are saying that mario's mess has polluted the island and caused their energy source, the shine sprites, to vanish.\n\nnow the falsely accused mario has promised to clean up the island, but...how?\n\nnever fear! fludd, the latest invention from gadd science, inc., can help mario tidy up the island, take on baddies, and lend a nozzle in all kinds of sticky situations.\n\ncan mario clean the island, capture the villain, and clear his good name? it\u2019s time for another mario adventure to get started!",
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
            "yoshi",
            "3d platformer",
            "climbing",
            "swimming",
            "mario",
            "turtle",
            "explosion",
            "anthropomorphism",
            "super-ness",
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
            "male antagonist",
            "violent plants",
            "moving platforms",
            "been here before",
            "water level",
            "sleeping",
            "tentacles",
            "boss assistance",
            "linear gameplay",
            "gliding",
            "kidnapping",
            "italian accent",
            "wiggler",
            "foreshadowing",
            "collection marathon",
            "retroachievements",
            "princess peach",
            "beach"
        ],
        "release_date": "2002"
    },
    "smw": {
        "igdb_id": "1070",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8lo8.jpg",
        "game_name": "Super Mario World",
        "igdb_name": "super mario world",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "arcade",
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "mario is having a vacation in dinosaur land when he learns that princess peach toadstool has been kidnapped by the evil king koopa bowser. when mario starts searching for her he finds a giant egg with a dinosaur named yoshi hatching out of it. yoshi tells mario that his fellow dinosaurs have been imprisoned in eggs by bowser's underlings. the intrepid plumber has to travel to their castles, rescue the dinosaurs, and eventually face king koopa himself, forcing him to release the princess.",
        "keywords": [
            "dinosaurs",
            "princess",
            "yoshi",
            "mario",
            "digital distribution",
            "bonus stage",
            "damsel in distress",
            "retroachievements"
        ],
        "release_date": "1990"
    },
    "smz3": {
        "igdb_id": "210231",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5zep.jpg",
        "game_name": "SMZ3",
        "igdb_name": "super metroid and a link to the past crossover randomizer",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "open world"
        ],
        "platforms": [
            "super nintendo entertainment system"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2018"
    },
    "sm_map_rando": {
        "igdb_id": "1103",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5osy.jpg",
        "game_name": "Super Metroid Map Rando",
        "igdb_name": "super metroid",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "thriller"
        ],
        "platforms": [
            "super nintendo entertainment system",
            "wii",
            "wii u",
            "new nintendo 3ds",
            "super famicom"
        ],
        "storyline": "after samus completed her mission and eradicated the entire metroid population on sr388 as commanded by the galactic federation (sans the metroid hatchling, which she nicknamed \"baby\"), she brought the hatchling to the ceres space colony for research. however, shortly after she left, she received a distress signal from the station and returned to investigate.\n\nwhen samus arrives at the space science academy where the baby was being studied, she finds all the scientists slaughtered and the containment unit that held the baby missing. upon further exploration of the station, she finds the baby in a small capsule. as she approaches, ridley appears and grabs the capsule. after a brief battle, samus repels ridley, and he activates a self-destruct sequence to destroy ceres.\n\nafter escaping the explosion, ridley flees to zebes, and samus goes after him.",
        "keywords": [
            "aliens",
            "exploration",
            "2d",
            "16-bit",
            "metroidvania",
            "time manipulation",
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
            "liberation",
            "mercenary",
            "sequence breaking",
            "isolation",
            "interconnected-world"
        ],
        "release_date": "1994"
    },
    "soe": {
        "igdb_id": "1359",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8kz6.jpg",
        "game_name": "Secret of Evermore",
        "igdb_name": "secret of evermore",
        "rating": [
            "mild animated violence"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)"
        ],
        "themes": [
            "action",
            "science fiction",
            "historical"
        ],
        "platforms": [
            "super nintendo entertainment system"
        ],
        "storyline": "in dr. sidney ruffleberg's old, decaying mansion, a boy and his dog stumble upon a mysterious machine. by sheer accident they are propelled into evermore, a one-time utopia that now has become a confounding and deadly world. a world of prehistoric jungles, ancient civilizations, medieval kingdoms and futuristic cities. during his odyssey, the boy must master a variety of weapons, learn to harness the forces of alchemy, and make powerful allies to battle evermore's diabolical monsters. what's more, his dog masters shape-changing to aid the quest. but even if they can muster enough skill and courage, even if they can uncover the mysterious clues, they can only find their way home by discovering the secret of evermore.",
        "keywords": [
            "medieval",
            "futuristic",
            "dog",
            "giant insects",
            "sprinting mechanics",
            "mana",
            "ambient music"
        ],
        "release_date": "1995"
    },
    "sonic_heroes": {
        "igdb_id": "4156",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9olx.jpg",
        "game_name": "Sonic Heroes",
        "igdb_name": "sonic heroes",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "platform",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "xbox",
            "nintendo gamecube",
            "pc (microsoft windows)",
            "playstation 2"
        ],
        "storyline": "dr. eggman has come back to challenge sonic and crew again to defeat his new scheme. sonic the hedgehog, miles \"tails\" prower, and knuckles the echidna gladly accept and race off to tackle the doctor's latest plan. meanwhile, rouge the bat swings in on one of eggman's old fortresses and discovers shadow the hedgehog encapsuled. after an odd encounter, rouge, shadow, and e-123 omega join up to find out what happened to shadow and to get revenge on eggman.\nat a resort, amy rose looks at an ad that shows sonic in it with chocola and froggy, cheese's and big's best friends respectively. after getting over boredom, amy, cream the rabbit, and big the cat decide to find sonic and get what they want back. elsewhere, in a run down building, the chaotix detective agency receive a package that contains a walkie-talkie. tempting them, vector the crocodile, espio the chameleon and charmy bee decide to work for this mysterious person, so they can earn some money.",
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
            "spiky-haired protagonist",
            "on-the-fly character switching",
            "retroachievements"
        ],
        "release_date": "2003"
    },
    "sotn": {
        "igdb_id": "1128",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co53m8.jpg",
        "game_name": "Symphony of the Night",
        "igdb_name": "castlevania: symphony of the night",
        "rating": [
            "animated blood and gore",
            "animated violence",
            "violence",
            "blood and gore",
            "cartoon violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "horror",
            "open world"
        ],
        "platforms": [
            "playstation 3",
            "playstation",
            "playstation portable",
            "xbox 360"
        ],
        "storyline": "the game's story takes place during the year 1797, 5 years after the events of rondo of blood and begins with richter belmont's defeat of count dracula, mirroring the end of the former game. however, despite dracula being defeated, richter vanishes without a trace. castlevania rises again five years later, and while there are no belmonts to storm the castle, alucard, the son of dracula, awakens from his self-induced sleep, and decides to investigate what transpired during his slumber.\n\nmeanwhile, maria renard, richter's sister-in-law, enters castlevania herself to search for the missing richter. she assists alucard multiple times throughout the game.",
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
            "wolf",
            "nudity",
            "bats",
            "day/night cycle",
            "explosion",
            "digital distribution",
            "leveling up",
            "human",
            "polygonal 3d",
            "psone classics",
            "shopping",
            "skeletons",
            "descendants of other characters",
            "save point",
            "melee",
            "real-time combat",
            "a.i. companion",
            "secret area",
            "rock music",
            "rpg elements",
            "moving platforms",
            "sequence breaking",
            "villain",
            "shape-shifting",
            "speedrun",
            "villain turned good",
            "over 100% completion",
            "completion percentage",
            "meme origin",
            "androgyny",
            "creature compendium",
            "behind the waterfall",
            "isolation",
            "interconnected-world"
        ],
        "release_date": "1997"
    },
    "spire": {
        "igdb_id": "296831",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co82c5.jpg",
        "game_name": "Slay the Spire",
        "igdb_name": "slay the spire ii",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "strategy",
            "indie",
            "card & board game"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [
            "roguelike"
        ],
        "release_date": ""
    },
    "spyro3": {
        "igdb_id": "1578",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7t4m.jpg",
        "game_name": "Spyro 3",
        "igdb_name": "spyro: year of the dragon",
        "rating": [
            "comic mischief"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "comedy"
        ],
        "platforms": [
            "playstation 3",
            "playstation",
            "playstation portable"
        ],
        "storyline": "the game follows the titular purple dragon spyro as he travels to the forgotten worlds after 150 magical dragon eggs are stolen from the land of the dragons by an evil sorceress.",
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
            "psone classics",
            "game reference",
            "cameo appearance",
            "auto-saving",
            "real-time combat",
            "moving platforms",
            "gliding",
            "time trials"
        ],
        "release_date": "2000"
    },
    "ss": {
        "igdb_id": "534",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5wrj.jpg",
        "game_name": "Skyward Sword",
        "igdb_name": "the legend of zelda: skyward sword",
        "rating": [
            "fantasy violence",
            "animated blood",
            "comic mischief"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "historical",
            "open world"
        ],
        "platforms": [
            "wii",
            "wii u"
        ],
        "storyline": "born on an island suspended in the sky, a young man called link accepts his destiny to venture to the world below to save his childhood friend zelda after being kidnapped and brought to an abandoned land.",
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
            "motion control",
            "potion",
            "auto-aim",
            "real-time combat",
            "mercenary",
            "violent plants",
            "mine cart sequence",
            "androgyny",
            "ancient advanced civilization technology",
            "context sensitive",
            "living inventory",
            "behind the waterfall",
            "monomyth"
        ],
        "release_date": "2011"
    },
    "stardew_valley": {
        "igdb_id": "17000",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa93h.jpg",
        "game_name": "Stardew Valley",
        "igdb_name": "stardew valley",
        "rating": [
            "fantasy violence",
            "mild blood",
            "mild language",
            "simulated gambling",
            "use of tobacco",
            "use of alcohol",
            "use of alcohol and tobacco"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "role-playing (rpg)",
            "simulator",
            "strategy",
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy",
            "business",
            "sandbox",
            "romance"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "wii u",
            "playstation vita",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "you\u2019ve inherited your grandfather\u2019s old farm plot in stardew valley. armed with hand-me-down tools and a few coins, you set out to begin your new life. can you learn to live off the land and turn these overgrown fields into a thriving home? it won\u2019t be easy. ever since joja corporation came to town, the old ways of life have all but disappeared. the community center, once the town\u2019s most vibrant hub of activity, now lies in shambles. but the valley seems full of opportunity. with a little dedication, you might just be the one to restore stardew valley to greatness!",
        "keywords": [
            "monsters",
            "animals",
            "sword",
            "minigames",
            "2d",
            "fishing",
            "crafting",
            "chicken",
            "fairy",
            "achievements",
            "pixel art",
            "snow",
            "relaxing",
            "mining",
            "day/night cycle",
            "customizable characters",
            "deliberately retro",
            "controller support",
            "beach"
        ],
        "release_date": "2016"
    },
    "star_fox_64": {
        "igdb_id": "2591",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2e4k.jpg",
        "game_name": "Star Fox 64",
        "igdb_name": "star fox 64",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "shooter"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "wii",
            "nintendo 64",
            "wii u"
        ],
        "storyline": "mad scientist andross arises as the emperor of venom and declares war on the entire lylat system, starting with corneria. general pepper sends in the star fox team to protect the key planets of the lylat system and stop dr. andross.",
        "keywords": [
            "gravity",
            "death",
            "robots",
            "frog",
            "spaceship",
            "flight",
            "multiple endings",
            "artificial intelligence",
            "wolf",
            "dog",
            "talking animals",
            "anthropomorphism",
            "voice acting",
            "polygonal 3d",
            "descendants of other characters",
            "a.i. companion",
            "secret area",
            "difficulty level",
            "villain",
            "auto-scrolling levels",
            "meme origin",
            "retroachievements"
        ],
        "release_date": "1997"
    },
    "subnautica": {
        "igdb_id": "9254",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coa938.jpg",
        "game_name": "Subnautica",
        "igdb_name": "subnautica",
        "rating": [
            "mild language",
            "fantasy violence"
        ],
        "player_perspectives": [
            "first person",
            "virtual reality"
        ],
        "genres": [
            "adventure",
            "indie"
        ],
        "themes": [
            "science fiction",
            "survival",
            "open world"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "android",
            "pc (microsoft windows)",
            "ios",
            "steamvr",
            "playstation 5",
            "mac",
            "oculus rift",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "you have crash-landed on an alien ocean world, and the only way to go is down. subnautica's oceans range from sun drenched shallow coral reefs to treacherous deep-sea trenches, lava fields, and bio-luminescent underwater rivers. manage your oxygen supply as you explore kelp forests, plateaus, reefs, and winding cave systems. the water teems with life: some of it helpful, much of it harmful.\n\nafter crash landing in your life pod, the clock is ticking to find water, food, and to develop the equipment you need to explore. collect resources from the ocean around you. craft diving gear, lights, habitat modules, and submersibles. venture deeper and further form to find rarer resources, allowing you to craft more advanced items.",
        "keywords": [
            "exploration",
            "swimming",
            "underwater gameplay"
        ],
        "release_date": "2018"
    },
    "swr": {
        "igdb_id": "154",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3wj7.jpg",
        "game_name": "Star Wars Episode I Racer",
        "igdb_name": "star wars: episode i - racer",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "racing"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "playstation 4",
            "nintendo 64",
            "pc (microsoft windows)",
            "mac",
            "xbox one",
            "nintendo switch",
            "dreamcast"
        ],
        "storyline": "",
        "keywords": [
            "robots"
        ],
        "release_date": "1999"
    },
    "tboir": {
        "igdb_id": "310643",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8kxf.jpg",
        "game_name": "The Binding of Isaac Repentance",
        "igdb_name": "the binding of isaac: repentance",
        "rating": [
            "blood and gore",
            "crude humor",
            "violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "shooter",
            "indie"
        ],
        "themes": [],
        "platforms": [
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2021"
    },
    "terraria": {
        "igdb_id": "1879",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1rbo.jpg",
        "game_name": "Terraria",
        "igdb_name": "terraria",
        "rating": [
            "mild suggestive themes",
            "blood and gore",
            "use of alcohol",
            "cartoon violence",
            "suggestive themes",
            "violence",
            "blood",
            "alcohol reference"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "simulator",
            "strategy",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction",
            "horror",
            "survival",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "google stadia",
            "playstation 3",
            "playstation 4",
            "linux",
            "nintendo 3ds",
            "windows phone",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "wii u",
            "playstation vita",
            "xbox 360",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "exploration",
            "magic",
            "2d",
            "construction",
            "fishing",
            "crafting",
            "death",
            "procedural generation",
            "mummy",
            "rabbit",
            "flight",
            "action-adventure",
            "fairy",
            "undead",
            "pixel art",
            "snow",
            "teleportation",
            "mining",
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
            "falling damage",
            "pick your gender",
            "melee",
            "underwater gameplay",
            "violent plants",
            "merchants",
            "mana",
            "you can pet the dog",
            "bees"
        ],
        "release_date": "2011"
    },
    "tetrisattack": {
        "igdb_id": "2739",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2w6k.jpg",
        "game_name": "Tetris Attack",
        "igdb_name": "tetris attack",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "puzzle"
        ],
        "themes": [
            "action",
            "kids"
        ],
        "platforms": [
            "super nintendo entertainment system"
        ],
        "storyline": "the story mode takes place in the world of yoshi's island, where bowser and his minions have cursed all of yoshi's friends. playing as yoshi, the player must defeat each of his friends in order to remove the curse. once all friends have been freed, the game proceeds to a series of bowser's minions, and then to bowser himself. during these final matches, the player can select yoshi or any of his friends to play out the stage.",
        "keywords": [
            "retroachievements"
        ],
        "release_date": "1996"
    },
    "timespinner": {
        "igdb_id": "28952",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co24ag.jpg",
        "game_name": "Timespinner",
        "igdb_name": "timespinner",
        "rating": [
            "fantasy violence",
            "sexual themes",
            "mild language"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "playstation vita",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "with her family murdered in front of her and the ancient timespinner device destroyed, lunais is suddenly transported into a unknown world, stranded with seemingly no hope of return. using her power to control time, lunais vows to take her revenge on the evil lachiem empire, but sometimes the course of history isn\u2019t quite as black and white as it seems...",
        "keywords": [
            "time travel",
            "metroidvania",
            "time manipulation",
            "female protagonist",
            "action-adventure",
            "pixel art",
            "steam greenlight",
            "crowdfunding",
            "digital distribution",
            "deliberately retro",
            "crowd funded",
            "merchants",
            "lgbtq+"
        ],
        "release_date": "2018"
    },
    "tloz": {
        "igdb_id": "1022",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1uii.jpg",
        "game_name": "The Legend of Zelda",
        "igdb_name": "the legend of zelda",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "family computer disk system",
            "nintendo 3ds",
            "wii",
            "family computer",
            "wii u",
            "nintendo entertainment system"
        ],
        "storyline": "in one of the darkest times in the kingdom of hyrule, a young boy named link takes on an epic quest to restore the fragmented triforce of wisdom and save the princess zelda from the clutches of the evil ganon.",
        "keywords": [
            "fairy",
            "overworld",
            "meme origin",
            "retroachievements"
        ],
        "release_date": "1986"
    },
    "tloz_ooa": {
        "igdb_id": "1041",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2tw1.jpg",
        "game_name": "The Legend of Zelda - Oracle of Ages",
        "igdb_name": "the legend of zelda: oracle of ages",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "game boy color",
            "nintendo 3ds"
        ],
        "storyline": "a pall of darkness has fallen over the land of labrynna. the sorceress of shadows has captured the oracle of ages and is using her power to do evil. link has been summoned to help and must travel back and forth in time to stop the sorceress of shadows and return labrynna to its former glory.",
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
            "dancing",
            "silent protagonist",
            "climbing",
            "swimming",
            "sword & sorcery",
            "explosion",
            "block puzzle",
            "anthropomorphism",
            "shopping",
            "damsel in distress",
            "disorientation zone",
            "descendants of other characters",
            "side quests",
            "real-time combat",
            "shielded enemies",
            "walking through walls",
            "multiple gameplay perspectives",
            "conveyor belt",
            "punctuation mark above head",
            "sequence breaking",
            "villain",
            "jumping puzzle",
            "time paradox",
            "context sensitive",
            "status effects",
            "behind the waterfall",
            "plane shifting"
        ],
        "release_date": "2001"
    },
    "tloz_oos": {
        "igdb_id": "1032",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2tw0.jpg",
        "game_name": "The Legend of Zelda - Oracle of Seasons",
        "igdb_name": "the legend of zelda: oracle of seasons",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "game boy color",
            "nintendo 3ds"
        ],
        "storyline": "the land of holodrum is slowly withering. onox, the general of darkness, has imprisoned the oracle of seasons and is draining the very life out of the land. with the seasons in tumult and the forces of evil running rampant, the world looks for a hero... and finds link. his quest won't be easy - he'll have to master the seasons themselves if he's to turn back the evil tide.",
        "keywords": [
            "pirates",
            "time travel",
            "magic",
            "grinding",
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
            "portals",
            "pixel art",
            "dog",
            "teleportation",
            "silent protagonist",
            "climbing",
            "sword & sorcery",
            "block puzzle",
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
            "multiple gameplay perspectives",
            "villain",
            "fetch quests",
            "poisoning",
            "context sensitive",
            "status effects",
            "plane shifting",
            "damage over time"
        ],
        "release_date": "2001"
    },
    "tloz_ph": {
        "igdb_id": "1037",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3ocu.jpg",
        "game_name": "The Legend of Zelda - Phantom Hourglass",
        "igdb_name": "the legend of zelda: phantom hourglass",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "wii u",
            "nintendo ds"
        ],
        "storyline": "many months have passed since the events of the legend of zelda: the wind waker, and link, tetra and tetra\u2019s band of pirates have set sail in search of new lands. they come across a patch of ocean covered in a dense fog, in which they discover an abandoned ship. tetra falls into danger when she explores the ship alone, and link falls into the ocean when he attempts to rescue her. when he washes up unconscious on the shores of a mysterious island, he is awakened by the sound of a fairy\u2019s voice. with the aid of this fairy, he sets off to find tetra \u2013 and his way back to the seas he once knew.",
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
            "easy",
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
            "nameless protagonist",
            "comic relief",
            "damage over time",
            "monomyth",
            "bees"
        ],
        "release_date": "2007"
    },
    "tmc": {
        "igdb_id": "1035",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3nsk.jpg",
        "game_name": "The Minish Cap",
        "igdb_name": "the legend of zelda: the minish cap",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "nintendo 3ds",
            "wii u",
            "game boy advance"
        ],
        "storyline": "while at a festival with princess zelda, link encounters a mysterious mage called vaati who turns the princess to stone. helpless to stop them, link is asked by the king to meet with a race of tiny people known as the minish, who may be able to help with their predicament. on his travels, link teams up with a talking cap called ezlo, who is able to shrink link to the size of a minish so that he can meet with them. with his newfound abilities, link must save the kingdom from vaati's menace.",
        "keywords": [
            "ghosts",
            "magic",
            "mascot",
            "death",
            "maze",
            "mummy",
            "gambling",
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
            "language selection",
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
            "royalty",
            "potion",
            "melee",
            "grapple",
            "real-time combat",
            "secret area",
            "unbeatable enemies",
            "shielded enemies",
            "coming of age",
            "moving platforms",
            "punctuation mark above head",
            "sequence breaking",
            "villain",
            "been here before",
            "sleeping",
            "multiple enemy boss fights",
            "boss assistance",
            "fetch quests",
            "gliding",
            "poisoning",
            "resized enemy",
            "drawbridge",
            "fast traveling",
            "living inventory",
            "falling object",
            "status effects",
            "behind the waterfall",
            "foreshadowing",
            "plane shifting",
            "damage over time",
            "monomyth"
        ],
        "release_date": "2004"
    },
    "toontown": {
        "igdb_id": "25326",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co28yv.jpg",
        "game_name": "Toontown",
        "igdb_name": "toontown online",
        "rating": [
            "cartoon violence",
            "comic mischief"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)"
        ],
        "themes": [
            "comedy",
            "open world"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "toontown online's story centers on an ongoing battle between a population of cartoon animals known as the toons and a collection of business-minded robots known as the cogs who are trying to take over the town. players would choose and customize their own toon and go on to complete toontasks, play mini-games, and fight the cogs.",
        "keywords": [
            "minigames",
            "go-kart"
        ],
        "release_date": "2003"
    },
    "tp": {
        "igdb_id": "134014",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w1h.jpg",
        "game_name": "Twilight Princess",
        "igdb_name": "the legend of zelda: twilight princess",
        "rating": [
            "fantasy violence",
            "animated blood"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "wii"
        ],
        "storyline": "link, a young farm boy whose tasks consist of herding goats to watching children in ordon village, is asked by the mayor to run an errand in castle town. but things went strange that day: the land becomes dark and strange creatures appear from another world called the twilight realm which turns most people into ghosts. unlike the others, link transforms into a wolf but is captured. a mysterious figure named midna helps him break free, and with the aid of her magic, they set off to free the land from the shadows. link must explore the vast land of hyrule and uncover the mystery behind its plunge into darkness.",
        "keywords": [
            "motion control"
        ],
        "release_date": "2006"
    },
    "tracker": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Universal Tracker",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "trackmania": {
        "igdb_id": "133807",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2fe9.jpg",
        "game_name": "Trackmania",
        "igdb_name": "trackmania",
        "rating": [],
        "player_perspectives": [
            "first person",
            "third person"
        ],
        "genres": [
            "racing",
            "sport",
            "arcade"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "xbox one"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2020"
    },
    "ttyd": {
        "igdb_id": "328663",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co9p1w.jpg",
        "game_name": "Paper Mario The Thousand Year Door",
        "igdb_name": "paper mario: the thousand-year door",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "puzzle"
        ],
        "themes": [],
        "platforms": [
            "web browser"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2004"
    },
    "tunic": {
        "igdb_id": "23733",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/td1t8kb33gyo8mvhl2pc.jpg",
        "game_name": "TUNIC",
        "igdb_name": "tunic",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "xbox series x|s",
            "playstation 4",
            "pc (microsoft windows)",
            "playstation 5",
            "mac",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "tunic is an action adventure game about a small fox in a big world, who must explore the countryside, fight monsters, and discover secrets. crafted to evoke feelings of classic action adventure games, tunic will challenge the player with unique items, skillful combat techniques, and arcane mysteries as our hero forges their way through an intriguing new world.",
        "keywords": [
            "exploration",
            "sword",
            "3d",
            "difficult",
            "forest",
            "stylized",
            "achievements",
            "cute",
            "atmospheric",
            "family friendly",
            "great soundtrack",
            "digital distribution",
            "anthropomorphism",
            "secret area",
            "controller support",
            "soulslike"
        ],
        "release_date": "2022"
    },
    "tww": {
        "igdb_id": "1033",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3ohz.jpg",
        "game_name": "The Wind Waker",
        "igdb_name": "the legend of zelda: the wind waker",
        "rating": [
            "violence"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy"
        ],
        "platforms": [
            "nintendo gamecube"
        ],
        "storyline": "set hundreds of years after the events of ocarina of time, the wind waker finds the hero link living with his grandmother on the outset island, one of the many small islands lost amidst the waters of the great sea. on his tenth birthday, link encounters a giant bird carrying a girl. he rescues the girl, but as a result his own sister is taken away by the bird. the girl is a pirate captain named tetra, who agrees to help link find and rescue his sister. during the course of their journey, the two of them realize that a powerful, legendary evil is active again, and must find a way to stop him.",
        "keywords": [
            "archery",
            "action-adventure",
            "fairy",
            "day/night cycle",
            "sword & sorcery",
            "auto-aim",
            "living inventory"
        ],
        "release_date": "2002"
    },
    "tyrian": {
        "igdb_id": "14432",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2zg1.jpg",
        "game_name": "Tyrian",
        "igdb_name": "tyrian 2000",
        "rating": [
            "animated violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "shooter",
            "arcade"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac",
            "dos"
        ],
        "storyline": "",
        "keywords": [
            "pixel art"
        ],
        "release_date": "1999"
    },
    "ufo50": {
        "igdb_id": "54555",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co24v0.jpg",
        "game_name": "UFO 50",
        "igdb_name": "ufo 50",
        "rating": [
            "blood",
            "violence",
            "simulated gambling",
            "use of drugs"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "puzzle",
            "role-playing (rpg)",
            "strategy",
            "adventure",
            "indie",
            "arcade"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "nintendo switch"
        ],
        "storyline": "",
        "keywords": [
            "digital distribution",
            "deliberately retro"
        ],
        "release_date": "2024"
    },
    "ultrakill": {
        "igdb_id": "124333",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co46s3.jpg",
        "game_name": "ULTRAKILL",
        "igdb_name": "ultrakill",
        "rating": [
            "violence",
            "blood and gore"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter",
            "platform",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "mankind has gone extinct and the only beings left on earth are machines fueled by blood.\nbut now that blood is starting to run out on the surface...\n\nmachines are racing to the depths of hell in search of more.",
        "keywords": [
            "bloody",
            "robots",
            "stylized",
            "silent protagonist",
            "great soundtrack",
            "robot protagonist",
            "rock music"
        ],
        "release_date": "2020"
    },
    "undertale": {
        "igdb_id": "12517",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2855.jpg",
        "game_name": "Undertale",
        "igdb_name": "undertale",
        "rating": [
            "mild blood",
            "mild language",
            "use of tobacco",
            "simulated gambling",
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "role-playing (rpg)",
            "turn-based strategy (tbs)",
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy",
            "horror",
            "comedy",
            "drama"
        ],
        "platforms": [
            "playstation 4",
            "linux",
            "pc (microsoft windows)",
            "mac",
            "playstation vita",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "\"a long time ago, two races ruled peacefully over the earth: humans and monsters. one day, a terrible war broke out between the two races. after a long battle, the humans were victorious. they sealed the monsters underground with a magical spell.\n\nin the year 201x, a small child scales mt. ebott. it is said that those who climb the mountain never return.\n\nseeking refuge from the rainy weather, the child enters a cave and discovers an enormous hole.\n\nmoving closer to get a better look... the child falls in.\n\nnow, our story begins.\"",
        "keywords": [
            "retro",
            "psychological horror",
            "dark",
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
        "release_date": "2015"
    },
    "v6": {
        "igdb_id": "1990",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4ieg.jpg",
        "game_name": "VVVVVV",
        "igdb_name": "vvvvvv",
        "rating": [
            "mild fantasy violence",
            "mild language"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure",
            "indie",
            "arcade"
        ],
        "themes": [
            "action",
            "fantasy",
            "science fiction"
        ],
        "platforms": [
            "playstation 4",
            "ouya",
            "linux",
            "nintendo 3ds",
            "android",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "playstation vita",
            "nintendo switch"
        ],
        "storyline": "a spaceship with six crew members - viridian, victoria, vitellary, vermillion, verdigris, and violet - suddenly encountered mysterious trouble while underway.\nthe group escapes by means of a teleportation device, but for some reason all the crew members are sent to different places.\nviridian, the protagonist, must find the other crew members and escape from this mysterious labyrinth...",
        "keywords": [
            "ghosts",
            "exploration",
            "retro",
            "gravity",
            "2d",
            "metroidvania",
            "death",
            "spaceship",
            "space",
            "achievements",
            "pixel art",
            "teleportation",
            "2d platformer",
            "digital distribution",
            "world map",
            "deliberately retro",
            "save point",
            "checkpoints",
            "unstable platforms",
            "stereoscopic 3d",
            "instant kill",
            "moving platforms",
            "auto-scrolling levels",
            "time trials",
            "controller support",
            "conversation"
        ],
        "release_date": "2010"
    },
    "wargroove": {
        "igdb_id": "27441",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4hgb.jpg",
        "game_name": "Wargroove",
        "igdb_name": "wargroove",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "strategy",
            "turn-based strategy (tbs)",
            "tactical",
            "indie"
        ],
        "themes": [
            "fantasy",
            "warfare"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "wargroove is a modern take on the simple yet deep turn-based tactical gameplay popularised in the 2000s by handheld games such as advance wars. as big fans of those games we were disappointed to find that nothing in this genre was available on current generation platforms and set out to fill the gap ourselves. wargroove aims to recreate the charm and accessibility of the titles that inspired it whilst bringing modern technology into the formula. this modern focus allows for higher resolution pixel art, robust online play and deep modding capability, ultimately creating the most complete experience for advance wars and tbs fans.",
        "keywords": [
            "pixel art"
        ],
        "release_date": "2019"
    },
    "wargroove2": {
        "igdb_id": "241149",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co731u.jpg",
        "game_name": "Wargroove 2",
        "igdb_name": "wargroove 2",
        "rating": [
            "fantasy violence"
        ],
        "player_perspectives": [
            "bird view / isometric",
            "side view"
        ],
        "genres": [
            "role-playing (rpg)",
            "strategy",
            "turn-based strategy (tbs)",
            "indie"
        ],
        "themes": [
            "fantasy",
            "warfare"
        ],
        "platforms": [
            "xbox series x|s",
            "pc (microsoft windows)",
            "xbox one",
            "nintendo switch"
        ],
        "storyline": "three years have passed since queen mercia and her allies defeated the ancient adversaries and restored peace to aurania. now, an ambitious foreign faction is unearthing forbidden technologies that could have catastrophic consequences for the land and its people. battle your way through 3 campaigns following 1 interweaving story. only bold decisions, smart resourcing, and tactical know-how can repair a fractured realm\u2026",
        "keywords": [
            "pirates"
        ],
        "release_date": "2023"
    },
    "witness": {
        "igdb_id": "5601",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3hih.jpg",
        "game_name": "The Witness",
        "igdb_name": "the witness",
        "rating": [
            "alcohol reference"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "puzzle",
            "adventure",
            "indie"
        ],
        "themes": [
            "science fiction",
            "open world",
            "mystery"
        ],
        "platforms": [
            "playstation 4",
            "pc (microsoft windows)",
            "ios",
            "mac",
            "xbox one"
        ],
        "storyline": "you wake up, alone, on a strange island full of puzzles that will challenge and surprise you.\n\nyou don't remember who you are, and you don't remember how you got here, but there's one thing you can do: explore the island in hope of discovering clues, regaining your memory, and somehow finding your way home.",
        "keywords": [
            "exploration",
            "procedural generation",
            "maze",
            "backtracking",
            "time limit",
            "multiple endings",
            "amnesia",
            "easy",
            "darkness",
            "digital distribution",
            "voice acting",
            "bink video",
            "polygonal 3d",
            "pop culture reference",
            "game reference",
            "auto-saving",
            "useable vehicles",
            "stat tracking",
            "secret area"
        ],
        "release_date": "2016"
    },
    "wl": {
        "igdb_id": "1072",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co216h.jpg",
        "game_name": "Wario Land",
        "igdb_name": "wario land: super mario land 3",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "nintendo 3ds",
            "game boy"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "1994"
    },
    "wl4": {
        "igdb_id": "1699",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1wpx.jpg",
        "game_name": "Wario Land 4",
        "igdb_name": "wario land 4",
        "rating": [
            "comic mischief"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action"
        ],
        "platforms": [
            "nintendo 3ds",
            "wii u",
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [
            "ghosts",
            "anime",
            "minigames",
            "flight",
            "time limit",
            "multiple endings",
            "portals",
            "pixel art",
            "sequel",
            "swimming",
            "digital distribution",
            "countdown timer",
            "cat",
            "sprinting mechanics",
            "ice stage",
            "melee",
            "unbeatable enemies",
            "moving platforms",
            "sequence breaking",
            "sliding down ladders"
        ],
        "release_date": "2001"
    },
    "wordipelago": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Wordipelago",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "xenobladex": {
        "igdb_id": "2366",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1nwh.jpg",
        "game_name": "Xenoblade X",
        "igdb_name": "xenoblade chronicles x",
        "rating": [
            "suggestive themes",
            "use of alcohol",
            "language",
            "violence",
            "animated blood"
        ],
        "player_perspectives": [
            "third person"
        ],
        "genres": [
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction",
            "sandbox",
            "open world"
        ],
        "platforms": [
            "wii u"
        ],
        "storyline": "xenoblade chronicles x opens as humanity, warned of its impending destruction in the crossfire between two warring alien races, constructs interstellar arks to escape earth. however, only a few arks escape the destruction, including the white whale ark. two years after launching, the white whale is attacked and transported to mira. during the crash-landing, the lifehold\u2014a device containing the majority of the human colonists\u2014is separated from the white whale, with lifepods containing colonists being scattered across mira. the avatar is awoken from a lifepod by elma and brought back to new los angeles. while suffering from amnesia, the avatar joins blade, working with elma and lin to recover more lifepods and search for the lifehold. during their missions across mira, blade encounters multiple alien races, learning that those attacking them are part of the ganglion coalition, an alliance of races led by the ganglion race, who are intent on destroying humanity.",
        "keywords": [
            "aliens",
            "construction",
            "robots",
            "flight",
            "action-adventure",
            "amnesia",
            "day/night cycle",
            "spiritual successor",
            "customizable characters",
            "voice acting",
            "polygonal 3d",
            "loot gathering",
            "party system",
            "side quests",
            "real-time combat",
            "useable vehicles",
            "censored version"
        ],
        "release_date": "2015"
    },
    "yachtdice": {
        "igdb_id": "",
        "cover_url": "",
        "game_name": "Yacht Dice",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [
            "multiplayer"
        ],
        "themes": [],
        "platforms": [
            "archipelago"
        ],
        "storyline": "",
        "keywords": [
            "hints",
            "archipelago",
            "multiworld"
        ],
        "release_date": ""
    },
    "yoshisisland": {
        "igdb_id": "1073",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kn9.jpg",
        "game_name": "Yoshi's Island",
        "igdb_name": "super mario world 2: yoshi's island",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform"
        ],
        "themes": [
            "action",
            "fantasy",
            "kids"
        ],
        "platforms": [
            "satellaview",
            "super nintendo entertainment system",
            "super famicom"
        ],
        "storyline": "a stork carrying the infant mario brothers is attacked by kamek the magikoopa, who steals baby luigi and knocks baby mario out of the sky. baby mario lands on yoshi's island on the back of yoshi himself. with the help of his seven other yoshi friends, yoshi must traverse the island to safely reunite baby mario with his brother and get the babies to their parents.",
        "keywords": [
            "dinosaurs",
            "side-scrolling",
            "yoshi",
            "digital distribution",
            "kidnapping"
        ],
        "release_date": "1995"
    },
    "yugioh06": {
        "igdb_id": "49377",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7yau.jpg",
        "game_name": "Yu-Gi-Oh! 2006",
        "igdb_name": "yu-gi-oh! ultimate masters: world championship tournament 2006",
        "rating": [],
        "player_perspectives": [
            "bird view / isometric",
            "text"
        ],
        "genres": [
            "strategy",
            "turn-based strategy (tbs)",
            "card & board game"
        ],
        "themes": [
            "fantasy",
            "survival"
        ],
        "platforms": [
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [
            "monsters"
        ],
        "release_date": "2006"
    },
    "yugiohddm": {
        "igdb_id": "49211",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co5ztw.jpg",
        "game_name": "Yu-Gi-Oh! Dungeon Dice Monsters",
        "igdb_name": "yu-gi-oh! dungeon dice monsters",
        "rating": [
            "mild violence"
        ],
        "player_perspectives": [
            "first person",
            "bird view / isometric"
        ],
        "genres": [
            "puzzle",
            "strategy",
            "turn-based strategy (tbs)",
            "card & board game"
        ],
        "themes": [
            "fantasy"
        ],
        "platforms": [
            "game boy advance"
        ],
        "storyline": "dungeon dice monsters is the newest addition to the yu-gi-oh! universe. as featured in the dungeon dice monsters story arc in the animated television series, players collect and fight with dice inscribed with mystical powers and magic in order to defeat their opponents. enter a dozen different tournaments and ultimately faceoff against the scheming creator of dungeon dice monsters, duke devlin.",
        "keywords": [
            "anime",
            "language selection",
            "shopping",
            "merchants"
        ],
        "release_date": "2001"
    },
    "zelda2": {
        "igdb_id": "1025",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1uje.jpg",
        "game_name": "Zelda II: The Adventure of Link",
        "igdb_name": "zelda ii: the adventure of link",
        "rating": [
            "mild fantasy violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "adventure"
        ],
        "themes": [
            "action",
            "fantasy",
            "sandbox"
        ],
        "platforms": [
            "family computer disk system",
            "nintendo 3ds",
            "wii",
            "wii u",
            "nintendo entertainment system"
        ],
        "storyline": "several years after the events of the legend of zelda, link has just turned sixteen and discovers a strange birthmark on his hand. with the help of impa, zelda's nursemaid, link learns that this mark is the key to unlock a secret room where princess zelda lies sleeping. when young, princess zelda was given knowledge of the triforce of power which was used to rule the kingdom of hyrule, but when a magician unsuccessfully tried to find out about the triforce from zelda, he put her into an eternal sleep. in his grief, the prince placed zelda in this room hoping she may wake some day. he ordered all female children in the royal household to be named zelda from this point on, so the tragedy would not be forgotten. now, to bring princess zelda back, link must locate all the pieces of the triforce which have been hidden throughout the land.",
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
            "8-bit",
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
        "release_date": "1987"
    },
    "zillion": {
        "igdb_id": "18141",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7xxj.jpg",
        "game_name": "Zillion",
        "igdb_name": "zillion",
        "rating": [],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "platform",
            "puzzle"
        ],
        "themes": [
            "science fiction"
        ],
        "platforms": [
            "sega master system/mark iii"
        ],
        "storyline": "are you ready for the ultimate danger? you're alone, outnumbered and there's no guarantee you'll make it alive. you're j.j. your objective: secretly infiltrate the underground labyrinth of the norsa empire and steal their plans for domination. armed with the ultra speed and power of the zillion laser, your mission is complex. and sheer strength will not win this one alone. you'll need more brains than brawn in this sophisticated operation. so, how will you think your way to victory? with cunning strategy and memory to guide you successfully through the maze which awaits. where once inside, you'll find the information needed to destroy the norsas and restore peace forever.",
        "keywords": [
            "anime",
            "metroidvania",
            "action-adventure"
        ],
        "release_date": "1987"
    },
    "zork_grand_inquisitor": {
        "igdb_id": "1955",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2kql.jpg",
        "game_name": "Zork Grand Inquisitor",
        "igdb_name": "zork: grand inquisitor",
        "rating": [
            "comic mischief",
            "suggestive themes",
            "use of alcohol and tobacco"
        ],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "point-and-click",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "fantasy",
            "comedy"
        ],
        "platforms": [
            "pc (microsoft windows)",
            "mac"
        ],
        "storyline": "",
        "keywords": [
            "magic"
        ],
        "release_date": "1997"
    }
} # type: ignore

SEARCH_INDEX = {
    "popular": [
        "alttp",
        "sc2",
        "oot",
        "kh2",
        "hk",
        "sm64ex",
        "pokemon_frlg"
    ],
    "adventure": [
        "mm_recomp",
        "sadx",
        "shivers",
        "residentevil3remake",
        "pokemon_crystal",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "ahit",
        "aus",
        "osrs",
        "crosscode",
        "oribf",
        "celeste",
        "tww",
        "v6",
        "dark_souls_3",
        "mm2",
        "pokemon_frlg",
        "getting_over_it",
        "sm64ex",
        "dlcquest",
        "sm_map_rando",
        "simpsonshitnrun",
        "blasphemous",
        "noita",
        "sonic_heroes",
        "kdl3",
        "alttp",
        "ffmq",
        "bomb_rush_cyberfunk",
        "tmc",
        "stardew_valley",
        "witness",
        "zelda2",
        "timespinner",
        "cuphead",
        "earthbound",
        "shorthike",
        "sm64hacks",
        "pokemon_emerald",
        "mzm",
        "animal_well",
        "undertale",
        "sm",
        "luigismansion",
        "hk",
        "mmx3",
        "poe",
        "hylics2",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ff4fe",
        "oot",
        "sotn",
        "albw",
        "chainedechoes",
        "aquaria",
        "gstla",
        "lingo",
        "tunic",
        "smo",
        "spyro3",
        "ror1",
        "cvcotm",
        "seaofthieves",
        "kh2",
        "xenobladex",
        "enderlilies",
        "peaks_of_yore",
        "cv64",
        "ufo50",
        "ff1",
        "dkc3",
        "hcniko",
        "raft",
        "tloz",
        "terraria",
        "rac2",
        "tloz_ooa",
        "satisfactory",
        "dw1",
        "momodoramoonlitfarewell",
        "dsr",
        "smz3",
        "lego_star_wars_tcs",
        "tloz_ph",
        "dk64",
        "ladx",
        "mm3",
        "sly1",
        "banjo_tooie",
        "rogue_legacy",
        "messenger",
        "sms",
        "outer_wilds",
        "smw",
        "dark_souls_2",
        "hades",
        "minecraft",
        "faxanadu",
        "monster_sanctuary",
        "mlss",
        "tloz_oos",
        "wl4",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "dontstarvetogether",
        "ss",
        "pokemon_rb",
        "k64",
        "kh1",
        "inscryption",
        "sa2b",
        "tp",
        "adventure"
    ],
    "bird view / isometric": [
        "sms",
        "balatro",
        "diddy_kong_racing",
        "overcooked2",
        "albw",
        "chainedechoes",
        "openrct2",
        "placidplasticducksim",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "sonic_heroes",
        "wargroove2",
        "rimworld",
        "shapez",
        "hades",
        "tunic",
        "sc2",
        "ffmq",
        "mmbn3",
        "spyro3",
        "ctjot",
        "osrs",
        "factorio",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "factorio_saws",
        "tmc",
        "cuphead",
        "ufo50",
        "civ_6",
        "earthbound",
        "landstalker",
        "ff1",
        "wargroove",
        "shorthike",
        "tloz",
        "dontstarvetogether",
        "tloz_ooa",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "against_the_storm",
        "brotato",
        "pokemon_emerald",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "smz3",
        "tyrian",
        "tloz_ph",
        "undertale",
        "yugiohddm",
        "ladx",
        "adventure",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "tboir",
        "hylics2",
        "soe",
        "sims4",
        "ff4fe"
    ],
    "bird": [
        "sms",
        "balatro",
        "diddy_kong_racing",
        "overcooked2",
        "albw",
        "chainedechoes",
        "openrct2",
        "placidplasticducksim",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "sonic_heroes",
        "wargroove2",
        "rimworld",
        "shapez",
        "hades",
        "minecraft",
        "sc2",
        "ffmq",
        "mmbn3",
        "spyro3",
        "tunic",
        "aus",
        "ctjot",
        "osrs",
        "crosscode",
        "factorio",
        "stardew_valley",
        "tloz_oos",
        "factorio_saws",
        "tmc",
        "cuphead",
        "ufo50",
        "civ_6",
        "earthbound",
        "landstalker",
        "ff1",
        "dkc3",
        "wargroove",
        "shorthike",
        "tloz",
        "dontstarvetogether",
        "tloz_ooa",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "against_the_storm",
        "brotato",
        "pokemon_emerald",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "smz3",
        "tyrian",
        "tloz_ph",
        "undertale",
        "yugiohddm",
        "ladx",
        "adventure",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "tboir",
        "hylics2",
        "banjo_tooie",
        "soe",
        "sims4",
        "rogue_legacy",
        "ff4fe"
    ],
    "view": [
        "diddy_kong_racing",
        "pokemon_crystal",
        "papermario",
        "wl",
        "aus",
        "osrs",
        "crosscode",
        "marioland2",
        "civ_6",
        "oribf",
        "celeste",
        "lufia2ac",
        "v6",
        "against_the_storm",
        "brotato",
        "mm2",
        "pokemon_frlg",
        "getting_over_it",
        "dlcquest",
        "sm_map_rando",
        "blasphemous",
        "meritous",
        "sims4",
        "tetrisattack",
        "balatro",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "sonic_heroes",
        "kdl3",
        "alttp",
        "sc2",
        "ffmq",
        "tmc",
        "stardew_valley",
        "zelda2",
        "timespinner",
        "cuphead",
        "earthbound",
        "wargroove",
        "shorthike",
        "yoshisisland",
        "pokemon_emerald",
        "mzm",
        "animal_well",
        "undertale",
        "sm",
        "dungeon_clawler",
        "hk",
        "mmx3",
        "poe",
        "hylics2",
        "spire",
        "soe",
        "ff4fe",
        "sotn",
        "albw",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "aquaria",
        "dkc",
        "gstla",
        "tunic",
        "spyro3",
        "ror1",
        "cvcotm",
        "factorio",
        "dkc2",
        "enderlilies",
        "ufo50",
        "ff1",
        "dkc3",
        "tloz",
        "terraria",
        "tloz_ooa",
        "dw1",
        "momodoramoonlitfarewell",
        "smz3",
        "tloz_ph",
        "megamix",
        "ladx",
        "mm3",
        "tboir",
        "rogue_legacy",
        "messenger",
        "sms",
        "smw",
        "rimworld",
        "hades",
        "faxanadu",
        "mmbn3",
        "zillion",
        "monster_sanctuary",
        "mlss",
        "ctjot",
        "tloz_oos",
        "factorio_saws",
        "landstalker",
        "wl4",
        "dontstarvetogether",
        "pokemon_rb",
        "k64",
        "pmd_eos",
        "musedash",
        "yugioh06",
        "inscryption",
        "tyrian",
        "yugiohddm",
        "adventure",
        "ffta",
        "shapez"
    ],
    "/": [
        "sms",
        "balatro",
        "diddy_kong_racing",
        "overcooked2",
        "albw",
        "chainedechoes",
        "openrct2",
        "placidplasticducksim",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "sonic_heroes",
        "wargroove2",
        "rimworld",
        "shapez",
        "hades",
        "tunic",
        "sc2",
        "ffmq",
        "mmbn3",
        "spyro3",
        "ctjot",
        "osrs",
        "factorio",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "factorio_saws",
        "tmc",
        "cuphead",
        "ufo50",
        "civ_6",
        "earthbound",
        "landstalker",
        "ff1",
        "wargroove",
        "shorthike",
        "tloz",
        "dontstarvetogether",
        "tloz_ooa",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "against_the_storm",
        "brotato",
        "pokemon_emerald",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "smz3",
        "tyrian",
        "tloz_ph",
        "undertale",
        "yugiohddm",
        "ladx",
        "adventure",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "tboir",
        "hylics2",
        "soe",
        "sims4",
        "ff4fe"
    ],
    "isometric": [
        "sms",
        "balatro",
        "diddy_kong_racing",
        "overcooked2",
        "albw",
        "chainedechoes",
        "openrct2",
        "placidplasticducksim",
        "pokemon_crystal",
        "alttp",
        "gstla",
        "sonic_heroes",
        "wargroove2",
        "rimworld",
        "shapez",
        "hades",
        "tunic",
        "sc2",
        "ffmq",
        "mmbn3",
        "spyro3",
        "ctjot",
        "osrs",
        "factorio",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "factorio_saws",
        "tmc",
        "cuphead",
        "ufo50",
        "civ_6",
        "earthbound",
        "landstalker",
        "ff1",
        "wargroove",
        "shorthike",
        "tloz",
        "dontstarvetogether",
        "tloz_ooa",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "against_the_storm",
        "brotato",
        "pokemon_emerald",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "smz3",
        "tyrian",
        "tloz_ph",
        "undertale",
        "yugiohddm",
        "ladx",
        "adventure",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "tboir",
        "hylics2",
        "soe",
        "sims4",
        "ff4fe"
    ],
    "fantasy": [
        "mm_recomp",
        "pokemon_crystal",
        "papermario",
        "ahit",
        "osrs",
        "civ_6",
        "oribf",
        "celeste",
        "tww",
        "lufia2ac",
        "v6",
        "against_the_storm",
        "dark_souls_3",
        "pokemon_frlg",
        "sm64ex",
        "blasphemous",
        "sims4",
        "noita",
        "alttp",
        "ffmq",
        "tmc",
        "stardew_valley",
        "zelda2",
        "timespinner",
        "cuphead",
        "earthbound",
        "wargroove",
        "shorthike",
        "yoshisisland",
        "sm64hacks",
        "pokemon_emerald",
        "undertale",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "spire",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ff4fe",
        "oot",
        "ultrakill",
        "albw",
        "chainedechoes",
        "wargroove2",
        "aquaria",
        "gstla",
        "tunic",
        "smo",
        "ror1",
        "huniepop",
        "dkc2",
        "kh2",
        "enderlilies",
        "seaofthieves",
        "ff1",
        "tloz",
        "terraria",
        "dsr",
        "heretic",
        "tloz_ph",
        "ladx",
        "fm",
        "banjo_tooie",
        "rogue_legacy",
        "smw",
        "dark_souls_2",
        "hades",
        "minecraft",
        "faxanadu",
        "monster_sanctuary",
        "mlss",
        "ctjot",
        "tloz_oos",
        "landstalker",
        "cat_quest",
        "ss",
        "pokemon_rb",
        "pmd_eos",
        "kh1",
        "yugioh06",
        "yugiohddm",
        "tp",
        "adventure",
        "ffta"
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
        "tetrisattack",
        "smw",
        "pokemon_crystal",
        "dkc",
        "alttp",
        "gstla",
        "kdl3",
        "papermario",
        "ffmq",
        "faxanadu",
        "mlss",
        "dkc2",
        "xenobladex",
        "zelda2",
        "earthbound",
        "ff1",
        "dkc3",
        "tloz",
        "lufia2ac",
        "yoshisisland",
        "kh1",
        "pokemon_emerald",
        "smz3",
        "sm_map_rando",
        "sm",
        "mm3",
        "adventure",
        "ffta",
        "mmx3",
        "soe",
        "ff4fe"
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
        "mm_recomp",
        "oot",
        "balatro",
        "sotn",
        "diddy_kong_racing",
        "dark_souls_2",
        "albw",
        "overcooked2",
        "dkc",
        "alttp",
        "gstla",
        "papermario",
        "hades",
        "jakanddaxter",
        "smo",
        "spyro3",
        "cvcotm",
        "mlss",
        "seaofthieves",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "enderlilies",
        "tmc",
        "witness",
        "zelda2",
        "cuphead",
        "earthbound",
        "oribf",
        "dkc3",
        "hcniko",
        "celeste",
        "tloz",
        "tww",
        "celeste64",
        "terraria",
        "ss",
        "lufia2ac",
        "tloz_ooa",
        "k64",
        "against_the_storm",
        "smz3",
        "lego_star_wars_tcs",
        "tloz_ph",
        "undertale",
        "tp",
        "simpsonshitnrun",
        "blasphemous",
        "ladx",
        "sly1",
        "ttyd",
        "spire",
        "ffta",
        "tboir",
        "banjo_tooie",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "storm": [
        "against_the_storm"
    ],
    "real time strategy (rts)": [
        "mmbn3",
        "openrct2",
        "against_the_storm",
        "rimworld",
        "sc2"
    ],
    "real": [
        "mmbn3",
        "openrct2",
        "against_the_storm",
        "rimworld",
        "sc2"
    ],
    "time": [
        "sms",
        "apeescape",
        "mk64",
        "mm_recomp",
        "oot",
        "outer_wilds",
        "diddy_kong_racing",
        "pokemon_crystal",
        "openrct2",
        "alttp",
        "rimworld",
        "sc2",
        "jakanddaxter",
        "metroidprime",
        "mmbn3",
        "ror1",
        "spyro3",
        "ctjot",
        "ahit",
        "tmc",
        "tloz_oos",
        "witness",
        "timespinner",
        "cv64",
        "earthbound",
        "wl4",
        "tloz_ooa",
        "v6",
        "pmd_eos",
        "against_the_storm",
        "pokemon_emerald",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "sly1",
        "ffta",
        "rogue_legacy"
    ],
    "strategy": [
        "balatro",
        "overcooked2",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "papermario",
        "rimworld",
        "sc2",
        "mmbn3",
        "monster_sanctuary",
        "factorio",
        "huniepop",
        "stardew_valley",
        "factorio_saws",
        "ufo50",
        "civ_6",
        "earthbound",
        "wargroove",
        "terraria",
        "dontstarvetogether",
        "pokemon_rb",
        "pmd_eos",
        "satisfactory",
        "against_the_storm",
        "huniepop2",
        "pokemon_emerald",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "undertale",
        "yugiohddm",
        "dungeon_clawler",
        "ffta",
        "hylics2",
        "fm",
        "spire",
        "shapez"
    ],
    "(rts)": [
        "mmbn3",
        "openrct2",
        "against_the_storm",
        "rimworld",
        "sc2"
    ],
    "simulator": [
        "outer_wilds",
        "doronko_wanko",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "openrct2",
        "rimworld",
        "minecraft",
        "factorio",
        "huniepop",
        "seaofthieves",
        "stardew_valley",
        "factorio_saws",
        "civ_6",
        "raft",
        "terraria",
        "dontstarvetogether",
        "satisfactory",
        "against_the_storm",
        "huniepop2",
        "getting_over_it",
        "dungeon_clawler",
        "powerwashsimulator",
        "sims4",
        "shapez"
    ],
    "indie": [
        "shivers",
        "balatro",
        "outer_wilds",
        "ultrakill",
        "noita",
        "overcooked2",
        "chainedechoes",
        "wargroove2",
        "aquaria",
        "rimworld",
        "shapez",
        "hades",
        "rogue_legacy",
        "tunic",
        "lethal_company",
        "ror1",
        "monster_sanctuary",
        "osu",
        "aus",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "factorio",
        "huniepop",
        "enderlilies",
        "factorio_saws",
        "peaks_of_yore",
        "stardew_valley",
        "timespinner",
        "witness",
        "cuphead",
        "ufo50",
        "wargroove",
        "hcniko",
        "shorthike",
        "celeste",
        "cat_quest",
        "raft",
        "ror2",
        "subnautica",
        "celeste64",
        "terraria",
        "dontstarvetogether",
        "v6",
        "satisfactory",
        "musedash",
        "against_the_storm",
        "brotato",
        "huniepop2",
        "momodoramoonlitfarewell",
        "inscryption",
        "getting_over_it",
        "animal_well",
        "dlcquest",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "hk",
        "powerwashsimulator",
        "tboir",
        "hylics2",
        "spire",
        "pseudoregalia",
        "messenger"
    ],
    "xbox series x|s": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "wargroove2",
        "hades",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "enderlilies",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "raft",
        "satisfactory",
        "against_the_storm",
        "brotato",
        "trackmania",
        "momodoramoonlitfarewell",
        "inscryption",
        "animal_well",
        "powerwashsimulator"
    ],
    "xbox": [
        "sadx",
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "sotn",
        "placidplasticducksim",
        "dark_souls_2",
        "chainedechoes",
        "overcooked2",
        "sonic_heroes",
        "wargroove2",
        "hades",
        "tunic",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "seaofthieves",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "oribf",
        "shorthike",
        "celeste",
        "raft",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "satisfactory",
        "dw1",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "momodoramoonlitfarewell",
        "inscryption",
        "trackmania",
        "sa2b",
        "dsr",
        "lego_star_wars_tcs",
        "animal_well",
        "dlcquest",
        "undertale",
        "simpsonshitnrun",
        "blasphemous",
        "hk",
        "poe",
        "powerwashsimulator",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "series": [
        "balatro",
        "doom_1993",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "wargroove2",
        "hades",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "doom_ii",
        "enderlilies",
        "residentevil2remake",
        "ror2",
        "raft",
        "subnautica",
        "satisfactory",
        "against_the_storm",
        "brotato",
        "trackmania",
        "momodoramoonlitfarewell",
        "inscryption",
        "animal_well",
        "powerwashsimulator"
    ],
    "x|s": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "wargroove2",
        "hades",
        "tunic",
        "bomb_rush_cyberfunk",
        "seaofthieves",
        "enderlilies",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "raft",
        "satisfactory",
        "against_the_storm",
        "brotato",
        "trackmania",
        "momodoramoonlitfarewell",
        "inscryption",
        "animal_well",
        "powerwashsimulator"
    ],
    "pc (microsoft windows)": [
        "sadx",
        "shivers",
        "residentevil3remake",
        "aus",
        "ahit",
        "osrs",
        "crosscode",
        "swr",
        "civ_6",
        "oribf",
        "celeste",
        "v6",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "getting_over_it",
        "dlcquest",
        "simpsonshitnrun",
        "blasphemous",
        "powerwashsimulator",
        "meritous",
        "sims4",
        "balatro",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "sonic_heroes",
        "sc2",
        "bomb_rush_cyberfunk",
        "witness",
        "stardew_valley",
        "timespinner",
        "cuphead",
        "wargroove",
        "shorthike",
        "bumpstik",
        "animal_well",
        "undertale",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "toontown",
        "spire",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ultrakill",
        "doronko_wanko",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "aquaria",
        "lingo",
        "tunic",
        "lethal_company",
        "quake",
        "ror1",
        "osu",
        "factorio",
        "huniepop",
        "seaofthieves",
        "enderlilies",
        "peaks_of_yore",
        "ufo50",
        "hcniko",
        "raft",
        "terraria",
        "satisfactory",
        "huniepop2",
        "momodoramoonlitfarewell",
        "dsr",
        "lego_star_wars_tcs",
        "heretic",
        "rogue_legacy",
        "messenger",
        "gzdoom",
        "outer_wilds",
        "dark_souls_2",
        "rimworld",
        "hades",
        "minecraft",
        "monster_sanctuary",
        "doom_ii",
        "factorio_saws",
        "landstalker",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "dontstarvetogether",
        "musedash",
        "inscryption",
        "sa2b",
        "tyrian",
        "shapez"
    ],
    "pc": [
        "sadx",
        "shivers",
        "residentevil3remake",
        "aus",
        "ahit",
        "osrs",
        "crosscode",
        "swr",
        "civ_6",
        "oribf",
        "celeste",
        "v6",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "getting_over_it",
        "dlcquest",
        "simpsonshitnrun",
        "blasphemous",
        "powerwashsimulator",
        "meritous",
        "sims4",
        "balatro",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "sonic_heroes",
        "sc2",
        "bomb_rush_cyberfunk",
        "witness",
        "stardew_valley",
        "timespinner",
        "cuphead",
        "wargroove",
        "shorthike",
        "bumpstik",
        "animal_well",
        "undertale",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "toontown",
        "spire",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ultrakill",
        "doronko_wanko",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "aquaria",
        "lingo",
        "tunic",
        "lethal_company",
        "quake",
        "ror1",
        "osu",
        "factorio",
        "huniepop",
        "seaofthieves",
        "enderlilies",
        "peaks_of_yore",
        "ufo50",
        "hcniko",
        "raft",
        "terraria",
        "satisfactory",
        "huniepop2",
        "momodoramoonlitfarewell",
        "dsr",
        "lego_star_wars_tcs",
        "heretic",
        "rogue_legacy",
        "messenger",
        "gzdoom",
        "outer_wilds",
        "dark_souls_2",
        "rimworld",
        "hades",
        "minecraft",
        "monster_sanctuary",
        "doom_ii",
        "factorio_saws",
        "landstalker",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "dontstarvetogether",
        "musedash",
        "inscryption",
        "sa2b",
        "tyrian",
        "shapez"
    ],
    "(microsoft": [
        "sadx",
        "shivers",
        "residentevil3remake",
        "aus",
        "ahit",
        "osrs",
        "crosscode",
        "swr",
        "civ_6",
        "oribf",
        "celeste",
        "v6",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "getting_over_it",
        "dlcquest",
        "simpsonshitnrun",
        "blasphemous",
        "powerwashsimulator",
        "meritous",
        "sims4",
        "balatro",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "sonic_heroes",
        "sc2",
        "bomb_rush_cyberfunk",
        "witness",
        "stardew_valley",
        "timespinner",
        "cuphead",
        "wargroove",
        "shorthike",
        "bumpstik",
        "animal_well",
        "undertale",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "toontown",
        "spire",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ultrakill",
        "doronko_wanko",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "aquaria",
        "lingo",
        "tunic",
        "lethal_company",
        "quake",
        "ror1",
        "osu",
        "factorio",
        "huniepop",
        "seaofthieves",
        "enderlilies",
        "peaks_of_yore",
        "ufo50",
        "hcniko",
        "raft",
        "terraria",
        "satisfactory",
        "huniepop2",
        "momodoramoonlitfarewell",
        "dsr",
        "lego_star_wars_tcs",
        "heretic",
        "rogue_legacy",
        "messenger",
        "gzdoom",
        "outer_wilds",
        "dark_souls_2",
        "rimworld",
        "hades",
        "minecraft",
        "monster_sanctuary",
        "doom_ii",
        "factorio_saws",
        "landstalker",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "dontstarvetogether",
        "musedash",
        "inscryption",
        "sa2b",
        "tyrian",
        "shapez"
    ],
    "windows)": [
        "sadx",
        "shivers",
        "residentevil3remake",
        "aus",
        "ahit",
        "osrs",
        "crosscode",
        "swr",
        "civ_6",
        "oribf",
        "celeste",
        "v6",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "getting_over_it",
        "dlcquest",
        "simpsonshitnrun",
        "blasphemous",
        "powerwashsimulator",
        "meritous",
        "sims4",
        "balatro",
        "noita",
        "overcooked2",
        "placidplasticducksim",
        "sonic_heroes",
        "sc2",
        "bomb_rush_cyberfunk",
        "witness",
        "stardew_valley",
        "timespinner",
        "cuphead",
        "wargroove",
        "shorthike",
        "bumpstik",
        "animal_well",
        "undertale",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "toontown",
        "spire",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "ultrakill",
        "doronko_wanko",
        "chainedechoes",
        "openrct2",
        "wargroove2",
        "aquaria",
        "lingo",
        "tunic",
        "lethal_company",
        "quake",
        "ror1",
        "osu",
        "factorio",
        "huniepop",
        "seaofthieves",
        "enderlilies",
        "peaks_of_yore",
        "ufo50",
        "hcniko",
        "raft",
        "terraria",
        "satisfactory",
        "huniepop2",
        "momodoramoonlitfarewell",
        "dsr",
        "lego_star_wars_tcs",
        "heretic",
        "rogue_legacy",
        "messenger",
        "gzdoom",
        "outer_wilds",
        "dark_souls_2",
        "rimworld",
        "hades",
        "minecraft",
        "monster_sanctuary",
        "doom_ii",
        "factorio_saws",
        "landstalker",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "dontstarvetogether",
        "musedash",
        "inscryption",
        "sa2b",
        "tyrian",
        "shapez"
    ],
    "playstation 5": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "hades",
        "tunic",
        "bomb_rush_cyberfunk",
        "crosscode",
        "seaofthieves",
        "residentevil2remake",
        "ror2",
        "raft",
        "subnautica",
        "satisfactory",
        "against_the_storm",
        "brotato",
        "trackmania",
        "momodoramoonlitfarewell",
        "inscryption",
        "animal_well",
        "poe",
        "powerwashsimulator",
        "messenger"
    ],
    "playstation": [
        "apeescape",
        "sadx",
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "sotn",
        "placidplasticducksim",
        "dark_souls_2",
        "chainedechoes",
        "overcooked2",
        "sonic_heroes",
        "hades",
        "tunic",
        "jakanddaxter",
        "spyro3",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "kh2",
        "seaofthieves",
        "enderlilies",
        "stardew_valley",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "shorthike",
        "celeste",
        "cat_quest",
        "raft",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "rac2",
        "v6",
        "satisfactory",
        "dw1",
        "kh1",
        "against_the_storm",
        "brotato",
        "dark_souls_3",
        "momodoramoonlitfarewell",
        "inscryption",
        "trackmania",
        "sa2b",
        "dsr",
        "lego_star_wars_tcs",
        "animal_well",
        "undertale",
        "simpsonshitnrun",
        "blasphemous",
        "sly1",
        "hk",
        "poe",
        "powerwashsimulator",
        "fm",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "5": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "hades",
        "tunic",
        "bomb_rush_cyberfunk",
        "crosscode",
        "seaofthieves",
        "residentevil2remake",
        "ror2",
        "raft",
        "subnautica",
        "satisfactory",
        "against_the_storm",
        "brotato",
        "trackmania",
        "momodoramoonlitfarewell",
        "inscryption",
        "animal_well",
        "poe",
        "powerwashsimulator",
        "messenger"
    ],
    "nintendo switch": [
        "balatro",
        "outer_wilds",
        "doronko_wanko",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "wargroove2",
        "hades",
        "tunic",
        "smo",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "factorio",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "cuphead",
        "swr",
        "ufo50",
        "wargroove",
        "oribf",
        "hcniko",
        "shorthike",
        "celeste",
        "cat_quest",
        "ror2",
        "subnautica",
        "terraria",
        "dontstarvetogether",
        "v6",
        "musedash",
        "against_the_storm",
        "brotato",
        "momodoramoonlitfarewell",
        "inscryption",
        "dsr",
        "animal_well",
        "undertale",
        "megamix",
        "blasphemous",
        "hk",
        "powerwashsimulator",
        "tboir",
        "rogue_legacy",
        "messenger"
    ],
    "nintendo": [
        "mm_recomp",
        "mk64",
        "diddy_kong_racing",
        "pokemon_crystal",
        "papermario",
        "wl",
        "metroidprime",
        "ahit",
        "crosscode",
        "marioland2",
        "swr",
        "oribf",
        "celeste",
        "tww",
        "lufia2ac",
        "v6",
        "against_the_storm",
        "brotato",
        "mm2",
        "sm64ex",
        "sm_map_rando",
        "simpsonshitnrun",
        "blasphemous",
        "powerwashsimulator",
        "tetrisattack",
        "balatro",
        "placidplasticducksim",
        "overcooked2",
        "sonic_heroes",
        "kdl3",
        "alttp",
        "ffmq",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "tmc",
        "stardew_valley",
        "zelda2",
        "timespinner",
        "cuphead",
        "earthbound",
        "wargroove",
        "shorthike",
        "mario_kart_double_dash",
        "yoshisisland",
        "sm64hacks",
        "animal_well",
        "undertale",
        "sm",
        "luigismansion",
        "hk",
        "mmx3",
        "soe",
        "ff4fe",
        "oot",
        "doronko_wanko",
        "albw",
        "chainedechoes",
        "wargroove2",
        "dkc",
        "tunic",
        "smo",
        "ror1",
        "factorio",
        "dkc2",
        "enderlilies",
        "cv64",
        "ufo50",
        "ff1",
        "dkc3",
        "hcniko",
        "tloz",
        "terraria",
        "tloz_ooa",
        "dw1",
        "momodoramoonlitfarewell",
        "dsr",
        "smz3",
        "tloz_ph",
        "dk64",
        "megamix",
        "ladx",
        "mm3",
        "tboir",
        "banjo_tooie",
        "rogue_legacy",
        "messenger",
        "sms",
        "outer_wilds",
        "smw",
        "hades",
        "faxanadu",
        "monster_sanctuary",
        "ctjot",
        "tloz_oos",
        "wl4",
        "cat_quest",
        "ror2",
        "subnautica",
        "dontstarvetogether",
        "pokemon_rb",
        "k64",
        "pmd_eos",
        "musedash",
        "inscryption"
    ],
    "switch": [
        "balatro",
        "outer_wilds",
        "doronko_wanko",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "wargroove2",
        "hades",
        "tunic",
        "smo",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "factorio",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "cuphead",
        "swr",
        "ufo50",
        "wargroove",
        "oribf",
        "hcniko",
        "shorthike",
        "celeste",
        "cat_quest",
        "ror2",
        "subnautica",
        "terraria",
        "dontstarvetogether",
        "v6",
        "musedash",
        "against_the_storm",
        "brotato",
        "momodoramoonlitfarewell",
        "inscryption",
        "dsr",
        "animal_well",
        "undertale",
        "megamix",
        "blasphemous",
        "hk",
        "powerwashsimulator",
        "tboir",
        "rogue_legacy",
        "messenger"
    ],
    "base building": [
        "satisfactory",
        "shapez",
        "against_the_storm",
        "rimworld"
    ],
    "base": [
        "satisfactory",
        "shapez",
        "against_the_storm",
        "rimworld"
    ],
    "building": [
        "satisfactory",
        "shapez",
        "against_the_storm",
        "rimworld"
    ],
    "roguelite": [
        "ror2",
        "ror1",
        "noita",
        "dungeon_clawler",
        "against_the_storm",
        "brotato",
        "hades"
    ],
    "a hat in time": [
        "ahit"
    ],
    "a": [
        "smo",
        "ahit",
        "albw",
        "alttp",
        "dark_souls_3",
        "sm64hacks",
        "sm64ex",
        "shorthike",
        "smz3"
    ],
    "hat": [
        "ahit"
    ],
    "in": [
        "sms",
        "oot",
        "smw",
        "albw",
        "alttp",
        "papermario",
        "smo",
        "metroidprime",
        "ahit",
        "tmc",
        "tloz_oos",
        "zelda2",
        "earthbound",
        "ss",
        "tloz_ooa",
        "kh1",
        "dark_souls_3",
        "sm64hacks",
        "sm64ex",
        "sm_map_rando",
        "tloz_ph",
        "sm"
    ],
    "first person": [
        "shivers",
        "outer_wilds",
        "doom_1993",
        "ultrakill",
        "lingo",
        "minecraft",
        "lethal_company",
        "metroidprime",
        "quake",
        "ahit",
        "star_fox_64",
        "huniepop",
        "seaofthieves",
        "witness",
        "doom_ii",
        "cv64",
        "swr",
        "earthbound",
        "raft",
        "subnautica",
        "satisfactory",
        "huniepop2",
        "trackmania",
        "inscryption",
        "heretic",
        "yugiohddm",
        "powerwashsimulator",
        "hylics2",
        "fm",
        "zork_grand_inquisitor",
        "sims4"
    ],
    "first": [
        "shivers",
        "outer_wilds",
        "doom_1993",
        "ultrakill",
        "lingo",
        "minecraft",
        "lethal_company",
        "metroidprime",
        "quake",
        "ahit",
        "star_fox_64",
        "huniepop",
        "seaofthieves",
        "witness",
        "doom_ii",
        "cv64",
        "swr",
        "earthbound",
        "raft",
        "subnautica",
        "satisfactory",
        "huniepop2",
        "trackmania",
        "inscryption",
        "heretic",
        "yugiohddm",
        "powerwashsimulator",
        "hylics2",
        "fm",
        "zork_grand_inquisitor",
        "sims4"
    ],
    "person": [
        "apeescape",
        "mk64",
        "mm_recomp",
        "sadx",
        "shivers",
        "residentevil3remake",
        "diddy_kong_racing",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "ahit",
        "swr",
        "tww",
        "dark_souls_3",
        "trackmania",
        "getting_over_it",
        "sm64ex",
        "simpsonshitnrun",
        "powerwashsimulator",
        "sims4",
        "doom_1993",
        "placidplasticducksim",
        "sonic_heroes",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "witness",
        "earthbound",
        "mario_kart_double_dash",
        "sm64hacks",
        "luigismansion",
        "hylics2",
        "toontown",
        "soe",
        "zork_grand_inquisitor",
        "pseudoregalia",
        "oot",
        "ultrakill",
        "albw",
        "gstla",
        "lingo",
        "lethal_company",
        "smo",
        "quake",
        "spyro3",
        "huniepop",
        "kh2",
        "seaofthieves",
        "xenobladex",
        "cv64",
        "hcniko",
        "raft",
        "rac2",
        "satisfactory",
        "dw1",
        "huniepop2",
        "dsr",
        "lego_star_wars_tcs",
        "heretic",
        "dk64",
        "megamix",
        "sly1",
        "fm",
        "banjo_tooie",
        "sms",
        "gzdoom",
        "outer_wilds",
        "dark_souls_2",
        "minecraft",
        "doom_ii",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "subnautica",
        "celeste64",
        "ss",
        "kh1",
        "inscryption",
        "sa2b",
        "yugiohddm",
        "tp"
    ],
    "third person": [
        "sms",
        "apeescape",
        "mk64",
        "gzdoom",
        "mm_recomp",
        "oot",
        "residentevil3remake",
        "sadx",
        "diddy_kong_racing",
        "dark_souls_2",
        "albw",
        "placidplasticducksim",
        "sonic_heroes",
        "gstla",
        "papermario",
        "minecraft",
        "jakanddaxter",
        "smo",
        "spyro3",
        "ahit",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "kh2",
        "xenobladex",
        "cv64",
        "swr",
        "hcniko",
        "raft",
        "cat_quest",
        "residentevil2remake",
        "ror2",
        "tww",
        "celeste64",
        "mario_kart_double_dash",
        "rac2",
        "ss",
        "dw1",
        "kh1",
        "dark_souls_3",
        "sm64hacks",
        "trackmania",
        "sa2b",
        "dsr",
        "getting_over_it",
        "sm64ex",
        "lego_star_wars_tcs",
        "dk64",
        "luigismansion",
        "megamix",
        "tp",
        "simpsonshitnrun",
        "sly1",
        "hylics2",
        "toontown",
        "banjo_tooie",
        "soe",
        "sims4",
        "pseudoregalia"
    ],
    "third": [
        "sms",
        "apeescape",
        "mk64",
        "gzdoom",
        "mm_recomp",
        "oot",
        "residentevil3remake",
        "sadx",
        "diddy_kong_racing",
        "dark_souls_2",
        "albw",
        "placidplasticducksim",
        "sonic_heroes",
        "gstla",
        "papermario",
        "minecraft",
        "jakanddaxter",
        "smo",
        "spyro3",
        "ahit",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "kh2",
        "xenobladex",
        "cv64",
        "swr",
        "hcniko",
        "raft",
        "cat_quest",
        "residentevil2remake",
        "ror2",
        "tww",
        "celeste64",
        "mario_kart_double_dash",
        "rac2",
        "ss",
        "dw1",
        "kh1",
        "dark_souls_3",
        "sm64hacks",
        "trackmania",
        "sa2b",
        "dsr",
        "getting_over_it",
        "sm64ex",
        "lego_star_wars_tcs",
        "dk64",
        "luigismansion",
        "megamix",
        "tp",
        "simpsonshitnrun",
        "sly1",
        "hylics2",
        "toontown",
        "banjo_tooie",
        "soe",
        "sims4",
        "pseudoregalia"
    ],
    "platform": [
        "sms",
        "apeescape",
        "sadx",
        "gzdoom",
        "ultrakill",
        "smw",
        "sotn",
        "sonic_heroes",
        "aquaria",
        "dkc",
        "kdl3",
        "wl",
        "rogue_legacy",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "ror1",
        "smo",
        "cvcotm",
        "monster_sanctuary",
        "aus",
        "ahit",
        "bomb_rush_cyberfunk",
        "zillion",
        "dkc2",
        "enderlilies",
        "timespinner",
        "peaks_of_yore",
        "marioland2",
        "cv64",
        "zelda2",
        "cuphead",
        "ufo50",
        "oribf",
        "dkc3",
        "hcniko",
        "wl4",
        "celeste",
        "celeste64",
        "terraria",
        "rac2",
        "v6",
        "yoshisisland",
        "k64",
        "sm64hacks",
        "momodoramoonlitfarewell",
        "mm2",
        "sa2b",
        "getting_over_it",
        "sm64ex",
        "lego_star_wars_tcs",
        "mzm",
        "smz3",
        "animal_well",
        "dlcquest",
        "sm_map_rando",
        "dk64",
        "sm",
        "simpsonshitnrun",
        "blasphemous",
        "mm3",
        "sly1",
        "spyro3",
        "hk",
        "mmx3",
        "hylics2",
        "banjo_tooie",
        "pseudoregalia",
        "messenger"
    ],
    "action": [
        "apeescape",
        "mk64",
        "mm_recomp",
        "sadx",
        "residentevil3remake",
        "diddy_kong_racing",
        "pokemon_crystal",
        "papermario",
        "wl",
        "jakanddaxter",
        "metroidprime",
        "ahit",
        "aus",
        "crosscode",
        "marioland2",
        "swr",
        "oribf",
        "celeste",
        "tww",
        "v6",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "mm2",
        "pokemon_frlg",
        "getting_over_it",
        "sm64ex",
        "dlcquest",
        "sm_map_rando",
        "simpsonshitnrun",
        "blasphemous",
        "sims4",
        "tetrisattack",
        "doom_1993",
        "noita",
        "overcooked2",
        "sonic_heroes",
        "kdl3",
        "alttp",
        "sc2",
        "ffmq",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "tmc",
        "zelda2",
        "timespinner",
        "cuphead",
        "earthbound",
        "mario_kart_double_dash",
        "yoshisisland",
        "sm64hacks",
        "pokemon_emerald",
        "mzm",
        "animal_well",
        "sm",
        "luigismansion",
        "dungeon_clawler",
        "hk",
        "mmx3",
        "poe",
        "soe",
        "pseudoregalia",
        "ff4fe",
        "oot",
        "ultrakill",
        "doronko_wanko",
        "sotn",
        "albw",
        "chainedechoes",
        "dkc",
        "gstla",
        "tunic",
        "lethal_company",
        "smo",
        "quake",
        "ror1",
        "spyro3",
        "cvcotm",
        "osu",
        "seaofthieves",
        "dkc2",
        "kh2",
        "enderlilies",
        "xenobladex",
        "peaks_of_yore",
        "cv64",
        "ufo50",
        "ff1",
        "dkc3",
        "hcniko",
        "tloz",
        "terraria",
        "rac2",
        "tloz_ooa",
        "dw1",
        "momodoramoonlitfarewell",
        "dsr",
        "smz3",
        "lego_star_wars_tcs",
        "tloz_ph",
        "dk64",
        "ladx",
        "mm3",
        "sly1",
        "banjo_tooie",
        "rogue_legacy",
        "messenger",
        "sms",
        "gzdoom",
        "outer_wilds",
        "smw",
        "dark_souls_2",
        "hades",
        "faxanadu",
        "mmbn3",
        "monster_sanctuary",
        "mlss",
        "ctjot",
        "tloz_oos",
        "doom_ii",
        "landstalker",
        "wl4",
        "residentevil2remake",
        "cat_quest",
        "ror2",
        "celeste64",
        "dontstarvetogether",
        "ss",
        "pokemon_rb",
        "k64",
        "kh1",
        "musedash",
        "sa2b",
        "tyrian",
        "tp"
    ],
    "playstation 4": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "hades",
        "tunic",
        "jakanddaxter",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "kh2",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "shorthike",
        "celeste",
        "cat_quest",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "v6",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "inscryption",
        "dsr",
        "undertale",
        "blasphemous",
        "hk",
        "poe",
        "powerwashsimulator",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "4": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "hades",
        "tunic",
        "jakanddaxter",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "kh2",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "wl4",
        "shorthike",
        "celeste",
        "cat_quest",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "v6",
        "dw1",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "inscryption",
        "dsr",
        "undertale",
        "blasphemous",
        "hk",
        "poe",
        "powerwashsimulator",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "mac": [
        "balatro",
        "residentevil3remake",
        "overcooked2",
        "chainedechoes",
        "openrct2",
        "aquaria",
        "rimworld",
        "hades",
        "minecraft",
        "sc2",
        "tunic",
        "quake",
        "ror1",
        "monster_sanctuary",
        "osu",
        "ahit",
        "osrs",
        "crosscode",
        "factorio",
        "huniepop",
        "doom_ii",
        "factorio_saws",
        "stardew_valley",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "civ_6",
        "landstalker",
        "shorthike",
        "celeste",
        "cat_quest",
        "residentevil2remake",
        "subnautica",
        "terraria",
        "dontstarvetogether",
        "v6",
        "musedash",
        "brotato",
        "huniepop2",
        "inscryption",
        "getting_over_it",
        "tyrian",
        "lego_star_wars_tcs",
        "heretic",
        "dlcquest",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "hk",
        "poe",
        "hylics2",
        "toontown",
        "zork_grand_inquisitor",
        "sims4",
        "rogue_legacy",
        "shapez"
    ],
    "xbox one": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "wargroove2",
        "hades",
        "tunic",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "seaofthieves",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "oribf",
        "shorthike",
        "celeste",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "inscryption",
        "dsr",
        "undertale",
        "blasphemous",
        "hk",
        "poe",
        "powerwashsimulator",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "one": [
        "balatro",
        "outer_wilds",
        "residentevil3remake",
        "placidplasticducksim",
        "overcooked2",
        "chainedechoes",
        "wargroove2",
        "hades",
        "tunic",
        "ror1",
        "monster_sanctuary",
        "ahit",
        "bomb_rush_cyberfunk",
        "crosscode",
        "seaofthieves",
        "stardew_valley",
        "enderlilies",
        "timespinner",
        "witness",
        "cuphead",
        "swr",
        "wargroove",
        "oribf",
        "shorthike",
        "celeste",
        "residentevil2remake",
        "ror2",
        "subnautica",
        "terraria",
        "brotato",
        "dark_souls_3",
        "trackmania",
        "inscryption",
        "dsr",
        "undertale",
        "blasphemous",
        "hk",
        "poe",
        "powerwashsimulator",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "time travel": [
        "apeescape",
        "mm_recomp",
        "oot",
        "outer_wilds",
        "ctjot",
        "ahit",
        "tloz_ooa",
        "tloz_oos",
        "pmd_eos",
        "timespinner",
        "earthbound"
    ],
    "travel": [
        "apeescape",
        "mm_recomp",
        "oot",
        "outer_wilds",
        "ctjot",
        "ahit",
        "tloz_ooa",
        "albw",
        "tloz_oos",
        "doom_ii",
        "pmd_eos",
        "timespinner",
        "alttp",
        "earthbound"
    ],
    "spaceship": [
        "metroidprime",
        "mzm",
        "ahit",
        "star_fox_64",
        "v6",
        "civ_6"
    ],
    "female protagonist": [
        "metroidprime",
        "mzm",
        "sm_map_rando",
        "undertale",
        "celeste64",
        "sm",
        "ahit",
        "dkc2",
        "enderlilies",
        "timespinner",
        "cv64",
        "hcniko",
        "earthbound",
        "dkc3",
        "rogue_legacy",
        "shorthike",
        "celeste"
    ],
    "female": [
        "metroidprime",
        "mzm",
        "sm_map_rando",
        "undertale",
        "celeste64",
        "sm",
        "ahit",
        "dkc2",
        "enderlilies",
        "timespinner",
        "cv64",
        "hcniko",
        "earthbound",
        "dkc3",
        "rogue_legacy",
        "shorthike",
        "celeste"
    ],
    "protagonist": [
        "apeescape",
        "oot",
        "ultrakill",
        "doom_1993",
        "pokemon_crystal",
        "sonic_heroes",
        "dkc",
        "alttp",
        "gstla",
        "papermario",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "quake",
        "mlss",
        "ahit",
        "tmc",
        "dkc2",
        "tloz_oos",
        "enderlilies",
        "timespinner",
        "zelda2",
        "cv64",
        "earthbound",
        "hcniko",
        "dkc3",
        "shorthike",
        "celeste",
        "celeste64",
        "ss",
        "tloz_ooa",
        "k64",
        "kh1",
        "pokemon_emerald",
        "mm2",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "undertale",
        "sm",
        "simpsonshitnrun",
        "blasphemous",
        "ladx",
        "mm3",
        "hk",
        "mmx3",
        "rogue_legacy"
    ],
    "action-adventure": [
        "sms",
        "mm_recomp",
        "oot",
        "sotn",
        "dark_souls_2",
        "albw",
        "aquaria",
        "alttp",
        "minecraft",
        "metroidprime",
        "zillion",
        "cvcotm",
        "aus",
        "ahit",
        "crosscode",
        "seaofthieves",
        "tloz_oos",
        "tmc",
        "timespinner",
        "xenobladex",
        "zelda2",
        "cv64",
        "landstalker",
        "tww",
        "terraria",
        "dontstarvetogether",
        "ss",
        "tloz_ooa",
        "kh1",
        "dark_souls_3",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "luigismansion",
        "ladx",
        "hk",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "cute": [
        "animal_well",
        "undertale",
        "ahit",
        "musedash",
        "sims4",
        "hcniko",
        "tunic",
        "shorthike",
        "celeste"
    ],
    "snow": [
        "jakanddaxter",
        "lego_star_wars_tcs",
        "metroidprime",
        "mk64",
        "ahit",
        "terraria",
        "diddy_kong_racing",
        "albw",
        "stardew_valley",
        "dkc",
        "ffta",
        "gstla",
        "hcniko",
        "dkc3",
        "minecraft",
        "celeste"
    ],
    "wall jump": [
        "smo",
        "mzm",
        "sms",
        "sm_map_rando",
        "cvcotm",
        "sm",
        "ahit",
        "simpsonshitnrun",
        "mmx3",
        "oribf"
    ],
    "wall": [
        "sms",
        "mk64",
        "oot",
        "dkc",
        "papermario",
        "jakanddaxter",
        "smo",
        "cvcotm",
        "mlss",
        "ahit",
        "tmc",
        "dkc2",
        "doom_ii",
        "oribf",
        "kh1",
        "mzm",
        "sm_map_rando",
        "undertale",
        "dk64",
        "sm",
        "simpsonshitnrun",
        "ladx",
        "ffta",
        "mmx3",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "jump": [
        "smo",
        "mzm",
        "sms",
        "sm_map_rando",
        "cvcotm",
        "sm",
        "ahit",
        "simpsonshitnrun",
        "mmx3",
        "oribf"
    ],
    "3d platformer": [
        "smo",
        "sms",
        "ahit",
        "bomb_rush_cyberfunk",
        "shorthike",
        "sonic_heroes",
        "sm64hacks",
        "hcniko",
        "sm64ex"
    ],
    "3d": [
        "sms",
        "apeescape",
        "mk64",
        "oot",
        "sotn",
        "dark_souls_2",
        "albw",
        "sonic_heroes",
        "lingo",
        "tunic",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "smo",
        "spyro3",
        "ahit",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "witness",
        "xenobladex",
        "cv64",
        "hcniko",
        "shorthike",
        "ss",
        "v6",
        "k64",
        "dw1",
        "kh1",
        "dark_souls_3",
        "sm64hacks",
        "dsr",
        "sm64ex",
        "lego_star_wars_tcs",
        "tloz_ph",
        "dk64",
        "luigismansion",
        "simpsonshitnrun",
        "sly1",
        "poe",
        "powerwashsimulator",
        "hylics2"
    ],
    "platformer": [
        "smo",
        "sms",
        "ahit",
        "bomb_rush_cyberfunk",
        "blasphemous",
        "v6",
        "sonic_heroes",
        "hk",
        "hylics2",
        "sm64hacks",
        "sm64ex",
        "hcniko",
        "shorthike"
    ],
    "swimming": [
        "sms",
        "oot",
        "albw",
        "aquaria",
        "alttp",
        "dkc",
        "minecraft",
        "jakanddaxter",
        "smo",
        "quake",
        "spyro3",
        "ahit",
        "tmc",
        "dkc2",
        "wl4",
        "hcniko",
        "dkc3",
        "subnautica",
        "terraria",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "sm64ex",
        "banjo_tooie"
    ],
    "steam greenlight": [
        "timespinner",
        "ror1",
        "dlcquest",
        "ahit"
    ],
    "steam": [
        "timespinner",
        "ror1",
        "dlcquest",
        "ahit"
    ],
    "greenlight": [
        "timespinner",
        "ror1",
        "dlcquest",
        "ahit"
    ],
    "crowdfunding": [
        "ror1",
        "ahit",
        "crosscode",
        "hk",
        "timespinner"
    ],
    "crowd funded": [
        "ror1",
        "ahit",
        "crosscode",
        "hk",
        "timespinner"
    ],
    "crowd": [
        "ror1",
        "ahit",
        "crosscode",
        "hk",
        "timespinner"
    ],
    "funded": [
        "ror1",
        "ahit",
        "crosscode",
        "hk",
        "timespinner"
    ],
    "collection marathon": [
        "sms",
        "dk64",
        "ahit",
        "k64",
        "banjo_tooie"
    ],
    "collection": [
        "sms",
        "dk64",
        "ahit",
        "k64",
        "banjo_tooie"
    ],
    "marathon": [
        "sms",
        "dk64",
        "ahit",
        "k64",
        "banjo_tooie"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "mm_recomp",
        "oot",
        "tloz",
        "tloz_ph",
        "tww",
        "tp",
        "ss",
        "ladx",
        "tloz_ooa",
        "tmc",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "of": [
        "sms",
        "mm_recomp",
        "oot",
        "balatro",
        "sotn",
        "albw",
        "pokemon_crystal",
        "dkc",
        "alttp",
        "hades",
        "sc2",
        "jakanddaxter",
        "smo",
        "ror1",
        "spyro3",
        "cvcotm",
        "star_fox_64",
        "seaofthieves",
        "dkc2",
        "tloz_oos",
        "enderlilies",
        "tmc",
        "peaks_of_yore",
        "zelda2",
        "cv64",
        "earthbound",
        "oribf",
        "dkc3",
        "celeste",
        "ror2",
        "tloz",
        "tww",
        "celeste64",
        "ss",
        "lufia2ac",
        "tloz_ooa",
        "pmd_eos",
        "pokemon_emerald",
        "tloz_ph",
        "dk64",
        "luigismansion",
        "tp",
        "ladx",
        "sly1",
        "poe",
        "ffta",
        "tboir",
        "soe",
        "rogue_legacy"
    ],
    "zelda:": [
        "mm_recomp",
        "oot",
        "tww",
        "tloz_ph",
        "tp",
        "ss",
        "ladx",
        "tloz_ooa",
        "tmc",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "link": [
        "zelda2",
        "alttp",
        "albw",
        "smz3"
    ],
    "between": [
        "albw"
    ],
    "worlds": [
        "albw"
    ],
    "puzzle": [
        "mm_recomp",
        "oot",
        "shivers",
        "outer_wilds",
        "tetrisattack",
        "placidplasticducksim",
        "albw",
        "alttp",
        "lingo",
        "tunic",
        "spyro3",
        "metroidprime",
        "zillion",
        "crosscode",
        "huniepop",
        "tloz_oos",
        "doom_ii",
        "tmc",
        "witness",
        "cv64",
        "ufo50",
        "candybox2",
        "oribf",
        "hcniko",
        "wl4",
        "tww",
        "ss",
        "lufia2ac",
        "tloz_ooa",
        "v6",
        "bumpstik",
        "huniepop2",
        "inscryption",
        "animal_well",
        "tloz_ph",
        "undertale",
        "yugiohddm",
        "tp",
        "ladx",
        "mm3",
        "ttyd",
        "zork_grand_inquisitor",
        "rogue_legacy",
        "shapez"
    ],
    "historical": [
        "heretic",
        "quake",
        "soe",
        "ss",
        "albw",
        "fm",
        "civ_6",
        "candybox2"
    ],
    "sandbox": [
        "sms",
        "oot",
        "noita",
        "placidplasticducksim",
        "albw",
        "minecraft",
        "smo",
        "faxanadu",
        "osrs",
        "factorio",
        "stardew_valley",
        "xenobladex",
        "zelda2",
        "factorio_saws",
        "landstalker",
        "terraria",
        "dontstarvetogether",
        "satisfactory",
        "powerwashsimulator",
        "sims4",
        "shapez"
    ],
    "open world": [
        "mm_recomp",
        "oot",
        "outer_wilds",
        "sotn",
        "albw",
        "gstla",
        "lingo",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "smo",
        "osrs",
        "seaofthieves",
        "witness",
        "xenobladex",
        "shorthike",
        "subnautica",
        "tloz",
        "terraria",
        "dontstarvetogether",
        "ss",
        "pokemon_rb",
        "satisfactory",
        "sm64hacks",
        "sm64ex",
        "smz3",
        "mzm",
        "simpsonshitnrun",
        "toontown"
    ],
    "open": [
        "mm_recomp",
        "oot",
        "outer_wilds",
        "sotn",
        "albw",
        "gstla",
        "lingo",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "smo",
        "osrs",
        "seaofthieves",
        "witness",
        "xenobladex",
        "shorthike",
        "subnautica",
        "tloz",
        "terraria",
        "dontstarvetogether",
        "ss",
        "pokemon_rb",
        "satisfactory",
        "sm64hacks",
        "sm64ex",
        "smz3",
        "mzm",
        "simpsonshitnrun",
        "toontown"
    ],
    "world": [
        "mm_recomp",
        "oot",
        "outer_wilds",
        "smw",
        "sotn",
        "dark_souls_2",
        "albw",
        "pokemon_crystal",
        "aquaria",
        "alttp",
        "dkc",
        "gstla",
        "lingo",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "smo",
        "osrs",
        "seaofthieves",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "tmc",
        "witness",
        "xenobladex",
        "zelda2",
        "earthbound",
        "dkc3",
        "shorthike",
        "subnautica",
        "tloz",
        "terraria",
        "dontstarvetogether",
        "ss",
        "v6",
        "pokemon_rb",
        "yoshisisland",
        "satisfactory",
        "dw1",
        "dark_souls_3",
        "sm64hacks",
        "yugioh06",
        "sm64ex",
        "smz3",
        "mzm",
        "tloz_ph",
        "simpsonshitnrun",
        "ladx",
        "toontown"
    ],
    "nintendo 3ds": [
        "tloz",
        "wl4",
        "terraria",
        "tloz_ooa",
        "ladx",
        "mm3",
        "tmc",
        "albw",
        "pokemon_crystal",
        "pokemon_rb",
        "tloz_oos",
        "v6",
        "marioland2",
        "zelda2",
        "wl",
        "mm2",
        "ff1"
    ],
    "3ds": [
        "smw",
        "albw",
        "pokemon_crystal",
        "dkc",
        "alttp",
        "wl",
        "tmc",
        "dkc2",
        "tloz_oos",
        "zelda2",
        "marioland2",
        "earthbound",
        "ff1",
        "dkc3",
        "wl4",
        "tloz",
        "terraria",
        "tloz_ooa",
        "v6",
        "pokemon_rb",
        "mm2",
        "sm_map_rando",
        "sm",
        "ladx",
        "mm3",
        "mmx3"
    ],
    "medieval": [
        "heretic",
        "quake",
        "soe",
        "ss",
        "dark_souls_2",
        "albw",
        "dark_souls_3",
        "candybox2",
        "rogue_legacy"
    ],
    "magic": [
        "sotn",
        "noita",
        "dark_souls_2",
        "albw",
        "aquaria",
        "alttp",
        "gstla",
        "faxanadu",
        "cvcotm",
        "ctjot",
        "tmc",
        "tloz_oos",
        "zelda2",
        "cv64",
        "cuphead",
        "candybox2",
        "terraria",
        "dsr",
        "heretic",
        "ladx",
        "poe",
        "ffta",
        "zork_grand_inquisitor",
        "rogue_legacy"
    ],
    "minigames": [
        "spyro3",
        "apeescape",
        "oot",
        "tloz_ph",
        "dk64",
        "tloz_ooa",
        "albw",
        "pokemon_crystal",
        "stardew_valley",
        "k64",
        "gstla",
        "kh1",
        "toontown",
        "hcniko",
        "pokemon_emerald",
        "wl4",
        "dkc3",
        "rogue_legacy"
    ],
    "2.5d": [
        "heretic",
        "doom_1993",
        "albw",
        "doom_ii",
        "k64",
        "dkc",
        "dkc3"
    ],
    "archery": [
        "mm_recomp",
        "oot",
        "tww",
        "ss",
        "albw",
        "alttp",
        "minecraft"
    ],
    "fairy": [
        "mm_recomp",
        "oot",
        "tloz",
        "tloz_ph",
        "tww",
        "dk64",
        "terraria",
        "tloz_ooa",
        "ladx",
        "tmc",
        "albw",
        "stardew_valley",
        "tloz_oos",
        "k64",
        "zelda2",
        "alttp",
        "huniepop2",
        "landstalker"
    ],
    "princess": [
        "sms",
        "mk64",
        "oot",
        "smw",
        "albw",
        "alttp",
        "papermario",
        "mlss",
        "tmc",
        "tloz_oos",
        "mario_kart_double_dash",
        "ss",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "sm64ex",
        "lego_star_wars_tcs",
        "tloz_ph",
        "tp",
        "ladx"
    ],
    "sequel": [
        "sms",
        "mm_recomp",
        "mk64",
        "oot",
        "dark_souls_2",
        "albw",
        "alttp",
        "gstla",
        "smo",
        "dkc2",
        "doom_ii",
        "zelda2",
        "civ_6",
        "wl4",
        "dontstarvetogether",
        "dw1",
        "dark_souls_3",
        "mm2",
        "mm3",
        "ffta",
        "mmx3",
        "hylics2",
        "banjo_tooie"
    ],
    "sword & sorcery": [
        "ffmq",
        "mm_recomp",
        "heretic",
        "oot",
        "spyro3",
        "tww",
        "terraria",
        "ss",
        "ladx",
        "tloz_ooa",
        "dark_souls_2",
        "albw",
        "tloz_oos",
        "tmc",
        "kh1",
        "dark_souls_3"
    ],
    "sword": [
        "mm_recomp",
        "oot",
        "dark_souls_2",
        "albw",
        "tunic",
        "minecraft",
        "ffmq",
        "spyro3",
        "tmc",
        "stardew_valley",
        "tloz_oos",
        "tww",
        "terraria",
        "ss",
        "tloz_ooa",
        "kh1",
        "dark_souls_3",
        "heretic",
        "ladx",
        "hk"
    ],
    "&": [
        "mm_recomp",
        "oot",
        "balatro",
        "dark_souls_2",
        "albw",
        "ffmq",
        "spyro3",
        "mlss",
        "tmc",
        "tloz_oos",
        "tww",
        "terraria",
        "rac2",
        "ss",
        "tloz_ooa",
        "kh1",
        "dark_souls_3",
        "yugioh06",
        "inscryption",
        "heretic",
        "yugiohddm",
        "simpsonshitnrun",
        "ladx",
        "fm",
        "spire"
    ],
    "sorcery": [
        "ffmq",
        "mm_recomp",
        "heretic",
        "oot",
        "spyro3",
        "tww",
        "terraria",
        "ss",
        "ladx",
        "tloz_ooa",
        "dark_souls_2",
        "albw",
        "tloz_oos",
        "tmc",
        "kh1",
        "dark_souls_3"
    ],
    "darkness": [
        "albw",
        "aquaria",
        "alttp",
        "dkc",
        "minecraft",
        "tmc",
        "dkc2",
        "witness",
        "doom_ii",
        "zelda2",
        "earthbound",
        "dkc3",
        "terraria",
        "sm_map_rando",
        "sm",
        "luigismansion",
        "ladx",
        "mm3",
        "rogue_legacy"
    ],
    "digital distribution": [
        "apeescape",
        "oot",
        "smw",
        "sotn",
        "albw",
        "dkc",
        "tunic",
        "minecraft",
        "quake",
        "mlss",
        "crosscode",
        "dkc2",
        "factorio",
        "doom_ii",
        "seaofthieves",
        "timespinner",
        "tloz_oos",
        "tmc",
        "witness",
        "cuphead",
        "ufo50",
        "civ_6",
        "oribf",
        "wl4",
        "celeste",
        "terraria",
        "dontstarvetogether",
        "v6",
        "yoshisisland",
        "musedash",
        "huniepop2",
        "sm64hacks",
        "getting_over_it",
        "sm64ex",
        "heretic",
        "dlcquest",
        "dk64",
        "ladx",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "digital": [
        "apeescape",
        "oot",
        "smw",
        "sotn",
        "albw",
        "dkc",
        "tunic",
        "minecraft",
        "quake",
        "mlss",
        "crosscode",
        "dkc2",
        "factorio",
        "doom_ii",
        "seaofthieves",
        "timespinner",
        "tloz_oos",
        "tmc",
        "witness",
        "cuphead",
        "ufo50",
        "civ_6",
        "oribf",
        "wl4",
        "celeste",
        "terraria",
        "dontstarvetogether",
        "v6",
        "yoshisisland",
        "musedash",
        "huniepop2",
        "sm64hacks",
        "getting_over_it",
        "sm64ex",
        "heretic",
        "dlcquest",
        "dk64",
        "ladx",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "distribution": [
        "apeescape",
        "oot",
        "smw",
        "sotn",
        "albw",
        "dkc",
        "tunic",
        "minecraft",
        "quake",
        "mlss",
        "crosscode",
        "dkc2",
        "factorio",
        "doom_ii",
        "seaofthieves",
        "timespinner",
        "tloz_oos",
        "tmc",
        "witness",
        "cuphead",
        "ufo50",
        "civ_6",
        "oribf",
        "wl4",
        "celeste",
        "terraria",
        "dontstarvetogether",
        "v6",
        "yoshisisland",
        "musedash",
        "huniepop2",
        "sm64hacks",
        "getting_over_it",
        "sm64ex",
        "heretic",
        "dlcquest",
        "dk64",
        "ladx",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "anthropomorphism": [
        "sms",
        "apeescape",
        "mk64",
        "diddy_kong_racing",
        "albw",
        "sonic_heroes",
        "dkc",
        "papermario",
        "tunic",
        "jakanddaxter",
        "spyro3",
        "mlss",
        "star_fox_64",
        "tmc",
        "dkc2",
        "tloz_oos",
        "cv64",
        "cuphead",
        "hcniko",
        "dkc3",
        "tloz_ooa",
        "k64",
        "kh1",
        "undertale",
        "dk64",
        "sly1",
        "banjo_tooie"
    ],
    "polygonal 3d": [
        "sms",
        "apeescape",
        "mk64",
        "oot",
        "sotn",
        "albw",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "spyro3",
        "star_fox_64",
        "witness",
        "xenobladex",
        "cv64",
        "ss",
        "k64",
        "dw1",
        "kh1",
        "lego_star_wars_tcs",
        "tloz_ph",
        "dk64",
        "luigismansion",
        "simpsonshitnrun",
        "sly1"
    ],
    "polygonal": [
        "sms",
        "apeescape",
        "mk64",
        "oot",
        "sotn",
        "albw",
        "minecraft",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "spyro3",
        "star_fox_64",
        "witness",
        "xenobladex",
        "cv64",
        "ss",
        "k64",
        "dw1",
        "kh1",
        "lego_star_wars_tcs",
        "tloz_ph",
        "dk64",
        "luigismansion",
        "simpsonshitnrun",
        "sly1"
    ],
    "bow and arrow": [
        "oot",
        "ror1",
        "tloz_ph",
        "terraria",
        "ss",
        "ladx",
        "dark_souls_2",
        "albw",
        "tloz_oos",
        "tmc",
        "poe",
        "ffta",
        "alttp",
        "cuphead",
        "rogue_legacy",
        "minecraft"
    ],
    "bow": [
        "oot",
        "ror1",
        "tloz_ph",
        "terraria",
        "ss",
        "ladx",
        "dark_souls_2",
        "albw",
        "tloz_oos",
        "tmc",
        "poe",
        "ffta",
        "alttp",
        "cuphead",
        "rogue_legacy",
        "minecraft"
    ],
    "and": [
        "oot",
        "dark_souls_2",
        "albw",
        "openrct2",
        "alttp",
        "hades",
        "minecraft",
        "jakanddaxter",
        "quake",
        "ror1",
        "tmc",
        "tloz_oos",
        "doom_ii",
        "cv64",
        "cuphead",
        "civ_6",
        "oribf",
        "terraria",
        "ss",
        "smz3",
        "tloz_ph",
        "blasphemous",
        "ladx",
        "sly1",
        "poe",
        "ffta",
        "mmx3",
        "rogue_legacy"
    ],
    "arrow": [
        "oot",
        "ror1",
        "tloz_ph",
        "terraria",
        "ss",
        "ladx",
        "dark_souls_2",
        "albw",
        "tloz_oos",
        "tmc",
        "poe",
        "ffta",
        "alttp",
        "cuphead",
        "rogue_legacy",
        "minecraft"
    ],
    "damsel in distress": [
        "sms",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "smw",
        "ss",
        "tloz_ooa",
        "tmc",
        "albw",
        "tloz_oos",
        "zelda2",
        "alttp",
        "kh1",
        "papermario",
        "earthbound"
    ],
    "damsel": [
        "sms",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "smw",
        "ss",
        "tloz_ooa",
        "tmc",
        "albw",
        "tloz_oos",
        "zelda2",
        "alttp",
        "kh1",
        "papermario",
        "earthbound"
    ],
    "distress": [
        "sms",
        "metroidprime",
        "oot",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "smw",
        "ss",
        "tloz_ooa",
        "tmc",
        "albw",
        "tloz_oos",
        "zelda2",
        "alttp",
        "kh1",
        "papermario",
        "earthbound"
    ],
    "upgradeable weapons": [
        "metroidprime",
        "mzm",
        "dk64",
        "dark_souls_2",
        "albw",
        "tmc",
        "mmx3",
        "cv64",
        "mm2"
    ],
    "upgradeable": [
        "metroidprime",
        "mzm",
        "dk64",
        "dark_souls_2",
        "albw",
        "tmc",
        "mmx3",
        "cv64",
        "mm2"
    ],
    "weapons": [
        "metroidprime",
        "mzm",
        "dk64",
        "dark_souls_2",
        "albw",
        "tmc",
        "mmx3",
        "cv64",
        "mm2"
    ],
    "disorientation zone": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tmc",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "disorientation": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tmc",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "zone": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tmc",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "descendants of other characters": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "sms",
        "dk64",
        "luigismansion",
        "sotn",
        "star_fox_64",
        "sly1",
        "tloz_ooa",
        "tmc",
        "dkc2",
        "albw",
        "dkc",
        "cv64",
        "earthbound",
        "dkc3",
        "rogue_legacy"
    ],
    "descendants": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "sms",
        "dk64",
        "luigismansion",
        "sotn",
        "star_fox_64",
        "sly1",
        "tloz_ooa",
        "tmc",
        "dkc2",
        "albw",
        "dkc",
        "cv64",
        "earthbound",
        "dkc3",
        "rogue_legacy"
    ],
    "other": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "sms",
        "dk64",
        "luigismansion",
        "sotn",
        "star_fox_64",
        "sly1",
        "tloz_ooa",
        "tmc",
        "dkc2",
        "albw",
        "dkc",
        "cv64",
        "earthbound",
        "dkc3",
        "rogue_legacy"
    ],
    "characters": [
        "sms",
        "mm_recomp",
        "oot",
        "sotn",
        "dark_souls_2",
        "albw",
        "dkc",
        "jakanddaxter",
        "star_fox_64",
        "tmc",
        "dkc2",
        "stardew_valley",
        "xenobladex",
        "cv64",
        "earthbound",
        "dkc3",
        "terraria",
        "tloz_ooa",
        "dark_souls_3",
        "lego_star_wars_tcs",
        "dk64",
        "luigismansion",
        "sly1",
        "rogue_legacy"
    ],
    "save point": [
        "sotn",
        "albw",
        "aquaria",
        "dkc",
        "gstla",
        "papermario",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "cvcotm",
        "mlss",
        "dkc2",
        "cv64",
        "earthbound",
        "dkc3",
        "v6",
        "kh1",
        "mzm",
        "sm_map_rando",
        "sm",
        "luigismansion"
    ],
    "save": [
        "sotn",
        "albw",
        "aquaria",
        "dkc",
        "gstla",
        "papermario",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "cvcotm",
        "mlss",
        "dkc2",
        "cv64",
        "earthbound",
        "dkc3",
        "v6",
        "kh1",
        "mzm",
        "sm_map_rando",
        "sm",
        "luigismansion"
    ],
    "point": [
        "sotn",
        "albw",
        "aquaria",
        "dkc",
        "gstla",
        "papermario",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "cvcotm",
        "mlss",
        "dkc2",
        "cv64",
        "earthbound",
        "dkc3",
        "v6",
        "kh1",
        "mzm",
        "sm_map_rando",
        "sm",
        "luigismansion"
    ],
    "stereoscopic 3d": [
        "luigismansion",
        "sly1",
        "v6",
        "albw",
        "minecraft"
    ],
    "stereoscopic": [
        "luigismansion",
        "sly1",
        "v6",
        "albw",
        "minecraft"
    ],
    "side quests": [
        "oot",
        "tloz_ph",
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "albw",
        "pokemon_crystal",
        "tloz_oos",
        "tmc",
        "xenobladex",
        "alttp",
        "pokemon_emerald",
        "sc2"
    ],
    "side": [
        "oot",
        "tetrisattack",
        "smw",
        "sotn",
        "noita",
        "dark_souls_2",
        "albw",
        "pokemon_crystal",
        "wargroove2",
        "aquaria",
        "alttp",
        "dkc",
        "kdl3",
        "papermario",
        "wl",
        "sc2",
        "ffmq",
        "faxanadu",
        "ror1",
        "zillion",
        "cvcotm",
        "mlss",
        "aus",
        "monster_sanctuary",
        "tmc",
        "dkc2",
        "tloz_oos",
        "enderlilies",
        "timespinner",
        "xenobladex",
        "marioland2",
        "zelda2",
        "cuphead",
        "ufo50",
        "wargroove",
        "ff1",
        "dkc3",
        "oribf",
        "wl4",
        "celeste",
        "terraria",
        "tloz_ooa",
        "lufia2ac",
        "v6",
        "pokemon_rb",
        "yoshisisland",
        "k64",
        "musedash",
        "messenger",
        "mm2",
        "momodoramoonlitfarewell",
        "pokemon_emerald",
        "pokemon_frlg",
        "getting_over_it",
        "smz3",
        "mzm",
        "animal_well",
        "dlcquest",
        "sm_map_rando",
        "sm",
        "megamix",
        "tloz_ph",
        "blasphemous",
        "ladx",
        "dungeon_clawler",
        "mm3",
        "hk",
        "mmx3",
        "hylics2",
        "spire",
        "rogue_legacy",
        "ff4fe"
    ],
    "quests": [
        "metroidprime",
        "oot",
        "tloz_ph",
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "albw",
        "pokemon_crystal",
        "tloz_oos",
        "tmc",
        "xenobladex",
        "alttp",
        "zelda2",
        "pokemon_emerald",
        "sc2"
    ],
    "potion": [
        "tloz_ph",
        "ss",
        "ladx",
        "tmc",
        "albw",
        "pokemon_crystal",
        "tloz_oos",
        "poe",
        "zelda2",
        "gstla",
        "kh1",
        "alttp",
        "pokemon_emerald",
        "rogue_legacy",
        "minecraft"
    ],
    "real-time combat": [
        "sms",
        "oot",
        "doom_1993",
        "sotn",
        "dark_souls_2",
        "albw",
        "dkc",
        "alttp",
        "minecraft",
        "spyro3",
        "metroidprime",
        "quake",
        "tmc",
        "tloz_oos",
        "xenobladex",
        "doom_ii",
        "zelda2",
        "cv64",
        "landstalker",
        "ss",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "sm64ex",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "ladx"
    ],
    "real-time": [
        "sms",
        "oot",
        "doom_1993",
        "sotn",
        "dark_souls_2",
        "albw",
        "dkc",
        "alttp",
        "minecraft",
        "spyro3",
        "metroidprime",
        "quake",
        "tmc",
        "tloz_oos",
        "xenobladex",
        "doom_ii",
        "zelda2",
        "cv64",
        "landstalker",
        "ss",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "sm64ex",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "ladx"
    ],
    "combat": [
        "sms",
        "oot",
        "doom_1993",
        "sotn",
        "dark_souls_2",
        "albw",
        "dkc",
        "alttp",
        "minecraft",
        "spyro3",
        "metroidprime",
        "quake",
        "tmc",
        "tloz_oos",
        "xenobladex",
        "doom_ii",
        "zelda2",
        "cv64",
        "landstalker",
        "ss",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "sm64ex",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "ladx"
    ],
    "self-referential humor": [
        "mlss",
        "dkc2",
        "albw",
        "papermario",
        "earthbound"
    ],
    "self-referential": [
        "mlss",
        "dkc2",
        "albw",
        "papermario",
        "earthbound"
    ],
    "humor": [
        "mlss",
        "dkc2",
        "albw",
        "papermario",
        "earthbound"
    ],
    "multiple gameplay perspectives": [
        "metroidprime",
        "tloz_ooa",
        "tloz_oos",
        "albw",
        "minecraft"
    ],
    "multiple": [
        "apeescape",
        "sotn",
        "dark_souls_2",
        "albw",
        "sonic_heroes",
        "dkc",
        "alttp",
        "minecraft",
        "spyro3",
        "metroidprime",
        "mlss",
        "star_fox_64",
        "tmc",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "witness",
        "cv64",
        "cuphead",
        "civ_6",
        "earthbound",
        "wl4",
        "dkc3",
        "tloz_ooa",
        "k64",
        "kh1",
        "lego_star_wars_tcs",
        "mzm",
        "undertale",
        "dk64",
        "mm3",
        "mmx3",
        "rogue_legacy"
    ],
    "gameplay": [
        "sms",
        "oot",
        "albw",
        "aquaria",
        "dkc",
        "minecraft",
        "smo",
        "metroidprime",
        "quake",
        "dkc2",
        "tloz_oos",
        "subnautica",
        "terraria",
        "tloz_ooa",
        "kh1",
        "sm64hacks",
        "mm2",
        "sm64ex",
        "mm3",
        "mmx3",
        "banjo_tooie"
    ],
    "perspectives": [
        "metroidprime",
        "tloz_ooa",
        "tloz_oos",
        "albw",
        "minecraft"
    ],
    "rpg elements": [
        "lego_star_wars_tcs",
        "mzm",
        "mlss",
        "sotn",
        "dark_souls_2",
        "albw",
        "zelda2",
        "banjo_tooie",
        "oribf",
        "minecraft"
    ],
    "rpg": [
        "lego_star_wars_tcs",
        "mzm",
        "mlss",
        "sotn",
        "dark_souls_2",
        "albw",
        "zelda2",
        "banjo_tooie",
        "oribf",
        "minecraft"
    ],
    "elements": [
        "lego_star_wars_tcs",
        "mzm",
        "mlss",
        "sotn",
        "dark_souls_2",
        "albw",
        "zelda2",
        "banjo_tooie",
        "oribf",
        "minecraft"
    ],
    "mercenary": [
        "metroidprime",
        "oot",
        "quake",
        "sm_map_rando",
        "sm",
        "ss",
        "dark_souls_2",
        "albw",
        "alttp",
        "sc2"
    ],
    "coming of age": [
        "jakanddaxter",
        "oot",
        "tmc",
        "albw",
        "pokemon_crystal",
        "ffta",
        "alttp",
        "pokemon_emerald",
        "oribf"
    ],
    "coming": [
        "jakanddaxter",
        "oot",
        "tmc",
        "albw",
        "pokemon_crystal",
        "ffta",
        "alttp",
        "pokemon_emerald",
        "oribf"
    ],
    "age": [
        "jakanddaxter",
        "oot",
        "tmc",
        "albw",
        "pokemon_crystal",
        "factorio_saws",
        "ffta",
        "gstla",
        "alttp",
        "pokemon_emerald",
        "oribf"
    ],
    "dimension travel": [
        "doom_ii",
        "mm_recomp",
        "alttp",
        "albw"
    ],
    "dimension": [
        "doom_ii",
        "mm_recomp",
        "alttp",
        "albw"
    ],
    "androgyny": [
        "oot",
        "sotn",
        "ss",
        "albw",
        "ffta",
        "gstla"
    ],
    "fast traveling": [
        "oot",
        "tloz_ph",
        "undertale",
        "tmc",
        "albw",
        "hk",
        "poe",
        "alttp",
        "pokemon_emerald"
    ],
    "fast": [
        "oot",
        "tloz_ph",
        "undertale",
        "tmc",
        "albw",
        "hk",
        "poe",
        "alttp",
        "pokemon_emerald"
    ],
    "traveling": [
        "oot",
        "tloz_ph",
        "undertale",
        "tmc",
        "albw",
        "hk",
        "poe",
        "alttp",
        "pokemon_emerald"
    ],
    "context sensitive": [
        "oot",
        "tloz_ph",
        "ss",
        "tloz_ooa",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "context": [
        "oot",
        "tloz_ph",
        "ss",
        "tloz_ooa",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "sensitive": [
        "oot",
        "tloz_ph",
        "ss",
        "tloz_ooa",
        "albw",
        "tloz_oos",
        "alttp"
    ],
    "living inventory": [
        "mm_recomp",
        "oot",
        "tww",
        "ss",
        "tmc",
        "albw",
        "alttp"
    ],
    "living": [
        "mm_recomp",
        "oot",
        "tww",
        "ss",
        "tmc",
        "albw",
        "alttp"
    ],
    "inventory": [
        "mm_recomp",
        "oot",
        "tww",
        "ss",
        "tmc",
        "albw",
        "alttp"
    ],
    "bees": [
        "tloz_ph",
        "terraria",
        "dontstarvetogether",
        "albw",
        "alttp",
        "minecraft",
        "raft"
    ],
    "a link to the past": [
        "alttp"
    ],
    "the legend of zelda: a link to the past": [
        "alttp"
    ],
    "to": [
        "alttp",
        "smz3"
    ],
    "past": [
        "alttp",
        "smz3"
    ],
    "satellaview": [
        "alttp",
        "yoshisisland"
    ],
    "super nintendo entertainment system": [
        "ffmq",
        "sm_map_rando",
        "tetrisattack",
        "soe",
        "sm",
        "smw",
        "smz3",
        "lufia2ac",
        "dkc2",
        "yoshisisland",
        "dkc",
        "alttp",
        "kdl3",
        "mmx3",
        "earthbound",
        "dkc3",
        "ff4fe"
    ],
    "super": [
        "sms",
        "tetrisattack",
        "smw",
        "dkc",
        "alttp",
        "kdl3",
        "wl",
        "ffmq",
        "smo",
        "dkc2",
        "marioland2",
        "earthbound",
        "dkc3",
        "lufia2ac",
        "yoshisisland",
        "sm64hacks",
        "sm64ex",
        "smz3",
        "sm_map_rando",
        "sm",
        "mmx3",
        "soe",
        "ff4fe"
    ],
    "entertainment": [
        "tetrisattack",
        "smw",
        "dkc",
        "alttp",
        "kdl3",
        "ffmq",
        "faxanadu",
        "dkc2",
        "zelda2",
        "earthbound",
        "ff1",
        "dkc3",
        "tloz",
        "lufia2ac",
        "yoshisisland",
        "smz3",
        "sm_map_rando",
        "sm",
        "mm3",
        "mmx3",
        "soe",
        "ff4fe"
    ],
    "wii": [
        "mm_recomp",
        "mk64",
        "oot",
        "smw",
        "dkc",
        "alttp",
        "gstla",
        "kdl3",
        "papermario",
        "ffmq",
        "faxanadu",
        "cvcotm",
        "mlss",
        "star_fox_64",
        "tmc",
        "dkc2",
        "stardew_valley",
        "xenobladex",
        "zelda2",
        "landstalker",
        "earthbound",
        "ff1",
        "dkc3",
        "wl4",
        "tloz",
        "terraria",
        "ss",
        "k64",
        "pmd_eos",
        "sm64hacks",
        "sm64ex",
        "lego_star_wars_tcs",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "tp",
        "mm3",
        "hk",
        "ffta",
        "mmx3",
        "ff4fe"
    ],
    "wii u": [
        "mm_recomp",
        "mk64",
        "oot",
        "smw",
        "dkc",
        "alttp",
        "gstla",
        "kdl3",
        "papermario",
        "ffmq",
        "cvcotm",
        "mlss",
        "star_fox_64",
        "tmc",
        "dkc2",
        "stardew_valley",
        "xenobladex",
        "zelda2",
        "earthbound",
        "ff1",
        "dkc3",
        "wl4",
        "tloz",
        "terraria",
        "ss",
        "k64",
        "pmd_eos",
        "sm64hacks",
        "sm64ex",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "mm3",
        "hk",
        "ffta",
        "mmx3"
    ],
    "u": [
        "mm_recomp",
        "mk64",
        "oot",
        "smw",
        "dkc",
        "alttp",
        "gstla",
        "kdl3",
        "papermario",
        "ffmq",
        "cvcotm",
        "mlss",
        "star_fox_64",
        "tmc",
        "dkc2",
        "stardew_valley",
        "xenobladex",
        "zelda2",
        "earthbound",
        "ff1",
        "dkc3",
        "wl4",
        "tloz",
        "terraria",
        "ss",
        "k64",
        "pmd_eos",
        "sm64hacks",
        "sm64ex",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "mm3",
        "hk",
        "ffta",
        "mmx3"
    ],
    "new nintendo 3ds": [
        "sm_map_rando",
        "sm",
        "smw",
        "dkc2",
        "dkc",
        "alttp",
        "mmx3",
        "earthbound",
        "dkc3"
    ],
    "new": [
        "sm_map_rando",
        "sm",
        "smw",
        "dkc2",
        "dkc",
        "alttp",
        "mmx3",
        "earthbound",
        "dkc3"
    ],
    "super famicom": [
        "ffmq",
        "sm_map_rando",
        "sm",
        "smw",
        "lufia2ac",
        "dkc2",
        "yoshisisland",
        "dkc",
        "alttp",
        "kdl3",
        "mmx3",
        "earthbound",
        "dkc3"
    ],
    "famicom": [
        "ffmq",
        "sm_map_rando",
        "sm",
        "smw",
        "lufia2ac",
        "dkc2",
        "yoshisisland",
        "dkc",
        "alttp",
        "kdl3",
        "mmx3",
        "earthbound",
        "dkc3"
    ],
    "ghosts": [
        "sms",
        "sotn",
        "alttp",
        "papermario",
        "ffmq",
        "metroidprime",
        "mlss",
        "aus",
        "tmc",
        "dkc2",
        "cv64",
        "cuphead",
        "earthbound",
        "wl4",
        "tloz_ooa",
        "v6",
        "lego_star_wars_tcs",
        "luigismansion",
        "simpsonshitnrun",
        "sly1",
        "rogue_legacy"
    ],
    "mascot": [
        "jakanddaxter",
        "spyro3",
        "tloz_ph",
        "ladx",
        "mm3",
        "sly1",
        "tloz_oos",
        "tmc",
        "k64",
        "kdl3",
        "alttp",
        "papermario",
        "mm2"
    ],
    "death": [
        "sms",
        "mk64",
        "oot",
        "sotn",
        "dark_souls_2",
        "openrct2",
        "dkc",
        "alttp",
        "gstla",
        "papermario",
        "minecraft",
        "metroidprime",
        "quake",
        "cvcotm",
        "star_fox_64",
        "tmc",
        "tloz_oos",
        "doom_ii",
        "zelda2",
        "cv64",
        "terraria",
        "tloz_ooa",
        "v6",
        "kh1",
        "dark_souls_3",
        "mm2",
        "mzm",
        "heretic",
        "tloz_ph",
        "dk64",
        "luigismansion",
        "ladx",
        "mm3",
        "sly1",
        "ffta",
        "mmx3",
        "rogue_legacy"
    ],
    "maze": [
        "mzm",
        "doom_1993",
        "ladx",
        "tmc",
        "witness",
        "openrct2",
        "alttp",
        "cv64",
        "papermario"
    ],
    "backtracking": [
        "oot",
        "sotn",
        "alttp",
        "jakanddaxter",
        "faxanadu",
        "metroidprime",
        "quake",
        "cvcotm",
        "tmc",
        "tloz_oos",
        "witness",
        "cv64",
        "kh1",
        "mzm",
        "tloz_ph",
        "undertale",
        "ladx",
        "ffta",
        "banjo_tooie"
    ],
    "undead": [
        "ffmq",
        "heretic",
        "oot",
        "mlss",
        "terraria",
        "sotn",
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "tloz_oos",
        "tmc",
        "alttp",
        "cv64",
        "papermario",
        "dsr"
    ],
    "campaign": [
        "oot",
        "tloz_ph",
        "ss",
        "tloz_ooa",
        "ladx",
        "tmc",
        "tloz_oos",
        "zelda2",
        "alttp"
    ],
    "portals": [
        "quake",
        "alttp",
        "wl4",
        "tloz_oos"
    ],
    "pixel art": [
        "sotn",
        "alttp",
        "ror1",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "tmc",
        "timespinner",
        "zelda2",
        "wargroove",
        "wl4",
        "hcniko",
        "celeste",
        "terraria",
        "v6",
        "mm2",
        "tyrian",
        "mzm",
        "animal_well",
        "sm_map_rando",
        "undertale",
        "sm",
        "blasphemous",
        "ladx",
        "mm3",
        "rogue_legacy"
    ],
    "pixel": [
        "sotn",
        "alttp",
        "ror1",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "tmc",
        "timespinner",
        "zelda2",
        "wargroove",
        "wl4",
        "hcniko",
        "celeste",
        "terraria",
        "v6",
        "mm2",
        "tyrian",
        "mzm",
        "animal_well",
        "sm_map_rando",
        "undertale",
        "sm",
        "blasphemous",
        "ladx",
        "mm3",
        "rogue_legacy"
    ],
    "art": [
        "sotn",
        "alttp",
        "ror1",
        "crosscode",
        "stardew_valley",
        "tloz_oos",
        "tmc",
        "timespinner",
        "zelda2",
        "wargroove",
        "wl4",
        "hcniko",
        "celeste",
        "terraria",
        "v6",
        "mm2",
        "tyrian",
        "mzm",
        "animal_well",
        "sm_map_rando",
        "undertale",
        "sm",
        "blasphemous",
        "ladx",
        "mm3",
        "rogue_legacy"
    ],
    "easter egg": [
        "apeescape",
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "easter": [
        "apeescape",
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "egg": [
        "apeescape",
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "teleportation": [
        "jakanddaxter",
        "terraria",
        "v6",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "doom_ii",
        "alttp",
        "cv64",
        "pokemon_emerald",
        "earthbound",
        "rogue_legacy"
    ],
    "giant insects": [
        "sms",
        "dk64",
        "mlss",
        "dkc2",
        "hk",
        "dkc",
        "alttp",
        "pokemon_emerald",
        "soe",
        "dkc3"
    ],
    "giant": [
        "sms",
        "dk64",
        "mlss",
        "dkc2",
        "hk",
        "dkc",
        "alttp",
        "pokemon_emerald",
        "soe",
        "dkc3"
    ],
    "insects": [
        "sms",
        "dk64",
        "mlss",
        "dkc2",
        "hk",
        "dkc",
        "alttp",
        "pokemon_emerald",
        "soe",
        "dkc3"
    ],
    "silent protagonist": [
        "oot",
        "ultrakill",
        "doom_1993",
        "dkc",
        "alttp",
        "gstla",
        "papermario",
        "jakanddaxter",
        "quake",
        "mlss",
        "tmc",
        "dkc2",
        "tloz_oos",
        "zelda2",
        "ss",
        "tloz_ooa",
        "k64",
        "pokemon_emerald",
        "tloz_ph",
        "blasphemous",
        "ladx",
        "hk"
    ],
    "silent": [
        "oot",
        "ultrakill",
        "doom_1993",
        "dkc",
        "alttp",
        "gstla",
        "papermario",
        "jakanddaxter",
        "quake",
        "mlss",
        "tmc",
        "dkc2",
        "tloz_oos",
        "zelda2",
        "ss",
        "tloz_ooa",
        "k64",
        "pokemon_emerald",
        "tloz_ph",
        "blasphemous",
        "ladx",
        "hk"
    ],
    "explosion": [
        "sms",
        "mk64",
        "sotn",
        "openrct2",
        "sonic_heroes",
        "alttp",
        "minecraft",
        "ffmq",
        "metroidprime",
        "quake",
        "tmc",
        "dkc2",
        "doom_ii",
        "zelda2",
        "cv64",
        "cuphead",
        "dkc3",
        "terraria",
        "tloz_ooa",
        "mm2",
        "lego_star_wars_tcs",
        "mzm",
        "sm_map_rando",
        "sm",
        "simpsonshitnrun",
        "mm3",
        "ffta",
        "mmx3",
        "rogue_legacy"
    ],
    "block puzzle": [
        "oot",
        "alttp",
        "tloz_ooa",
        "tloz_oos"
    ],
    "block": [
        "oot",
        "alttp",
        "tloz_ooa",
        "tloz_oos"
    ],
    "monkey": [
        "apeescape",
        "mk64",
        "dk64",
        "ladx",
        "diddy_kong_racing",
        "dkc2",
        "dkc",
        "alttp",
        "dkc3"
    ],
    "nintendo power": [
        "sm_map_rando",
        "sm",
        "dkc2",
        "dkc",
        "alttp",
        "earthbound",
        "dkc3"
    ],
    "power": [
        "sm_map_rando",
        "sm",
        "dkc2",
        "dkc",
        "alttp",
        "earthbound",
        "dkc3"
    ],
    "world map": [
        "jakanddaxter",
        "metroidprime",
        "oot",
        "tloz_ph",
        "ladx",
        "v6",
        "tmc",
        "dkc2",
        "pokemon_crystal",
        "tloz_oos",
        "aquaria",
        "alttp",
        "dkc",
        "dkc3"
    ],
    "map": [
        "jakanddaxter",
        "metroidprime",
        "oot",
        "tloz_ph",
        "ladx",
        "v6",
        "tmc",
        "dkc2",
        "pokemon_crystal",
        "tloz_oos",
        "aquaria",
        "alttp",
        "dkc",
        "dkc3"
    ],
    "human": [
        "sms",
        "apeescape",
        "quake",
        "tloz_ph",
        "terraria",
        "sotn",
        "simpsonshitnrun",
        "ladx",
        "ss",
        "dark_souls_2",
        "doom_ii",
        "zelda2",
        "alttp",
        "cv64",
        "gstla",
        "dark_souls_3",
        "papermario",
        "sc2"
    ],
    "shopping": [
        "lego_star_wars_tcs",
        "tloz_ph",
        "mlss",
        "yugiohddm",
        "sotn",
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "dw1",
        "alttp",
        "cv64",
        "cuphead",
        "pokemon_emerald"
    ],
    "ice stage": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "oot",
        "terraria",
        "tmc",
        "dkc2",
        "dkc",
        "alttp",
        "cv64",
        "banjo_tooie",
        "wl4",
        "dkc3"
    ],
    "ice": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "oot",
        "terraria",
        "tmc",
        "dkc2",
        "dkc",
        "alttp",
        "cv64",
        "banjo_tooie",
        "wl4",
        "dkc3"
    ],
    "stage": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "oot",
        "spyro3",
        "smw",
        "terraria",
        "tmc",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "alttp",
        "cv64",
        "banjo_tooie",
        "wl4",
        "dkc3"
    ],
    "saving the world": [
        "tloz_ph",
        "dark_souls_2",
        "tmc",
        "zelda2",
        "alttp",
        "earthbound"
    ],
    "saving": [
        "tloz_ph",
        "dark_souls_2",
        "tmc",
        "zelda2",
        "alttp",
        "earthbound"
    ],
    "grapple": [
        "lego_star_wars_tcs",
        "metroidprime",
        "oot",
        "tloz_ph",
        "tmc",
        "alttp"
    ],
    "secret area": [
        "heretic",
        "sm_map_rando",
        "sm",
        "sotn",
        "star_fox_64",
        "tunic",
        "diddy_kong_racing",
        "tmc",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "witness",
        "dkc",
        "alttp",
        "zelda2",
        "hcniko",
        "dkc3",
        "rogue_legacy"
    ],
    "secret": [
        "sotn",
        "diddy_kong_racing",
        "dkc",
        "alttp",
        "tunic",
        "quake",
        "star_fox_64",
        "tmc",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "witness",
        "zelda2",
        "hcniko",
        "dkc3",
        "dsr",
        "heretic",
        "sm_map_rando",
        "sm",
        "soe",
        "rogue_legacy"
    ],
    "area": [
        "heretic",
        "sm_map_rando",
        "sm",
        "sotn",
        "star_fox_64",
        "tunic",
        "diddy_kong_racing",
        "tmc",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "witness",
        "dkc",
        "alttp",
        "zelda2",
        "hcniko",
        "dkc3",
        "rogue_legacy"
    ],
    "shielded enemies": [
        "tloz_ooa",
        "tmc",
        "hk",
        "alttp",
        "dkc3",
        "rogue_legacy"
    ],
    "shielded": [
        "tloz_ooa",
        "tmc",
        "hk",
        "alttp",
        "dkc3",
        "rogue_legacy"
    ],
    "enemies": [
        "tloz_ooa",
        "tmc",
        "hk",
        "alttp",
        "kh1",
        "papermario",
        "wl4",
        "dkc3",
        "rogue_legacy"
    ],
    "walking through walls": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "doom_ii",
        "alttp"
    ],
    "walking": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "doom_ii",
        "alttp"
    ],
    "through": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "doom_ii",
        "alttp"
    ],
    "walls": [
        "oot",
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "doom_ii",
        "alttp"
    ],
    "liberation": [
        "lego_star_wars_tcs",
        "sm_map_rando",
        "sm",
        "dkc2",
        "alttp"
    ],
    "conveyor belt": [
        "mm2",
        "tloz_ooa",
        "alttp",
        "cuphead"
    ],
    "conveyor": [
        "mm2",
        "tloz_ooa",
        "alttp",
        "cuphead"
    ],
    "belt": [
        "mm2",
        "tloz_ooa",
        "alttp",
        "cuphead"
    ],
    "villain": [
        "lego_star_wars_tcs",
        "oot",
        "cvcotm",
        "sotn",
        "star_fox_64",
        "mm2",
        "mm3",
        "tloz_ooa",
        "tloz_oos",
        "tmc",
        "zelda2",
        "dkc",
        "gstla",
        "alttp",
        "kh1",
        "papermario",
        "banjo_tooie"
    ],
    "recurring boss": [
        "dk64",
        "mm3",
        "dkc2",
        "dkc",
        "alttp",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "banjo_tooie",
        "dkc3"
    ],
    "recurring": [
        "dk64",
        "mm3",
        "dkc2",
        "dkc",
        "alttp",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "banjo_tooie",
        "dkc3"
    ],
    "boss": [
        "sms",
        "mm_recomp",
        "oot",
        "dark_souls_2",
        "dkc",
        "alttp",
        "papermario",
        "metroidprime",
        "tmc",
        "dkc2",
        "doom_ii",
        "cuphead",
        "dkc3",
        "kh1",
        "pokemon_emerald",
        "tloz_ph",
        "dk64",
        "mm3",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "been here before": [
        "sms",
        "oot",
        "tloz_ph",
        "simpsonshitnrun",
        "tmc",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "alttp"
    ],
    "been": [
        "sms",
        "oot",
        "tloz_ph",
        "simpsonshitnrun",
        "tmc",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "alttp"
    ],
    "here": [
        "sms",
        "oot",
        "tloz_ph",
        "simpsonshitnrun",
        "tmc",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "alttp",
        "hcniko"
    ],
    "before": [
        "sms",
        "oot",
        "tloz_ph",
        "simpsonshitnrun",
        "tmc",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "alttp"
    ],
    "sleeping": [
        "sms",
        "tmc",
        "pokemon_crystal",
        "gstla",
        "alttp",
        "papermario",
        "minecraft"
    ],
    "merchants": [
        "faxanadu",
        "yugiohddm",
        "terraria",
        "hk",
        "timespinner",
        "alttp",
        "candybox2"
    ],
    "multiple enemy boss fights": [
        "mm3",
        "dark_souls_2",
        "tmc",
        "alttp",
        "cuphead"
    ],
    "enemy": [
        "oot",
        "mm3",
        "dark_souls_2",
        "dkc2",
        "tmc",
        "dkc",
        "alttp",
        "cuphead",
        "rogue_legacy"
    ],
    "fights": [
        "mm3",
        "dark_souls_2",
        "tmc",
        "alttp",
        "cuphead"
    ],
    "fetch quests": [
        "metroidprime",
        "tloz_ph",
        "ladx",
        "tmc",
        "tloz_oos",
        "zelda2",
        "alttp"
    ],
    "fetch": [
        "metroidprime",
        "tloz_ph",
        "ladx",
        "tmc",
        "tloz_oos",
        "zelda2",
        "alttp"
    ],
    "kidnapping": [
        "sms",
        "yoshisisland",
        "openrct2",
        "alttp",
        "earthbound"
    ],
    "poisoning": [
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "alttp",
        "cv64",
        "papermario",
        "pokemon_emerald",
        "minecraft"
    ],
    "time paradox": [
        "jakanddaxter",
        "oot",
        "tloz_ooa",
        "alttp",
        "cv64"
    ],
    "paradox": [
        "jakanddaxter",
        "oot",
        "tloz_ooa",
        "alttp",
        "cv64"
    ],
    "falling object": [
        "mk64",
        "alttp",
        "mm3",
        "tmc"
    ],
    "falling": [
        "metroidprime",
        "mk64",
        "oot",
        "terraria",
        "mm3",
        "tmc",
        "alttp",
        "cv64",
        "minecraft"
    ],
    "object": [
        "mk64",
        "alttp",
        "mm3",
        "tmc"
    ],
    "status effects": [
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "tloz_oos",
        "pokemon_crystal",
        "tmc",
        "zelda2",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "status": [
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "tloz_oos",
        "pokemon_crystal",
        "tmc",
        "zelda2",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "effects": [
        "tloz_ooa",
        "ladx",
        "dark_souls_2",
        "tloz_oos",
        "pokemon_crystal",
        "tmc",
        "zelda2",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "minecraft"
    ],
    "hidden room": [
        "doom_ii",
        "heretic",
        "alttp",
        "dark_souls_2"
    ],
    "hidden": [
        "doom_ii",
        "heretic",
        "alttp",
        "dark_souls_2"
    ],
    "room": [
        "doom_ii",
        "heretic",
        "alttp",
        "dark_souls_2"
    ],
    "another world": [
        "doom_ii",
        "mm_recomp",
        "alttp",
        "ladx"
    ],
    "another": [
        "doom_ii",
        "mm_recomp",
        "alttp",
        "ladx"
    ],
    "plane shifting": [
        "tloz_ooa",
        "alttp",
        "tmc",
        "tloz_oos"
    ],
    "plane": [
        "tloz_ooa",
        "alttp",
        "tmc",
        "tloz_oos"
    ],
    "shifting": [
        "tloz_ooa",
        "alttp",
        "tmc",
        "tloz_oos"
    ],
    "damage over time": [
        "jakanddaxter",
        "oot",
        "tloz_ph",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "ffta",
        "alttp",
        "pokemon_emerald"
    ],
    "damage": [
        "jakanddaxter",
        "metroidprime",
        "oot",
        "tloz_ph",
        "terraria",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "ffta",
        "alttp",
        "cv64",
        "pokemon_emerald",
        "minecraft"
    ],
    "over": [
        "jakanddaxter",
        "oot",
        "tloz_ph",
        "dk64",
        "sotn",
        "tmc",
        "tloz_oos",
        "pokemon_crystal",
        "doom_ii",
        "dkc",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "dkc3",
        "getting_over_it"
    ],
    "monomyth": [
        "tloz_ph",
        "ss",
        "mm3",
        "tmc",
        "zelda2",
        "alttp",
        "mm2"
    ],
    "buddy system": [
        "dkc",
        "alttp",
        "dkc3",
        "dkc2"
    ],
    "buddy": [
        "dkc",
        "alttp",
        "dkc3",
        "dkc2"
    ],
    "retroachievements": [
        "sms",
        "mm_recomp",
        "mk64",
        "oot",
        "tetrisattack",
        "smw",
        "diddy_kong_racing",
        "sonic_heroes",
        "dkc",
        "alttp",
        "kdl3",
        "papermario",
        "ffmq",
        "quake",
        "star_fox_64",
        "dkc2",
        "cv64",
        "earthbound",
        "dkc3",
        "tloz",
        "lufia2ac",
        "k64",
        "sm64hacks",
        "sm64ex",
        "dk64",
        "mmx3",
        "banjo_tooie",
        "ff4fe"
    ],
    "animal well": [
        "animal_well"
    ],
    "animal": [
        "oot",
        "animal_well",
        "ladx",
        "pokemon_crystal",
        "pokemon_emerald"
    ],
    "well": [
        "animal_well"
    ],
    "side view": [
        "tetrisattack",
        "smw",
        "sotn",
        "noita",
        "pokemon_crystal",
        "wargroove2",
        "aquaria",
        "dkc",
        "kdl3",
        "papermario",
        "wl",
        "ffmq",
        "faxanadu",
        "ror1",
        "zillion",
        "cvcotm",
        "mlss",
        "aus",
        "monster_sanctuary",
        "dkc2",
        "enderlilies",
        "timespinner",
        "zelda2",
        "marioland2",
        "cuphead",
        "ufo50",
        "wargroove",
        "ff1",
        "dkc3",
        "oribf",
        "wl4",
        "celeste",
        "terraria",
        "lufia2ac",
        "v6",
        "pokemon_rb",
        "yoshisisland",
        "k64",
        "musedash",
        "messenger",
        "mm2",
        "momodoramoonlitfarewell",
        "pokemon_emerald",
        "pokemon_frlg",
        "getting_over_it",
        "smz3",
        "mzm",
        "animal_well",
        "dlcquest",
        "sm_map_rando",
        "sm",
        "megamix",
        "blasphemous",
        "ladx",
        "dungeon_clawler",
        "mm3",
        "hk",
        "mmx3",
        "hylics2",
        "spire",
        "rogue_legacy",
        "ff4fe"
    ],
    "horror": [
        "mm_recomp",
        "shivers",
        "doom_1993",
        "residentevil3remake",
        "sotn",
        "lethal_company",
        "quake",
        "cvcotm",
        "doom_ii",
        "cv64",
        "residentevil2remake",
        "terraria",
        "dontstarvetogether",
        "inscryption",
        "getting_over_it",
        "animal_well",
        "undertale",
        "luigismansion",
        "blasphemous",
        "poe"
    ],
    "survival": [
        "lethal_company",
        "ror2",
        "ror1",
        "animal_well",
        "subnautica",
        "residentevil3remake",
        "terraria",
        "residentevil2remake",
        "dontstarvetogether",
        "factorio",
        "dungeon_clawler",
        "factorio_saws",
        "yugioh06",
        "rimworld",
        "minecraft",
        "raft"
    ],
    "mystery": [
        "animal_well",
        "outer_wilds",
        "witness",
        "pmd_eos",
        "inscryption"
    ],
    "exploration": [
        "outer_wilds",
        "pokemon_crystal",
        "aquaria",
        "lingo",
        "tunic",
        "jakanddaxter",
        "lethal_company",
        "metroidprime",
        "seaofthieves",
        "witness",
        "cv64",
        "hcniko",
        "shorthike",
        "celeste",
        "subnautica",
        "terraria",
        "v6",
        "pokemon_emerald",
        "dlcquest",
        "animal_well",
        "sm_map_rando",
        "sm",
        "tloz_ph",
        "hylics2",
        "rogue_legacy"
    ],
    "retro": [
        "smo",
        "dlcquest",
        "animal_well",
        "undertale",
        "terraria",
        "blasphemous",
        "v6",
        "stardew_valley",
        "timespinner",
        "hylics2",
        "cuphead",
        "messenger",
        "ufo50",
        "minecraft",
        "celeste"
    ],
    "dark": [
        "animal_well",
        "undertale",
        "dark_souls_2",
        "hk",
        "dark_souls_3",
        "dsr"
    ],
    "2d": [
        "sotn",
        "smo",
        "stardew_valley",
        "zelda2",
        "cuphead",
        "earthbound",
        "celeste",
        "terraria",
        "dontstarvetogether",
        "v6",
        "musedash",
        "animal_well",
        "sm_map_rando",
        "undertale",
        "sm",
        "blasphemous",
        "hk",
        "hylics2",
        "messenger"
    ],
    "metroidvania": [
        "sotn",
        "dark_souls_2",
        "aquaria",
        "faxanadu",
        "metroidprime",
        "zillion",
        "cvcotm",
        "monster_sanctuary",
        "aus",
        "enderlilies",
        "timespinner",
        "zelda2",
        "oribf",
        "v6",
        "momodoramoonlitfarewell",
        "mzm",
        "animal_well",
        "sm_map_rando",
        "sm",
        "blasphemous",
        "hk",
        "pseudoregalia",
        "rogue_legacy",
        "messenger"
    ],
    "atmospheric": [
        "animal_well",
        "dontstarvetogether",
        "hk",
        "powerwashsimulator",
        "hylics2",
        "tunic",
        "celeste"
    ],
    "relaxing": [
        "animal_well",
        "stardew_valley",
        "powerwashsimulator",
        "sims4",
        "hcniko",
        "shorthike"
    ],
    "controller support": [
        "animal_well",
        "v6",
        "stardew_valley",
        "hk",
        "hcniko",
        "tunic"
    ],
    "controller": [
        "animal_well",
        "v6",
        "stardew_valley",
        "hk",
        "hcniko",
        "tunic"
    ],
    "support": [
        "animal_well",
        "v6",
        "stardew_valley",
        "hk",
        "ffta",
        "gstla",
        "cv64",
        "kh1",
        "fm",
        "hcniko",
        "tunic"
    ],
    "ape escape": [
        "apeescape"
    ],
    "ape": [
        "apeescape",
        "mk64",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "escape": [
        "apeescape"
    ],
    "playstation 3": [
        "lego_star_wars_tcs",
        "apeescape",
        "sadx",
        "spyro3",
        "terraria",
        "sotn",
        "dark_souls_2",
        "kh2",
        "sa2b",
        "rogue_legacy"
    ],
    "3": [
        "lego_star_wars_tcs",
        "apeescape",
        "mmbn3",
        "sadx",
        "spyro3",
        "residentevil3remake",
        "terraria",
        "sotn",
        "mm3",
        "dark_souls_2",
        "kh2",
        "kdl3",
        "wl",
        "sa2b",
        "rogue_legacy"
    ],
    "playstation portable": [
        "spyro3",
        "apeescape",
        "sotn"
    ],
    "portable": [
        "spyro3",
        "apeescape",
        "sotn"
    ],
    "anime": [
        "apeescape",
        "zillion",
        "osu",
        "yugiohddm",
        "pokemon_emerald",
        "huniepop",
        "pokemon_crystal",
        "dw1",
        "gstla",
        "musedash",
        "huniepop2",
        "fm",
        "wl4"
    ],
    "dinosaurs": [
        "smo",
        "apeescape",
        "sms",
        "smw",
        "yoshisisland",
        "banjo_tooie",
        "earthbound"
    ],
    "collecting": [
        "apeescape",
        "mzm",
        "pokemon_rb",
        "pokemon_crystal",
        "zelda2",
        "pokemon_emerald",
        "banjo_tooie",
        "pokemon_frlg"
    ],
    "multiple endings": [
        "apeescape",
        "metroidprime",
        "mzm",
        "undertale",
        "dk64",
        "sotn",
        "star_fox_64",
        "witness",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "k64",
        "mmx3",
        "kh1",
        "cv64",
        "cuphead",
        "civ_6",
        "wl4"
    ],
    "endings": [
        "apeescape",
        "metroidprime",
        "mzm",
        "undertale",
        "dk64",
        "sotn",
        "star_fox_64",
        "witness",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "k64",
        "mmx3",
        "kh1",
        "cv64",
        "cuphead",
        "civ_6",
        "wl4"
    ],
    "amnesia": [
        "apeescape",
        "tloz_ph",
        "witness",
        "xenobladex",
        "sonic_heroes",
        "aquaria"
    ],
    "voice acting": [
        "jakanddaxter",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "star_fox_64",
        "witness",
        "xenobladex",
        "doom_ii",
        "sonic_heroes",
        "dw1",
        "kh1",
        "cv64",
        "huniepop2",
        "cuphead",
        "civ_6"
    ],
    "voice": [
        "jakanddaxter",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "star_fox_64",
        "witness",
        "xenobladex",
        "doom_ii",
        "sonic_heroes",
        "dw1",
        "kh1",
        "cv64",
        "huniepop2",
        "cuphead",
        "civ_6"
    ],
    "acting": [
        "jakanddaxter",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "star_fox_64",
        "witness",
        "xenobladex",
        "doom_ii",
        "sonic_heroes",
        "dw1",
        "kh1",
        "cv64",
        "huniepop2",
        "cuphead",
        "civ_6"
    ],
    "psone classics": [
        "spyro3",
        "apeescape",
        "sotn",
        "mm3",
        "mm2"
    ],
    "psone": [
        "spyro3",
        "apeescape",
        "sotn",
        "mm3",
        "mm2"
    ],
    "classics": [
        "spyro3",
        "apeescape",
        "sotn",
        "mm3",
        "mm2"
    ],
    "moving platforms": [
        "sms",
        "apeescape",
        "sotn",
        "sonic_heroes",
        "dkc",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "spyro3",
        "cvcotm",
        "tmc",
        "cv64",
        "wl4",
        "dkc3",
        "v6",
        "k64",
        "mm2",
        "tloz_ph",
        "dk64",
        "blasphemous",
        "ladx",
        "mm3",
        "sly1",
        "mmx3"
    ],
    "moving": [
        "sms",
        "apeescape",
        "sotn",
        "sonic_heroes",
        "dkc",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "spyro3",
        "cvcotm",
        "tmc",
        "cv64",
        "wl4",
        "dkc3",
        "v6",
        "k64",
        "mm2",
        "tloz_ph",
        "dk64",
        "blasphemous",
        "ladx",
        "mm3",
        "sly1",
        "mmx3"
    ],
    "platforms": [
        "sms",
        "apeescape",
        "sotn",
        "sonic_heroes",
        "dkc",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "quake",
        "spyro3",
        "cvcotm",
        "tmc",
        "doom_ii",
        "zelda2",
        "cv64",
        "oribf",
        "dkc3",
        "wl4",
        "v6",
        "k64",
        "mm2",
        "sm_map_rando",
        "tloz_ph",
        "dk64",
        "sm",
        "blasphemous",
        "ladx",
        "mm3",
        "sly1",
        "mmx3"
    ],
    "spiky-haired protagonist": [
        "jakanddaxter",
        "apeescape",
        "simpsonshitnrun",
        "sonic_heroes",
        "kh1"
    ],
    "spiky-haired": [
        "jakanddaxter",
        "apeescape",
        "simpsonshitnrun",
        "sonic_heroes",
        "kh1"
    ],
    "time trials": [
        "spyro3",
        "apeescape",
        "mk64",
        "sly1",
        "diddy_kong_racing",
        "v6"
    ],
    "trials": [
        "spyro3",
        "apeescape",
        "mk64",
        "sly1",
        "diddy_kong_racing",
        "v6"
    ],
    "sudoku": [
        "apsudoku"
    ],
    "multiplayer": [
        "tracker",
        "chatipelago",
        "debug",
        "generic",
        "archipidle",
        "apsudoku",
        "jigsaw",
        "clique",
        "paint",
        "wordipelago",
        "saving_princess",
        "yachtdice",
        "checksfinder"
    ],
    "archipelago": [
        "clique",
        "tracker",
        "chatipelago",
        "bumpstik",
        "debug",
        "archipidle",
        "generic",
        "jigsaw",
        "apsudoku",
        "paint",
        "wordipelago",
        "saving_princess",
        "yachtdice",
        "checksfinder"
    ],
    "hints": [
        "tracker",
        "chatipelago",
        "debug",
        "generic",
        "archipidle",
        "apsudoku",
        "jigsaw",
        "clique",
        "paint",
        "wordipelago",
        "saving_princess",
        "yachtdice",
        "checksfinder"
    ],
    "multiworld": [
        "tracker",
        "chatipelago",
        "debug",
        "generic",
        "archipidle",
        "apsudoku",
        "jigsaw",
        "clique",
        "paint",
        "wordipelago",
        "saving_princess",
        "yachtdice",
        "checksfinder"
    ],
    "aquaria": [
        "aquaria"
    ],
    "drama": [
        "earthbound",
        "aquaria",
        "undertale",
        "hades"
    ],
    "linux": [
        "doom_1993",
        "overcooked2",
        "chainedechoes",
        "openrct2",
        "aquaria",
        "rimworld",
        "minecraft",
        "quake",
        "ror1",
        "monster_sanctuary",
        "osu",
        "crosscode",
        "factorio",
        "huniepop",
        "stardew_valley",
        "factorio_saws",
        "timespinner",
        "landstalker",
        "shorthike",
        "celeste",
        "cat_quest",
        "celeste64",
        "terraria",
        "dontstarvetogether",
        "v6",
        "bumpstik",
        "inscryption",
        "getting_over_it",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "hk",
        "rogue_legacy",
        "shapez"
    ],
    "android": [
        "cat_quest",
        "lego_star_wars_tcs",
        "subnautica",
        "balatro",
        "osu",
        "terraria",
        "osrs",
        "blasphemous",
        "v6",
        "dungeon_clawler",
        "stardew_valley",
        "aquaria",
        "musedash",
        "brotato",
        "getting_over_it",
        "shapez"
    ],
    "ios": [
        "balatro",
        "residentevil3remake",
        "aquaria",
        "hades",
        "osu",
        "osrs",
        "witness",
        "stardew_valley",
        "residentevil2remake",
        "cat_quest",
        "subnautica",
        "terraria",
        "v6",
        "musedash",
        "brotato",
        "getting_over_it",
        "lego_star_wars_tcs",
        "blasphemous",
        "dungeon_clawler",
        "shapez"
    ],
    "alternate costumes": [
        "lego_star_wars_tcs",
        "smo",
        "sms",
        "simpsonshitnrun",
        "aquaria",
        "kh1",
        "cv64"
    ],
    "alternate": [
        "lego_star_wars_tcs",
        "smo",
        "sms",
        "simpsonshitnrun",
        "aquaria",
        "kh1",
        "cv64"
    ],
    "costumes": [
        "lego_star_wars_tcs",
        "smo",
        "sms",
        "simpsonshitnrun",
        "aquaria",
        "kh1",
        "cv64"
    ],
    "underwater gameplay": [
        "smo",
        "metroidprime",
        "oot",
        "quake",
        "sms",
        "subnautica",
        "terraria",
        "mm2",
        "mm3",
        "dkc2",
        "aquaria",
        "kh1",
        "dkc",
        "mmx3",
        "sm64hacks",
        "banjo_tooie",
        "sm64ex"
    ],
    "underwater": [
        "smo",
        "metroidprime",
        "oot",
        "quake",
        "sms",
        "subnautica",
        "terraria",
        "mm2",
        "mm3",
        "dkc2",
        "aquaria",
        "kh1",
        "dkc",
        "mmx3",
        "sm64hacks",
        "banjo_tooie",
        "sm64ex"
    ],
    "shape-shifting": [
        "metroidprime",
        "mm_recomp",
        "sotn",
        "k64",
        "aquaria",
        "kdl3",
        "banjo_tooie"
    ],
    "plot twist": [
        "oot",
        "undertale",
        "aquaria",
        "kh1",
        "cv64"
    ],
    "plot": [
        "oot",
        "undertale",
        "aquaria",
        "kh1",
        "cv64"
    ],
    "twist": [
        "oot",
        "undertale",
        "aquaria",
        "kh1",
        "cv64"
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
        "undertale",
        "aus",
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "celeste"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "balatro",
        "chainedechoes",
        "wargroove2",
        "papermario",
        "monster_sanctuary",
        "civ_6",
        "wargroove",
        "earthbound",
        "pokemon_rb",
        "pmd_eos",
        "pokemon_emerald",
        "yugioh06",
        "pokemon_frlg",
        "undertale",
        "yugiohddm",
        "dungeon_clawler",
        "ffta",
        "hylics2",
        "fm"
    ],
    "turn-based": [
        "balatro",
        "chainedechoes",
        "pokemon_crystal",
        "wargroove2",
        "gstla",
        "papermario",
        "ffmq",
        "monster_sanctuary",
        "mlss",
        "civ_6",
        "earthbound",
        "wargroove",
        "pokemon_rb",
        "pmd_eos",
        "pokemon_emerald",
        "yugioh06",
        "pokemon_frlg",
        "undertale",
        "yugiohddm",
        "dungeon_clawler",
        "ffta",
        "hylics2",
        "fm"
    ],
    "(tbs)": [
        "balatro",
        "chainedechoes",
        "wargroove2",
        "papermario",
        "monster_sanctuary",
        "civ_6",
        "wargroove",
        "earthbound",
        "pokemon_rb",
        "pmd_eos",
        "pokemon_emerald",
        "yugioh06",
        "pokemon_frlg",
        "undertale",
        "yugiohddm",
        "dungeon_clawler",
        "ffta",
        "hylics2",
        "fm"
    ],
    "card & board game": [
        "balatro",
        "yugiohddm",
        "spire",
        "yugioh06",
        "inscryption",
        "fm"
    ],
    "card": [
        "balatro",
        "yugiohddm",
        "spire",
        "yugioh06",
        "inscryption",
        "fm"
    ],
    "board": [
        "balatro",
        "yugiohddm",
        "spire",
        "yugioh06",
        "inscryption",
        "fm"
    ],
    "game": [
        "oot",
        "balatro",
        "pokemon_crystal",
        "gstla",
        "wl",
        "hades",
        "smo",
        "mmbn3",
        "spyro3",
        "cvcotm",
        "mlss",
        "tmc",
        "dkc2",
        "tloz_oos",
        "doom_ii",
        "witness",
        "marioland2",
        "cuphead",
        "earthbound",
        "wl4",
        "hcniko",
        "celeste",
        "ss",
        "tloz_ooa",
        "pokemon_rb",
        "pokemon_emerald",
        "mm2",
        "inscryption",
        "yugioh06",
        "pokemon_frlg",
        "mzm",
        "tloz_ph",
        "dk64",
        "yugiohddm",
        "ladx",
        "ffta",
        "fm",
        "spire",
        "rogue_legacy"
    ],
    "roguelike": [
        "ror1",
        "balatro",
        "dungeon_clawler",
        "hades",
        "pmd_eos",
        "spire",
        "rogue_legacy"
    ],
    "banjo-tooie": [
        "banjo_tooie"
    ],
    "comedy": [
        "doronko_wanko",
        "diddy_kong_racing",
        "overcooked2",
        "placidplasticducksim",
        "papermario",
        "jakanddaxter",
        "lethal_company",
        "quake",
        "spyro3",
        "mlss",
        "huniepop",
        "dkc2",
        "cuphead",
        "candybox2",
        "hcniko",
        "rac2",
        "dw1",
        "kh1",
        "musedash",
        "getting_over_it",
        "lego_star_wars_tcs",
        "dlcquest",
        "undertale",
        "dk64",
        "luigismansion",
        "simpsonshitnrun",
        "sly1",
        "toontown",
        "banjo_tooie",
        "zork_grand_inquisitor",
        "sims4",
        "rogue_legacy",
        "messenger"
    ],
    "nintendo 64": [
        "mm_recomp",
        "mk64",
        "oot",
        "swr",
        "dk64",
        "star_fox_64",
        "diddy_kong_racing",
        "k64",
        "cv64",
        "papermario",
        "sm64hacks",
        "banjo_tooie",
        "sm64ex"
    ],
    "64": [
        "mm_recomp",
        "mk64",
        "oot",
        "swr",
        "dk64",
        "star_fox_64",
        "diddy_kong_racing",
        "k64",
        "cv64",
        "papermario",
        "sm64hacks",
        "banjo_tooie",
        "sm64ex"
    ],
    "aliens": [
        "lego_star_wars_tcs",
        "lethal_company",
        "metroidprime",
        "mzm",
        "quake",
        "sm_map_rando",
        "sm",
        "simpsonshitnrun",
        "factorio",
        "xenobladex",
        "factorio_saws",
        "banjo_tooie",
        "earthbound",
        "hcniko",
        "sc2"
    ],
    "animals": [
        "star_fox_64",
        "sly1",
        "diddy_kong_racing",
        "dkc2",
        "stardew_valley",
        "dkc",
        "hcniko",
        "banjo_tooie",
        "dkc3",
        "minecraft"
    ],
    "flight": [
        "lego_star_wars_tcs",
        "spyro3",
        "terraria",
        "star_fox_64",
        "mm2",
        "diddy_kong_racing",
        "mm3",
        "xenobladex",
        "dkc",
        "hylics2",
        "banjo_tooie",
        "wl4",
        "rogue_legacy",
        "shorthike"
    ],
    "witches": [
        "tloz_ooa",
        "tmc",
        "tloz_oos",
        "enderlilies",
        "cv64",
        "banjo_tooie",
        "minecraft"
    ],
    "achievements": [
        "lego_star_wars_tcs",
        "sotn",
        "blasphemous",
        "v6",
        "dark_souls_2",
        "stardew_valley",
        "doom_ii",
        "hk",
        "sonic_heroes",
        "musedash",
        "huniepop2",
        "cuphead",
        "banjo_tooie",
        "oribf",
        "hcniko",
        "tunic",
        "minecraft"
    ],
    "talking animals": [
        "star_fox_64",
        "sly1",
        "diddy_kong_racing",
        "dkc2",
        "dkc",
        "hcniko",
        "banjo_tooie",
        "dkc3"
    ],
    "talking": [
        "star_fox_64",
        "sly1",
        "diddy_kong_racing",
        "dkc2",
        "dkc",
        "hcniko",
        "banjo_tooie",
        "dkc3"
    ],
    "breaking the fourth wall": [
        "jakanddaxter",
        "undertale",
        "mlss",
        "simpsonshitnrun",
        "ladx",
        "tmc",
        "dkc2",
        "doom_ii",
        "ffta",
        "dkc",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "breaking": [
        "oot",
        "sotn",
        "dkc",
        "papermario",
        "jakanddaxter",
        "metroidprime",
        "mlss",
        "tmc",
        "dkc2",
        "doom_ii",
        "wl4",
        "tloz_ooa",
        "mzm",
        "sm_map_rando",
        "undertale",
        "sm",
        "simpsonshitnrun",
        "ladx",
        "ffta",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "fourth": [
        "jakanddaxter",
        "undertale",
        "mlss",
        "simpsonshitnrun",
        "ladx",
        "tmc",
        "dkc2",
        "doom_ii",
        "ffta",
        "dkc",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "cameo appearance": [
        "jakanddaxter",
        "spyro3",
        "oot",
        "dkc2",
        "banjo_tooie"
    ],
    "cameo": [
        "jakanddaxter",
        "spyro3",
        "oot",
        "dkc2",
        "banjo_tooie"
    ],
    "appearance": [
        "jakanddaxter",
        "spyro3",
        "oot",
        "dkc2",
        "banjo_tooie"
    ],
    "character growth": [
        "banjo_tooie",
        "oot",
        "dk64",
        "pokemon_crystal"
    ],
    "character": [
        "lego_star_wars_tcs",
        "mk64",
        "oot",
        "dk64",
        "dkc2",
        "pokemon_crystal",
        "sonic_heroes",
        "dkc",
        "cv64",
        "pokemon_emerald",
        "banjo_tooie",
        "dkc3",
        "minecraft"
    ],
    "growth": [
        "banjo_tooie",
        "oot",
        "dk64",
        "pokemon_crystal"
    ],
    "invisible wall": [
        "mk64",
        "oot",
        "dk64",
        "kh1",
        "banjo_tooie"
    ],
    "invisible": [
        "mk64",
        "oot",
        "dk64",
        "kh1",
        "banjo_tooie"
    ],
    "temporary invincibility": [
        "jakanddaxter",
        "faxanadu",
        "mk64",
        "quake",
        "dkc2",
        "doom_ii",
        "sonic_heroes",
        "cuphead",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "temporary": [
        "jakanddaxter",
        "faxanadu",
        "mk64",
        "quake",
        "dkc2",
        "doom_ii",
        "sonic_heroes",
        "cuphead",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "invincibility": [
        "jakanddaxter",
        "faxanadu",
        "mk64",
        "quake",
        "dkc2",
        "doom_ii",
        "sonic_heroes",
        "cuphead",
        "papermario",
        "banjo_tooie",
        "rogue_legacy"
    ],
    "gliding": [
        "spyro3",
        "sms",
        "sly1",
        "tmc",
        "kh1",
        "banjo_tooie"
    ],
    "lgbtq+": [
        "celeste64",
        "simpsonshitnrun",
        "timespinner",
        "banjo_tooie",
        "sims4",
        "rogue_legacy",
        "celeste"
    ],
    "blasphemous": [
        "blasphemous"
    ],
    "role-playing (rpg)": [
        "sotn",
        "noita",
        "dark_souls_2",
        "chainedechoes",
        "pokemon_crystal",
        "wargroove2",
        "gstla",
        "papermario",
        "hades",
        "tunic",
        "ffmq",
        "faxanadu",
        "mmbn3",
        "ror1",
        "cvcotm",
        "mlss",
        "ctjot",
        "monster_sanctuary",
        "bomb_rush_cyberfunk",
        "osrs",
        "crosscode",
        "huniepop",
        "kh2",
        "enderlilies",
        "stardew_valley",
        "timespinner",
        "tloz_oos",
        "xenobladex",
        "zelda2",
        "ufo50",
        "landstalker",
        "earthbound",
        "candybox2",
        "ff1",
        "cat_quest",
        "terraria",
        "tloz_ooa",
        "lufia2ac",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "kh1",
        "brotato",
        "dark_souls_3",
        "pokemon_emerald",
        "pokemon_frlg",
        "dsr",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "hylics2",
        "toontown",
        "soe",
        "sims4",
        "rogue_legacy",
        "ff4fe"
    ],
    "role-playing": [
        "sotn",
        "noita",
        "dark_souls_2",
        "chainedechoes",
        "pokemon_crystal",
        "wargroove2",
        "gstla",
        "papermario",
        "hades",
        "tunic",
        "ffmq",
        "faxanadu",
        "mmbn3",
        "ror1",
        "cvcotm",
        "mlss",
        "ctjot",
        "monster_sanctuary",
        "bomb_rush_cyberfunk",
        "osrs",
        "crosscode",
        "huniepop",
        "kh2",
        "enderlilies",
        "stardew_valley",
        "timespinner",
        "tloz_oos",
        "xenobladex",
        "zelda2",
        "ufo50",
        "landstalker",
        "earthbound",
        "candybox2",
        "ff1",
        "cat_quest",
        "terraria",
        "tloz_ooa",
        "lufia2ac",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "kh1",
        "brotato",
        "dark_souls_3",
        "pokemon_emerald",
        "pokemon_frlg",
        "dsr",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "hylics2",
        "toontown",
        "soe",
        "sims4",
        "rogue_legacy",
        "ff4fe"
    ],
    "(rpg)": [
        "sotn",
        "noita",
        "dark_souls_2",
        "chainedechoes",
        "pokemon_crystal",
        "wargroove2",
        "gstla",
        "papermario",
        "hades",
        "tunic",
        "ffmq",
        "faxanadu",
        "mmbn3",
        "ror1",
        "cvcotm",
        "mlss",
        "ctjot",
        "monster_sanctuary",
        "bomb_rush_cyberfunk",
        "osrs",
        "crosscode",
        "huniepop",
        "kh2",
        "enderlilies",
        "stardew_valley",
        "timespinner",
        "tloz_oos",
        "xenobladex",
        "zelda2",
        "ufo50",
        "landstalker",
        "earthbound",
        "candybox2",
        "ff1",
        "cat_quest",
        "terraria",
        "tloz_ooa",
        "lufia2ac",
        "pokemon_rb",
        "pmd_eos",
        "dw1",
        "kh1",
        "brotato",
        "dark_souls_3",
        "pokemon_emerald",
        "pokemon_frlg",
        "dsr",
        "undertale",
        "blasphemous",
        "dungeon_clawler",
        "poe",
        "ffta",
        "meritous",
        "hylics2",
        "toontown",
        "soe",
        "sims4",
        "rogue_legacy",
        "ff4fe"
    ],
    "hack and slash/beat 'em up": [
        "ror1",
        "blasphemous",
        "poe",
        "cv64",
        "hades"
    ],
    "hack": [
        "ror1",
        "blasphemous",
        "poe",
        "cv64",
        "hades"
    ],
    "slash/beat": [
        "ror1",
        "blasphemous",
        "poe",
        "cv64",
        "hades"
    ],
    "'em": [
        "ror1",
        "blasphemous",
        "poe",
        "cv64",
        "hades"
    ],
    "up": [
        "ror1",
        "undertale",
        "cvcotm",
        "sotn",
        "blasphemous",
        "dark_souls_2",
        "pokemon_crystal",
        "zelda2",
        "poe",
        "dw1",
        "gstla",
        "cv64",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "landstalker",
        "earthbound",
        "hades"
    ],
    "bloody": [
        "metroidprime",
        "heretic",
        "quake",
        "ultrakill",
        "sotn",
        "blasphemous",
        "doom_ii",
        "poe",
        "cv64",
        "residentevil2remake"
    ],
    "difficult": [
        "ror1",
        "dontstarvetogether",
        "blasphemous",
        "tunic",
        "zelda2",
        "messenger",
        "hades",
        "getting_over_it",
        "celeste"
    ],
    "side-scrolling": [
        "sotn",
        "dkc",
        "kdl3",
        "dkc2",
        "zelda2",
        "cuphead",
        "dkc3",
        "yoshisisland",
        "k64",
        "musedash",
        "mm2",
        "mzm",
        "sm_map_rando",
        "sm",
        "blasphemous",
        "mm3",
        "mmx3",
        "hylics2",
        "rogue_legacy"
    ],
    "crossover": [
        "mk64",
        "blasphemous",
        "diddy_kong_racing",
        "kh1",
        "hcniko",
        "smz3"
    ],
    "religion": [
        "oot",
        "blasphemous",
        "cv64",
        "civ_6",
        "earthbound"
    ],
    "nudity": [
        "sotn",
        "blasphemous",
        "huniepop",
        "musedash",
        "huniepop2"
    ],
    "2d platformer": [
        "smo",
        "blasphemous",
        "v6",
        "hk",
        "hylics2"
    ],
    "great soundtrack": [
        "ultrakill",
        "undertale",
        "bomb_rush_cyberfunk",
        "blasphemous",
        "shorthike",
        "hylics2",
        "tunic",
        "getting_over_it",
        "celeste"
    ],
    "great": [
        "ultrakill",
        "undertale",
        "bomb_rush_cyberfunk",
        "blasphemous",
        "shorthike",
        "hylics2",
        "tunic",
        "getting_over_it",
        "celeste"
    ],
    "soundtrack": [
        "ultrakill",
        "undertale",
        "bomb_rush_cyberfunk",
        "blasphemous",
        "shorthike",
        "hylics2",
        "tunic",
        "getting_over_it",
        "celeste"
    ],
    "parrying": [
        "blasphemous",
        "dark_souls_2",
        "hk",
        "dark_souls_3",
        "cuphead"
    ],
    "soulslike": [
        "tunic",
        "blasphemous",
        "dark_souls_2",
        "enderlilies",
        "dark_souls_3",
        "dsr"
    ],
    "you can pet the dog": [
        "undertale",
        "terraria",
        "blasphemous",
        "seaofthieves",
        "overcooked2",
        "sims4",
        "hades"
    ],
    "you": [
        "undertale",
        "terraria",
        "blasphemous",
        "seaofthieves",
        "overcooked2",
        "sims4",
        "hades"
    ],
    "can": [
        "undertale",
        "terraria",
        "blasphemous",
        "seaofthieves",
        "overcooked2",
        "sims4",
        "hades"
    ],
    "pet": [
        "undertale",
        "terraria",
        "blasphemous",
        "seaofthieves",
        "overcooked2",
        "sims4",
        "hades"
    ],
    "dog": [
        "smo",
        "oot",
        "undertale",
        "doronko_wanko",
        "terraria",
        "star_fox_64",
        "blasphemous",
        "sly1",
        "overcooked2",
        "seaofthieves",
        "tloz_oos",
        "tmc",
        "cv64",
        "soe",
        "sims4",
        "hcniko",
        "hades",
        "minecraft"
    ],
    "interconnected-world": [
        "mzm",
        "sm_map_rando",
        "sm",
        "luigismansion",
        "sotn",
        "blasphemous",
        "dark_souls_2",
        "hk",
        "dark_souls_3",
        "dsr"
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
        "ultrakill",
        "outer_wilds",
        "doom_1993",
        "rimworld",
        "sc2",
        "jakanddaxter",
        "lethal_company",
        "metroidprime",
        "mmbn3",
        "quake",
        "ror1",
        "zillion",
        "ctjot",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "crosscode",
        "factorio",
        "witness",
        "doom_ii",
        "factorio_saws",
        "xenobladex",
        "swr",
        "earthbound",
        "ror2",
        "subnautica",
        "terraria",
        "rac2",
        "v6",
        "satisfactory",
        "brotato",
        "mm2",
        "pokemon_frlg",
        "tyrian",
        "lego_star_wars_tcs",
        "mzm",
        "sm_map_rando",
        "sm",
        "mm3",
        "mmx3",
        "soe"
    ],
    "science": [
        "ultrakill",
        "outer_wilds",
        "doom_1993",
        "rimworld",
        "sc2",
        "jakanddaxter",
        "lethal_company",
        "metroidprime",
        "mmbn3",
        "quake",
        "ror1",
        "zillion",
        "ctjot",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "crosscode",
        "factorio",
        "witness",
        "doom_ii",
        "factorio_saws",
        "xenobladex",
        "swr",
        "earthbound",
        "ror2",
        "subnautica",
        "terraria",
        "rac2",
        "v6",
        "satisfactory",
        "brotato",
        "mm2",
        "pokemon_frlg",
        "tyrian",
        "lego_star_wars_tcs",
        "mzm",
        "sm_map_rando",
        "sm",
        "mm3",
        "mmx3",
        "soe"
    ],
    "fiction": [
        "ultrakill",
        "outer_wilds",
        "doom_1993",
        "rimworld",
        "sc2",
        "jakanddaxter",
        "lethal_company",
        "metroidprime",
        "mmbn3",
        "quake",
        "ror1",
        "zillion",
        "ctjot",
        "bomb_rush_cyberfunk",
        "star_fox_64",
        "crosscode",
        "factorio",
        "witness",
        "doom_ii",
        "factorio_saws",
        "xenobladex",
        "swr",
        "earthbound",
        "ror2",
        "subnautica",
        "terraria",
        "rac2",
        "v6",
        "satisfactory",
        "brotato",
        "mm2",
        "pokemon_frlg",
        "tyrian",
        "lego_star_wars_tcs",
        "mzm",
        "sm_map_rando",
        "sm",
        "mm3",
        "mmx3",
        "soe"
    ],
    "spiritual successor": [
        "quake",
        "mlss",
        "bomb_rush_cyberfunk",
        "xenobladex",
        "papermario"
    ],
    "spiritual": [
        "quake",
        "mlss",
        "bomb_rush_cyberfunk",
        "xenobladex",
        "papermario"
    ],
    "successor": [
        "quake",
        "mlss",
        "bomb_rush_cyberfunk",
        "xenobladex",
        "papermario"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "ultrakill",
        "doom_1993",
        "residentevil3remake",
        "noita",
        "metroidprime",
        "quake",
        "ror1",
        "star_fox_64",
        "crosscode",
        "doom_ii",
        "cuphead",
        "ufo50",
        "residentevil2remake",
        "ror2",
        "rac2",
        "brotato",
        "tyrian",
        "mzm",
        "heretic",
        "sm_map_rando",
        "sm",
        "mmx3",
        "tboir"
    ],
    "arcade": [
        "mk64",
        "ultrakill",
        "osu",
        "megamix",
        "mario_kart_double_dash",
        "smw",
        "mm3",
        "dungeon_clawler",
        "noita",
        "overcooked2",
        "v6",
        "brotato",
        "cuphead",
        "trackmania",
        "tyrian",
        "ufo50",
        "messenger"
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
        "bumpstik",
        "minecraft"
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
    "2": [
        "jakanddaxter",
        "ror2",
        "smo",
        "rac2",
        "simpsonshitnrun",
        "sly1",
        "overcooked2",
        "kh2",
        "sonic_heroes",
        "wargroove2",
        "dw1",
        "kh1",
        "hylics2",
        "candybox2",
        "residentevil2remake"
    ],
    "text": [
        "osrs",
        "huniepop",
        "huniepop2",
        "yugioh06",
        "candybox2"
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
    "management": [
        "ffta",
        "rimworld",
        "civ_6",
        "candybox2",
        "sims4"
    ],
    "cat quest": [
        "cat_quest"
    ],
    "cat": [
        "cat_quest",
        "tmc",
        "dkc2",
        "tloz_oos",
        "kh1",
        "cuphead",
        "wl4",
        "minecraft"
    ],
    "quest": [
        "cat_quest",
        "dlcquest",
        "ffmq",
        "dkc2"
    ],
    "celeste": [
        "celeste64",
        "celeste"
    ],
    "google stadia": [
        "ror2",
        "terraria",
        "celeste"
    ],
    "google": [
        "ror2",
        "terraria",
        "celeste"
    ],
    "stadia": [
        "ror2",
        "terraria",
        "celeste"
    ],
    "story rich": [
        "undertale",
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "celeste"
    ],
    "rich": [
        "undertale",
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "celeste"
    ],
    "music": [
        "ultrakill",
        "sotn",
        "placidplasticducksim",
        "sonic_heroes",
        "dkc",
        "gstla",
        "hades",
        "ffmq",
        "metroidprime",
        "smo",
        "osu",
        "dkc2",
        "doom_ii",
        "cv64",
        "cuphead",
        "civ_6",
        "dkc3",
        "celeste",
        "musedash",
        "mzm",
        "megamix",
        "ffta",
        "soe"
    ],
    "conversation": [
        "enderlilies",
        "undertale",
        "v6",
        "celeste"
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
        "ffmq",
        "chainedechoes",
        "pmd_eos",
        "ffta",
        "hylics2",
        "ff1",
        "ff4fe"
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
        "jakanddaxter",
        "metroidprime",
        "ss",
        "gstla",
        "civ_6"
    ],
    "iv": [
        "civ_6"
    ],
    "educational": [
        "civ_6"
    ],
    "4x (explore, expand, exploit, and exterminate)": [
        "civ_6",
        "openrct2"
    ],
    "4x": [
        "civ_6",
        "openrct2"
    ],
    "(explore,": [
        "civ_6",
        "openrct2"
    ],
    "expand,": [
        "civ_6",
        "openrct2"
    ],
    "exploit,": [
        "civ_6",
        "openrct2"
    ],
    "exterminate)": [
        "civ_6",
        "openrct2"
    ],
    "construction": [
        "civ_6",
        "terraria",
        "xenobladex",
        "minecraft"
    ],
    "mining": [
        "civ_6",
        "terraria",
        "stardew_valley",
        "minecraft"
    ],
    "bink video": [
        "simpsonshitnrun",
        "witness",
        "poe",
        "dark_souls_3",
        "civ_6"
    ],
    "bink": [
        "simpsonshitnrun",
        "witness",
        "poe",
        "dark_souls_3",
        "civ_6"
    ],
    "video": [
        "simpsonshitnrun",
        "witness",
        "poe",
        "dark_souls_3",
        "civ_6"
    ],
    "loot gathering": [
        "dk64",
        "terraria",
        "xenobladex",
        "cv64",
        "civ_6",
        "minecraft"
    ],
    "loot": [
        "dk64",
        "terraria",
        "xenobladex",
        "cv64",
        "civ_6",
        "minecraft"
    ],
    "gathering": [
        "dk64",
        "terraria",
        "xenobladex",
        "cv64",
        "civ_6",
        "minecraft"
    ],
    "royalty": [
        "mlss",
        "tmc",
        "civ_6",
        "earthbound",
        "rogue_legacy"
    ],
    "ambient music": [
        "metroidprime",
        "mzm",
        "dkc2",
        "dkc",
        "cv64",
        "civ_6",
        "soe",
        "dkc3"
    ],
    "ambient": [
        "metroidprime",
        "mzm",
        "dkc2",
        "dkc",
        "cv64",
        "civ_6",
        "soe",
        "dkc3"
    ],
    "clique": [
        "clique"
    ],
    "crosscode": [
        "crosscode"
    ],
    "16-bit": [
        "sm_map_rando",
        "sm",
        "crosscode",
        "earthbound",
        "rogue_legacy"
    ],
    "a.i. companion": [
        "oot",
        "sotn",
        "star_fox_64",
        "crosscode",
        "kh1"
    ],
    "a.i.": [
        "oot",
        "sotn",
        "star_fox_64",
        "crosscode",
        "kh1"
    ],
    "companion": [
        "oot",
        "sotn",
        "star_fox_64",
        "crosscode",
        "kh1"
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
        "pmd_eos",
        "tloz_ph",
        "ctjot"
    ],
    "ds": [
        "pmd_eos",
        "tloz_ph",
        "ctjot"
    ],
    "cuphead": [
        "cuphead"
    ],
    "pirates": [
        "metroidprime",
        "mzm",
        "tloz_ph",
        "tloz_ooa",
        "seaofthieves",
        "dkc2",
        "tloz_oos",
        "wargroove2",
        "kh1",
        "cuphead"
    ],
    "shark": [
        "jakanddaxter",
        "dkc",
        "cuphead",
        "raft"
    ],
    "robots": [
        "lego_star_wars_tcs",
        "sms",
        "ultrakill",
        "star_fox_64",
        "mm3",
        "xenobladex",
        "sonic_heroes",
        "mmx3",
        "cuphead",
        "swr",
        "mm2",
        "earthbound"
    ],
    "run and gun": [
        "doom_ii",
        "mmx3",
        "quake",
        "cuphead"
    ],
    "run": [
        "quake",
        "simpsonshitnrun",
        "doom_ii",
        "mmx3",
        "cuphead"
    ],
    "gun": [
        "doom_ii",
        "mmx3",
        "quake",
        "cuphead"
    ],
    "dancing": [
        "dkc2",
        "tloz_ooa",
        "dkc3",
        "cuphead"
    ],
    "violent plants": [
        "sms",
        "metroidprime",
        "terraria",
        "ss",
        "cuphead",
        "rogue_legacy"
    ],
    "violent": [
        "sms",
        "metroidprime",
        "terraria",
        "ss",
        "cuphead",
        "rogue_legacy"
    ],
    "plants": [
        "sms",
        "metroidprime",
        "terraria",
        "ss",
        "cuphead",
        "rogue_legacy"
    ],
    "auto-scrolling levels": [
        "star_fox_64",
        "v6",
        "dkc2",
        "k64",
        "dkc",
        "cuphead",
        "dkc3"
    ],
    "auto-scrolling": [
        "star_fox_64",
        "v6",
        "dkc2",
        "k64",
        "dkc",
        "cuphead",
        "dkc3"
    ],
    "levels": [
        "star_fox_64",
        "v6",
        "dkc2",
        "k64",
        "dkc",
        "cuphead",
        "dkc3"
    ],
    "boss assistance": [
        "sms",
        "metroidprime",
        "mm_recomp",
        "oot",
        "tloz_ph",
        "dark_souls_2",
        "dkc2",
        "tmc",
        "doom_ii",
        "dkc",
        "cuphead",
        "papermario",
        "rogue_legacy"
    ],
    "assistance": [
        "sms",
        "metroidprime",
        "mm_recomp",
        "oot",
        "tloz_ph",
        "dark_souls_2",
        "dkc2",
        "tmc",
        "doom_ii",
        "dkc",
        "cuphead",
        "papermario",
        "rogue_legacy"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "summoning support": [
        "ffta",
        "gstla",
        "cv64",
        "kh1",
        "fm"
    ],
    "summoning": [
        "ffta",
        "gstla",
        "cv64",
        "kh1",
        "fm"
    ],
    "horse": [
        "oot",
        "cvcotm",
        "sotn",
        "cv64",
        "rogue_legacy",
        "minecraft"
    ],
    "multiple protagonists": [
        "lego_star_wars_tcs",
        "spyro3",
        "dk64",
        "mlss",
        "sotn",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "mmx3",
        "cv64",
        "earthbound",
        "dkc3",
        "rogue_legacy"
    ],
    "protagonists": [
        "lego_star_wars_tcs",
        "spyro3",
        "dk64",
        "mlss",
        "sotn",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "mmx3",
        "cv64",
        "earthbound",
        "dkc3",
        "rogue_legacy"
    ],
    "traps": [
        "dark_souls_2",
        "tmc",
        "doom_ii",
        "cv64",
        "rogue_legacy",
        "minecraft"
    ],
    "bats": [
        "mk64",
        "cvcotm",
        "terraria",
        "sotn",
        "pokemon_crystal",
        "zelda2",
        "cv64"
    ],
    "day/night cycle": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "tww",
        "dk64",
        "terraria",
        "sotn",
        "ss",
        "stardew_valley",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "minecraft"
    ],
    "day/night": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "tww",
        "dk64",
        "terraria",
        "sotn",
        "ss",
        "stardew_valley",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "minecraft"
    ],
    "cycle": [
        "jakanddaxter",
        "mm_recomp",
        "oot",
        "tww",
        "dk64",
        "terraria",
        "sotn",
        "ss",
        "stardew_valley",
        "pokemon_crystal",
        "xenobladex",
        "cv64",
        "minecraft"
    ],
    "character select screen": [
        "lego_star_wars_tcs",
        "mk64",
        "cv64",
        "dk64"
    ],
    "select": [
        "lego_star_wars_tcs",
        "mk64",
        "cv64",
        "dk64"
    ],
    "screen": [
        "lego_star_wars_tcs",
        "mk64",
        "dk64",
        "mlss",
        "pokemon_crystal",
        "gstla",
        "cv64",
        "papermario",
        "pokemon_emerald"
    ],
    "skeletons": [
        "heretic",
        "undertale",
        "cvcotm",
        "terraria",
        "sotn",
        "sly1",
        "seaofthieves",
        "cv64",
        "minecraft"
    ],
    "falling damage": [
        "metroidprime",
        "oot",
        "terraria",
        "cv64",
        "minecraft"
    ],
    "unstable platforms": [
        "sms",
        "metroidprime",
        "sm_map_rando",
        "cvcotm",
        "sm",
        "sly1",
        "v6",
        "tmc",
        "doom_ii",
        "zelda2",
        "dkc",
        "cv64",
        "oribf"
    ],
    "unstable": [
        "sms",
        "metroidprime",
        "sm_map_rando",
        "cvcotm",
        "sm",
        "sly1",
        "v6",
        "tmc",
        "doom_ii",
        "zelda2",
        "dkc",
        "cv64",
        "oribf"
    ],
    "melee": [
        "doom_1993",
        "sotn",
        "dark_souls_2",
        "pokemon_crystal",
        "kdl3",
        "gstla",
        "papermario",
        "quake",
        "cvcotm",
        "tmc",
        "doom_ii",
        "cv64",
        "wl4",
        "terraria",
        "k64",
        "kh1",
        "pokemon_emerald",
        "lego_star_wars_tcs",
        "heretic",
        "sly1",
        "ffta"
    ],
    "male antagonist": [
        "mm2",
        "earthbound",
        "cv64",
        "sms"
    ],
    "male": [
        "mm2",
        "earthbound",
        "cv64",
        "sms"
    ],
    "antagonist": [
        "mm2",
        "earthbound",
        "cv64",
        "sms"
    ],
    "instant kill": [
        "v6",
        "dkc2",
        "dkc",
        "cv64",
        "mm2"
    ],
    "instant": [
        "v6",
        "dkc2",
        "dkc",
        "cv64",
        "mm2"
    ],
    "kill": [
        "v6",
        "dkc2",
        "dkc",
        "cv64",
        "mm2"
    ],
    "difficulty level": [
        "metroidprime",
        "mk64",
        "mzm",
        "osu",
        "star_fox_64",
        "doom_ii",
        "musedash",
        "cv64",
        "mm2",
        "minecraft"
    ],
    "difficulty": [
        "metroidprime",
        "mk64",
        "mzm",
        "osu",
        "star_fox_64",
        "doom_ii",
        "musedash",
        "cv64",
        "mm2",
        "minecraft"
    ],
    "level": [
        "sms",
        "metroidprime",
        "mk64",
        "mzm",
        "oot",
        "osu",
        "star_fox_64",
        "dkc2",
        "doom_ii",
        "dkc",
        "kh1",
        "cv64",
        "musedash",
        "mm2",
        "minecraft"
    ],
    "drawbridge": [
        "oot",
        "cv64",
        "rogue_legacy",
        "tmc"
    ],
    "castlevania - circle of the moon": [
        "cvcotm"
    ],
    "castlevania: circle of the moon": [
        "cvcotm"
    ],
    "castlevania:": [
        "sotn",
        "cvcotm"
    ],
    "circle": [
        "cvcotm"
    ],
    "moon": [
        "cvcotm"
    ],
    "game boy advance": [
        "mmbn3",
        "mzm",
        "cvcotm",
        "mlss",
        "yugiohddm",
        "tmc",
        "ffta",
        "gstla",
        "yugioh06",
        "pokemon_emerald",
        "earthbound",
        "wl4",
        "pokemon_frlg"
    ],
    "boy": [
        "pokemon_crystal",
        "gstla",
        "wl",
        "mmbn3",
        "cvcotm",
        "mlss",
        "tmc",
        "tloz_oos",
        "marioland2",
        "earthbound",
        "wl4",
        "tloz_ooa",
        "pokemon_rb",
        "pokemon_emerald",
        "mm2",
        "yugioh06",
        "pokemon_frlg",
        "mzm",
        "yugiohddm",
        "ladx",
        "ffta"
    ],
    "advance": [
        "mmbn3",
        "mzm",
        "cvcotm",
        "mlss",
        "yugiohddm",
        "tmc",
        "ffta",
        "gstla",
        "yugioh06",
        "pokemon_emerald",
        "earthbound",
        "wl4",
        "pokemon_frlg"
    ],
    "gravity": [
        "lego_star_wars_tcs",
        "metroidprime",
        "mzm",
        "oot",
        "cvcotm",
        "dk64",
        "sotn",
        "star_fox_64",
        "v6",
        "dkc2",
        "dkc",
        "papermario",
        "dkc3"
    ],
    "wolf": [
        "cvcotm",
        "sotn",
        "star_fox_64",
        "rogue_legacy",
        "minecraft"
    ],
    "leveling up": [
        "undertale",
        "cvcotm",
        "sotn",
        "dark_souls_2",
        "pokemon_crystal",
        "zelda2",
        "poe",
        "dw1",
        "gstla",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "landstalker",
        "earthbound"
    ],
    "leveling": [
        "undertale",
        "cvcotm",
        "sotn",
        "dark_souls_2",
        "pokemon_crystal",
        "zelda2",
        "poe",
        "dw1",
        "gstla",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "landstalker",
        "earthbound"
    ],
    "dark souls ii": [
        "dark_souls_2"
    ],
    "souls": [
        "dark_souls_2",
        "dark_souls_3"
    ],
    "ii": [
        "dark_souls_2",
        "kh2",
        "spire",
        "mm2",
        "ff4fe"
    ],
    "xbox 360": [
        "lego_star_wars_tcs",
        "sadx",
        "dlcquest",
        "terraria",
        "sotn",
        "dark_souls_2",
        "sa2b"
    ],
    "360": [
        "lego_star_wars_tcs",
        "sadx",
        "dlcquest",
        "terraria",
        "sotn",
        "dark_souls_2",
        "sa2b"
    ],
    "spider": [
        "sly1",
        "dark_souls_2",
        "dkc2",
        "zelda2",
        "oribf",
        "minecraft"
    ],
    "customizable characters": [
        "lego_star_wars_tcs",
        "terraria",
        "dark_souls_2",
        "stardew_valley",
        "xenobladex",
        "dark_souls_3"
    ],
    "customizable": [
        "lego_star_wars_tcs",
        "terraria",
        "dark_souls_2",
        "stardew_valley",
        "xenobladex",
        "dark_souls_3"
    ],
    "checkpoints": [
        "jakanddaxter",
        "smo",
        "sly1",
        "mm3",
        "dark_souls_2",
        "dkc2",
        "v6",
        "sonic_heroes",
        "dkc",
        "mmx3",
        "mm2",
        "dkc3"
    ],
    "sliding down ladders": [
        "k64",
        "wl4",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "sliding": [
        "k64",
        "wl4",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "down": [
        "k64",
        "wl4",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "ladders": [
        "k64",
        "wl4",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "fire manipulation": [
        "dark_souls_2",
        "pokemon_crystal",
        "gstla",
        "papermario",
        "pokemon_emerald",
        "earthbound",
        "rogue_legacy",
        "minecraft"
    ],
    "fire": [
        "dark_souls_2",
        "pokemon_crystal",
        "gstla",
        "papermario",
        "pokemon_emerald",
        "earthbound",
        "rogue_legacy",
        "minecraft"
    ],
    "manipulation": [
        "oot",
        "sm_map_rando",
        "sm",
        "dark_souls_2",
        "pokemon_crystal",
        "timespinner",
        "gstla",
        "papermario",
        "pokemon_emerald",
        "earthbound",
        "rogue_legacy",
        "minecraft"
    ],
    "dark souls iii": [
        "dark_souls_3"
    ],
    "iii": [
        "zillion",
        "dark_souls_3"
    ],
    "pick your gender": [
        "terraria",
        "pokemon_emerald",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "pick": [
        "terraria",
        "pokemon_emerald",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "your": [
        "terraria",
        "pokemon_emerald",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "gender": [
        "terraria",
        "pokemon_emerald",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "entering world in a painting": [
        "smo",
        "sm64ex",
        "sm64hacks",
        "dark_souls_3"
    ],
    "entering": [
        "smo",
        "sm64ex",
        "sm64hacks",
        "dark_souls_3"
    ],
    "painting": [
        "smo",
        "sm64ex",
        "sm64hacks",
        "dark_souls_3"
    ],
    "debug": [
        "debug"
    ],
    "diddy kong racing": [
        "diddy_kong_racing"
    ],
    "diddy": [
        "diddy_kong_racing"
    ],
    "kong": [
        "dk64",
        "diddy_kong_racing",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "racing": [
        "jakanddaxter",
        "mk64",
        "mario_kart_double_dash",
        "simpsonshitnrun",
        "diddy_kong_racing",
        "trackmania",
        "swr"
    ],
    "go-kart": [
        "mario_kart_double_dash",
        "mk64",
        "diddy_kong_racing",
        "toontown"
    ],
    "behind the waterfall": [
        "smo",
        "sotn",
        "ss",
        "tloz_ooa",
        "diddy_kong_racing",
        "tmc",
        "gstla",
        "dkc3",
        "hcniko"
    ],
    "behind": [
        "smo",
        "sotn",
        "ss",
        "tloz_ooa",
        "diddy_kong_racing",
        "tmc",
        "gstla",
        "dkc3",
        "hcniko"
    ],
    "waterfall": [
        "smo",
        "sotn",
        "ss",
        "tloz_ooa",
        "diddy_kong_racing",
        "tmc",
        "gstla",
        "dkc3",
        "hcniko"
    ],
    "donkey kong 64": [
        "dk64"
    ],
    "donkey": [
        "dkc2",
        "dkc",
        "dkc3",
        "dk64"
    ],
    "artificial intelligence": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "dk64",
        "star_fox_64",
        "sly1",
        "doom_ii"
    ],
    "artificial": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "dk64",
        "star_fox_64",
        "sly1",
        "doom_ii"
    ],
    "intelligence": [
        "jakanddaxter",
        "metroidprime",
        "mk64",
        "dk64",
        "star_fox_64",
        "sly1",
        "doom_ii"
    ],
    "death match": [
        "heretic",
        "mk64",
        "quake",
        "dk64",
        "doom_ii"
    ],
    "match": [
        "heretic",
        "mk64",
        "quake",
        "dk64",
        "doom_ii"
    ],
    "gorilla": [
        "dkc2",
        "dkc",
        "dkc3",
        "dk64"
    ],
    "franchise reboot": [
        "ffmq",
        "ffta",
        "dkc",
        "dk64"
    ],
    "franchise": [
        "ffmq",
        "ffta",
        "dkc",
        "dk64"
    ],
    "reboot": [
        "ffmq",
        "ffta",
        "dkc",
        "dk64"
    ],
    "western games based on japanese ips": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "western": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "games": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "based": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "on": [
        "metroidprime",
        "dk64",
        "dkc2",
        "doom_ii",
        "dkc",
        "dkc3"
    ],
    "japanese": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "ips": [
        "metroidprime",
        "dk64",
        "dkc2",
        "dkc",
        "dkc3"
    ],
    "over 100% completion": [
        "dk64",
        "sotn",
        "doom_ii",
        "dkc",
        "dkc3"
    ],
    "100%": [
        "dk64",
        "sotn",
        "doom_ii",
        "dkc",
        "dkc3"
    ],
    "completion": [
        "metroidprime",
        "mzm",
        "dk64",
        "sotn",
        "dkc2",
        "doom_ii",
        "dkc",
        "dkc3"
    ],
    "completion percentage": [
        "metroidprime",
        "mzm",
        "dk64",
        "sotn",
        "dkc2"
    ],
    "percentage": [
        "metroidprime",
        "mzm",
        "dk64",
        "sotn",
        "dkc2"
    ],
    "mine cart sequence": [
        "dkc2",
        "ss",
        "dkc",
        "dk64"
    ],
    "mine": [
        "dkc2",
        "ss",
        "dkc",
        "dk64"
    ],
    "cart": [
        "dkc2",
        "ss",
        "dkc",
        "dk64"
    ],
    "sequence": [
        "metroidprime",
        "mzm",
        "oot",
        "sm_map_rando",
        "dk64",
        "sm",
        "sotn",
        "ss",
        "tloz_ooa",
        "tmc",
        "dkc2",
        "doom_ii",
        "dkc",
        "wl4"
    ],
    "invisibility": [
        "quake",
        "doom_1993",
        "dk64",
        "sly1",
        "doom_ii",
        "papermario"
    ],
    "foreshadowing": [
        "sms",
        "metroidprime",
        "mzm",
        "dk64",
        "tmc"
    ],
    "donkey kong country": [
        "dkc"
    ],
    "country": [
        "dkc",
        "dkc3",
        "dkc2"
    ],
    "frog": [
        "jakanddaxter",
        "star_fox_64",
        "dkc2",
        "dkc",
        "hcniko"
    ],
    "overworld": [
        "ffmq",
        "tloz",
        "dkc2",
        "zelda2",
        "ffta",
        "dkc",
        "gstla",
        "dkc3"
    ],
    "bonus stage": [
        "spyro3",
        "smw",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "dkc3"
    ],
    "bonus": [
        "spyro3",
        "smw",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "dkc3"
    ],
    "rhinoceros": [
        "mmx3",
        "dkc",
        "dkc3",
        "dkc2"
    ],
    "crocodile": [
        "dkc",
        "sly1",
        "dkc3",
        "dkc2"
    ],
    "water level": [
        "sms",
        "oot",
        "dkc2",
        "dkc",
        "kh1",
        "mm2"
    ],
    "water": [
        "sms",
        "oot",
        "dkc2",
        "dkc",
        "kh1",
        "mm2"
    ],
    "speedrun": [
        "metroidprime",
        "quake",
        "sotn",
        "dkc",
        "sm64hacks",
        "sm64ex"
    ],
    "villain turned good": [
        "sotn",
        "dkc",
        "gstla",
        "kh1"
    ],
    "turned": [
        "sotn",
        "dkc",
        "gstla",
        "kh1"
    ],
    "good": [
        "sotn",
        "dkc",
        "gstla",
        "kh1"
    ],
    "resized enemy": [
        "oot",
        "tmc",
        "dkc2",
        "dkc",
        "rogue_legacy"
    ],
    "resized": [
        "oot",
        "tmc",
        "dkc2",
        "dkc",
        "rogue_legacy"
    ],
    "on-the-fly character switching": [
        "lego_star_wars_tcs",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "dkc3"
    ],
    "on-the-fly": [
        "lego_star_wars_tcs",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "dkc3"
    ],
    "switching": [
        "lego_star_wars_tcs",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "dkc3"
    ],
    "secret areas within secret areas": [
        "doom_ii",
        "dkc",
        "quake",
        "dsr"
    ],
    "areas": [
        "doom_ii",
        "dkc",
        "quake",
        "dsr"
    ],
    "within": [
        "doom_ii",
        "dkc",
        "quake",
        "dsr"
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
        "marioland2",
        "huniepop2",
        "sa2b"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "jakanddaxter",
        "sms",
        "terraria",
        "tloz_ooa",
        "sly1",
        "tmc",
        "dkc2",
        "tloz_oos"
    ],
    "game reference": [
        "spyro3",
        "oot",
        "tmc",
        "dkc2",
        "witness",
        "doom_ii",
        "hcniko",
        "rogue_legacy"
    ],
    "reference": [
        "spyro3",
        "oot",
        "simpsonshitnrun",
        "placidplasticducksim",
        "tmc",
        "dkc2",
        "witness",
        "doom_ii",
        "hcniko",
        "rogue_legacy"
    ],
    "sprinting mechanics": [
        "sms",
        "mm_recomp",
        "oot",
        "dkc2",
        "pokemon_crystal",
        "sm64hacks",
        "pokemon_emerald",
        "soe",
        "wl4",
        "sm64ex"
    ],
    "sprinting": [
        "sms",
        "mm_recomp",
        "oot",
        "dkc2",
        "pokemon_crystal",
        "sm64hacks",
        "pokemon_emerald",
        "soe",
        "wl4",
        "sm64ex"
    ],
    "mechanics": [
        "sms",
        "mm_recomp",
        "oot",
        "dkc2",
        "pokemon_crystal",
        "sm64hacks",
        "pokemon_emerald",
        "soe",
        "wl4",
        "sm64ex"
    ],
    "fireworks": [
        "mlss",
        "simpsonshitnrun",
        "sly1",
        "dkc2",
        "k64"
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
        "dkc3",
        "huniepop2"
    ],
    "trouble!": [
        "dkc3"
    ],
    "snowman": [
        "minecraft",
        "sm64hacks",
        "papermario",
        "dkc3",
        "sm64ex"
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
        "smo",
        "dlcquest",
        "terraria",
        "v6",
        "stardew_valley",
        "timespinner",
        "ufo50",
        "minecraft"
    ],
    "deliberately": [
        "smo",
        "dlcquest",
        "terraria",
        "v6",
        "stardew_valley",
        "timespinner",
        "ufo50",
        "minecraft"
    ],
    "punctuation mark above head": [
        "dlcquest",
        "simpsonshitnrun",
        "tloz_ooa",
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy"
    ],
    "punctuation": [
        "dlcquest",
        "simpsonshitnrun",
        "tloz_ooa",
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy"
    ],
    "mark": [
        "dlcquest",
        "simpsonshitnrun",
        "tloz_ooa",
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy"
    ],
    "above": [
        "dlcquest",
        "simpsonshitnrun",
        "tloz_ooa",
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy"
    ],
    "head": [
        "dlcquest",
        "simpsonshitnrun",
        "tloz_ooa",
        "tmc",
        "pokemon_crystal",
        "pokemon_emerald",
        "rogue_legacy"
    ],
    "dont starve together": [
        "dontstarvetogether"
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
        "terraria",
        "dontstarvetogether",
        "factorio",
        "seaofthieves",
        "stardew_valley",
        "factorio_saws",
        "satisfactory",
        "minecraft",
        "raft"
    ],
    "funny": [
        "undertale",
        "dontstarvetogether",
        "powerwashsimulator",
        "huniepop2",
        "getting_over_it",
        "sims4",
        "shorthike"
    ],
    "survival horror": [
        "lethal_company",
        "dontstarvetogether",
        "residentevil3remake",
        "residentevil2remake"
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
        "heretic",
        "quake",
        "doom_1993",
        "doom_ii",
        "tyrian"
    ],
    "futuristic": [
        "mmbn3",
        "mmx3",
        "soe",
        "doom_1993"
    ],
    "doom ii": [
        "doom_ii"
    ],
    "doom ii: hell on earth": [
        "doom_ii"
    ],
    "ii:": [
        "doom_ii",
        "lufia2ac",
        "zelda2",
        "sc2"
    ],
    "hell": [
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
        "tmc",
        "witness",
        "doom_ii",
        "rogue_legacy"
    ],
    "pop": [
        "simpsonshitnrun",
        "placidplasticducksim",
        "tmc",
        "witness",
        "doom_ii",
        "rogue_legacy"
    ],
    "culture": [
        "simpsonshitnrun",
        "placidplasticducksim",
        "tmc",
        "witness",
        "doom_ii",
        "rogue_legacy"
    ],
    "stat tracking": [
        "osu",
        "simpsonshitnrun",
        "witness",
        "doom_ii",
        "ffta",
        "kh1",
        "rogue_legacy"
    ],
    "stat": [
        "osu",
        "simpsonshitnrun",
        "witness",
        "doom_ii",
        "ffta",
        "kh1",
        "rogue_legacy"
    ],
    "tracking": [
        "osu",
        "simpsonshitnrun",
        "witness",
        "doom_ii",
        "ffta",
        "kh1",
        "rogue_legacy"
    ],
    "rock music": [
        "ffmq",
        "ultrakill",
        "sotn",
        "doom_ii",
        "sonic_heroes",
        "ffta",
        "gstla"
    ],
    "rock": [
        "ffmq",
        "ultrakill",
        "sotn",
        "doom_ii",
        "sonic_heroes",
        "ffta",
        "gstla"
    ],
    "sequence breaking": [
        "metroidprime",
        "oot",
        "mzm",
        "sm_map_rando",
        "sm",
        "sotn",
        "tloz_ooa",
        "tmc",
        "doom_ii",
        "wl4"
    ],
    "jumping puzzle": [
        "doom_ii",
        "tloz_ooa",
        "mm3",
        "rogue_legacy"
    ],
    "jumping": [
        "doom_ii",
        "tloz_ooa",
        "mm3",
        "rogue_legacy"
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
    "dungeon clawler": [
        "dungeon_clawler"
    ],
    "dungeon": [
        "dungeon_clawler",
        "yugiohddm"
    ],
    "clawler": [
        "dungeon_clawler"
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
        "sms",
        "metroidprime",
        "tww",
        "luigismansion",
        "mario_kart_double_dash",
        "simpsonshitnrun",
        "sonic_heroes",
        "dw1"
    ],
    "gamecube": [
        "sms",
        "metroidprime",
        "tww",
        "luigismansion",
        "mario_kart_double_dash",
        "simpsonshitnrun",
        "sonic_heroes",
        "dw1"
    ],
    "playstation 2": [
        "jakanddaxter",
        "rac2",
        "simpsonshitnrun",
        "sly1",
        "kh2",
        "sonic_heroes",
        "dw1",
        "kh1"
    ],
    "tie-in": [
        "lego_star_wars_tcs",
        "dw1",
        "simpsonshitnrun",
        "fm"
    ],
    "earthbound": [
        "earthbound"
    ],
    "mummy": [
        "ffmq",
        "earthbound",
        "terraria",
        "tmc"
    ],
    "party system": [
        "ffmq",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "earthbound"
    ],
    "party": [
        "ffmq",
        "mk64",
        "mlss",
        "placidplasticducksim",
        "overcooked2",
        "xenobladex",
        "pokemon_crystal",
        "ffta",
        "gstla",
        "kh1",
        "papermario",
        "pokemon_emerald",
        "earthbound"
    ],
    "robot protagonist": [
        "ultrakill",
        "mm3",
        "mmx3",
        "mm2",
        "earthbound"
    ],
    "robot": [
        "ultrakill",
        "mm3",
        "mmx3",
        "mm2",
        "earthbound"
    ],
    "censored version": [
        "earthbound",
        "oot",
        "xenobladex",
        "residentevil2remake"
    ],
    "censored": [
        "earthbound",
        "oot",
        "xenobladex",
        "residentevil2remake"
    ],
    "version": [
        "oot",
        "pokemon_rb",
        "pokemon_crystal",
        "xenobladex",
        "pokemon_emerald",
        "earthbound",
        "pokemon_frlg",
        "residentevil2remake"
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
    "forest": [
        "enderlilies",
        "oribf",
        "hcniko",
        "tunic"
    ],
    "factorio": [
        "factorio"
    ],
    "factorio space age without space": [
        "factorio_saws"
    ],
    "factorio: space age": [
        "factorio_saws"
    ],
    "factorio:": [
        "factorio_saws"
    ],
    "space": [
        "v6",
        "factorio_saws",
        "marioland2",
        "getting_over_it",
        "sc2"
    ],
    "faxanadu": [
        "faxanadu"
    ],
    "family computer": [
        "tloz",
        "faxanadu",
        "ff1",
        "mm3"
    ],
    "family": [
        "faxanadu",
        "tloz",
        "sims4",
        "mm3",
        "zelda2",
        "powerwashsimulator",
        "ff1",
        "tunic",
        "shorthike"
    ],
    "computer": [
        "tloz",
        "faxanadu",
        "mm3",
        "zelda2",
        "ff1"
    ],
    "nintendo entertainment system": [
        "tloz",
        "faxanadu",
        "mm3",
        "zelda2",
        "ff1"
    ],
    "nameless protagonist": [
        "faxanadu",
        "pokemon_emerald",
        "tloz_ph",
        "pokemon_crystal"
    ],
    "nameless": [
        "faxanadu",
        "pokemon_emerald",
        "tloz_ph",
        "pokemon_crystal"
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
        "mk64",
        "tetrisattack",
        "mario_kart_double_dash",
        "placidplasticducksim",
        "overcooked2",
        "pokemon_rb",
        "pokemon_crystal",
        "yoshisisland",
        "pmd_eos",
        "pokemon_emerald",
        "ff1",
        "pokemon_frlg",
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
        "ffmq",
        "placidplasticducksim",
        "musedash",
        "getting_over_it",
        "sims4",
        "shorthike"
    ],
    "ninja": [
        "ffmq",
        "ffta",
        "rogue_legacy",
        "messenger"
    ],
    "final fantasy tactics advance": [
        "ffta"
    ],
    "tactics": [
        "ffta"
    ],
    "tactical": [
        "mmbn3",
        "ffta",
        "wargroove",
        "overcooked2"
    ],
    "grinding": [
        "osrs",
        "seaofthieves",
        "tloz_oos",
        "ffta",
        "kh1"
    ],
    "permadeath": [
        "ffta",
        "ror1",
        "rogue_legacy",
        "minecraft"
    ],
    "mana": [
        "terraria",
        "poe",
        "ffta",
        "soe"
    ],
    "random encounter": [
        "pokemon_crystal",
        "ffta",
        "gstla",
        "kh1",
        "pokemon_emerald"
    ],
    "random": [
        "pokemon_crystal",
        "ffta",
        "gstla",
        "kh1",
        "pokemon_emerald"
    ],
    "encounter": [
        "pokemon_crystal",
        "ffta",
        "gstla",
        "kh1",
        "pokemon_emerald"
    ],
    "yu-gi-oh! forbidden memories": [
        "fm"
    ],
    "yu-gi-oh!": [
        "yugioh06",
        "yugiohddm",
        "fm"
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
    "psychological horror": [
        "lethal_company",
        "mm_recomp",
        "undertale",
        "getting_over_it"
    ],
    "psychological": [
        "lethal_company",
        "mm_recomp",
        "undertale",
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
    "ancient advanced civilization technology": [
        "jakanddaxter",
        "metroidprime",
        "ss",
        "gstla"
    ],
    "ancient": [
        "jakanddaxter",
        "metroidprime",
        "ss",
        "gstla"
    ],
    "advanced": [
        "jakanddaxter",
        "metroidprime",
        "ss",
        "gstla"
    ],
    "technology": [
        "jakanddaxter",
        "metroidprime",
        "ss",
        "gstla"
    ],
    "battle screen": [
        "mlss",
        "pokemon_crystal",
        "gstla",
        "papermario",
        "pokemon_emerald"
    ],
    "battle": [
        "mmbn3",
        "mlss",
        "pokemon_crystal",
        "gstla",
        "papermario",
        "pokemon_emerald",
        "sa2b"
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
    "stylized": [
        "ultrakill",
        "hades",
        "hylics2",
        "hcniko",
        "tunic"
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
    "fishing": [
        "minecraft",
        "terraria",
        "ladx",
        "stardew_valley",
        "hcniko",
        "shorthike"
    ],
    "beach": [
        "smo",
        "sms",
        "stardew_valley",
        "hcniko",
        "minecraft"
    ],
    "heretic": [
        "heretic"
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
    "creature compendium": [
        "hk",
        "pokemon_emerald",
        "sotn",
        "metroidprime"
    ],
    "creature": [
        "hk",
        "pokemon_emerald",
        "sotn",
        "metroidprime"
    ],
    "compendium": [
        "hk",
        "pokemon_emerald",
        "sotn",
        "metroidprime"
    ],
    "hunie pop": [
        "huniepop"
    ],
    "huniepop": [
        "huniepop2",
        "huniepop"
    ],
    "visual novel": [
        "huniepop2",
        "huniepop"
    ],
    "visual": [
        "huniepop2",
        "huniepop"
    ],
    "novel": [
        "huniepop2",
        "huniepop"
    ],
    "erotic": [
        "huniepop2",
        "huniepop"
    ],
    "romance": [
        "sims4",
        "huniepop2",
        "huniepop",
        "stardew_valley"
    ],
    "hunie pop 2": [
        "huniepop2"
    ],
    "huniepop 2: double date": [
        "huniepop2"
    ],
    "date": [
        "huniepop2"
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
        "jakanddaxter",
        "mmx3",
        "quake",
        "rogue_legacy"
    ],
    "language selection": [
        "jakanddaxter",
        "yugiohddm",
        "sly1",
        "tmc",
        "minecraft"
    ],
    "language": [
        "jakanddaxter",
        "yugiohddm",
        "sly1",
        "tmc",
        "minecraft"
    ],
    "selection": [
        "jakanddaxter",
        "yugiohddm",
        "sly1",
        "tmc",
        "minecraft"
    ],
    "auto-saving": [
        "jakanddaxter",
        "spyro3",
        "witness",
        "minecraft"
    ],
    "useable vehicles": [
        "jakanddaxter",
        "simpsonshitnrun",
        "witness",
        "xenobladex"
    ],
    "useable": [
        "jakanddaxter",
        "simpsonshitnrun",
        "witness",
        "xenobladex"
    ],
    "vehicles": [
        "jakanddaxter",
        "simpsonshitnrun",
        "witness",
        "xenobladex"
    ],
    "destructible environment": [
        "jakanddaxter",
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "sly1",
        "kh1"
    ],
    "destructible": [
        "jakanddaxter",
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "sly1",
        "kh1"
    ],
    "environment": [
        "jakanddaxter",
        "lego_star_wars_tcs",
        "simpsonshitnrun",
        "sly1",
        "kh1"
    ],
    "comic relief": [
        "jakanddaxter",
        "kh1",
        "tloz_ph",
        "ladx"
    ],
    "comic": [
        "jakanddaxter",
        "kh1",
        "tloz_ph",
        "ladx"
    ],
    "relief": [
        "jakanddaxter",
        "kh1",
        "tloz_ph",
        "ladx"
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
    "crystal": [
        "k64",
        "pokemon_crystal"
    ],
    "shards": [
        "k64"
    ],
    "kid friendly": [
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "openrct2",
        "k64",
        "pokemon_emerald"
    ],
    "kid": [
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "openrct2",
        "k64",
        "pokemon_emerald"
    ],
    "friendly": [
        "lego_star_wars_tcs",
        "pokemon_crystal",
        "openrct2",
        "k64",
        "powerwashsimulator",
        "pokemon_emerald",
        "sims4",
        "tunic",
        "shorthike"
    ],
    "whale": [
        "k64",
        "kdl3",
        "kh1",
        "marioland2"
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
        "kdl3",
        "marioland2",
        "wl4",
        "wl"
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
    "unbeatable enemies": [
        "kh1",
        "tmc",
        "papermario",
        "wl4"
    ],
    "unbeatable": [
        "kh1",
        "tmc",
        "papermario",
        "wl4"
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
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "pokemon_crystal"
    ],
    "color": [
        "tloz_ooa",
        "ladx",
        "tloz_oos",
        "pokemon_crystal"
    ],
    "chicken": [
        "oot",
        "ladx",
        "stardew_valley",
        "minecraft"
    ],
    "tentacles": [
        "sms",
        "metroidprime",
        "mlss",
        "ladx",
        "pokemon_crystal",
        "papermario",
        "pokemon_emerald"
    ],
    "animal cruelty": [
        "pokemon_emerald",
        "oot",
        "ladx",
        "pokemon_crystal"
    ],
    "cruelty": [
        "pokemon_emerald",
        "oot",
        "ladx",
        "pokemon_crystal"
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
        "quake",
        "zillion"
    ],
    "mega": [
        "mmbn3",
        "megamix",
        "mm2",
        "mm3",
        "mmx3",
        "landstalker"
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
    "motion control": [
        "lego_star_wars_tcs",
        "ss",
        "smo",
        "tp"
    ],
    "motion": [
        "lego_star_wars_tcs",
        "ss",
        "smo",
        "tp"
    ],
    "control": [
        "lego_star_wars_tcs",
        "ss",
        "smo",
        "tp"
    ],
    "character creation": [
        "lego_star_wars_tcs",
        "pokemon_emerald",
        "minecraft",
        "pokemon_crystal"
    ],
    "creation": [
        "lego_star_wars_tcs",
        "pokemon_emerald",
        "minecraft",
        "pokemon_crystal"
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
    "monsters": [
        "lethal_company",
        "yugiohddm",
        "stardew_valley",
        "yugioh06",
        "pokemon_frlg",
        "minecraft"
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
    "italian accent": [
        "sms",
        "mk64",
        "mlss",
        "luigismansion"
    ],
    "italian": [
        "sms",
        "mk64",
        "mlss",
        "luigismansion"
    ],
    "accent": [
        "sms",
        "mk64",
        "mlss",
        "luigismansion"
    ],
    "super mario land 2": [
        "marioland2"
    ],
    "super mario land 2: 6 golden coins": [
        "marioland2"
    ],
    "mario": [
        "smo",
        "sms",
        "mk64",
        "mlss",
        "smw",
        "mario_kart_double_dash",
        "yoshisisland",
        "marioland2",
        "papermario",
        "sm64hacks",
        "wl",
        "sm64ex"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "mm2",
        "marioland2",
        "pokemon_rb",
        "wl"
    ],
    "turtle": [
        "sms",
        "mk64",
        "mlss",
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
    "yoshi": [
        "mario_kart_double_dash",
        "yoshisisland",
        "sms",
        "smw"
    ],
    "princess peach": [
        "sms",
        "mlss",
        "mario_kart_double_dash",
        "sm64hacks",
        "sm64ex"
    ],
    "peach": [
        "sms",
        "mlss",
        "mario_kart_double_dash",
        "sm64hacks",
        "sm64ex"
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
    "project": [
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
    "8-bit": [
        "mm2",
        "mm3",
        "zelda2",
        "messenger"
    ],
    "metroid prime": [
        "metroidprime"
    ],
    "metroid": [
        "metroidprime",
        "sm_map_rando",
        "sm",
        "smz3"
    ],
    "prime": [
        "metroidprime"
    ],
    "time limit": [
        "sms",
        "metroidprime",
        "ror1",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "tmc",
        "witness",
        "wl4",
        "rogue_legacy"
    ],
    "limit": [
        "sms",
        "metroidprime",
        "ror1",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "tmc",
        "witness",
        "wl4",
        "rogue_legacy"
    ],
    "countdown timer": [
        "metroidprime",
        "oot",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "tmc",
        "wl4",
        "rogue_legacy"
    ],
    "countdown": [
        "metroidprime",
        "oot",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "tmc",
        "wl4",
        "rogue_legacy"
    ],
    "timer": [
        "metroidprime",
        "oot",
        "mzm",
        "sm_map_rando",
        "tloz_ph",
        "sm",
        "simpsonshitnrun",
        "tmc",
        "wl4",
        "rogue_legacy"
    ],
    "auto-aim": [
        "metroidprime",
        "oot",
        "quake",
        "mm_recomp",
        "tww",
        "ss"
    ],
    "linear gameplay": [
        "sms",
        "metroidprime",
        "sm64hacks",
        "sm64ex"
    ],
    "linear": [
        "sms",
        "metroidprime",
        "sm64hacks",
        "sm64ex"
    ],
    "meme origin": [
        "metroidprime",
        "mm_recomp",
        "tloz",
        "sotn",
        "star_fox_64",
        "zelda2",
        "minecraft"
    ],
    "meme": [
        "metroidprime",
        "mm_recomp",
        "tloz",
        "sotn",
        "star_fox_64",
        "zelda2",
        "minecraft"
    ],
    "origin": [
        "metroidprime",
        "mm_recomp",
        "tloz",
        "sotn",
        "star_fox_64",
        "zelda2",
        "minecraft"
    ],
    "isolation": [
        "metroidprime",
        "mzm",
        "sm_map_rando",
        "sm",
        "sotn"
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
    "procedural generation": [
        "terraria",
        "rogue_legacy",
        "minecraft",
        "witness"
    ],
    "procedural": [
        "terraria",
        "rogue_legacy",
        "minecraft",
        "witness"
    ],
    "generation": [
        "terraria",
        "rogue_legacy",
        "minecraft",
        "witness"
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
    "easy": [
        "oot",
        "tloz_ph",
        "witness",
        "mlss"
    ],
    "super-ness": [
        "sms",
        "sm64ex",
        "sm64hacks",
        "mlss"
    ],
    "wiggler": [
        "smo",
        "sms",
        "mlss",
        "sm64hacks",
        "sm64ex"
    ],
    "mega man 2": [
        "mm2"
    ],
    "mega man ii": [
        "mm2"
    ],
    "man": [
        "mm2",
        "mmbn3",
        "mmx3",
        "mm3"
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
    "time manipulation": [
        "oot",
        "sm_map_rando",
        "sm",
        "timespinner",
        "rogue_legacy"
    ],
    "openrct2": [
        "openrct2"
    ],
    "business": [
        "openrct2",
        "powerwashsimulator",
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
    "thriller": [
        "oribf",
        "sm",
        "sm_map_rando"
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
        "ttyd",
        "papermario"
    ],
    "gambling": [
        "tmc",
        "pokemon_crystal",
        "papermario",
        "pokemon_emerald",
        "rogue_legacy"
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
        "pokemon_rb",
        "pokemon_crystal",
        "pmd_eos",
        "pokemon_emerald",
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
    "family friendly": [
        "powerwashsimulator",
        "sims4",
        "tunic",
        "shorthike"
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
    "playstation vita": [
        "ror1",
        "undertale",
        "terraria",
        "v6",
        "stardew_valley",
        "timespinner",
        "rogue_legacy"
    ],
    "vita": [
        "ror1",
        "undertale",
        "terraria",
        "v6",
        "stardew_valley",
        "timespinner",
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
        "sonic_heroes",
        "sa2b",
        "sadx"
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
        "wargroove",
        "sc2"
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
        "zork_grand_inquisitor",
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
    "the sims 4": [
        "sims4"
    ],
    "sims": [
        "sims4"
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
        "sm_map_rando",
        "sm"
    ],
    "super mario 64": [
        "sm64hacks",
        "sm64ex"
    ],
    "rabbit": [
        "smo",
        "terraria",
        "tloz_ooa",
        "sonic_heroes",
        "sm64hacks",
        "sm64ex"
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
    "nintendo switch 2": [
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
        "tloz_ooa",
        "tloz_oos"
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
    "universal tracker": [
        "tracker"
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
        "wl4",
        "wl"
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
    "dice": [
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
    ]
} # type: ignore