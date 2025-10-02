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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaazl.jpg",
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
            "swimming"
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
            "moving platforms",
            "time trials"
        ],
        "release_date": "1999"
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
        "storyline": "you are an egg. leap out of your nest and begin exploring the world, collecting hearts to increase your life and upgrades that can help you jump higher or give you other abilities.",
        "keywords": [
            "ghosts",
            "minigames",
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
            "achievements",
            "pixel art",
            "silent protagonist",
            "great soundtrack",
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
            "great soundtrack"
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
            "lgbtq+"
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
    "celeste_open_world": {
        "igdb_id": "26226",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3byy.jpg",
        "game_name": "Celeste (Open World)",
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
            "lgbtq+"
        ],
        "release_date": "2018"
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
            "turn-based",
            "spaceship",
            "multiple endings",
            "sequel",
            "digital distribution",
            "voice acting",
            "loot gathering",
            "ambient music"
        ],
        "release_date": "2005"
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
            "action-adventure",
            "pixel art",
            "digital distribution"
        ],
        "release_date": "2018"
    },
    "crystal_project": {
        "igdb_id": "181444",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co48fv.jpg",
        "game_name": "Crystal Project",
        "igdb_name": "crystal project",
        "rating": [
            "mild language",
            "fantasy violence",
            "mild blood"
        ],
        "player_perspectives": [
            "third person",
            "bird view / isometric"
        ],
        "genres": [
            "platform",
            "role-playing (rpg)",
            "strategy",
            "turn-based strategy (tbs)",
            "tactical",
            "adventure",
            "indie"
        ],
        "themes": [
            "fantasy",
            "mystery"
        ],
        "platforms": [
            "linux",
            "pc (microsoft windows)",
            "mac",
            "nintendo switch"
        ],
        "storyline": "explore the world, find crystals, and fulfill the prophecy to bring balance to the land of sequoia.\n\n...or maybe you'd rather spend your time collecting neat equipment and artifacts? or tame strange creatures and fill out all the entries in your archive? or perhaps you'd rather hunt down every monster and conquer the world's toughest bosses. or maybe you'd rather travel to the farthest reaches of the land and uncover the world's greatest mysteries.\n\nthe choice is yours, as it should be! or is it? they say that those who stray out of line will be punished, killed, or worse. maybe it's for your own good that you stick to collecting crystals, just like everyone else. but where would the adventure be in that?",
        "keywords": [
            "3d",
            "metroidvania",
            "jrpg",
            "atmospheric"
        ],
        "release_date": "2022"
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
            "human",
            "soulslike",
            "interconnected-world"
        ],
        "release_date": "2016"
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
            "digital distribution",
            "deliberately retro",
            "punctuation mark above head"
        ],
        "release_date": "2011"
    },
    "dontstarvetogether": {
        "igdb_id": "17832",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaaqp.jpg",
        "game_name": "Don't Starve Together",
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
            "soulslike",
            "interconnected-world"
        ],
        "release_date": "2018"
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
            "shopping"
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
            "witches",
            "soulslike"
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
            "merchants"
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
        "release_date": "2003"
    },
    "flipwitch": {
        "igdb_id": "361419",
        "cover_url": "",
        "game_name": "Flipwitch Forbidden Sex Hex",
        "igdb_name": "",
        "rating": "",
        "player_perspectives": [],
        "genres": [],
        "themes": [],
        "platforms": [],
        "storyline": "",
        "keywords": [],
        "release_date": ""
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
            "turn-based"
        ],
        "release_date": "1999"
    },
    "frogmonster": {
        "igdb_id": "187372",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7l4c.jpg",
        "game_name": "Frog Monster",
        "igdb_name": "frogmonster",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "shooter",
            "adventure",
            "indie"
        ],
        "themes": [
            "action",
            "fantasy",
            "open world"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "in a world, existing before and still, built through the powerful and cunning minds of the creators, a new being emerges. the world, once flourishing with enriching creatures and plants, is changing rapidly and dangerously. beasts, designed by a wicked and corrupt creator, tear apart and threaten the creatures that still survive. you, the final hope from melora, a na\u00efve and endangered creator, will journey though the unraveling, unique lands, battle the mindless beasts, and revive the world that once was.",
        "keywords": [
            "3d",
            "metroidvania",
            "atmospheric"
        ],
        "release_date": "2024"
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
            "difficult",
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
            "digital distribution",
            "skeletons",
            "melee",
            "secret area"
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
            "anime"
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
        "release_date": "2001"
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
            "silent protagonist",
            "anthropomorphism",
            "polygonal 3d",
            "melee",
            "moving platforms",
            "shape-shifting",
            "auto-scrolling levels",
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
    "kindergarten_2": {
        "igdb_id": "118637",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co2vk4.jpg",
        "game_name": "Kindergarten 2",
        "igdb_name": "kindergarten 2",
        "rating": [],
        "player_perspectives": [],
        "genres": [
            "adventure",
            "indie"
        ],
        "themes": [],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2019"
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
            "exploration"
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
            "adventure",
            "indie"
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
            "interconnected-world"
        ],
        "release_date": "2001"
    },
    "lunacid": {
        "igdb_id": "192291",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co7cdv.jpg",
        "game_name": "Lunacid",
        "igdb_name": "lunacid",
        "rating": [],
        "player_perspectives": [
            "first person"
        ],
        "genres": [
            "role-playing (rpg)",
            "indie"
        ],
        "themes": [
            "fantasy",
            "horror"
        ],
        "platforms": [
            "pc (microsoft windows)"
        ],
        "storyline": "long ago a great beast arose from the sea and covered the earth in a poison fog. now those deemed undesirable are thrown into a great well, which has become a pit of chaos and disease. you awaken in a moonlit subterranean world, having been thrown into the great well for crimes unknown. the only way out is to go further down and confront the sleeping old one below. on the way there will be many creatures and secrets to discover.",
        "keywords": [],
        "release_date": "2023"
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
            "turtle"
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
        "keywords": [],
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
            "2d",
            "metroidvania",
            "difficult"
        ],
        "release_date": "2018"
    },
    "metroidfusion": {
        "igdb_id": "1104",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co3w49.jpg",
        "game_name": "Metroid Fusion",
        "igdb_name": "metroid fusion",
        "rating": [
            "mild fantasy violence",
            "violence"
        ],
        "player_perspectives": [
            "side view"
        ],
        "genres": [
            "shooter",
            "platform",
            "puzzle",
            "adventure"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "nintendo 3ds",
            "wii u",
            "game boy advance"
        ],
        "storyline": "the game begins with samus aran acting as a bodyguard for the biologic's research team on planet sr388. eventually, a hornoad confronts them and is killed by samus. however, a globular yellow organism (an x) emerges from the hornoad as it is destroyed and enters samus's body.\nfeeling no initial effects, samus continues escorting the researchers and completes the assignment. on the way back to the laboratory, however, samus loses consciousness, and her gunship crashes into an asteroid belt. the ship's emergency systems automatically ejected samus' escape pod, saving her from the crash, but her gunship is completely destroyed. samus is quickly attended to by a medical crew, who discover that the creature that entered her body on sr388 was actually a parasitic organism that they soon named x.\n\nsamus infected 2\nsamus, infected by the x parasites.\nthe organic components of samus's power suit had become so integrated with her system that it could not be removed while she was unconscious. large portions of her infected suit had to be surgically removed, dramatically altering its appearance. however, the x in samus's central nervous system were too embedded to be removed safely; samus's chances of survival were lower than one percent.\nmetroids are the only known predator of the x; however, since samus destroyed all the metroids on sr388 in a previous mission, the x were able to multiply unchecked. seeing this as the key to curing her, doctors proposed using a metroid cell from samus' dead baby metroid to make an anti-x vaccine. apparently, the federation had managed to preserve a cell culture from the baby that saved samus while she was on zebes a second time. the serum was prepared and injected without delay, completely eradicating the x. there were, however, two side effects: samus could no longer be hurt by normal x and could even absorb them to replenish health and ammunition, but she also inherited the metroids' vulnerability to cold.\n\nupon recovering, samus is sent to investigate an explosion on the biologic space laboratories research station, where the specimens from sr388 and the infected pieces of her power suit are being held. once she arrives at the station, samus immediately heads to the quarantine bay, where she encounters and kills a hornoad that has been infected by an x parasite. samus speaks with her new gunship's computer (whom she has named \"adam\", as it reminds her of a former co) and learns that the specimens brought back by the field team have become infected by the x. the computer also reveals that the x can use the dna of its prey to create a perfect copy, meaning any organic life on the station may also be infected.\n\nsa-x 1\nthe sa-x.\nas she continues to explore the station, samus discovers that the x have used the infected portions of her power suit to create a copy of samus herself, dubbed the sa-x (or samus aran-x). since the sa-x arose from samus's fully-upgraded power suit, it has all of her powered-up abilities, as evidenced by it using a power bomb to escape the quarantine bay. by exploding the bomb, the sa-x also destroyed the capsules holding the x specimens, releasing them all into the station. well into her investigation of the station, samus stumbles upon the facility's restricted lab. here, she finds dozens of infant metroids and several more metroids in various stages of maturity, all in stasis; these were the results of a cloning project of which samus was not previously aware. shortly after samus discovers them, the sa-x attempts to destroy its predators, but its plan backfires: the metroids break free and the emergency fail-safes are activated as a result. samus barely escapes before the lab locks down completely and is jettisoned from the station, exploding over sr388.\nafter the incident at the restricted lab, samus speaks with her ship's computer, who is angry about the discovery and subsequent destruction of the metroids. the computer explains that the federation had been secretly working on a metroid breeding program, for \"peaceful applications\". the computer reveals that the station's srx environment, a replica of the sr388 ecosystem, was ideal for raising alpha, gamma, zeta, and even omega metroids. the research uncovered techniques for rapid growth, allowing an infant grow into an omega metroid in mere days. unfortunately, the sa-x had been tracking samus down and followed her to the lab's location. much to samus's surprise, the computer also mentions that the sa-x has been reproducing asexually and there are no fewer than 10 aboard the station.\n\nlater, the computer tells samus that she has caused enough damage and instructs her to leave the rest of the investigation to the federation. apparently, the federation has taken an interest in the x and sa-x and believe that this life-form has endless applications. samus, having seen the sa-x's destructive capabilities firsthand, is strongly against this. she is convinced that the x will overwhelm the federation troops as soon as they land, absorbing their powers and knowledge in the process. if this happens, they could easily spread throughout the galaxy and \"galactic civilization will end.\"\n\nas an alternative, samus decides to activate the station's self-destruct mechanism in order to destroy the x, risking her own life in the process. however, her ship's computer has locked samus in a navigation room, as the federation has ordered it to keep her confined until their arrival. desperate, samus yells at the computer: \"don't let them do this. can't you see what will happen, adam?\" puzzled at the use of the name, the computer inquires as to who this adam was. samus reveals that he had been her previous commanding officer and had died saving her life. apparently moved by samus's revelation, the computer agrees with the plan, and suggests that if samus were to alter the station's orbit, then she might be able to include the planet in the explosion, thus ensuring the destruction of the x on planet sr388 as well as those on the station. at this point, samus realizes that her ship's computer truly is adam malkovich, whose personality had been uploaded to a computer prior to his death.\n\nsamus hurries to the operations room, where she is confronted by an sa-x. she manages to defeat it, but its core-x escapes before she can absorb it. ignoring its escape, samus initiates the self-destruct sequence and hurries back to her ship. however, she finds the docking bay in ruins and her ship gone. before she can react to the situation, an omega metroid appears, apparently having escaped from the restricted lab before its destruction and grown to full size in record time. samus possesses no weapon capable of damaging the metroid, and a single swipe of its claw reduces her energy reserves to one unit. as the omega metroid prepares to finish her off, the sa-x returns, and attacks the metroid with its ice beam, injuring it. however, it was greatly weakened from its fight with samus and is quickly defeated by the metroid. this time, the core-x hovers over samus, allowing her to absorb it and obtain the \"unnamed suit\" as well as the ice beam and restoring her genetic condition to its pre-vaccine state. using her regained abilities, samus fights and kills the omega metroid after a fierce struggle. after the battle, samus's ship reenters the bay, having been piloted by the computer, adam, and the same etecoons and dachoras she saved on the previous mission to zebes and later on the habitation deck.\n\nas samus leaves the station, it is shown crashing into sr388, destroying both the station and the planet, ridding the universe of the x forever.\n\nreflecting on her actions, samus doubts people will understand why she destroyed the x, nor will they realize the danger that was barely averted. samus believes she will be held responsible for defying the federation, but adam comforts her, telling her: \"do not worry. one of them will understand. one of them must.\" a final reflection, samus goes on to say: \"we are all bound by our experiences. they are the limits of our consciousness. but in the end, the human soul will ever reach for the truth... this is what adam taught me.\"",
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
        "release_date": "2002"
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
            "darkness",
            "explosion",
            "checkpoints",
            "underwater gameplay",
            "moving platforms",
            "villain",
            "recurring boss",
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
        "keywords": [],
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
            "strategy",
            "indie"
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
            "easter egg",
            "explosion"
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
        "keywords": [],
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
            "pc (microsoft windows)",
            "mac",
            "android",
            "ios"
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
            "nintendo switch 2",
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
            "bow and arrow",
            "potion",
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
            "story rich"
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
            "bloody"
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
        "keywords": [],
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
        "keywords": [],
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
            "difficult",
            "time limit",
            "pixel art",
            "bow and arrow",
            "roguelite"
        ],
        "release_date": "2013"
    },
    "ror2": {
        "igdb_id": "28512",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaavb.jpg",
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
        "rating": [
            "fantasy violence"
        ],
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
            "crafting"
        ],
        "release_date": "2024"
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
        "keywords": [],
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
            "human",
            "polygonal 3d",
            "breaking the fourth wall",
            "pop culture reference",
            "stat tracking",
            "punctuation mark above head",
            "been here before",
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
            "cute",
            "funny",
            "relaxing",
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
            "digital distribution",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "retroachievements"
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
            "digital distribution",
            "sprinting mechanics",
            "real-time combat",
            "underwater gameplay",
            "speedrun",
            "retroachievements"
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
            "alternate costumes",
            "deliberately retro",
            "checkpoints",
            "underwater gameplay",
            "behind the waterfall"
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
            "dog",
            "giant insects",
            "sprinting mechanics",
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
            "pc (microsoft windows)",
            "playstation 2",
            "xbox",
            "nintendo gamecube"
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
        "release_date": "2026"
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
            "game reference",
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
            "nintendo switch 2",
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
            "robots",
            "retroachievements"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/coaamg.jpg",
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
            "female protagonist",
            "action-adventure",
            "pixel art",
            "digital distribution",
            "deliberately retro",
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
            "minigames"
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
        "keywords": [],
        "release_date": "2006"
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
            "living inventory",
            "retroachievements"
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
        "release_date": "2001"
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
        "release_date": "2015"
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
            "digital distribution"
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
        "keywords": [],
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
        "sm64ex"
    ],
    "adventure": [
        "dark_souls_3",
        "timespinner",
        "kdl3",
        "enderlilies",
        "zelda2",
        "blasphemous",
        "ff4fe",
        "mzm",
        "cat_quest",
        "seaofthieves",
        "tloz",
        "dkc3",
        "messenger",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "xenobladex",
        "oribf",
        "pseudoregalia",
        "sly1",
        "metroidprime",
        "crystal_project",
        "dw1",
        "pokemon_emerald",
        "banjo_tooie",
        "terraria",
        "wl4",
        "gstla",
        "jakanddaxter",
        "peaks_of_yore",
        "osrs",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "smz3",
        "earthbound",
        "tww",
        "tunic",
        "animal_well",
        "spyro3",
        "simpsonshitnrun",
        "sotn",
        "sm64ex",
        "frogmonster",
        "celeste",
        "lingo",
        "shorthike",
        "mmx3",
        "raft",
        "dontstarvetogether",
        "ss",
        "celeste64",
        "mm2",
        "minecraft",
        "papermario",
        "crosscode",
        "rogue_legacy",
        "v6",
        "tloz_oos",
        "dk64",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "ladx",
        "tloz_ph",
        "tloz_ooa",
        "ufo50",
        "adventure",
        "pokemon_frlg",
        "hk",
        "pokemon_rb",
        "zork_grand_inquisitor",
        "mm3",
        "getting_over_it",
        "cv64",
        "residentevil2remake",
        "dark_souls_2",
        "sm",
        "tp",
        "metroidfusion",
        "albw",
        "cuphead",
        "lego_star_wars_tcs",
        "sm64hacks",
        "shivers",
        "sms",
        "ror2",
        "noita",
        "mm_recomp",
        "momodoramoonlitfarewell",
        "sadx",
        "faxanadu",
        "witness",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "rac2",
        "outer_wilds",
        "subnautica",
        "mlss",
        "chainedechoes",
        "pokemon_crystal",
        "alttp",
        "ff1",
        "ffmq",
        "dsr",
        "inscryption",
        "hylics2",
        "oot",
        "k64",
        "stardew_valley",
        "tmc",
        "cvcotm",
        "hades",
        "sa2b",
        "smo",
        "kh1",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "smw",
        "residentevil3remake",
        "kh2",
        "luigismansion"
    ],
    "bird view / isometric": [
        "chainedechoes",
        "pokemon_rb",
        "spyro3",
        "placidplasticducksim",
        "pokemon_crystal",
        "mmbn3",
        "balatro",
        "openrct2",
        "wargroove",
        "against_the_storm",
        "alttp",
        "meritous",
        "sims4",
        "ff1",
        "ff4fe",
        "ffmq",
        "pmd_eos",
        "overcooked2",
        "shapez",
        "brotato",
        "tloz",
        "yugiohddm",
        "adventure",
        "poe",
        "shorthike",
        "inscryption",
        "ffta",
        "hylics2",
        "ctjot",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "stardew_valley",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "tyrian",
        "tmc",
        "hades",
        "factorio",
        "landstalker",
        "soe",
        "crosscode",
        "crystal_project",
        "dw1",
        "pokemon_emerald",
        "rimworld",
        "tloz_oos",
        "sonic_heroes",
        "wargroove2",
        "ladx",
        "gstla",
        "civ_6",
        "osrs",
        "tloz_ph",
        "smz3",
        "undertale",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "ufo50",
        "tunic",
        "sc2",
        "factorio_saws",
        "pokemon_frlg"
    ],
    "bird": [
        "chainedechoes",
        "pokemon_rb",
        "spyro3",
        "placidplasticducksim",
        "pokemon_crystal",
        "mmbn3",
        "balatro",
        "openrct2",
        "wargroove",
        "against_the_storm",
        "alttp",
        "meritous",
        "sims4",
        "ff1",
        "ff4fe",
        "ffmq",
        "pmd_eos",
        "overcooked2",
        "shapez",
        "brotato",
        "tloz",
        "yugiohddm",
        "dkc3",
        "poe",
        "shorthike",
        "inscryption",
        "ffta",
        "hylics2",
        "ctjot",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "factorio_saws",
        "stardew_valley",
        "minecraft",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "tyrian",
        "tmc",
        "hades",
        "factorio",
        "landstalker",
        "soe",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "dw1",
        "pokemon_emerald",
        "rimworld",
        "banjo_tooie",
        "tloz_oos",
        "aus",
        "sonic_heroes",
        "wargroove2",
        "ladx",
        "gstla",
        "civ_6",
        "osrs",
        "tloz_ph",
        "smz3",
        "undertale",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "ufo50",
        "tunic",
        "sc2",
        "adventure",
        "pokemon_frlg"
    ],
    "view": [
        "timespinner",
        "kdl3",
        "wargroove",
        "enderlilies",
        "meritous",
        "sims4",
        "zelda2",
        "blasphemous",
        "ff4fe",
        "mzm",
        "brotato",
        "tloz",
        "dkc3",
        "messenger",
        "poe",
        "aquaria",
        "ror1",
        "oribf",
        "zillion",
        "crystal_project",
        "dw1",
        "pokemon_emerald",
        "rimworld",
        "terraria",
        "tetrisattack",
        "wl4",
        "gstla",
        "civ_6",
        "osrs",
        "dlcquest",
        "musedash",
        "smz3",
        "earthbound",
        "tunic",
        "sc2",
        "animal_well",
        "spyro3",
        "placidplasticducksim",
        "mmbn3",
        "balatro",
        "sotn",
        "celeste",
        "lufia2ac",
        "yugiohddm",
        "shorthike",
        "mmx3",
        "dontstarvetogether",
        "mm2",
        "dkc2",
        "wl",
        "tyrian",
        "papermario",
        "crosscode",
        "soe",
        "rogue_legacy",
        "v6",
        "tloz_oos",
        "marioland2",
        "yoshisisland",
        "aus",
        "monster_sanctuary",
        "ladx",
        "tloz_ph",
        "tloz_ooa",
        "ufo50",
        "adventure",
        "pokemon_frlg",
        "hk",
        "pokemon_rb",
        "mm3",
        "getting_over_it",
        "overcooked2",
        "shapez",
        "sm",
        "spire",
        "metroidfusion",
        "albw",
        "cuphead",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "noita",
        "landstalker",
        "momodoramoonlitfarewell",
        "wargroove2",
        "faxanadu",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "mlss",
        "chainedechoes",
        "dkc",
        "pokemon_crystal",
        "openrct2",
        "against_the_storm",
        "alttp",
        "megamix",
        "ff1",
        "pmd_eos",
        "ffmq",
        "inscryption",
        "ffta",
        "hylics2",
        "ctjot",
        "k64",
        "stardew_valley",
        "tmc",
        "cvcotm",
        "hades",
        "factorio",
        "sonic_heroes",
        "smw",
        "yugioh06",
        "factorio_saws"
    ],
    "/": [
        "chainedechoes",
        "pokemon_rb",
        "spyro3",
        "placidplasticducksim",
        "pokemon_crystal",
        "mmbn3",
        "balatro",
        "openrct2",
        "wargroove",
        "against_the_storm",
        "alttp",
        "meritous",
        "sims4",
        "ff1",
        "ff4fe",
        "ffmq",
        "pmd_eos",
        "overcooked2",
        "shapez",
        "brotato",
        "tloz",
        "yugiohddm",
        "adventure",
        "poe",
        "shorthike",
        "inscryption",
        "ffta",
        "hylics2",
        "ctjot",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "stardew_valley",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "tyrian",
        "tmc",
        "hades",
        "factorio",
        "landstalker",
        "soe",
        "crosscode",
        "crystal_project",
        "dw1",
        "pokemon_emerald",
        "rimworld",
        "tloz_oos",
        "sonic_heroes",
        "wargroove2",
        "ladx",
        "gstla",
        "civ_6",
        "osrs",
        "tloz_ph",
        "smz3",
        "undertale",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "ufo50",
        "tunic",
        "sc2",
        "factorio_saws",
        "pokemon_frlg"
    ],
    "isometric": [
        "chainedechoes",
        "pokemon_rb",
        "spyro3",
        "placidplasticducksim",
        "pokemon_crystal",
        "mmbn3",
        "balatro",
        "openrct2",
        "wargroove",
        "against_the_storm",
        "alttp",
        "meritous",
        "sims4",
        "ff1",
        "ff4fe",
        "ffmq",
        "pmd_eos",
        "overcooked2",
        "shapez",
        "brotato",
        "tloz",
        "yugiohddm",
        "adventure",
        "poe",
        "shorthike",
        "inscryption",
        "ffta",
        "hylics2",
        "ctjot",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "stardew_valley",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "tyrian",
        "tmc",
        "hades",
        "factorio",
        "landstalker",
        "soe",
        "crosscode",
        "crystal_project",
        "dw1",
        "pokemon_emerald",
        "rimworld",
        "tloz_oos",
        "sonic_heroes",
        "wargroove2",
        "ladx",
        "gstla",
        "civ_6",
        "osrs",
        "tloz_ph",
        "smz3",
        "undertale",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "ufo50",
        "tunic",
        "sc2",
        "factorio_saws",
        "pokemon_frlg"
    ],
    "fantasy": [
        "dark_souls_3",
        "timespinner",
        "wargroove",
        "enderlilies",
        "zelda2",
        "sims4",
        "blasphemous",
        "ff4fe",
        "cat_quest",
        "seaofthieves",
        "tloz",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "oribf",
        "pseudoregalia",
        "crystal_project",
        "pokemon_emerald",
        "banjo_tooie",
        "terraria",
        "gstla",
        "civ_6",
        "lunacid",
        "osrs",
        "huniepop",
        "earthbound",
        "tww",
        "tunic",
        "sm64ex",
        "frogmonster",
        "celeste",
        "lufia2ac",
        "yugiohddm",
        "fm",
        "shorthike",
        "ss",
        "minecraft",
        "dkc2",
        "papermario",
        "rogue_legacy",
        "v6",
        "tloz_oos",
        "yoshisisland",
        "monster_sanctuary",
        "ladx",
        "tloz_ph",
        "adventure",
        "pokemon_frlg",
        "hk",
        "pokemon_rb",
        "zork_grand_inquisitor",
        "dark_souls_2",
        "tp",
        "spire",
        "albw",
        "cuphead",
        "sm64hacks",
        "noita",
        "ultrakill",
        "landstalker",
        "mm_recomp",
        "wargroove2",
        "faxanadu",
        "celeste_open_world",
        "undertale",
        "mlss",
        "chainedechoes",
        "heretic",
        "pokemon_crystal",
        "against_the_storm",
        "alttp",
        "ff1",
        "pmd_eos",
        "ffmq",
        "dsr",
        "ffta",
        "hylics2",
        "ctjot",
        "oot",
        "stardew_valley",
        "tmc",
        "hades",
        "smo",
        "kh1",
        "smw",
        "yugioh06",
        "kh2"
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
        "mm3",
        "pokemon_crystal",
        "kdl3",
        "alttp",
        "zelda2",
        "ff4fe",
        "ff1",
        "ffmq",
        "sm",
        "tloz",
        "lufia2ac",
        "dkc3",
        "mmx3",
        "ffta",
        "dkc",
        "xenobladex",
        "dkc2",
        "papermario",
        "soe",
        "pokemon_emerald",
        "tetrisattack",
        "yoshisisland",
        "kh1",
        "faxanadu",
        "gstla",
        "sm_map_rando",
        "smz3",
        "smw",
        "earthbound",
        "adventure",
        "mlss"
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
        "spyro3",
        "doom_ii",
        "simpsonshitnrun",
        "against_the_storm",
        "alttp",
        "sotn",
        "enderlilies",
        "zelda2",
        "sims4",
        "blasphemous",
        "dark_souls_2",
        "overcooked2",
        "seaofthieves",
        "tloz",
        "lufia2ac",
        "dkc3",
        "messenger",
        "spire",
        "tp",
        "ffta",
        "metroidfusion",
        "albw",
        "lego_star_wars_tcs",
        "mlss",
        "k64",
        "oot",
        "ss",
        "oribf",
        "celeste64",
        "diddy_kong_racing",
        "dkc2",
        "sly1",
        "tboir",
        "tmc",
        "cvcotm",
        "hades",
        "mm_recomp",
        "papermario",
        "rogue_legacy",
        "ttyd",
        "banjo_tooie",
        "terraria",
        "smo",
        "tloz_oos",
        "ladx",
        "gstla",
        "hcniko",
        "jakanddaxter",
        "witness",
        "tloz_ph",
        "smz3",
        "undertale",
        "earthbound",
        "tloz_ooa",
        "tww",
        "dkc"
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
        "spyro3",
        "timespinner",
        "pokemon_crystal",
        "mmbn3",
        "openrct2",
        "simpsonshitnrun",
        "against_the_storm",
        "alttp",
        "apeescape",
        "pmd_eos",
        "sm",
        "shorthike",
        "ahit",
        "ror1",
        "ffta",
        "metroidfusion",
        "ctjot",
        "mk64",
        "oot",
        "diddy_kong_racing",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "mm_recomp",
        "rogue_legacy",
        "pokemon_emerald",
        "rimworld",
        "v6",
        "tloz_oos",
        "wl4",
        "jakanddaxter",
        "witness",
        "sm_map_rando",
        "tloz_ph",
        "earthbound",
        "tloz_ooa",
        "sc2",
        "outer_wilds"
    ],
    "strategy": [
        "chainedechoes",
        "pokemon_rb",
        "mmbn3",
        "balatro",
        "openrct2",
        "wargroove",
        "against_the_storm",
        "pokemon_frlg",
        "pmd_eos",
        "overcooked2",
        "shapez",
        "yugiohddm",
        "spire",
        "fm",
        "inscryption",
        "ffta",
        "hylics2",
        "dontstarvetogether",
        "stardew_valley",
        "factorio",
        "crystal_project",
        "pokemon_emerald",
        "rimworld",
        "terraria",
        "monster_sanctuary",
        "wargroove2",
        "civ_6",
        "satisfactory",
        "undertale",
        "yugioh06",
        "huniepop",
        "earthbound",
        "ufo50",
        "sc2",
        "factorio_saws",
        "huniepop2"
    ],
    "(rts)": [
        "mmbn3",
        "openrct2",
        "against_the_storm",
        "rimworld",
        "sc2"
    ],
    "simulator": [
        "placidplasticducksim",
        "getting_over_it",
        "openrct2",
        "against_the_storm",
        "doronko_wanko",
        "sims4",
        "overcooked2",
        "shapez",
        "seaofthieves",
        "raft",
        "dontstarvetogether",
        "factorio_saws",
        "stardew_valley",
        "minecraft",
        "noita",
        "factorio",
        "rimworld",
        "terraria",
        "civ_6",
        "satisfactory",
        "huniepop",
        "powerwashsimulator",
        "outer_wilds",
        "huniepop2"
    ],
    "indie": [
        "chainedechoes",
        "hk",
        "timespinner",
        "getting_over_it",
        "openrct2",
        "balatro",
        "wargroove",
        "against_the_storm",
        "enderlilies",
        "blasphemous",
        "frogmonster",
        "overcooked2",
        "cat_quest",
        "shapez",
        "brotato",
        "celeste",
        "messenger",
        "spire",
        "aquaria",
        "lingo",
        "shorthike",
        "ahit",
        "ror1",
        "inscryption",
        "hylics2",
        "raft",
        "dontstarvetogether",
        "cuphead",
        "stardew_valley",
        "pseudoregalia",
        "celeste64",
        "shivers",
        "subnautica",
        "tboir",
        "ror2",
        "powerwashsimulator",
        "hades",
        "noita",
        "factorio",
        "ultrakill",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "rimworld",
        "v6",
        "terraria",
        "outer_wilds",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "wargroove2",
        "osu",
        "hcniko",
        "lunacid",
        "peaks_of_yore",
        "lethal_company",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "huniepop",
        "satisfactory",
        "undertale",
        "ufo50",
        "tunic",
        "factorio_saws",
        "animal_well",
        "huniepop2"
    ],
    "xbox series x|s": [
        "placidplasticducksim",
        "animal_well",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "enderlilies",
        "brotato",
        "seaofthieves",
        "inscryption",
        "raft",
        "ror2",
        "hades",
        "trackmania",
        "momodoramoonlitfarewell",
        "outer_wilds",
        "wargroove2",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "subnautica"
    ],
    "xbox": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "simpsonshitnrun",
        "wargroove",
        "residentevil2remake",
        "against_the_storm",
        "sotn",
        "enderlilies",
        "sims4",
        "blasphemous",
        "dark_souls_2",
        "overcooked2",
        "brotato",
        "seaofthieves",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "raft",
        "lego_star_wars_tcs",
        "cuphead",
        "stardew_valley",
        "oribf",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "dw1",
        "momodoramoonlitfarewell",
        "trackmania",
        "terraria",
        "sa2b",
        "sadx",
        "outer_wilds",
        "monster_sanctuary",
        "sonic_heroes",
        "wargroove2",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "dlcquest",
        "residentevil3remake",
        "satisfactory",
        "undertale",
        "tunic",
        "powerwashsimulator",
        "animal_well"
    ],
    "series": [
        "placidplasticducksim",
        "animal_well",
        "doom_ii",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "enderlilies",
        "brotato",
        "seaofthieves",
        "inscryption",
        "raft",
        "subnautica",
        "ror2",
        "hades",
        "trackmania",
        "momodoramoonlitfarewell",
        "wargroove2",
        "doom_1993",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "x|s": [
        "placidplasticducksim",
        "animal_well",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "enderlilies",
        "brotato",
        "seaofthieves",
        "inscryption",
        "raft",
        "ror2",
        "hades",
        "trackmania",
        "momodoramoonlitfarewell",
        "outer_wilds",
        "wargroove2",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "subnautica"
    ],
    "pc (microsoft windows)": [
        "dark_souls_3",
        "timespinner",
        "wargroove",
        "enderlilies",
        "meritous",
        "sims4",
        "blasphemous",
        "toontown",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "oribf",
        "pseudoregalia",
        "crystal_project",
        "rimworld",
        "terraria",
        "osu",
        "civ_6",
        "lunacid",
        "peaks_of_yore",
        "osrs",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "musedash",
        "huniepop",
        "gzdoom",
        "tunic",
        "sc2",
        "animal_well",
        "placidplasticducksim",
        "doom_ii",
        "balatro",
        "simpsonshitnrun",
        "doronko_wanko",
        "frogmonster",
        "celeste",
        "lingo",
        "shorthike",
        "raft",
        "dontstarvetogether",
        "celeste64",
        "minecraft",
        "tyrian",
        "crosscode",
        "rogue_legacy",
        "bumpstik",
        "v6",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "ufo50",
        "hk",
        "zork_grand_inquisitor",
        "getting_over_it",
        "residentevil2remake",
        "dark_souls_2",
        "overcooked2",
        "shapez",
        "spire",
        "lego_star_wars_tcs",
        "cuphead",
        "shivers",
        "ror2",
        "noita",
        "ultrakill",
        "landstalker",
        "trackmania",
        "momodoramoonlitfarewell",
        "sadx",
        "wargroove2",
        "lethal_company",
        "witness",
        "celeste_open_world",
        "undertale",
        "outer_wilds",
        "subnautica",
        "huniepop2",
        "chainedechoes",
        "heretic",
        "openrct2",
        "against_the_storm",
        "quake",
        "dsr",
        "swr",
        "inscryption",
        "hylics2",
        "factorio_saws",
        "stardew_valley",
        "hades",
        "factorio",
        "sa2b",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "residentevil3remake",
        "powerwashsimulator"
    ],
    "pc": [
        "dark_souls_3",
        "timespinner",
        "wargroove",
        "enderlilies",
        "meritous",
        "sims4",
        "blasphemous",
        "toontown",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "oribf",
        "pseudoregalia",
        "crystal_project",
        "rimworld",
        "terraria",
        "osu",
        "civ_6",
        "lunacid",
        "peaks_of_yore",
        "osrs",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "musedash",
        "huniepop",
        "gzdoom",
        "tunic",
        "sc2",
        "animal_well",
        "placidplasticducksim",
        "doom_ii",
        "balatro",
        "simpsonshitnrun",
        "doronko_wanko",
        "frogmonster",
        "celeste",
        "lingo",
        "shorthike",
        "raft",
        "dontstarvetogether",
        "celeste64",
        "minecraft",
        "tyrian",
        "crosscode",
        "rogue_legacy",
        "bumpstik",
        "v6",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "ufo50",
        "hk",
        "zork_grand_inquisitor",
        "getting_over_it",
        "residentevil2remake",
        "dark_souls_2",
        "overcooked2",
        "shapez",
        "spire",
        "lego_star_wars_tcs",
        "cuphead",
        "shivers",
        "ror2",
        "noita",
        "ultrakill",
        "landstalker",
        "trackmania",
        "momodoramoonlitfarewell",
        "sadx",
        "wargroove2",
        "lethal_company",
        "witness",
        "celeste_open_world",
        "undertale",
        "outer_wilds",
        "subnautica",
        "huniepop2",
        "chainedechoes",
        "heretic",
        "openrct2",
        "against_the_storm",
        "quake",
        "dsr",
        "swr",
        "inscryption",
        "hylics2",
        "factorio_saws",
        "stardew_valley",
        "hades",
        "factorio",
        "sa2b",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "residentevil3remake",
        "powerwashsimulator"
    ],
    "(microsoft": [
        "dark_souls_3",
        "timespinner",
        "wargroove",
        "enderlilies",
        "meritous",
        "sims4",
        "blasphemous",
        "toontown",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "oribf",
        "pseudoregalia",
        "crystal_project",
        "rimworld",
        "terraria",
        "osu",
        "civ_6",
        "lunacid",
        "peaks_of_yore",
        "osrs",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "musedash",
        "huniepop",
        "gzdoom",
        "tunic",
        "sc2",
        "animal_well",
        "placidplasticducksim",
        "doom_ii",
        "balatro",
        "simpsonshitnrun",
        "doronko_wanko",
        "frogmonster",
        "celeste",
        "lingo",
        "shorthike",
        "raft",
        "dontstarvetogether",
        "celeste64",
        "minecraft",
        "tyrian",
        "crosscode",
        "rogue_legacy",
        "bumpstik",
        "v6",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "ufo50",
        "hk",
        "zork_grand_inquisitor",
        "getting_over_it",
        "residentevil2remake",
        "dark_souls_2",
        "overcooked2",
        "shapez",
        "spire",
        "lego_star_wars_tcs",
        "cuphead",
        "shivers",
        "ror2",
        "noita",
        "ultrakill",
        "landstalker",
        "trackmania",
        "momodoramoonlitfarewell",
        "sadx",
        "wargroove2",
        "lethal_company",
        "witness",
        "celeste_open_world",
        "undertale",
        "outer_wilds",
        "subnautica",
        "huniepop2",
        "chainedechoes",
        "heretic",
        "openrct2",
        "against_the_storm",
        "quake",
        "dsr",
        "swr",
        "inscryption",
        "hylics2",
        "factorio_saws",
        "stardew_valley",
        "hades",
        "factorio",
        "sa2b",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "residentevil3remake",
        "powerwashsimulator"
    ],
    "windows)": [
        "dark_souls_3",
        "timespinner",
        "wargroove",
        "enderlilies",
        "meritous",
        "sims4",
        "blasphemous",
        "toontown",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "aquaria",
        "ahit",
        "ror1",
        "oribf",
        "pseudoregalia",
        "crystal_project",
        "rimworld",
        "terraria",
        "osu",
        "civ_6",
        "lunacid",
        "peaks_of_yore",
        "osrs",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "musedash",
        "huniepop",
        "gzdoom",
        "tunic",
        "sc2",
        "animal_well",
        "placidplasticducksim",
        "doom_ii",
        "balatro",
        "simpsonshitnrun",
        "doronko_wanko",
        "frogmonster",
        "celeste",
        "lingo",
        "shorthike",
        "raft",
        "dontstarvetogether",
        "celeste64",
        "minecraft",
        "tyrian",
        "crosscode",
        "rogue_legacy",
        "bumpstik",
        "v6",
        "kindergarten_2",
        "aus",
        "monster_sanctuary",
        "ufo50",
        "hk",
        "zork_grand_inquisitor",
        "getting_over_it",
        "residentevil2remake",
        "dark_souls_2",
        "overcooked2",
        "shapez",
        "spire",
        "lego_star_wars_tcs",
        "cuphead",
        "shivers",
        "ror2",
        "noita",
        "ultrakill",
        "landstalker",
        "trackmania",
        "momodoramoonlitfarewell",
        "sadx",
        "wargroove2",
        "lethal_company",
        "witness",
        "celeste_open_world",
        "undertale",
        "outer_wilds",
        "subnautica",
        "huniepop2",
        "chainedechoes",
        "heretic",
        "openrct2",
        "against_the_storm",
        "quake",
        "dsr",
        "swr",
        "inscryption",
        "hylics2",
        "factorio_saws",
        "stardew_valley",
        "hades",
        "factorio",
        "sa2b",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "residentevil3remake",
        "powerwashsimulator"
    ],
    "playstation 5": [
        "placidplasticducksim",
        "animal_well",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "inscryption",
        "raft",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "trackmania",
        "momodoramoonlitfarewell",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "playstation": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "spyro3",
        "timespinner",
        "balatro",
        "simpsonshitnrun",
        "wargroove",
        "residentevil2remake",
        "against_the_storm",
        "sotn",
        "apeescape",
        "enderlilies",
        "sims4",
        "blasphemous",
        "dark_souls_2",
        "overcooked2",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "fm",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "raft",
        "lego_star_wars_tcs",
        "cuphead",
        "stardew_valley",
        "sly1",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "dw1",
        "momodoramoonlitfarewell",
        "trackmania",
        "v6",
        "terraria",
        "sa2b",
        "sadx",
        "outer_wilds",
        "kh1",
        "monster_sanctuary",
        "sonic_heroes",
        "jakanddaxter",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "satisfactory",
        "residentevil3remake",
        "rac2",
        "kh2",
        "undertale",
        "tunic",
        "powerwashsimulator",
        "animal_well"
    ],
    "5": [
        "placidplasticducksim",
        "animal_well",
        "balatro",
        "residentevil2remake",
        "against_the_storm",
        "brotato",
        "seaofthieves",
        "messenger",
        "poe",
        "inscryption",
        "raft",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "trackmania",
        "momodoramoonlitfarewell",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "nintendo switch": [
        "chainedechoes",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "against_the_storm",
        "doronko_wanko",
        "enderlilies",
        "megamix",
        "blasphemous",
        "overcooked2",
        "cat_quest",
        "brotato",
        "celeste",
        "messenger",
        "dsr",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "dontstarvetogether",
        "cuphead",
        "stardew_valley",
        "oribf",
        "subnautica",
        "tboir",
        "ror2",
        "hades",
        "factorio",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "v6",
        "terraria",
        "smo",
        "outer_wilds",
        "monster_sanctuary",
        "wargroove2",
        "hcniko",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "musedash",
        "undertale",
        "ufo50",
        "tunic",
        "powerwashsimulator",
        "animal_well"
    ],
    "nintendo": [
        "timespinner",
        "kdl3",
        "wargroove",
        "enderlilies",
        "zelda2",
        "blasphemous",
        "ff4fe",
        "cat_quest",
        "brotato",
        "tloz",
        "dkc3",
        "messenger",
        "ahit",
        "ror1",
        "mario_kart_double_dash",
        "oribf",
        "star_fox_64",
        "metroidprime",
        "crystal_project",
        "dw1",
        "banjo_tooie",
        "terraria",
        "tetrisattack",
        "wl4",
        "bomb_rush_cyberfunk",
        "musedash",
        "smz3",
        "earthbound",
        "tww",
        "tunic",
        "animal_well",
        "placidplasticducksim",
        "balatro",
        "simpsonshitnrun",
        "doronko_wanko",
        "sm64ex",
        "celeste",
        "lufia2ac",
        "shorthike",
        "mmx3",
        "dontstarvetogether",
        "mk64",
        "mm2",
        "dkc2",
        "wl",
        "papermario",
        "crosscode",
        "soe",
        "rogue_legacy",
        "v6",
        "tloz_oos",
        "marioland2",
        "dk64",
        "yoshisisland",
        "monster_sanctuary",
        "ladx",
        "tloz_ph",
        "tloz_ooa",
        "ufo50",
        "hk",
        "pokemon_rb",
        "mm3",
        "cv64",
        "overcooked2",
        "sm",
        "metroidfusion",
        "albw",
        "cuphead",
        "sm64hacks",
        "diddy_kong_racing",
        "tboir",
        "sms",
        "ror2",
        "mm_recomp",
        "momodoramoonlitfarewell",
        "wargroove2",
        "faxanadu",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "outer_wilds",
        "subnautica",
        "dkc",
        "chainedechoes",
        "pokemon_crystal",
        "against_the_storm",
        "alttp",
        "megamix",
        "ff1",
        "pmd_eos",
        "ffmq",
        "dsr",
        "swr",
        "inscryption",
        "ctjot",
        "oot",
        "k64",
        "stardew_valley",
        "tmc",
        "hades",
        "factorio",
        "smo",
        "sonic_heroes",
        "hcniko",
        "smw",
        "luigismansion",
        "powerwashsimulator"
    ],
    "switch": [
        "chainedechoes",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "against_the_storm",
        "doronko_wanko",
        "enderlilies",
        "megamix",
        "blasphemous",
        "overcooked2",
        "cat_quest",
        "brotato",
        "celeste",
        "messenger",
        "dsr",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "dontstarvetogether",
        "cuphead",
        "stardew_valley",
        "oribf",
        "subnautica",
        "tboir",
        "ror2",
        "hades",
        "factorio",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "v6",
        "terraria",
        "smo",
        "outer_wilds",
        "monster_sanctuary",
        "wargroove2",
        "hcniko",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "musedash",
        "undertale",
        "ufo50",
        "tunic",
        "powerwashsimulator",
        "animal_well"
    ],
    "roguelite": [
        "brotato",
        "ror2",
        "noita",
        "hades",
        "ror1",
        "against_the_storm"
    ],
    "a hat in time": [
        "ahit"
    ],
    "a": [
        "shorthike",
        "ahit",
        "smz3",
        "alttp",
        "albw"
    ],
    "hat": [
        "ahit"
    ],
    "in": [
        "ss",
        "metroidprime",
        "sms",
        "sm_map_rando",
        "tloz_ph",
        "tmc",
        "ahit",
        "alttp",
        "papermario",
        "smw",
        "earthbound",
        "tloz_ooa",
        "zelda2",
        "albw",
        "oot",
        "tloz_oos",
        "kh1",
        "sm"
    ],
    "first person": [
        "zork_grand_inquisitor",
        "heretic",
        "doom_ii",
        "cv64",
        "sims4",
        "frogmonster",
        "quake",
        "seaofthieves",
        "yugiohddm",
        "fm",
        "lingo",
        "ahit",
        "swr",
        "inscryption",
        "hylics2",
        "raft",
        "shivers",
        "minecraft",
        "star_fox_64",
        "subnautica",
        "metroidprime",
        "ultrakill",
        "trackmania",
        "lunacid",
        "lethal_company",
        "witness",
        "doom_1993",
        "satisfactory",
        "huniepop",
        "earthbound",
        "powerwashsimulator",
        "outer_wilds",
        "huniepop2"
    ],
    "first": [
        "zork_grand_inquisitor",
        "heretic",
        "doom_ii",
        "cv64",
        "sims4",
        "frogmonster",
        "quake",
        "seaofthieves",
        "yugiohddm",
        "fm",
        "lingo",
        "ahit",
        "swr",
        "inscryption",
        "hylics2",
        "raft",
        "shivers",
        "minecraft",
        "star_fox_64",
        "subnautica",
        "metroidprime",
        "ultrakill",
        "trackmania",
        "lunacid",
        "lethal_company",
        "witness",
        "doom_1993",
        "satisfactory",
        "huniepop",
        "earthbound",
        "powerwashsimulator",
        "outer_wilds",
        "huniepop2"
    ],
    "person": [
        "dark_souls_3",
        "sims4",
        "toontown",
        "cat_quest",
        "seaofthieves",
        "ahit",
        "mario_kart_double_dash",
        "xenobladex",
        "pseudoregalia",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "crystal_project",
        "dw1",
        "banjo_tooie",
        "gstla",
        "jakanddaxter",
        "lunacid",
        "bomb_rush_cyberfunk",
        "huniepop",
        "earthbound",
        "tww",
        "gzdoom",
        "spyro3",
        "placidplasticducksim",
        "doom_ii",
        "simpsonshitnrun",
        "sm64ex",
        "frogmonster",
        "yugiohddm",
        "fm",
        "lingo",
        "raft",
        "mk64",
        "ss",
        "celeste64",
        "minecraft",
        "papermario",
        "soe",
        "dk64",
        "zork_grand_inquisitor",
        "getting_over_it",
        "cv64",
        "residentevil2remake",
        "dark_souls_2",
        "tp",
        "albw",
        "lego_star_wars_tcs",
        "sm64hacks",
        "shivers",
        "diddy_kong_racing",
        "sms",
        "ror2",
        "ultrakill",
        "mm_recomp",
        "trackmania",
        "sadx",
        "lethal_company",
        "witness",
        "doom_1993",
        "rac2",
        "subnautica",
        "outer_wilds",
        "huniepop2",
        "heretic",
        "apeescape",
        "megamix",
        "quake",
        "dsr",
        "swr",
        "inscryption",
        "hylics2",
        "oot",
        "sa2b",
        "smo",
        "kh1",
        "sonic_heroes",
        "hcniko",
        "satisfactory",
        "residentevil3remake",
        "kh2",
        "luigismansion",
        "powerwashsimulator"
    ],
    "third person": [
        "dark_souls_3",
        "spyro3",
        "placidplasticducksim",
        "getting_over_it",
        "cv64",
        "simpsonshitnrun",
        "residentevil2remake",
        "apeescape",
        "megamix",
        "sims4",
        "sm64ex",
        "dark_souls_2",
        "toontown",
        "cat_quest",
        "tp",
        "dsr",
        "ahit",
        "swr",
        "hylics2",
        "raft",
        "albw",
        "lego_star_wars_tcs",
        "mario_kart_double_dash",
        "mk64",
        "oot",
        "sm64hacks",
        "ss",
        "pseudoregalia",
        "celeste64",
        "xenobladex",
        "minecraft",
        "diddy_kong_racing",
        "star_fox_64",
        "sly1",
        "sms",
        "ror2",
        "mm_recomp",
        "papermario",
        "crystal_project",
        "soe",
        "dw1",
        "trackmania",
        "banjo_tooie",
        "sa2b",
        "dk64",
        "sadx",
        "kh1",
        "smo",
        "sonic_heroes",
        "gstla",
        "hcniko",
        "jakanddaxter",
        "bomb_rush_cyberfunk",
        "residentevil3remake",
        "rac2",
        "kh2",
        "tww",
        "gzdoom",
        "luigismansion"
    ],
    "third": [
        "dark_souls_3",
        "spyro3",
        "placidplasticducksim",
        "getting_over_it",
        "cv64",
        "simpsonshitnrun",
        "residentevil2remake",
        "apeescape",
        "megamix",
        "sims4",
        "sm64ex",
        "dark_souls_2",
        "toontown",
        "cat_quest",
        "tp",
        "dsr",
        "ahit",
        "swr",
        "hylics2",
        "raft",
        "albw",
        "lego_star_wars_tcs",
        "mario_kart_double_dash",
        "mk64",
        "oot",
        "sm64hacks",
        "ss",
        "pseudoregalia",
        "celeste64",
        "xenobladex",
        "minecraft",
        "diddy_kong_racing",
        "star_fox_64",
        "sly1",
        "sms",
        "ror2",
        "mm_recomp",
        "papermario",
        "crystal_project",
        "soe",
        "dw1",
        "trackmania",
        "banjo_tooie",
        "sa2b",
        "dk64",
        "sadx",
        "kh1",
        "smo",
        "sonic_heroes",
        "gstla",
        "hcniko",
        "jakanddaxter",
        "bomb_rush_cyberfunk",
        "residentevil3remake",
        "rac2",
        "kh2",
        "tww",
        "gzdoom",
        "luigismansion"
    ],
    "platform": [
        "hk",
        "spyro3",
        "mm3",
        "timespinner",
        "getting_over_it",
        "kdl3",
        "cv64",
        "simpsonshitnrun",
        "sotn",
        "apeescape",
        "enderlilies",
        "zelda2",
        "blasphemous",
        "mzm",
        "sm64ex",
        "sm",
        "celeste",
        "dkc3",
        "messenger",
        "aquaria",
        "ahit",
        "ror1",
        "mmx3",
        "metroidfusion",
        "hylics2",
        "lego_star_wars_tcs",
        "cuphead",
        "k64",
        "sm64hacks",
        "oribf",
        "celeste64",
        "mm2",
        "pseudoregalia",
        "zillion",
        "dkc2",
        "sly1",
        "metroidprime",
        "sms",
        "wl",
        "cvcotm",
        "ultrakill",
        "crystal_project",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "banjo_tooie",
        "terraria",
        "marioland2",
        "dk64",
        "sa2b",
        "sadx",
        "smo",
        "v6",
        "aus",
        "monster_sanctuary",
        "sonic_heroes",
        "wl4",
        "faxanadu",
        "hcniko",
        "jakanddaxter",
        "peaks_of_yore",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "dlcquest",
        "smw",
        "rac2",
        "smz3",
        "gzdoom",
        "ufo50",
        "animal_well",
        "yoshisisland",
        "dkc"
    ],
    "action": [
        "dark_souls_3",
        "timespinner",
        "kdl3",
        "enderlilies",
        "zelda2",
        "sims4",
        "blasphemous",
        "ff4fe",
        "mzm",
        "cat_quest",
        "brotato",
        "seaofthieves",
        "tloz",
        "dkc3",
        "messenger",
        "poe",
        "ahit",
        "ror1",
        "mario_kart_double_dash",
        "xenobladex",
        "oribf",
        "pseudoregalia",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "dw1",
        "pokemon_emerald",
        "banjo_tooie",
        "terraria",
        "tetrisattack",
        "wl4",
        "osu",
        "gstla",
        "jakanddaxter",
        "peaks_of_yore",
        "bomb_rush_cyberfunk",
        "dlcquest",
        "musedash",
        "smz3",
        "earthbound",
        "tww",
        "gzdoom",
        "tunic",
        "sc2",
        "animal_well",
        "spyro3",
        "doom_ii",
        "mmbn3",
        "simpsonshitnrun",
        "doronko_wanko",
        "sotn",
        "sm64ex",
        "frogmonster",
        "celeste",
        "mmx3",
        "dontstarvetogether",
        "mk64",
        "ss",
        "celeste64",
        "mm2",
        "dkc2",
        "wl",
        "tyrian",
        "papermario",
        "crosscode",
        "soe",
        "rogue_legacy",
        "v6",
        "tloz_oos",
        "marioland2",
        "dk64",
        "yoshisisland",
        "aus",
        "monster_sanctuary",
        "ladx",
        "tloz_ph",
        "tloz_ooa",
        "ufo50",
        "pokemon_frlg",
        "hk",
        "pokemon_rb",
        "mm3",
        "getting_over_it",
        "cv64",
        "residentevil2remake",
        "dark_souls_2",
        "overcooked2",
        "sm",
        "tp",
        "metroidfusion",
        "albw",
        "cuphead",
        "lego_star_wars_tcs",
        "sm64hacks",
        "diddy_kong_racing",
        "sms",
        "ror2",
        "noita",
        "ultrakill",
        "landstalker",
        "mm_recomp",
        "trackmania",
        "momodoramoonlitfarewell",
        "sadx",
        "faxanadu",
        "lethal_company",
        "sm_map_rando",
        "doom_1993",
        "celeste_open_world",
        "rac2",
        "outer_wilds",
        "mlss",
        "chainedechoes",
        "dkc",
        "pokemon_crystal",
        "alttp",
        "apeescape",
        "ff1",
        "ffmq",
        "quake",
        "dsr",
        "swr",
        "ctjot",
        "oot",
        "k64",
        "tmc",
        "cvcotm",
        "hades",
        "sa2b",
        "smo",
        "kh1",
        "sonic_heroes",
        "hcniko",
        "smw",
        "residentevil3remake",
        "kh2",
        "luigismansion"
    ],
    "playstation 4": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "residentevil2remake",
        "enderlilies",
        "sims4",
        "blasphemous",
        "overcooked2",
        "cat_quest",
        "brotato",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "cuphead",
        "stardew_valley",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "trackmania",
        "v6",
        "terraria",
        "monster_sanctuary",
        "jakanddaxter",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "undertale",
        "residentevil3remake",
        "kh2",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "4": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "residentevil2remake",
        "enderlilies",
        "sims4",
        "blasphemous",
        "overcooked2",
        "cat_quest",
        "brotato",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "cuphead",
        "stardew_valley",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "dw1",
        "trackmania",
        "v6",
        "terraria",
        "wl4",
        "monster_sanctuary",
        "jakanddaxter",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "undertale",
        "residentevil3remake",
        "kh2",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "mac": [
        "chainedechoes",
        "hk",
        "zork_grand_inquisitor",
        "timespinner",
        "heretic",
        "doom_ii",
        "getting_over_it",
        "balatro",
        "openrct2",
        "residentevil2remake",
        "sims4",
        "blasphemous",
        "toontown",
        "overcooked2",
        "cat_quest",
        "shapez",
        "brotato",
        "quake",
        "celeste",
        "poe",
        "aquaria",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "hylics2",
        "lego_star_wars_tcs",
        "dontstarvetogether",
        "cuphead",
        "stardew_valley",
        "minecraft",
        "tyrian",
        "hades",
        "factorio",
        "landstalker",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "rimworld",
        "v6",
        "terraria",
        "monster_sanctuary",
        "osu",
        "civ_6",
        "witness",
        "osrs",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "residentevil3remake",
        "huniepop",
        "undertale",
        "tunic",
        "sc2",
        "factorio_saws",
        "subnautica",
        "huniepop2"
    ],
    "xbox one": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "residentevil2remake",
        "enderlilies",
        "sims4",
        "blasphemous",
        "overcooked2",
        "brotato",
        "seaofthieves",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "cuphead",
        "stardew_valley",
        "oribf",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "trackmania",
        "terraria",
        "monster_sanctuary",
        "wargroove2",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "undertale",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "one": [
        "chainedechoes",
        "dark_souls_3",
        "hk",
        "placidplasticducksim",
        "timespinner",
        "balatro",
        "wargroove",
        "residentevil2remake",
        "enderlilies",
        "sims4",
        "blasphemous",
        "overcooked2",
        "brotato",
        "seaofthieves",
        "celeste",
        "messenger",
        "dsr",
        "poe",
        "shorthike",
        "ahit",
        "ror1",
        "swr",
        "inscryption",
        "cuphead",
        "stardew_valley",
        "oribf",
        "subnautica",
        "ror2",
        "hades",
        "crosscode",
        "rogue_legacy",
        "trackmania",
        "terraria",
        "monster_sanctuary",
        "wargroove2",
        "witness",
        "bomb_rush_cyberfunk",
        "celeste_open_world",
        "undertale",
        "residentevil3remake",
        "tunic",
        "powerwashsimulator",
        "outer_wilds"
    ],
    "time travel": [
        "timespinner",
        "pmd_eos",
        "ahit",
        "mm_recomp",
        "apeescape",
        "earthbound",
        "tloz_ooa",
        "ctjot",
        "oot",
        "tloz_oos",
        "outer_wilds"
    ],
    "travel": [
        "timespinner",
        "pmd_eos",
        "ahit",
        "mm_recomp",
        "apeescape",
        "earthbound",
        "tloz_ooa",
        "ctjot",
        "oot",
        "tloz_oos",
        "outer_wilds"
    ],
    "spaceship": [
        "star_fox_64",
        "metroidprime",
        "civ_6",
        "ahit",
        "metroidfusion",
        "mzm",
        "v6"
    ],
    "female protagonist": [
        "timespinner",
        "cv64",
        "enderlilies",
        "mzm",
        "sm",
        "celeste",
        "dkc3",
        "shorthike",
        "ahit",
        "metroidfusion",
        "celeste64",
        "dkc2",
        "metroidprime",
        "rogue_legacy",
        "hcniko",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "earthbound"
    ],
    "female": [
        "timespinner",
        "cv64",
        "enderlilies",
        "mzm",
        "sm",
        "celeste",
        "dkc3",
        "shorthike",
        "ahit",
        "metroidfusion",
        "celeste64",
        "dkc2",
        "metroidprime",
        "rogue_legacy",
        "hcniko",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "earthbound"
    ],
    "protagonist": [
        "hk",
        "timespinner",
        "cv64",
        "alttp",
        "enderlilies",
        "zelda2",
        "blasphemous",
        "mzm",
        "sm",
        "quake",
        "celeste",
        "dkc3",
        "shorthike",
        "ahit",
        "metroidfusion",
        "mlss",
        "oot",
        "k64",
        "ss",
        "celeste64",
        "dkc2",
        "metroidprime",
        "tmc",
        "ultrakill",
        "papermario",
        "rogue_legacy",
        "pokemon_emerald",
        "tloz_oos",
        "ladx",
        "gstla",
        "hcniko",
        "jakanddaxter",
        "sm_map_rando",
        "tloz_ph",
        "doom_1993",
        "celeste_open_world",
        "undertale",
        "earthbound",
        "tloz_ooa",
        "dkc"
    ],
    "action-adventure": [
        "dark_souls_3",
        "hk",
        "timespinner",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "dark_souls_2",
        "sm",
        "seaofthieves",
        "aquaria",
        "ahit",
        "metroidfusion",
        "albw",
        "dontstarvetogether",
        "oot",
        "ss",
        "xenobladex",
        "zillion",
        "minecraft",
        "metroidprime",
        "sms",
        "tmc",
        "cvcotm",
        "landstalker",
        "mm_recomp",
        "crosscode",
        "rogue_legacy",
        "banjo_tooie",
        "terraria",
        "tloz_oos",
        "kh1",
        "aus",
        "ladx",
        "sm_map_rando",
        "tloz_ph",
        "tloz_ooa",
        "tww",
        "luigismansion"
    ],
    "cute": [
        "celeste",
        "hcniko",
        "shorthike",
        "ahit",
        "celeste_open_world",
        "musedash",
        "undertale",
        "sims4",
        "tunic",
        "animal_well"
    ],
    "snow": [
        "minecraft",
        "celeste",
        "diddy_kong_racing",
        "dkc3",
        "gstla",
        "hcniko",
        "jakanddaxter",
        "metroidprime",
        "shorthike",
        "ahit",
        "celeste_open_world",
        "ffta",
        "albw",
        "mk64",
        "terraria",
        "stardew_valley",
        "lego_star_wars_tcs",
        "dkc"
    ],
    "wall jump": [
        "sms",
        "sm_map_rando",
        "cvcotm",
        "simpsonshitnrun",
        "ahit",
        "mmx3",
        "metroidfusion",
        "mzm",
        "smo",
        "oribf",
        "sm"
    ],
    "wall": [
        "doom_ii",
        "simpsonshitnrun",
        "mzm",
        "sm",
        "ahit",
        "mmx3",
        "ffta",
        "metroidfusion",
        "dkc",
        "oribf",
        "dkc2",
        "sms",
        "tmc",
        "cvcotm",
        "papermario",
        "rogue_legacy",
        "banjo_tooie",
        "smo",
        "ladx",
        "jakanddaxter",
        "sm_map_rando",
        "undertale",
        "mlss"
    ],
    "jump": [
        "sms",
        "sm_map_rando",
        "cvcotm",
        "simpsonshitnrun",
        "ahit",
        "mmx3",
        "metroidfusion",
        "mzm",
        "smo",
        "oribf",
        "sm"
    ],
    "3d platformer": [
        "sonic_heroes",
        "hcniko",
        "sms",
        "shorthike",
        "ahit",
        "bomb_rush_cyberfunk",
        "smo",
        "sm64ex",
        "sm64hacks"
    ],
    "3d": [
        "dark_souls_3",
        "spyro3",
        "cv64",
        "simpsonshitnrun",
        "sotn",
        "apeescape",
        "sm64ex",
        "frogmonster",
        "dark_souls_2",
        "quake",
        "dsr",
        "poe",
        "lingo",
        "shorthike",
        "ahit",
        "hylics2",
        "albw",
        "lego_star_wars_tcs",
        "mk64",
        "k64",
        "oot",
        "sm64hacks",
        "ss",
        "xenobladex",
        "minecraft",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "sms",
        "crystal_project",
        "dw1",
        "smo",
        "dk64",
        "kh1",
        "sonic_heroes",
        "hcniko",
        "jakanddaxter",
        "witness",
        "tloz_ph",
        "bomb_rush_cyberfunk",
        "tunic",
        "luigismansion",
        "powerwashsimulator"
    ],
    "platformer": [
        "sonic_heroes",
        "hcniko",
        "sms",
        "shorthike",
        "ahit",
        "bomb_rush_cyberfunk",
        "smo",
        "sm64ex",
        "sm64hacks"
    ],
    "swimming": [
        "spyro3",
        "alttp",
        "sm64ex",
        "quake",
        "dkc3",
        "aquaria",
        "ahit",
        "albw",
        "oot",
        "sm64hacks",
        "minecraft",
        "dkc2",
        "sms",
        "tmc",
        "banjo_tooie",
        "terraria",
        "smo",
        "kh1",
        "wl4",
        "hcniko",
        "jakanddaxter",
        "tloz_ooa",
        "subnautica",
        "dkc"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "tloz",
        "ss",
        "ladx",
        "tp",
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "alttp",
        "tloz_ooa",
        "tww",
        "albw",
        "oot",
        "tloz_oos"
    ],
    "of": [
        "spyro3",
        "pokemon_crystal",
        "cv64",
        "alttp",
        "sotn",
        "enderlilies",
        "zelda2",
        "pmd_eos",
        "seaofthieves",
        "tloz",
        "lufia2ac",
        "dkc3",
        "tp",
        "poe",
        "ror1",
        "ffta",
        "albw",
        "oot",
        "ss",
        "oribf",
        "celeste64",
        "dkc2",
        "star_fox_64",
        "sly1",
        "sms",
        "tboir",
        "ror2",
        "cvcotm",
        "tmc",
        "mm_recomp",
        "soe",
        "rogue_legacy",
        "pokemon_emerald",
        "tloz_oos",
        "dk64",
        "ladx",
        "jakanddaxter",
        "peaks_of_yore",
        "tloz_ph",
        "earthbound",
        "tloz_ooa",
        "tww",
        "luigismansion",
        "sc2",
        "dkc"
    ],
    "zelda:": [
        "ss",
        "ladx",
        "tp",
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "alttp",
        "tloz_ooa",
        "tww",
        "albw",
        "oot",
        "tloz_oos"
    ],
    "link": [
        "alttp",
        "zelda2",
        "smz3",
        "albw"
    ],
    "between": [
        "albw"
    ],
    "worlds": [
        "albw"
    ],
    "puzzle": [
        "zork_grand_inquisitor",
        "spyro3",
        "placidplasticducksim",
        "doom_ii",
        "cv64",
        "alttp",
        "shapez",
        "yugiohddm",
        "lufia2ac",
        "tp",
        "lingo",
        "inscryption",
        "metroidfusion",
        "albw",
        "oot",
        "ss",
        "oribf",
        "shivers",
        "zillion",
        "tmc",
        "mm_recomp",
        "crosscode",
        "rogue_legacy",
        "ttyd",
        "bumpstik",
        "v6",
        "tloz_oos",
        "tetrisattack",
        "outer_wilds",
        "wl4",
        "ladx",
        "hcniko",
        "witness",
        "tloz_ph",
        "ufo50",
        "undertale",
        "huniepop",
        "tloz_ooa",
        "tww",
        "candybox2",
        "tunic",
        "animal_well",
        "huniepop2"
    ],
    "historical": [
        "quake",
        "heretic",
        "civ_6",
        "fm",
        "albw",
        "soe",
        "candybox2",
        "ss"
    ],
    "sandbox": [
        "placidplasticducksim",
        "zelda2",
        "sims4",
        "shapez",
        "albw",
        "dontstarvetogether",
        "oot",
        "xenobladex",
        "stardew_valley",
        "factorio_saws",
        "minecraft",
        "sms",
        "noita",
        "factorio",
        "landstalker",
        "terraria",
        "smo",
        "faxanadu",
        "osrs",
        "satisfactory",
        "powerwashsimulator"
    ],
    "open world": [
        "pokemon_rb",
        "simpsonshitnrun",
        "sotn",
        "mzm",
        "sm64ex",
        "frogmonster",
        "toontown",
        "seaofthieves",
        "tloz",
        "lingo",
        "shorthike",
        "albw",
        "dontstarvetogether",
        "oot",
        "ss",
        "sm64hacks",
        "xenobladex",
        "minecraft",
        "subnautica",
        "metroidprime",
        "mm_recomp",
        "terraria",
        "smo",
        "gstla",
        "jakanddaxter",
        "witness",
        "osrs",
        "satisfactory",
        "smz3",
        "outer_wilds"
    ],
    "open": [
        "pokemon_rb",
        "simpsonshitnrun",
        "sotn",
        "mzm",
        "sm64ex",
        "frogmonster",
        "toontown",
        "seaofthieves",
        "tloz",
        "lingo",
        "shorthike",
        "albw",
        "dontstarvetogether",
        "oot",
        "ss",
        "sm64hacks",
        "xenobladex",
        "minecraft",
        "subnautica",
        "metroidprime",
        "mm_recomp",
        "terraria",
        "smo",
        "gstla",
        "jakanddaxter",
        "witness",
        "osrs",
        "satisfactory",
        "smz3",
        "outer_wilds"
    ],
    "world": [
        "pokemon_rb",
        "pokemon_crystal",
        "simpsonshitnrun",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "frogmonster",
        "dark_souls_2",
        "sm64ex",
        "toontown",
        "seaofthieves",
        "tloz",
        "dkc3",
        "aquaria",
        "lingo",
        "shorthike",
        "albw",
        "dontstarvetogether",
        "oot",
        "ss",
        "sm64hacks",
        "xenobladex",
        "minecraft",
        "dkc2",
        "subnautica",
        "metroidprime",
        "tmc",
        "mm_recomp",
        "dw1",
        "v6",
        "terraria",
        "smo",
        "tloz_oos",
        "yoshisisland",
        "ladx",
        "gstla",
        "jakanddaxter",
        "witness",
        "osrs",
        "tloz_ph",
        "satisfactory",
        "smz3",
        "smw",
        "yugioh06",
        "earthbound",
        "outer_wilds",
        "dkc"
    ],
    "nintendo 3ds": [
        "mm2",
        "pokemon_rb",
        "tloz",
        "mm3",
        "ladx",
        "wl4",
        "pokemon_crystal",
        "wl",
        "tmc",
        "metroidfusion",
        "zelda2",
        "tloz_ooa",
        "v6",
        "albw",
        "ff1",
        "tloz_oos",
        "terraria",
        "marioland2"
    ],
    "3ds": [
        "pokemon_rb",
        "mm3",
        "pokemon_crystal",
        "alttp",
        "zelda2",
        "ff1",
        "sm",
        "tloz",
        "dkc3",
        "mmx3",
        "metroidfusion",
        "albw",
        "mm2",
        "dkc2",
        "wl",
        "tmc",
        "v6",
        "terraria",
        "marioland2",
        "tloz_oos",
        "wl4",
        "ladx",
        "sm_map_rando",
        "smw",
        "earthbound",
        "tloz_ooa",
        "dkc"
    ],
    "medieval": [
        "dark_souls_3",
        "quake",
        "ss",
        "heretic",
        "albw",
        "soe",
        "rogue_legacy",
        "candybox2",
        "dark_souls_2"
    ],
    "magic": [
        "zork_grand_inquisitor",
        "heretic",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "dark_souls_2",
        "dsr",
        "poe",
        "aquaria",
        "ffta",
        "ctjot",
        "albw",
        "cuphead",
        "tmc",
        "cvcotm",
        "noita",
        "rogue_legacy",
        "terraria",
        "tloz_oos",
        "ladx",
        "faxanadu",
        "gstla",
        "candybox2"
    ],
    "minigames": [
        "spyro3",
        "pokemon_crystal",
        "apeescape",
        "toontown",
        "dkc3",
        "albw",
        "oot",
        "k64",
        "stardew_valley",
        "rogue_legacy",
        "pokemon_emerald",
        "dk64",
        "kh1",
        "wl4",
        "aus",
        "gstla",
        "hcniko",
        "tloz_ph",
        "tloz_ooa"
    ],
    "2.5d": [
        "dkc3",
        "heretic",
        "doom_ii",
        "doom_1993",
        "albw",
        "k64",
        "dkc"
    ],
    "archery": [
        "minecraft",
        "ss",
        "mm_recomp",
        "alttp",
        "tww",
        "albw",
        "oot"
    ],
    "fairy": [
        "tloz",
        "ladx",
        "stardew_valley",
        "tloz_ph",
        "tloz_oos",
        "tmc",
        "landstalker",
        "alttp",
        "mm_recomp",
        "zelda2",
        "tloz_ooa",
        "terraria",
        "tww",
        "albw",
        "oot",
        "k64",
        "dk64",
        "huniepop2"
    ],
    "princess": [
        "ss",
        "ladx",
        "tp",
        "tmc",
        "tloz_ph",
        "albw",
        "alttp",
        "papermario",
        "smw",
        "tloz_ooa",
        "lego_star_wars_tcs",
        "mk64",
        "oot",
        "tloz_oos",
        "kh1",
        "mlss"
    ],
    "sequel": [
        "dark_souls_3",
        "mm3",
        "doom_ii",
        "alttp",
        "zelda2",
        "dark_souls_2",
        "mmx3",
        "ffta",
        "hylics2",
        "albw",
        "mk64",
        "dontstarvetogether",
        "oot",
        "mm2",
        "dkc2",
        "sms",
        "mm_recomp",
        "dw1",
        "banjo_tooie",
        "smo",
        "wl4",
        "gstla",
        "civ_6"
    ],
    "sword & sorcery": [
        "dark_souls_3",
        "spyro3",
        "ss",
        "ladx",
        "heretic",
        "tmc",
        "tloz_oos",
        "mm_recomp",
        "tloz_ooa",
        "terraria",
        "tww",
        "albw",
        "dark_souls_2",
        "ffmq",
        "oot",
        "kh1"
    ],
    "sword": [
        "dark_souls_3",
        "spyro3",
        "ss",
        "ladx",
        "heretic",
        "tmc",
        "tloz_oos",
        "mm_recomp",
        "tloz_ooa",
        "terraria",
        "tww",
        "albw",
        "dark_souls_2",
        "ffmq",
        "oot",
        "kh1"
    ],
    "&": [
        "dark_souls_3",
        "spyro3",
        "heretic",
        "balatro",
        "simpsonshitnrun",
        "dark_souls_2",
        "ffmq",
        "yugiohddm",
        "spire",
        "fm",
        "inscryption",
        "albw",
        "ss",
        "oot",
        "tmc",
        "mm_recomp",
        "terraria",
        "tloz_oos",
        "kh1",
        "ladx",
        "yugioh06",
        "rac2",
        "tloz_ooa",
        "tww",
        "mlss"
    ],
    "sorcery": [
        "dark_souls_3",
        "spyro3",
        "ss",
        "ladx",
        "heretic",
        "tmc",
        "tloz_oos",
        "mm_recomp",
        "tloz_ooa",
        "terraria",
        "tww",
        "albw",
        "dark_souls_2",
        "ffmq",
        "oot",
        "kh1"
    ],
    "darkness": [
        "mm3",
        "doom_ii",
        "alttp",
        "zelda2",
        "sm",
        "dkc3",
        "aquaria",
        "metroidfusion",
        "albw",
        "minecraft",
        "dkc2",
        "tmc",
        "rogue_legacy",
        "terraria",
        "ladx",
        "witness",
        "sm_map_rando",
        "earthbound",
        "luigismansion",
        "dkc"
    ],
    "digital distribution": [
        "timespinner",
        "heretic",
        "doom_ii",
        "getting_over_it",
        "sotn",
        "apeescape",
        "sm64ex",
        "quake",
        "seaofthieves",
        "celeste",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "dkc",
        "mlss",
        "oot",
        "sm64hacks",
        "oribf",
        "minecraft",
        "dkc2",
        "tmc",
        "factorio",
        "crosscode",
        "rogue_legacy",
        "banjo_tooie",
        "terraria",
        "tloz_oos",
        "dk64",
        "v6",
        "yoshisisland",
        "wl4",
        "ladx",
        "civ_6",
        "witness",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "smw",
        "ufo50",
        "tunic",
        "huniepop2"
    ],
    "digital": [
        "timespinner",
        "heretic",
        "doom_ii",
        "getting_over_it",
        "sotn",
        "apeescape",
        "sm64ex",
        "quake",
        "seaofthieves",
        "celeste",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "dkc",
        "mlss",
        "oot",
        "sm64hacks",
        "oribf",
        "minecraft",
        "dkc2",
        "tmc",
        "factorio",
        "crosscode",
        "rogue_legacy",
        "banjo_tooie",
        "terraria",
        "tloz_oos",
        "dk64",
        "v6",
        "yoshisisland",
        "wl4",
        "ladx",
        "civ_6",
        "witness",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "smw",
        "ufo50",
        "tunic",
        "huniepop2"
    ],
    "distribution": [
        "timespinner",
        "heretic",
        "doom_ii",
        "getting_over_it",
        "sotn",
        "apeescape",
        "sm64ex",
        "quake",
        "seaofthieves",
        "celeste",
        "albw",
        "cuphead",
        "dontstarvetogether",
        "dkc",
        "mlss",
        "oot",
        "sm64hacks",
        "oribf",
        "minecraft",
        "dkc2",
        "tmc",
        "factorio",
        "crosscode",
        "rogue_legacy",
        "banjo_tooie",
        "terraria",
        "tloz_oos",
        "dk64",
        "v6",
        "yoshisisland",
        "wl4",
        "ladx",
        "civ_6",
        "witness",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "smw",
        "ufo50",
        "tunic",
        "huniepop2"
    ],
    "anthropomorphism": [
        "spyro3",
        "cv64",
        "apeescape",
        "dkc3",
        "shorthike",
        "albw",
        "mk64",
        "cuphead",
        "k64",
        "dkc",
        "diddy_kong_racing",
        "dkc2",
        "sly1",
        "sms",
        "star_fox_64",
        "tmc",
        "papermario",
        "banjo_tooie",
        "tloz_oos",
        "dk64",
        "kh1",
        "sonic_heroes",
        "hcniko",
        "jakanddaxter",
        "undertale",
        "tloz_ooa",
        "tunic",
        "mlss"
    ],
    "polygonal 3d": [
        "spyro3",
        "cv64",
        "simpsonshitnrun",
        "sotn",
        "apeescape",
        "quake",
        "albw",
        "mk64",
        "oot",
        "k64",
        "lego_star_wars_tcs",
        "ss",
        "xenobladex",
        "minecraft",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "sms",
        "dw1",
        "dk64",
        "kh1",
        "jakanddaxter",
        "witness",
        "tloz_ph",
        "luigismansion"
    ],
    "polygonal": [
        "spyro3",
        "cv64",
        "simpsonshitnrun",
        "sotn",
        "apeescape",
        "quake",
        "albw",
        "mk64",
        "oot",
        "k64",
        "lego_star_wars_tcs",
        "ss",
        "xenobladex",
        "minecraft",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "sms",
        "dw1",
        "dk64",
        "kh1",
        "jakanddaxter",
        "witness",
        "tloz_ph",
        "luigismansion"
    ],
    "bow and arrow": [
        "minecraft",
        "ss",
        "ladx",
        "poe",
        "tmc",
        "tloz_ph",
        "tloz_oos",
        "ror1",
        "alttp",
        "ffta",
        "rogue_legacy",
        "albw",
        "cuphead",
        "dark_souls_2",
        "terraria",
        "oot"
    ],
    "bow": [
        "minecraft",
        "ss",
        "ladx",
        "poe",
        "tmc",
        "tloz_ph",
        "tloz_oos",
        "ror1",
        "alttp",
        "ffta",
        "rogue_legacy",
        "albw",
        "cuphead",
        "dark_souls_2",
        "terraria",
        "oot"
    ],
    "and": [
        "openrct2",
        "cv64",
        "alttp",
        "blasphemous",
        "dark_souls_2",
        "poe",
        "ror1",
        "ffta",
        "albw",
        "cuphead",
        "oot",
        "ss",
        "oribf",
        "minecraft",
        "sly1",
        "tmc",
        "hades",
        "rogue_legacy",
        "terraria",
        "tloz_oos",
        "ladx",
        "civ_6",
        "jakanddaxter",
        "tloz_ph",
        "smz3"
    ],
    "arrow": [
        "minecraft",
        "ss",
        "ladx",
        "poe",
        "tmc",
        "tloz_ph",
        "tloz_oos",
        "ror1",
        "alttp",
        "ffta",
        "rogue_legacy",
        "albw",
        "cuphead",
        "dark_souls_2",
        "terraria",
        "oot"
    ],
    "damsel in distress": [
        "ss",
        "metroidprime",
        "sms",
        "sm_map_rando",
        "tloz_ph",
        "tmc",
        "alttp",
        "papermario",
        "smw",
        "earthbound",
        "tloz_ooa",
        "zelda2",
        "albw",
        "oot",
        "tloz_oos",
        "kh1",
        "sm"
    ],
    "damsel": [
        "ss",
        "metroidprime",
        "sms",
        "sm_map_rando",
        "tloz_ph",
        "tmc",
        "alttp",
        "papermario",
        "smw",
        "earthbound",
        "tloz_ooa",
        "zelda2",
        "albw",
        "oot",
        "tloz_oos",
        "kh1",
        "sm"
    ],
    "distress": [
        "ss",
        "metroidprime",
        "sms",
        "sm_map_rando",
        "tloz_ph",
        "tmc",
        "alttp",
        "papermario",
        "smw",
        "earthbound",
        "tloz_ooa",
        "zelda2",
        "albw",
        "oot",
        "tloz_oos",
        "kh1",
        "sm"
    ],
    "upgradeable weapons": [
        "mm2",
        "mzm",
        "metroidprime",
        "cv64",
        "tmc",
        "mmx3",
        "metroidfusion",
        "albw",
        "dark_souls_2",
        "dk64"
    ],
    "upgradeable": [
        "mm2",
        "mzm",
        "metroidprime",
        "cv64",
        "tmc",
        "mmx3",
        "metroidfusion",
        "albw",
        "dark_souls_2",
        "dk64"
    ],
    "weapons": [
        "mm2",
        "mzm",
        "metroidprime",
        "cv64",
        "tmc",
        "mmx3",
        "metroidfusion",
        "albw",
        "dark_souls_2",
        "dk64"
    ],
    "disorientation zone": [
        "ladx",
        "tmc",
        "alttp",
        "tloz_ooa",
        "albw",
        "oot",
        "tloz_oos"
    ],
    "disorientation": [
        "ladx",
        "tmc",
        "alttp",
        "tloz_ooa",
        "albw",
        "oot",
        "tloz_oos"
    ],
    "zone": [
        "ladx",
        "tmc",
        "alttp",
        "tloz_ooa",
        "albw",
        "oot",
        "tloz_oos"
    ],
    "descendants of other characters": [
        "dkc2",
        "dkc3",
        "sly1",
        "jakanddaxter",
        "sms",
        "cv64",
        "star_fox_64",
        "tmc",
        "mm_recomp",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "tloz_ooa",
        "albw",
        "luigismansion",
        "oot",
        "dk64",
        "dkc"
    ],
    "descendants": [
        "dkc2",
        "dkc3",
        "sly1",
        "jakanddaxter",
        "sms",
        "cv64",
        "star_fox_64",
        "tmc",
        "mm_recomp",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "tloz_ooa",
        "albw",
        "luigismansion",
        "oot",
        "dk64",
        "dkc"
    ],
    "other": [
        "dkc2",
        "dkc3",
        "sly1",
        "jakanddaxter",
        "sms",
        "cv64",
        "star_fox_64",
        "tmc",
        "mm_recomp",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "tloz_ooa",
        "albw",
        "luigismansion",
        "oot",
        "dk64",
        "dkc"
    ],
    "characters": [
        "dark_souls_3",
        "cv64",
        "sotn",
        "dark_souls_2",
        "dkc3",
        "albw",
        "lego_star_wars_tcs",
        "oot",
        "xenobladex",
        "stardew_valley",
        "dkc2",
        "star_fox_64",
        "sly1",
        "sms",
        "tmc",
        "mm_recomp",
        "rogue_legacy",
        "terraria",
        "dk64",
        "jakanddaxter",
        "earthbound",
        "tloz_ooa",
        "luigismansion",
        "dkc"
    ],
    "save point": [
        "cv64",
        "sotn",
        "mzm",
        "sm",
        "dkc3",
        "aquaria",
        "metroidfusion",
        "albw",
        "dkc",
        "dkc2",
        "metroidprime",
        "cvcotm",
        "papermario",
        "v6",
        "kh1",
        "faxanadu",
        "gstla",
        "jakanddaxter",
        "sm_map_rando",
        "earthbound",
        "luigismansion",
        "mlss"
    ],
    "save": [
        "cv64",
        "sotn",
        "mzm",
        "sm",
        "dkc3",
        "aquaria",
        "metroidfusion",
        "albw",
        "dkc",
        "dkc2",
        "metroidprime",
        "cvcotm",
        "papermario",
        "v6",
        "kh1",
        "faxanadu",
        "gstla",
        "jakanddaxter",
        "sm_map_rando",
        "earthbound",
        "luigismansion",
        "mlss"
    ],
    "point": [
        "cv64",
        "sotn",
        "mzm",
        "sm",
        "dkc3",
        "aquaria",
        "metroidfusion",
        "albw",
        "dkc",
        "dkc2",
        "metroidprime",
        "cvcotm",
        "papermario",
        "v6",
        "kh1",
        "faxanadu",
        "gstla",
        "jakanddaxter",
        "sm_map_rando",
        "earthbound",
        "luigismansion",
        "mlss"
    ],
    "side quests": [
        "ladx",
        "dark_souls_2",
        "pokemon_crystal",
        "pokemon_emerald",
        "tmc",
        "tloz_ph",
        "tloz_oos",
        "alttp",
        "tloz_ooa",
        "albw",
        "xenobladex",
        "oot",
        "sc2"
    ],
    "side": [
        "hk",
        "pokemon_rb",
        "mm3",
        "timespinner",
        "pokemon_crystal",
        "getting_over_it",
        "kdl3",
        "wargroove",
        "alttp",
        "sotn",
        "enderlilies",
        "pokemon_frlg",
        "megamix",
        "zelda2",
        "blasphemous",
        "ff4fe",
        "ff1",
        "dark_souls_2",
        "ffmq",
        "mzm",
        "sm",
        "celeste",
        "lufia2ac",
        "dkc3",
        "messenger",
        "spire",
        "aquaria",
        "ror1",
        "mmx3",
        "metroidfusion",
        "hylics2",
        "albw",
        "cuphead",
        "mlss",
        "k64",
        "oot",
        "xenobladex",
        "oribf",
        "zillion",
        "mm2",
        "dkc2",
        "wl",
        "tmc",
        "cvcotm",
        "noita",
        "papermario",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "pokemon_emerald",
        "v6",
        "terraria",
        "marioland2",
        "tetrisattack",
        "tloz_oos",
        "yoshisisland",
        "wl4",
        "aus",
        "monster_sanctuary",
        "wargroove2",
        "ladx",
        "faxanadu",
        "sm_map_rando",
        "tloz_ph",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "smw",
        "smz3",
        "tloz_ooa",
        "ufo50",
        "sc2",
        "animal_well",
        "dkc"
    ],
    "quests": [
        "ladx",
        "pokemon_crystal",
        "metroidprime",
        "pokemon_emerald",
        "tmc",
        "tloz_ph",
        "tloz_oos",
        "alttp",
        "zelda2",
        "tloz_ooa",
        "albw",
        "xenobladex",
        "dark_souls_2",
        "sc2",
        "oot"
    ],
    "potion": [
        "minecraft",
        "ladx",
        "gstla",
        "pokemon_crystal",
        "poe",
        "pokemon_emerald",
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "rogue_legacy",
        "albw",
        "ss",
        "tloz_oos",
        "kh1"
    ],
    "real-time combat": [
        "spyro3",
        "doom_ii",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "sm64ex",
        "dark_souls_2",
        "sm",
        "quake",
        "albw",
        "xenobladex",
        "oot",
        "ss",
        "sm64hacks",
        "minecraft",
        "metroidprime",
        "sms",
        "tmc",
        "landstalker",
        "tloz_oos",
        "dk64",
        "kh1",
        "ladx",
        "sm_map_rando",
        "tloz_ph",
        "doom_1993",
        "tloz_ooa",
        "dkc"
    ],
    "real-time": [
        "spyro3",
        "doom_ii",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "sm64ex",
        "dark_souls_2",
        "sm",
        "quake",
        "albw",
        "xenobladex",
        "oot",
        "ss",
        "sm64hacks",
        "minecraft",
        "metroidprime",
        "sms",
        "tmc",
        "landstalker",
        "tloz_oos",
        "dk64",
        "kh1",
        "ladx",
        "sm_map_rando",
        "tloz_ph",
        "doom_1993",
        "tloz_ooa",
        "dkc"
    ],
    "combat": [
        "spyro3",
        "doom_ii",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "sm64ex",
        "dark_souls_2",
        "sm",
        "quake",
        "albw",
        "xenobladex",
        "oot",
        "ss",
        "sm64hacks",
        "minecraft",
        "metroidprime",
        "sms",
        "tmc",
        "landstalker",
        "tloz_oos",
        "dk64",
        "kh1",
        "ladx",
        "sm_map_rando",
        "tloz_ph",
        "doom_1993",
        "tloz_ooa",
        "dkc"
    ],
    "self-referential humor": [
        "dkc2",
        "papermario",
        "metroidfusion",
        "earthbound",
        "albw",
        "mlss"
    ],
    "self-referential": [
        "dkc2",
        "papermario",
        "metroidfusion",
        "earthbound",
        "albw",
        "mlss"
    ],
    "humor": [
        "dkc2",
        "papermario",
        "metroidfusion",
        "earthbound",
        "albw",
        "mlss"
    ],
    "rpg elements": [
        "minecraft",
        "mzm",
        "dark_souls_2",
        "albw",
        "metroidfusion",
        "sotn",
        "zelda2",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "oribf",
        "mlss"
    ],
    "rpg": [
        "minecraft",
        "mzm",
        "dark_souls_2",
        "albw",
        "metroidfusion",
        "sotn",
        "zelda2",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "oribf",
        "mlss"
    ],
    "elements": [
        "minecraft",
        "mzm",
        "dark_souls_2",
        "albw",
        "metroidfusion",
        "sotn",
        "zelda2",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "oribf",
        "mlss"
    ],
    "mercenary": [
        "quake",
        "ss",
        "dark_souls_2",
        "metroidprime",
        "sm_map_rando",
        "alttp",
        "albw",
        "oot",
        "sc2",
        "sm"
    ],
    "coming of age": [
        "pokemon_crystal",
        "jakanddaxter",
        "pokemon_emerald",
        "tmc",
        "alttp",
        "ffta",
        "albw",
        "oot",
        "oribf"
    ],
    "coming": [
        "pokemon_crystal",
        "jakanddaxter",
        "pokemon_emerald",
        "tmc",
        "alttp",
        "ffta",
        "albw",
        "oot",
        "oribf"
    ],
    "age": [
        "gstla",
        "pokemon_crystal",
        "jakanddaxter",
        "pokemon_emerald",
        "tmc",
        "alttp",
        "ffta",
        "albw",
        "oot",
        "factorio_saws",
        "oribf"
    ],
    "androgyny": [
        "ss",
        "gstla",
        "ffta",
        "sotn",
        "albw",
        "oot"
    ],
    "fast traveling": [
        "hk",
        "pokemon_emerald",
        "poe",
        "tmc",
        "tloz_ph",
        "undertale",
        "alttp",
        "albw",
        "oot"
    ],
    "fast": [
        "hk",
        "pokemon_emerald",
        "poe",
        "tmc",
        "tloz_ph",
        "undertale",
        "alttp",
        "albw",
        "oot"
    ],
    "traveling": [
        "hk",
        "pokemon_emerald",
        "poe",
        "tmc",
        "tloz_ph",
        "undertale",
        "alttp",
        "albw",
        "oot"
    ],
    "context sensitive": [
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "albw",
        "ss",
        "tloz_oos",
        "oot"
    ],
    "context": [
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "albw",
        "ss",
        "tloz_oos",
        "oot"
    ],
    "sensitive": [
        "tloz_ph",
        "alttp",
        "tloz_ooa",
        "albw",
        "ss",
        "tloz_oos",
        "oot"
    ],
    "living inventory": [
        "tmc",
        "mm_recomp",
        "alttp",
        "tww",
        "albw",
        "ss",
        "oot"
    ],
    "living": [
        "tmc",
        "mm_recomp",
        "alttp",
        "tww",
        "albw",
        "ss",
        "oot"
    ],
    "inventory": [
        "tmc",
        "mm_recomp",
        "alttp",
        "tww",
        "albw",
        "ss",
        "oot"
    ],
    "bees": [
        "minecraft",
        "tloz_ph",
        "alttp",
        "raft",
        "albw",
        "dontstarvetogether",
        "terraria"
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
        "dkc2",
        "dkc3",
        "lufia2ac",
        "kdl3",
        "sm_map_rando",
        "mmx3",
        "smz3",
        "alttp",
        "smw",
        "soe",
        "earthbound",
        "sm",
        "ff4fe",
        "ffmq",
        "tetrisattack",
        "yoshisisland",
        "dkc"
    ],
    "super": [
        "kdl3",
        "alttp",
        "sm64ex",
        "ff4fe",
        "ffmq",
        "sm",
        "lufia2ac",
        "dkc3",
        "mmx3",
        "sm64hacks",
        "dkc2",
        "sms",
        "wl",
        "soe",
        "smo",
        "marioland2",
        "tetrisattack",
        "yoshisisland",
        "sm_map_rando",
        "smz3",
        "smw",
        "earthbound",
        "dkc"
    ],
    "entertainment": [
        "mm3",
        "kdl3",
        "alttp",
        "zelda2",
        "ff4fe",
        "ff1",
        "ffmq",
        "sm",
        "tloz",
        "lufia2ac",
        "dkc3",
        "mmx3",
        "dkc2",
        "soe",
        "tetrisattack",
        "yoshisisland",
        "faxanadu",
        "sm_map_rando",
        "smz3",
        "smw",
        "earthbound",
        "dkc"
    ],
    "wii": [
        "hk",
        "mm3",
        "kdl3",
        "alttp",
        "zelda2",
        "mzm",
        "ff4fe",
        "ff1",
        "ffmq",
        "pmd_eos",
        "sm64ex",
        "sm",
        "tloz",
        "tp",
        "dkc3",
        "mmx3",
        "ffta",
        "metroidfusion",
        "lego_star_wars_tcs",
        "mk64",
        "mlss",
        "k64",
        "oot",
        "sm64hacks",
        "ss",
        "stardew_valley",
        "xenobladex",
        "dkc2",
        "star_fox_64",
        "tmc",
        "cvcotm",
        "landstalker",
        "mm_recomp",
        "papermario",
        "terraria",
        "dk64",
        "wl4",
        "faxanadu",
        "gstla",
        "sm_map_rando",
        "tloz_ph",
        "smw",
        "earthbound",
        "dkc"
    ],
    "wii u": [
        "hk",
        "mm3",
        "kdl3",
        "alttp",
        "zelda2",
        "mzm",
        "ff1",
        "pmd_eos",
        "ffmq",
        "sm64ex",
        "sm",
        "tloz",
        "dkc3",
        "mmx3",
        "ffta",
        "metroidfusion",
        "dkc",
        "mk64",
        "oot",
        "k64",
        "sm64hacks",
        "ss",
        "stardew_valley",
        "xenobladex",
        "dkc2",
        "star_fox_64",
        "tmc",
        "cvcotm",
        "mm_recomp",
        "papermario",
        "terraria",
        "dk64",
        "wl4",
        "gstla",
        "sm_map_rando",
        "tloz_ph",
        "smw",
        "earthbound",
        "mlss"
    ],
    "u": [
        "hk",
        "mm3",
        "kdl3",
        "alttp",
        "zelda2",
        "mzm",
        "ff1",
        "pmd_eos",
        "ffmq",
        "sm64ex",
        "sm",
        "tloz",
        "dkc3",
        "mmx3",
        "ffta",
        "metroidfusion",
        "dkc",
        "mk64",
        "oot",
        "k64",
        "sm64hacks",
        "ss",
        "stardew_valley",
        "xenobladex",
        "dkc2",
        "star_fox_64",
        "tmc",
        "cvcotm",
        "mm_recomp",
        "papermario",
        "terraria",
        "dk64",
        "wl4",
        "gstla",
        "sm_map_rando",
        "tloz_ph",
        "smw",
        "earthbound",
        "mlss"
    ],
    "new nintendo 3ds": [
        "dkc2",
        "dkc3",
        "sm_map_rando",
        "mmx3",
        "alttp",
        "smw",
        "earthbound",
        "sm",
        "dkc"
    ],
    "new": [
        "dkc2",
        "dkc3",
        "sm_map_rando",
        "mmx3",
        "alttp",
        "smw",
        "earthbound",
        "sm",
        "dkc"
    ],
    "super famicom": [
        "dkc2",
        "dkc3",
        "lufia2ac",
        "kdl3",
        "sm_map_rando",
        "mmx3",
        "alttp",
        "smw",
        "earthbound",
        "sm",
        "ffmq",
        "yoshisisland",
        "dkc"
    ],
    "famicom": [
        "dkc2",
        "dkc3",
        "lufia2ac",
        "kdl3",
        "sm_map_rando",
        "mmx3",
        "alttp",
        "smw",
        "earthbound",
        "sm",
        "ffmq",
        "yoshisisland",
        "dkc"
    ],
    "ghosts": [
        "cv64",
        "simpsonshitnrun",
        "alttp",
        "sotn",
        "ffmq",
        "lego_star_wars_tcs",
        "cuphead",
        "dkc2",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "papermario",
        "rogue_legacy",
        "v6",
        "wl4",
        "aus",
        "earthbound",
        "tloz_ooa",
        "luigismansion",
        "mlss"
    ],
    "mascot": [
        "mm2",
        "spyro3",
        "mm3",
        "ladx",
        "sly1",
        "jakanddaxter",
        "kdl3",
        "tmc",
        "tloz_ph",
        "alttp",
        "papermario",
        "tloz_oos",
        "k64"
    ],
    "death": [
        "dark_souls_3",
        "mm3",
        "heretic",
        "doom_ii",
        "openrct2",
        "cv64",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "dark_souls_2",
        "quake",
        "mmx3",
        "ffta",
        "metroidfusion",
        "oot",
        "mm2",
        "minecraft",
        "star_fox_64",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "cvcotm",
        "papermario",
        "rogue_legacy",
        "v6",
        "terraria",
        "tloz_oos",
        "dk64",
        "kh1",
        "ladx",
        "gstla",
        "tloz_ph",
        "tloz_ooa",
        "luigismansion",
        "dkc"
    ],
    "maze": [
        "ladx",
        "openrct2",
        "cv64",
        "tmc",
        "witness",
        "doom_1993",
        "alttp",
        "papermario",
        "mzm"
    ],
    "backtracking": [
        "cv64",
        "alttp",
        "sotn",
        "mzm",
        "quake",
        "ffta",
        "metroidfusion",
        "oot",
        "metroidprime",
        "tmc",
        "cvcotm",
        "banjo_tooie",
        "tloz_oos",
        "kh1",
        "ladx",
        "faxanadu",
        "jakanddaxter",
        "witness",
        "tloz_ph",
        "undertale"
    ],
    "undead": [
        "ladx",
        "dsr",
        "heretic",
        "cv64",
        "tmc",
        "tloz_oos",
        "alttp",
        "papermario",
        "sotn",
        "tloz_ooa",
        "terraria",
        "dark_souls_2",
        "ffmq",
        "oot",
        "mlss"
    ],
    "campaign": [
        "ladx",
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "tloz_ooa",
        "ss",
        "tloz_oos",
        "oot"
    ],
    "pixel art": [
        "mm3",
        "timespinner",
        "wargroove",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "blasphemous",
        "sm",
        "celeste",
        "ror1",
        "metroidfusion",
        "stardew_valley",
        "mm2",
        "tyrian",
        "tmc",
        "crosscode",
        "rogue_legacy",
        "v6",
        "terraria",
        "tloz_oos",
        "wl4",
        "ladx",
        "hcniko",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "animal_well"
    ],
    "pixel": [
        "mm3",
        "timespinner",
        "wargroove",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "blasphemous",
        "sm",
        "celeste",
        "ror1",
        "metroidfusion",
        "stardew_valley",
        "mm2",
        "tyrian",
        "tmc",
        "crosscode",
        "rogue_legacy",
        "v6",
        "terraria",
        "tloz_oos",
        "wl4",
        "ladx",
        "hcniko",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "animal_well"
    ],
    "art": [
        "mm3",
        "timespinner",
        "wargroove",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "blasphemous",
        "sm",
        "celeste",
        "ror1",
        "metroidfusion",
        "stardew_valley",
        "mm2",
        "tyrian",
        "tmc",
        "crosscode",
        "rogue_legacy",
        "v6",
        "terraria",
        "tloz_oos",
        "wl4",
        "ladx",
        "hcniko",
        "sm_map_rando",
        "celeste_open_world",
        "undertale",
        "animal_well"
    ],
    "easter egg": [
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "metroidfusion",
        "apeescape",
        "papermario",
        "rogue_legacy",
        "banjo_tooie"
    ],
    "easter": [
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "metroidfusion",
        "apeescape",
        "papermario",
        "rogue_legacy",
        "banjo_tooie"
    ],
    "egg": [
        "ladx",
        "doom_ii",
        "openrct2",
        "alttp",
        "metroidfusion",
        "apeescape",
        "papermario",
        "rogue_legacy",
        "banjo_tooie"
    ],
    "teleportation": [
        "pokemon_crystal",
        "jakanddaxter",
        "doom_ii",
        "cv64",
        "tmc",
        "alttp",
        "earthbound",
        "rogue_legacy",
        "v6",
        "pokemon_emerald",
        "tloz_oos",
        "terraria"
    ],
    "giant insects": [
        "hk",
        "dkc2",
        "dkc3",
        "pokemon_emerald",
        "sms",
        "alttp",
        "soe",
        "mlss",
        "dk64",
        "dkc"
    ],
    "giant": [
        "hk",
        "dkc2",
        "dkc3",
        "pokemon_emerald",
        "sms",
        "alttp",
        "soe",
        "mlss",
        "dk64",
        "dkc"
    ],
    "insects": [
        "hk",
        "dkc2",
        "dkc3",
        "pokemon_emerald",
        "sms",
        "alttp",
        "soe",
        "mlss",
        "dk64",
        "dkc"
    ],
    "silent protagonist": [
        "hk",
        "alttp",
        "zelda2",
        "blasphemous",
        "quake",
        "dkc",
        "ss",
        "k64",
        "oot",
        "dkc2",
        "tmc",
        "ultrakill",
        "papermario",
        "pokemon_emerald",
        "tloz_oos",
        "ladx",
        "gstla",
        "jakanddaxter",
        "tloz_ph",
        "doom_1993",
        "tloz_ooa",
        "mlss"
    ],
    "silent": [
        "hk",
        "alttp",
        "zelda2",
        "blasphemous",
        "quake",
        "dkc",
        "ss",
        "k64",
        "oot",
        "dkc2",
        "tmc",
        "ultrakill",
        "papermario",
        "pokemon_emerald",
        "tloz_oos",
        "ladx",
        "gstla",
        "jakanddaxter",
        "tloz_ph",
        "doom_1993",
        "tloz_ooa",
        "mlss"
    ],
    "explosion": [
        "mm3",
        "doom_ii",
        "openrct2",
        "cv64",
        "simpsonshitnrun",
        "alttp",
        "sotn",
        "zelda2",
        "mzm",
        "ffmq",
        "sm",
        "quake",
        "dkc3",
        "mmx3",
        "ffta",
        "metroidfusion",
        "lego_star_wars_tcs",
        "mk64",
        "cuphead",
        "mm2",
        "minecraft",
        "dkc2",
        "metroidprime",
        "sms",
        "tmc",
        "rogue_legacy",
        "terraria",
        "sonic_heroes",
        "sm_map_rando",
        "tloz_ooa"
    ],
    "monkey": [
        "diddy_kong_racing",
        "dkc2",
        "dkc3",
        "ladx",
        "alttp",
        "apeescape",
        "mk64",
        "dk64",
        "dkc"
    ],
    "nintendo power": [
        "dkc2",
        "dkc3",
        "sm_map_rando",
        "alttp",
        "earthbound",
        "sm",
        "dkc"
    ],
    "power": [
        "dkc2",
        "dkc3",
        "sm_map_rando",
        "alttp",
        "earthbound",
        "sm",
        "dkc"
    ],
    "world map": [
        "dkc2",
        "dkc3",
        "ladx",
        "jakanddaxter",
        "metroidprime",
        "aquaria",
        "pokemon_crystal",
        "tloz_ph",
        "tmc",
        "alttp",
        "v6",
        "oot",
        "tloz_oos",
        "dkc"
    ],
    "map": [
        "dkc2",
        "dkc3",
        "ladx",
        "jakanddaxter",
        "metroidprime",
        "aquaria",
        "pokemon_crystal",
        "tloz_ph",
        "tmc",
        "alttp",
        "v6",
        "oot",
        "tloz_oos",
        "dkc"
    ],
    "human": [
        "dark_souls_3",
        "doom_ii",
        "cv64",
        "simpsonshitnrun",
        "alttp",
        "sotn",
        "apeescape",
        "zelda2",
        "dark_souls_2",
        "quake",
        "metroidfusion",
        "ss",
        "sms",
        "papermario",
        "terraria",
        "ladx",
        "gstla",
        "tloz_ph",
        "sc2"
    ],
    "shopping": [
        "yugiohddm",
        "pokemon_crystal",
        "pokemon_emerald",
        "cv64",
        "tmc",
        "tloz_ph",
        "alttp",
        "sotn",
        "tloz_ooa",
        "dw1",
        "lego_star_wars_tcs",
        "cuphead",
        "tloz_oos",
        "mlss"
    ],
    "ice stage": [
        "wl4",
        "dkc2",
        "dkc3",
        "jakanddaxter",
        "metroidprime",
        "cv64",
        "tmc",
        "alttp",
        "metroidfusion",
        "mk64",
        "banjo_tooie",
        "terraria",
        "oot",
        "dkc"
    ],
    "ice": [
        "wl4",
        "dkc2",
        "dkc3",
        "jakanddaxter",
        "metroidprime",
        "cv64",
        "tmc",
        "alttp",
        "metroidfusion",
        "mk64",
        "banjo_tooie",
        "terraria",
        "oot",
        "dkc"
    ],
    "stage": [
        "wl4",
        "sonic_heroes",
        "spyro3",
        "dkc2",
        "dkc3",
        "jakanddaxter",
        "metroidprime",
        "cv64",
        "tmc",
        "alttp",
        "metroidfusion",
        "smw",
        "mk64",
        "banjo_tooie",
        "terraria",
        "oot",
        "dkc"
    ],
    "saving the world": [
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "earthbound",
        "dark_souls_2"
    ],
    "saving": [
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "earthbound",
        "dark_souls_2"
    ],
    "grapple": [
        "metroidprime",
        "tmc",
        "tloz_ph",
        "alttp",
        "lego_star_wars_tcs",
        "oot"
    ],
    "secret area": [
        "heretic",
        "doom_ii",
        "alttp",
        "sotn",
        "zelda2",
        "sm",
        "dkc3",
        "metroidfusion",
        "dkc2",
        "diddy_kong_racing",
        "star_fox_64",
        "tmc",
        "rogue_legacy",
        "tloz_oos",
        "hcniko",
        "witness",
        "sm_map_rando",
        "tunic",
        "dkc"
    ],
    "secret": [
        "heretic",
        "doom_ii",
        "alttp",
        "sotn",
        "zelda2",
        "sm",
        "dkc3",
        "metroidfusion",
        "dkc2",
        "diddy_kong_racing",
        "star_fox_64",
        "tmc",
        "soe",
        "rogue_legacy",
        "tloz_oos",
        "hcniko",
        "witness",
        "sm_map_rando",
        "tunic",
        "dkc"
    ],
    "area": [
        "heretic",
        "doom_ii",
        "alttp",
        "sotn",
        "zelda2",
        "sm",
        "dkc3",
        "metroidfusion",
        "dkc2",
        "diddy_kong_racing",
        "star_fox_64",
        "tmc",
        "rogue_legacy",
        "tloz_oos",
        "hcniko",
        "witness",
        "sm_map_rando",
        "tunic",
        "dkc"
    ],
    "shielded enemies": [
        "hk",
        "dkc3",
        "tmc",
        "alttp",
        "tloz_ooa",
        "rogue_legacy"
    ],
    "shielded": [
        "hk",
        "dkc3",
        "tmc",
        "alttp",
        "tloz_ooa",
        "rogue_legacy"
    ],
    "enemies": [
        "hk",
        "dkc3",
        "tmc",
        "alttp",
        "tloz_ooa",
        "rogue_legacy"
    ],
    "walking through walls": [
        "ladx",
        "doom_ii",
        "alttp",
        "tloz_ooa",
        "oot",
        "tloz_oos"
    ],
    "walking": [
        "ladx",
        "doom_ii",
        "alttp",
        "tloz_ooa",
        "oot",
        "tloz_oos"
    ],
    "through": [
        "ladx",
        "doom_ii",
        "alttp",
        "tloz_ooa",
        "oot",
        "tloz_oos"
    ],
    "walls": [
        "ladx",
        "doom_ii",
        "alttp",
        "tloz_ooa",
        "oot",
        "tloz_oos"
    ],
    "villain": [
        "mm2",
        "mm3",
        "star_fox_64",
        "tmc",
        "cvcotm",
        "alttp",
        "metroidfusion",
        "papermario",
        "sotn",
        "tloz_ooa",
        "zelda2",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "tloz_oos",
        "oot",
        "kh1"
    ],
    "recurring boss": [
        "mm3",
        "dkc2",
        "dkc3",
        "alttp",
        "metroidfusion",
        "papermario",
        "pokemon_emerald",
        "banjo_tooie",
        "dk64",
        "kh1",
        "dkc"
    ],
    "recurring": [
        "mm3",
        "dkc2",
        "dkc3",
        "alttp",
        "metroidfusion",
        "papermario",
        "pokemon_emerald",
        "banjo_tooie",
        "dk64",
        "kh1",
        "dkc"
    ],
    "boss": [
        "mm3",
        "doom_ii",
        "alttp",
        "dark_souls_2",
        "dkc3",
        "metroidfusion",
        "cuphead",
        "oot",
        "dkc2",
        "metroidprime",
        "sms",
        "tmc",
        "mm_recomp",
        "papermario",
        "rogue_legacy",
        "pokemon_emerald",
        "banjo_tooie",
        "dk64",
        "kh1",
        "tloz_ph",
        "dkc"
    ],
    "been here before": [
        "gstla",
        "pokemon_crystal",
        "sms",
        "tmc",
        "simpsonshitnrun",
        "tloz_ph",
        "alttp",
        "ffta",
        "oot"
    ],
    "been": [
        "gstla",
        "pokemon_crystal",
        "sms",
        "tmc",
        "simpsonshitnrun",
        "tloz_ph",
        "alttp",
        "ffta",
        "oot"
    ],
    "here": [
        "gstla",
        "hcniko",
        "pokemon_crystal",
        "sms",
        "tmc",
        "simpsonshitnrun",
        "tloz_ph",
        "alttp",
        "ffta",
        "oot"
    ],
    "before": [
        "gstla",
        "pokemon_crystal",
        "sms",
        "tmc",
        "simpsonshitnrun",
        "tloz_ph",
        "alttp",
        "ffta",
        "oot"
    ],
    "sleeping": [
        "minecraft",
        "gstla",
        "pokemon_crystal",
        "sms",
        "tmc",
        "alttp",
        "papermario"
    ],
    "merchants": [
        "hk",
        "yugiohddm",
        "faxanadu",
        "timespinner",
        "alttp",
        "candybox2",
        "terraria"
    ],
    "fetch quests": [
        "ladx",
        "metroidprime",
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "tloz_oos"
    ],
    "fetch": [
        "ladx",
        "metroidprime",
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "tloz_oos"
    ],
    "poisoning": [
        "minecraft",
        "pokemon_crystal",
        "cv64",
        "tmc",
        "alttp",
        "papermario",
        "pokemon_emerald",
        "tloz_oos"
    ],
    "status effects": [
        "minecraft",
        "ladx",
        "pokemon_crystal",
        "tmc",
        "alttp",
        "zelda2",
        "earthbound",
        "tloz_ooa",
        "pokemon_emerald",
        "dark_souls_2",
        "tloz_oos"
    ],
    "status": [
        "minecraft",
        "ladx",
        "pokemon_crystal",
        "tmc",
        "alttp",
        "zelda2",
        "earthbound",
        "tloz_ooa",
        "pokemon_emerald",
        "dark_souls_2",
        "tloz_oos"
    ],
    "effects": [
        "minecraft",
        "ladx",
        "pokemon_crystal",
        "tmc",
        "alttp",
        "zelda2",
        "earthbound",
        "tloz_ooa",
        "pokemon_emerald",
        "dark_souls_2",
        "tloz_oos"
    ],
    "damage over time": [
        "pokemon_crystal",
        "jakanddaxter",
        "tmc",
        "tloz_ph",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "oot",
        "tloz_oos"
    ],
    "damage": [
        "pokemon_crystal",
        "jakanddaxter",
        "tmc",
        "tloz_ph",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "oot",
        "tloz_oos"
    ],
    "over": [
        "pokemon_crystal",
        "jakanddaxter",
        "getting_over_it",
        "tmc",
        "tloz_ph",
        "alttp",
        "ffta",
        "pokemon_emerald",
        "oot",
        "tloz_oos"
    ],
    "monomyth": [
        "mm2",
        "mm3",
        "tmc",
        "tloz_ph",
        "alttp",
        "zelda2",
        "ss"
    ],
    "retroachievements": [
        "kdl3",
        "cv64",
        "alttp",
        "sm64ex",
        "ff4fe",
        "ffmq",
        "quake",
        "tloz",
        "lufia2ac",
        "dkc3",
        "swr",
        "mmx3",
        "mk64",
        "oot",
        "k64",
        "sm64hacks",
        "diddy_kong_racing",
        "dkc2",
        "star_fox_64",
        "metroidprime",
        "sms",
        "mm_recomp",
        "papermario",
        "banjo_tooie",
        "tetrisattack",
        "dk64",
        "sonic_heroes",
        "smw",
        "earthbound",
        "tww",
        "dkc"
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
        "hk",
        "pokemon_rb",
        "mm3",
        "timespinner",
        "pokemon_crystal",
        "getting_over_it",
        "kdl3",
        "wargroove",
        "sotn",
        "enderlilies",
        "pokemon_frlg",
        "megamix",
        "zelda2",
        "blasphemous",
        "ff4fe",
        "ff1",
        "ffmq",
        "mzm",
        "sm",
        "celeste",
        "lufia2ac",
        "dkc3",
        "messenger",
        "spire",
        "aquaria",
        "ror1",
        "mmx3",
        "metroidfusion",
        "hylics2",
        "mlss",
        "cuphead",
        "k64",
        "oribf",
        "zillion",
        "mm2",
        "dkc2",
        "wl",
        "cvcotm",
        "noita",
        "papermario",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "pokemon_emerald",
        "v6",
        "terraria",
        "marioland2",
        "tetrisattack",
        "yoshisisland",
        "wl4",
        "aus",
        "monster_sanctuary",
        "wargroove2",
        "ladx",
        "faxanadu",
        "sm_map_rando",
        "celeste_open_world",
        "dlcquest",
        "musedash",
        "smw",
        "smz3",
        "ufo50",
        "animal_well",
        "dkc"
    ],
    "horror": [
        "doom_ii",
        "getting_over_it",
        "cv64",
        "residentevil2remake",
        "sotn",
        "blasphemous",
        "quake",
        "poe",
        "inscryption",
        "dontstarvetogether",
        "shivers",
        "cvcotm",
        "mm_recomp",
        "terraria",
        "lunacid",
        "lethal_company",
        "doom_1993",
        "undertale",
        "residentevil3remake",
        "luigismansion",
        "animal_well"
    ],
    "survival": [
        "minecraft",
        "subnautica",
        "ror2",
        "rimworld",
        "residentevil2remake",
        "factorio",
        "ror1",
        "residentevil3remake",
        "yugioh06",
        "raft",
        "dontstarvetogether",
        "terraria",
        "factorio_saws",
        "animal_well"
    ],
    "mystery": [
        "animal_well",
        "witness",
        "inscryption",
        "crystal_project",
        "pmd_eos",
        "outer_wilds"
    ],
    "exploration": [
        "animal_well",
        "pokemon_crystal",
        "cv64",
        "sm",
        "seaofthieves",
        "celeste",
        "aquaria",
        "lingo",
        "shorthike",
        "metroidfusion",
        "hylics2",
        "subnautica",
        "metroidprime",
        "rogue_legacy",
        "pokemon_emerald",
        "v6",
        "terraria",
        "hcniko",
        "jakanddaxter",
        "lethal_company",
        "sm_map_rando",
        "tloz_ph",
        "witness",
        "celeste_open_world",
        "dlcquest",
        "tunic",
        "outer_wilds"
    ],
    "retro": [
        "minecraft",
        "celeste",
        "messenger",
        "timespinner",
        "ufo50",
        "celeste_open_world",
        "dlcquest",
        "undertale",
        "hylics2",
        "blasphemous",
        "cuphead",
        "v6",
        "terraria",
        "smo",
        "stardew_valley",
        "animal_well"
    ],
    "2d": [
        "hk",
        "celeste",
        "messenger",
        "sm_map_rando",
        "celeste_open_world",
        "musedash",
        "undertale",
        "sotn",
        "zelda2",
        "earthbound",
        "blasphemous",
        "cuphead",
        "v6",
        "terraria",
        "stardew_valley",
        "animal_well",
        "dontstarvetogether",
        "sm"
    ],
    "metroidvania": [
        "hk",
        "timespinner",
        "sotn",
        "enderlilies",
        "zelda2",
        "mzm",
        "blasphemous",
        "frogmonster",
        "dark_souls_2",
        "sm",
        "messenger",
        "aquaria",
        "metroidfusion",
        "pseudoregalia",
        "oribf",
        "zillion",
        "metroidprime",
        "cvcotm",
        "crystal_project",
        "rogue_legacy",
        "momodoramoonlitfarewell",
        "v6",
        "aus",
        "monster_sanctuary",
        "faxanadu",
        "sm_map_rando",
        "animal_well"
    ],
    "atmospheric": [
        "hk",
        "celeste",
        "frogmonster",
        "shorthike",
        "tunic",
        "celeste_open_world",
        "crystal_project",
        "hylics2",
        "dontstarvetogether",
        "powerwashsimulator",
        "animal_well"
    ],
    "relaxing": [
        "hcniko",
        "stardew_valley",
        "shorthike",
        "sims4",
        "powerwashsimulator",
        "animal_well"
    ],
    "controller support": [
        "hk",
        "hcniko",
        "shorthike",
        "tunic",
        "v6",
        "stardew_valley",
        "animal_well"
    ],
    "controller": [
        "hk",
        "hcniko",
        "shorthike",
        "tunic",
        "v6",
        "stardew_valley",
        "animal_well"
    ],
    "support": [
        "hk",
        "hcniko",
        "shorthike",
        "tunic",
        "v6",
        "stardew_valley",
        "animal_well"
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
        "spyro3",
        "sotn",
        "apeescape",
        "rogue_legacy",
        "kh2",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "sa2b",
        "sadx"
    ],
    "3": [
        "spyro3",
        "mm3",
        "kdl3",
        "mmbn3",
        "wl",
        "residentevil3remake",
        "apeescape",
        "kh2",
        "rogue_legacy",
        "sotn",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "sa2b",
        "sadx"
    ],
    "playstation portable": [
        "sotn",
        "apeescape",
        "spyro3"
    ],
    "portable": [
        "sotn",
        "apeescape",
        "spyro3"
    ],
    "anime": [
        "wl4",
        "yugiohddm",
        "osu",
        "gstla",
        "pokemon_crystal",
        "fm",
        "zillion",
        "musedash",
        "apeescape",
        "huniepop",
        "dw1",
        "pokemon_emerald",
        "huniepop2"
    ],
    "dinosaurs": [
        "sms",
        "smw",
        "apeescape",
        "earthbound",
        "banjo_tooie",
        "smo",
        "yoshisisland"
    ],
    "collecting": [
        "pokemon_rb",
        "mzm",
        "pokemon_crystal",
        "apeescape",
        "zelda2",
        "pokemon_emerald",
        "banjo_tooie",
        "pokemon_frlg"
    ],
    "multiple endings": [
        "wl4",
        "dkc2",
        "star_fox_64",
        "civ_6",
        "doom_ii",
        "cv64",
        "metroidprime",
        "witness",
        "mmx3",
        "undertale",
        "sotn",
        "apeescape",
        "mzm",
        "cuphead",
        "tloz_oos",
        "k64",
        "dk64",
        "kh1"
    ],
    "multiple": [
        "spyro3",
        "doom_ii",
        "cv64",
        "sotn",
        "apeescape",
        "mzm",
        "dkc3",
        "mmx3",
        "lego_star_wars_tcs",
        "cuphead",
        "dkc",
        "k64",
        "dkc2",
        "star_fox_64",
        "metroidprime",
        "rogue_legacy",
        "tloz_oos",
        "dk64",
        "kh1",
        "wl4",
        "sonic_heroes",
        "civ_6",
        "witness",
        "undertale",
        "earthbound",
        "mlss"
    ],
    "endings": [
        "wl4",
        "dkc2",
        "star_fox_64",
        "civ_6",
        "doom_ii",
        "cv64",
        "metroidprime",
        "witness",
        "mmx3",
        "undertale",
        "sotn",
        "apeescape",
        "mzm",
        "cuphead",
        "tloz_oos",
        "k64",
        "dk64",
        "kh1"
    ],
    "amnesia": [
        "sonic_heroes",
        "witness",
        "aquaria",
        "tloz_ph",
        "apeescape",
        "xenobladex"
    ],
    "voice acting": [
        "sonic_heroes",
        "star_fox_64",
        "sly1",
        "doom_ii",
        "civ_6",
        "cv64",
        "jakanddaxter",
        "simpsonshitnrun",
        "sms",
        "witness",
        "xenobladex",
        "apeescape",
        "dw1",
        "cuphead",
        "kh1",
        "huniepop2"
    ],
    "voice": [
        "sonic_heroes",
        "star_fox_64",
        "sly1",
        "doom_ii",
        "civ_6",
        "cv64",
        "jakanddaxter",
        "simpsonshitnrun",
        "sms",
        "witness",
        "xenobladex",
        "apeescape",
        "dw1",
        "cuphead",
        "kh1",
        "huniepop2"
    ],
    "acting": [
        "sonic_heroes",
        "star_fox_64",
        "sly1",
        "doom_ii",
        "civ_6",
        "cv64",
        "jakanddaxter",
        "simpsonshitnrun",
        "sms",
        "witness",
        "xenobladex",
        "apeescape",
        "dw1",
        "cuphead",
        "kh1",
        "huniepop2"
    ],
    "moving platforms": [
        "spyro3",
        "mm3",
        "cv64",
        "sotn",
        "apeescape",
        "blasphemous",
        "quake",
        "dkc3",
        "mmx3",
        "k64",
        "mm2",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "cvcotm",
        "papermario",
        "v6",
        "dk64",
        "wl4",
        "sonic_heroes",
        "ladx",
        "jakanddaxter",
        "tloz_ph",
        "dkc"
    ],
    "moving": [
        "spyro3",
        "mm3",
        "cv64",
        "sotn",
        "apeescape",
        "blasphemous",
        "quake",
        "dkc3",
        "mmx3",
        "k64",
        "mm2",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "cvcotm",
        "papermario",
        "v6",
        "dk64",
        "wl4",
        "sonic_heroes",
        "ladx",
        "jakanddaxter",
        "tloz_ph",
        "dkc"
    ],
    "platforms": [
        "spyro3",
        "mm3",
        "doom_ii",
        "cv64",
        "sotn",
        "apeescape",
        "zelda2",
        "blasphemous",
        "sm",
        "quake",
        "dkc3",
        "mmx3",
        "k64",
        "oribf",
        "mm2",
        "sly1",
        "metroidprime",
        "sms",
        "tmc",
        "cvcotm",
        "papermario",
        "v6",
        "dk64",
        "wl4",
        "sonic_heroes",
        "ladx",
        "jakanddaxter",
        "sm_map_rando",
        "tloz_ph",
        "dkc"
    ],
    "time trials": [
        "spyro3",
        "diddy_kong_racing",
        "sly1",
        "apeescape",
        "mk64",
        "v6"
    ],
    "trials": [
        "spyro3",
        "diddy_kong_racing",
        "sly1",
        "apeescape",
        "mk64",
        "v6"
    ],
    "aquaria": [
        "aquaria"
    ],
    "drama": [
        "undertale",
        "aquaria",
        "earthbound",
        "hades"
    ],
    "linux": [
        "chainedechoes",
        "hk",
        "timespinner",
        "getting_over_it",
        "openrct2",
        "blasphemous",
        "overcooked2",
        "cat_quest",
        "shapez",
        "quake",
        "celeste",
        "aquaria",
        "shorthike",
        "ror1",
        "inscryption",
        "dontstarvetogether",
        "stardew_valley",
        "celeste64",
        "minecraft",
        "factorio",
        "landstalker",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "bumpstik",
        "rimworld",
        "terraria",
        "v6",
        "monster_sanctuary",
        "osu",
        "doom_1993",
        "celeste_open_world",
        "undertale",
        "huniepop",
        "factorio_saws"
    ],
    "android": [
        "brotato",
        "osu",
        "subnautica",
        "getting_over_it",
        "aquaria",
        "balatro",
        "osrs",
        "musedash",
        "blasphemous",
        "v6",
        "terraria",
        "stardew_valley",
        "lego_star_wars_tcs",
        "cat_quest",
        "shapez"
    ],
    "ios": [
        "getting_over_it",
        "balatro",
        "residentevil2remake",
        "blasphemous",
        "cat_quest",
        "shapez",
        "brotato",
        "aquaria",
        "lego_star_wars_tcs",
        "stardew_valley",
        "hades",
        "v6",
        "terraria",
        "osu",
        "witness",
        "osrs",
        "musedash",
        "residentevil3remake",
        "subnautica"
    ],
    "alternate costumes": [
        "sms",
        "aquaria",
        "cv64",
        "simpsonshitnrun",
        "metroidfusion",
        "lego_star_wars_tcs",
        "smo",
        "kh1"
    ],
    "alternate": [
        "sms",
        "aquaria",
        "cv64",
        "simpsonshitnrun",
        "metroidfusion",
        "lego_star_wars_tcs",
        "smo",
        "kh1"
    ],
    "costumes": [
        "sms",
        "aquaria",
        "cv64",
        "simpsonshitnrun",
        "metroidfusion",
        "lego_star_wars_tcs",
        "smo",
        "kh1"
    ],
    "underwater gameplay": [
        "mm2",
        "quake",
        "sm64hacks",
        "mm3",
        "dkc2",
        "metroidprime",
        "sms",
        "aquaria",
        "mmx3",
        "metroidfusion",
        "smo",
        "sm64ex",
        "banjo_tooie",
        "terraria",
        "oot",
        "subnautica",
        "kh1",
        "dkc"
    ],
    "underwater": [
        "mm2",
        "quake",
        "sm64hacks",
        "mm3",
        "dkc2",
        "metroidprime",
        "sms",
        "aquaria",
        "mmx3",
        "metroidfusion",
        "smo",
        "sm64ex",
        "banjo_tooie",
        "terraria",
        "oot",
        "subnautica",
        "kh1",
        "dkc"
    ],
    "gameplay": [
        "mm2",
        "quake",
        "sm64hacks",
        "mm3",
        "dkc2",
        "metroidprime",
        "sms",
        "aquaria",
        "mmx3",
        "metroidfusion",
        "smo",
        "sm64ex",
        "banjo_tooie",
        "terraria",
        "oot",
        "subnautica",
        "kh1",
        "dkc"
    ],
    "shape-shifting": [
        "metroidprime",
        "kdl3",
        "aquaria",
        "mm_recomp",
        "sotn",
        "banjo_tooie",
        "k64"
    ],
    "plot twist": [
        "aquaria",
        "cv64",
        "undertale",
        "metroidfusion",
        "oot",
        "kh1"
    ],
    "plot": [
        "aquaria",
        "cv64",
        "undertale",
        "metroidfusion",
        "oot",
        "kh1"
    ],
    "twist": [
        "aquaria",
        "cv64",
        "undertale",
        "metroidfusion",
        "oot",
        "kh1"
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
        "aus",
        "celeste",
        "getting_over_it",
        "hades",
        "celeste_open_world",
        "undertale",
        "hylics2",
        "powerwashsimulator"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "chainedechoes",
        "monster_sanctuary",
        "pokemon_rb",
        "wargroove2",
        "yugiohddm",
        "civ_6",
        "fm",
        "balatro",
        "wargroove",
        "undertale",
        "ffta",
        "crystal_project",
        "earthbound",
        "hylics2",
        "yugioh06",
        "pokemon_emerald",
        "pmd_eos",
        "pokemon_frlg"
    ],
    "turn-based": [
        "chainedechoes",
        "pokemon_rb",
        "pokemon_crystal",
        "balatro",
        "wargroove",
        "pmd_eos",
        "ffmq",
        "yugiohddm",
        "fm",
        "ffta",
        "hylics2",
        "mlss",
        "papermario",
        "crystal_project",
        "pokemon_emerald",
        "monster_sanctuary",
        "wargroove2",
        "gstla",
        "civ_6",
        "undertale",
        "yugioh06",
        "earthbound",
        "pokemon_frlg"
    ],
    "(tbs)": [
        "chainedechoes",
        "monster_sanctuary",
        "pokemon_rb",
        "wargroove2",
        "yugiohddm",
        "civ_6",
        "fm",
        "balatro",
        "wargroove",
        "undertale",
        "ffta",
        "crystal_project",
        "earthbound",
        "hylics2",
        "yugioh06",
        "pokemon_emerald",
        "pmd_eos",
        "pokemon_frlg"
    ],
    "card & board game": [
        "yugiohddm",
        "spire",
        "fm",
        "balatro",
        "inscryption",
        "yugioh06"
    ],
    "card": [
        "yugiohddm",
        "spire",
        "fm",
        "balatro",
        "inscryption",
        "yugioh06"
    ],
    "board": [
        "yugiohddm",
        "spire",
        "fm",
        "balatro",
        "inscryption",
        "yugioh06"
    ],
    "game": [
        "pokemon_rb",
        "spyro3",
        "pokemon_crystal",
        "doom_ii",
        "mmbn3",
        "balatro",
        "pokemon_frlg",
        "mzm",
        "yugiohddm",
        "spire",
        "fm",
        "inscryption",
        "ffta",
        "metroidfusion",
        "oot",
        "mm2",
        "dkc2",
        "wl",
        "tmc",
        "cvcotm",
        "rogue_legacy",
        "pokemon_emerald",
        "tloz_oos",
        "marioland2",
        "wl4",
        "ladx",
        "gstla",
        "hcniko",
        "witness",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "mlss"
    ],
    "roguelike": [
        "spire",
        "balatro",
        "hades",
        "ror1",
        "rogue_legacy",
        "pmd_eos"
    ],
    "banjo-tooie": [
        "banjo_tooie"
    ],
    "quiz/trivia": [
        "banjo_tooie"
    ],
    "comedy": [
        "zork_grand_inquisitor",
        "spyro3",
        "placidplasticducksim",
        "getting_over_it",
        "simpsonshitnrun",
        "doronko_wanko",
        "sims4",
        "toontown",
        "overcooked2",
        "quake",
        "messenger",
        "lego_star_wars_tcs",
        "cuphead",
        "diddy_kong_racing",
        "dkc2",
        "sly1",
        "papermario",
        "rogue_legacy",
        "dw1",
        "banjo_tooie",
        "dk64",
        "kh1",
        "hcniko",
        "jakanddaxter",
        "lethal_company",
        "dlcquest",
        "musedash",
        "undertale",
        "huniepop",
        "rac2",
        "candybox2",
        "luigismansion",
        "mlss"
    ],
    "nintendo 64": [
        "sm64hacks",
        "diddy_kong_racing",
        "star_fox_64",
        "cv64",
        "swr",
        "mm_recomp",
        "papermario",
        "sm64ex",
        "mk64",
        "banjo_tooie",
        "k64",
        "oot",
        "dk64"
    ],
    "64": [
        "sm64hacks",
        "diddy_kong_racing",
        "star_fox_64",
        "cv64",
        "swr",
        "mm_recomp",
        "papermario",
        "sm64ex",
        "mk64",
        "banjo_tooie",
        "k64",
        "oot",
        "dk64"
    ],
    "aliens": [
        "quake",
        "mzm",
        "hcniko",
        "metroidprime",
        "lethal_company",
        "sm_map_rando",
        "simpsonshitnrun",
        "factorio",
        "metroidfusion",
        "earthbound",
        "lego_star_wars_tcs",
        "xenobladex",
        "banjo_tooie",
        "sc2",
        "factorio_saws",
        "sm"
    ],
    "flight": [
        "mm2",
        "wl4",
        "spyro3",
        "mm3",
        "diddy_kong_racing",
        "star_fox_64",
        "shorthike",
        "hylics2",
        "rogue_legacy",
        "lego_star_wars_tcs",
        "xenobladex",
        "banjo_tooie",
        "terraria",
        "dkc"
    ],
    "witches": [
        "minecraft",
        "cv64",
        "tmc",
        "enderlilies",
        "tloz_ooa",
        "banjo_tooie",
        "tloz_oos"
    ],
    "achievements": [
        "hk",
        "sonic_heroes",
        "minecraft",
        "dark_souls_2",
        "doom_ii",
        "hcniko",
        "shorthike",
        "tunic",
        "musedash",
        "sotn",
        "v6",
        "blasphemous",
        "cuphead",
        "banjo_tooie",
        "stardew_valley",
        "lego_star_wars_tcs",
        "oribf",
        "huniepop2"
    ],
    "talking animals": [
        "dkc2",
        "diddy_kong_racing",
        "dkc3",
        "hcniko",
        "sly1",
        "star_fox_64",
        "banjo_tooie",
        "dkc"
    ],
    "talking": [
        "dkc2",
        "diddy_kong_racing",
        "dkc3",
        "hcniko",
        "sly1",
        "star_fox_64",
        "banjo_tooie",
        "dkc"
    ],
    "animals": [
        "dkc2",
        "diddy_kong_racing",
        "dkc3",
        "hcniko",
        "sly1",
        "star_fox_64",
        "banjo_tooie",
        "dkc"
    ],
    "breaking the fourth wall": [
        "dkc2",
        "ladx",
        "doom_ii",
        "jakanddaxter",
        "tmc",
        "simpsonshitnrun",
        "undertale",
        "papermario",
        "ffta",
        "metroidfusion",
        "rogue_legacy",
        "mlss",
        "banjo_tooie",
        "dkc"
    ],
    "breaking": [
        "doom_ii",
        "simpsonshitnrun",
        "sotn",
        "mzm",
        "sm",
        "ffta",
        "metroidfusion",
        "dkc",
        "oot",
        "dkc2",
        "metroidprime",
        "tmc",
        "papermario",
        "rogue_legacy",
        "banjo_tooie",
        "wl4",
        "ladx",
        "jakanddaxter",
        "sm_map_rando",
        "undertale",
        "tloz_ooa",
        "mlss"
    ],
    "fourth": [
        "dkc2",
        "ladx",
        "doom_ii",
        "jakanddaxter",
        "tmc",
        "simpsonshitnrun",
        "undertale",
        "papermario",
        "ffta",
        "metroidfusion",
        "rogue_legacy",
        "mlss",
        "banjo_tooie",
        "dkc"
    ],
    "temporary invincibility": [
        "quake",
        "sonic_heroes",
        "dkc2",
        "faxanadu",
        "doom_ii",
        "jakanddaxter",
        "mk64",
        "papermario",
        "rogue_legacy",
        "cuphead",
        "banjo_tooie"
    ],
    "temporary": [
        "quake",
        "sonic_heroes",
        "dkc2",
        "faxanadu",
        "doom_ii",
        "jakanddaxter",
        "mk64",
        "papermario",
        "rogue_legacy",
        "cuphead",
        "banjo_tooie"
    ],
    "invincibility": [
        "quake",
        "sonic_heroes",
        "dkc2",
        "faxanadu",
        "doom_ii",
        "jakanddaxter",
        "mk64",
        "papermario",
        "rogue_legacy",
        "cuphead",
        "banjo_tooie"
    ],
    "gliding": [
        "spyro3",
        "sly1",
        "sms",
        "tmc",
        "shorthike",
        "banjo_tooie",
        "kh1"
    ],
    "lgbtq+": [
        "celeste",
        "timespinner",
        "simpsonshitnrun",
        "celeste_open_world",
        "rogue_legacy",
        "sims4",
        "banjo_tooie",
        "celeste64"
    ],
    "blasphemous": [
        "blasphemous"
    ],
    "role-playing (rpg)": [
        "chainedechoes",
        "dark_souls_3",
        "pokemon_rb",
        "timespinner",
        "pokemon_crystal",
        "mmbn3",
        "sotn",
        "enderlilies",
        "meritous",
        "pokemon_frlg",
        "sims4",
        "blasphemous",
        "ff4fe",
        "dark_souls_2",
        "ff1",
        "ffmq",
        "pmd_eos",
        "toontown",
        "cat_quest",
        "brotato",
        "lufia2ac",
        "dsr",
        "poe",
        "ror1",
        "zelda2",
        "ffta",
        "hylics2",
        "ctjot",
        "xenobladex",
        "stardew_valley",
        "cvcotm",
        "hades",
        "noita",
        "landstalker",
        "papermario",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "dw1",
        "soe",
        "pokemon_emerald",
        "terraria",
        "tloz_oos",
        "kh1",
        "monster_sanctuary",
        "wargroove2",
        "faxanadu",
        "gstla",
        "lunacid",
        "osrs",
        "ufo50",
        "bomb_rush_cyberfunk",
        "undertale",
        "huniepop",
        "earthbound",
        "kh2",
        "tloz_ooa",
        "candybox2",
        "tunic",
        "mlss"
    ],
    "role-playing": [
        "chainedechoes",
        "dark_souls_3",
        "pokemon_rb",
        "timespinner",
        "pokemon_crystal",
        "mmbn3",
        "sotn",
        "enderlilies",
        "meritous",
        "pokemon_frlg",
        "sims4",
        "blasphemous",
        "ff4fe",
        "dark_souls_2",
        "ff1",
        "ffmq",
        "pmd_eos",
        "toontown",
        "cat_quest",
        "brotato",
        "lufia2ac",
        "dsr",
        "poe",
        "ror1",
        "zelda2",
        "ffta",
        "hylics2",
        "ctjot",
        "xenobladex",
        "stardew_valley",
        "cvcotm",
        "hades",
        "noita",
        "landstalker",
        "papermario",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "dw1",
        "soe",
        "pokemon_emerald",
        "terraria",
        "tloz_oos",
        "kh1",
        "monster_sanctuary",
        "wargroove2",
        "faxanadu",
        "gstla",
        "lunacid",
        "osrs",
        "ufo50",
        "bomb_rush_cyberfunk",
        "undertale",
        "huniepop",
        "earthbound",
        "kh2",
        "tloz_ooa",
        "candybox2",
        "tunic",
        "mlss"
    ],
    "(rpg)": [
        "chainedechoes",
        "dark_souls_3",
        "pokemon_rb",
        "timespinner",
        "pokemon_crystal",
        "mmbn3",
        "sotn",
        "enderlilies",
        "meritous",
        "pokemon_frlg",
        "sims4",
        "blasphemous",
        "ff4fe",
        "dark_souls_2",
        "ff1",
        "ffmq",
        "pmd_eos",
        "toontown",
        "cat_quest",
        "brotato",
        "lufia2ac",
        "dsr",
        "poe",
        "ror1",
        "zelda2",
        "ffta",
        "hylics2",
        "ctjot",
        "xenobladex",
        "stardew_valley",
        "cvcotm",
        "hades",
        "noita",
        "landstalker",
        "papermario",
        "crosscode",
        "crystal_project",
        "rogue_legacy",
        "dw1",
        "soe",
        "pokemon_emerald",
        "terraria",
        "tloz_oos",
        "kh1",
        "monster_sanctuary",
        "wargroove2",
        "faxanadu",
        "gstla",
        "lunacid",
        "osrs",
        "ufo50",
        "bomb_rush_cyberfunk",
        "undertale",
        "huniepop",
        "earthbound",
        "kh2",
        "tloz_ooa",
        "candybox2",
        "tunic",
        "mlss"
    ],
    "hack and slash/beat 'em up": [
        "poe",
        "cv64",
        "hades",
        "ror1",
        "blasphemous"
    ],
    "hack": [
        "poe",
        "cv64",
        "hades",
        "ror1",
        "blasphemous"
    ],
    "slash/beat": [
        "poe",
        "cv64",
        "hades",
        "ror1",
        "blasphemous"
    ],
    "'em": [
        "poe",
        "cv64",
        "hades",
        "ror1",
        "blasphemous"
    ],
    "up": [
        "gstla",
        "pokemon_crystal",
        "poe",
        "pokemon_emerald",
        "cv64",
        "cvcotm",
        "hades",
        "ror1",
        "landstalker",
        "undertale",
        "papermario",
        "sotn",
        "zelda2",
        "earthbound",
        "dw1",
        "blasphemous",
        "dark_souls_2",
        "kh1"
    ],
    "bloody": [
        "quake",
        "heretic",
        "doom_ii",
        "metroidprime",
        "cv64",
        "poe",
        "ultrakill",
        "residentevil2remake",
        "sotn",
        "blasphemous"
    ],
    "difficult": [
        "celeste",
        "messenger",
        "getting_over_it",
        "tunic",
        "hades",
        "ror1",
        "celeste_open_world",
        "zelda2",
        "blasphemous",
        "dontstarvetogether"
    ],
    "side-scrolling": [
        "mm3",
        "kdl3",
        "sotn",
        "zelda2",
        "mzm",
        "blasphemous",
        "sm",
        "dkc3",
        "mmx3",
        "metroidfusion",
        "hylics2",
        "cuphead",
        "k64",
        "mm2",
        "dkc2",
        "rogue_legacy",
        "yoshisisland",
        "sm_map_rando",
        "musedash",
        "dkc"
    ],
    "great soundtrack": [
        "celeste",
        "getting_over_it",
        "shorthike",
        "ultrakill",
        "celeste_open_world",
        "bomb_rush_cyberfunk",
        "undertale",
        "hylics2",
        "blasphemous",
        "tunic"
    ],
    "great": [
        "celeste",
        "getting_over_it",
        "shorthike",
        "ultrakill",
        "celeste_open_world",
        "bomb_rush_cyberfunk",
        "undertale",
        "hylics2",
        "blasphemous",
        "tunic"
    ],
    "soundtrack": [
        "celeste",
        "getting_over_it",
        "shorthike",
        "ultrakill",
        "celeste_open_world",
        "bomb_rush_cyberfunk",
        "undertale",
        "hylics2",
        "blasphemous",
        "tunic"
    ],
    "soulslike": [
        "dark_souls_3",
        "dsr",
        "enderlilies",
        "blasphemous",
        "tunic",
        "dark_souls_2"
    ],
    "you can pet the dog": [
        "seaofthieves",
        "hades",
        "undertale",
        "sims4",
        "blasphemous",
        "terraria",
        "overcooked2"
    ],
    "you": [
        "seaofthieves",
        "hades",
        "undertale",
        "sims4",
        "blasphemous",
        "terraria",
        "overcooked2"
    ],
    "can": [
        "seaofthieves",
        "hades",
        "undertale",
        "sims4",
        "blasphemous",
        "terraria",
        "overcooked2"
    ],
    "pet": [
        "seaofthieves",
        "hades",
        "undertale",
        "sims4",
        "blasphemous",
        "terraria",
        "overcooked2"
    ],
    "dog": [
        "minecraft",
        "seaofthieves",
        "star_fox_64",
        "hcniko",
        "sly1",
        "cv64",
        "tmc",
        "tloz_oos",
        "hades",
        "undertale",
        "doronko_wanko",
        "soe",
        "sims4",
        "blasphemous",
        "oot",
        "terraria",
        "smo",
        "overcooked2"
    ],
    "interconnected-world": [
        "dark_souls_3",
        "hk",
        "mzm",
        "dsr",
        "sm_map_rando",
        "luigismansion",
        "sotn",
        "blasphemous",
        "dark_souls_2",
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
        "trackmania",
        "bomb_rush_cyberfunk"
    ],
    "science fiction": [
        "mm3",
        "doom_ii",
        "mmbn3",
        "mzm",
        "sm",
        "brotato",
        "quake",
        "ror1",
        "mmx3",
        "swr",
        "metroidfusion",
        "ctjot",
        "lego_star_wars_tcs",
        "xenobladex",
        "zillion",
        "mm2",
        "star_fox_64",
        "subnautica",
        "metroidprime",
        "tyrian",
        "ror2",
        "ultrakill",
        "factorio",
        "soe",
        "crosscode",
        "rimworld",
        "v6",
        "terraria",
        "jakanddaxter",
        "lethal_company",
        "sm_map_rando",
        "witness",
        "doom_1993",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "rac2",
        "earthbound",
        "sc2",
        "factorio_saws",
        "outer_wilds",
        "pokemon_frlg"
    ],
    "science": [
        "mm3",
        "doom_ii",
        "mmbn3",
        "mzm",
        "sm",
        "brotato",
        "quake",
        "ror1",
        "mmx3",
        "swr",
        "metroidfusion",
        "ctjot",
        "lego_star_wars_tcs",
        "xenobladex",
        "zillion",
        "mm2",
        "star_fox_64",
        "subnautica",
        "metroidprime",
        "tyrian",
        "ror2",
        "ultrakill",
        "factorio",
        "soe",
        "crosscode",
        "rimworld",
        "v6",
        "terraria",
        "jakanddaxter",
        "lethal_company",
        "sm_map_rando",
        "witness",
        "doom_1993",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "rac2",
        "earthbound",
        "sc2",
        "factorio_saws",
        "outer_wilds",
        "pokemon_frlg"
    ],
    "fiction": [
        "mm3",
        "doom_ii",
        "mmbn3",
        "mzm",
        "sm",
        "brotato",
        "quake",
        "ror1",
        "mmx3",
        "swr",
        "metroidfusion",
        "ctjot",
        "lego_star_wars_tcs",
        "xenobladex",
        "zillion",
        "mm2",
        "star_fox_64",
        "subnautica",
        "metroidprime",
        "tyrian",
        "ror2",
        "ultrakill",
        "factorio",
        "soe",
        "crosscode",
        "rimworld",
        "v6",
        "terraria",
        "jakanddaxter",
        "lethal_company",
        "sm_map_rando",
        "witness",
        "doom_1993",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "rac2",
        "earthbound",
        "sc2",
        "factorio_saws",
        "outer_wilds",
        "pokemon_frlg"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "heretic",
        "doom_ii",
        "residentevil2remake",
        "mzm",
        "frogmonster",
        "sm",
        "brotato",
        "quake",
        "ror1",
        "mmx3",
        "metroidfusion",
        "cuphead",
        "star_fox_64",
        "tboir",
        "metroidprime",
        "tyrian",
        "ror2",
        "noita",
        "ultrakill",
        "crosscode",
        "sm_map_rando",
        "doom_1993",
        "residentevil3remake",
        "rac2",
        "ufo50"
    ],
    "arcade": [
        "brotato",
        "mm3",
        "osu",
        "messenger",
        "tyrian",
        "noita",
        "mk64",
        "ultrakill",
        "smw",
        "megamix",
        "trackmania",
        "ufo50",
        "cuphead",
        "v6",
        "mario_kart_double_dash",
        "overcooked2"
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
    "archipelago": [
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
        "kindergarten_2",
        "sonic_heroes",
        "wargroove2",
        "sly1",
        "jakanddaxter",
        "ror2",
        "simpsonshitnrun",
        "residentevil2remake",
        "rac2",
        "hylics2",
        "dw1",
        "kh2",
        "candybox2",
        "smo",
        "stardew_valley",
        "overcooked2",
        "kh1"
    ],
    "text": [
        "osrs",
        "yugioh06",
        "huniepop",
        "candybox2",
        "huniepop2"
    ],
    "web browser": [
        "ttyd",
        "candybox2"
    ],
    "web": [
        "ttyd",
        "candybox2"
    ],
    "browser": [
        "ttyd",
        "candybox2"
    ],
    "cat quest": [
        "cat_quest"
    ],
    "cat": [
        "wl4",
        "minecraft",
        "dkc2",
        "cat_quest",
        "tmc",
        "cuphead",
        "tloz_oos",
        "kh1"
    ],
    "quest": [
        "ffmq",
        "dkc2",
        "cat_quest",
        "dlcquest"
    ],
    "celeste": [
        "celeste_open_world",
        "celeste",
        "celeste64"
    ],
    "google stadia": [
        "ror2",
        "celeste",
        "terraria",
        "celeste_open_world"
    ],
    "google": [
        "ror2",
        "celeste",
        "terraria",
        "celeste_open_world"
    ],
    "stadia": [
        "ror2",
        "celeste",
        "terraria",
        "celeste_open_world"
    ],
    "story rich": [
        "celeste",
        "getting_over_it",
        "hades",
        "celeste_open_world",
        "undertale",
        "hylics2",
        "powerwashsimulator"
    ],
    "rich": [
        "celeste",
        "getting_over_it",
        "hades",
        "celeste_open_world",
        "undertale",
        "hylics2",
        "powerwashsimulator"
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
        "chainedechoes",
        "ffta",
        "crystal_project",
        "hylics2",
        "ff1",
        "ff4fe",
        "pmd_eos",
        "ffmq"
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
        "minecraft",
        "civ_6",
        "cv64",
        "xenobladex",
        "terraria",
        "dk64"
    ],
    "loot": [
        "minecraft",
        "civ_6",
        "cv64",
        "xenobladex",
        "terraria",
        "dk64"
    ],
    "gathering": [
        "minecraft",
        "civ_6",
        "cv64",
        "xenobladex",
        "terraria",
        "dk64"
    ],
    "ambient music": [
        "dkc2",
        "dkc3",
        "civ_6",
        "metroidprime",
        "cv64",
        "soe",
        "metroidfusion",
        "mzm",
        "dkc"
    ],
    "ambient": [
        "dkc2",
        "dkc3",
        "civ_6",
        "metroidprime",
        "cv64",
        "soe",
        "metroidfusion",
        "mzm",
        "dkc"
    ],
    "music": [
        "placidplasticducksim",
        "doom_ii",
        "cv64",
        "sotn",
        "megamix",
        "mzm",
        "ffmq",
        "dkc3",
        "ffta",
        "metroidfusion",
        "dkc2",
        "metroidprime",
        "ultrakill",
        "soe",
        "sonic_heroes",
        "osu",
        "gstla",
        "civ_6",
        "musedash",
        "dkc"
    ],
    "crosscode": [
        "crosscode"
    ],
    "crystal project": [
        "crystal_project"
    ],
    "crystal": [
        "k64",
        "crystal_project",
        "pokemon_crystal"
    ],
    "project": [
        "crystal_project",
        "megamix"
    ],
    "tactical": [
        "mmbn3",
        "wargroove",
        "ffta",
        "crystal_project",
        "overcooked2"
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
        "wargroove2",
        "seaofthieves",
        "dkc2",
        "metroidprime",
        "tloz_ph",
        "metroidfusion",
        "tloz_ooa",
        "mzm",
        "cuphead",
        "tloz_oos",
        "kh1"
    ],
    "robots": [
        "mm2",
        "sonic_heroes",
        "mm3",
        "star_fox_64",
        "sms",
        "xenobladex",
        "ultrakill",
        "swr",
        "mmx3",
        "metroidfusion",
        "earthbound",
        "lego_star_wars_tcs",
        "cuphead"
    ],
    "violent plants": [
        "sms",
        "metroidprime",
        "metroidfusion",
        "rogue_legacy",
        "cuphead",
        "ss",
        "terraria"
    ],
    "violent": [
        "sms",
        "metroidprime",
        "metroidfusion",
        "rogue_legacy",
        "cuphead",
        "ss",
        "terraria"
    ],
    "plants": [
        "sms",
        "metroidprime",
        "metroidfusion",
        "rogue_legacy",
        "cuphead",
        "ss",
        "terraria"
    ],
    "auto-scrolling levels": [
        "dkc2",
        "dkc3",
        "star_fox_64",
        "cuphead",
        "v6",
        "k64",
        "dkc"
    ],
    "auto-scrolling": [
        "dkc2",
        "dkc3",
        "star_fox_64",
        "cuphead",
        "v6",
        "k64",
        "dkc"
    ],
    "levels": [
        "dkc2",
        "dkc3",
        "star_fox_64",
        "cuphead",
        "v6",
        "k64",
        "dkc"
    ],
    "boss assistance": [
        "dkc2",
        "doom_ii",
        "metroidprime",
        "sms",
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "papermario",
        "rogue_legacy",
        "cuphead",
        "dark_souls_2",
        "oot",
        "dkc"
    ],
    "assistance": [
        "dkc2",
        "doom_ii",
        "metroidprime",
        "sms",
        "tmc",
        "tloz_ph",
        "mm_recomp",
        "papermario",
        "rogue_legacy",
        "cuphead",
        "dark_souls_2",
        "oot",
        "dkc"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "horse": [
        "minecraft",
        "cv64",
        "cvcotm",
        "sotn",
        "rogue_legacy",
        "oot"
    ],
    "multiple protagonists": [
        "sonic_heroes",
        "spyro3",
        "dkc2",
        "dkc3",
        "cv64",
        "mmx3",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "lego_star_wars_tcs",
        "mlss",
        "dk64",
        "dkc"
    ],
    "protagonists": [
        "sonic_heroes",
        "spyro3",
        "dkc2",
        "dkc3",
        "cv64",
        "mmx3",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "lego_star_wars_tcs",
        "mlss",
        "dk64",
        "dkc"
    ],
    "traps": [
        "minecraft",
        "doom_ii",
        "cv64",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "dark_souls_2"
    ],
    "bats": [
        "pokemon_crystal",
        "cv64",
        "cvcotm",
        "sotn",
        "zelda2",
        "mk64",
        "terraria"
    ],
    "day/night cycle": [
        "minecraft",
        "ss",
        "pokemon_crystal",
        "jakanddaxter",
        "cv64",
        "stardew_valley",
        "mm_recomp",
        "sotn",
        "tww",
        "xenobladex",
        "oot",
        "terraria",
        "dk64"
    ],
    "day/night": [
        "minecraft",
        "ss",
        "pokemon_crystal",
        "jakanddaxter",
        "cv64",
        "stardew_valley",
        "mm_recomp",
        "sotn",
        "tww",
        "xenobladex",
        "oot",
        "terraria",
        "dk64"
    ],
    "cycle": [
        "minecraft",
        "ss",
        "pokemon_crystal",
        "jakanddaxter",
        "cv64",
        "stardew_valley",
        "mm_recomp",
        "sotn",
        "tww",
        "xenobladex",
        "oot",
        "terraria",
        "dk64"
    ],
    "skeletons": [
        "minecraft",
        "seaofthieves",
        "heretic",
        "sly1",
        "cv64",
        "cvcotm",
        "undertale",
        "sotn",
        "terraria"
    ],
    "unstable platforms": [
        "sly1",
        "doom_ii",
        "metroidprime",
        "cv64",
        "sms",
        "cvcotm",
        "sm_map_rando",
        "tmc",
        "zelda2",
        "sm",
        "v6",
        "oribf",
        "dkc"
    ],
    "unstable": [
        "sly1",
        "doom_ii",
        "metroidprime",
        "cv64",
        "sms",
        "cvcotm",
        "sm_map_rando",
        "tmc",
        "zelda2",
        "sm",
        "v6",
        "oribf",
        "dkc"
    ],
    "melee": [
        "heretic",
        "doom_ii",
        "kdl3",
        "cv64",
        "pokemon_crystal",
        "sotn",
        "dark_souls_2",
        "quake",
        "ffta",
        "metroidfusion",
        "lego_star_wars_tcs",
        "k64",
        "sly1",
        "tmc",
        "cvcotm",
        "papermario",
        "pokemon_emerald",
        "terraria",
        "kh1",
        "wl4",
        "gstla",
        "doom_1993",
        "tunic"
    ],
    "instant kill": [
        "mm2",
        "dkc2",
        "cv64",
        "metroidfusion",
        "v6",
        "dkc"
    ],
    "instant": [
        "mm2",
        "dkc2",
        "cv64",
        "metroidfusion",
        "v6",
        "dkc"
    ],
    "kill": [
        "mm2",
        "dkc2",
        "cv64",
        "metroidfusion",
        "v6",
        "dkc"
    ],
    "difficulty level": [
        "mm2",
        "minecraft",
        "osu",
        "star_fox_64",
        "metroidprime",
        "doom_ii",
        "cv64",
        "musedash",
        "mzm",
        "mk64"
    ],
    "difficulty": [
        "mm2",
        "minecraft",
        "osu",
        "star_fox_64",
        "metroidprime",
        "doom_ii",
        "cv64",
        "musedash",
        "mzm",
        "mk64"
    ],
    "level": [
        "mm2",
        "minecraft",
        "dkc2",
        "osu",
        "star_fox_64",
        "doom_ii",
        "metroidprime",
        "cv64",
        "sms",
        "musedash",
        "mzm",
        "mk64",
        "oot",
        "kh1",
        "dkc"
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
        "wl4",
        "yugiohddm",
        "gstla",
        "pokemon_emerald",
        "mmbn3",
        "tmc",
        "cvcotm",
        "metroidfusion",
        "ffta",
        "earthbound",
        "pokemon_frlg",
        "yugioh06",
        "mzm",
        "mlss"
    ],
    "boy": [
        "pokemon_rb",
        "pokemon_crystal",
        "mmbn3",
        "mzm",
        "yugiohddm",
        "ffta",
        "metroidfusion",
        "mlss",
        "mm2",
        "wl",
        "tmc",
        "cvcotm",
        "pokemon_emerald",
        "tloz_oos",
        "marioland2",
        "wl4",
        "ladx",
        "gstla",
        "yugioh06",
        "earthbound",
        "tloz_ooa",
        "pokemon_frlg"
    ],
    "advance": [
        "wl4",
        "yugiohddm",
        "gstla",
        "pokemon_emerald",
        "mmbn3",
        "tmc",
        "cvcotm",
        "metroidfusion",
        "ffta",
        "earthbound",
        "pokemon_frlg",
        "yugioh06",
        "mzm",
        "mlss"
    ],
    "gravity": [
        "dkc2",
        "dkc3",
        "mzm",
        "metroidprime",
        "star_fox_64",
        "cvcotm",
        "papermario",
        "metroidfusion",
        "sotn",
        "v6",
        "lego_star_wars_tcs",
        "oot",
        "dk64",
        "dkc"
    ],
    "leveling up": [
        "gstla",
        "pokemon_crystal",
        "poe",
        "cvcotm",
        "landstalker",
        "undertale",
        "papermario",
        "sotn",
        "zelda2",
        "earthbound",
        "dw1",
        "pokemon_emerald",
        "dark_souls_2",
        "kh1"
    ],
    "leveling": [
        "gstla",
        "pokemon_crystal",
        "poe",
        "cvcotm",
        "landstalker",
        "undertale",
        "papermario",
        "sotn",
        "zelda2",
        "earthbound",
        "dw1",
        "pokemon_emerald",
        "dark_souls_2",
        "kh1"
    ],
    "dark souls ii": [
        "dark_souls_2"
    ],
    "dark": [
        "dark_souls_3",
        "dark_souls_2",
        "dsr"
    ],
    "souls": [
        "dark_souls_3",
        "dark_souls_2"
    ],
    "ii": [
        "mm2",
        "spire",
        "kh2",
        "ff4fe",
        "dark_souls_2"
    ],
    "xbox 360": [
        "dlcquest",
        "sotn",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "sa2b",
        "sadx"
    ],
    "360": [
        "dlcquest",
        "sotn",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "sa2b",
        "sadx"
    ],
    "spider": [
        "minecraft",
        "dkc2",
        "sly1",
        "zelda2",
        "dark_souls_2",
        "oribf"
    ],
    "customizable characters": [
        "dark_souls_3",
        "lego_star_wars_tcs",
        "xenobladex",
        "dark_souls_2",
        "terraria",
        "stardew_valley"
    ],
    "customizable": [
        "dark_souls_3",
        "lego_star_wars_tcs",
        "xenobladex",
        "dark_souls_2",
        "terraria",
        "stardew_valley"
    ],
    "checkpoints": [
        "mm2",
        "sonic_heroes",
        "mm3",
        "dkc2",
        "dkc3",
        "sly1",
        "jakanddaxter",
        "mmx3",
        "v6",
        "dark_souls_2",
        "smo",
        "dkc"
    ],
    "fire manipulation": [
        "minecraft",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "rogue_legacy",
        "pokemon_emerald",
        "dark_souls_2"
    ],
    "fire": [
        "minecraft",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "rogue_legacy",
        "pokemon_emerald",
        "dark_souls_2"
    ],
    "manipulation": [
        "minecraft",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "rogue_legacy",
        "pokemon_emerald",
        "dark_souls_2"
    ],
    "dark souls iii": [
        "dark_souls_3"
    ],
    "iii": [
        "dark_souls_3",
        "zillion"
    ],
    "diddy kong racing": [
        "diddy_kong_racing"
    ],
    "diddy": [
        "diddy_kong_racing"
    ],
    "kong": [
        "diddy_kong_racing",
        "dkc3",
        "dkc2",
        "dk64",
        "dkc"
    ],
    "racing": [
        "diddy_kong_racing",
        "jakanddaxter",
        "simpsonshitnrun",
        "mk64",
        "swr",
        "trackmania",
        "mario_kart_double_dash"
    ],
    "behind the waterfall": [
        "diddy_kong_racing",
        "gstla",
        "dkc3",
        "hcniko",
        "tmc",
        "sotn",
        "tloz_ooa",
        "ss",
        "smo"
    ],
    "behind": [
        "diddy_kong_racing",
        "gstla",
        "dkc3",
        "hcniko",
        "tmc",
        "sotn",
        "tloz_ooa",
        "ss",
        "smo"
    ],
    "waterfall": [
        "diddy_kong_racing",
        "gstla",
        "dkc3",
        "hcniko",
        "tmc",
        "sotn",
        "tloz_ooa",
        "ss",
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
        "star_fox_64",
        "sly1",
        "jakanddaxter",
        "metroidprime",
        "doom_ii",
        "mk64",
        "dk64"
    ],
    "artificial": [
        "star_fox_64",
        "sly1",
        "jakanddaxter",
        "metroidprime",
        "doom_ii",
        "mk64",
        "dk64"
    ],
    "intelligence": [
        "star_fox_64",
        "sly1",
        "jakanddaxter",
        "metroidprime",
        "doom_ii",
        "mk64",
        "dk64"
    ],
    "completion percentage": [
        "dkc2",
        "metroidprime",
        "metroidfusion",
        "sotn",
        "mzm",
        "dk64"
    ],
    "completion": [
        "dkc2",
        "metroidprime",
        "metroidfusion",
        "sotn",
        "mzm",
        "dk64"
    ],
    "percentage": [
        "dkc2",
        "metroidprime",
        "metroidfusion",
        "sotn",
        "mzm",
        "dk64"
    ],
    "invisibility": [
        "quake",
        "sly1",
        "doom_ii",
        "doom_1993",
        "papermario",
        "dk64"
    ],
    "foreshadowing": [
        "sms",
        "metroidprime",
        "tmc",
        "metroidfusion",
        "mzm",
        "dk64"
    ],
    "donkey kong country": [
        "dkc"
    ],
    "country": [
        "dkc2",
        "dkc3",
        "dkc"
    ],
    "overworld": [
        "tloz",
        "dkc2",
        "dkc3",
        "gstla",
        "ffta",
        "zelda2",
        "ffmq",
        "dkc"
    ],
    "bonus stage": [
        "sonic_heroes",
        "spyro3",
        "dkc2",
        "dkc3",
        "smw",
        "dkc"
    ],
    "bonus": [
        "sonic_heroes",
        "spyro3",
        "dkc2",
        "dkc3",
        "smw",
        "dkc"
    ],
    "water level": [
        "mm2",
        "dkc2",
        "sms",
        "oot",
        "kh1",
        "dkc"
    ],
    "water": [
        "mm2",
        "dkc2",
        "sms",
        "oot",
        "kh1",
        "dkc"
    ],
    "speedrun": [
        "quake",
        "metroidprime",
        "metroidfusion",
        "sotn",
        "sm64ex",
        "sm64hacks",
        "dkc"
    ],
    "donkey kong country 2": [
        "dkc2"
    ],
    "donkey kong country 2: diddy's kong quest": [
        "dkc2"
    ],
    "2:": [
        "dkc2",
        "sa2b",
        "yoshisisland",
        "marioland2",
        "huniepop2"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "dkc2",
        "sly1",
        "sms",
        "jakanddaxter",
        "tmc",
        "shorthike",
        "tloz_ooa",
        "tloz_oos",
        "terraria"
    ],
    "game reference": [
        "spyro3",
        "dkc2",
        "hcniko",
        "doom_ii",
        "witness",
        "tmc",
        "rogue_legacy",
        "oot"
    ],
    "reference": [
        "spyro3",
        "placidplasticducksim",
        "dkc2",
        "hcniko",
        "doom_ii",
        "witness",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy",
        "oot"
    ],
    "sprinting mechanics": [
        "wl4",
        "dkc2",
        "pokemon_crystal",
        "sms",
        "sm64ex",
        "mm_recomp",
        "soe",
        "pokemon_emerald",
        "oot",
        "sm64hacks"
    ],
    "sprinting": [
        "wl4",
        "dkc2",
        "pokemon_crystal",
        "sms",
        "sm64ex",
        "mm_recomp",
        "soe",
        "pokemon_emerald",
        "oot",
        "sm64hacks"
    ],
    "mechanics": [
        "wl4",
        "dkc2",
        "pokemon_crystal",
        "sms",
        "sm64ex",
        "mm_recomp",
        "soe",
        "pokemon_emerald",
        "oot",
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
        "dkc3",
        "huniepop2"
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
        "minecraft",
        "timespinner",
        "dlcquest",
        "ufo50",
        "v6",
        "terraria",
        "smo",
        "stardew_valley"
    ],
    "deliberately": [
        "minecraft",
        "timespinner",
        "dlcquest",
        "ufo50",
        "v6",
        "terraria",
        "smo",
        "stardew_valley"
    ],
    "punctuation mark above head": [
        "pokemon_crystal",
        "tmc",
        "simpsonshitnrun",
        "dlcquest",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "punctuation": [
        "pokemon_crystal",
        "tmc",
        "simpsonshitnrun",
        "dlcquest",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "mark": [
        "pokemon_crystal",
        "tmc",
        "simpsonshitnrun",
        "dlcquest",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "above": [
        "pokemon_crystal",
        "tmc",
        "simpsonshitnrun",
        "dlcquest",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "head": [
        "pokemon_crystal",
        "tmc",
        "simpsonshitnrun",
        "dlcquest",
        "rogue_legacy",
        "tloz_ooa",
        "pokemon_emerald"
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
        "minecraft",
        "seaofthieves",
        "stardew_valley",
        "factorio",
        "satisfactory",
        "raft",
        "dontstarvetogether",
        "terraria",
        "factorio_saws"
    ],
    "funny": [
        "getting_over_it",
        "shorthike",
        "undertale",
        "sims4",
        "dontstarvetogether",
        "powerwashsimulator",
        "huniepop2"
    ],
    "doom 1993": [
        "doom_1993"
    ],
    "doom": [
        "doom_1993",
        "doom_ii"
    ],
    "windows mobile": [
        "doom_1993"
    ],
    "windows": [
        "terraria",
        "doom_1993"
    ],
    "mobile": [
        "quake",
        "doom_1993",
        "mmx3"
    ],
    "pc-9800 series": [
        "doom_1993",
        "doom_ii"
    ],
    "pc-9800": [
        "doom_1993",
        "doom_ii"
    ],
    "dos": [
        "quake",
        "heretic",
        "doom_ii",
        "tyrian",
        "doom_1993"
    ],
    "doom ii": [
        "doom_ii"
    ],
    "doom ii: hell on earth": [
        "doom_ii"
    ],
    "ii:": [
        "sc2",
        "zelda2",
        "lufia2ac",
        "doom_ii"
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
        "placidplasticducksim",
        "doom_ii",
        "witness",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "pop": [
        "placidplasticducksim",
        "doom_ii",
        "witness",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "culture": [
        "placidplasticducksim",
        "doom_ii",
        "witness",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "stat tracking": [
        "osu",
        "doom_ii",
        "witness",
        "simpsonshitnrun",
        "ffta",
        "rogue_legacy",
        "kh1"
    ],
    "stat": [
        "osu",
        "doom_ii",
        "witness",
        "simpsonshitnrun",
        "ffta",
        "rogue_legacy",
        "kh1"
    ],
    "tracking": [
        "osu",
        "doom_ii",
        "witness",
        "simpsonshitnrun",
        "ffta",
        "rogue_legacy",
        "kh1"
    ],
    "rock music": [
        "sonic_heroes",
        "gstla",
        "doom_ii",
        "ultrakill",
        "ffta",
        "sotn",
        "ffmq"
    ],
    "rock": [
        "sonic_heroes",
        "gstla",
        "doom_ii",
        "ultrakill",
        "ffta",
        "sotn",
        "ffmq"
    ],
    "sequence breaking": [
        "wl4",
        "metroidprime",
        "doom_ii",
        "sm_map_rando",
        "tmc",
        "sotn",
        "tloz_ooa",
        "mzm",
        "oot",
        "sm"
    ],
    "sequence": [
        "wl4",
        "metroidprime",
        "doom_ii",
        "sm_map_rando",
        "tmc",
        "sotn",
        "tloz_ooa",
        "mzm",
        "oot",
        "sm"
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
        "sonic_heroes",
        "metroidprime",
        "sms",
        "simpsonshitnrun",
        "tww",
        "dw1",
        "mario_kart_double_dash",
        "luigismansion"
    ],
    "gamecube": [
        "sonic_heroes",
        "metroidprime",
        "sms",
        "simpsonshitnrun",
        "tww",
        "dw1",
        "mario_kart_double_dash",
        "luigismansion"
    ],
    "playstation 2": [
        "sonic_heroes",
        "sly1",
        "jakanddaxter",
        "simpsonshitnrun",
        "rac2",
        "kh2",
        "dw1",
        "kh1"
    ],
    "earthbound": [
        "earthbound"
    ],
    "party system": [
        "gstla",
        "pokemon_crystal",
        "papermario",
        "ffta",
        "earthbound",
        "pokemon_emerald",
        "xenobladex",
        "ffmq",
        "kh1",
        "mlss"
    ],
    "party": [
        "placidplasticducksim",
        "gstla",
        "pokemon_crystal",
        "xenobladex",
        "papermario",
        "ffta",
        "earthbound",
        "pokemon_emerald",
        "mk64",
        "ffmq",
        "overcooked2",
        "kh1",
        "mlss"
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
        "factorio_saws"
    ],
    "faxanadu": [
        "faxanadu"
    ],
    "family computer": [
        "ff1",
        "tloz",
        "mm3",
        "faxanadu"
    ],
    "family": [
        "tloz",
        "mm3",
        "faxanadu",
        "zelda2",
        "ff1"
    ],
    "computer": [
        "tloz",
        "mm3",
        "faxanadu",
        "zelda2",
        "ff1"
    ],
    "nintendo entertainment system": [
        "tloz",
        "mm3",
        "faxanadu",
        "zelda2",
        "ff1"
    ],
    "final fantasy": [
        "ff1"
    ],
    "final": [
        "ff1",
        "ff4fe",
        "ffmq",
        "ffta"
    ],
    "kids": [
        "pokemon_rb",
        "minecraft",
        "placidplasticducksim",
        "pokemon_crystal",
        "pokemon_emerald",
        "mk64",
        "lego_star_wars_tcs",
        "ff1",
        "pmd_eos",
        "mario_kart_double_dash",
        "tetrisattack",
        "overcooked2",
        "yoshisisland",
        "pokemon_frlg"
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
        "placidplasticducksim",
        "getting_over_it",
        "shorthike",
        "musedash",
        "sims4",
        "ffmq"
    ],
    "final fantasy tactics advance": [
        "ffta"
    ],
    "tactics": [
        "ffta"
    ],
    "flipwitch forbidden sex hex": [
        "flipwitch"
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
        "marioland2",
        "gstla"
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
    "stylized": [
        "hcniko",
        "shorthike",
        "hades",
        "ultrakill",
        "hylics2",
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
        "ladx",
        "hcniko",
        "shorthike",
        "terraria",
        "stardew_valley"
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
    "hunie pop": [
        "huniepop"
    ],
    "huniepop": [
        "huniepop",
        "huniepop2"
    ],
    "visual novel": [
        "huniepop",
        "huniepop2"
    ],
    "visual": [
        "huniepop",
        "huniepop2"
    ],
    "novel": [
        "huniepop",
        "huniepop2"
    ],
    "erotic": [
        "huniepop",
        "huniepop2"
    ],
    "romance": [
        "huniepop",
        "stardew_valley",
        "sims4",
        "huniepop2"
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
        "mmx3",
        "quake",
        "rogue_legacy",
        "jakanddaxter"
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
        "kdl3",
        "marioland2",
        "wl4",
        "wl"
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
        "ladx",
        "sadx"
    ],
    "game boy color": [
        "tloz_oos",
        "tloz_ooa",
        "ladx",
        "pokemon_crystal"
    ],
    "color": [
        "tloz_oos",
        "tloz_ooa",
        "ladx",
        "pokemon_crystal"
    ],
    "tentacles": [
        "ladx",
        "pokemon_crystal",
        "metroidprime",
        "sms",
        "papermario",
        "pokemon_emerald",
        "mlss"
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
        "quake",
        "zillion",
        "landstalker"
    ],
    "mega": [
        "mm2",
        "mm3",
        "mmbn3",
        "landstalker",
        "mmx3",
        "megamix"
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
        "star_fox_64",
        "swr",
        "lego_star_wars_tcs"
    ],
    "wars:": [
        "swr",
        "lego_star_wars_tcs"
    ],
    "complete": [
        "lego_star_wars_tcs"
    ],
    "saga": [
        "mlss",
        "lego_star_wars_tcs"
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
    "super mario land 2": [
        "marioland2"
    ],
    "super mario land 2: 6 golden coins": [
        "marioland2"
    ],
    "mario": [
        "sm64hacks",
        "sms",
        "wl",
        "mk64",
        "papermario",
        "smw",
        "smo",
        "sm64ex",
        "mario_kart_double_dash",
        "marioland2",
        "yoshisisland",
        "mlss"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "mm2",
        "pokemon_rb",
        "marioland2",
        "wl"
    ],
    "turtle": [
        "sly1",
        "sms",
        "papermario",
        "mk64",
        "marioland2",
        "mlss"
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
        "metroidprime",
        "sm_map_rando",
        "smz3",
        "metroidfusion",
        "sm"
    ],
    "fusion": [
        "metroidfusion"
    ],
    "time limit": [
        "wl4",
        "metroidprime",
        "sms",
        "witness",
        "sm_map_rando",
        "simpsonshitnrun",
        "shorthike",
        "tloz_ph",
        "ror1",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "sm"
    ],
    "limit": [
        "wl4",
        "metroidprime",
        "sms",
        "witness",
        "sm_map_rando",
        "simpsonshitnrun",
        "shorthike",
        "tloz_ph",
        "ror1",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "sm"
    ],
    "countdown timer": [
        "wl4",
        "metroidprime",
        "sm_map_rando",
        "simpsonshitnrun",
        "tloz_ph",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "mzm",
        "oot",
        "sm"
    ],
    "countdown": [
        "wl4",
        "metroidprime",
        "sm_map_rando",
        "simpsonshitnrun",
        "tloz_ph",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "mzm",
        "oot",
        "sm"
    ],
    "timer": [
        "wl4",
        "metroidprime",
        "sm_map_rando",
        "simpsonshitnrun",
        "tloz_ph",
        "tmc",
        "metroidfusion",
        "rogue_legacy",
        "mzm",
        "oot",
        "sm"
    ],
    "isolation": [
        "metroidprime",
        "sm_map_rando",
        "metroidfusion",
        "sotn",
        "mzm",
        "sm"
    ],
    "metroid prime": [
        "metroidprime"
    ],
    "prime": [
        "metroidprime"
    ],
    "auto-aim": [
        "quake",
        "metroidprime",
        "mm_recomp",
        "tww",
        "ss",
        "oot"
    ],
    "meme origin": [
        "minecraft",
        "tloz",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "zelda2"
    ],
    "meme": [
        "minecraft",
        "tloz",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "zelda2"
    ],
    "origin": [
        "minecraft",
        "tloz",
        "star_fox_64",
        "metroidprime",
        "mm_recomp",
        "sotn",
        "zelda2"
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
        "mm2",
        "mm3",
        "mmbn3",
        "mmx3"
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
        "mmbn3",
        "sa2b"
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
        "quake",
        "mmx3"
    ],
    "device": [
        "quake",
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
        "openrct2",
        "stardew_valley",
        "powerwashsimulator"
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
        "sm_map_rando",
        "oribf",
        "sm"
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
    "nintendo switch 2": [
        "smo",
        "stardew_valley",
        "overcooked2"
    ],
    "paper mario": [
        "papermario"
    ],
    "paper": [
        "papermario",
        "ttyd"
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
        "pokemon_frlg",
        "pokemon_crystal",
        "pokemon_emerald"
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
        "timespinner",
        "ror1",
        "undertale",
        "rogue_legacy",
        "v6",
        "terraria",
        "stardew_valley"
    ],
    "vita": [
        "timespinner",
        "ror1",
        "undertale",
        "rogue_legacy",
        "v6",
        "terraria",
        "stardew_valley"
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
    "run": [
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
        "sonic_heroes",
        "tloz_ooa",
        "smo",
        "sm64ex",
        "terraria",
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
    ]
} # type: ignore