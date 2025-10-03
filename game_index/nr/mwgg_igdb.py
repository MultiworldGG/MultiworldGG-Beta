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
        "age_rating": "nr",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "e",
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
        "age_rating": "nr",
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
        "age_rating": "nr",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "nr",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "12",
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
        "age_rating": "16",
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
        "age_rating": "16",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "nr",
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
        "age_rating": "12",
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
        "age_rating": "16",
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
        "age_rating": "16",
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
        "age_rating": "3",
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
        "age_rating": "16",
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
        "age_rating": "e",
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
        "age_rating": "12",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "",
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
        "age_rating": "e",
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
        "age_rating": "nr",
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
        "age_rating": "e",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "m",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "nr",
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
        "age_rating": "nr",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "nr",
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
        "age_rating": "nr",
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
        "age_rating": "e",
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
        "age_rating": "e",
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
        "age_rating": "nr",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "12",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "12",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "16",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "nr",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "18",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "nr",
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
        "age_rating": "t",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "18",
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
        "age_rating": "18",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "e",
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
        "age_rating": "e",
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
        "age_rating": "3",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "t",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "e",
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
        "age_rating": "3",
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
            "playstation 3",
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
            "retroachievements"
        ],
        "release_date": "2003"
    },
    "sotn": {
        "igdb_id": "1128",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co53m8.jpg",
        "game_name": "Symphony of the Night",
        "igdb_name": "castlevania: symphony of the night",
        "age_rating": "12",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "12",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "16",
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
        "age_rating": "12",
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
        "age_rating": "e",
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
        "age_rating": "12",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "nr",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "e",
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
        "age_rating": "18",
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
        "age_rating": "m",
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
        "age_rating": "12",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "7",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "12",
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
        "age_rating": "e",
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
        "age_rating": "3",
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
        "age_rating": "3",
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
        "age_rating": "7",
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
        "age_rating": "nr",
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
        "age_rating": "t",
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
        "metroidprime",
        "rogue_legacy",
        "rac2",
        "osrs",
        "ffmq",
        "luigismansion",
        "albw",
        "messenger",
        "sms",
        "raft",
        "mlss",
        "xenobladex",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "banjo_tooie",
        "ladx",
        "ff4fe",
        "blasphemous",
        "smw",
        "tloz_ooa",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "dark_souls_3",
        "dontstarvetogether",
        "hcniko",
        "adventure",
        "dkc3",
        "cuphead",
        "noita",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "mm3",
        "spyro3",
        "mzm",
        "tloz_ph",
        "pokemon_emerald",
        "v6",
        "dsr",
        "kindergarten_2",
        "metroidfusion",
        "subnautica",
        "terraria",
        "lingo",
        "pokemon_frlg",
        "smo",
        "mm_recomp",
        "k64",
        "ror2",
        "inscryption",
        "tunic",
        "sly1",
        "alttp",
        "hades",
        "enderlilies",
        "sotn",
        "faxanadu",
        "celeste64",
        "zelda2",
        "sm_map_rando",
        "hk",
        "ufo50",
        "mmx3",
        "sadx",
        "sm",
        "jakanddaxter",
        "pokemon_crystal",
        "dk64",
        "tww",
        "momodoramoonlitfarewell",
        "crystal_project",
        "kdl3",
        "shivers",
        "aus",
        "sm64hacks",
        "tloz_oos",
        "crosscode",
        "monster_sanctuary",
        "dw1",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "outer_wilds",
        "cv64",
        "animal_well",
        "kh2",
        "tloz",
        "smz3",
        "stardew_valley",
        "oribf",
        "oot",
        "ff1",
        "ror1",
        "papermario",
        "cvcotm",
        "kh1",
        "tmc",
        "satisfactory",
        "zork_grand_inquisitor",
        "sm64ex",
        "undertale",
        "celeste_open_world",
        "tp",
        "lego_star_wars_tcs",
        "cat_quest",
        "mm2",
        "shorthike",
        "wl4",
        "pokemon_rb",
        "gstla",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "witness",
        "earthbound",
        "sonic_heroes",
        "aquaria",
        "poe",
        "ss"
    ],
    "bird view / isometric": [
        "soe",
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "landstalker",
        "factorio_saws",
        "tloz",
        "mmbn3",
        "smz3",
        "stardew_valley",
        "yugioh06",
        "inscryption",
        "adventure",
        "tunic",
        "wargroove2",
        "cuphead",
        "alttp",
        "ff1",
        "ffmq",
        "hades",
        "meritous",
        "osrs",
        "sims4",
        "hylics2",
        "sc2",
        "albw",
        "diddy_kong_racing",
        "tmc",
        "ufo50",
        "sms",
        "placidplasticducksim",
        "pokemon_crystal",
        "spyro3",
        "undertale",
        "tyrian",
        "ctjot",
        "against_the_storm",
        "crystal_project",
        "ladx",
        "overcooked2",
        "ff4fe",
        "rimworld",
        "shorthike",
        "tloz_ph",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "tloz_oos",
        "gstla",
        "chainedechoes",
        "shapez",
        "tloz_ooa",
        "tboir",
        "yugiohddm",
        "crosscode",
        "earthbound",
        "sonic_heroes",
        "dw1",
        "poe",
        "brotato",
        "factorio"
    ],
    "bird": [
        "soe",
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "landstalker",
        "factorio_saws",
        "tloz",
        "mmbn3",
        "smz3",
        "stardew_valley",
        "yugioh06",
        "inscryption",
        "adventure",
        "dkc3",
        "rogue_legacy",
        "tunic",
        "wargroove2",
        "cuphead",
        "alttp",
        "ff1",
        "ffmq",
        "hades",
        "meritous",
        "osrs",
        "sims4",
        "hylics2",
        "sc2",
        "albw",
        "diddy_kong_racing",
        "tmc",
        "ufo50",
        "sms",
        "placidplasticducksim",
        "pokemon_crystal",
        "spyro3",
        "undertale",
        "tyrian",
        "ctjot",
        "against_the_storm",
        "banjo_tooie",
        "crystal_project",
        "ladx",
        "overcooked2",
        "ff4fe",
        "rimworld",
        "shorthike",
        "tloz_ph",
        "balatro",
        "aus",
        "ffta",
        "pokemon_emerald",
        "pokemon_rb",
        "gstla",
        "chainedechoes",
        "shapez",
        "tloz_ooa",
        "tboir",
        "tloz_oos",
        "crosscode",
        "yugiohddm",
        "earthbound",
        "sonic_heroes",
        "dw1",
        "minecraft",
        "poe",
        "brotato",
        "factorio"
    ],
    "view": [
        "factorio_saws",
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "ffmq",
        "sc2",
        "albw",
        "messenger",
        "sms",
        "mlss",
        "musedash",
        "getting_over_it",
        "ctjot",
        "against_the_storm",
        "ladx",
        "ff4fe",
        "blasphemous",
        "yugiohddm",
        "smw",
        "tloz_ooa",
        "shapez",
        "factorio",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "adventure",
        "dkc3",
        "cuphead",
        "meritous",
        "sims4",
        "noita",
        "hylics2",
        "mm3",
        "spyro3",
        "tyrian",
        "megamix",
        "mzm",
        "tloz_ph",
        "rimworld",
        "balatro",
        "pokemon_emerald",
        "wl",
        "v6",
        "metroidfusion",
        "brotato",
        "terraria",
        "soe",
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dkc",
        "k64",
        "yugioh06",
        "inscryption",
        "tunic",
        "alttp",
        "hades",
        "enderlilies",
        "sotn",
        "faxanadu",
        "zelda2",
        "sm_map_rando",
        "diddy_kong_racing",
        "hk",
        "ufo50",
        "tetrisattack",
        "zillion",
        "mmx3",
        "sm",
        "placidplasticducksim",
        "pokemon_crystal",
        "momodoramoonlitfarewell",
        "crystal_project",
        "kdl3",
        "aus",
        "tloz_oos",
        "ffta",
        "crosscode",
        "monster_sanctuary",
        "dw1",
        "celeste",
        "dlcquest",
        "yoshisisland",
        "landstalker",
        "animal_well",
        "tloz",
        "mmbn3",
        "smz3",
        "stardew_valley",
        "oribf",
        "ff1",
        "ror1",
        "papermario",
        "lufia2ac",
        "dkc2",
        "cvcotm",
        "tmc",
        "undertale",
        "celeste_open_world",
        "marioland2",
        "mm2",
        "overcooked2",
        "shorthike",
        "wl4",
        "pokemon_rb",
        "gstla",
        "chainedechoes",
        "tboir",
        "timespinner",
        "earthbound",
        "sonic_heroes",
        "aquaria",
        "poe",
        "spire"
    ],
    "/": [
        "soe",
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "landstalker",
        "factorio_saws",
        "tloz",
        "mmbn3",
        "smz3",
        "stardew_valley",
        "yugioh06",
        "inscryption",
        "adventure",
        "tunic",
        "wargroove2",
        "cuphead",
        "alttp",
        "ff1",
        "ffmq",
        "hades",
        "meritous",
        "osrs",
        "sims4",
        "hylics2",
        "sc2",
        "albw",
        "diddy_kong_racing",
        "tmc",
        "ufo50",
        "sms",
        "placidplasticducksim",
        "pokemon_crystal",
        "spyro3",
        "undertale",
        "tyrian",
        "ctjot",
        "against_the_storm",
        "crystal_project",
        "ladx",
        "overcooked2",
        "ff4fe",
        "rimworld",
        "shorthike",
        "tloz_ph",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "tloz_oos",
        "gstla",
        "chainedechoes",
        "shapez",
        "tloz_ooa",
        "tboir",
        "yugiohddm",
        "crosscode",
        "earthbound",
        "sonic_heroes",
        "dw1",
        "poe",
        "brotato",
        "factorio"
    ],
    "isometric": [
        "soe",
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "landstalker",
        "factorio_saws",
        "tloz",
        "mmbn3",
        "smz3",
        "stardew_valley",
        "yugioh06",
        "inscryption",
        "adventure",
        "tunic",
        "wargroove2",
        "cuphead",
        "alttp",
        "ff1",
        "ffmq",
        "hades",
        "meritous",
        "osrs",
        "sims4",
        "hylics2",
        "sc2",
        "albw",
        "diddy_kong_racing",
        "tmc",
        "ufo50",
        "sms",
        "placidplasticducksim",
        "pokemon_crystal",
        "spyro3",
        "undertale",
        "tyrian",
        "ctjot",
        "against_the_storm",
        "crystal_project",
        "ladx",
        "overcooked2",
        "ff4fe",
        "rimworld",
        "shorthike",
        "tloz_ph",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "tloz_oos",
        "gstla",
        "chainedechoes",
        "shapez",
        "tloz_ooa",
        "tboir",
        "yugiohddm",
        "crosscode",
        "earthbound",
        "sonic_heroes",
        "dw1",
        "poe",
        "brotato",
        "factorio"
    ],
    "fantasy": [
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "ffmq",
        "albw",
        "heretic",
        "mlss",
        "ctjot",
        "against_the_storm",
        "banjo_tooie",
        "frogmonster",
        "ladx",
        "ff4fe",
        "blasphemous",
        "yugiohddm",
        "smw",
        "pseudoregalia",
        "minecraft",
        "dark_souls_2",
        "dark_souls_3",
        "pmd_eos",
        "civ_6",
        "adventure",
        "cuphead",
        "sims4",
        "noita",
        "hylics2",
        "ahit",
        "tloz_ph",
        "huniepop",
        "pokemon_emerald",
        "v6",
        "dsr",
        "terraria",
        "pokemon_frlg",
        "wargroove",
        "smo",
        "mm_recomp",
        "yugioh06",
        "tunic",
        "alttp",
        "hades",
        "enderlilies",
        "faxanadu",
        "zelda2",
        "hk",
        "pokemon_crystal",
        "tww",
        "crystal_project",
        "tloz_oos",
        "sm64hacks",
        "ffta",
        "monster_sanctuary",
        "seaofthieves",
        "celeste",
        "yoshisisland",
        "landstalker",
        "kh2",
        "tloz",
        "stardew_valley",
        "oribf",
        "oot",
        "ff1",
        "fm",
        "ror1",
        "papermario",
        "lufia2ac",
        "dkc2",
        "kh1",
        "tmc",
        "zork_grand_inquisitor",
        "sm64ex",
        "undertale",
        "celeste_open_world",
        "tp",
        "cat_quest",
        "shorthike",
        "ultrakill",
        "pokemon_rb",
        "lunacid",
        "gstla",
        "chainedechoes",
        "timespinner",
        "earthbound",
        "aquaria",
        "poe",
        "ss",
        "spire"
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
        "soe",
        "dkc",
        "yoshisisland",
        "tloz",
        "smz3",
        "adventure",
        "dkc3",
        "alttp",
        "ff1",
        "ffmq",
        "papermario",
        "faxanadu",
        "lufia2ac",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "kh1",
        "tetrisattack",
        "mmx3",
        "sm",
        "mlss",
        "xenobladex",
        "mm3",
        "pokemon_crystal",
        "ff4fe",
        "kdl3",
        "ffta",
        "pokemon_emerald",
        "gstla",
        "smw",
        "earthbound"
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
        "dkc",
        "mm_recomp",
        "hcniko",
        "smo",
        "k64",
        "tloz",
        "smz3",
        "oribf",
        "dkc3",
        "oot",
        "rogue_legacy",
        "sly1",
        "alttp",
        "hades",
        "sims4",
        "enderlilies",
        "papermario",
        "lufia2ac",
        "celeste64",
        "sotn",
        "dkc2",
        "zelda2",
        "albw",
        "diddy_kong_racing",
        "cvcotm",
        "tmc",
        "messenger",
        "simpsonshitnrun",
        "jakanddaxter",
        "mlss",
        "spyro3",
        "undertale",
        "doom_ii",
        "tp",
        "tww",
        "ttyd",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "against_the_storm",
        "ladx",
        "overcooked2",
        "tloz_ph",
        "blasphemous",
        "tloz_oos",
        "ffta",
        "gstla",
        "tloz_ooa",
        "tboir",
        "witness",
        "earthbound",
        "seaofthieves",
        "dark_souls_2",
        "metroidfusion",
        "terraria",
        "ss",
        "spire"
    ],
    "storm": [
        "against_the_storm"
    ],
    "real time strategy (rts)": [
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3",
        "rimworld"
    ],
    "real": [
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3",
        "rimworld"
    ],
    "time": [
        "openrct2",
        "mk64",
        "mm_recomp",
        "metroidprime",
        "pmd_eos",
        "mmbn3",
        "rogue_legacy",
        "oot",
        "sly1",
        "alttp",
        "ror1",
        "sc2",
        "sm_map_rando",
        "diddy_kong_racing",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "sm",
        "jakanddaxter",
        "ahit",
        "pokemon_crystal",
        "spyro3",
        "ctjot",
        "apeescape",
        "against_the_storm",
        "tloz_ph",
        "rimworld",
        "shorthike",
        "tloz_oos",
        "wl4",
        "ffta",
        "pokemon_emerald",
        "tloz_ooa",
        "timespinner",
        "witness",
        "earthbound",
        "v6",
        "metroidfusion",
        "outer_wilds"
    ],
    "strategy": [
        "openrct2",
        "pokemon_frlg",
        "wargroove",
        "dontstarvetogether",
        "pmd_eos",
        "civ_6",
        "factorio_saws",
        "mmbn3",
        "stardew_valley",
        "yugioh06",
        "inscryption",
        "wargroove2",
        "fm",
        "hylics2",
        "sc2",
        "ufo50",
        "satisfactory",
        "undertale",
        "huniepop2",
        "crystal_project",
        "against_the_storm",
        "overcooked2",
        "huniepop",
        "rimworld",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "chainedechoes",
        "shapez",
        "earthbound",
        "monster_sanctuary",
        "factorio",
        "terraria",
        "spire"
    ],
    "(rts)": [
        "openrct2",
        "sc2",
        "against_the_storm",
        "mmbn3",
        "rimworld"
    ],
    "simulator": [
        "openrct2",
        "doronko_wanko",
        "dontstarvetogether",
        "civ_6",
        "factorio_saws",
        "stardew_valley",
        "sims4",
        "noita",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "getting_over_it",
        "huniepop2",
        "against_the_storm",
        "overcooked2",
        "huniepop",
        "rimworld",
        "shapez",
        "minecraft",
        "powerwashsimulator",
        "seaofthieves",
        "factorio",
        "terraria",
        "outer_wilds"
    ],
    "indie": [
        "openrct2",
        "wargroove",
        "dontstarvetogether",
        "hcniko",
        "ror2",
        "animal_well",
        "factorio_saws",
        "osu",
        "stardew_valley",
        "inscryption",
        "terraria",
        "rogue_legacy",
        "tunic",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "enderlilies",
        "noita",
        "ror1",
        "celeste64",
        "hylics2",
        "lethal_company",
        "bomb_rush_cyberfunk",
        "hk",
        "ufo50",
        "messenger",
        "satisfactory",
        "raft",
        "ahit",
        "peaks_of_yore",
        "musedash",
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "huniepop2",
        "frogmonster",
        "against_the_storm",
        "cat_quest",
        "crystal_project",
        "momodoramoonlitfarewell",
        "overcooked2",
        "shivers",
        "blasphemous",
        "huniepop",
        "rimworld",
        "shorthike",
        "balatro",
        "aus",
        "lunacid",
        "ultrakill",
        "chainedechoes",
        "shapez",
        "tboir",
        "timespinner",
        "crosscode",
        "witness",
        "v6",
        "pseudoregalia",
        "aquaria",
        "monster_sanctuary",
        "outer_wilds",
        "kindergarten_2",
        "powerwashsimulator",
        "brotato",
        "factorio",
        "subnautica",
        "dlcquest",
        "lingo",
        "spire"
    ],
    "xbox series x|s": [
        "ror2",
        "animal_well",
        "inscryption",
        "tunic",
        "wargroove2",
        "hades",
        "enderlilies",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "trackmania",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "balatro",
        "residentevil3remake",
        "residentevil2remake",
        "powerwashsimulator",
        "seaofthieves",
        "brotato",
        "subnautica",
        "outer_wilds"
    ],
    "xbox": [
        "wargroove",
        "ror2",
        "animal_well",
        "stardew_valley",
        "oribf",
        "inscryption",
        "terraria",
        "rogue_legacy",
        "tunic",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "sims4",
        "enderlilies",
        "ror1",
        "sotn",
        "bomb_rush_cyberfunk",
        "hk",
        "messenger",
        "satisfactory",
        "simpsonshitnrun",
        "sadx",
        "raft",
        "swr",
        "ahit",
        "placidplasticducksim",
        "sa2b",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "against_the_storm",
        "momodoramoonlitfarewell",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "witness",
        "dsr",
        "sonic_heroes",
        "monster_sanctuary",
        "dw1",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "dark_souls_2",
        "poe",
        "brotato",
        "seaofthieves",
        "subnautica",
        "dlcquest",
        "dark_souls_3"
    ],
    "series": [
        "ror2",
        "animal_well",
        "inscryption",
        "tunic",
        "wargroove2",
        "hades",
        "enderlilies",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "trackmania",
        "doom_ii",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "doom_1993",
        "balatro",
        "residentevil3remake",
        "residentevil2remake",
        "powerwashsimulator",
        "seaofthieves",
        "brotato",
        "subnautica",
        "outer_wilds"
    ],
    "x|s": [
        "ror2",
        "animal_well",
        "inscryption",
        "tunic",
        "wargroove2",
        "hades",
        "enderlilies",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "trackmania",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "balatro",
        "residentevil3remake",
        "residentevil2remake",
        "powerwashsimulator",
        "seaofthieves",
        "brotato",
        "subnautica",
        "outer_wilds"
    ],
    "pc (microsoft windows)": [
        "factorio_saws",
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "lethal_company",
        "sc2",
        "messenger",
        "raft",
        "heretic",
        "musedash",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "against_the_storm",
        "blasphemous",
        "shapez",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "factorio",
        "dark_souls_3",
        "doronko_wanko",
        "bumpstik",
        "dontstarvetogether",
        "hcniko",
        "civ_6",
        "cuphead",
        "meritous",
        "sims4",
        "noita",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "doom_ii",
        "huniepop2",
        "tyrian",
        "huniepop",
        "rimworld",
        "balatro",
        "v6",
        "dsr",
        "kindergarten_2",
        "gzdoom",
        "brotato",
        "subnautica",
        "terraria",
        "lingo",
        "openrct2",
        "wargroove",
        "ror2",
        "inscryption",
        "tunic",
        "hades",
        "enderlilies",
        "celeste64",
        "hk",
        "ufo50",
        "sadx",
        "swr",
        "placidplasticducksim",
        "momodoramoonlitfarewell",
        "crystal_project",
        "shivers",
        "aus",
        "crosscode",
        "monster_sanctuary",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "osu",
        "outer_wilds",
        "landstalker",
        "animal_well",
        "stardew_valley",
        "toontown",
        "oribf",
        "ror1",
        "satisfactory",
        "zork_grand_inquisitor",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "cat_quest",
        "overcooked2",
        "shorthike",
        "ultrakill",
        "lunacid",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "witness",
        "sonic_heroes",
        "aquaria",
        "powerwashsimulator",
        "poe",
        "spire"
    ],
    "pc": [
        "factorio_saws",
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "lethal_company",
        "sc2",
        "messenger",
        "raft",
        "heretic",
        "musedash",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "against_the_storm",
        "blasphemous",
        "shapez",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "factorio",
        "dark_souls_3",
        "doronko_wanko",
        "bumpstik",
        "dontstarvetogether",
        "hcniko",
        "civ_6",
        "cuphead",
        "meritous",
        "sims4",
        "noita",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "doom_ii",
        "huniepop2",
        "tyrian",
        "huniepop",
        "rimworld",
        "balatro",
        "v6",
        "dsr",
        "kindergarten_2",
        "gzdoom",
        "brotato",
        "subnautica",
        "terraria",
        "lingo",
        "openrct2",
        "wargroove",
        "ror2",
        "inscryption",
        "tunic",
        "hades",
        "enderlilies",
        "celeste64",
        "hk",
        "ufo50",
        "sadx",
        "swr",
        "placidplasticducksim",
        "momodoramoonlitfarewell",
        "crystal_project",
        "shivers",
        "aus",
        "crosscode",
        "monster_sanctuary",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "osu",
        "outer_wilds",
        "landstalker",
        "animal_well",
        "stardew_valley",
        "toontown",
        "oribf",
        "ror1",
        "satisfactory",
        "zork_grand_inquisitor",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "cat_quest",
        "overcooked2",
        "shorthike",
        "ultrakill",
        "lunacid",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "witness",
        "sonic_heroes",
        "aquaria",
        "powerwashsimulator",
        "poe",
        "spire"
    ],
    "(microsoft": [
        "factorio_saws",
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "lethal_company",
        "sc2",
        "messenger",
        "raft",
        "heretic",
        "musedash",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "against_the_storm",
        "blasphemous",
        "shapez",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "factorio",
        "dark_souls_3",
        "doronko_wanko",
        "bumpstik",
        "dontstarvetogether",
        "hcniko",
        "civ_6",
        "cuphead",
        "meritous",
        "sims4",
        "noita",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "doom_ii",
        "huniepop2",
        "tyrian",
        "huniepop",
        "rimworld",
        "balatro",
        "v6",
        "dsr",
        "kindergarten_2",
        "gzdoom",
        "brotato",
        "subnautica",
        "terraria",
        "lingo",
        "openrct2",
        "wargroove",
        "ror2",
        "inscryption",
        "tunic",
        "hades",
        "enderlilies",
        "celeste64",
        "hk",
        "ufo50",
        "sadx",
        "swr",
        "placidplasticducksim",
        "momodoramoonlitfarewell",
        "crystal_project",
        "shivers",
        "aus",
        "crosscode",
        "monster_sanctuary",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "osu",
        "outer_wilds",
        "landstalker",
        "animal_well",
        "stardew_valley",
        "toontown",
        "oribf",
        "ror1",
        "satisfactory",
        "zork_grand_inquisitor",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "cat_quest",
        "overcooked2",
        "shorthike",
        "ultrakill",
        "lunacid",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "witness",
        "sonic_heroes",
        "aquaria",
        "powerwashsimulator",
        "poe",
        "spire"
    ],
    "windows)": [
        "factorio_saws",
        "rogue_legacy",
        "wargroove2",
        "osrs",
        "lethal_company",
        "sc2",
        "messenger",
        "raft",
        "heretic",
        "musedash",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "against_the_storm",
        "blasphemous",
        "shapez",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "factorio",
        "dark_souls_3",
        "doronko_wanko",
        "bumpstik",
        "dontstarvetogether",
        "hcniko",
        "civ_6",
        "cuphead",
        "meritous",
        "sims4",
        "noita",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "doom_ii",
        "huniepop2",
        "tyrian",
        "huniepop",
        "rimworld",
        "balatro",
        "v6",
        "dsr",
        "kindergarten_2",
        "gzdoom",
        "brotato",
        "subnautica",
        "terraria",
        "lingo",
        "openrct2",
        "wargroove",
        "ror2",
        "inscryption",
        "tunic",
        "hades",
        "enderlilies",
        "celeste64",
        "hk",
        "ufo50",
        "sadx",
        "swr",
        "placidplasticducksim",
        "momodoramoonlitfarewell",
        "crystal_project",
        "shivers",
        "aus",
        "crosscode",
        "monster_sanctuary",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "osu",
        "outer_wilds",
        "landstalker",
        "animal_well",
        "stardew_valley",
        "toontown",
        "oribf",
        "ror1",
        "satisfactory",
        "zork_grand_inquisitor",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "cat_quest",
        "overcooked2",
        "shorthike",
        "ultrakill",
        "lunacid",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "witness",
        "sonic_heroes",
        "aquaria",
        "powerwashsimulator",
        "poe",
        "spire"
    ],
    "playstation 5": [
        "ror2",
        "animal_well",
        "inscryption",
        "tunic",
        "hades",
        "bomb_rush_cyberfunk",
        "messenger",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "trackmania",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "balatro",
        "crosscode",
        "residentevil3remake",
        "residentevil2remake",
        "powerwashsimulator",
        "seaofthieves",
        "poe",
        "brotato",
        "subnautica",
        "outer_wilds"
    ],
    "playstation": [
        "wargroove",
        "ror2",
        "animal_well",
        "kh2",
        "stardew_valley",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "sly1",
        "celeste",
        "rac2",
        "cuphead",
        "hades",
        "fm",
        "sims4",
        "enderlilies",
        "ror1",
        "sotn",
        "bomb_rush_cyberfunk",
        "hk",
        "kh1",
        "messenger",
        "satisfactory",
        "simpsonshitnrun",
        "sadx",
        "raft",
        "swr",
        "jakanddaxter",
        "ahit",
        "placidplasticducksim",
        "sa2b",
        "spyro3",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "lego_star_wars_tcs",
        "apeescape",
        "against_the_storm",
        "cat_quest",
        "momodoramoonlitfarewell",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "v6",
        "witness",
        "dsr",
        "sonic_heroes",
        "monster_sanctuary",
        "dw1",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "dark_souls_2",
        "poe",
        "brotato",
        "seaofthieves",
        "subnautica",
        "terraria",
        "dark_souls_3"
    ],
    "5": [
        "ror2",
        "animal_well",
        "inscryption",
        "tunic",
        "hades",
        "bomb_rush_cyberfunk",
        "messenger",
        "satisfactory",
        "raft",
        "placidplasticducksim",
        "trackmania",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "balatro",
        "crosscode",
        "residentevil3remake",
        "residentevil2remake",
        "powerwashsimulator",
        "seaofthieves",
        "poe",
        "brotato",
        "subnautica",
        "outer_wilds"
    ],
    "nintendo switch": [
        "doronko_wanko",
        "wargroove",
        "smo",
        "dontstarvetogether",
        "hcniko",
        "ror2",
        "animal_well",
        "stardew_valley",
        "oribf",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "ufo50",
        "messenger",
        "swr",
        "ahit",
        "placidplasticducksim",
        "musedash",
        "undertale",
        "celeste_open_world",
        "megamix",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "cat_quest",
        "crystal_project",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "tboir",
        "timespinner",
        "crosscode",
        "v6",
        "dsr",
        "monster_sanctuary",
        "powerwashsimulator",
        "brotato",
        "factorio",
        "subnautica",
        "terraria",
        "outer_wilds"
    ],
    "nintendo": [
        "mk64",
        "metroidprime",
        "rogue_legacy",
        "wargroove2",
        "ffmq",
        "luigismansion",
        "albw",
        "messenger",
        "sms",
        "musedash",
        "ctjot",
        "against_the_storm",
        "banjo_tooie",
        "ladx",
        "ff4fe",
        "blasphemous",
        "smw",
        "tloz_ooa",
        "factorio",
        "doronko_wanko",
        "dontstarvetogether",
        "hcniko",
        "pmd_eos",
        "star_fox_64",
        "dkc3",
        "cuphead",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "mm3",
        "megamix",
        "tloz_ph",
        "balatro",
        "wl",
        "v6",
        "dsr",
        "metroidfusion",
        "brotato",
        "subnautica",
        "terraria",
        "soe",
        "wargroove",
        "dkc",
        "mm_recomp",
        "smo",
        "k64",
        "ror2",
        "inscryption",
        "tunic",
        "alttp",
        "hades",
        "enderlilies",
        "faxanadu",
        "zelda2",
        "sm_map_rando",
        "diddy_kong_racing",
        "hk",
        "ufo50",
        "tetrisattack",
        "mmx3",
        "sm",
        "swr",
        "placidplasticducksim",
        "pokemon_crystal",
        "dk64",
        "tww",
        "momodoramoonlitfarewell",
        "crystal_project",
        "kdl3",
        "tloz_oos",
        "sm64hacks",
        "crosscode",
        "monster_sanctuary",
        "dw1",
        "celeste",
        "outer_wilds",
        "cv64",
        "yoshisisland",
        "animal_well",
        "tloz",
        "smz3",
        "stardew_valley",
        "oribf",
        "oot",
        "ff1",
        "ror1",
        "papermario",
        "lufia2ac",
        "dkc2",
        "tmc",
        "sm64ex",
        "undertale",
        "celeste_open_world",
        "marioland2",
        "cat_quest",
        "mm2",
        "overcooked2",
        "shorthike",
        "wl4",
        "pokemon_rb",
        "chainedechoes",
        "tboir",
        "timespinner",
        "earthbound",
        "sonic_heroes",
        "powerwashsimulator",
        "mario_kart_double_dash"
    ],
    "switch": [
        "doronko_wanko",
        "wargroove",
        "smo",
        "dontstarvetogether",
        "hcniko",
        "ror2",
        "animal_well",
        "stardew_valley",
        "oribf",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "ufo50",
        "messenger",
        "swr",
        "ahit",
        "placidplasticducksim",
        "musedash",
        "undertale",
        "celeste_open_world",
        "megamix",
        "momodoramoonlitfarewell",
        "against_the_storm",
        "cat_quest",
        "crystal_project",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "tboir",
        "timespinner",
        "crosscode",
        "v6",
        "dsr",
        "monster_sanctuary",
        "powerwashsimulator",
        "brotato",
        "factorio",
        "subnautica",
        "terraria",
        "outer_wilds"
    ],
    "roguelite": [
        "hades",
        "ror1",
        "noita",
        "ror2",
        "against_the_storm",
        "brotato"
    ],
    "a hat in time": [
        "ahit"
    ],
    "a": [
        "ahit",
        "alttp",
        "albw",
        "smz3",
        "shorthike"
    ],
    "hat": [
        "ahit"
    ],
    "in": [
        "ahit",
        "alttp",
        "smw",
        "tloz_ooa",
        "tloz_ph",
        "papermario",
        "metroidprime",
        "earthbound",
        "zelda2",
        "sm_map_rando",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "oot",
        "tloz_oos"
    ],
    "first person": [
        "cv64",
        "metroidprime",
        "star_fox_64",
        "inscryption",
        "sims4",
        "fm",
        "hylics2",
        "lethal_company",
        "satisfactory",
        "zork_grand_inquisitor",
        "raft",
        "swr",
        "heretic",
        "ahit",
        "trackmania",
        "doom_ii",
        "huniepop2",
        "frogmonster",
        "doom_1993",
        "shivers",
        "huniepop",
        "ultrakill",
        "lunacid",
        "yugiohddm",
        "witness",
        "earthbound",
        "quake",
        "minecraft",
        "outer_wilds",
        "powerwashsimulator",
        "seaofthieves",
        "subnautica",
        "lingo"
    ],
    "first": [
        "cv64",
        "metroidprime",
        "star_fox_64",
        "inscryption",
        "sims4",
        "fm",
        "hylics2",
        "lethal_company",
        "satisfactory",
        "zork_grand_inquisitor",
        "raft",
        "swr",
        "heretic",
        "ahit",
        "trackmania",
        "doom_ii",
        "huniepop2",
        "frogmonster",
        "doom_1993",
        "shivers",
        "huniepop",
        "ultrakill",
        "lunacid",
        "yugiohddm",
        "witness",
        "earthbound",
        "quake",
        "minecraft",
        "outer_wilds",
        "powerwashsimulator",
        "seaofthieves",
        "subnautica",
        "lingo"
    ],
    "person": [
        "mk64",
        "metroidprime",
        "rac2",
        "luigismansion",
        "lethal_company",
        "albw",
        "sms",
        "raft",
        "heretic",
        "xenobladex",
        "getting_over_it",
        "sa2b",
        "frogmonster",
        "banjo_tooie",
        "apeescape",
        "yugiohddm",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "dark_souls_3",
        "hcniko",
        "star_fox_64",
        "sims4",
        "hylics2",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "spyro3",
        "doom_ii",
        "huniepop2",
        "megamix",
        "huniepop",
        "dsr",
        "gzdoom",
        "subnautica",
        "lingo",
        "soe",
        "smo",
        "mm_recomp",
        "ror2",
        "inscryption",
        "sly1",
        "celeste64",
        "diddy_kong_racing",
        "sadx",
        "swr",
        "jakanddaxter",
        "placidplasticducksim",
        "dk64",
        "tww",
        "crystal_project",
        "doom_1993",
        "shivers",
        "sm64hacks",
        "dw1",
        "seaofthieves",
        "outer_wilds",
        "cv64",
        "kh2",
        "toontown",
        "oot",
        "mario_kart_double_dash",
        "fm",
        "papermario",
        "kh1",
        "satisfactory",
        "zork_grand_inquisitor",
        "sm64ex",
        "trackmania",
        "tp",
        "lego_star_wars_tcs",
        "cat_quest",
        "ultrakill",
        "lunacid",
        "gstla",
        "witness",
        "residentevil3remake",
        "earthbound",
        "sonic_heroes",
        "powerwashsimulator",
        "ss"
    ],
    "third person": [
        "soe",
        "mk64",
        "cv64",
        "smo",
        "mm_recomp",
        "hcniko",
        "ror2",
        "star_fox_64",
        "ss",
        "kh2",
        "toontown",
        "oot",
        "sly1",
        "rac2",
        "sims4",
        "luigismansion",
        "papermario",
        "celeste64",
        "hylics2",
        "albw",
        "bomb_rush_cyberfunk",
        "diddy_kong_racing",
        "kh1",
        "sms",
        "simpsonshitnrun",
        "sadx",
        "raft",
        "swr",
        "jakanddaxter",
        "ahit",
        "xenobladex",
        "placidplasticducksim",
        "getting_over_it",
        "dk64",
        "sa2b",
        "sm64ex",
        "spyro3",
        "tp",
        "trackmania",
        "tww",
        "megamix",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "apeescape",
        "cat_quest",
        "crystal_project",
        "sm64hacks",
        "gstla",
        "residentevil3remake",
        "dsr",
        "pseudoregalia",
        "sonic_heroes",
        "dw1",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "gzdoom",
        "dark_souls_3",
        "mario_kart_double_dash"
    ],
    "third": [
        "soe",
        "mk64",
        "cv64",
        "smo",
        "mm_recomp",
        "hcniko",
        "ror2",
        "star_fox_64",
        "ss",
        "kh2",
        "toontown",
        "oot",
        "sly1",
        "rac2",
        "sims4",
        "luigismansion",
        "papermario",
        "celeste64",
        "hylics2",
        "albw",
        "bomb_rush_cyberfunk",
        "diddy_kong_racing",
        "kh1",
        "sms",
        "simpsonshitnrun",
        "sadx",
        "raft",
        "swr",
        "jakanddaxter",
        "ahit",
        "xenobladex",
        "placidplasticducksim",
        "getting_over_it",
        "dk64",
        "sa2b",
        "sm64ex",
        "spyro3",
        "tp",
        "trackmania",
        "tww",
        "megamix",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "apeescape",
        "cat_quest",
        "crystal_project",
        "sm64hacks",
        "gstla",
        "residentevil3remake",
        "dsr",
        "pseudoregalia",
        "sonic_heroes",
        "dw1",
        "residentevil2remake",
        "minecraft",
        "dark_souls_2",
        "gzdoom",
        "dark_souls_3",
        "mario_kart_double_dash"
    ],
    "platform": [
        "cv64",
        "dkc",
        "smo",
        "hcniko",
        "metroidprime",
        "k64",
        "yoshisisland",
        "animal_well",
        "smz3",
        "oribf",
        "terraria",
        "dkc3",
        "rogue_legacy",
        "sly1",
        "rac2",
        "cuphead",
        "enderlilies",
        "ror1",
        "faxanadu",
        "celeste64",
        "hylics2",
        "dkc2",
        "sm_map_rando",
        "sotn",
        "bomb_rush_cyberfunk",
        "zelda2",
        "cvcotm",
        "hk",
        "ufo50",
        "messenger",
        "sms",
        "simpsonshitnrun",
        "mmx3",
        "sadx",
        "sm",
        "zillion",
        "jakanddaxter",
        "ahit",
        "peaks_of_yore",
        "mm3",
        "getting_over_it",
        "dk64",
        "sa2b",
        "sm64ex",
        "celeste_open_world",
        "spyro3",
        "marioland2",
        "lego_star_wars_tcs",
        "apeescape",
        "banjo_tooie",
        "crystal_project",
        "momodoramoonlitfarewell",
        "mm2",
        "kdl3",
        "blasphemous",
        "mzm",
        "ultrakill",
        "aus",
        "sm64hacks",
        "wl4",
        "smw",
        "timespinner",
        "wl",
        "v6",
        "sonic_heroes",
        "pseudoregalia",
        "aquaria",
        "monster_sanctuary",
        "gzdoom",
        "metroidfusion",
        "celeste",
        "dlcquest"
    ],
    "action": [
        "mk64",
        "metroidprime",
        "ss",
        "rogue_legacy",
        "rac2",
        "ffmq",
        "luigismansion",
        "lethal_company",
        "sc2",
        "albw",
        "messenger",
        "sms",
        "mlss",
        "xenobladex",
        "musedash",
        "getting_over_it",
        "sa2b",
        "ctjot",
        "apeescape",
        "banjo_tooie",
        "frogmonster",
        "ladx",
        "ff4fe",
        "blasphemous",
        "smw",
        "tloz_ooa",
        "quake",
        "pseudoregalia",
        "residentevil2remake",
        "dark_souls_2",
        "dark_souls_3",
        "doronko_wanko",
        "dontstarvetogether",
        "hcniko",
        "star_fox_64",
        "dkc3",
        "cuphead",
        "sims4",
        "noita",
        "bomb_rush_cyberfunk",
        "simpsonshitnrun",
        "ahit",
        "peaks_of_yore",
        "mm3",
        "spyro3",
        "doom_ii",
        "tyrian",
        "mzm",
        "tloz_ph",
        "pokemon_emerald",
        "wl",
        "v6",
        "dsr",
        "gzdoom",
        "metroidfusion",
        "brotato",
        "terraria",
        "soe",
        "pokemon_frlg",
        "dkc",
        "mm_recomp",
        "smo",
        "k64",
        "ror2",
        "tunic",
        "sly1",
        "alttp",
        "hades",
        "enderlilies",
        "sotn",
        "faxanadu",
        "celeste64",
        "zelda2",
        "sm_map_rando",
        "diddy_kong_racing",
        "hk",
        "ufo50",
        "tetrisattack",
        "mmx3",
        "sadx",
        "sm",
        "swr",
        "jakanddaxter",
        "pokemon_crystal",
        "dk64",
        "tww",
        "momodoramoonlitfarewell",
        "doom_1993",
        "kdl3",
        "aus",
        "sm64hacks",
        "tloz_oos",
        "crosscode",
        "monster_sanctuary",
        "dw1",
        "seaofthieves",
        "celeste",
        "dlcquest",
        "osu",
        "outer_wilds",
        "cv64",
        "yoshisisland",
        "landstalker",
        "animal_well",
        "kh2",
        "tloz",
        "mmbn3",
        "smz3",
        "oribf",
        "oot",
        "ff1",
        "ror1",
        "papermario",
        "dkc2",
        "cvcotm",
        "kh1",
        "tmc",
        "sm64ex",
        "trackmania",
        "celeste_open_world",
        "tp",
        "marioland2",
        "lego_star_wars_tcs",
        "cat_quest",
        "mm2",
        "overcooked2",
        "ultrakill",
        "wl4",
        "pokemon_rb",
        "gstla",
        "chainedechoes",
        "timespinner",
        "residentevil3remake",
        "earthbound",
        "sonic_heroes",
        "poe",
        "mario_kart_double_dash"
    ],
    "playstation 4": [
        "wargroove",
        "ror2",
        "kh2",
        "stardew_valley",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "celeste",
        "cuphead",
        "hades",
        "sims4",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "messenger",
        "swr",
        "jakanddaxter",
        "ahit",
        "placidplasticducksim",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "cat_quest",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "v6",
        "witness",
        "dsr",
        "monster_sanctuary",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "poe",
        "brotato",
        "subnautica",
        "terraria",
        "dark_souls_3"
    ],
    "4": [
        "wargroove",
        "ror2",
        "kh2",
        "stardew_valley",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "celeste",
        "cuphead",
        "hades",
        "sims4",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "messenger",
        "swr",
        "jakanddaxter",
        "ahit",
        "placidplasticducksim",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "cat_quest",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "wl4",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "v6",
        "witness",
        "dsr",
        "monster_sanctuary",
        "dw1",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "poe",
        "brotato",
        "subnautica",
        "terraria",
        "dark_souls_3"
    ],
    "mac": [
        "openrct2",
        "dontstarvetogether",
        "civ_6",
        "landstalker",
        "factorio_saws",
        "stardew_valley",
        "toontown",
        "inscryption",
        "terraria",
        "rogue_legacy",
        "tunic",
        "celeste",
        "cuphead",
        "osrs",
        "hades",
        "sims4",
        "ror1",
        "hylics2",
        "sc2",
        "hk",
        "zork_grand_inquisitor",
        "swr",
        "heretic",
        "ahit",
        "musedash",
        "getting_over_it",
        "undertale",
        "doom_ii",
        "celeste_open_world",
        "huniepop2",
        "tyrian",
        "lego_star_wars_tcs",
        "crystal_project",
        "cat_quest",
        "overcooked2",
        "blasphemous",
        "huniepop",
        "rimworld",
        "shorthike",
        "balatro",
        "chainedechoes",
        "shapez",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "v6",
        "witness",
        "quake",
        "aquaria",
        "monster_sanctuary",
        "residentevil2remake",
        "minecraft",
        "poe",
        "brotato",
        "factorio",
        "subnautica",
        "dlcquest",
        "osu"
    ],
    "xbox one": [
        "wargroove",
        "ror2",
        "stardew_valley",
        "oribf",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "sims4",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "messenger",
        "swr",
        "ahit",
        "placidplasticducksim",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "witness",
        "dsr",
        "monster_sanctuary",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "seaofthieves",
        "poe",
        "brotato",
        "subnautica",
        "terraria",
        "dark_souls_3"
    ],
    "one": [
        "wargroove",
        "ror2",
        "stardew_valley",
        "oribf",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "celeste",
        "cuphead",
        "hades",
        "sims4",
        "enderlilies",
        "ror1",
        "bomb_rush_cyberfunk",
        "hk",
        "messenger",
        "swr",
        "ahit",
        "placidplasticducksim",
        "trackmania",
        "undertale",
        "celeste_open_world",
        "overcooked2",
        "blasphemous",
        "shorthike",
        "balatro",
        "chainedechoes",
        "timespinner",
        "crosscode",
        "residentevil3remake",
        "witness",
        "dsr",
        "monster_sanctuary",
        "residentevil2remake",
        "outer_wilds",
        "powerwashsimulator",
        "seaofthieves",
        "poe",
        "brotato",
        "subnautica",
        "terraria",
        "dark_souls_3"
    ],
    "time travel": [
        "ahit",
        "tloz_ooa",
        "timespinner",
        "mm_recomp",
        "earthbound",
        "pmd_eos",
        "ctjot",
        "apeescape",
        "outer_wilds",
        "oot",
        "tloz_oos"
    ],
    "travel": [
        "ahit",
        "tloz_ooa",
        "timespinner",
        "mm_recomp",
        "earthbound",
        "pmd_eos",
        "ctjot",
        "apeescape",
        "outer_wilds",
        "oot",
        "tloz_oos"
    ],
    "spaceship": [
        "ahit",
        "metroidprime",
        "v6",
        "civ_6",
        "star_fox_64",
        "metroidfusion",
        "mzm"
    ],
    "female protagonist": [
        "cv64",
        "hcniko",
        "metroidprime",
        "rogue_legacy",
        "dkc3",
        "enderlilies",
        "celeste64",
        "dkc2",
        "sm_map_rando",
        "sm",
        "ahit",
        "undertale",
        "celeste_open_world",
        "mzm",
        "shorthike",
        "timespinner",
        "earthbound",
        "metroidfusion",
        "celeste"
    ],
    "female": [
        "cv64",
        "hcniko",
        "metroidprime",
        "rogue_legacy",
        "dkc3",
        "enderlilies",
        "celeste64",
        "dkc2",
        "sm_map_rando",
        "sm",
        "ahit",
        "undertale",
        "celeste_open_world",
        "mzm",
        "shorthike",
        "timespinner",
        "earthbound",
        "metroidfusion",
        "celeste"
    ],
    "protagonist": [
        "cv64",
        "dkc",
        "hcniko",
        "metroidprime",
        "k64",
        "dkc3",
        "oot",
        "rogue_legacy",
        "alttp",
        "enderlilies",
        "papermario",
        "celeste64",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "hk",
        "tmc",
        "sm",
        "jakanddaxter",
        "ahit",
        "mlss",
        "undertale",
        "celeste_open_world",
        "ladx",
        "mzm",
        "doom_1993",
        "tloz_ph",
        "blasphemous",
        "shorthike",
        "ultrakill",
        "tloz_oos",
        "pokemon_emerald",
        "gstla",
        "tloz_ooa",
        "timespinner",
        "earthbound",
        "quake",
        "metroidfusion",
        "celeste",
        "ss"
    ],
    "action-adventure": [
        "cv64",
        "mm_recomp",
        "dontstarvetogether",
        "metroidprime",
        "landstalker",
        "rogue_legacy",
        "oot",
        "alttp",
        "luigismansion",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "albw",
        "cvcotm",
        "hk",
        "kh1",
        "tmc",
        "zillion",
        "sms",
        "sm",
        "ahit",
        "xenobladex",
        "tww",
        "banjo_tooie",
        "ladx",
        "tloz_ph",
        "aus",
        "tloz_oos",
        "tloz_ooa",
        "timespinner",
        "crosscode",
        "aquaria",
        "minecraft",
        "seaofthieves",
        "dark_souls_2",
        "metroidfusion",
        "terraria",
        "dark_souls_3",
        "ss"
    ],
    "cute": [
        "ahit",
        "sims4",
        "musedash",
        "undertale",
        "hcniko",
        "celeste_open_world",
        "animal_well",
        "celeste",
        "tunic",
        "shorthike"
    ],
    "snow": [
        "ffta",
        "ahit",
        "gstla",
        "mk64",
        "dkc",
        "hcniko",
        "celeste_open_world",
        "metroidprime",
        "albw",
        "diddy_kong_racing",
        "minecraft",
        "lego_star_wars_tcs",
        "stardew_valley",
        "celeste",
        "terraria",
        "shorthike",
        "dkc3",
        "jakanddaxter"
    ],
    "wall jump": [
        "ahit",
        "smo",
        "sm_map_rando",
        "cvcotm",
        "mzm",
        "metroidfusion",
        "oribf",
        "simpsonshitnrun",
        "mmx3",
        "sm",
        "sms"
    ],
    "wall": [
        "dkc",
        "smo",
        "oribf",
        "rogue_legacy",
        "papermario",
        "dkc2",
        "sm_map_rando",
        "cvcotm",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "mmx3",
        "sm",
        "jakanddaxter",
        "ahit",
        "mlss",
        "undertale",
        "doom_ii",
        "banjo_tooie",
        "ladx",
        "mzm",
        "ffta",
        "metroidfusion"
    ],
    "jump": [
        "ahit",
        "smo",
        "sm_map_rando",
        "cvcotm",
        "mzm",
        "metroidfusion",
        "oribf",
        "simpsonshitnrun",
        "mmx3",
        "sm",
        "sms"
    ],
    "3d platformer": [
        "sm64hacks",
        "ahit",
        "sm64ex",
        "smo",
        "hcniko",
        "sonic_heroes",
        "bomb_rush_cyberfunk",
        "sms",
        "shorthike"
    ],
    "3d": [
        "mk64",
        "cv64",
        "smo",
        "hcniko",
        "metroidprime",
        "k64",
        "star_fox_64",
        "tunic",
        "oot",
        "sly1",
        "luigismansion",
        "sotn",
        "hylics2",
        "albw",
        "bomb_rush_cyberfunk",
        "kh1",
        "sms",
        "simpsonshitnrun",
        "jakanddaxter",
        "ahit",
        "xenobladex",
        "spyro3",
        "dk64",
        "sm64ex",
        "frogmonster",
        "crystal_project",
        "apeescape",
        "lego_star_wars_tcs",
        "dark_souls_3",
        "tloz_ph",
        "shorthike",
        "sm64hacks",
        "witness",
        "dsr",
        "quake",
        "sonic_heroes",
        "dw1",
        "minecraft",
        "powerwashsimulator",
        "dark_souls_2",
        "poe",
        "lingo",
        "ss"
    ],
    "platformer": [
        "sm64hacks",
        "ahit",
        "sm64ex",
        "smo",
        "hcniko",
        "sonic_heroes",
        "bomb_rush_cyberfunk",
        "sms",
        "shorthike"
    ],
    "swimming": [
        "dkc",
        "smo",
        "hcniko",
        "dkc3",
        "oot",
        "alttp",
        "dkc2",
        "albw",
        "kh1",
        "tmc",
        "sms",
        "jakanddaxter",
        "ahit",
        "spyro3",
        "sm64ex",
        "banjo_tooie",
        "wl4",
        "sm64hacks",
        "tloz_ooa",
        "quake",
        "aquaria",
        "minecraft",
        "subnautica",
        "terraria"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "alttp",
        "tloz_ooa",
        "mm_recomp",
        "tp",
        "tww",
        "albw",
        "ss",
        "tloz",
        "tmc",
        "ladx",
        "tloz_ph",
        "oot",
        "tloz_oos"
    ],
    "of": [
        "soe",
        "cv64",
        "dkc",
        "mm_recomp",
        "pmd_eos",
        "ror2",
        "star_fox_64",
        "tloz",
        "oribf",
        "dkc3",
        "oot",
        "rogue_legacy",
        "sly1",
        "alttp",
        "enderlilies",
        "luigismansion",
        "lufia2ac",
        "celeste64",
        "ror1",
        "dkc2",
        "sc2",
        "albw",
        "sotn",
        "zelda2",
        "cvcotm",
        "tmc",
        "sms",
        "jakanddaxter",
        "peaks_of_yore",
        "pokemon_crystal",
        "dk64",
        "spyro3",
        "tp",
        "tww",
        "ladx",
        "tloz_ph",
        "tloz_oos",
        "ffta",
        "pokemon_emerald",
        "tloz_ooa",
        "tboir",
        "earthbound",
        "seaofthieves",
        "poe",
        "ss"
    ],
    "zelda:": [
        "alttp",
        "tloz_ooa",
        "mm_recomp",
        "tp",
        "tww",
        "albw",
        "ss",
        "tmc",
        "ladx",
        "tloz_ph",
        "oot",
        "tloz_oos"
    ],
    "link": [
        "albw",
        "alttp",
        "smz3",
        "zelda2"
    ],
    "between": [
        "albw"
    ],
    "worlds": [
        "albw"
    ],
    "puzzle": [
        "bumpstik",
        "cv64",
        "mm_recomp",
        "hcniko",
        "animal_well",
        "oribf",
        "inscryption",
        "tunic",
        "rogue_legacy",
        "oot",
        "alttp",
        "lufia2ac",
        "albw",
        "tmc",
        "ufo50",
        "tetrisattack",
        "zillion",
        "zork_grand_inquisitor",
        "candybox2",
        "placidplasticducksim",
        "spyro3",
        "undertale",
        "doom_ii",
        "tp",
        "huniepop2",
        "tww",
        "ttyd",
        "ladx",
        "tloz_ph",
        "shivers",
        "huniepop",
        "tloz_oos",
        "wl4",
        "yugiohddm",
        "tloz_ooa",
        "shapez",
        "witness",
        "crosscode",
        "v6",
        "outer_wilds",
        "metroidfusion",
        "lingo",
        "ss"
    ],
    "historical": [
        "heretic",
        "soe",
        "candybox2",
        "fm",
        "quake",
        "civ_6",
        "albw",
        "ss"
    ],
    "sandbox": [
        "smo",
        "dontstarvetogether",
        "landstalker",
        "factorio_saws",
        "stardew_valley",
        "oot",
        "osrs",
        "sims4",
        "noita",
        "faxanadu",
        "zelda2",
        "albw",
        "satisfactory",
        "sms",
        "xenobladex",
        "placidplasticducksim",
        "shapez",
        "minecraft",
        "powerwashsimulator",
        "factorio",
        "terraria"
    ],
    "open world": [
        "smo",
        "mm_recomp",
        "dontstarvetogether",
        "metroidprime",
        "tloz",
        "smz3",
        "toontown",
        "oot",
        "osrs",
        "sotn",
        "lingo",
        "albw",
        "satisfactory",
        "simpsonshitnrun",
        "jakanddaxter",
        "xenobladex",
        "sm64ex",
        "frogmonster",
        "mzm",
        "shorthike",
        "pokemon_rb",
        "sm64hacks",
        "gstla",
        "witness",
        "minecraft",
        "seaofthieves",
        "subnautica",
        "terraria",
        "outer_wilds",
        "ss"
    ],
    "open": [
        "smo",
        "mm_recomp",
        "dontstarvetogether",
        "metroidprime",
        "tloz",
        "smz3",
        "toontown",
        "oot",
        "osrs",
        "sotn",
        "lingo",
        "albw",
        "satisfactory",
        "simpsonshitnrun",
        "jakanddaxter",
        "xenobladex",
        "sm64ex",
        "frogmonster",
        "mzm",
        "shorthike",
        "pokemon_rb",
        "sm64hacks",
        "gstla",
        "witness",
        "minecraft",
        "seaofthieves",
        "subnautica",
        "terraria",
        "outer_wilds",
        "ss"
    ],
    "world": [
        "dkc",
        "mm_recomp",
        "dontstarvetogether",
        "metroidprime",
        "smo",
        "yoshisisland",
        "tloz",
        "smz3",
        "yugioh06",
        "toontown",
        "dkc3",
        "oot",
        "alttp",
        "osrs",
        "sotn",
        "dkc2",
        "zelda2",
        "albw",
        "tmc",
        "satisfactory",
        "simpsonshitnrun",
        "jakanddaxter",
        "xenobladex",
        "pokemon_crystal",
        "sm64ex",
        "frogmonster",
        "ladx",
        "mzm",
        "tloz_ph",
        "shorthike",
        "tloz_oos",
        "pokemon_rb",
        "sm64hacks",
        "gstla",
        "smw",
        "witness",
        "earthbound",
        "v6",
        "aquaria",
        "dw1",
        "minecraft",
        "outer_wilds",
        "dark_souls_2",
        "seaofthieves",
        "subnautica",
        "terraria",
        "lingo",
        "ss"
    ],
    "nintendo 3ds": [
        "pokemon_rb",
        "ff1",
        "mm3",
        "tloz_ooa",
        "pokemon_crystal",
        "wl4",
        "wl",
        "v6",
        "zelda2",
        "albw",
        "marioland2",
        "tloz",
        "tmc",
        "metroidfusion",
        "ladx",
        "mm2",
        "terraria",
        "tloz_oos"
    ],
    "3ds": [
        "dkc",
        "tloz",
        "dkc3",
        "alttp",
        "ff1",
        "dkc2",
        "sm_map_rando",
        "albw",
        "zelda2",
        "tmc",
        "mmx3",
        "sm",
        "mm3",
        "pokemon_crystal",
        "marioland2",
        "ladx",
        "mm2",
        "tloz_oos",
        "pokemon_rb",
        "wl4",
        "smw",
        "tloz_ooa",
        "wl",
        "earthbound",
        "v6",
        "metroidfusion",
        "terraria"
    ],
    "medieval": [
        "heretic",
        "soe",
        "candybox2",
        "quake",
        "albw",
        "dark_souls_2",
        "dark_souls_3",
        "rogue_legacy",
        "ss"
    ],
    "magic": [
        "cv64",
        "rogue_legacy",
        "cuphead",
        "alttp",
        "noita",
        "faxanadu",
        "sotn",
        "zelda2",
        "albw",
        "cvcotm",
        "tmc",
        "zork_grand_inquisitor",
        "heretic",
        "candybox2",
        "ctjot",
        "ladx",
        "tloz_oos",
        "ffta",
        "gstla",
        "dsr",
        "aquaria",
        "dark_souls_2",
        "poe",
        "terraria"
    ],
    "minigames": [
        "hcniko",
        "k64",
        "stardew_valley",
        "toontown",
        "rogue_legacy",
        "dkc3",
        "oot",
        "albw",
        "kh1",
        "pokemon_crystal",
        "dk64",
        "spyro3",
        "apeescape",
        "tloz_ph",
        "wl4",
        "aus",
        "pokemon_emerald",
        "gstla",
        "tloz_ooa"
    ],
    "2.5d": [
        "heretic",
        "dkc",
        "doom_ii",
        "k64",
        "albw",
        "doom_1993",
        "dkc3"
    ],
    "archery": [
        "alttp",
        "mm_recomp",
        "tww",
        "albw",
        "ss",
        "minecraft",
        "oot"
    ],
    "fairy": [
        "alttp",
        "tloz_ooa",
        "dk64",
        "mm_recomp",
        "huniepop2",
        "k64",
        "albw",
        "landstalker",
        "tww",
        "tloz",
        "tmc",
        "ladx",
        "stardew_valley",
        "zelda2",
        "tloz_ph",
        "terraria",
        "oot",
        "tloz_oos"
    ],
    "princess": [
        "mk64",
        "alttp",
        "mlss",
        "smw",
        "tloz_ooa",
        "papermario",
        "tp",
        "albw",
        "ss",
        "kh1",
        "lego_star_wars_tcs",
        "ladx",
        "tmc",
        "tloz_ph",
        "oot",
        "tloz_oos"
    ],
    "sequel": [
        "mk64",
        "smo",
        "mm_recomp",
        "dontstarvetogether",
        "civ_6",
        "oot",
        "alttp",
        "hylics2",
        "dkc2",
        "zelda2",
        "albw",
        "sms",
        "mmx3",
        "mm3",
        "doom_ii",
        "banjo_tooie",
        "mm2",
        "wl4",
        "ffta",
        "gstla",
        "dw1",
        "dark_souls_2",
        "dark_souls_3"
    ],
    "sword & sorcery": [
        "heretic",
        "tloz_ooa",
        "ffmq",
        "spyro3",
        "mm_recomp",
        "tww",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "dark_souls_2",
        "ladx",
        "terraria",
        "dark_souls_3",
        "oot",
        "tloz_oos"
    ],
    "sword": [
        "heretic",
        "tloz_ooa",
        "ffmq",
        "spyro3",
        "mm_recomp",
        "tww",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "dark_souls_2",
        "ladx",
        "terraria",
        "dark_souls_3",
        "oot",
        "tloz_oos"
    ],
    "&": [
        "mm_recomp",
        "yugioh06",
        "inscryption",
        "oot",
        "rac2",
        "ffmq",
        "fm",
        "albw",
        "kh1",
        "tmc",
        "simpsonshitnrun",
        "heretic",
        "mlss",
        "spyro3",
        "tww",
        "ladx",
        "balatro",
        "tloz_oos",
        "yugiohddm",
        "tloz_ooa",
        "dark_souls_2",
        "terraria",
        "dark_souls_3",
        "ss",
        "spire"
    ],
    "sorcery": [
        "heretic",
        "tloz_ooa",
        "ffmq",
        "spyro3",
        "mm_recomp",
        "tww",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "dark_souls_2",
        "ladx",
        "terraria",
        "dark_souls_3",
        "oot",
        "tloz_oos"
    ],
    "darkness": [
        "dkc",
        "rogue_legacy",
        "dkc3",
        "alttp",
        "luigismansion",
        "dkc2",
        "sm_map_rando",
        "albw",
        "zelda2",
        "tmc",
        "sm",
        "mm3",
        "doom_ii",
        "ladx",
        "witness",
        "earthbound",
        "aquaria",
        "minecraft",
        "metroidfusion",
        "terraria"
    ],
    "digital distribution": [
        "dkc",
        "dontstarvetogether",
        "civ_6",
        "yoshisisland",
        "oribf",
        "terraria",
        "tunic",
        "rogue_legacy",
        "oot",
        "cuphead",
        "sotn",
        "dkc2",
        "albw",
        "tmc",
        "ufo50",
        "heretic",
        "mlss",
        "musedash",
        "getting_over_it",
        "dk64",
        "sm64ex",
        "doom_ii",
        "celeste_open_world",
        "huniepop2",
        "banjo_tooie",
        "apeescape",
        "ladx",
        "tloz_oos",
        "sm64hacks",
        "wl4",
        "smw",
        "timespinner",
        "crosscode",
        "witness",
        "v6",
        "quake",
        "minecraft",
        "seaofthieves",
        "celeste",
        "factorio",
        "dlcquest"
    ],
    "digital": [
        "dkc",
        "dontstarvetogether",
        "civ_6",
        "yoshisisland",
        "oribf",
        "terraria",
        "tunic",
        "rogue_legacy",
        "oot",
        "cuphead",
        "sotn",
        "dkc2",
        "albw",
        "tmc",
        "ufo50",
        "heretic",
        "mlss",
        "musedash",
        "getting_over_it",
        "dk64",
        "sm64ex",
        "doom_ii",
        "celeste_open_world",
        "huniepop2",
        "banjo_tooie",
        "apeescape",
        "ladx",
        "tloz_oos",
        "sm64hacks",
        "wl4",
        "smw",
        "timespinner",
        "crosscode",
        "witness",
        "v6",
        "quake",
        "minecraft",
        "seaofthieves",
        "celeste",
        "factorio",
        "dlcquest"
    ],
    "distribution": [
        "dkc",
        "dontstarvetogether",
        "civ_6",
        "yoshisisland",
        "oribf",
        "terraria",
        "tunic",
        "rogue_legacy",
        "oot",
        "cuphead",
        "sotn",
        "dkc2",
        "albw",
        "tmc",
        "ufo50",
        "heretic",
        "mlss",
        "musedash",
        "getting_over_it",
        "dk64",
        "sm64ex",
        "doom_ii",
        "celeste_open_world",
        "huniepop2",
        "banjo_tooie",
        "apeescape",
        "ladx",
        "tloz_oos",
        "sm64hacks",
        "wl4",
        "smw",
        "timespinner",
        "crosscode",
        "witness",
        "v6",
        "quake",
        "minecraft",
        "seaofthieves",
        "celeste",
        "factorio",
        "dlcquest"
    ],
    "anthropomorphism": [
        "mk64",
        "cv64",
        "dkc",
        "hcniko",
        "k64",
        "star_fox_64",
        "tunic",
        "dkc3",
        "sly1",
        "cuphead",
        "papermario",
        "dkc2",
        "albw",
        "diddy_kong_racing",
        "kh1",
        "tmc",
        "sms",
        "jakanddaxter",
        "mlss",
        "spyro3",
        "dk64",
        "undertale",
        "banjo_tooie",
        "apeescape",
        "shorthike",
        "tloz_oos",
        "tloz_ooa",
        "sonic_heroes"
    ],
    "polygonal 3d": [
        "mk64",
        "cv64",
        "metroidprime",
        "k64",
        "star_fox_64",
        "oot",
        "sly1",
        "luigismansion",
        "sotn",
        "albw",
        "kh1",
        "sms",
        "simpsonshitnrun",
        "jakanddaxter",
        "xenobladex",
        "spyro3",
        "dk64",
        "lego_star_wars_tcs",
        "apeescape",
        "tloz_ph",
        "witness",
        "quake",
        "dw1",
        "minecraft",
        "ss"
    ],
    "polygonal": [
        "mk64",
        "cv64",
        "metroidprime",
        "k64",
        "star_fox_64",
        "oot",
        "sly1",
        "luigismansion",
        "sotn",
        "albw",
        "kh1",
        "sms",
        "simpsonshitnrun",
        "jakanddaxter",
        "xenobladex",
        "spyro3",
        "dk64",
        "lego_star_wars_tcs",
        "apeescape",
        "tloz_ph",
        "witness",
        "quake",
        "dw1",
        "minecraft",
        "ss"
    ],
    "bow and arrow": [
        "ffta",
        "cuphead",
        "alttp",
        "ror1",
        "albw",
        "ss",
        "minecraft",
        "tmc",
        "dark_souls_2",
        "ladx",
        "poe",
        "tloz_ph",
        "terraria",
        "rogue_legacy",
        "oot",
        "tloz_oos"
    ],
    "bow": [
        "ffta",
        "cuphead",
        "alttp",
        "ror1",
        "albw",
        "ss",
        "minecraft",
        "tmc",
        "dark_souls_2",
        "ladx",
        "poe",
        "tloz_ph",
        "terraria",
        "rogue_legacy",
        "oot",
        "tloz_oos"
    ],
    "and": [
        "openrct2",
        "cv64",
        "civ_6",
        "smz3",
        "oribf",
        "rogue_legacy",
        "oot",
        "sly1",
        "cuphead",
        "alttp",
        "hades",
        "ror1",
        "albw",
        "tmc",
        "jakanddaxter",
        "ladx",
        "tloz_ph",
        "blasphemous",
        "tloz_oos",
        "ffta",
        "minecraft",
        "dark_souls_2",
        "poe",
        "terraria",
        "ss"
    ],
    "arrow": [
        "ffta",
        "cuphead",
        "alttp",
        "ror1",
        "albw",
        "ss",
        "minecraft",
        "tmc",
        "dark_souls_2",
        "ladx",
        "poe",
        "tloz_ph",
        "terraria",
        "rogue_legacy",
        "oot",
        "tloz_oos"
    ],
    "damsel in distress": [
        "alttp",
        "smw",
        "tloz_ooa",
        "tloz_ph",
        "papermario",
        "metroidprime",
        "earthbound",
        "zelda2",
        "sm_map_rando",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "oot",
        "tloz_oos"
    ],
    "damsel": [
        "alttp",
        "smw",
        "tloz_ooa",
        "tloz_ph",
        "papermario",
        "metroidprime",
        "earthbound",
        "zelda2",
        "sm_map_rando",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "oot",
        "tloz_oos"
    ],
    "distress": [
        "alttp",
        "smw",
        "tloz_ooa",
        "tloz_ph",
        "papermario",
        "metroidprime",
        "earthbound",
        "zelda2",
        "sm_map_rando",
        "albw",
        "ss",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "oot",
        "tloz_oos"
    ],
    "upgradeable weapons": [
        "cv64",
        "dk64",
        "metroidprime",
        "albw",
        "tmc",
        "metroidfusion",
        "dark_souls_2",
        "mzm",
        "mm2",
        "mmx3"
    ],
    "upgradeable": [
        "cv64",
        "dk64",
        "metroidprime",
        "albw",
        "tmc",
        "metroidfusion",
        "dark_souls_2",
        "mzm",
        "mm2",
        "mmx3"
    ],
    "weapons": [
        "cv64",
        "dk64",
        "metroidprime",
        "albw",
        "tmc",
        "metroidfusion",
        "dark_souls_2",
        "mzm",
        "mm2",
        "mmx3"
    ],
    "disorientation zone": [
        "alttp",
        "tloz_ooa",
        "albw",
        "tmc",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "disorientation": [
        "alttp",
        "tloz_ooa",
        "albw",
        "tmc",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "zone": [
        "alttp",
        "tloz_ooa",
        "albw",
        "tmc",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "descendants of other characters": [
        "tloz_ooa",
        "cv64",
        "dk64",
        "dkc",
        "luigismansion",
        "earthbound",
        "mm_recomp",
        "dkc2",
        "rogue_legacy",
        "albw",
        "sotn",
        "star_fox_64",
        "tmc",
        "sms",
        "dkc3",
        "oot",
        "sly1",
        "jakanddaxter"
    ],
    "descendants": [
        "tloz_ooa",
        "cv64",
        "dk64",
        "dkc",
        "luigismansion",
        "earthbound",
        "mm_recomp",
        "dkc2",
        "rogue_legacy",
        "albw",
        "sotn",
        "star_fox_64",
        "tmc",
        "sms",
        "dkc3",
        "oot",
        "sly1",
        "jakanddaxter"
    ],
    "other": [
        "tloz_ooa",
        "cv64",
        "dk64",
        "dkc",
        "luigismansion",
        "earthbound",
        "mm_recomp",
        "dkc2",
        "rogue_legacy",
        "albw",
        "sotn",
        "star_fox_64",
        "tmc",
        "sms",
        "dkc3",
        "oot",
        "sly1",
        "jakanddaxter"
    ],
    "characters": [
        "cv64",
        "dkc",
        "mm_recomp",
        "star_fox_64",
        "stardew_valley",
        "rogue_legacy",
        "dkc3",
        "oot",
        "sly1",
        "luigismansion",
        "sotn",
        "dkc2",
        "albw",
        "tmc",
        "sms",
        "jakanddaxter",
        "xenobladex",
        "dk64",
        "lego_star_wars_tcs",
        "tloz_ooa",
        "earthbound",
        "dark_souls_2",
        "terraria",
        "dark_souls_3"
    ],
    "save point": [
        "cv64",
        "dkc",
        "metroidprime",
        "dkc3",
        "luigismansion",
        "faxanadu",
        "papermario",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "albw",
        "cvcotm",
        "kh1",
        "sm",
        "jakanddaxter",
        "mlss",
        "mzm",
        "gstla",
        "earthbound",
        "v6",
        "aquaria",
        "metroidfusion"
    ],
    "save": [
        "cv64",
        "dkc",
        "metroidprime",
        "dkc3",
        "luigismansion",
        "faxanadu",
        "papermario",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "albw",
        "cvcotm",
        "kh1",
        "sm",
        "jakanddaxter",
        "mlss",
        "mzm",
        "gstla",
        "earthbound",
        "v6",
        "aquaria",
        "metroidfusion"
    ],
    "point": [
        "cv64",
        "dkc",
        "metroidprime",
        "dkc3",
        "luigismansion",
        "faxanadu",
        "papermario",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "albw",
        "cvcotm",
        "kh1",
        "sm",
        "jakanddaxter",
        "mlss",
        "mzm",
        "gstla",
        "earthbound",
        "v6",
        "aquaria",
        "metroidfusion"
    ],
    "side quests": [
        "pokemon_emerald",
        "alttp",
        "tloz_ooa",
        "xenobladex",
        "pokemon_crystal",
        "sc2",
        "albw",
        "tmc",
        "ladx",
        "dark_souls_2",
        "tloz_ph",
        "oot",
        "tloz_oos"
    ],
    "side": [
        "pokemon_frlg",
        "wargroove",
        "dkc",
        "k64",
        "yoshisisland",
        "animal_well",
        "smz3",
        "oribf",
        "terraria",
        "dkc3",
        "oot",
        "rogue_legacy",
        "wargroove2",
        "cuphead",
        "alttp",
        "ff1",
        "ffmq",
        "zelda2",
        "enderlilies",
        "noita",
        "faxanadu",
        "hylics2",
        "lufia2ac",
        "dkc2",
        "papermario",
        "albw",
        "ror1",
        "sc2",
        "cvcotm",
        "hk",
        "sm_map_rando",
        "tmc",
        "tetrisattack",
        "messenger",
        "ufo50",
        "zillion",
        "mmx3",
        "sm",
        "mlss",
        "xenobladex",
        "mm3",
        "musedash",
        "getting_over_it",
        "pokemon_crystal",
        "celeste_open_world",
        "marioland2",
        "megamix",
        "momodoramoonlitfarewell",
        "ladx",
        "mzm",
        "mm2",
        "ff4fe",
        "blasphemous",
        "kdl3",
        "sotn",
        "tloz_ph",
        "aus",
        "pokemon_rb",
        "tloz_oos",
        "pokemon_emerald",
        "wl4",
        "smw",
        "tloz_ooa",
        "timespinner",
        "wl",
        "v6",
        "aquaria",
        "monster_sanctuary",
        "dark_souls_2",
        "metroidfusion",
        "celeste",
        "dlcquest",
        "spire"
    ],
    "quests": [
        "pokemon_emerald",
        "alttp",
        "tloz_ooa",
        "xenobladex",
        "pokemon_crystal",
        "metroidprime",
        "sc2",
        "zelda2",
        "albw",
        "tmc",
        "ladx",
        "dark_souls_2",
        "tloz_ph",
        "oot",
        "tloz_oos"
    ],
    "potion": [
        "pokemon_emerald",
        "alttp",
        "gstla",
        "pokemon_crystal",
        "zelda2",
        "albw",
        "kh1",
        "minecraft",
        "ladx",
        "poe",
        "tmc",
        "tloz_ph",
        "rogue_legacy",
        "ss",
        "tloz_oos"
    ],
    "real-time combat": [
        "cv64",
        "dkc",
        "metroidprime",
        "landstalker",
        "oot",
        "alttp",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "albw",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "xenobladex",
        "spyro3",
        "dk64",
        "sm64ex",
        "doom_ii",
        "ladx",
        "doom_1993",
        "tloz_ph",
        "tloz_oos",
        "sm64hacks",
        "tloz_ooa",
        "quake",
        "minecraft",
        "dark_souls_2",
        "ss"
    ],
    "real-time": [
        "cv64",
        "dkc",
        "metroidprime",
        "landstalker",
        "oot",
        "alttp",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "albw",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "xenobladex",
        "spyro3",
        "dk64",
        "sm64ex",
        "doom_ii",
        "ladx",
        "doom_1993",
        "tloz_ph",
        "tloz_oos",
        "sm64hacks",
        "tloz_ooa",
        "quake",
        "minecraft",
        "dark_souls_2",
        "ss"
    ],
    "combat": [
        "cv64",
        "dkc",
        "metroidprime",
        "landstalker",
        "oot",
        "alttp",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "albw",
        "kh1",
        "tmc",
        "sms",
        "sm",
        "xenobladex",
        "spyro3",
        "dk64",
        "sm64ex",
        "doom_ii",
        "ladx",
        "doom_1993",
        "tloz_ph",
        "tloz_oos",
        "sm64hacks",
        "tloz_ooa",
        "quake",
        "minecraft",
        "dark_souls_2",
        "ss"
    ],
    "self-referential humor": [
        "mlss",
        "papermario",
        "earthbound",
        "dkc2",
        "albw",
        "metroidfusion"
    ],
    "self-referential": [
        "mlss",
        "papermario",
        "earthbound",
        "dkc2",
        "albw",
        "metroidfusion"
    ],
    "humor": [
        "mlss",
        "papermario",
        "earthbound",
        "dkc2",
        "albw",
        "metroidfusion"
    ],
    "rpg elements": [
        "mlss",
        "sotn",
        "zelda2",
        "albw",
        "minecraft",
        "lego_star_wars_tcs",
        "metroidfusion",
        "banjo_tooie",
        "dark_souls_2",
        "mzm",
        "oribf"
    ],
    "rpg": [
        "mlss",
        "sotn",
        "zelda2",
        "albw",
        "minecraft",
        "lego_star_wars_tcs",
        "metroidfusion",
        "banjo_tooie",
        "dark_souls_2",
        "mzm",
        "oribf"
    ],
    "elements": [
        "mlss",
        "sotn",
        "zelda2",
        "albw",
        "minecraft",
        "lego_star_wars_tcs",
        "metroidfusion",
        "banjo_tooie",
        "dark_souls_2",
        "mzm",
        "oribf"
    ],
    "mercenary": [
        "alttp",
        "metroidprime",
        "quake",
        "sc2",
        "albw",
        "sm_map_rando",
        "ss",
        "dark_souls_2",
        "sm",
        "oot"
    ],
    "coming of age": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "pokemon_crystal",
        "albw",
        "tmc",
        "oribf",
        "oot",
        "jakanddaxter"
    ],
    "coming": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "pokemon_crystal",
        "albw",
        "tmc",
        "oribf",
        "oot",
        "jakanddaxter"
    ],
    "age": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "gstla",
        "pokemon_crystal",
        "albw",
        "factorio_saws",
        "tmc",
        "oribf",
        "oot",
        "jakanddaxter"
    ],
    "androgyny": [
        "ffta",
        "gstla",
        "sotn",
        "albw",
        "ss",
        "oot"
    ],
    "fast traveling": [
        "pokemon_emerald",
        "alttp",
        "undertale",
        "albw",
        "hk",
        "tmc",
        "poe",
        "tloz_ph",
        "oot"
    ],
    "fast": [
        "pokemon_emerald",
        "alttp",
        "undertale",
        "albw",
        "hk",
        "tmc",
        "poe",
        "tloz_ph",
        "oot"
    ],
    "traveling": [
        "pokemon_emerald",
        "alttp",
        "undertale",
        "albw",
        "hk",
        "tmc",
        "poe",
        "tloz_ph",
        "oot"
    ],
    "context sensitive": [
        "alttp",
        "tloz_ooa",
        "oot",
        "albw",
        "tloz_ph",
        "ss",
        "tloz_oos"
    ],
    "context": [
        "alttp",
        "tloz_ooa",
        "oot",
        "albw",
        "tloz_ph",
        "ss",
        "tloz_oos"
    ],
    "sensitive": [
        "alttp",
        "tloz_ooa",
        "oot",
        "albw",
        "tloz_ph",
        "ss",
        "tloz_oos"
    ],
    "living inventory": [
        "alttp",
        "mm_recomp",
        "oot",
        "tww",
        "albw",
        "tmc",
        "ss"
    ],
    "living": [
        "alttp",
        "mm_recomp",
        "oot",
        "tww",
        "albw",
        "tmc",
        "ss"
    ],
    "inventory": [
        "alttp",
        "mm_recomp",
        "oot",
        "tww",
        "albw",
        "tmc",
        "ss"
    ],
    "bees": [
        "alttp",
        "dontstarvetogether",
        "albw",
        "minecraft",
        "tloz_ph",
        "terraria",
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
        "soe",
        "alttp",
        "smw",
        "ffmq",
        "dkc",
        "sm",
        "lufia2ac",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "yoshisisland",
        "smz3",
        "tetrisattack",
        "ff4fe",
        "mmx3",
        "dkc3",
        "kdl3"
    ],
    "super": [
        "soe",
        "dkc",
        "smo",
        "yoshisisland",
        "smz3",
        "dkc3",
        "alttp",
        "ffmq",
        "lufia2ac",
        "dkc2",
        "sm_map_rando",
        "tetrisattack",
        "sms",
        "mmx3",
        "sm",
        "sm64ex",
        "marioland2",
        "ff4fe",
        "kdl3",
        "sm64hacks",
        "smw",
        "wl",
        "earthbound"
    ],
    "entertainment": [
        "soe",
        "dkc",
        "yoshisisland",
        "tloz",
        "smz3",
        "dkc3",
        "alttp",
        "ff1",
        "ffmq",
        "faxanadu",
        "lufia2ac",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "tetrisattack",
        "mmx3",
        "sm",
        "mm3",
        "ff4fe",
        "kdl3",
        "smw",
        "earthbound"
    ],
    "wii": [
        "mk64",
        "dkc",
        "mm_recomp",
        "k64",
        "pmd_eos",
        "star_fox_64",
        "landstalker",
        "tloz",
        "stardew_valley",
        "dkc3",
        "oot",
        "alttp",
        "ff1",
        "ffmq",
        "papermario",
        "faxanadu",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "cvcotm",
        "hk",
        "tmc",
        "mmx3",
        "sm",
        "mlss",
        "xenobladex",
        "mm3",
        "dk64",
        "sm64ex",
        "tp",
        "lego_star_wars_tcs",
        "mzm",
        "tloz_ph",
        "ff4fe",
        "kdl3",
        "wl4",
        "sm64hacks",
        "ffta",
        "gstla",
        "smw",
        "earthbound",
        "metroidfusion",
        "terraria",
        "ss"
    ],
    "wii u": [
        "mk64",
        "dkc",
        "mm_recomp",
        "k64",
        "pmd_eos",
        "star_fox_64",
        "tloz",
        "stardew_valley",
        "dkc3",
        "oot",
        "alttp",
        "ff1",
        "ffmq",
        "papermario",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "cvcotm",
        "hk",
        "tmc",
        "mmx3",
        "sm",
        "mlss",
        "xenobladex",
        "mm3",
        "dk64",
        "sm64ex",
        "mzm",
        "tloz_ph",
        "kdl3",
        "wl4",
        "sm64hacks",
        "ffta",
        "gstla",
        "smw",
        "earthbound",
        "metroidfusion",
        "terraria",
        "ss"
    ],
    "u": [
        "mk64",
        "dkc",
        "mm_recomp",
        "k64",
        "pmd_eos",
        "star_fox_64",
        "tloz",
        "stardew_valley",
        "dkc3",
        "oot",
        "alttp",
        "ff1",
        "ffmq",
        "papermario",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "cvcotm",
        "hk",
        "tmc",
        "mmx3",
        "sm",
        "mlss",
        "xenobladex",
        "mm3",
        "dk64",
        "sm64ex",
        "mzm",
        "tloz_ph",
        "kdl3",
        "wl4",
        "sm64hacks",
        "ffta",
        "gstla",
        "smw",
        "earthbound",
        "metroidfusion",
        "terraria",
        "ss"
    ],
    "new nintendo 3ds": [
        "alttp",
        "smw",
        "dkc",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "mmx3",
        "dkc3",
        "sm"
    ],
    "new": [
        "alttp",
        "smw",
        "dkc",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "mmx3",
        "dkc3",
        "sm"
    ],
    "super famicom": [
        "alttp",
        "smw",
        "ffmq",
        "dkc",
        "lufia2ac",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "yoshisisland",
        "kdl3",
        "mmx3",
        "dkc3",
        "sm"
    ],
    "famicom": [
        "alttp",
        "smw",
        "ffmq",
        "dkc",
        "lufia2ac",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "yoshisisland",
        "kdl3",
        "mmx3",
        "dkc3",
        "sm"
    ],
    "ghosts": [
        "cv64",
        "metroidprime",
        "rogue_legacy",
        "sly1",
        "cuphead",
        "alttp",
        "ffmq",
        "luigismansion",
        "papermario",
        "sotn",
        "dkc2",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "mlss",
        "lego_star_wars_tcs",
        "aus",
        "wl4",
        "tloz_ooa",
        "earthbound",
        "v6"
    ],
    "mascot": [
        "alttp",
        "tloz_ph",
        "mm3",
        "tloz_oos",
        "spyro3",
        "papermario",
        "k64",
        "tmc",
        "ladx",
        "mm2",
        "kdl3",
        "sly1",
        "jakanddaxter"
    ],
    "death": [
        "openrct2",
        "cv64",
        "dkc",
        "metroidprime",
        "star_fox_64",
        "rogue_legacy",
        "oot",
        "sly1",
        "alttp",
        "luigismansion",
        "papermario",
        "sotn",
        "zelda2",
        "cvcotm",
        "kh1",
        "tmc",
        "sms",
        "mmx3",
        "heretic",
        "mm3",
        "dk64",
        "doom_ii",
        "ladx",
        "mzm",
        "mm2",
        "tloz_ph",
        "tloz_oos",
        "ffta",
        "gstla",
        "tloz_ooa",
        "v6",
        "quake",
        "minecraft",
        "dark_souls_2",
        "metroidfusion",
        "terraria",
        "dark_souls_3"
    ],
    "maze": [
        "openrct2",
        "alttp",
        "cv64",
        "witness",
        "papermario",
        "tmc",
        "mzm",
        "ladx",
        "doom_1993"
    ],
    "backtracking": [
        "cv64",
        "metroidprime",
        "oot",
        "alttp",
        "sotn",
        "faxanadu",
        "cvcotm",
        "kh1",
        "tmc",
        "jakanddaxter",
        "undertale",
        "banjo_tooie",
        "ladx",
        "mzm",
        "tloz_ph",
        "tloz_oos",
        "ffta",
        "witness",
        "quake",
        "metroidfusion"
    ],
    "undead": [
        "heretic",
        "alttp",
        "mlss",
        "ffmq",
        "cv64",
        "tloz_ooa",
        "papermario",
        "sotn",
        "dsr",
        "tmc",
        "dark_souls_2",
        "ladx",
        "terraria",
        "oot",
        "tloz_oos"
    ],
    "campaign": [
        "alttp",
        "tloz_ooa",
        "oot",
        "zelda2",
        "tmc",
        "ladx",
        "tloz_ph",
        "ss",
        "tloz_oos"
    ],
    "pixel art": [
        "wargroove",
        "hcniko",
        "animal_well",
        "stardew_valley",
        "rogue_legacy",
        "alttp",
        "ror1",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "tmc",
        "sm",
        "mm3",
        "undertale",
        "celeste_open_world",
        "tyrian",
        "ladx",
        "mzm",
        "mm2",
        "blasphemous",
        "tloz_oos",
        "wl4",
        "timespinner",
        "crosscode",
        "v6",
        "metroidfusion",
        "celeste",
        "terraria"
    ],
    "pixel": [
        "wargroove",
        "hcniko",
        "animal_well",
        "stardew_valley",
        "rogue_legacy",
        "alttp",
        "ror1",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "tmc",
        "sm",
        "mm3",
        "undertale",
        "celeste_open_world",
        "tyrian",
        "ladx",
        "mzm",
        "mm2",
        "blasphemous",
        "tloz_oos",
        "wl4",
        "timespinner",
        "crosscode",
        "v6",
        "metroidfusion",
        "celeste",
        "terraria"
    ],
    "art": [
        "wargroove",
        "hcniko",
        "animal_well",
        "stardew_valley",
        "rogue_legacy",
        "alttp",
        "ror1",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "tmc",
        "sm",
        "mm3",
        "undertale",
        "celeste_open_world",
        "tyrian",
        "ladx",
        "mzm",
        "mm2",
        "blasphemous",
        "tloz_oos",
        "wl4",
        "timespinner",
        "crosscode",
        "v6",
        "metroidfusion",
        "celeste",
        "terraria"
    ],
    "easter egg": [
        "openrct2",
        "alttp",
        "papermario",
        "doom_ii",
        "ladx",
        "banjo_tooie",
        "apeescape",
        "metroidfusion",
        "rogue_legacy"
    ],
    "easter": [
        "openrct2",
        "alttp",
        "papermario",
        "doom_ii",
        "ladx",
        "banjo_tooie",
        "apeescape",
        "metroidfusion",
        "rogue_legacy"
    ],
    "egg": [
        "openrct2",
        "alttp",
        "papermario",
        "doom_ii",
        "ladx",
        "banjo_tooie",
        "apeescape",
        "metroidfusion",
        "rogue_legacy"
    ],
    "teleportation": [
        "pokemon_emerald",
        "alttp",
        "tloz_oos",
        "cv64",
        "pokemon_crystal",
        "doom_ii",
        "earthbound",
        "v6",
        "tmc",
        "terraria",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "giant insects": [
        "soe",
        "pokemon_emerald",
        "alttp",
        "mlss",
        "dk64",
        "dkc",
        "dkc2",
        "hk",
        "sms",
        "dkc3"
    ],
    "giant": [
        "soe",
        "pokemon_emerald",
        "alttp",
        "mlss",
        "dk64",
        "dkc",
        "dkc2",
        "hk",
        "sms",
        "dkc3"
    ],
    "insects": [
        "soe",
        "pokemon_emerald",
        "alttp",
        "mlss",
        "dk64",
        "dkc",
        "dkc2",
        "hk",
        "sms",
        "dkc3"
    ],
    "silent protagonist": [
        "dkc",
        "k64",
        "oot",
        "alttp",
        "papermario",
        "dkc2",
        "zelda2",
        "hk",
        "tmc",
        "jakanddaxter",
        "mlss",
        "ladx",
        "tloz_ph",
        "doom_1993",
        "blasphemous",
        "ultrakill",
        "tloz_oos",
        "pokemon_emerald",
        "gstla",
        "tloz_ooa",
        "quake",
        "ss"
    ],
    "silent": [
        "dkc",
        "k64",
        "oot",
        "alttp",
        "papermario",
        "dkc2",
        "zelda2",
        "hk",
        "tmc",
        "jakanddaxter",
        "mlss",
        "ladx",
        "tloz_ph",
        "doom_1993",
        "blasphemous",
        "ultrakill",
        "tloz_oos",
        "pokemon_emerald",
        "gstla",
        "tloz_ooa",
        "quake",
        "ss"
    ],
    "explosion": [
        "openrct2",
        "mk64",
        "cv64",
        "metroidprime",
        "dkc3",
        "rogue_legacy",
        "cuphead",
        "alttp",
        "ffmq",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "mmx3",
        "sm",
        "mm3",
        "doom_ii",
        "lego_star_wars_tcs",
        "mzm",
        "mm2",
        "ffta",
        "tloz_ooa",
        "quake",
        "sonic_heroes",
        "minecraft",
        "metroidfusion",
        "terraria"
    ],
    "monkey": [
        "mk64",
        "alttp",
        "dk64",
        "dkc",
        "dkc2",
        "diddy_kong_racing",
        "apeescape",
        "ladx",
        "dkc3"
    ],
    "nintendo power": [
        "alttp",
        "dkc",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "dkc3",
        "sm"
    ],
    "power": [
        "alttp",
        "dkc",
        "earthbound",
        "dkc2",
        "sm_map_rando",
        "dkc3",
        "sm"
    ],
    "world map": [
        "alttp",
        "tloz_oos",
        "pokemon_crystal",
        "dkc",
        "metroidprime",
        "v6",
        "dkc2",
        "aquaria",
        "tmc",
        "ladx",
        "tloz_ph",
        "dkc3",
        "oot",
        "jakanddaxter"
    ],
    "map": [
        "alttp",
        "tloz_oos",
        "pokemon_crystal",
        "dkc",
        "metroidprime",
        "v6",
        "dkc2",
        "aquaria",
        "tmc",
        "ladx",
        "tloz_ph",
        "dkc3",
        "oot",
        "jakanddaxter"
    ],
    "human": [
        "cv64",
        "alttp",
        "papermario",
        "sotn",
        "sc2",
        "zelda2",
        "sms",
        "simpsonshitnrun",
        "doom_ii",
        "apeescape",
        "ladx",
        "tloz_ph",
        "gstla",
        "quake",
        "dark_souls_2",
        "metroidfusion",
        "terraria",
        "dark_souls_3",
        "ss"
    ],
    "shopping": [
        "pokemon_emerald",
        "cuphead",
        "alttp",
        "mlss",
        "tloz_ooa",
        "cv64",
        "pokemon_crystal",
        "yugiohddm",
        "sotn",
        "dw1",
        "tmc",
        "lego_star_wars_tcs",
        "tloz_ph",
        "tloz_oos"
    ],
    "ice stage": [
        "mk64",
        "alttp",
        "cv64",
        "dkc",
        "wl4",
        "metroidprime",
        "dkc2",
        "tmc",
        "banjo_tooie",
        "metroidfusion",
        "terraria",
        "dkc3",
        "oot",
        "jakanddaxter"
    ],
    "ice": [
        "mk64",
        "alttp",
        "cv64",
        "dkc",
        "wl4",
        "metroidprime",
        "dkc2",
        "tmc",
        "banjo_tooie",
        "metroidfusion",
        "terraria",
        "dkc3",
        "oot",
        "jakanddaxter"
    ],
    "stage": [
        "mk64",
        "alttp",
        "smw",
        "cv64",
        "spyro3",
        "dkc",
        "wl4",
        "metroidprime",
        "dkc2",
        "sonic_heroes",
        "tmc",
        "banjo_tooie",
        "metroidfusion",
        "terraria",
        "dkc3",
        "oot",
        "jakanddaxter"
    ],
    "saving the world": [
        "alttp",
        "earthbound",
        "zelda2",
        "tmc",
        "dark_souls_2",
        "tloz_ph"
    ],
    "saving": [
        "alttp",
        "earthbound",
        "zelda2",
        "tmc",
        "dark_souls_2",
        "tloz_ph"
    ],
    "grapple": [
        "alttp",
        "metroidprime",
        "tmc",
        "lego_star_wars_tcs",
        "tloz_ph",
        "oot"
    ],
    "secret area": [
        "dkc",
        "hcniko",
        "star_fox_64",
        "tunic",
        "rogue_legacy",
        "dkc3",
        "alttp",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "diddy_kong_racing",
        "tmc",
        "sm",
        "heretic",
        "doom_ii",
        "tloz_oos",
        "witness",
        "metroidfusion"
    ],
    "secret": [
        "soe",
        "dkc",
        "hcniko",
        "star_fox_64",
        "tunic",
        "rogue_legacy",
        "dkc3",
        "alttp",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "diddy_kong_racing",
        "tmc",
        "sm",
        "heretic",
        "doom_ii",
        "tloz_oos",
        "witness",
        "metroidfusion"
    ],
    "area": [
        "dkc",
        "hcniko",
        "star_fox_64",
        "tunic",
        "rogue_legacy",
        "dkc3",
        "alttp",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "diddy_kong_racing",
        "tmc",
        "sm",
        "heretic",
        "doom_ii",
        "tloz_oos",
        "witness",
        "metroidfusion"
    ],
    "shielded enemies": [
        "alttp",
        "tloz_ooa",
        "rogue_legacy",
        "hk",
        "tmc",
        "dkc3"
    ],
    "shielded": [
        "alttp",
        "tloz_ooa",
        "rogue_legacy",
        "hk",
        "tmc",
        "dkc3"
    ],
    "enemies": [
        "alttp",
        "tloz_ooa",
        "rogue_legacy",
        "hk",
        "tmc",
        "dkc3"
    ],
    "walking through walls": [
        "alttp",
        "tloz_ooa",
        "doom_ii",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "walking": [
        "alttp",
        "tloz_ooa",
        "doom_ii",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "through": [
        "alttp",
        "tloz_ooa",
        "doom_ii",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "walls": [
        "alttp",
        "tloz_ooa",
        "doom_ii",
        "ladx",
        "oot",
        "tloz_oos"
    ],
    "villain": [
        "alttp",
        "tloz_ooa",
        "mm3",
        "papermario",
        "sotn",
        "zelda2",
        "star_fox_64",
        "kh1",
        "lego_star_wars_tcs",
        "cvcotm",
        "banjo_tooie",
        "metroidfusion",
        "tmc",
        "mm2",
        "oot",
        "tloz_oos"
    ],
    "recurring boss": [
        "pokemon_emerald",
        "alttp",
        "mm3",
        "dk64",
        "dkc",
        "papermario",
        "dkc2",
        "kh1",
        "banjo_tooie",
        "metroidfusion",
        "dkc3"
    ],
    "recurring": [
        "pokemon_emerald",
        "alttp",
        "mm3",
        "dk64",
        "dkc",
        "papermario",
        "dkc2",
        "kh1",
        "banjo_tooie",
        "metroidfusion",
        "dkc3"
    ],
    "boss": [
        "dkc",
        "mm_recomp",
        "metroidprime",
        "rogue_legacy",
        "dkc3",
        "oot",
        "cuphead",
        "alttp",
        "papermario",
        "dkc2",
        "kh1",
        "tmc",
        "sms",
        "mm3",
        "dk64",
        "doom_ii",
        "banjo_tooie",
        "tloz_ph",
        "pokemon_emerald",
        "dark_souls_2",
        "metroidfusion"
    ],
    "been here before": [
        "ffta",
        "alttp",
        "gstla",
        "tloz_ph",
        "pokemon_crystal",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "oot"
    ],
    "been": [
        "ffta",
        "alttp",
        "gstla",
        "tloz_ph",
        "pokemon_crystal",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "oot"
    ],
    "here": [
        "ffta",
        "alttp",
        "gstla",
        "tloz_ph",
        "pokemon_crystal",
        "hcniko",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "oot"
    ],
    "before": [
        "ffta",
        "alttp",
        "gstla",
        "tloz_ph",
        "pokemon_crystal",
        "tmc",
        "sms",
        "simpsonshitnrun",
        "oot"
    ],
    "sleeping": [
        "alttp",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "minecraft",
        "tmc",
        "sms"
    ],
    "merchants": [
        "candybox2",
        "alttp",
        "yugiohddm",
        "timespinner",
        "faxanadu",
        "hk",
        "terraria"
    ],
    "fetch quests": [
        "alttp",
        "metroidprime",
        "zelda2",
        "tmc",
        "ladx",
        "tloz_ph",
        "tloz_oos"
    ],
    "fetch": [
        "alttp",
        "metroidprime",
        "zelda2",
        "tmc",
        "ladx",
        "tloz_ph",
        "tloz_oos"
    ],
    "poisoning": [
        "pokemon_emerald",
        "alttp",
        "cv64",
        "pokemon_crystal",
        "papermario",
        "minecraft",
        "tmc",
        "tloz_oos"
    ],
    "status effects": [
        "pokemon_emerald",
        "alttp",
        "tloz_ooa",
        "pokemon_crystal",
        "earthbound",
        "zelda2",
        "minecraft",
        "tmc",
        "ladx",
        "dark_souls_2",
        "tloz_oos"
    ],
    "status": [
        "pokemon_emerald",
        "alttp",
        "tloz_ooa",
        "pokemon_crystal",
        "earthbound",
        "zelda2",
        "minecraft",
        "tmc",
        "ladx",
        "dark_souls_2",
        "tloz_oos"
    ],
    "effects": [
        "pokemon_emerald",
        "alttp",
        "tloz_ooa",
        "pokemon_crystal",
        "earthbound",
        "zelda2",
        "minecraft",
        "tmc",
        "ladx",
        "dark_souls_2",
        "tloz_oos"
    ],
    "damage over time": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "tloz_oos",
        "pokemon_crystal",
        "tmc",
        "tloz_ph",
        "oot",
        "jakanddaxter"
    ],
    "damage": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "tloz_oos",
        "pokemon_crystal",
        "tmc",
        "tloz_ph",
        "oot",
        "jakanddaxter"
    ],
    "over": [
        "ffta",
        "pokemon_emerald",
        "alttp",
        "tloz_oos",
        "getting_over_it",
        "pokemon_crystal",
        "tmc",
        "tloz_ph",
        "oot",
        "jakanddaxter"
    ],
    "monomyth": [
        "tloz_ph",
        "alttp",
        "mm3",
        "zelda2",
        "tmc",
        "mm2",
        "ss"
    ],
    "retroachievements": [
        "mk64",
        "cv64",
        "dkc",
        "mm_recomp",
        "metroidprime",
        "k64",
        "star_fox_64",
        "tloz",
        "dkc3",
        "oot",
        "alttp",
        "ffmq",
        "papermario",
        "lufia2ac",
        "dkc2",
        "diddy_kong_racing",
        "tetrisattack",
        "sms",
        "mmx3",
        "swr",
        "dk64",
        "sm64ex",
        "tww",
        "banjo_tooie",
        "ff4fe",
        "kdl3",
        "sm64hacks",
        "smw",
        "earthbound",
        "quake",
        "sonic_heroes"
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
        "pokemon_frlg",
        "wargroove",
        "dkc",
        "k64",
        "yoshisisland",
        "animal_well",
        "smz3",
        "oribf",
        "terraria",
        "dkc3",
        "rogue_legacy",
        "wargroove2",
        "cuphead",
        "ff1",
        "ffmq",
        "enderlilies",
        "noita",
        "faxanadu",
        "hylics2",
        "lufia2ac",
        "dkc2",
        "papermario",
        "ror1",
        "sm_map_rando",
        "sotn",
        "cvcotm",
        "hk",
        "ufo50",
        "zelda2",
        "tetrisattack",
        "messenger",
        "zillion",
        "mmx3",
        "sm",
        "mlss",
        "mm3",
        "musedash",
        "getting_over_it",
        "pokemon_crystal",
        "celeste_open_world",
        "marioland2",
        "megamix",
        "momodoramoonlitfarewell",
        "ladx",
        "mzm",
        "mm2",
        "ff4fe",
        "blasphemous",
        "kdl3",
        "aus",
        "pokemon_rb",
        "wl4",
        "pokemon_emerald",
        "smw",
        "timespinner",
        "wl",
        "v6",
        "aquaria",
        "monster_sanctuary",
        "metroidfusion",
        "celeste",
        "dlcquest",
        "spire"
    ],
    "horror": [
        "cv64",
        "mm_recomp",
        "dontstarvetogether",
        "animal_well",
        "inscryption",
        "luigismansion",
        "sotn",
        "lethal_company",
        "cvcotm",
        "getting_over_it",
        "undertale",
        "doom_ii",
        "doom_1993",
        "shivers",
        "blasphemous",
        "lunacid",
        "residentevil3remake",
        "quake",
        "residentevil2remake",
        "poe",
        "terraria"
    ],
    "survival": [
        "ror1",
        "residentevil3remake",
        "dontstarvetogether",
        "ror2",
        "residentevil2remake",
        "animal_well",
        "minecraft",
        "factorio_saws",
        "yugioh06",
        "factorio",
        "subnautica",
        "terraria",
        "rimworld",
        "raft"
    ],
    "mystery": [
        "witness",
        "pmd_eos",
        "animal_well",
        "crystal_project",
        "inscryption",
        "outer_wilds"
    ],
    "exploration": [
        "cv64",
        "hcniko",
        "metroidprime",
        "animal_well",
        "terraria",
        "tunic",
        "rogue_legacy",
        "hylics2",
        "lethal_company",
        "lingo",
        "sm_map_rando",
        "sm",
        "jakanddaxter",
        "pokemon_crystal",
        "celeste_open_world",
        "tloz_ph",
        "shorthike",
        "pokemon_emerald",
        "witness",
        "v6",
        "aquaria",
        "seaofthieves",
        "metroidfusion",
        "celeste",
        "subnautica",
        "dlcquest",
        "outer_wilds"
    ],
    "retro": [
        "cuphead",
        "terraria",
        "smo",
        "timespinner",
        "undertale",
        "celeste_open_world",
        "hylics2",
        "v6",
        "animal_well",
        "minecraft",
        "stardew_valley",
        "ufo50",
        "celeste",
        "messenger",
        "dlcquest",
        "blasphemous"
    ],
    "2d": [
        "cuphead",
        "musedash",
        "undertale",
        "sotn",
        "dontstarvetogether",
        "celeste_open_world",
        "earthbound",
        "v6",
        "sm_map_rando",
        "zelda2",
        "animal_well",
        "hk",
        "stardew_valley",
        "celeste",
        "messenger",
        "terraria",
        "blasphemous",
        "sm"
    ],
    "metroidvania": [
        "metroidprime",
        "animal_well",
        "oribf",
        "rogue_legacy",
        "enderlilies",
        "sotn",
        "faxanadu",
        "zelda2",
        "sm_map_rando",
        "cvcotm",
        "hk",
        "messenger",
        "zillion",
        "sm",
        "frogmonster",
        "crystal_project",
        "momodoramoonlitfarewell",
        "mzm",
        "blasphemous",
        "aus",
        "timespinner",
        "v6",
        "pseudoregalia",
        "aquaria",
        "monster_sanctuary",
        "dark_souls_2",
        "metroidfusion"
    ],
    "atmospheric": [
        "dontstarvetogether",
        "celeste_open_world",
        "hylics2",
        "animal_well",
        "hk",
        "frogmonster",
        "crystal_project",
        "powerwashsimulator",
        "celeste",
        "tunic",
        "shorthike"
    ],
    "relaxing": [
        "sims4",
        "hcniko",
        "animal_well",
        "powerwashsimulator",
        "stardew_valley",
        "shorthike"
    ],
    "controller support": [
        "hcniko",
        "v6",
        "animal_well",
        "hk",
        "stardew_valley",
        "tunic",
        "shorthike"
    ],
    "controller": [
        "hcniko",
        "v6",
        "animal_well",
        "hk",
        "stardew_valley",
        "tunic",
        "shorthike"
    ],
    "support": [
        "hcniko",
        "v6",
        "animal_well",
        "hk",
        "stardew_valley",
        "tunic",
        "shorthike"
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
        "sa2b",
        "spyro3",
        "sotn",
        "sonic_heroes",
        "kh2",
        "lego_star_wars_tcs",
        "apeescape",
        "dark_souls_2",
        "sadx",
        "terraria",
        "rogue_legacy"
    ],
    "3": [
        "mm3",
        "terraria",
        "sa2b",
        "spyro3",
        "residentevil3remake",
        "sotn",
        "wl",
        "sonic_heroes",
        "kh2",
        "lego_star_wars_tcs",
        "apeescape",
        "dark_souls_2",
        "mmbn3",
        "sadx",
        "kdl3",
        "rogue_legacy"
    ],
    "playstation portable": [
        "spyro3",
        "sotn",
        "apeescape"
    ],
    "portable": [
        "spyro3",
        "sotn",
        "apeescape"
    ],
    "anime": [
        "pokemon_emerald",
        "yugiohddm",
        "gstla",
        "fm",
        "musedash",
        "pokemon_crystal",
        "huniepop2",
        "dw1",
        "osu",
        "apeescape",
        "zillion",
        "huniepop",
        "wl4"
    ],
    "dinosaurs": [
        "smw",
        "smo",
        "earthbound",
        "yoshisisland",
        "banjo_tooie",
        "apeescape",
        "sms"
    ],
    "collecting": [
        "pokemon_rb",
        "pokemon_emerald",
        "pokemon_frlg",
        "pokemon_crystal",
        "zelda2",
        "mzm",
        "banjo_tooie",
        "apeescape"
    ],
    "multiple endings": [
        "cuphead",
        "cv64",
        "wl4",
        "dk64",
        "sotn",
        "doom_ii",
        "metroidprime",
        "undertale",
        "dkc2",
        "civ_6",
        "k64",
        "star_fox_64",
        "witness",
        "kh1",
        "apeescape",
        "mzm",
        "mmx3",
        "tloz_oos"
    ],
    "multiple": [
        "cv64",
        "dkc",
        "metroidprime",
        "k64",
        "civ_6",
        "star_fox_64",
        "rogue_legacy",
        "dkc3",
        "cuphead",
        "sotn",
        "dkc2",
        "kh1",
        "mmx3",
        "mlss",
        "spyro3",
        "dk64",
        "undertale",
        "doom_ii",
        "lego_star_wars_tcs",
        "apeescape",
        "mzm",
        "tloz_oos",
        "wl4",
        "witness",
        "earthbound",
        "sonic_heroes"
    ],
    "endings": [
        "cuphead",
        "cv64",
        "wl4",
        "dk64",
        "sotn",
        "doom_ii",
        "metroidprime",
        "undertale",
        "dkc2",
        "civ_6",
        "k64",
        "star_fox_64",
        "witness",
        "kh1",
        "apeescape",
        "mzm",
        "mmx3",
        "tloz_oos"
    ],
    "amnesia": [
        "xenobladex",
        "witness",
        "sonic_heroes",
        "aquaria",
        "apeescape",
        "tloz_ph"
    ],
    "voice acting": [
        "cuphead",
        "xenobladex",
        "cv64",
        "witness",
        "doom_ii",
        "huniepop2",
        "civ_6",
        "sonic_heroes",
        "dw1",
        "star_fox_64",
        "kh1",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "jakanddaxter"
    ],
    "voice": [
        "cuphead",
        "xenobladex",
        "cv64",
        "witness",
        "doom_ii",
        "huniepop2",
        "civ_6",
        "sonic_heroes",
        "dw1",
        "star_fox_64",
        "kh1",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "jakanddaxter"
    ],
    "acting": [
        "cuphead",
        "xenobladex",
        "cv64",
        "witness",
        "doom_ii",
        "huniepop2",
        "civ_6",
        "sonic_heroes",
        "dw1",
        "star_fox_64",
        "kh1",
        "apeescape",
        "sms",
        "simpsonshitnrun",
        "sly1",
        "jakanddaxter"
    ],
    "moving platforms": [
        "cv64",
        "dkc",
        "metroidprime",
        "k64",
        "dkc3",
        "sly1",
        "papermario",
        "sotn",
        "cvcotm",
        "tmc",
        "sms",
        "mmx3",
        "jakanddaxter",
        "mm3",
        "spyro3",
        "dk64",
        "apeescape",
        "ladx",
        "mm2",
        "tloz_ph",
        "blasphemous",
        "wl4",
        "v6",
        "quake",
        "sonic_heroes"
    ],
    "moving": [
        "cv64",
        "dkc",
        "metroidprime",
        "k64",
        "dkc3",
        "sly1",
        "papermario",
        "sotn",
        "cvcotm",
        "tmc",
        "sms",
        "mmx3",
        "jakanddaxter",
        "mm3",
        "spyro3",
        "dk64",
        "apeescape",
        "ladx",
        "mm2",
        "tloz_ph",
        "blasphemous",
        "wl4",
        "v6",
        "quake",
        "sonic_heroes"
    ],
    "platforms": [
        "cv64",
        "dkc",
        "metroidprime",
        "k64",
        "oribf",
        "dkc3",
        "sly1",
        "papermario",
        "sotn",
        "zelda2",
        "sm_map_rando",
        "cvcotm",
        "tmc",
        "sms",
        "mmx3",
        "sm",
        "jakanddaxter",
        "mm3",
        "spyro3",
        "dk64",
        "doom_ii",
        "apeescape",
        "ladx",
        "mm2",
        "tloz_ph",
        "blasphemous",
        "wl4",
        "v6",
        "quake",
        "sonic_heroes"
    ],
    "time trials": [
        "mk64",
        "spyro3",
        "v6",
        "diddy_kong_racing",
        "apeescape",
        "sly1"
    ],
    "trials": [
        "mk64",
        "spyro3",
        "v6",
        "diddy_kong_racing",
        "apeescape",
        "sly1"
    ],
    "aquaria": [
        "aquaria"
    ],
    "drama": [
        "aquaria",
        "undertale",
        "earthbound",
        "hades"
    ],
    "linux": [
        "openrct2",
        "bumpstik",
        "dontstarvetogether",
        "landstalker",
        "factorio_saws",
        "stardew_valley",
        "inscryption",
        "rogue_legacy",
        "ror1",
        "celeste64",
        "hk",
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "crystal_project",
        "cat_quest",
        "doom_1993",
        "overcooked2",
        "blasphemous",
        "huniepop",
        "rimworld",
        "shorthike",
        "chainedechoes",
        "shapez",
        "timespinner",
        "crosscode",
        "v6",
        "quake",
        "aquaria",
        "monster_sanctuary",
        "minecraft",
        "celeste",
        "factorio",
        "terraria",
        "osu"
    ],
    "android": [
        "osrs",
        "shapez",
        "musedash",
        "getting_over_it",
        "v6",
        "aquaria",
        "osu",
        "lego_star_wars_tcs",
        "stardew_valley",
        "cat_quest",
        "brotato",
        "subnautica",
        "terraria",
        "blasphemous",
        "balatro"
    ],
    "ios": [
        "stardew_valley",
        "osrs",
        "hades",
        "musedash",
        "getting_over_it",
        "lego_star_wars_tcs",
        "cat_quest",
        "blasphemous",
        "balatro",
        "shapez",
        "witness",
        "residentevil3remake",
        "v6",
        "aquaria",
        "residentevil2remake",
        "brotato",
        "subnautica",
        "terraria",
        "osu"
    ],
    "alternate costumes": [
        "cv64",
        "smo",
        "aquaria",
        "kh1",
        "lego_star_wars_tcs",
        "metroidfusion",
        "sms",
        "simpsonshitnrun"
    ],
    "alternate": [
        "cv64",
        "smo",
        "aquaria",
        "kh1",
        "lego_star_wars_tcs",
        "metroidfusion",
        "sms",
        "simpsonshitnrun"
    ],
    "costumes": [
        "cv64",
        "smo",
        "aquaria",
        "kh1",
        "lego_star_wars_tcs",
        "metroidfusion",
        "sms",
        "simpsonshitnrun"
    ],
    "underwater gameplay": [
        "sm64hacks",
        "mm3",
        "dkc",
        "sm64ex",
        "metroidprime",
        "smo",
        "dkc2",
        "quake",
        "aquaria",
        "kh1",
        "banjo_tooie",
        "metroidfusion",
        "subnautica",
        "mm2",
        "terraria",
        "mmx3",
        "oot",
        "sms"
    ],
    "underwater": [
        "sm64hacks",
        "mm3",
        "dkc",
        "sm64ex",
        "metroidprime",
        "smo",
        "dkc2",
        "quake",
        "aquaria",
        "kh1",
        "banjo_tooie",
        "metroidfusion",
        "subnautica",
        "mm2",
        "terraria",
        "mmx3",
        "oot",
        "sms"
    ],
    "gameplay": [
        "sm64hacks",
        "mm3",
        "dkc",
        "sm64ex",
        "metroidprime",
        "smo",
        "dkc2",
        "quake",
        "aquaria",
        "kh1",
        "banjo_tooie",
        "metroidfusion",
        "subnautica",
        "mm2",
        "terraria",
        "mmx3",
        "oot",
        "sms"
    ],
    "shape-shifting": [
        "mm_recomp",
        "metroidprime",
        "sotn",
        "k64",
        "aquaria",
        "banjo_tooie",
        "kdl3"
    ],
    "plot twist": [
        "cv64",
        "undertale",
        "aquaria",
        "kh1",
        "metroidfusion",
        "oot"
    ],
    "plot": [
        "cv64",
        "undertale",
        "aquaria",
        "kh1",
        "metroidfusion",
        "oot"
    ],
    "twist": [
        "cv64",
        "undertale",
        "aquaria",
        "kh1",
        "metroidfusion",
        "oot"
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
        "hades",
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "hylics2",
        "powerwashsimulator",
        "celeste",
        "aus"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "pokemon_frlg",
        "chainedechoes",
        "wargroove",
        "fm",
        "undertale",
        "earthbound",
        "hylics2",
        "pmd_eos",
        "civ_6",
        "monster_sanctuary",
        "crystal_project",
        "yugioh06",
        "wargroove2",
        "balatro"
    ],
    "turn-based": [
        "pokemon_frlg",
        "wargroove",
        "pmd_eos",
        "civ_6",
        "yugioh06",
        "wargroove2",
        "ffmq",
        "fm",
        "papermario",
        "hylics2",
        "mlss",
        "pokemon_crystal",
        "undertale",
        "crystal_project",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "gstla",
        "chainedechoes",
        "earthbound",
        "monster_sanctuary"
    ],
    "(tbs)": [
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "pokemon_frlg",
        "chainedechoes",
        "wargroove",
        "fm",
        "undertale",
        "earthbound",
        "hylics2",
        "pmd_eos",
        "civ_6",
        "monster_sanctuary",
        "crystal_project",
        "yugioh06",
        "wargroove2",
        "balatro"
    ],
    "card & board game": [
        "balatro",
        "yugiohddm",
        "fm",
        "yugioh06",
        "inscryption",
        "spire"
    ],
    "card": [
        "balatro",
        "yugiohddm",
        "fm",
        "yugioh06",
        "inscryption",
        "spire"
    ],
    "board": [
        "balatro",
        "yugiohddm",
        "fm",
        "yugioh06",
        "inscryption",
        "spire"
    ],
    "game": [
        "pokemon_frlg",
        "hcniko",
        "mmbn3",
        "yugioh06",
        "inscryption",
        "rogue_legacy",
        "oot",
        "fm",
        "dkc2",
        "cvcotm",
        "tmc",
        "mlss",
        "pokemon_crystal",
        "spyro3",
        "doom_ii",
        "marioland2",
        "ladx",
        "mzm",
        "mm2",
        "balatro",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "tloz_oos",
        "gstla",
        "tloz_ooa",
        "wl4",
        "yugiohddm",
        "witness",
        "wl",
        "earthbound",
        "metroidfusion",
        "spire"
    ],
    "roguelike": [
        "hades",
        "ror1",
        "pmd_eos",
        "spire",
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
        "doronko_wanko",
        "hcniko",
        "toontown",
        "rogue_legacy",
        "sly1",
        "rac2",
        "cuphead",
        "sims4",
        "luigismansion",
        "papermario",
        "lethal_company",
        "dkc2",
        "diddy_kong_racing",
        "kh1",
        "messenger",
        "zork_grand_inquisitor",
        "simpsonshitnrun",
        "jakanddaxter",
        "candybox2",
        "mlss",
        "placidplasticducksim",
        "musedash",
        "getting_over_it",
        "dk64",
        "spyro3",
        "undertale",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "overcooked2",
        "huniepop",
        "quake",
        "dw1",
        "dlcquest"
    ],
    "nintendo 64": [
        "sm64hacks",
        "mk64",
        "cv64",
        "dk64",
        "mm_recomp",
        "papermario",
        "sm64ex",
        "swr",
        "k64",
        "star_fox_64",
        "diddy_kong_racing",
        "banjo_tooie",
        "oot"
    ],
    "64": [
        "sm64hacks",
        "mk64",
        "cv64",
        "dk64",
        "mm_recomp",
        "papermario",
        "sm64ex",
        "swr",
        "k64",
        "star_fox_64",
        "diddy_kong_racing",
        "banjo_tooie",
        "oot"
    ],
    "aliens": [
        "xenobladex",
        "hcniko",
        "earthbound",
        "lethal_company",
        "metroidprime",
        "quake",
        "sc2",
        "sm_map_rando",
        "factorio_saws",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "metroidfusion",
        "mzm",
        "factorio",
        "simpsonshitnrun",
        "sm"
    ],
    "flight": [
        "xenobladex",
        "mm3",
        "spyro3",
        "dkc",
        "hylics2",
        "star_fox_64",
        "diddy_kong_racing",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "mm2",
        "terraria",
        "shorthike",
        "rogue_legacy",
        "wl4"
    ],
    "witches": [
        "tloz_ooa",
        "cv64",
        "enderlilies",
        "minecraft",
        "tmc",
        "banjo_tooie",
        "tloz_oos"
    ],
    "achievements": [
        "cuphead",
        "musedash",
        "sotn",
        "doom_ii",
        "hcniko",
        "v6",
        "huniepop2",
        "sonic_heroes",
        "hk",
        "lego_star_wars_tcs",
        "banjo_tooie",
        "dark_souls_2",
        "minecraft",
        "stardew_valley",
        "oribf",
        "tunic",
        "blasphemous",
        "shorthike"
    ],
    "talking animals": [
        "dkc",
        "hcniko",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "banjo_tooie",
        "dkc3",
        "sly1"
    ],
    "talking": [
        "dkc",
        "hcniko",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "banjo_tooie",
        "dkc3",
        "sly1"
    ],
    "animals": [
        "dkc",
        "hcniko",
        "dkc2",
        "star_fox_64",
        "diddy_kong_racing",
        "banjo_tooie",
        "dkc3",
        "sly1"
    ],
    "breaking the fourth wall": [
        "ffta",
        "mlss",
        "dkc",
        "papermario",
        "doom_ii",
        "undertale",
        "dkc2",
        "tmc",
        "banjo_tooie",
        "ladx",
        "metroidfusion",
        "simpsonshitnrun",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "breaking": [
        "dkc",
        "metroidprime",
        "rogue_legacy",
        "oot",
        "papermario",
        "sotn",
        "dkc2",
        "sm_map_rando",
        "tmc",
        "simpsonshitnrun",
        "sm",
        "jakanddaxter",
        "mlss",
        "undertale",
        "doom_ii",
        "banjo_tooie",
        "ladx",
        "mzm",
        "wl4",
        "ffta",
        "tloz_ooa",
        "metroidfusion"
    ],
    "fourth": [
        "ffta",
        "mlss",
        "dkc",
        "papermario",
        "doom_ii",
        "undertale",
        "dkc2",
        "tmc",
        "banjo_tooie",
        "ladx",
        "metroidfusion",
        "simpsonshitnrun",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "temporary invincibility": [
        "cuphead",
        "mk64",
        "papermario",
        "faxanadu",
        "doom_ii",
        "dkc2",
        "quake",
        "sonic_heroes",
        "banjo_tooie",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "temporary": [
        "cuphead",
        "mk64",
        "papermario",
        "faxanadu",
        "doom_ii",
        "dkc2",
        "quake",
        "sonic_heroes",
        "banjo_tooie",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "invincibility": [
        "cuphead",
        "mk64",
        "papermario",
        "faxanadu",
        "doom_ii",
        "dkc2",
        "quake",
        "sonic_heroes",
        "banjo_tooie",
        "rogue_legacy",
        "jakanddaxter"
    ],
    "gliding": [
        "spyro3",
        "kh1",
        "tmc",
        "banjo_tooie",
        "sms",
        "shorthike",
        "sly1"
    ],
    "lgbtq+": [
        "sims4",
        "timespinner",
        "celeste_open_world",
        "celeste64",
        "banjo_tooie",
        "celeste",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "blasphemous": [
        "blasphemous"
    ],
    "role-playing (rpg)": [
        "soe",
        "pokemon_frlg",
        "pmd_eos",
        "landstalker",
        "kh2",
        "mmbn3",
        "stardew_valley",
        "toontown",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "meritous",
        "ff1",
        "ffmq",
        "hades",
        "osrs",
        "enderlilies",
        "noita",
        "faxanadu",
        "hylics2",
        "lufia2ac",
        "papermario",
        "ror1",
        "sotn",
        "bomb_rush_cyberfunk",
        "zelda2",
        "cvcotm",
        "kh1",
        "ufo50",
        "candybox2",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "undertale",
        "ctjot",
        "crystal_project",
        "cat_quest",
        "ff4fe",
        "blasphemous",
        "huniepop",
        "tloz_oos",
        "pokemon_rb",
        "ffta",
        "lunacid",
        "pokemon_emerald",
        "gstla",
        "chainedechoes",
        "tloz_ooa",
        "timespinner",
        "crosscode",
        "earthbound",
        "dsr",
        "monster_sanctuary",
        "dw1",
        "sims4",
        "dark_souls_2",
        "poe",
        "brotato",
        "terraria",
        "dark_souls_3"
    ],
    "role-playing": [
        "soe",
        "pokemon_frlg",
        "pmd_eos",
        "landstalker",
        "kh2",
        "mmbn3",
        "stardew_valley",
        "toontown",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "meritous",
        "ff1",
        "ffmq",
        "hades",
        "osrs",
        "enderlilies",
        "noita",
        "faxanadu",
        "hylics2",
        "lufia2ac",
        "papermario",
        "ror1",
        "sotn",
        "bomb_rush_cyberfunk",
        "zelda2",
        "cvcotm",
        "kh1",
        "ufo50",
        "candybox2",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "undertale",
        "ctjot",
        "crystal_project",
        "cat_quest",
        "ff4fe",
        "blasphemous",
        "huniepop",
        "tloz_oos",
        "pokemon_rb",
        "ffta",
        "lunacid",
        "pokemon_emerald",
        "gstla",
        "chainedechoes",
        "tloz_ooa",
        "timespinner",
        "crosscode",
        "earthbound",
        "dsr",
        "monster_sanctuary",
        "dw1",
        "sims4",
        "dark_souls_2",
        "poe",
        "brotato",
        "terraria",
        "dark_souls_3"
    ],
    "(rpg)": [
        "soe",
        "pokemon_frlg",
        "pmd_eos",
        "landstalker",
        "kh2",
        "mmbn3",
        "stardew_valley",
        "toontown",
        "tunic",
        "rogue_legacy",
        "wargroove2",
        "meritous",
        "ff1",
        "ffmq",
        "hades",
        "osrs",
        "enderlilies",
        "noita",
        "faxanadu",
        "hylics2",
        "lufia2ac",
        "papermario",
        "ror1",
        "sotn",
        "bomb_rush_cyberfunk",
        "zelda2",
        "cvcotm",
        "kh1",
        "ufo50",
        "candybox2",
        "mlss",
        "xenobladex",
        "pokemon_crystal",
        "undertale",
        "ctjot",
        "crystal_project",
        "cat_quest",
        "ff4fe",
        "blasphemous",
        "huniepop",
        "tloz_oos",
        "pokemon_rb",
        "ffta",
        "lunacid",
        "pokemon_emerald",
        "gstla",
        "chainedechoes",
        "tloz_ooa",
        "timespinner",
        "crosscode",
        "earthbound",
        "dsr",
        "monster_sanctuary",
        "dw1",
        "sims4",
        "dark_souls_2",
        "poe",
        "brotato",
        "terraria",
        "dark_souls_3"
    ],
    "hack and slash/beat 'em up": [
        "hades",
        "cv64",
        "ror1",
        "poe",
        "blasphemous"
    ],
    "hack": [
        "hades",
        "cv64",
        "ror1",
        "poe",
        "blasphemous"
    ],
    "slash/beat": [
        "hades",
        "cv64",
        "ror1",
        "poe",
        "blasphemous"
    ],
    "'em": [
        "hades",
        "cv64",
        "ror1",
        "poe",
        "blasphemous"
    ],
    "up": [
        "pokemon_emerald",
        "gstla",
        "hades",
        "cv64",
        "pokemon_crystal",
        "ror1",
        "papermario",
        "sotn",
        "earthbound",
        "undertale",
        "zelda2",
        "dw1",
        "landstalker",
        "cvcotm",
        "kh1",
        "dark_souls_2",
        "poe",
        "blasphemous"
    ],
    "bloody": [
        "heretic",
        "cv64",
        "sotn",
        "metroidprime",
        "doom_ii",
        "quake",
        "residentevil2remake",
        "poe",
        "blasphemous",
        "ultrakill"
    ],
    "difficult": [
        "hades",
        "getting_over_it",
        "ror1",
        "dontstarvetogether",
        "celeste_open_world",
        "zelda2",
        "celeste",
        "messenger",
        "tunic",
        "blasphemous"
    ],
    "side-scrolling": [
        "dkc",
        "k64",
        "yoshisisland",
        "rogue_legacy",
        "dkc3",
        "cuphead",
        "sotn",
        "hylics2",
        "dkc2",
        "sm_map_rando",
        "zelda2",
        "mmx3",
        "sm",
        "mm3",
        "musedash",
        "mzm",
        "mm2",
        "kdl3",
        "blasphemous",
        "metroidfusion"
    ],
    "great soundtrack": [
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "hylics2",
        "bomb_rush_cyberfunk",
        "celeste",
        "tunic",
        "blasphemous",
        "shorthike",
        "ultrakill"
    ],
    "great": [
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "hylics2",
        "bomb_rush_cyberfunk",
        "celeste",
        "tunic",
        "blasphemous",
        "shorthike",
        "ultrakill"
    ],
    "soundtrack": [
        "getting_over_it",
        "undertale",
        "celeste_open_world",
        "hylics2",
        "bomb_rush_cyberfunk",
        "celeste",
        "tunic",
        "blasphemous",
        "shorthike",
        "ultrakill"
    ],
    "soulslike": [
        "enderlilies",
        "blasphemous",
        "dsr",
        "dark_souls_2",
        "tunic",
        "dark_souls_3"
    ],
    "you can pet the dog": [
        "sims4",
        "hades",
        "undertale",
        "seaofthieves",
        "overcooked2",
        "terraria",
        "blasphemous"
    ],
    "you": [
        "sims4",
        "hades",
        "undertale",
        "seaofthieves",
        "overcooked2",
        "terraria",
        "blasphemous"
    ],
    "can": [
        "sims4",
        "hades",
        "undertale",
        "seaofthieves",
        "overcooked2",
        "terraria",
        "blasphemous"
    ],
    "pet": [
        "sims4",
        "hades",
        "undertale",
        "seaofthieves",
        "overcooked2",
        "terraria",
        "blasphemous"
    ],
    "dog": [
        "soe",
        "doronko_wanko",
        "hades",
        "cv64",
        "sims4",
        "smo",
        "undertale",
        "hcniko",
        "star_fox_64",
        "minecraft",
        "seaofthieves",
        "tmc",
        "overcooked2",
        "terraria",
        "blasphemous",
        "oot",
        "sly1",
        "tloz_oos"
    ],
    "interconnected-world": [
        "blasphemous",
        "luigismansion",
        "sotn",
        "dsr",
        "sm_map_rando",
        "hk",
        "dark_souls_2",
        "mzm",
        "dark_souls_3",
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
        "soe",
        "pokemon_frlg",
        "metroidprime",
        "ror2",
        "star_fox_64",
        "factorio_saws",
        "mmbn3",
        "rac2",
        "ror1",
        "lethal_company",
        "sc2",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "zillion",
        "mmx3",
        "sm",
        "swr",
        "jakanddaxter",
        "xenobladex",
        "mm3",
        "doom_ii",
        "tyrian",
        "ctjot",
        "lego_star_wars_tcs",
        "mzm",
        "doom_1993",
        "mm2",
        "rimworld",
        "ultrakill",
        "witness",
        "crosscode",
        "earthbound",
        "v6",
        "quake",
        "metroidfusion",
        "brotato",
        "factorio",
        "subnautica",
        "terraria",
        "outer_wilds"
    ],
    "science": [
        "soe",
        "pokemon_frlg",
        "metroidprime",
        "ror2",
        "star_fox_64",
        "factorio_saws",
        "mmbn3",
        "rac2",
        "ror1",
        "lethal_company",
        "sc2",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "zillion",
        "mmx3",
        "sm",
        "swr",
        "jakanddaxter",
        "xenobladex",
        "mm3",
        "doom_ii",
        "tyrian",
        "ctjot",
        "lego_star_wars_tcs",
        "mzm",
        "doom_1993",
        "mm2",
        "rimworld",
        "ultrakill",
        "witness",
        "crosscode",
        "earthbound",
        "v6",
        "quake",
        "metroidfusion",
        "brotato",
        "factorio",
        "subnautica",
        "terraria",
        "outer_wilds"
    ],
    "fiction": [
        "soe",
        "pokemon_frlg",
        "metroidprime",
        "ror2",
        "star_fox_64",
        "factorio_saws",
        "mmbn3",
        "rac2",
        "ror1",
        "lethal_company",
        "sc2",
        "sm_map_rando",
        "bomb_rush_cyberfunk",
        "satisfactory",
        "zillion",
        "mmx3",
        "sm",
        "swr",
        "jakanddaxter",
        "xenobladex",
        "mm3",
        "doom_ii",
        "tyrian",
        "ctjot",
        "lego_star_wars_tcs",
        "mzm",
        "doom_1993",
        "mm2",
        "rimworld",
        "ultrakill",
        "witness",
        "crosscode",
        "earthbound",
        "v6",
        "quake",
        "metroidfusion",
        "brotato",
        "factorio",
        "subnautica",
        "terraria",
        "outer_wilds"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "metroidprime",
        "ror2",
        "star_fox_64",
        "rac2",
        "cuphead",
        "ror1",
        "noita",
        "sm_map_rando",
        "ufo50",
        "mmx3",
        "sm",
        "heretic",
        "doom_ii",
        "tyrian",
        "frogmonster",
        "mzm",
        "doom_1993",
        "ultrakill",
        "tboir",
        "crosscode",
        "residentevil3remake",
        "quake",
        "residentevil2remake",
        "metroidfusion",
        "brotato"
    ],
    "arcade": [
        "cuphead",
        "mk64",
        "smw",
        "mm3",
        "trackmania",
        "noita",
        "v6",
        "tyrian",
        "ultrakill",
        "megamix",
        "ufo50",
        "brotato",
        "messenger",
        "overcooked2",
        "osu",
        "mario_kart_double_dash"
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
    "2": [
        "candybox2",
        "smo",
        "hylics2",
        "rac2",
        "sonic_heroes",
        "ror2",
        "dw1",
        "residentevil2remake",
        "kh1",
        "kh2",
        "kindergarten_2",
        "stardew_valley",
        "wargroove2",
        "overcooked2",
        "simpsonshitnrun",
        "sly1",
        "jakanddaxter"
    ],
    "text": [
        "candybox2",
        "osrs",
        "huniepop2",
        "yugioh06",
        "huniepop"
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
        "cuphead",
        "wl4",
        "dkc2",
        "minecraft",
        "kh1",
        "tmc",
        "cat_quest",
        "tloz_oos"
    ],
    "quest": [
        "ffmq",
        "dlcquest",
        "dkc2",
        "cat_quest"
    ],
    "celeste": [
        "celeste_open_world",
        "celeste64",
        "celeste"
    ],
    "google stadia": [
        "ror2",
        "terraria",
        "celeste_open_world",
        "celeste"
    ],
    "google": [
        "ror2",
        "terraria",
        "celeste_open_world",
        "celeste"
    ],
    "stadia": [
        "ror2",
        "terraria",
        "celeste_open_world",
        "celeste"
    ],
    "story rich": [
        "hades",
        "getting_over_it",
        "undertale",
        "hylics2",
        "celeste_open_world",
        "powerwashsimulator",
        "celeste"
    ],
    "rich": [
        "hades",
        "getting_over_it",
        "undertale",
        "hylics2",
        "celeste_open_world",
        "powerwashsimulator",
        "celeste"
    ],
    "celeste 64": [
        "celeste64"
    ],
    "celeste 64: fragments of the mountain": [
        "celeste64"
    ],
    "64:": [
        "celeste64",
        "k64"
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
        "ffta",
        "chainedechoes",
        "ffmq",
        "ff1",
        "hylics2",
        "pmd_eos",
        "crystal_project",
        "ff4fe"
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
        "xenobladex",
        "cv64",
        "dk64",
        "civ_6",
        "minecraft",
        "terraria"
    ],
    "loot": [
        "xenobladex",
        "cv64",
        "dk64",
        "civ_6",
        "minecraft",
        "terraria"
    ],
    "gathering": [
        "xenobladex",
        "cv64",
        "dk64",
        "civ_6",
        "minecraft",
        "terraria"
    ],
    "ambient music": [
        "soe",
        "cv64",
        "dkc",
        "metroidprime",
        "dkc2",
        "civ_6",
        "metroidfusion",
        "mzm",
        "dkc3"
    ],
    "ambient": [
        "soe",
        "cv64",
        "dkc",
        "metroidprime",
        "dkc2",
        "civ_6",
        "metroidfusion",
        "mzm",
        "dkc3"
    ],
    "music": [
        "soe",
        "cv64",
        "dkc",
        "metroidprime",
        "civ_6",
        "dkc3",
        "ffmq",
        "sotn",
        "dkc2",
        "placidplasticducksim",
        "musedash",
        "doom_ii",
        "megamix",
        "mzm",
        "ultrakill",
        "ffta",
        "gstla",
        "sonic_heroes",
        "metroidfusion",
        "osu"
    ],
    "crosscode": [
        "crosscode"
    ],
    "crystal project": [
        "crystal_project"
    ],
    "crystal": [
        "pokemon_crystal",
        "crystal_project",
        "k64"
    ],
    "project": [
        "megamix",
        "crystal_project"
    ],
    "tactical": [
        "ffta",
        "wargroove",
        "crystal_project",
        "mmbn3",
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
        "cuphead",
        "tloz_ooa",
        "metroidprime",
        "dkc2",
        "kh1",
        "seaofthieves",
        "metroidfusion",
        "mzm",
        "tloz_ph",
        "wargroove2",
        "tloz_oos"
    ],
    "robots": [
        "cuphead",
        "xenobladex",
        "mm3",
        "earthbound",
        "sonic_heroes",
        "star_fox_64",
        "ultrakill",
        "lego_star_wars_tcs",
        "metroidfusion",
        "mm2",
        "mmx3",
        "swr",
        "sms"
    ],
    "violent plants": [
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "sms",
        "terraria",
        "rogue_legacy",
        "ss"
    ],
    "violent": [
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "sms",
        "terraria",
        "rogue_legacy",
        "ss"
    ],
    "plants": [
        "cuphead",
        "metroidprime",
        "metroidfusion",
        "sms",
        "terraria",
        "rogue_legacy",
        "ss"
    ],
    "auto-scrolling levels": [
        "cuphead",
        "dkc",
        "v6",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc3"
    ],
    "auto-scrolling": [
        "cuphead",
        "dkc",
        "v6",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc3"
    ],
    "levels": [
        "cuphead",
        "dkc",
        "v6",
        "dkc2",
        "k64",
        "star_fox_64",
        "dkc3"
    ],
    "boss assistance": [
        "cuphead",
        "tloz_ph",
        "dkc",
        "mm_recomp",
        "doom_ii",
        "metroidprime",
        "papermario",
        "dkc2",
        "tmc",
        "dark_souls_2",
        "sms",
        "rogue_legacy",
        "oot"
    ],
    "assistance": [
        "cuphead",
        "tloz_ph",
        "dkc",
        "mm_recomp",
        "doom_ii",
        "metroidprime",
        "papermario",
        "dkc2",
        "tmc",
        "dark_souls_2",
        "sms",
        "rogue_legacy",
        "oot"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "horse": [
        "cv64",
        "sotn",
        "cvcotm",
        "minecraft",
        "rogue_legacy",
        "oot"
    ],
    "multiple protagonists": [
        "mlss",
        "cv64",
        "spyro3",
        "dk64",
        "dkc",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "dkc2",
        "sonic_heroes",
        "lego_star_wars_tcs",
        "mmx3",
        "dkc3"
    ],
    "protagonists": [
        "mlss",
        "cv64",
        "spyro3",
        "dk64",
        "dkc",
        "sotn",
        "earthbound",
        "rogue_legacy",
        "dkc2",
        "sonic_heroes",
        "lego_star_wars_tcs",
        "mmx3",
        "dkc3"
    ],
    "traps": [
        "cv64",
        "doom_ii",
        "minecraft",
        "tmc",
        "metroidfusion",
        "dark_souls_2",
        "rogue_legacy"
    ],
    "bats": [
        "mk64",
        "cv64",
        "pokemon_crystal",
        "sotn",
        "zelda2",
        "cvcotm",
        "terraria"
    ],
    "day/night cycle": [
        "xenobladex",
        "cv64",
        "pokemon_crystal",
        "dk64",
        "mm_recomp",
        "sotn",
        "tww",
        "ss",
        "minecraft",
        "stardew_valley",
        "terraria",
        "oot",
        "jakanddaxter"
    ],
    "day/night": [
        "xenobladex",
        "cv64",
        "pokemon_crystal",
        "dk64",
        "mm_recomp",
        "sotn",
        "tww",
        "ss",
        "minecraft",
        "stardew_valley",
        "terraria",
        "oot",
        "jakanddaxter"
    ],
    "cycle": [
        "xenobladex",
        "cv64",
        "pokemon_crystal",
        "dk64",
        "mm_recomp",
        "sotn",
        "tww",
        "ss",
        "minecraft",
        "stardew_valley",
        "terraria",
        "oot",
        "jakanddaxter"
    ],
    "skeletons": [
        "heretic",
        "cv64",
        "undertale",
        "sotn",
        "cvcotm",
        "seaofthieves",
        "minecraft",
        "terraria",
        "sly1"
    ],
    "unstable platforms": [
        "cv64",
        "dkc",
        "metroidprime",
        "doom_ii",
        "v6",
        "zelda2",
        "sm_map_rando",
        "cvcotm",
        "tmc",
        "oribf",
        "sm",
        "sly1",
        "sms"
    ],
    "unstable": [
        "cv64",
        "dkc",
        "metroidprime",
        "doom_ii",
        "v6",
        "zelda2",
        "sm_map_rando",
        "cvcotm",
        "tmc",
        "oribf",
        "sm",
        "sly1",
        "sms"
    ],
    "melee": [
        "cv64",
        "k64",
        "tunic",
        "sly1",
        "papermario",
        "sotn",
        "cvcotm",
        "kh1",
        "tmc",
        "heretic",
        "pokemon_crystal",
        "doom_ii",
        "lego_star_wars_tcs",
        "doom_1993",
        "kdl3",
        "wl4",
        "ffta",
        "pokemon_emerald",
        "gstla",
        "quake",
        "dark_souls_2",
        "metroidfusion",
        "terraria"
    ],
    "instant kill": [
        "cv64",
        "dkc",
        "v6",
        "dkc2",
        "metroidfusion",
        "mm2"
    ],
    "instant": [
        "cv64",
        "dkc",
        "v6",
        "dkc2",
        "metroidfusion",
        "mm2"
    ],
    "kill": [
        "cv64",
        "dkc",
        "v6",
        "dkc2",
        "metroidfusion",
        "mm2"
    ],
    "difficulty level": [
        "mk64",
        "cv64",
        "musedash",
        "metroidprime",
        "doom_ii",
        "star_fox_64",
        "minecraft",
        "mzm",
        "mm2",
        "osu"
    ],
    "difficulty": [
        "mk64",
        "cv64",
        "musedash",
        "metroidprime",
        "doom_ii",
        "star_fox_64",
        "minecraft",
        "mzm",
        "mm2",
        "osu"
    ],
    "level": [
        "mk64",
        "cv64",
        "musedash",
        "dkc",
        "doom_ii",
        "metroidprime",
        "dkc2",
        "star_fox_64",
        "kh1",
        "minecraft",
        "mzm",
        "mm2",
        "osu",
        "oot",
        "sms"
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
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "gstla",
        "mlss",
        "pokemon_frlg",
        "earthbound",
        "yugioh06",
        "cvcotm",
        "tmc",
        "metroidfusion",
        "mmbn3",
        "mzm",
        "wl4"
    ],
    "boy": [
        "pokemon_frlg",
        "mmbn3",
        "yugioh06",
        "cvcotm",
        "tmc",
        "mlss",
        "pokemon_crystal",
        "marioland2",
        "ladx",
        "mzm",
        "mm2",
        "tloz_oos",
        "pokemon_rb",
        "ffta",
        "pokemon_emerald",
        "wl4",
        "gstla",
        "tloz_ooa",
        "yugiohddm",
        "wl",
        "earthbound",
        "metroidfusion"
    ],
    "advance": [
        "ffta",
        "pokemon_emerald",
        "yugiohddm",
        "gstla",
        "mlss",
        "pokemon_frlg",
        "earthbound",
        "yugioh06",
        "cvcotm",
        "tmc",
        "metroidfusion",
        "mmbn3",
        "mzm",
        "wl4"
    ],
    "gravity": [
        "dk64",
        "dkc",
        "metroidprime",
        "papermario",
        "sotn",
        "dkc2",
        "v6",
        "star_fox_64",
        "cvcotm",
        "lego_star_wars_tcs",
        "metroidfusion",
        "mzm",
        "dkc3",
        "oot"
    ],
    "leveling up": [
        "pokemon_emerald",
        "gstla",
        "pokemon_crystal",
        "undertale",
        "papermario",
        "sotn",
        "earthbound",
        "zelda2",
        "dw1",
        "landstalker",
        "cvcotm",
        "kh1",
        "dark_souls_2",
        "poe"
    ],
    "leveling": [
        "pokemon_emerald",
        "gstla",
        "pokemon_crystal",
        "undertale",
        "papermario",
        "sotn",
        "earthbound",
        "zelda2",
        "dw1",
        "landstalker",
        "cvcotm",
        "kh1",
        "dark_souls_2",
        "poe"
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
        "kh2",
        "dark_souls_2",
        "mm2",
        "ff4fe",
        "spire"
    ],
    "xbox 360": [
        "sa2b",
        "sotn",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "dlcquest",
        "sadx"
    ],
    "360": [
        "sa2b",
        "sotn",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "terraria",
        "dlcquest",
        "sadx"
    ],
    "spider": [
        "dkc2",
        "zelda2",
        "minecraft",
        "dark_souls_2",
        "oribf",
        "sly1"
    ],
    "customizable characters": [
        "xenobladex",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "stardew_valley",
        "terraria",
        "dark_souls_3"
    ],
    "customizable": [
        "xenobladex",
        "lego_star_wars_tcs",
        "dark_souls_2",
        "stardew_valley",
        "terraria",
        "dark_souls_3"
    ],
    "checkpoints": [
        "mm3",
        "dkc",
        "smo",
        "v6",
        "dkc2",
        "sonic_heroes",
        "dark_souls_2",
        "mm2",
        "mmx3",
        "dkc3",
        "sly1",
        "jakanddaxter"
    ],
    "fire manipulation": [
        "pokemon_emerald",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "minecraft",
        "dark_souls_2",
        "rogue_legacy"
    ],
    "fire": [
        "pokemon_emerald",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "minecraft",
        "dark_souls_2",
        "rogue_legacy"
    ],
    "manipulation": [
        "pokemon_emerald",
        "gstla",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "minecraft",
        "dark_souls_2",
        "rogue_legacy"
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
        "dk64",
        "dkc",
        "dkc2",
        "diddy_kong_racing",
        "dkc3"
    ],
    "racing": [
        "mk64",
        "trackmania",
        "swr",
        "diddy_kong_racing",
        "simpsonshitnrun",
        "mario_kart_double_dash",
        "jakanddaxter"
    ],
    "behind the waterfall": [
        "gstla",
        "tloz_ooa",
        "smo",
        "sotn",
        "hcniko",
        "diddy_kong_racing",
        "tmc",
        "dkc3",
        "ss"
    ],
    "behind": [
        "gstla",
        "tloz_ooa",
        "smo",
        "sotn",
        "hcniko",
        "diddy_kong_racing",
        "tmc",
        "dkc3",
        "ss"
    ],
    "waterfall": [
        "gstla",
        "tloz_ooa",
        "smo",
        "sotn",
        "hcniko",
        "diddy_kong_racing",
        "tmc",
        "dkc3",
        "ss"
    ],
    "donkey kong 64": [
        "dk64"
    ],
    "donkey": [
        "dk64",
        "dkc3",
        "dkc2",
        "dkc"
    ],
    "artificial intelligence": [
        "mk64",
        "dk64",
        "metroidprime",
        "doom_ii",
        "star_fox_64",
        "sly1",
        "jakanddaxter"
    ],
    "artificial": [
        "mk64",
        "dk64",
        "metroidprime",
        "doom_ii",
        "star_fox_64",
        "sly1",
        "jakanddaxter"
    ],
    "intelligence": [
        "mk64",
        "dk64",
        "metroidprime",
        "doom_ii",
        "star_fox_64",
        "sly1",
        "jakanddaxter"
    ],
    "completion percentage": [
        "dk64",
        "sotn",
        "metroidprime",
        "dkc2",
        "mzm",
        "metroidfusion"
    ],
    "completion": [
        "dk64",
        "sotn",
        "metroidprime",
        "dkc2",
        "mzm",
        "metroidfusion"
    ],
    "percentage": [
        "dk64",
        "sotn",
        "metroidprime",
        "dkc2",
        "mzm",
        "metroidfusion"
    ],
    "invisibility": [
        "dk64",
        "papermario",
        "doom_ii",
        "quake",
        "doom_1993",
        "sly1"
    ],
    "foreshadowing": [
        "dk64",
        "metroidprime",
        "tmc",
        "mzm",
        "metroidfusion",
        "sms"
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
        "ffta",
        "gstla",
        "ffmq",
        "dkc",
        "dkc2",
        "zelda2",
        "tloz",
        "dkc3"
    ],
    "bonus stage": [
        "smw",
        "spyro3",
        "dkc",
        "sonic_heroes",
        "dkc2",
        "dkc3"
    ],
    "bonus": [
        "smw",
        "spyro3",
        "dkc",
        "sonic_heroes",
        "dkc2",
        "dkc3"
    ],
    "water level": [
        "dkc",
        "dkc2",
        "kh1",
        "mm2",
        "oot",
        "sms"
    ],
    "water": [
        "dkc",
        "dkc2",
        "kh1",
        "mm2",
        "oot",
        "sms"
    ],
    "speedrun": [
        "sm64hacks",
        "dkc",
        "sm64ex",
        "metroidprime",
        "sotn",
        "quake",
        "metroidfusion"
    ],
    "donkey kong country 2": [
        "dkc2"
    ],
    "donkey kong country 2: diddy's kong quest": [
        "dkc2"
    ],
    "2:": [
        "sa2b",
        "huniepop2",
        "dkc2",
        "yoshisisland",
        "marioland2"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "tloz_ooa",
        "tloz_oos",
        "dkc2",
        "tmc",
        "sms",
        "terraria",
        "shorthike",
        "sly1",
        "jakanddaxter"
    ],
    "game reference": [
        "spyro3",
        "witness",
        "doom_ii",
        "hcniko",
        "dkc2",
        "tmc",
        "rogue_legacy",
        "oot"
    ],
    "reference": [
        "placidplasticducksim",
        "spyro3",
        "witness",
        "doom_ii",
        "hcniko",
        "dkc2",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy",
        "oot"
    ],
    "sprinting mechanics": [
        "sm64hacks",
        "soe",
        "pokemon_emerald",
        "pokemon_crystal",
        "sm64ex",
        "mm_recomp",
        "dkc2",
        "sms",
        "oot",
        "wl4"
    ],
    "sprinting": [
        "sm64hacks",
        "soe",
        "pokemon_emerald",
        "pokemon_crystal",
        "sm64ex",
        "mm_recomp",
        "dkc2",
        "sms",
        "oot",
        "wl4"
    ],
    "mechanics": [
        "sm64hacks",
        "soe",
        "pokemon_emerald",
        "pokemon_crystal",
        "sm64ex",
        "mm_recomp",
        "dkc2",
        "sms",
        "oot",
        "wl4"
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
        "mario_kart_double_dash",
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
        "smo",
        "timespinner",
        "v6",
        "dlcquest",
        "minecraft",
        "stardew_valley",
        "ufo50",
        "terraria"
    ],
    "deliberately": [
        "smo",
        "timespinner",
        "v6",
        "dlcquest",
        "minecraft",
        "stardew_valley",
        "ufo50",
        "terraria"
    ],
    "punctuation mark above head": [
        "pokemon_emerald",
        "tloz_ooa",
        "pokemon_crystal",
        "simpsonshitnrun",
        "tmc",
        "dlcquest",
        "rogue_legacy"
    ],
    "punctuation": [
        "pokemon_emerald",
        "tloz_ooa",
        "pokemon_crystal",
        "simpsonshitnrun",
        "tmc",
        "dlcquest",
        "rogue_legacy"
    ],
    "mark": [
        "pokemon_emerald",
        "tloz_ooa",
        "pokemon_crystal",
        "simpsonshitnrun",
        "tmc",
        "dlcquest",
        "rogue_legacy"
    ],
    "above": [
        "pokemon_emerald",
        "tloz_ooa",
        "pokemon_crystal",
        "simpsonshitnrun",
        "tmc",
        "dlcquest",
        "rogue_legacy"
    ],
    "head": [
        "pokemon_emerald",
        "tloz_ooa",
        "pokemon_crystal",
        "simpsonshitnrun",
        "tmc",
        "dlcquest",
        "rogue_legacy"
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
        "dontstarvetogether",
        "factorio_saws",
        "minecraft",
        "seaofthieves",
        "stardew_valley",
        "satisfactory",
        "factorio",
        "terraria",
        "raft"
    ],
    "funny": [
        "sims4",
        "getting_over_it",
        "undertale",
        "dontstarvetogether",
        "huniepop2",
        "powerwashsimulator",
        "shorthike"
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
        "doom_1993",
        "terraria"
    ],
    "mobile": [
        "doom_1993",
        "mmx3",
        "quake"
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
        "heretic",
        "doom_ii",
        "quake",
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
        "zelda2",
        "doom_ii",
        "lufia2ac",
        "sc2"
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
        "witness",
        "doom_ii",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "pop": [
        "placidplasticducksim",
        "witness",
        "doom_ii",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "culture": [
        "placidplasticducksim",
        "witness",
        "doom_ii",
        "tmc",
        "simpsonshitnrun",
        "rogue_legacy"
    ],
    "stat tracking": [
        "ffta",
        "witness",
        "doom_ii",
        "kh1",
        "simpsonshitnrun",
        "osu",
        "rogue_legacy"
    ],
    "stat": [
        "ffta",
        "witness",
        "doom_ii",
        "kh1",
        "simpsonshitnrun",
        "osu",
        "rogue_legacy"
    ],
    "tracking": [
        "ffta",
        "witness",
        "doom_ii",
        "kh1",
        "simpsonshitnrun",
        "osu",
        "rogue_legacy"
    ],
    "rock music": [
        "ffta",
        "gstla",
        "ffmq",
        "sotn",
        "doom_ii",
        "sonic_heroes",
        "ultrakill"
    ],
    "rock": [
        "ffta",
        "gstla",
        "ffmq",
        "sotn",
        "doom_ii",
        "sonic_heroes",
        "ultrakill"
    ],
    "sequence breaking": [
        "tloz_ooa",
        "sotn",
        "metroidprime",
        "doom_ii",
        "oot",
        "sm_map_rando",
        "tmc",
        "mzm",
        "sm",
        "wl4"
    ],
    "sequence": [
        "tloz_ooa",
        "sotn",
        "metroidprime",
        "doom_ii",
        "oot",
        "sm_map_rando",
        "tmc",
        "mzm",
        "sm",
        "wl4"
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
        "luigismansion",
        "metroidprime",
        "sonic_heroes",
        "tww",
        "dw1",
        "sms",
        "simpsonshitnrun",
        "mario_kart_double_dash"
    ],
    "gamecube": [
        "luigismansion",
        "metroidprime",
        "sonic_heroes",
        "tww",
        "dw1",
        "sms",
        "simpsonshitnrun",
        "mario_kart_double_dash"
    ],
    "playstation 2": [
        "sonic_heroes",
        "dw1",
        "kh1",
        "kh2",
        "jakanddaxter",
        "simpsonshitnrun",
        "sly1",
        "rac2"
    ],
    "earthbound": [
        "earthbound"
    ],
    "party system": [
        "ffta",
        "pokemon_emerald",
        "gstla",
        "mlss",
        "ffmq",
        "xenobladex",
        "pokemon_crystal",
        "papermario",
        "earthbound",
        "kh1"
    ],
    "party": [
        "ffta",
        "pokemon_emerald",
        "mk64",
        "gstla",
        "mlss",
        "ffmq",
        "placidplasticducksim",
        "pokemon_crystal",
        "xenobladex",
        "papermario",
        "earthbound",
        "kh1",
        "overcooked2"
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
        "faxanadu",
        "tloz",
        "ff1",
        "mm3"
    ],
    "family": [
        "ff1",
        "mm3",
        "faxanadu",
        "zelda2",
        "tloz"
    ],
    "computer": [
        "ff1",
        "mm3",
        "faxanadu",
        "zelda2",
        "tloz"
    ],
    "nintendo entertainment system": [
        "ff1",
        "mm3",
        "faxanadu",
        "zelda2",
        "tloz"
    ],
    "final fantasy": [
        "ff1"
    ],
    "final": [
        "ffta",
        "ff4fe",
        "ff1",
        "ffmq"
    ],
    "kids": [
        "pokemon_rb",
        "pokemon_emerald",
        "mk64",
        "pokemon_frlg",
        "ff1",
        "placidplasticducksim",
        "pokemon_crystal",
        "pmd_eos",
        "yoshisisland",
        "minecraft",
        "lego_star_wars_tcs",
        "tetrisattack",
        "overcooked2",
        "mario_kart_double_dash"
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
        "ffmq",
        "musedash",
        "getting_over_it",
        "sims4",
        "shorthike"
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
        "yugiohddm",
        "yugioh06",
        "fm"
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
        "hades",
        "hcniko",
        "hylics2",
        "tunic",
        "shorthike",
        "ultrakill"
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
        "hcniko",
        "minecraft",
        "ladx",
        "stardew_valley",
        "terraria",
        "shorthike"
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
        "sims4",
        "stardew_valley",
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
        "rogue_legacy",
        "quake",
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
        "marioland2",
        "kdl3",
        "wl",
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
        "sadx",
        "ladx"
    ],
    "game boy color": [
        "pokemon_crystal",
        "ladx",
        "tloz_oos",
        "tloz_ooa"
    ],
    "color": [
        "pokemon_crystal",
        "ladx",
        "tloz_oos",
        "tloz_ooa"
    ],
    "tentacles": [
        "pokemon_emerald",
        "mlss",
        "pokemon_crystal",
        "papermario",
        "metroidprime",
        "ladx",
        "sms"
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
        "zillion",
        "landstalker",
        "quake"
    ],
    "mega": [
        "mm3",
        "landstalker",
        "megamix",
        "mmbn3",
        "mm2",
        "mmx3"
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
        "lego_star_wars_tcs",
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
        "mk64",
        "mlss",
        "smw",
        "sm64ex",
        "papermario",
        "smo",
        "wl",
        "yoshisisland",
        "marioland2",
        "sms",
        "mario_kart_double_dash"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "pokemon_rb",
        "marioland2",
        "wl",
        "mm2"
    ],
    "turtle": [
        "mk64",
        "mlss",
        "papermario",
        "marioland2",
        "sms",
        "sly1"
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
        "metroidfusion",
        "smz3",
        "sm"
    ],
    "fusion": [
        "metroidfusion"
    ],
    "time limit": [
        "tloz_ph",
        "ror1",
        "witness",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "tmc",
        "metroidfusion",
        "sms",
        "simpsonshitnrun",
        "shorthike",
        "sm",
        "wl4"
    ],
    "limit": [
        "tloz_ph",
        "ror1",
        "witness",
        "metroidprime",
        "rogue_legacy",
        "sm_map_rando",
        "tmc",
        "metroidfusion",
        "sms",
        "simpsonshitnrun",
        "shorthike",
        "sm",
        "wl4"
    ],
    "countdown timer": [
        "metroidprime",
        "sm_map_rando",
        "tmc",
        "mzm",
        "metroidfusion",
        "tloz_ph",
        "simpsonshitnrun",
        "sm",
        "rogue_legacy",
        "oot",
        "wl4"
    ],
    "countdown": [
        "metroidprime",
        "sm_map_rando",
        "tmc",
        "mzm",
        "metroidfusion",
        "tloz_ph",
        "simpsonshitnrun",
        "sm",
        "rogue_legacy",
        "oot",
        "wl4"
    ],
    "timer": [
        "metroidprime",
        "sm_map_rando",
        "tmc",
        "mzm",
        "metroidfusion",
        "tloz_ph",
        "simpsonshitnrun",
        "sm",
        "rogue_legacy",
        "oot",
        "wl4"
    ],
    "isolation": [
        "sotn",
        "metroidprime",
        "sm_map_rando",
        "mzm",
        "metroidfusion",
        "sm"
    ],
    "metroid prime": [
        "metroidprime"
    ],
    "prime": [
        "metroidprime"
    ],
    "auto-aim": [
        "mm_recomp",
        "metroidprime",
        "oot",
        "quake",
        "tww",
        "ss"
    ],
    "meme origin": [
        "mm_recomp",
        "metroidprime",
        "sotn",
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz"
    ],
    "meme": [
        "mm_recomp",
        "metroidprime",
        "sotn",
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz"
    ],
    "origin": [
        "mm_recomp",
        "metroidprime",
        "sotn",
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz"
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
        "mm2",
        "mmx3",
        "mmbn3",
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
    "forest": [
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
    "nintendo switch 2": [
        "overcooked2",
        "stardew_valley",
        "smo"
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
        "pokemon_emerald",
        "pokemon_frlg",
        "pokemon_crystal",
        "pmd_eos"
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
        "pokemon_crystal",
        "pokemon_emerald",
        "pokemon_frlg",
        "pokemon_rb"
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
        "residentevil2remake",
        "residentevil3remake"
    ],
    "evil": [
        "residentevil2remake",
        "residentevil3remake"
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
        "timespinner",
        "undertale",
        "v6",
        "stardew_valley",
        "terraria",
        "rogue_legacy"
    ],
    "vita": [
        "ror1",
        "timespinner",
        "undertale",
        "v6",
        "stardew_valley",
        "terraria",
        "rogue_legacy"
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
        "wargroove",
        "sc2",
        "wargroove2"
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
        "sm",
        "sm_map_rando"
    ],
    "super mario 64": [
        "sm64hacks",
        "sm64ex"
    ],
    "rabbit": [
        "sm64hacks",
        "tloz_ooa",
        "sm64ex",
        "smo",
        "sonic_heroes",
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
        "wargroove",
        "wargroove2"
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