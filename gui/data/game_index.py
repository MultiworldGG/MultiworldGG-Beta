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
    
    def get_game(self, game_name: str) -> dict:
        """
        Get full game data for a specific game.
        
        Args:
            game_name: The name of the game to retrieve
            
        Returns:
            Dictionary containing all game data
        """
        return self.games.get(game_name, {})
    
    def get_all_games(self) -> dict:
        """
        Get all game data.
        
        Returns:
            Dictionary containing all games and their data
        """
        return self.games.copy()

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
            "bees",
            "link",
            "zelda",
            "legend of zelda"
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
            "dimension travel",
            "fetch quests",
            "kidnapping",
            "poisoning",
            "time paradox",
            "fast traveling",
            "context sensitive",
            "living inventory",
            "status effects",
            "hidden room",
            "another world",
            "damage over time",
            "monomyth",
            "buddy system",
            "retroachievements",
            "bees",
            "popular",
            "zelda",
            "link"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co4pcj.jpg",
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
            "human",
            "pick your gender",
            "parrying",
            "sliding down ladders",
            "entering world in a painting",
            "soulslike",
            "interconnected-world",
            "popular"
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
            "hidden room",
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
            "pc (microsoft windows)"
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
            "16-bit",
            "turn-based",
            "robots",
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
            "turn-based strategy (tbs)",
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
            "turn-based strategy (tbs)",
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
            "summoning support"
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
            "interconnected-world",
            "popular"
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
            "coming of age",
            "moving platforms",
            "temporary invincibility",
            "spiky-haired protagonist",
            "ancient advanced civilization technology",
            "time paradox",
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
            "villain",
            "recurring boss",
            "water level",
            "invisible wall",
            "plot twist",
            "villain turned good",
            "spiky-haired protagonist",
            "gliding",
            "random encounter",
            "whale"
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
        "keywords": [
            "popular"
        ],
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
            "link",
            "zelda",
            "legend of zelda"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co991n.jpg",
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
            "difficult"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co8fu6.jpg",
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
            "construction",
            "fishing",
            "crafting",
            "death",
            "procedural generation",
            "horse",
            "chicken",
            "action-adventure",
            "achievements",
            "traps",
            "snow",
            "wolf",
            "mining",
            "swimming",
            "day/night cycle",
            "darkness",
            "explosion",
            "digital distribution",
            "spider",
            "cat",
            "language selection",
            "polygonal 3d",
            "bow and arrow",
            "deliberately retro",
            "falling damage",
            "stereoscopic 3d",
            "potion",
            "auto-saving",
            "real-time combat",
            "difficulty level",
            "multiple gameplay perspectives",
            "rpg elements",
            "sleeping",
            "meme origin",
            "fire manipulation",
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
            "polygonal 3d",
            "ice stage",
            "difficulty level",
            "invisible wall",
            "temporary invincibility",
            "time trials",
            "italian accent",
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
            "explosion",
            "psone classics",
            "upgradeable weapons",
            "checkpoints",
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
            "role-playing (rpg)"
        ],
        "themes": [
            "action",
            "science fiction"
        ],
        "platforms": [
            "wii u",
            "game boy advance"
        ],
        "storyline": "",
        "keywords": [],
        "release_date": "2002"
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
            "time paradox",
            "fast traveling",
            "censored version",
            "context sensitive",
            "living inventory",
            "damage over time",
            "retroachievements",
            "popular",
            "link",
            "zelda",
            "legend of zelda"
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
            "creature compendium",
            "status effects",
            "damage over time",
            "popular"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1j6x.jpg",
        "game_name": "Rimworld",
        "igdb_name": "rimworld",
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
            "resized enemy",
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
        "release_date": "2019"
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
            "mercenary",
            "popular"
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
            "princess peach",
            "popular"
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
            "deliberately retro",
            "checkpoints",
            "underwater gameplay",
            "wiggler",
            "behind the waterfall",
            "entering world in a painting"
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
            "princess peach"
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
            "monomyth",
            "link",
            "zelda",
            "legend of zelda"
        ],
        "release_date": "2011"
    },
    "stardew_valley": {
        "igdb_id": "17000",
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/xrpmydnu9rpxvxfjkiu7.jpg",
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
            "popular"
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
        "cover_url": "https://images.igdb.com/igdb/image/upload/t_thumb/co1iqw.jpg",
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
            "role-playing (rpg)",
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
            "meme origin"
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
            "time paradox",
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
            "damage over time",
            "zelda",
            "legend of zelda",
            "link"
        ],
        "release_date": "2001"
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
            "link",
            "zelda",
            "legend of zelda"
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
            "living inventory",
            "link",
            "zelda",
            "legend of zelda"
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
        "rating": [],
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
            "pc (microsoft windows)"
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
            "darkness",
            "digital distribution",
            "voice acting",
            "polygonal 3d",
            "pop culture reference",
            "game reference",
            "auto-saving",
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
            "monomyth",
            "link",
            "zelda"
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
    "adventure": [
        "sm64hacks",
        "hades",
        "minecraft",
        "dontstarvetogether",
        "hk",
        "messenger",
        "tloz_ooa",
        "residentevil2remake",
        "monster_sanctuary",
        "wl4",
        "tp",
        "satisfactory",
        "sly1",
        "shivers",
        "kh2",
        "inscryption",
        "timespinner",
        "cuphead",
        "earthbound",
        "dark_souls_2",
        "luigismansion",
        "tunic",
        "mzm",
        "blasphemous",
        "terraria",
        "spyro3",
        "ror2",
        "seaofthieves",
        "pokemon_emerald",
        "pokemon_frlg",
        "dlcquest",
        "rogue_legacy",
        "smo",
        "mm2",
        "ffmq",
        "celeste64",
        "witness",
        "kh1",
        "subnautica",
        "cat_quest",
        "albw",
        "shorthike",
        "sm",
        "animal_well",
        "ff1",
        "oot",
        "cvcotm",
        "mm_recomp",
        "dsr",
        "sms",
        "v6",
        "mlss",
        "sadx",
        "aquaria",
        "dkc3",
        "sm_map_rando",
        "xenobladex",
        "hylics2",
        "dw1",
        "banjo_tooie",
        "faxanadu",
        "outer_wilds",
        "alttp",
        "smw",
        "ror1",
        "sotn",
        "getting_over_it",
        "k64",
        "momodoramoonlitfarewell",
        "chainedechoes",
        "dk64",
        "ahit",
        "osrs",
        "rac2",
        "aus",
        "metroidprime",
        "sm64ex",
        "celeste",
        "pokemon_crystal",
        "gstla",
        "sonic_heroes",
        "tww",
        "pokemon_rb",
        "cv64",
        "lingo",
        "tloz",
        "oribf",
        "stardew_valley",
        "ss",
        "tloz_oos",
        "peaks_of_yore",
        "crosscode",
        "smz3",
        "undertale",
        "jakanddaxter",
        "pseudoregalia",
        "bomb_rush_cyberfunk",
        "sa2b",
        "adventure",
        "noita",
        "zork_grand_inquisitor",
        "hcniko",
        "ladx",
        "residentevil3remake",
        "enderlilies",
        "ff4fe",
        "zelda2",
        "raft",
        "dark_souls_3",
        "ufo50",
        "kdl3",
        "papermario"
    ],
    "bird view / isometric": [
        "ctjot",
        "tloz_oos",
        "hades",
        "mmbn3",
        "wargroove",
        "wargroove2",
        "dontstarvetogether",
        "dungeon_clawler",
        "chainedechoes",
        "ffmq",
        "tyrian",
        "crosscode",
        "smz3",
        "rimworld",
        "osrs",
        "tloz_ooa",
        "albw",
        "shapez",
        "undertale",
        "placidplasticducksim",
        "shorthike",
        "ff1",
        "civ_6",
        "sms",
        "pokemon_crystal",
        "inscryption",
        "against_the_storm",
        "adventure",
        "balatro",
        "gstla",
        "factorio",
        "yugioh06",
        "sonic_heroes",
        "cuphead",
        "sc2",
        "yugiohddm",
        "ffta",
        "overcooked2",
        "pmd_eos",
        "earthbound",
        "ladx",
        "meritous",
        "landstalker",
        "pokemon_rb",
        "tboir",
        "openrct2",
        "hylics2",
        "dw1",
        "ff4fe",
        "tunic",
        "brotato",
        "factorio_saws",
        "spyro3",
        "sims4",
        "tloz",
        "alttp",
        "ufo50",
        "diddy_kong_racing",
        "pokemon_emerald",
        "soe",
        "stardew_valley",
        "pokemon_frlg"
    ],
    "fantasy": [
        "sm64hacks",
        "ctjot",
        "yoshisisland",
        "hades",
        "wargroove",
        "wargroove2",
        "minecraft",
        "hk",
        "dungeon_clawler",
        "monster_sanctuary",
        "tp",
        "kh2",
        "timespinner",
        "cuphead",
        "earthbound",
        "huniepop",
        "dark_souls_2",
        "tunic",
        "blasphemous",
        "terraria",
        "seaofthieves",
        "pokemon_emerald",
        "pokemon_frlg",
        "fm",
        "rogue_legacy",
        "smo",
        "heretic",
        "ffmq",
        "kh1",
        "cat_quest",
        "albw",
        "shorthike",
        "ff1",
        "oot",
        "mm_recomp",
        "dsr",
        "v6",
        "mlss",
        "yugioh06",
        "aquaria",
        "ffta",
        "spire",
        "hylics2",
        "banjo_tooie",
        "faxanadu",
        "sims4",
        "alttp",
        "smw",
        "ror1",
        "chainedechoes",
        "ahit",
        "osrs",
        "sm64ex",
        "celeste",
        "pokemon_crystal",
        "gstla",
        "pmd_eos",
        "tww",
        "pokemon_rb",
        "tloz",
        "oribf",
        "stardew_valley",
        "ss",
        "tloz_oos",
        "lufia2ac",
        "ultrakill",
        "dkc2",
        "undertale",
        "civ_6",
        "pseudoregalia",
        "against_the_storm",
        "adventure",
        "noita",
        "zork_grand_inquisitor",
        "ladx",
        "enderlilies",
        "landstalker",
        "yugiohddm",
        "ff4fe",
        "zelda2",
        "dark_souls_3",
        "papermario"
    ],
    "against the storm": [
        "against_the_storm"
    ],
    "against": [
        "against_the_storm"
    ],
    "storm": [
        "against_the_storm"
    ],
    "real time strategy": [
        "sc2",
        "against_the_storm",
        "rimworld",
        "openrct2"
    ],
    "rts": [
        "sc2",
        "against_the_storm",
        "rimworld",
        "openrct2"
    ],
    "simulator": [
        "getting_over_it",
        "minecraft",
        "dontstarvetogether",
        "dungeon_clawler",
        "rimworld",
        "shapez",
        "placidplasticducksim",
        "civ_6",
        "satisfactory",
        "powerwashsimulator",
        "against_the_storm",
        "noita",
        "factorio",
        "overcooked2",
        "huniepop2",
        "huniepop",
        "doronko_wanko",
        "openrct2",
        "terraria",
        "factorio_saws",
        "sims4",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "stardew_valley"
    ],
    "indie": [
        "dlcquest",
        "rogue_legacy",
        "hades",
        "getting_over_it",
        "peaks_of_yore",
        "wargroove",
        "wargroove2",
        "musedash",
        "dontstarvetogether",
        "hk",
        "momodoramoonlitfarewell",
        "dungeon_clawler",
        "lethal_company",
        "messenger",
        "chainedechoes",
        "crosscode",
        "ultrakill",
        "celeste64",
        "ahit",
        "rimworld",
        "witness",
        "subnautica",
        "cat_quest",
        "aus",
        "shapez",
        "undertale",
        "monster_sanctuary",
        "shorthike",
        "animal_well",
        "celeste",
        "satisfactory",
        "v6",
        "powerwashsimulator",
        "pseudoregalia",
        "shivers",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "against_the_storm",
        "noita",
        "balatro",
        "factorio",
        "aquaria",
        "cuphead",
        "huniepop2",
        "overcooked2",
        "spire",
        "hcniko",
        "osu",
        "huniepop",
        "enderlilies",
        "tboir",
        "hylics2",
        "blasphemous",
        "terraria",
        "brotato",
        "factorio_saws",
        "ror2",
        "outer_wilds",
        "raft",
        "ufo50",
        "stardew_valley",
        "ror1",
        "tunic"
    ],
    "xbox series xs": [
        "hades",
        "wargroove2",
        "momodoramoonlitfarewell",
        "subnautica",
        "residentevil2remake",
        "placidplasticducksim",
        "animal_well",
        "satisfactory",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "against_the_storm",
        "balatro",
        "residentevil3remake",
        "enderlilies",
        "brotato",
        "ror2",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "tunic",
        "trackmania"
    ],
    "xbox": [
        "dlcquest",
        "rogue_legacy",
        "hades",
        "swr",
        "wargroove",
        "wargroove2",
        "hk",
        "momodoramoonlitfarewell",
        "messenger",
        "chainedechoes",
        "trackmania",
        "crosscode",
        "ahit",
        "witness",
        "subnautica",
        "residentevil2remake",
        "undertale",
        "monster_sanctuary",
        "placidplasticducksim",
        "shorthike",
        "animal_well",
        "celeste",
        "dsr",
        "satisfactory",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "sa2b",
        "against_the_storm",
        "balatro",
        "sadx",
        "sonic_heroes",
        "cuphead",
        "overcooked2",
        "residentevil3remake",
        "dark_souls_2",
        "enderlilies",
        "dw1",
        "blasphemous",
        "terraria",
        "brotato",
        "ror2",
        "sims4",
        "outer_wilds",
        "raft",
        "dark_souls_3",
        "oribf",
        "seaofthieves",
        "stardew_valley",
        "ror1",
        "tunic",
        "sotn"
    ],
    "series": [
        "hades",
        "wargroove2",
        "momodoramoonlitfarewell",
        "subnautica",
        "residentevil2remake",
        "placidplasticducksim",
        "animal_well",
        "satisfactory",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "against_the_storm",
        "balatro",
        "doom_ii",
        "residentevil3remake",
        "enderlilies",
        "brotato",
        "ror2",
        "doom_1993",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "tunic",
        "trackmania"
    ],
    "pc (microsoft windows)": [
        "hades",
        "toontown",
        "wargroove",
        "wargroove2",
        "musedash",
        "minecraft",
        "bumpstik",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "messenger",
        "residentevil2remake",
        "monster_sanctuary",
        "satisfactory",
        "shivers",
        "inscryption",
        "timespinner",
        "cuphead",
        "doom_ii",
        "overcooked2",
        "osu",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "blasphemous",
        "terraria",
        "ror2",
        "seaofthieves",
        "dlcquest",
        "rogue_legacy",
        "heretic",
        "lethal_company",
        "celeste64",
        "rimworld",
        "witness",
        "subnautica",
        "cat_quest",
        "shorthike",
        "animal_well",
        "dsr",
        "v6",
        "powerwashsimulator",
        "sadx",
        "aquaria",
        "spire",
        "hylics2",
        "factorio_saws",
        "sims4",
        "outer_wilds",
        "ror1",
        "trackmania",
        "getting_over_it",
        "momodoramoonlitfarewell",
        "chainedechoes",
        "ahit",
        "osrs",
        "aus",
        "shapez",
        "celeste",
        "gzdoom",
        "balatro",
        "sonic_heroes",
        "tyrian",
        "doronko_wanko",
        "openrct2",
        "brotato",
        "lingo",
        "oribf",
        "stardew_valley",
        "peaks_of_yore",
        "swr",
        "crosscode",
        "ultrakill",
        "undertale",
        "placidplasticducksim",
        "civ_6",
        "pseudoregalia",
        "bomb_rush_cyberfunk",
        "sa2b",
        "against_the_storm",
        "noita",
        "factorio",
        "sc2",
        "zork_grand_inquisitor",
        "huniepop2",
        "hcniko",
        "residentevil3remake",
        "enderlilies",
        "landstalker",
        "raft",
        "dark_souls_3",
        "ufo50",
        "tunic"
    ],
    "pc": [
        "hades",
        "toontown",
        "wargroove",
        "wargroove2",
        "musedash",
        "minecraft",
        "bumpstik",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "messenger",
        "residentevil2remake",
        "monster_sanctuary",
        "satisfactory",
        "shivers",
        "inscryption",
        "timespinner",
        "cuphead",
        "doom_ii",
        "overcooked2",
        "osu",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "blasphemous",
        "terraria",
        "ror2",
        "seaofthieves",
        "dlcquest",
        "rogue_legacy",
        "heretic",
        "lethal_company",
        "celeste64",
        "rimworld",
        "witness",
        "subnautica",
        "cat_quest",
        "shorthike",
        "animal_well",
        "dsr",
        "v6",
        "powerwashsimulator",
        "sadx",
        "aquaria",
        "spire",
        "hylics2",
        "factorio_saws",
        "sims4",
        "outer_wilds",
        "ror1",
        "trackmania",
        "getting_over_it",
        "momodoramoonlitfarewell",
        "chainedechoes",
        "ahit",
        "osrs",
        "aus",
        "shapez",
        "celeste",
        "gzdoom",
        "balatro",
        "sonic_heroes",
        "tyrian",
        "doronko_wanko",
        "openrct2",
        "brotato",
        "lingo",
        "oribf",
        "stardew_valley",
        "peaks_of_yore",
        "swr",
        "crosscode",
        "ultrakill",
        "undertale",
        "placidplasticducksim",
        "civ_6",
        "pseudoregalia",
        "bomb_rush_cyberfunk",
        "sa2b",
        "against_the_storm",
        "noita",
        "factorio",
        "sc2",
        "zork_grand_inquisitor",
        "huniepop2",
        "hcniko",
        "residentevil3remake",
        "enderlilies",
        "landstalker",
        "raft",
        "dark_souls_3",
        "ufo50",
        "tunic"
    ],
    "windows": [
        "hades",
        "toontown",
        "wargroove",
        "wargroove2",
        "musedash",
        "minecraft",
        "bumpstik",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "messenger",
        "residentevil2remake",
        "monster_sanctuary",
        "satisfactory",
        "shivers",
        "inscryption",
        "timespinner",
        "cuphead",
        "doom_ii",
        "overcooked2",
        "osu",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "blasphemous",
        "terraria",
        "ror2",
        "seaofthieves",
        "dlcquest",
        "rogue_legacy",
        "heretic",
        "lethal_company",
        "celeste64",
        "rimworld",
        "witness",
        "subnautica",
        "cat_quest",
        "shorthike",
        "animal_well",
        "dsr",
        "v6",
        "powerwashsimulator",
        "sadx",
        "aquaria",
        "spire",
        "hylics2",
        "factorio_saws",
        "sims4",
        "outer_wilds",
        "ror1",
        "trackmania",
        "getting_over_it",
        "momodoramoonlitfarewell",
        "chainedechoes",
        "ahit",
        "osrs",
        "aus",
        "shapez",
        "celeste",
        "gzdoom",
        "balatro",
        "sonic_heroes",
        "tyrian",
        "doronko_wanko",
        "openrct2",
        "brotato",
        "lingo",
        "oribf",
        "stardew_valley",
        "peaks_of_yore",
        "swr",
        "crosscode",
        "ultrakill",
        "undertale",
        "placidplasticducksim",
        "civ_6",
        "pseudoregalia",
        "bomb_rush_cyberfunk",
        "sa2b",
        "against_the_storm",
        "noita",
        "factorio",
        "sc2",
        "zork_grand_inquisitor",
        "huniepop2",
        "hcniko",
        "residentevil3remake",
        "enderlilies",
        "landstalker",
        "raft",
        "dark_souls_3",
        "ufo50",
        "tunic"
    ],
    "playstation5": [
        "hades",
        "momodoramoonlitfarewell",
        "messenger",
        "crosscode",
        "subnautica",
        "residentevil2remake",
        "placidplasticducksim",
        "animal_well",
        "satisfactory",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "against_the_storm",
        "balatro",
        "residentevil3remake",
        "brotato",
        "ror2",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "tunic",
        "trackmania"
    ],
    "ps5": [
        "hades",
        "momodoramoonlitfarewell",
        "messenger",
        "crosscode",
        "subnautica",
        "residentevil2remake",
        "placidplasticducksim",
        "animal_well",
        "satisfactory",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "against_the_storm",
        "balatro",
        "residentevil3remake",
        "brotato",
        "ror2",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "tunic",
        "trackmania"
    ],
    "nintendo switch": [
        "rogue_legacy",
        "smo",
        "hades",
        "swr",
        "wargroove",
        "wargroove2",
        "musedash",
        "dontstarvetogether",
        "hk",
        "momodoramoonlitfarewell",
        "messenger",
        "chainedechoes",
        "crosscode",
        "ahit",
        "subnautica",
        "megamix",
        "cat_quest",
        "undertale",
        "monster_sanctuary",
        "placidplasticducksim",
        "shorthike",
        "animal_well",
        "celeste",
        "dsr",
        "v6",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "against_the_storm",
        "balatro",
        "factorio",
        "cuphead",
        "overcooked2",
        "hcniko",
        "enderlilies",
        "tboir",
        "blasphemous",
        "terraria",
        "brotato",
        "ror2",
        "outer_wilds",
        "oribf",
        "stardew_valley",
        "ror1",
        "tunic"
    ],
    "base building": [
        "shapez",
        "against_the_storm",
        "rimworld",
        "satisfactory"
    ],
    "roguelite": [
        "hades",
        "brotato",
        "noita",
        "against_the_storm",
        "ror2",
        "dungeon_clawler",
        "ror1"
    ],
    "a hat in time": [
        "ahit"
    ],
    "first person": [
        "heretic",
        "swr",
        "minecraft",
        "lethal_company",
        "ultrakill",
        "ahit",
        "witness",
        "subnautica",
        "metroidprime",
        "satisfactory",
        "powerwashsimulator",
        "shivers",
        "inscryption",
        "zork_grand_inquisitor",
        "doom_ii",
        "huniepop2",
        "earthbound",
        "huniepop",
        "yugiohddm",
        "cv64",
        "hylics2",
        "lingo",
        "doom_1993",
        "sims4",
        "outer_wilds",
        "raft",
        "seaofthieves",
        "star_fox_64",
        "fm",
        "trackmania"
    ],
    "third person": [
        "sm64hacks",
        "ss",
        "smo",
        "toontown",
        "getting_over_it",
        "swr",
        "minecraft",
        "dk64",
        "apeescape",
        "celeste64",
        "ahit",
        "kh1",
        "megamix",
        "cat_quest",
        "rac2",
        "albw",
        "residentevil2remake",
        "placidplasticducksim",
        "oot",
        "sm64ex",
        "mm_recomp",
        "dsr",
        "sms",
        "sly1",
        "jakanddaxter",
        "tp",
        "pseudoregalia",
        "kh2",
        "bomb_rush_cyberfunk",
        "sa2b",
        "gzdoom",
        "gstla",
        "mario_kart_double_dash",
        "sadx",
        "sonic_heroes",
        "hcniko",
        "residentevil3remake",
        "tww",
        "dark_souls_2",
        "luigismansion",
        "cv64",
        "hylics2",
        "dw1",
        "xenobladex",
        "banjo_tooie",
        "spyro3",
        "ror2",
        "sims4",
        "star_fox_64",
        "raft",
        "dark_souls_3",
        "mk64",
        "diddy_kong_racing",
        "soe",
        "papermario",
        "trackmania"
    ],
    "platform": [
        "dlcquest",
        "sm64hacks",
        "wl",
        "rogue_legacy",
        "smo",
        "yoshisisland",
        "peaks_of_yore",
        "getting_over_it",
        "hk",
        "k64",
        "mm2",
        "momodoramoonlitfarewell",
        "messenger",
        "dk64",
        "apeescape",
        "celeste64",
        "ahit",
        "smz3",
        "ultrakill",
        "dkc2",
        "rac2",
        "aus",
        "zillion",
        "metroidprime",
        "monster_sanctuary",
        "dkc",
        "animal_well",
        "sm",
        "sm64ex",
        "cvcotm",
        "celeste",
        "wl4",
        "sms",
        "sly1",
        "jakanddaxter",
        "v6",
        "pseudoregalia",
        "marioland2",
        "bomb_rush_cyberfunk",
        "timespinner",
        "sa2b",
        "gzdoom",
        "sadx",
        "sonic_heroes",
        "aquaria",
        "cuphead",
        "hcniko",
        "dkc3",
        "enderlilies",
        "sm_map_rando",
        "cv64",
        "hylics2",
        "mzm",
        "blasphemous",
        "terraria",
        "zelda2",
        "banjo_tooie",
        "spyro3",
        "faxanadu",
        "oribf",
        "ufo50",
        "smw",
        "kdl3",
        "ror1",
        "sotn"
    ],
    "action": [
        "sm64hacks",
        "ctjot",
        "yoshisisland",
        "hades",
        "musedash",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "messenger",
        "tloz_ooa",
        "residentevil2remake",
        "monster_sanctuary",
        "wl4",
        "tp",
        "sly1",
        "kh2",
        "timespinner",
        "cuphead",
        "doom_ii",
        "overcooked2",
        "earthbound",
        "osu",
        "dark_souls_2",
        "luigismansion",
        "tunic",
        "mzm",
        "blasphemous",
        "terraria",
        "spyro3",
        "ror2",
        "seaofthieves",
        "pokemon_emerald",
        "soe",
        "pokemon_frlg",
        "dlcquest",
        "rogue_legacy",
        "smo",
        "mm2",
        "lethal_company",
        "ffmq",
        "apeescape",
        "celeste64",
        "kh1",
        "cat_quest",
        "albw",
        "dkc",
        "animal_well",
        "ff1",
        "oot",
        "sm",
        "cvcotm",
        "mm_recomp",
        "dsr",
        "sms",
        "v6",
        "mlss",
        "sadx",
        "dkc3",
        "sm_map_rando",
        "xenobladex",
        "dw1",
        "banjo_tooie",
        "doom_1993",
        "faxanadu",
        "outer_wilds",
        "sims4",
        "alttp",
        "star_fox_64",
        "smw",
        "ror1",
        "sotn",
        "trackmania",
        "mmbn3",
        "getting_over_it",
        "k64",
        "momodoramoonlitfarewell",
        "chainedechoes",
        "dk64",
        "ahit",
        "rac2",
        "aus",
        "metroidprime",
        "sm64ex",
        "celeste",
        "pokemon_crystal",
        "gzdoom",
        "gstla",
        "mario_kart_double_dash",
        "sonic_heroes",
        "tww",
        "tyrian",
        "doronko_wanko",
        "pokemon_rb",
        "cv64",
        "tetrisattack",
        "brotato",
        "tloz",
        "oribf",
        "ss",
        "wl",
        "tloz_oos",
        "peaks_of_yore",
        "swr",
        "crosscode",
        "smz3",
        "ultrakill",
        "dkc2",
        "jakanddaxter",
        "pseudoregalia",
        "marioland2",
        "bomb_rush_cyberfunk",
        "sa2b",
        "noita",
        "sc2",
        "hcniko",
        "ladx",
        "residentevil3remake",
        "enderlilies",
        "landstalker",
        "ff4fe",
        "zelda2",
        "dark_souls_3",
        "mk64",
        "diddy_kong_racing",
        "ufo50",
        "kdl3",
        "papermario"
    ],
    "playstation4": [
        "rogue_legacy",
        "hades",
        "swr",
        "wargroove",
        "hk",
        "messenger",
        "chainedechoes",
        "crosscode",
        "ahit",
        "witness",
        "subnautica",
        "cat_quest",
        "residentevil2remake",
        "undertale",
        "monster_sanctuary",
        "placidplasticducksim",
        "shorthike",
        "celeste",
        "dsr",
        "v6",
        "jakanddaxter",
        "powerwashsimulator",
        "kh2",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "balatro",
        "cuphead",
        "overcooked2",
        "residentevil3remake",
        "enderlilies",
        "blasphemous",
        "terraria",
        "brotato",
        "ror2",
        "sims4",
        "outer_wilds",
        "dark_souls_3",
        "stardew_valley",
        "ror1",
        "tunic",
        "trackmania"
    ],
    "ps4": [
        "rogue_legacy",
        "hades",
        "swr",
        "wargroove",
        "hk",
        "messenger",
        "chainedechoes",
        "crosscode",
        "ahit",
        "witness",
        "subnautica",
        "cat_quest",
        "residentevil2remake",
        "undertale",
        "monster_sanctuary",
        "placidplasticducksim",
        "shorthike",
        "celeste",
        "wl4",
        "dsr",
        "v6",
        "jakanddaxter",
        "powerwashsimulator",
        "kh2",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "balatro",
        "cuphead",
        "overcooked2",
        "residentevil3remake",
        "enderlilies",
        "dw1",
        "blasphemous",
        "terraria",
        "brotato",
        "ror2",
        "sims4",
        "outer_wilds",
        "dark_souls_3",
        "stardew_valley",
        "ror1",
        "tunic",
        "trackmania"
    ],
    "mac": [
        "dlcquest",
        "rogue_legacy",
        "hades",
        "getting_over_it",
        "heretic",
        "toontown",
        "swr",
        "musedash",
        "minecraft",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "chainedechoes",
        "crosscode",
        "rimworld",
        "ahit",
        "witness",
        "osrs",
        "subnautica",
        "cat_quest",
        "residentevil2remake",
        "shapez",
        "undertale",
        "monster_sanctuary",
        "shorthike",
        "celeste",
        "civ_6",
        "v6",
        "inscryption",
        "timespinner",
        "balatro",
        "factorio",
        "aquaria",
        "cuphead",
        "doom_ii",
        "sc2",
        "huniepop2",
        "overcooked2",
        "zork_grand_inquisitor",
        "osu",
        "huniepop",
        "residentevil3remake",
        "landstalker",
        "tyrian",
        "openrct2",
        "hylics2",
        "blasphemous",
        "terraria",
        "brotato",
        "factorio_saws",
        "sims4",
        "stardew_valley",
        "ror1",
        "tunic"
    ],
    "xbox one": [
        "rogue_legacy",
        "hades",
        "swr",
        "wargroove",
        "wargroove2",
        "hk",
        "messenger",
        "chainedechoes",
        "crosscode",
        "ahit",
        "witness",
        "subnautica",
        "residentevil2remake",
        "undertale",
        "monster_sanctuary",
        "placidplasticducksim",
        "shorthike",
        "celeste",
        "dsr",
        "powerwashsimulator",
        "inscryption",
        "bomb_rush_cyberfunk",
        "timespinner",
        "balatro",
        "cuphead",
        "overcooked2",
        "residentevil3remake",
        "enderlilies",
        "blasphemous",
        "terraria",
        "brotato",
        "ror2",
        "sims4",
        "outer_wilds",
        "seaofthieves",
        "dark_souls_3",
        "oribf",
        "stardew_valley",
        "ror1",
        "tunic",
        "trackmania"
    ],
    "time travel": [
        "ctjot",
        "apeescape",
        "ahit",
        "tloz_oos",
        "timespinner",
        "tloz_ooa",
        "outer_wilds",
        "oot",
        "pmd_eos",
        "earthbound",
        "mm_recomp"
    ],
    "travel": [
        "ctjot",
        "apeescape",
        "ahit",
        "tloz_oos",
        "timespinner",
        "tloz_ooa",
        "albw",
        "outer_wilds",
        "alttp",
        "doom_ii",
        "oot",
        "pmd_eos",
        "earthbound",
        "mm_recomp"
    ],
    "spaceship": [
        "v6",
        "ahit",
        "mzm",
        "star_fox_64",
        "metroidprime",
        "civ_6"
    ],
    "female protagonist": [
        "dkc3",
        "enderlilies",
        "celeste64",
        "cv64",
        "ahit",
        "mzm",
        "dkc2",
        "rogue_legacy",
        "sm_map_rando",
        "timespinner",
        "undertale",
        "metroidprime",
        "shorthike",
        "sm",
        "earthbound",
        "hcniko",
        "celeste"
    ],
    "action-adventure": [
        "ss",
        "rogue_legacy",
        "tloz_oos",
        "minecraft",
        "dontstarvetogether",
        "hk",
        "crosscode",
        "ahit",
        "kh1",
        "aus",
        "albw",
        "tloz_ooa",
        "zillion",
        "metroidprime",
        "sm",
        "oot",
        "cvcotm",
        "mm_recomp",
        "sms",
        "timespinner",
        "aquaria",
        "ladx",
        "tww",
        "dark_souls_2",
        "landstalker",
        "sm_map_rando",
        "luigismansion",
        "cv64",
        "xenobladex",
        "terraria",
        "zelda2",
        "banjo_tooie",
        "seaofthieves",
        "alttp",
        "dark_souls_3",
        "sotn"
    ],
    "cute": [
        "ahit",
        "sims4",
        "musedash",
        "undertale",
        "shorthike",
        "animal_well",
        "hcniko",
        "celeste",
        "tunic"
    ],
    "snow": [
        "jakanddaxter",
        "dkc3",
        "ahit",
        "terraria",
        "gstla",
        "albw",
        "minecraft",
        "metroidprime",
        "mk64",
        "diddy_kong_racing",
        "dkc",
        "stardew_valley",
        "hcniko",
        "celeste",
        "ffta"
    ],
    "wall jump": [
        "sms",
        "smo",
        "sm_map_rando",
        "ahit",
        "mzm",
        "oribf",
        "sm",
        "cvcotm"
    ],
    "3d platformer": [
        "sms",
        "sm64hacks",
        "smo",
        "ahit",
        "bomb_rush_cyberfunk",
        "sonic_heroes",
        "shorthike",
        "sm64ex",
        "hcniko"
    ],
    "3d": [
        "sm64hacks",
        "ss",
        "smo",
        "minecraft",
        "k64",
        "dk64",
        "apeescape",
        "ahit",
        "kh1",
        "witness",
        "albw",
        "metroidprime",
        "shorthike",
        "oot",
        "sm64ex",
        "dsr",
        "sms",
        "sly1",
        "jakanddaxter",
        "v6",
        "powerwashsimulator",
        "bomb_rush_cyberfunk",
        "sonic_heroes",
        "hcniko",
        "dark_souls_2",
        "luigismansion",
        "cv64",
        "hylics2",
        "dw1",
        "xenobladex",
        "spyro3",
        "lingo",
        "star_fox_64",
        "dark_souls_3",
        "mk64",
        "tunic",
        "sotn"
    ],
    "swimming": [
        "sm64hacks",
        "smo",
        "minecraft",
        "ahit",
        "kh1",
        "dkc2",
        "subnautica",
        "tloz_ooa",
        "albw",
        "dkc",
        "sm64ex",
        "oot",
        "wl4",
        "sms",
        "jakanddaxter",
        "aquaria",
        "hcniko",
        "dkc3",
        "terraria",
        "banjo_tooie",
        "spyro3",
        "alttp"
    ],
    "a link between worlds": [
        "albw"
    ],
    "the legend of zelda: a link between worlds": [
        "albw"
    ],
    "legend": [
        "tww",
        "ss",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "tloz",
        "alttp",
        "tp",
        "oot",
        "ladx",
        "mm_recomp"
    ],
    "zelda:": [
        "tww",
        "ss",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "tp",
        "oot",
        "ladx",
        "mm_recomp"
    ],
    "link": [
        "tww",
        "ss",
        "smz3",
        "tloz_oos",
        "zelda2",
        "albw",
        "alttp",
        "oot",
        "ladx",
        "tp"
    ],
    "between": [
        "albw"
    ],
    "puzzle": [
        "ss",
        "rogue_legacy",
        "tloz_oos",
        "ttyd",
        "lufia2ac",
        "bumpstik",
        "crosscode",
        "witness",
        "tloz_ooa",
        "albw",
        "shapez",
        "undertale",
        "metroidprime",
        "placidplasticducksim",
        "zillion",
        "oot",
        "animal_well",
        "wl4",
        "mm_recomp",
        "tp",
        "v6",
        "shivers",
        "inscryption",
        "zork_grand_inquisitor",
        "doom_ii",
        "huniepop2",
        "ladx",
        "hcniko",
        "huniepop",
        "tww",
        "yugiohddm",
        "tetrisattack",
        "candybox2",
        "cv64",
        "spyro3",
        "lingo",
        "outer_wilds",
        "alttp",
        "oribf",
        "ufo50",
        "tunic"
    ],
    "historical": [
        "ss",
        "civ_6",
        "candybox2",
        "heretic",
        "albw",
        "soe",
        "fm"
    ],
    "sandbox": [
        "smo",
        "minecraft",
        "dontstarvetogether",
        "osrs",
        "albw",
        "shapez",
        "placidplasticducksim",
        "oot",
        "satisfactory",
        "sms",
        "powerwashsimulator",
        "noita",
        "factorio",
        "landstalker",
        "xenobladex",
        "terraria",
        "zelda2",
        "factorio_saws",
        "faxanadu",
        "sims4",
        "stardew_valley"
    ],
    "open world": [
        "sm64hacks",
        "ss",
        "smo",
        "toontown",
        "minecraft",
        "dontstarvetogether",
        "smz3",
        "witness",
        "osrs",
        "subnautica",
        "albw",
        "metroidprime",
        "shorthike",
        "sm64ex",
        "oot",
        "mm_recomp",
        "satisfactory",
        "jakanddaxter",
        "gstla",
        "pokemon_rb",
        "xenobladex",
        "mzm",
        "terraria",
        "lingo",
        "outer_wilds",
        "seaofthieves",
        "tloz",
        "sotn"
    ],
    "nintendo3ds": [
        "v6",
        "mm2",
        "wl",
        "marioland2",
        "pokemon_crystal",
        "pokemon_rb",
        "tloz_oos",
        "terraria",
        "zelda2",
        "tloz_ooa",
        "albw",
        "tloz",
        "ff1",
        "ladx",
        "wl4"
    ],
    "3ds": [
        "wl",
        "tloz_oos",
        "mm2",
        "dkc2",
        "tloz_ooa",
        "albw",
        "dkc",
        "ff1",
        "sm",
        "wl4",
        "v6",
        "marioland2",
        "pokemon_crystal",
        "earthbound",
        "ladx",
        "dkc3",
        "pokemon_rb",
        "sm_map_rando",
        "terraria",
        "zelda2",
        "tloz",
        "alttp",
        "smw"
    ],
    "medieval": [
        "ss",
        "rogue_legacy",
        "candybox2",
        "heretic",
        "albw",
        "dark_souls_3",
        "soe",
        "dark_souls_2"
    ],
    "magic": [
        "ctjot",
        "rogue_legacy",
        "tloz_oos",
        "heretic",
        "albw",
        "cvcotm",
        "dsr",
        "noita",
        "gstla",
        "aquaria",
        "cuphead",
        "zork_grand_inquisitor",
        "ffta",
        "ladx",
        "dark_souls_2",
        "candybox2",
        "cv64",
        "terraria",
        "zelda2",
        "faxanadu",
        "alttp",
        "sotn"
    ],
    "minigames": [
        "pokemon_emerald",
        "dkc3",
        "apeescape",
        "pokemon_crystal",
        "rogue_legacy",
        "kh1",
        "toontown",
        "spyro3",
        "gstla",
        "tloz_ooa",
        "albw",
        "k64",
        "oot",
        "stardew_valley",
        "hcniko",
        "wl4",
        "dk64"
    ],
    "2.5d": [
        "dkc3",
        "heretic",
        "doom_1993",
        "albw",
        "doom_ii",
        "k64",
        "dkc"
    ],
    "archery": [
        "tww",
        "ss",
        "albw",
        "alttp",
        "oot",
        "mm_recomp"
    ],
    "fairy": [
        "tww",
        "oot",
        "landstalker",
        "tloz_oos",
        "terraria",
        "zelda2",
        "tloz_ooa",
        "albw",
        "tloz",
        "alttp",
        "k64",
        "huniepop2",
        "stardew_valley",
        "ladx",
        "mm_recomp",
        "dk64"
    ],
    "princess": [
        "sms",
        "sm64hacks",
        "ss",
        "tp",
        "mlss",
        "kh1",
        "tloz_oos",
        "mario_kart_double_dash",
        "tloz_ooa",
        "albw",
        "alttp",
        "mk64",
        "sm64ex",
        "smw",
        "oot",
        "ladx",
        "papermario"
    ],
    "sequel": [
        "smo",
        "dontstarvetogether",
        "mm2",
        "dkc2",
        "albw",
        "oot",
        "wl4",
        "mm_recomp",
        "civ_6",
        "sms",
        "gstla",
        "doom_ii",
        "ffta",
        "dark_souls_2",
        "hylics2",
        "dw1",
        "zelda2",
        "banjo_tooie",
        "alttp",
        "dark_souls_3",
        "mk64"
    ],
    "sword & sorcery": [
        "tww",
        "ss",
        "kh1",
        "tloz_oos",
        "heretic",
        "terraria",
        "spyro3",
        "tloz_ooa",
        "albw",
        "dark_souls_3",
        "oot",
        "ladx",
        "ffmq",
        "mm_recomp",
        "dark_souls_2"
    ],
    "darkness": [
        "dkc3",
        "rogue_legacy",
        "luigismansion",
        "sm_map_rando",
        "witness",
        "dkc2",
        "terraria",
        "zelda2",
        "albw",
        "minecraft",
        "alttp",
        "aquaria",
        "doom_ii",
        "dkc",
        "earthbound",
        "ladx",
        "sm",
        "kh2",
        "kh3"
    ],
    "anthropomorphism": [
        "tloz_oos",
        "k64",
        "dk64",
        "apeescape",
        "kh1",
        "dkc2",
        "tloz_ooa",
        "albw",
        "undertale",
        "dkc",
        "sms",
        "sly1",
        "jakanddaxter",
        "mlss",
        "sonic_heroes",
        "cuphead",
        "hcniko",
        "dkc3",
        "tunic",
        "cv64",
        "banjo_tooie",
        "spyro3",
        "star_fox_64",
        "mk64",
        "diddy_kong_racing",
        "papermario"
    ],
    "polygonal 3d": [
        "ss",
        "minecraft",
        "k64",
        "dk64",
        "apeescape",
        "witness",
        "kh1",
        "albw",
        "metroidprime",
        "oot",
        "sms",
        "sly1",
        "jakanddaxter",
        "luigismansion",
        "cv64",
        "xenobladex",
        "dw1",
        "spyro3",
        "star_fox_64",
        "mk64",
        "sotn"
    ],
    "bow and arrow": [
        "ss",
        "rogue_legacy",
        "tloz_oos",
        "terraria",
        "albw",
        "minecraft",
        "alttp",
        "cuphead",
        "ror1",
        "ffta",
        "oot",
        "ladx",
        "dark_souls_2"
    ],
    "bow": [
        "ss",
        "rogue_legacy",
        "tloz_oos",
        "terraria",
        "albw",
        "minecraft",
        "alttp",
        "cuphead",
        "ror1",
        "ffta",
        "oot",
        "ladx",
        "dark_souls_2"
    ],
    "damsel in distress": [
        "sms",
        "ss",
        "sm_map_rando",
        "kh1",
        "tloz_oos",
        "zelda2",
        "smw",
        "tloz_ooa",
        "albw",
        "alttp",
        "metroidprime",
        "sm",
        "oot",
        "earthbound",
        "papermario"
    ],
    "damsel": [
        "sms",
        "ss",
        "sm_map_rando",
        "kh1",
        "tloz_oos",
        "zelda2",
        "smw",
        "tloz_ooa",
        "albw",
        "alttp",
        "metroidprime",
        "sm",
        "oot",
        "earthbound",
        "papermario"
    ],
    "upgradeable weapons": [
        "cv64",
        "mzm",
        "dark_souls_2",
        "albw",
        "metroidprime",
        "mm2",
        "dk64"
    ],
    "upgradeable": [
        "cv64",
        "mzm",
        "dark_souls_2",
        "albw",
        "metroidprime",
        "mm2",
        "dk64"
    ],
    "disorientation zone": [
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "oot",
        "ladx"
    ],
    "disorientation": [
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "oot",
        "ladx"
    ],
    "descendants of other characters": [
        "sms",
        "sly1",
        "jakanddaxter",
        "dkc3",
        "rogue_legacy",
        "luigismansion",
        "cv64",
        "dkc2",
        "star_fox_64",
        "albw",
        "sotn",
        "tloz_ooa",
        "dkc",
        "oot",
        "earthbound",
        "mm_recomp",
        "dk64"
    ],
    "descendants": [
        "sms",
        "sly1",
        "jakanddaxter",
        "dkc3",
        "rogue_legacy",
        "luigismansion",
        "cv64",
        "dkc2",
        "star_fox_64",
        "albw",
        "sotn",
        "tloz_ooa",
        "dkc",
        "oot",
        "earthbound",
        "mm_recomp",
        "dk64"
    ],
    "stereoscopic 3d": [
        "sly1",
        "v6",
        "luigismansion",
        "albw",
        "minecraft"
    ],
    "stereoscopic": [
        "sly1",
        "v6",
        "luigismansion",
        "albw",
        "minecraft"
    ],
    "side quests": [
        "pokemon_emerald",
        "pokemon_crystal",
        "xenobladex",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "sc2",
        "oot",
        "ladx",
        "dark_souls_2"
    ],
    "side": [
        "dlcquest",
        "wl",
        "rogue_legacy",
        "yoshisisland",
        "tloz_oos",
        "getting_over_it",
        "lufia2ac",
        "wargroove",
        "wargroove2",
        "musedash",
        "hk",
        "k64",
        "dungeon_clawler",
        "mm2",
        "momodoramoonlitfarewell",
        "messenger",
        "ffmq",
        "smz3",
        "dkc2",
        "megamix",
        "aus",
        "albw",
        "tloz_ooa",
        "zillion",
        "monster_sanctuary",
        "dkc",
        "ff1",
        "animal_well",
        "oot",
        "sm",
        "cvcotm",
        "celeste",
        "wl4",
        "v6",
        "mlss",
        "marioland2",
        "pokemon_crystal",
        "timespinner",
        "pokemon_frlg",
        "noita",
        "aquaria",
        "cuphead",
        "sc2",
        "spire",
        "ladx",
        "dark_souls_2",
        "dkc3",
        "enderlilies",
        "pokemon_rb",
        "sm_map_rando",
        "hylics2",
        "ff4fe",
        "blasphemous",
        "mzm",
        "terraria",
        "tetrisattack",
        "xenobladex",
        "zelda2",
        "faxanadu",
        "alttp",
        "oribf",
        "ufo50",
        "smw",
        "pokemon_emerald",
        "kdl3",
        "ror1",
        "papermario",
        "sotn"
    ],
    "quests": [
        "pokemon_emerald",
        "pokemon_crystal",
        "xenobladex",
        "tloz_oos",
        "zelda2",
        "tloz_ooa",
        "albw",
        "alttp",
        "metroidprime",
        "sc2",
        "oot",
        "ladx",
        "dark_souls_2"
    ],
    "potion": [
        "ss",
        "rogue_legacy",
        "pokemon_crystal",
        "kh1",
        "tloz_oos",
        "zelda2",
        "gstla",
        "albw",
        "minecraft",
        "alttp",
        "pokemon_emerald",
        "ladx"
    ],
    "real-time combat": [
        "sm64hacks",
        "ss",
        "tloz_oos",
        "minecraft",
        "dk64",
        "kh1",
        "tloz_ooa",
        "albw",
        "metroidprime",
        "dkc",
        "sm64ex",
        "oot",
        "sm",
        "sms",
        "doom_ii",
        "ladx",
        "dark_souls_2",
        "landstalker",
        "sm_map_rando",
        "cv64",
        "xenobladex",
        "zelda2",
        "spyro3",
        "doom_1993",
        "alttp",
        "sotn"
    ],
    "real-time": [
        "sm64hacks",
        "ss",
        "tloz_oos",
        "minecraft",
        "dk64",
        "kh1",
        "tloz_ooa",
        "albw",
        "metroidprime",
        "dkc",
        "sm64ex",
        "oot",
        "sm",
        "sms",
        "doom_ii",
        "ladx",
        "dark_souls_2",
        "landstalker",
        "sm_map_rando",
        "cv64",
        "xenobladex",
        "zelda2",
        "spyro3",
        "doom_1993",
        "alttp",
        "sotn"
    ],
    "combat": [
        "sm64hacks",
        "ss",
        "tloz_oos",
        "minecraft",
        "dk64",
        "kh1",
        "tloz_ooa",
        "albw",
        "metroidprime",
        "dkc",
        "sm64ex",
        "oot",
        "sm",
        "sms",
        "doom_ii",
        "ladx",
        "dark_souls_2",
        "landstalker",
        "sm_map_rando",
        "cv64",
        "xenobladex",
        "zelda2",
        "spyro3",
        "doom_1993",
        "alttp",
        "sotn"
    ],
    "self-referential humor": [
        "mlss",
        "dkc2",
        "albw",
        "earthbound",
        "papermario"
    ],
    "self-referential": [
        "mlss",
        "dkc2",
        "albw",
        "earthbound",
        "papermario"
    ],
    "humor": [
        "mlss",
        "dkc2",
        "albw",
        "earthbound",
        "papermario"
    ],
    "multiple gameplay perspectives": [
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "minecraft",
        "metroidprime"
    ],
    "rpg": [
        "mlss",
        "mzm",
        "zelda2",
        "banjo_tooie",
        "albw",
        "minecraft",
        "oribf",
        "sotn",
        "dark_souls_2"
    ],
    "elements": [
        "mlss",
        "mzm",
        "zelda2",
        "banjo_tooie",
        "albw",
        "minecraft",
        "oribf",
        "sotn",
        "dark_souls_2"
    ],
    "mercenary": [
        "ss",
        "sm_map_rando",
        "albw",
        "alttp",
        "metroidprime",
        "sc2",
        "sm",
        "oot",
        "dark_souls_2"
    ],
    "coming of age": [
        "pokemon_emerald",
        "jakanddaxter",
        "pokemon_crystal",
        "albw",
        "alttp",
        "oribf",
        "ffta",
        "oot"
    ],
    "coming": [
        "pokemon_emerald",
        "jakanddaxter",
        "pokemon_crystal",
        "albw",
        "alttp",
        "oribf",
        "ffta",
        "oot"
    ],
    "age": [
        "pokemon_emerald",
        "jakanddaxter",
        "pokemon_crystal",
        "factorio_saws",
        "gstla",
        "albw",
        "alttp",
        "oribf",
        "ffta",
        "oot"
    ],
    "dimension travel": [
        "mm_recomp",
        "albw",
        "alttp",
        "doom_ii"
    ],
    "dimension": [
        "mm_recomp",
        "albw",
        "alttp",
        "doom_ii"
    ],
    "androgyny": [
        "ss",
        "gstla",
        "albw",
        "ffta",
        "oot",
        "sotn"
    ],
    "fast traveling": [
        "pokemon_emerald",
        "albw",
        "alttp",
        "undertale",
        "hk",
        "oot"
    ],
    "fast": [
        "pokemon_emerald",
        "albw",
        "alttp",
        "undertale",
        "hk",
        "oot"
    ],
    "traveling": [
        "pokemon_emerald",
        "albw",
        "alttp",
        "undertale",
        "hk",
        "oot"
    ],
    "context sensitive": [
        "ss",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "oot"
    ],
    "context": [
        "ss",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "oot"
    ],
    "sensitive": [
        "ss",
        "tloz_oos",
        "tloz_ooa",
        "albw",
        "alttp",
        "oot"
    ],
    "living inventory": [
        "tww",
        "ss",
        "albw",
        "alttp",
        "oot",
        "mm_recomp"
    ],
    "living": [
        "tww",
        "ss",
        "albw",
        "alttp",
        "oot",
        "mm_recomp"
    ],
    "inventory": [
        "tww",
        "ss",
        "albw",
        "alttp",
        "oot",
        "mm_recomp"
    ],
    "bees": [
        "terraria",
        "albw",
        "minecraft",
        "alttp",
        "dontstarvetogether",
        "raft"
    ],
    "zelda": [
        "tww",
        "ss",
        "tloz_oos",
        "zelda2",
        "albw",
        "tloz",
        "alttp",
        "oot",
        "ladx",
        "tp"
    ],
    "legend of zelda": [
        "tww",
        "ss",
        "tloz_oos",
        "albw",
        "oot",
        "ladx",
        "tp"
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
        "dkc3",
        "smz3",
        "sm_map_rando",
        "soe",
        "tetrisattack",
        "ff4fe",
        "dkc2",
        "lufia2ac",
        "yoshisisland",
        "smw",
        "alttp",
        "dkc",
        "kdl3",
        "earthbound",
        "ffmq",
        "sm"
    ],
    "super": [
        "sm64hacks",
        "wl",
        "smo",
        "yoshisisland",
        "lufia2ac",
        "ffmq",
        "smz3",
        "dkc2",
        "kdl3",
        "dkc",
        "sm64ex",
        "sm",
        "sms",
        "marioland2",
        "earthbound",
        "dkc3",
        "sm_map_rando",
        "tetrisattack",
        "ff4fe",
        "alttp",
        "smw",
        "soe"
    ],
    "entertainment": [
        "yoshisisland",
        "lufia2ac",
        "ffmq",
        "smz3",
        "dkc2",
        "kdl3",
        "dkc",
        "ff1",
        "sm",
        "earthbound",
        "dkc3",
        "sm_map_rando",
        "tetrisattack",
        "ff4fe",
        "zelda2",
        "faxanadu",
        "tloz",
        "alttp",
        "smw",
        "soe"
    ],
    "wii": [
        "sm64hacks",
        "ss",
        "mmbn3",
        "hk",
        "k64",
        "ffmq",
        "dk64",
        "dkc2",
        "dkc",
        "ff1",
        "oot",
        "sm",
        "sm64ex",
        "cvcotm",
        "mm_recomp",
        "tp",
        "wl4",
        "mlss",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "dkc3",
        "landstalker",
        "sm_map_rando",
        "xenobladex",
        "ff4fe",
        "mzm",
        "terraria",
        "zelda2",
        "faxanadu",
        "star_fox_64",
        "tloz",
        "alttp",
        "mk64",
        "smw",
        "kdl3",
        "stardew_valley",
        "papermario"
    ],
    "wii u": [
        "sm64hacks",
        "ss",
        "mmbn3",
        "hk",
        "k64",
        "ffmq",
        "dk64",
        "dkc2",
        "dkc",
        "ff1",
        "oot",
        "sm",
        "sm64ex",
        "cvcotm",
        "mm_recomp",
        "wl4",
        "mlss",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "dkc3",
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "terraria",
        "zelda2",
        "star_fox_64",
        "tloz",
        "alttp",
        "mk64",
        "smw",
        "kdl3",
        "stardew_valley",
        "papermario"
    ],
    "u": [
        "sm64hacks",
        "ss",
        "mmbn3",
        "hk",
        "k64",
        "ffmq",
        "dk64",
        "dkc2",
        "dkc",
        "ff1",
        "oot",
        "sm",
        "sm64ex",
        "cvcotm",
        "mm_recomp",
        "wl4",
        "mlss",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "dkc3",
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "terraria",
        "zelda2",
        "star_fox_64",
        "tloz",
        "alttp",
        "mk64",
        "smw",
        "kdl3",
        "stardew_valley",
        "papermario"
    ],
    "new nintendo 3ds": [
        "dkc3",
        "sm_map_rando",
        "dkc2",
        "smw",
        "alttp",
        "dkc",
        "earthbound",
        "sm"
    ],
    "super famicom": [
        "dkc3",
        "sm_map_rando",
        "yoshisisland",
        "dkc2",
        "lufia2ac",
        "smw",
        "alttp",
        "dkc",
        "kdl3",
        "earthbound",
        "ffmq",
        "sm"
    ],
    "famicom": [
        "dkc3",
        "sm_map_rando",
        "yoshisisland",
        "dkc2",
        "lufia2ac",
        "smw",
        "alttp",
        "dkc",
        "kdl3",
        "earthbound",
        "ffmq",
        "sm"
    ],
    "ghosts": [
        "sms",
        "sly1",
        "v6",
        "mlss",
        "rogue_legacy",
        "luigismansion",
        "cv64",
        "dkc2",
        "aus",
        "tloz_ooa",
        "wl4",
        "alttp",
        "cuphead",
        "metroidprime",
        "earthbound",
        "ffmq",
        "papermario",
        "sotn"
    ],
    "mascot": [
        "sly1",
        "jakanddaxter",
        "tloz_oos",
        "spyro3",
        "alttp",
        "k64",
        "mm2",
        "kdl3",
        "ladx",
        "papermario"
    ],
    "death": [
        "rogue_legacy",
        "tloz_oos",
        "heretic",
        "minecraft",
        "mm2",
        "dk64",
        "kh1",
        "tloz_ooa",
        "metroidprime",
        "dkc",
        "oot",
        "cvcotm",
        "sms",
        "sly1",
        "v6",
        "gstla",
        "doom_ii",
        "ffta",
        "ladx",
        "dark_souls_2",
        "luigismansion",
        "cv64",
        "openrct2",
        "mzm",
        "terraria",
        "zelda2",
        "star_fox_64",
        "dark_souls_3",
        "alttp",
        "mk64",
        "papermario",
        "sotn"
    ],
    "maze": [
        "cv64",
        "openrct2",
        "mzm",
        "witness",
        "doom_1993",
        "alttp",
        "ladx",
        "papermario"
    ],
    "backtracking": [
        "jakanddaxter",
        "cv64",
        "kh1",
        "mzm",
        "tloz_oos",
        "witness",
        "banjo_tooie",
        "faxanadu",
        "alttp",
        "metroidprime",
        "undertale",
        "ffta",
        "oot",
        "ladx",
        "cvcotm",
        "sotn"
    ],
    "undead": [
        "mlss",
        "cv64",
        "tloz_oos",
        "heretic",
        "terraria",
        "dark_souls_2",
        "tloz_ooa",
        "sotn",
        "alttp",
        "oot",
        "ladx",
        "ffmq",
        "papermario",
        "dsr"
    ],
    "campaign": [
        "ss",
        "tloz_oos",
        "zelda2",
        "tloz_ooa",
        "alttp",
        "oot",
        "ladx"
    ],
    "pixel art": [
        "rogue_legacy",
        "tloz_oos",
        "wargroove",
        "mm2",
        "crosscode",
        "undertale",
        "sm",
        "animal_well",
        "celeste",
        "wl4",
        "v6",
        "timespinner",
        "ladx",
        "hcniko",
        "tyrian",
        "sm_map_rando",
        "mzm",
        "blasphemous",
        "terraria",
        "zelda2",
        "alttp",
        "stardew_valley",
        "ror1",
        "sotn"
    ],
    "pixel": [
        "rogue_legacy",
        "tloz_oos",
        "wargroove",
        "mm2",
        "crosscode",
        "undertale",
        "sm",
        "animal_well",
        "celeste",
        "wl4",
        "v6",
        "timespinner",
        "ladx",
        "hcniko",
        "tyrian",
        "sm_map_rando",
        "mzm",
        "blasphemous",
        "terraria",
        "zelda2",
        "alttp",
        "stardew_valley",
        "ror1",
        "sotn"
    ],
    "art": [
        "rogue_legacy",
        "tloz_oos",
        "wargroove",
        "mm2",
        "crosscode",
        "undertale",
        "sm",
        "animal_well",
        "celeste",
        "wl4",
        "v6",
        "timespinner",
        "ladx",
        "hcniko",
        "tyrian",
        "sm_map_rando",
        "mzm",
        "blasphemous",
        "terraria",
        "zelda2",
        "alttp",
        "stardew_valley",
        "ror1",
        "sotn"
    ],
    "easter egg": [
        "rogue_legacy",
        "apeescape",
        "openrct2",
        "banjo_tooie",
        "alttp",
        "doom_ii",
        "ladx",
        "papermario"
    ],
    "easter": [
        "rogue_legacy",
        "apeescape",
        "openrct2",
        "banjo_tooie",
        "alttp",
        "doom_ii",
        "ladx",
        "papermario"
    ],
    "egg": [
        "rogue_legacy",
        "apeescape",
        "openrct2",
        "banjo_tooie",
        "alttp",
        "doom_ii",
        "ladx",
        "papermario"
    ],
    "teleportation": [
        "v6",
        "jakanddaxter",
        "rogue_legacy",
        "pokemon_crystal",
        "cv64",
        "tloz_oos",
        "terraria",
        "alttp",
        "doom_ii",
        "pokemon_emerald",
        "earthbound"
    ],
    "giant insects": [
        "sms",
        "dkc3",
        "mlss",
        "dkc2",
        "alttp",
        "hk",
        "dkc",
        "pokemon_emerald",
        "soe",
        "dk64"
    ],
    "giant": [
        "sms",
        "dkc3",
        "mlss",
        "dkc2",
        "alttp",
        "hk",
        "dkc",
        "pokemon_emerald",
        "soe",
        "dk64"
    ],
    "insects": [
        "sms",
        "dkc3",
        "mlss",
        "dkc2",
        "alttp",
        "hk",
        "dkc",
        "pokemon_emerald",
        "soe",
        "dk64"
    ],
    "silent protagonist": [
        "ss",
        "tloz_oos",
        "hk",
        "k64",
        "ultrakill",
        "dkc2",
        "tloz_ooa",
        "dkc",
        "oot",
        "jakanddaxter",
        "mlss",
        "gstla",
        "ladx",
        "blasphemous",
        "zelda2",
        "doom_1993",
        "alttp",
        "pokemon_emerald",
        "papermario"
    ],
    "silent": [
        "ss",
        "tloz_oos",
        "hk",
        "k64",
        "ultrakill",
        "dkc2",
        "tloz_ooa",
        "dkc",
        "oot",
        "jakanddaxter",
        "mlss",
        "gstla",
        "ladx",
        "blasphemous",
        "zelda2",
        "doom_1993",
        "alttp",
        "pokemon_emerald",
        "papermario"
    ],
    "explosion": [
        "rogue_legacy",
        "minecraft",
        "mm2",
        "ffmq",
        "dkc2",
        "tloz_ooa",
        "metroidprime",
        "sm",
        "sms",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "ffta",
        "dkc3",
        "sm_map_rando",
        "cv64",
        "openrct2",
        "mzm",
        "terraria",
        "zelda2",
        "alttp",
        "mk64",
        "sotn"
    ],
    "block puzzle": [
        "tloz_oos",
        "oot",
        "alttp",
        "tloz_ooa"
    ],
    "block": [
        "tloz_oos",
        "oot",
        "alttp",
        "tloz_ooa"
    ],
    "monkey": [
        "dkc3",
        "apeescape",
        "dkc2",
        "alttp",
        "mk64",
        "diddy_kong_racing",
        "dkc",
        "ladx",
        "dk64"
    ],
    "nintendo power": [
        "dkc3",
        "sm_map_rando",
        "dkc2",
        "alttp",
        "dkc",
        "earthbound",
        "sm"
    ],
    "power": [
        "dkc3",
        "sm_map_rando",
        "dkc2",
        "alttp",
        "dkc",
        "earthbound",
        "sm"
    ],
    "world map": [
        "v6",
        "jakanddaxter",
        "dkc3",
        "pokemon_crystal",
        "tloz_oos",
        "dkc2",
        "alttp",
        "aquaria",
        "metroidprime",
        "dkc",
        "oot",
        "ladx"
    ],
    "map": [
        "v6",
        "jakanddaxter",
        "dkc3",
        "pokemon_crystal",
        "tloz_oos",
        "dkc2",
        "alttp",
        "aquaria",
        "metroidprime",
        "dkc",
        "oot",
        "ladx"
    ],
    "human": [
        "sms",
        "ss",
        "apeescape",
        "cv64",
        "terraria",
        "zelda2",
        "gstla",
        "sotn",
        "dark_souls_3",
        "alttp",
        "doom_ii",
        "sc2",
        "ladx",
        "papermario",
        "dark_souls_2"
    ],
    "shopping": [
        "mlss",
        "pokemon_crystal",
        "yugiohddm",
        "cv64",
        "tloz_oos",
        "dw1",
        "tloz_ooa",
        "alttp",
        "cuphead",
        "pokemon_emerald",
        "sotn"
    ],
    "ice stage": [
        "jakanddaxter",
        "dkc3",
        "cv64",
        "dkc2",
        "terraria",
        "banjo_tooie",
        "alttp",
        "metroidprime",
        "mk64",
        "dkc",
        "oot",
        "wl4"
    ],
    "ice": [
        "jakanddaxter",
        "dkc3",
        "cv64",
        "dkc2",
        "terraria",
        "banjo_tooie",
        "alttp",
        "metroidprime",
        "mk64",
        "dkc",
        "oot",
        "wl4"
    ],
    "stage": [
        "jakanddaxter",
        "dkc3",
        "cv64",
        "dkc2",
        "terraria",
        "banjo_tooie",
        "spyro3",
        "smw",
        "alttp",
        "metroidprime",
        "mk64",
        "sonic_heroes",
        "dkc",
        "oot",
        "wl4"
    ],
    "saving the world": [
        "zelda2",
        "earthbound",
        "alttp",
        "dark_souls_2"
    ],
    "saving": [
        "zelda2",
        "earthbound",
        "alttp",
        "dark_souls_2"
    ],
    "secret area": [
        "dkc3",
        "rogue_legacy",
        "sm_map_rando",
        "tunic",
        "tloz_oos",
        "witness",
        "dkc2",
        "heretic",
        "zelda2",
        "star_fox_64",
        "alttp",
        "doom_ii",
        "diddy_kong_racing",
        "dkc",
        "hcniko",
        "sm",
        "sotn"
    ],
    "secret": [
        "dkc3",
        "rogue_legacy",
        "sm_map_rando",
        "tunic",
        "tloz_oos",
        "witness",
        "dkc2",
        "heretic",
        "zelda2",
        "star_fox_64",
        "alttp",
        "doom_ii",
        "diddy_kong_racing",
        "dkc",
        "soe",
        "hcniko",
        "sm",
        "sotn"
    ],
    "area": [
        "dkc3",
        "rogue_legacy",
        "sm_map_rando",
        "tunic",
        "tloz_oos",
        "witness",
        "dkc2",
        "heretic",
        "zelda2",
        "star_fox_64",
        "alttp",
        "doom_ii",
        "diddy_kong_racing",
        "dkc",
        "hcniko",
        "sm",
        "sotn"
    ],
    "shielded enemies": [
        "rogue_legacy",
        "dkc3",
        "tloz_ooa",
        "alttp",
        "hk"
    ],
    "shielded": [
        "rogue_legacy",
        "dkc3",
        "tloz_ooa",
        "alttp",
        "hk"
    ],
    "enemies": [
        "rogue_legacy",
        "dkc3",
        "tloz_ooa",
        "alttp",
        "hk"
    ],
    "walking through walls": [
        "tloz_oos",
        "tloz_ooa",
        "alttp",
        "doom_ii",
        "oot",
        "ladx"
    ],
    "walking": [
        "tloz_oos",
        "tloz_ooa",
        "alttp",
        "doom_ii",
        "oot",
        "ladx"
    ],
    "through": [
        "tloz_oos",
        "tloz_ooa",
        "alttp",
        "doom_ii",
        "oot",
        "ladx"
    ],
    "walls": [
        "tloz_oos",
        "tloz_ooa",
        "alttp",
        "doom_ii",
        "oot",
        "ladx"
    ],
    "liberation": [
        "sm",
        "dkc2",
        "alttp",
        "sm_map_rando"
    ],
    "conveyor belt": [
        "mm2",
        "alttp",
        "cuphead",
        "tloz_ooa"
    ],
    "conveyor": [
        "mm2",
        "alttp",
        "cuphead",
        "tloz_ooa"
    ],
    "belt": [
        "mm2",
        "alttp",
        "cuphead",
        "tloz_ooa"
    ],
    "villain": [
        "oot",
        "kh1",
        "tloz_oos",
        "zelda2",
        "banjo_tooie",
        "gstla",
        "star_fox_64",
        "tloz_ooa",
        "alttp",
        "dkc",
        "mm2",
        "cvcotm",
        "papermario",
        "sotn"
    ],
    "recurring boss": [
        "dkc3",
        "kh1",
        "dkc2",
        "banjo_tooie",
        "alttp",
        "dkc",
        "pokemon_emerald",
        "papermario",
        "dk64"
    ],
    "recurring": [
        "dkc3",
        "kh1",
        "dkc2",
        "banjo_tooie",
        "alttp",
        "dkc",
        "pokemon_emerald",
        "papermario",
        "dk64"
    ],
    "boss": [
        "sms",
        "pokemon_emerald",
        "dkc3",
        "rogue_legacy",
        "kh1",
        "dkc2",
        "banjo_tooie",
        "dark_souls_2",
        "alttp",
        "cuphead",
        "doom_ii",
        "metroidprime",
        "dkc",
        "oot",
        "papermario",
        "mm_recomp",
        "dk64"
    ],
    "been here before": [
        "sms",
        "pokemon_crystal",
        "gstla",
        "alttp",
        "ffta",
        "oot"
    ],
    "been": [
        "sms",
        "pokemon_crystal",
        "gstla",
        "alttp",
        "ffta",
        "oot"
    ],
    "here": [
        "sms",
        "pokemon_crystal",
        "gstla",
        "alttp",
        "ffta",
        "oot",
        "hcniko"
    ],
    "before": [
        "sms",
        "pokemon_crystal",
        "gstla",
        "alttp",
        "ffta",
        "oot"
    ],
    "sleeping": [
        "sms",
        "pokemon_crystal",
        "gstla",
        "minecraft",
        "alttp",
        "papermario"
    ],
    "merchants": [
        "yugiohddm",
        "candybox2",
        "timespinner",
        "terraria",
        "faxanadu",
        "alttp",
        "hk"
    ],
    "fetch quests": [
        "tloz_oos",
        "zelda2",
        "alttp",
        "metroidprime",
        "ladx"
    ],
    "fetch": [
        "tloz_oos",
        "zelda2",
        "alttp",
        "metroidprime",
        "ladx"
    ],
    "kidnapping": [
        "sms",
        "yoshisisland",
        "openrct2",
        "alttp",
        "earthbound"
    ],
    "poisoning": [
        "pokemon_crystal",
        "cv64",
        "tloz_oos",
        "alttp",
        "pokemon_emerald",
        "papermario"
    ],
    "time paradox": [
        "jakanddaxter",
        "cv64",
        "tloz_ooa",
        "alttp",
        "oot"
    ],
    "paradox": [
        "jakanddaxter",
        "cv64",
        "tloz_ooa",
        "alttp",
        "oot"
    ],
    "status effects": [
        "pokemon_crystal",
        "tloz_oos",
        "zelda2",
        "tloz_ooa",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "ladx",
        "dark_souls_2"
    ],
    "status": [
        "pokemon_crystal",
        "tloz_oos",
        "zelda2",
        "tloz_ooa",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "ladx",
        "dark_souls_2"
    ],
    "effects": [
        "pokemon_crystal",
        "tloz_oos",
        "zelda2",
        "tloz_ooa",
        "alttp",
        "pokemon_emerald",
        "earthbound",
        "ladx",
        "dark_souls_2"
    ],
    "hidden room": [
        "heretic",
        "alttp",
        "doom_ii",
        "dark_souls_2"
    ],
    "hidden": [
        "heretic",
        "alttp",
        "doom_ii",
        "dark_souls_2"
    ],
    "room": [
        "heretic",
        "alttp",
        "doom_ii",
        "dark_souls_2"
    ],
    "another world": [
        "mm_recomp",
        "ladx",
        "alttp",
        "doom_ii"
    ],
    "another": [
        "mm_recomp",
        "ladx",
        "alttp",
        "doom_ii"
    ],
    "damage over time": [
        "pokemon_emerald",
        "jakanddaxter",
        "pokemon_crystal",
        "tloz_oos",
        "alttp",
        "ffta",
        "oot"
    ],
    "damage": [
        "pokemon_emerald",
        "jakanddaxter",
        "pokemon_crystal",
        "cv64",
        "tloz_oos",
        "terraria",
        "minecraft",
        "alttp",
        "metroidprime",
        "ffta",
        "oot"
    ],
    "over": [
        "pokemon_emerald",
        "jakanddaxter",
        "dkc3",
        "pokemon_crystal",
        "ffta",
        "tloz_oos",
        "getting_over_it",
        "sotn",
        "alttp",
        "doom_ii",
        "dkc",
        "oot",
        "dk64"
    ],
    "monomyth": [
        "mm2",
        "ss",
        "zelda2",
        "alttp"
    ],
    "buddy system": [
        "dkc",
        "dkc2",
        "alttp",
        "dkc3"
    ],
    "buddy": [
        "dkc",
        "dkc2",
        "alttp",
        "dkc3"
    ],
    "retroachievements": [
        "sm64hacks",
        "lufia2ac",
        "k64",
        "ffmq",
        "dk64",
        "dkc2",
        "dkc",
        "sm64ex",
        "oot",
        "mm_recomp",
        "sonic_heroes",
        "earthbound",
        "dkc3",
        "tetrisattack",
        "cv64",
        "ff4fe",
        "banjo_tooie",
        "star_fox_64",
        "alttp",
        "mk64",
        "diddy_kong_racing",
        "smw",
        "kdl3",
        "papermario"
    ],
    "popular": [
        "pokemon_emerald",
        "kh2",
        "sm64ex",
        "alttp",
        "dark_souls_3",
        "sc2",
        "hk",
        "oot",
        "stardew_valley"
    ],
    "animal well": [
        "animal_well"
    ],
    "animal": [
        "pokemon_emerald",
        "oot",
        "pokemon_crystal",
        "animal_well",
        "ladx"
    ],
    "well": [
        "animal_well"
    ],
    "side view": [
        "dlcquest",
        "wl",
        "rogue_legacy",
        "yoshisisland",
        "getting_over_it",
        "lufia2ac",
        "wargroove",
        "wargroove2",
        "musedash",
        "hk",
        "k64",
        "dungeon_clawler",
        "mm2",
        "momodoramoonlitfarewell",
        "messenger",
        "ffmq",
        "smz3",
        "dkc2",
        "megamix",
        "aus",
        "zillion",
        "monster_sanctuary",
        "dkc",
        "ff1",
        "animal_well",
        "sm",
        "cvcotm",
        "celeste",
        "wl4",
        "v6",
        "mlss",
        "marioland2",
        "pokemon_crystal",
        "timespinner",
        "pokemon_frlg",
        "noita",
        "aquaria",
        "cuphead",
        "spire",
        "ladx",
        "dkc3",
        "enderlilies",
        "pokemon_rb",
        "sm_map_rando",
        "hylics2",
        "ff4fe",
        "blasphemous",
        "mzm",
        "terraria",
        "tetrisattack",
        "zelda2",
        "faxanadu",
        "oribf",
        "ufo50",
        "smw",
        "pokemon_emerald",
        "kdl3",
        "ror1",
        "papermario",
        "sotn"
    ],
    "horror": [
        "residentevil3remake",
        "shivers",
        "luigismansion",
        "cv64",
        "inscryption",
        "blasphemous",
        "getting_over_it",
        "terraria",
        "doom_1993",
        "residentevil2remake",
        "undertale",
        "dontstarvetogether",
        "doom_ii",
        "animal_well",
        "lethal_company",
        "cvcotm",
        "mm_recomp",
        "sotn"
    ],
    "survival": [
        "rimworld",
        "subnautica",
        "terraria",
        "factorio_saws",
        "dungeon_clawler",
        "ror2",
        "yugioh06",
        "factorio",
        "residentevil2remake",
        "minecraft",
        "raft",
        "dontstarvetogether",
        "animal_well",
        "lethal_company",
        "ror1",
        "residentevil3remake"
    ],
    "mystery": [
        "witness",
        "inscryption",
        "outer_wilds",
        "animal_well",
        "pmd_eos"
    ],
    "exploration": [
        "dlcquest",
        "rogue_legacy",
        "lethal_company",
        "witness",
        "subnautica",
        "metroidprime",
        "shorthike",
        "sm",
        "animal_well",
        "celeste",
        "v6",
        "jakanddaxter",
        "pokemon_crystal",
        "aquaria",
        "hcniko",
        "sm_map_rando",
        "cv64",
        "hylics2",
        "terraria",
        "lingo",
        "outer_wilds",
        "seaofthieves",
        "pokemon_emerald",
        "tunic"
    ],
    "retro": [
        "dlcquest",
        "v6",
        "smo",
        "hylics2",
        "timespinner",
        "blasphemous",
        "terraria",
        "minecraft",
        "undertale",
        "cuphead",
        "ufo50",
        "animal_well",
        "stardew_valley",
        "messenger",
        "celeste"
    ],
    "dark": [
        "dark_souls_2",
        "dark_souls_3",
        "undertale",
        "hk",
        "animal_well",
        "dsr"
    ],
    "2d": [
        "smo",
        "musedash",
        "dontstarvetogether",
        "hk",
        "messenger",
        "undertale",
        "sm",
        "animal_well",
        "celeste",
        "v6",
        "cuphead",
        "earthbound",
        "sm_map_rando",
        "hylics2",
        "blasphemous",
        "terraria",
        "zelda2",
        "stardew_valley",
        "sotn"
    ],
    "metroidvania": [
        "rogue_legacy",
        "hk",
        "momodoramoonlitfarewell",
        "messenger",
        "aus",
        "zillion",
        "metroidprime",
        "monster_sanctuary",
        "sm",
        "animal_well",
        "cvcotm",
        "v6",
        "pseudoregalia",
        "timespinner",
        "aquaria",
        "dark_souls_2",
        "enderlilies",
        "sm_map_rando",
        "mzm",
        "blasphemous",
        "zelda2",
        "faxanadu",
        "oribf",
        "sotn"
    ],
    "atmospheric": [
        "powerwashsimulator",
        "hylics2",
        "dontstarvetogether",
        "hk",
        "animal_well",
        "celeste",
        "tunic"
    ],
    "relaxing": [
        "powerwashsimulator",
        "sims4",
        "shorthike",
        "animal_well",
        "stardew_valley",
        "hcniko"
    ],
    "controller support": [
        "v6",
        "hk",
        "animal_well",
        "stardew_valley",
        "hcniko",
        "tunic"
    ],
    "controller": [
        "v6",
        "hk",
        "animal_well",
        "stardew_valley",
        "hcniko",
        "tunic"
    ],
    "support": [
        "v6",
        "tunic",
        "cv64",
        "kh1",
        "gstla",
        "hk",
        "ffta",
        "animal_well",
        "stardew_valley",
        "hcniko",
        "fm"
    ],
    "ape escape": [
        "apeescape"
    ],
    "ape": [
        "dkc3",
        "apeescape",
        "dkc2",
        "mk64",
        "dkc",
        "dk64"
    ],
    "escape": [
        "apeescape"
    ],
    "ps3": [
        "rogue_legacy",
        "kh2",
        "apeescape",
        "terraria",
        "sa2b",
        "spyro3",
        "sadx",
        "sotn",
        "dark_souls_2"
    ],
    "playstation3": [
        "wl",
        "rogue_legacy",
        "kh2",
        "apeescape",
        "mmbn3",
        "terraria",
        "sa2b",
        "spyro3",
        "sadx",
        "sotn",
        "kdl3",
        "residentevil3remake",
        "dark_souls_2"
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
        "pokemon_emerald",
        "yugiohddm",
        "apeescape",
        "pokemon_crystal",
        "dw1",
        "fm",
        "gstla",
        "musedash",
        "wl4",
        "zillion",
        "huniepop2",
        "osu",
        "huniepop"
    ],
    "dinosaurs": [
        "sms",
        "smo",
        "apeescape",
        "yoshisisland",
        "banjo_tooie",
        "smw",
        "earthbound"
    ],
    "collecting": [
        "pokemon_crystal",
        "apeescape",
        "pokemon_rb",
        "mzm",
        "zelda2",
        "banjo_tooie",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "multiple endings": [
        "apeescape",
        "cv64",
        "kh1",
        "mzm",
        "dkc2",
        "tloz_oos",
        "witness",
        "star_fox_64",
        "sotn",
        "undertale",
        "cuphead",
        "doom_ii",
        "k64",
        "metroidprime",
        "wl4",
        "civ_6",
        "dk64"
    ],
    "endings": [
        "apeescape",
        "cv64",
        "kh1",
        "mzm",
        "dkc2",
        "tloz_oos",
        "witness",
        "star_fox_64",
        "sotn",
        "undertale",
        "cuphead",
        "doom_ii",
        "k64",
        "metroidprime",
        "wl4",
        "civ_6",
        "dk64"
    ],
    "amnesia": [
        "apeescape",
        "xenobladex",
        "witness",
        "sonic_heroes",
        "aquaria"
    ],
    "voice acting": [
        "sms",
        "sly1",
        "jakanddaxter",
        "apeescape",
        "cv64",
        "kh1",
        "dw1",
        "witness",
        "xenobladex",
        "star_fox_64",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "huniepop2",
        "civ_6"
    ],
    "voice": [
        "sms",
        "sly1",
        "jakanddaxter",
        "apeescape",
        "cv64",
        "kh1",
        "dw1",
        "witness",
        "xenobladex",
        "star_fox_64",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "huniepop2",
        "civ_6"
    ],
    "acting": [
        "sms",
        "sly1",
        "jakanddaxter",
        "apeescape",
        "cv64",
        "kh1",
        "dw1",
        "witness",
        "xenobladex",
        "star_fox_64",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "huniepop2",
        "civ_6"
    ],
    "psone classics": [
        "spyro3",
        "mm2",
        "apeescape",
        "sotn"
    ],
    "psone": [
        "spyro3",
        "mm2",
        "apeescape",
        "sotn"
    ],
    "classics": [
        "spyro3",
        "mm2",
        "apeescape",
        "sotn"
    ],
    "moving platforms": [
        "k64",
        "mm2",
        "dk64",
        "apeescape",
        "metroidprime",
        "dkc",
        "cvcotm",
        "wl4",
        "sms",
        "sly1",
        "jakanddaxter",
        "v6",
        "sonic_heroes",
        "ladx",
        "dkc3",
        "cv64",
        "blasphemous",
        "spyro3",
        "papermario",
        "sotn"
    ],
    "moving": [
        "k64",
        "mm2",
        "dk64",
        "apeescape",
        "metroidprime",
        "dkc",
        "cvcotm",
        "wl4",
        "sms",
        "sly1",
        "jakanddaxter",
        "v6",
        "sonic_heroes",
        "ladx",
        "dkc3",
        "cv64",
        "blasphemous",
        "spyro3",
        "papermario",
        "sotn"
    ],
    "platforms": [
        "k64",
        "mm2",
        "dk64",
        "apeescape",
        "metroidprime",
        "sm",
        "dkc",
        "cvcotm",
        "wl4",
        "sms",
        "sly1",
        "jakanddaxter",
        "v6",
        "sonic_heroes",
        "doom_ii",
        "ladx",
        "dkc3",
        "sm_map_rando",
        "cv64",
        "blasphemous",
        "zelda2",
        "spyro3",
        "oribf",
        "papermario",
        "sotn"
    ],
    "spiky-haired protagonist": [
        "kh1",
        "jakanddaxter",
        "sonic_heroes",
        "apeescape"
    ],
    "spiky-haired": [
        "kh1",
        "jakanddaxter",
        "sonic_heroes",
        "apeescape"
    ],
    "time trials": [
        "sly1",
        "v6",
        "apeescape",
        "spyro3",
        "mk64",
        "diddy_kong_racing"
    ],
    "trials": [
        "sly1",
        "v6",
        "apeescape",
        "spyro3",
        "mk64",
        "diddy_kong_racing"
    ],
    "sudoku": [
        "apsudoku"
    ],
    "multiplayer": [
        "generic",
        "saving_princess",
        "yachtdice",
        "wordipelago",
        "archipidle",
        "chatipelago",
        "paint",
        "jigsaw",
        "clique",
        "tracker",
        "apsudoku",
        "checksfinder"
    ],
    "archipelago": [
        "generic",
        "saving_princess",
        "yachtdice",
        "wordipelago",
        "archipidle",
        "chatipelago",
        "paint",
        "bumpstik",
        "jigsaw",
        "clique",
        "tracker",
        "apsudoku",
        "checksfinder"
    ],
    "hints": [
        "generic",
        "saving_princess",
        "yachtdice",
        "wordipelago",
        "archipidle",
        "chatipelago",
        "paint",
        "jigsaw",
        "clique",
        "tracker",
        "apsudoku",
        "checksfinder"
    ],
    "multiworld": [
        "generic",
        "saving_princess",
        "yachtdice",
        "wordipelago",
        "archipidle",
        "chatipelago",
        "paint",
        "jigsaw",
        "clique",
        "tracker",
        "apsudoku",
        "checksfinder"
    ],
    "aquaria": [
        "aquaria"
    ],
    "drama": [
        "hades",
        "earthbound",
        "undertale",
        "aquaria"
    ],
    "linux": [
        "rogue_legacy",
        "getting_over_it",
        "minecraft",
        "bumpstik",
        "dontstarvetogether",
        "hk",
        "dungeon_clawler",
        "chainedechoes",
        "crosscode",
        "celeste64",
        "rimworld",
        "cat_quest",
        "shapez",
        "undertale",
        "monster_sanctuary",
        "shorthike",
        "celeste",
        "v6",
        "inscryption",
        "timespinner",
        "factorio",
        "aquaria",
        "overcooked2",
        "osu",
        "huniepop",
        "landstalker",
        "openrct2",
        "blasphemous",
        "terraria",
        "factorio_saws",
        "doom_1993",
        "stardew_valley",
        "ror1"
    ],
    "android": [
        "v6",
        "osrs",
        "blasphemous",
        "getting_over_it",
        "brotato",
        "cat_quest",
        "subnautica",
        "balatro",
        "terraria",
        "musedash",
        "shapez",
        "aquaria",
        "dungeon_clawler",
        "stardew_valley",
        "osu"
    ],
    "ios": [
        "hades",
        "getting_over_it",
        "musedash",
        "dungeon_clawler",
        "witness",
        "osrs",
        "subnautica",
        "cat_quest",
        "residentevil2remake",
        "shapez",
        "v6",
        "balatro",
        "aquaria",
        "residentevil3remake",
        "osu",
        "blasphemous",
        "terraria",
        "brotato",
        "stardew_valley"
    ],
    "alternate costumes": [
        "sms",
        "smo",
        "cv64",
        "kh1",
        "aquaria"
    ],
    "alternate": [
        "sms",
        "smo",
        "cv64",
        "kh1",
        "aquaria"
    ],
    "costumes": [
        "sms",
        "smo",
        "cv64",
        "kh1",
        "aquaria"
    ],
    "underwater gameplay": [
        "sms",
        "sm64hacks",
        "oot",
        "smo",
        "kh1",
        "dkc2",
        "subnautica",
        "terraria",
        "banjo_tooie",
        "aquaria",
        "metroidprime",
        "sm64ex",
        "dkc",
        "mm2"
    ],
    "underwater": [
        "sms",
        "sm64hacks",
        "oot",
        "smo",
        "kh1",
        "dkc2",
        "subnautica",
        "terraria",
        "banjo_tooie",
        "aquaria",
        "metroidprime",
        "sm64ex",
        "dkc",
        "mm2"
    ],
    "shape-shifting": [
        "banjo_tooie",
        "metroidprime",
        "aquaria",
        "k64",
        "kdl3",
        "mm_recomp",
        "sotn"
    ],
    "plot twist": [
        "cv64",
        "kh1",
        "undertale",
        "aquaria",
        "oot"
    ],
    "plot": [
        "cv64",
        "kh1",
        "undertale",
        "aquaria",
        "oot"
    ],
    "twist": [
        "cv64",
        "kh1",
        "undertale",
        "aquaria",
        "oot"
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
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "aus",
        "undertale",
        "celeste"
    ],
    "balatro": [
        "balatro"
    ],
    "turn-based strategy (tbs)": [
        "wargroove",
        "wargroove2",
        "dungeon_clawler",
        "chainedechoes",
        "undertale",
        "monster_sanctuary",
        "papermario",
        "ff1",
        "civ_6",
        "pokemon_frlg",
        "yugioh06",
        "balatro",
        "ffta",
        "pmd_eos",
        "earthbound",
        "yugiohddm",
        "pokemon_rb",
        "hylics2",
        "ff4fe",
        "pokemon_emerald",
        "fm"
    ],
    "turn-based": [
        "wargroove",
        "wargroove2",
        "dungeon_clawler",
        "ffmq",
        "chainedechoes",
        "undertale",
        "monster_sanctuary",
        "papermario",
        "ff1",
        "civ_6",
        "mlss",
        "pokemon_crystal",
        "pokemon_frlg",
        "yugioh06",
        "gstla",
        "balatro",
        "ffta",
        "pmd_eos",
        "earthbound",
        "yugiohddm",
        "pokemon_rb",
        "hylics2",
        "ff4fe",
        "pokemon_emerald",
        "fm"
    ],
    "(tbs)": [
        "wargroove",
        "wargroove2",
        "dungeon_clawler",
        "chainedechoes",
        "undertale",
        "monster_sanctuary",
        "papermario",
        "ff1",
        "civ_6",
        "pokemon_frlg",
        "yugioh06",
        "balatro",
        "ffta",
        "pmd_eos",
        "earthbound",
        "yugiohddm",
        "pokemon_rb",
        "hylics2",
        "ff4fe",
        "pokemon_emerald",
        "fm"
    ],
    "card & board game": [
        "yugiohddm",
        "inscryption",
        "yugioh06",
        "balatro",
        "spire",
        "fm"
    ],
    "card": [
        "yugiohddm",
        "inscryption",
        "yugioh06",
        "balatro",
        "spire",
        "fm"
    ],
    "board": [
        "yugiohddm",
        "inscryption",
        "yugioh06",
        "balatro",
        "spire",
        "fm"
    ],
    "game": [
        "wl",
        "rogue_legacy",
        "tloz_oos",
        "mmbn3",
        "mm2",
        "witness",
        "dkc2",
        "tloz_ooa",
        "oot",
        "cvcotm",
        "wl4",
        "mlss",
        "marioland2",
        "pokemon_crystal",
        "inscryption",
        "pokemon_frlg",
        "yugioh06",
        "gstla",
        "balatro",
        "doom_ii",
        "ffta",
        "earthbound",
        "ladx",
        "hcniko",
        "spire",
        "yugiohddm",
        "pokemon_rb",
        "mzm",
        "spyro3",
        "pokemon_emerald",
        "fm"
    ],
    "roguelike": [
        "rogue_legacy",
        "hades",
        "balatro",
        "dungeon_clawler",
        "pmd_eos",
        "spire",
        "ror1"
    ],
    "banjo-tooie": [
        "banjo_tooie"
    ],
    "quiz/trivia": [
        "banjo_tooie"
    ],
    "comedy": [
        "dlcquest",
        "rogue_legacy",
        "toontown",
        "getting_over_it",
        "musedash",
        "lethal_company",
        "messenger",
        "dk64",
        "kh1",
        "dkc2",
        "rac2",
        "undertale",
        "placidplasticducksim",
        "sly1",
        "jakanddaxter",
        "mlss",
        "cuphead",
        "zork_grand_inquisitor",
        "overcooked2",
        "hcniko",
        "huniepop",
        "doronko_wanko",
        "luigismansion",
        "candybox2",
        "dw1",
        "banjo_tooie",
        "spyro3",
        "sims4",
        "diddy_kong_racing",
        "papermario"
    ],
    "nintendo 64": [
        "sm64hacks",
        "diddy_kong_racing",
        "cv64",
        "banjo_tooie",
        "swr",
        "sm64ex",
        "star_fox_64",
        "mk64",
        "k64",
        "papermario",
        "oot",
        "mm_recomp",
        "dk64"
    ],
    "64": [
        "sm64hacks",
        "diddy_kong_racing",
        "cv64",
        "banjo_tooie",
        "swr",
        "sm64ex",
        "star_fox_64",
        "mk64",
        "k64",
        "papermario",
        "oot",
        "mm_recomp",
        "dk64"
    ],
    "aliens": [
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "factorio_saws",
        "banjo_tooie",
        "factorio",
        "metroidprime",
        "sc2",
        "sm",
        "lethal_company",
        "earthbound",
        "hcniko"
    ],
    "animals": [
        "sly1",
        "dkc3",
        "dkc2",
        "banjo_tooie",
        "star_fox_64",
        "minecraft",
        "diddy_kong_racing",
        "dkc",
        "stardew_valley",
        "hcniko"
    ],
    "flight": [
        "rogue_legacy",
        "xenobladex",
        "hylics2",
        "terraria",
        "banjo_tooie",
        "spyro3",
        "star_fox_64",
        "shorthike",
        "diddy_kong_racing",
        "dkc",
        "mm2",
        "wl4"
    ],
    "witches": [
        "enderlilies",
        "cv64",
        "tloz_oos",
        "banjo_tooie",
        "tloz_ooa"
    ],
    "achievements": [
        "v6",
        "blasphemous",
        "banjo_tooie",
        "musedash",
        "minecraft",
        "oribf",
        "cuphead",
        "doom_ii",
        "hk",
        "sonic_heroes",
        "huniepop2",
        "sotn",
        "stardew_valley",
        "hcniko",
        "tunic",
        "dark_souls_2"
    ],
    "talking animals": [
        "sly1",
        "dkc3",
        "dkc2",
        "banjo_tooie",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "hcniko"
    ],
    "talking": [
        "sly1",
        "dkc3",
        "dkc2",
        "banjo_tooie",
        "star_fox_64",
        "diddy_kong_racing",
        "dkc",
        "hcniko"
    ],
    "breaking the fourth wall": [
        "jakanddaxter",
        "mlss",
        "rogue_legacy",
        "dkc2",
        "banjo_tooie",
        "undertale",
        "doom_ii",
        "dkc",
        "ladx",
        "papermario",
        "ffta"
    ],
    "breaking": [
        "rogue_legacy",
        "dkc2",
        "tloz_ooa",
        "undertale",
        "metroidprime",
        "sm",
        "dkc",
        "oot",
        "wl4",
        "jakanddaxter",
        "mlss",
        "doom_ii",
        "ffta",
        "ladx",
        "sm_map_rando",
        "mzm",
        "banjo_tooie",
        "papermario",
        "sotn"
    ],
    "fourth": [
        "jakanddaxter",
        "mlss",
        "rogue_legacy",
        "dkc2",
        "banjo_tooie",
        "undertale",
        "doom_ii",
        "dkc",
        "ladx",
        "papermario",
        "ffta"
    ],
    "cameo appearance": [
        "jakanddaxter",
        "dkc2",
        "spyro3",
        "banjo_tooie",
        "oot"
    ],
    "cameo": [
        "jakanddaxter",
        "dkc2",
        "spyro3",
        "banjo_tooie",
        "oot"
    ],
    "appearance": [
        "jakanddaxter",
        "dkc2",
        "spyro3",
        "banjo_tooie",
        "oot"
    ],
    "character growth": [
        "oot",
        "pokemon_crystal",
        "banjo_tooie",
        "dk64"
    ],
    "character": [
        "dkc3",
        "pokemon_crystal",
        "dkc2",
        "banjo_tooie",
        "sonic_heroes",
        "dkc",
        "oot",
        "dk64"
    ],
    "growth": [
        "oot",
        "pokemon_crystal",
        "banjo_tooie",
        "dk64"
    ],
    "invisible wall": [
        "kh1",
        "banjo_tooie",
        "mk64",
        "oot",
        "dk64"
    ],
    "invisible": [
        "kh1",
        "banjo_tooie",
        "mk64",
        "oot",
        "dk64"
    ],
    "temporary invincibility": [
        "jakanddaxter",
        "rogue_legacy",
        "dkc2",
        "banjo_tooie",
        "faxanadu",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "mk64",
        "papermario"
    ],
    "temporary": [
        "jakanddaxter",
        "rogue_legacy",
        "dkc2",
        "banjo_tooie",
        "faxanadu",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "mk64",
        "papermario"
    ],
    "invincibility": [
        "jakanddaxter",
        "rogue_legacy",
        "dkc2",
        "banjo_tooie",
        "faxanadu",
        "sonic_heroes",
        "cuphead",
        "doom_ii",
        "mk64",
        "papermario"
    ],
    "gliding": [
        "sms",
        "sly1",
        "kh1",
        "spyro3",
        "banjo_tooie"
    ],
    "lgbtq+": [
        "rogue_legacy",
        "celeste64",
        "timespinner",
        "banjo_tooie",
        "sims4",
        "celeste"
    ],
    "blasphemous": [
        "blasphemous"
    ],
    "role-playing (rpg)": [
        "ctjot",
        "rogue_legacy",
        "tloz_oos",
        "hades",
        "lufia2ac",
        "mmbn3",
        "toontown",
        "wargroove2",
        "dungeon_clawler",
        "chainedechoes",
        "ffmq",
        "crosscode",
        "kh1",
        "osrs",
        "cat_quest",
        "tloz_ooa",
        "undertale",
        "monster_sanctuary",
        "ff1",
        "cvcotm",
        "dsr",
        "mlss",
        "kh2",
        "pokemon_crystal",
        "bomb_rush_cyberfunk",
        "timespinner",
        "pokemon_frlg",
        "noita",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "enderlilies",
        "landstalker",
        "pokemon_rb",
        "candybox2",
        "hylics2",
        "dw1",
        "blasphemous",
        "ff4fe",
        "brotato",
        "terraria",
        "tunic",
        "xenobladex",
        "faxanadu",
        "sims4",
        "zelda2",
        "tloz",
        "dark_souls_3",
        "ufo50",
        "pokemon_emerald",
        "soe",
        "stardew_valley",
        "ror1",
        "papermario",
        "sotn"
    ],
    "role-playing": [
        "ctjot",
        "rogue_legacy",
        "tloz_oos",
        "hades",
        "lufia2ac",
        "mmbn3",
        "toontown",
        "wargroove2",
        "dungeon_clawler",
        "chainedechoes",
        "ffmq",
        "crosscode",
        "kh1",
        "osrs",
        "cat_quest",
        "tloz_ooa",
        "undertale",
        "monster_sanctuary",
        "ff1",
        "cvcotm",
        "dsr",
        "mlss",
        "kh2",
        "pokemon_crystal",
        "bomb_rush_cyberfunk",
        "timespinner",
        "pokemon_frlg",
        "noita",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "enderlilies",
        "landstalker",
        "pokemon_rb",
        "candybox2",
        "hylics2",
        "dw1",
        "blasphemous",
        "ff4fe",
        "brotato",
        "terraria",
        "tunic",
        "xenobladex",
        "faxanadu",
        "sims4",
        "zelda2",
        "tloz",
        "dark_souls_3",
        "ufo50",
        "pokemon_emerald",
        "soe",
        "stardew_valley",
        "ror1",
        "papermario",
        "sotn"
    ],
    "(rpg)": [
        "ctjot",
        "rogue_legacy",
        "tloz_oos",
        "hades",
        "lufia2ac",
        "mmbn3",
        "toontown",
        "wargroove2",
        "dungeon_clawler",
        "chainedechoes",
        "ffmq",
        "crosscode",
        "kh1",
        "osrs",
        "cat_quest",
        "tloz_ooa",
        "undertale",
        "monster_sanctuary",
        "ff1",
        "cvcotm",
        "dsr",
        "mlss",
        "kh2",
        "pokemon_crystal",
        "bomb_rush_cyberfunk",
        "timespinner",
        "pokemon_frlg",
        "noita",
        "gstla",
        "ffta",
        "pmd_eos",
        "earthbound",
        "huniepop",
        "dark_souls_2",
        "meritous",
        "enderlilies",
        "landstalker",
        "pokemon_rb",
        "candybox2",
        "hylics2",
        "dw1",
        "blasphemous",
        "ff4fe",
        "brotato",
        "terraria",
        "tunic",
        "xenobladex",
        "faxanadu",
        "sims4",
        "zelda2",
        "tloz",
        "dark_souls_3",
        "ufo50",
        "pokemon_emerald",
        "soe",
        "stardew_valley",
        "ror1",
        "papermario",
        "sotn"
    ],
    "hack and slash/beat 'em up": [
        "blasphemous",
        "hades",
        "ror1",
        "cv64"
    ],
    "hack": [
        "blasphemous",
        "hades",
        "ror1",
        "cv64"
    ],
    "slash/beat": [
        "blasphemous",
        "hades",
        "ror1",
        "cv64"
    ],
    "'em": [
        "blasphemous",
        "hades",
        "ror1",
        "cv64"
    ],
    "up": [
        "landstalker",
        "pokemon_crystal",
        "cv64",
        "kh1",
        "dw1",
        "blasphemous",
        "hades",
        "zelda2",
        "gstla",
        "sotn",
        "undertale",
        "pokemon_emerald",
        "earthbound",
        "ror1",
        "cvcotm",
        "papermario",
        "dark_souls_2"
    ],
    "bloody": [
        "ultrakill",
        "cv64",
        "heretic",
        "blasphemous",
        "residentevil2remake",
        "metroidprime",
        "doom_ii",
        "sotn"
    ],
    "difficult": [
        "hades",
        "blasphemous",
        "getting_over_it",
        "zelda2",
        "ror1",
        "dontstarvetogether",
        "messenger",
        "celeste",
        "tunic"
    ],
    "side-scrolling": [
        "dkc3",
        "rogue_legacy",
        "sm_map_rando",
        "yoshisisland",
        "hylics2",
        "mzm",
        "dkc2",
        "blasphemous",
        "zelda2",
        "musedash",
        "cuphead",
        "k64",
        "dkc",
        "mm2",
        "kdl3",
        "sm",
        "sotn"
    ],
    "crossover": [
        "smz3",
        "kh1",
        "blasphemous",
        "mk64",
        "diddy_kong_racing",
        "hcniko"
    ],
    "religion": [
        "cv64",
        "blasphemous",
        "oot",
        "earthbound",
        "civ_6"
    ],
    "nudity": [
        "blasphemous",
        "musedash",
        "huniepop2",
        "huniepop",
        "sotn"
    ],
    "2d platformer": [
        "v6",
        "smo",
        "hylics2",
        "blasphemous",
        "hk"
    ],
    "great soundtrack": [
        "ultrakill",
        "bomb_rush_cyberfunk",
        "hylics2",
        "blasphemous",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste",
        "tunic"
    ],
    "great": [
        "ultrakill",
        "bomb_rush_cyberfunk",
        "hylics2",
        "blasphemous",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste",
        "tunic"
    ],
    "soundtrack": [
        "ultrakill",
        "bomb_rush_cyberfunk",
        "hylics2",
        "blasphemous",
        "getting_over_it",
        "undertale",
        "shorthike",
        "celeste",
        "tunic"
    ],
    "parrying": [
        "blasphemous",
        "dark_souls_3",
        "cuphead",
        "hk",
        "dark_souls_2"
    ],
    "soulslike": [
        "enderlilies",
        "blasphemous",
        "dark_souls_2",
        "dark_souls_3",
        "tunic",
        "dsr"
    ],
    "you can pet the dog": [
        "blasphemous",
        "hades",
        "terraria",
        "sims4",
        "seaofthieves",
        "undertale",
        "overcooked2"
    ],
    "you": [
        "blasphemous",
        "hades",
        "terraria",
        "sims4",
        "seaofthieves",
        "undertale",
        "overcooked2"
    ],
    "can": [
        "blasphemous",
        "hades",
        "terraria",
        "sims4",
        "seaofthieves",
        "undertale",
        "overcooked2"
    ],
    "pet": [
        "blasphemous",
        "hades",
        "terraria",
        "sims4",
        "seaofthieves",
        "undertale",
        "overcooked2"
    ],
    "dog": [
        "sly1",
        "smo",
        "doronko_wanko",
        "cv64",
        "tloz_oos",
        "blasphemous",
        "hades",
        "terraria",
        "overcooked2",
        "sims4",
        "star_fox_64",
        "seaofthieves",
        "undertale",
        "oot",
        "soe",
        "hcniko"
    ],
    "interconnected-world": [
        "sm_map_rando",
        "luigismansion",
        "mzm",
        "blasphemous",
        "dark_souls_2",
        "sotn",
        "dark_souls_3",
        "hk",
        "sm",
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
        "ctjot",
        "mmbn3",
        "swr",
        "mm2",
        "lethal_company",
        "crosscode",
        "ultrakill",
        "rimworld",
        "witness",
        "subnautica",
        "rac2",
        "zillion",
        "metroidprime",
        "sm",
        "satisfactory",
        "v6",
        "jakanddaxter",
        "bomb_rush_cyberfunk",
        "factorio",
        "sc2",
        "doom_ii",
        "earthbound",
        "tyrian",
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "terraria",
        "brotato",
        "factorio_saws",
        "ror2",
        "doom_1993",
        "star_fox_64",
        "outer_wilds",
        "soe",
        "ror1",
        "pokemon_frlg"
    ],
    "science": [
        "ctjot",
        "mmbn3",
        "swr",
        "mm2",
        "lethal_company",
        "crosscode",
        "ultrakill",
        "rimworld",
        "witness",
        "subnautica",
        "rac2",
        "zillion",
        "metroidprime",
        "sm",
        "satisfactory",
        "v6",
        "jakanddaxter",
        "bomb_rush_cyberfunk",
        "factorio",
        "sc2",
        "doom_ii",
        "earthbound",
        "tyrian",
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "terraria",
        "brotato",
        "factorio_saws",
        "ror2",
        "doom_1993",
        "star_fox_64",
        "outer_wilds",
        "soe",
        "ror1",
        "pokemon_frlg"
    ],
    "fiction": [
        "ctjot",
        "mmbn3",
        "swr",
        "mm2",
        "lethal_company",
        "crosscode",
        "ultrakill",
        "rimworld",
        "witness",
        "subnautica",
        "rac2",
        "zillion",
        "metroidprime",
        "sm",
        "satisfactory",
        "v6",
        "jakanddaxter",
        "bomb_rush_cyberfunk",
        "factorio",
        "sc2",
        "doom_ii",
        "earthbound",
        "tyrian",
        "sm_map_rando",
        "xenobladex",
        "mzm",
        "terraria",
        "brotato",
        "factorio_saws",
        "ror2",
        "doom_1993",
        "star_fox_64",
        "outer_wilds",
        "soe",
        "ror1",
        "pokemon_frlg"
    ],
    "spiritual successor": [
        "bomb_rush_cyberfunk",
        "mlss",
        "papermario",
        "xenobladex"
    ],
    "spiritual": [
        "bomb_rush_cyberfunk",
        "mlss",
        "papermario",
        "xenobladex"
    ],
    "successor": [
        "bomb_rush_cyberfunk",
        "mlss",
        "papermario",
        "xenobladex"
    ],
    "brotato": [
        "brotato"
    ],
    "fighting": [
        "brotato"
    ],
    "shooter": [
        "heretic",
        "crosscode",
        "ultrakill",
        "rac2",
        "residentevil2remake",
        "metroidprime",
        "sm",
        "noita",
        "cuphead",
        "doom_ii",
        "residentevil3remake",
        "tyrian",
        "sm_map_rando",
        "tboir",
        "mzm",
        "brotato",
        "ror2",
        "doom_1993",
        "star_fox_64",
        "ufo50",
        "ror1"
    ],
    "arcade": [
        "v6",
        "tyrian",
        "ultrakill",
        "megamix",
        "brotato",
        "noita",
        "mario_kart_double_dash",
        "overcooked2",
        "cuphead",
        "mk64",
        "ufo50",
        "smw",
        "dungeon_clawler",
        "messenger",
        "osu",
        "trackmania"
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
    "2": [
        "sly1",
        "jakanddaxter",
        "smo",
        "kh2",
        "candybox2",
        "hylics2",
        "dw1",
        "kh1",
        "rac2",
        "ror2",
        "wargroove2",
        "residentevil2remake",
        "sonic_heroes",
        "overcooked2"
    ],
    "text": [
        "candybox2",
        "osrs",
        "yugioh06",
        "huniepop2",
        "huniepop"
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
    "management": [
        "rimworld",
        "candybox2",
        "sims4",
        "ffta",
        "civ_6"
    ],
    "cat quest": [
        "cat_quest"
    ],
    "cat": [
        "kh1",
        "tloz_oos",
        "dkc2",
        "cat_quest",
        "minecraft",
        "cuphead",
        "wl4"
    ],
    "quest": [
        "dlcquest",
        "dkc2",
        "cat_quest",
        "ffmq"
    ],
    "celeste": [
        "celeste",
        "celeste64"
    ],
    "google stadia": [
        "terraria",
        "celeste",
        "ror2"
    ],
    "google": [
        "terraria",
        "celeste",
        "ror2"
    ],
    "stadia": [
        "terraria",
        "celeste",
        "ror2"
    ],
    "story rich": [
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "undertale",
        "celeste"
    ],
    "rich": [
        "powerwashsimulator",
        "hylics2",
        "hades",
        "getting_over_it",
        "undertale",
        "celeste"
    ],
    "conversation": [
        "v6",
        "undertale",
        "enderlilies",
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
        "hylics2",
        "ff4fe",
        "ffta",
        "ff1",
        "pmd_eos",
        "chainedechoes"
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
        "ss",
        "gstla",
        "metroidprime",
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
    "construction": [
        "terraria",
        "minecraft",
        "civ_6",
        "xenobladex"
    ],
    "mining": [
        "terraria",
        "minecraft",
        "civ_6",
        "stardew_valley"
    ],
    "loot gathering": [
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "dk64"
    ],
    "loot": [
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "dk64"
    ],
    "gathering": [
        "xenobladex",
        "cv64",
        "terraria",
        "civ_6",
        "dk64"
    ],
    "royalty": [
        "rogue_legacy",
        "earthbound",
        "mlss",
        "civ_6"
    ],
    "ambient music": [
        "dkc3",
        "cv64",
        "mzm",
        "dkc2",
        "metroidprime",
        "dkc",
        "soe",
        "civ_6"
    ],
    "ambient": [
        "dkc3",
        "cv64",
        "mzm",
        "dkc2",
        "metroidprime",
        "dkc",
        "soe",
        "civ_6"
    ],
    "music": [
        "musedash",
        "ffmq",
        "ultrakill",
        "dkc2",
        "megamix",
        "metroidprime",
        "placidplasticducksim",
        "dkc",
        "civ_6",
        "gstla",
        "sonic_heroes",
        "doom_ii",
        "ffta",
        "osu",
        "dkc3",
        "cv64",
        "mzm",
        "soe",
        "sotn"
    ],
    "clique": [
        "clique"
    ],
    "crosscode": [
        "crosscode"
    ],
    "16-bit": [
        "rogue_legacy",
        "crosscode",
        "sm_map_rando",
        "sm",
        "earthbound"
    ],
    "a.i. companion": [
        "crosscode",
        "kh1",
        "star_fox_64",
        "oot",
        "sotn"
    ],
    "a.i.": [
        "crosscode",
        "kh1",
        "star_fox_64",
        "oot",
        "sotn"
    ],
    "companion": [
        "crosscode",
        "kh1",
        "star_fox_64",
        "oot",
        "sotn"
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
        "ctjot"
    ],
    "ds": [
        "pmd_eos",
        "ctjot"
    ],
    "cuphead": [
        "cuphead"
    ],
    "pirates": [
        "kh1",
        "mzm",
        "dkc2",
        "tloz_oos",
        "wargroove2",
        "tloz_ooa",
        "seaofthieves",
        "metroidprime",
        "cuphead"
    ],
    "shark": [
        "dkc",
        "jakanddaxter",
        "raft",
        "cuphead"
    ],
    "robots": [
        "sms",
        "ultrakill",
        "xenobladex",
        "swr",
        "star_fox_64",
        "sonic_heroes",
        "cuphead",
        "mm2",
        "earthbound"
    ],
    "dancing": [
        "tloz_ooa",
        "dkc2",
        "dkc3",
        "cuphead"
    ],
    "violent plants": [
        "sms",
        "ss",
        "rogue_legacy",
        "terraria",
        "metroidprime",
        "cuphead"
    ],
    "violent": [
        "sms",
        "ss",
        "rogue_legacy",
        "terraria",
        "metroidprime",
        "cuphead"
    ],
    "plants": [
        "sms",
        "ss",
        "rogue_legacy",
        "terraria",
        "metroidprime",
        "cuphead"
    ],
    "auto-scrolling levels": [
        "v6",
        "dkc3",
        "dkc2",
        "star_fox_64",
        "cuphead",
        "k64",
        "dkc"
    ],
    "auto-scrolling": [
        "v6",
        "dkc3",
        "dkc2",
        "star_fox_64",
        "cuphead",
        "k64",
        "dkc"
    ],
    "levels": [
        "v6",
        "dkc3",
        "dkc2",
        "star_fox_64",
        "cuphead",
        "k64",
        "dkc"
    ],
    "boss assistance": [
        "sms",
        "rogue_legacy",
        "dkc2",
        "cuphead",
        "doom_ii",
        "metroidprime",
        "dkc",
        "oot",
        "papermario",
        "mm_recomp",
        "dark_souls_2"
    ],
    "assistance": [
        "sms",
        "rogue_legacy",
        "dkc2",
        "cuphead",
        "doom_ii",
        "metroidprime",
        "dkc",
        "oot",
        "papermario",
        "mm_recomp",
        "dark_souls_2"
    ],
    "castlevania 64": [
        "cv64"
    ],
    "castlevania": [
        "cv64"
    ],
    "summoning support": [
        "cv64",
        "kh1",
        "gstla",
        "ffta",
        "fm"
    ],
    "summoning": [
        "cv64",
        "kh1",
        "gstla",
        "ffta",
        "fm"
    ],
    "horse": [
        "rogue_legacy",
        "cv64",
        "minecraft",
        "oot",
        "cvcotm",
        "sotn"
    ],
    "multiple protagonists": [
        "dkc3",
        "mlss",
        "rogue_legacy",
        "cv64",
        "dkc2",
        "spyro3",
        "sotn",
        "sonic_heroes",
        "dkc",
        "earthbound",
        "dk64"
    ],
    "protagonists": [
        "dkc3",
        "mlss",
        "rogue_legacy",
        "cv64",
        "dkc2",
        "spyro3",
        "sotn",
        "sonic_heroes",
        "dkc",
        "earthbound",
        "dk64"
    ],
    "traps": [
        "rogue_legacy",
        "cv64",
        "minecraft",
        "doom_ii",
        "dark_souls_2"
    ],
    "bats": [
        "pokemon_crystal",
        "cv64",
        "terraria",
        "zelda2",
        "mk64",
        "cvcotm",
        "sotn"
    ],
    "day/night cycle": [
        "tww",
        "jakanddaxter",
        "ss",
        "pokemon_crystal",
        "cv64",
        "xenobladex",
        "terraria",
        "minecraft",
        "sotn",
        "oot",
        "stardew_valley",
        "mm_recomp",
        "dk64"
    ],
    "day/night": [
        "tww",
        "jakanddaxter",
        "ss",
        "pokemon_crystal",
        "cv64",
        "xenobladex",
        "terraria",
        "minecraft",
        "sotn",
        "oot",
        "stardew_valley",
        "mm_recomp",
        "dk64"
    ],
    "cycle": [
        "tww",
        "jakanddaxter",
        "ss",
        "pokemon_crystal",
        "cv64",
        "xenobladex",
        "terraria",
        "minecraft",
        "sotn",
        "oot",
        "stardew_valley",
        "mm_recomp",
        "dk64"
    ],
    "skeletons": [
        "sly1",
        "cv64",
        "heretic",
        "terraria",
        "seaofthieves",
        "undertale",
        "cvcotm",
        "sotn"
    ],
    "falling damage": [
        "cv64",
        "terraria",
        "minecraft",
        "metroidprime",
        "oot"
    ],
    "falling": [
        "cv64",
        "terraria",
        "minecraft",
        "metroidprime",
        "oot"
    ],
    "unstable platforms": [
        "sms",
        "sly1",
        "v6",
        "sm_map_rando",
        "cv64",
        "zelda2",
        "oribf",
        "metroidprime",
        "doom_ii",
        "dkc",
        "cvcotm",
        "sm"
    ],
    "unstable": [
        "sms",
        "sly1",
        "v6",
        "sm_map_rando",
        "cv64",
        "zelda2",
        "oribf",
        "metroidprime",
        "doom_ii",
        "dkc",
        "cvcotm",
        "sm"
    ],
    "melee": [
        "sly1",
        "pokemon_crystal",
        "cv64",
        "kh1",
        "heretic",
        "terraria",
        "gstla",
        "doom_1993",
        "sotn",
        "wl4",
        "doom_ii",
        "k64",
        "ffta",
        "pokemon_emerald",
        "kdl3",
        "cvcotm",
        "papermario",
        "dark_souls_2"
    ],
    "male antagonist": [
        "sms",
        "mm2",
        "earthbound",
        "cv64"
    ],
    "male": [
        "sms",
        "mm2",
        "earthbound",
        "cv64"
    ],
    "antagonist": [
        "sms",
        "mm2",
        "earthbound",
        "cv64"
    ],
    "instant kill": [
        "v6",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "instant": [
        "v6",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "kill": [
        "v6",
        "cv64",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "difficulty level": [
        "cv64",
        "mzm",
        "star_fox_64",
        "musedash",
        "minecraft",
        "metroidprime",
        "mk64",
        "doom_ii",
        "mm2",
        "osu"
    ],
    "difficulty": [
        "cv64",
        "mzm",
        "star_fox_64",
        "musedash",
        "minecraft",
        "metroidprime",
        "mk64",
        "doom_ii",
        "mm2",
        "osu"
    ],
    "level": [
        "sms",
        "oot",
        "cv64",
        "kh1",
        "mzm",
        "dkc2",
        "star_fox_64",
        "musedash",
        "minecraft",
        "metroidprime",
        "doom_ii",
        "mk64",
        "dkc",
        "mm2",
        "osu"
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
        "mlss",
        "yugiohddm",
        "mzm",
        "mmbn3",
        "yugioh06",
        "gstla",
        "wl4",
        "ffta",
        "pokemon_emerald",
        "earthbound",
        "cvcotm",
        "pokemon_frlg"
    ],
    "boy": [
        "wl",
        "tloz_oos",
        "mmbn3",
        "mm2",
        "tloz_ooa",
        "wl4",
        "cvcotm",
        "mlss",
        "marioland2",
        "pokemon_crystal",
        "yugioh06",
        "gstla",
        "ffta",
        "earthbound",
        "ladx",
        "yugiohddm",
        "pokemon_rb",
        "mzm",
        "pokemon_emerald",
        "pokemon_frlg"
    ],
    "advance": [
        "mlss",
        "yugiohddm",
        "mzm",
        "mmbn3",
        "yugioh06",
        "gstla",
        "wl4",
        "ffta",
        "pokemon_emerald",
        "earthbound",
        "cvcotm",
        "pokemon_frlg"
    ],
    "gravity": [
        "v6",
        "dkc3",
        "mzm",
        "dkc2",
        "star_fox_64",
        "sotn",
        "metroidprime",
        "dkc",
        "oot",
        "cvcotm",
        "papermario",
        "dk64"
    ],
    "wolf": [
        "rogue_legacy",
        "star_fox_64",
        "minecraft",
        "cvcotm",
        "sotn"
    ],
    "leveling up": [
        "landstalker",
        "pokemon_crystal",
        "kh1",
        "dw1",
        "zelda2",
        "gstla",
        "sotn",
        "undertale",
        "pokemon_emerald",
        "earthbound",
        "cvcotm",
        "papermario",
        "dark_souls_2"
    ],
    "leveling": [
        "landstalker",
        "pokemon_crystal",
        "kh1",
        "dw1",
        "zelda2",
        "gstla",
        "sotn",
        "undertale",
        "pokemon_emerald",
        "earthbound",
        "cvcotm",
        "papermario",
        "dark_souls_2"
    ],
    "dark souls ii": [
        "dark_souls_2"
    ],
    "souls": [
        "dark_souls_3",
        "dark_souls_2"
    ],
    "ii": [
        "kh2",
        "ff4fe",
        "mm2",
        "spire",
        "dark_souls_2"
    ],
    "xbox 360": [
        "dlcquest",
        "terraria",
        "sa2b",
        "dark_souls_2",
        "sadx",
        "sotn"
    ],
    "360": [
        "dlcquest",
        "terraria",
        "sa2b",
        "dark_souls_2",
        "sadx",
        "sotn"
    ],
    "spider": [
        "sly1",
        "dkc2",
        "zelda2",
        "minecraft",
        "oribf",
        "dark_souls_2"
    ],
    "customizable characters": [
        "xenobladex",
        "terraria",
        "dark_souls_3",
        "stardew_valley",
        "dark_souls_2"
    ],
    "customizable": [
        "xenobladex",
        "terraria",
        "dark_souls_3",
        "stardew_valley",
        "dark_souls_2"
    ],
    "checkpoints": [
        "sly1",
        "jakanddaxter",
        "v6",
        "dkc3",
        "smo",
        "dkc2",
        "sonic_heroes",
        "dkc",
        "mm2",
        "dark_souls_2"
    ],
    "sliding down ladders": [
        "k64",
        "dark_souls_3",
        "wl4",
        "dark_souls_2"
    ],
    "sliding": [
        "k64",
        "dark_souls_3",
        "wl4",
        "dark_souls_2"
    ],
    "down": [
        "k64",
        "dark_souls_3",
        "wl4",
        "dark_souls_2"
    ],
    "ladders": [
        "k64",
        "dark_souls_3",
        "wl4",
        "dark_souls_2"
    ],
    "fire manipulation": [
        "rogue_legacy",
        "pokemon_crystal",
        "gstla",
        "minecraft",
        "pokemon_emerald",
        "earthbound",
        "papermario",
        "dark_souls_2"
    ],
    "fire": [
        "rogue_legacy",
        "pokemon_crystal",
        "gstla",
        "minecraft",
        "pokemon_emerald",
        "earthbound",
        "papermario",
        "dark_souls_2"
    ],
    "manipulation": [
        "pokemon_emerald",
        "rogue_legacy",
        "pokemon_crystal",
        "sm_map_rando",
        "timespinner",
        "gstla",
        "minecraft",
        "sm",
        "oot",
        "earthbound",
        "papermario",
        "dark_souls_2"
    ],
    "dark souls iii": [
        "dark_souls_3"
    ],
    "iii": [
        "zillion",
        "dark_souls_3"
    ],
    "pick your gender": [
        "pokemon_emerald",
        "terraria",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "pick": [
        "pokemon_emerald",
        "terraria",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "your": [
        "pokemon_emerald",
        "terraria",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "gender": [
        "pokemon_emerald",
        "terraria",
        "dark_souls_3",
        "pokemon_crystal"
    ],
    "entering world in a painting": [
        "sm64ex",
        "smo",
        "dark_souls_3",
        "sm64hacks"
    ],
    "entering": [
        "sm64ex",
        "smo",
        "dark_souls_3",
        "sm64hacks"
    ],
    "painting": [
        "sm64ex",
        "smo",
        "dark_souls_3",
        "sm64hacks"
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
        "diddy_kong_racing",
        "dkc",
        "dk64"
    ],
    "racing": [
        "jakanddaxter",
        "swr",
        "mario_kart_double_dash",
        "mk64",
        "diddy_kong_racing",
        "trackmania"
    ],
    "go-kart": [
        "mario_kart_double_dash",
        "toontown",
        "mk64",
        "diddy_kong_racing"
    ],
    "behind the waterfall": [
        "ss",
        "smo",
        "dkc3",
        "gstla",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "sotn"
    ],
    "behind": [
        "ss",
        "smo",
        "dkc3",
        "gstla",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "sotn"
    ],
    "waterfall": [
        "ss",
        "smo",
        "dkc3",
        "gstla",
        "tloz_ooa",
        "diddy_kong_racing",
        "hcniko",
        "sotn"
    ],
    "donkey kong 64": [
        "dk64"
    ],
    "donkey": [
        "dkc",
        "dkc2",
        "dkc3",
        "dk64"
    ],
    "artificial intelligence": [
        "sly1",
        "jakanddaxter",
        "star_fox_64",
        "metroidprime",
        "mk64",
        "doom_ii",
        "dk64"
    ],
    "artificial": [
        "sly1",
        "jakanddaxter",
        "star_fox_64",
        "metroidprime",
        "mk64",
        "doom_ii",
        "dk64"
    ],
    "intelligence": [
        "sly1",
        "jakanddaxter",
        "star_fox_64",
        "metroidprime",
        "mk64",
        "doom_ii",
        "dk64"
    ],
    "death match": [
        "heretic",
        "mk64",
        "doom_ii",
        "dk64"
    ],
    "match": [
        "heretic",
        "mk64",
        "doom_ii",
        "dk64"
    ],
    "gorilla": [
        "dkc",
        "dkc2",
        "dkc3",
        "dk64"
    ],
    "franchise reboot": [
        "dkc",
        "ffmq",
        "ffta",
        "dk64"
    ],
    "franchise": [
        "dkc",
        "ffmq",
        "ffta",
        "dk64"
    ],
    "reboot": [
        "dkc",
        "ffmq",
        "ffta",
        "dk64"
    ],
    "western games based on japanese ips": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "western": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "games": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "based": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "on": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "doom_ii",
        "dkc",
        "dk64"
    ],
    "japanese": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "ips": [
        "dkc3",
        "dkc2",
        "metroidprime",
        "dkc",
        "dk64"
    ],
    "over 100% completion": [
        "dkc3",
        "dk64",
        "doom_ii",
        "dkc",
        "sotn"
    ],
    "100%": [
        "dkc3",
        "dk64",
        "doom_ii",
        "dkc",
        "sotn"
    ],
    "completion": [
        "dkc3",
        "mzm",
        "dkc2",
        "sotn",
        "metroidprime",
        "doom_ii",
        "dkc",
        "dk64"
    ],
    "completion percentage": [
        "dk64",
        "mzm",
        "dkc2",
        "metroidprime",
        "sotn"
    ],
    "percentage": [
        "dk64",
        "mzm",
        "dkc2",
        "metroidprime",
        "sotn"
    ],
    "mine cart sequence": [
        "dkc",
        "dkc2",
        "ss",
        "dk64"
    ],
    "mine": [
        "dkc",
        "dkc2",
        "ss",
        "dk64"
    ],
    "cart": [
        "dkc",
        "dkc2",
        "ss",
        "dk64"
    ],
    "sequence": [
        "ss",
        "sm_map_rando",
        "mzm",
        "dkc2",
        "tloz_ooa",
        "sotn",
        "metroidprime",
        "doom_ii",
        "dkc",
        "oot",
        "wl4",
        "sm",
        "dk64"
    ],
    "invisibility": [
        "sly1",
        "doom_1993",
        "doom_ii",
        "papermario",
        "dk64"
    ],
    "foreshadowing": [
        "sms",
        "mzm",
        "metroidprime",
        "dk64"
    ],
    "donkey kong country": [
        "dkc"
    ],
    "country": [
        "dkc",
        "dkc2",
        "dkc3"
    ],
    "frog": [
        "jakanddaxter",
        "dkc2",
        "star_fox_64",
        "dkc",
        "hcniko"
    ],
    "overworld": [
        "dkc3",
        "dkc2",
        "zelda2",
        "gstla",
        "tloz",
        "dkc",
        "ffmq",
        "ffta"
    ],
    "bonus stage": [
        "dkc3",
        "dkc2",
        "spyro3",
        "smw",
        "sonic_heroes",
        "dkc"
    ],
    "bonus": [
        "dkc3",
        "dkc2",
        "spyro3",
        "smw",
        "sonic_heroes",
        "dkc"
    ],
    "crocodile": [
        "dkc",
        "sly1",
        "dkc2",
        "dkc3"
    ],
    "water level": [
        "sms",
        "oot",
        "kh1",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "water": [
        "sms",
        "oot",
        "kh1",
        "dkc2",
        "dkc",
        "mm2"
    ],
    "speedrun": [
        "sm64hacks",
        "metroidprime",
        "dkc",
        "sm64ex",
        "sotn"
    ],
    "villain turned good": [
        "dkc",
        "kh1",
        "gstla",
        "sotn"
    ],
    "turned": [
        "dkc",
        "kh1",
        "gstla",
        "sotn"
    ],
    "good": [
        "dkc",
        "kh1",
        "gstla",
        "sotn"
    ],
    "resized enemy": [
        "dkc",
        "oot",
        "dkc2",
        "rogue_legacy"
    ],
    "resized": [
        "dkc",
        "oot",
        "dkc2",
        "rogue_legacy"
    ],
    "enemy": [
        "dkc",
        "oot",
        "dkc2",
        "rogue_legacy"
    ],
    "on-the-fly character switching": [
        "dkc",
        "dkc2",
        "dkc3",
        "sonic_heroes"
    ],
    "on-the-fly": [
        "dkc",
        "dkc2",
        "dkc3",
        "sonic_heroes"
    ],
    "switching": [
        "dkc",
        "dkc2",
        "dkc3",
        "sonic_heroes"
    ],
    "donkey kong country 2": [
        "dkc2"
    ],
    "donkey kong country 2: diddy's kong quest": [
        "dkc2"
    ],
    "2:": [
        "marioland2",
        "yoshisisland",
        "dkc2",
        "sa2b",
        "huniepop2"
    ],
    "diddy's": [
        "dkc2"
    ],
    "climbing": [
        "sms",
        "sly1",
        "jakanddaxter",
        "tloz_oos",
        "dkc2",
        "terraria",
        "tloz_ooa"
    ],
    "game reference": [
        "rogue_legacy",
        "witness",
        "dkc2",
        "spyro3",
        "doom_ii",
        "oot",
        "hcniko"
    ],
    "reference": [
        "rogue_legacy",
        "witness",
        "dkc2",
        "spyro3",
        "placidplasticducksim",
        "doom_ii",
        "oot",
        "hcniko"
    ],
    "sprinting mechanics": [
        "sms",
        "pokemon_emerald",
        "sm64hacks",
        "pokemon_crystal",
        "dkc2",
        "sm64ex",
        "oot",
        "soe",
        "wl4",
        "mm_recomp"
    ],
    "sprinting": [
        "sms",
        "pokemon_emerald",
        "sm64hacks",
        "pokemon_crystal",
        "dkc2",
        "sm64ex",
        "oot",
        "soe",
        "wl4",
        "mm_recomp"
    ],
    "mechanics": [
        "sms",
        "pokemon_emerald",
        "sm64hacks",
        "pokemon_crystal",
        "dkc2",
        "sm64ex",
        "oot",
        "soe",
        "wl4",
        "mm_recomp"
    ],
    "fireworks": [
        "sly1",
        "dkc2",
        "mlss",
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
        "huniepop2",
        "dkc3"
    ],
    "trouble!": [
        "dkc3"
    ],
    "snowman": [
        "sm64ex",
        "sm64hacks",
        "dkc3",
        "papermario"
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
        "dlcquest",
        "v6",
        "smo",
        "timespinner",
        "terraria",
        "minecraft",
        "ufo50",
        "stardew_valley"
    ],
    "deliberately": [
        "dlcquest",
        "v6",
        "smo",
        "timespinner",
        "terraria",
        "minecraft",
        "ufo50",
        "stardew_valley"
    ],
    "punctuation mark above head": [
        "dlcquest",
        "rogue_legacy",
        "pokemon_crystal",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "punctuation": [
        "dlcquest",
        "rogue_legacy",
        "pokemon_crystal",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "mark": [
        "dlcquest",
        "rogue_legacy",
        "pokemon_crystal",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "above": [
        "dlcquest",
        "rogue_legacy",
        "pokemon_crystal",
        "tloz_ooa",
        "pokemon_emerald"
    ],
    "head": [
        "dlcquest",
        "rogue_legacy",
        "pokemon_crystal",
        "tloz_ooa",
        "pokemon_emerald"
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
        "factorio_saws",
        "factorio",
        "minecraft",
        "raft",
        "dontstarvetogether",
        "seaofthieves",
        "stardew_valley",
        "satisfactory"
    ],
    "funny": [
        "powerwashsimulator",
        "getting_over_it",
        "sims4",
        "undertale",
        "dontstarvetogether",
        "shorthike",
        "huniepop2"
    ],
    "survival horror": [
        "residentevil3remake",
        "lethal_company",
        "residentevil2remake",
        "dontstarvetogether"
    ],
    "doom 1993": [
        "doom_1993"
    ],
    "doom": [
        "doom_1993",
        "doom_ii"
    ],
    "dos": [
        "doom_1993",
        "heretic",
        "tyrian",
        "doom_ii"
    ],
    "doom ii": [
        "doom_ii"
    ],
    "doom ii: hell on earth": [
        "doom_ii"
    ],
    "ii:": [
        "lufia2ac",
        "sc2",
        "doom_ii",
        "zelda2"
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
        "rogue_legacy",
        "placidplasticducksim",
        "doom_ii",
        "witness"
    ],
    "pop": [
        "rogue_legacy",
        "placidplasticducksim",
        "doom_ii",
        "witness"
    ],
    "culture": [
        "rogue_legacy",
        "placidplasticducksim",
        "doom_ii",
        "witness"
    ],
    "stat tracking": [
        "rogue_legacy",
        "witness",
        "kh1",
        "doom_ii",
        "ffta",
        "osu"
    ],
    "stat": [
        "rogue_legacy",
        "witness",
        "kh1",
        "doom_ii",
        "ffta",
        "osu"
    ],
    "tracking": [
        "rogue_legacy",
        "witness",
        "kh1",
        "doom_ii",
        "ffta",
        "osu"
    ],
    "rock music": [
        "ultrakill",
        "gstla",
        "sonic_heroes",
        "doom_ii",
        "ffta",
        "ffmq",
        "sotn"
    ],
    "rock": [
        "ultrakill",
        "gstla",
        "sonic_heroes",
        "doom_ii",
        "ffta",
        "ffmq",
        "sotn"
    ],
    "sequence breaking": [
        "sm_map_rando",
        "mzm",
        "tloz_ooa",
        "metroidprime",
        "doom_ii",
        "sm",
        "oot",
        "wl4",
        "sotn"
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
        "luigismansion",
        "dw1",
        "mario_kart_double_dash",
        "sonic_heroes",
        "metroidprime",
        "tww"
    ],
    "gamecube": [
        "sms",
        "luigismansion",
        "dw1",
        "mario_kart_double_dash",
        "sonic_heroes",
        "metroidprime",
        "tww"
    ],
    "playstation 2": [
        "sly1",
        "jakanddaxter",
        "kh2",
        "kh1",
        "dw1",
        "rac2",
        "sonic_heroes"
    ],
    "earthbound": [
        "earthbound"
    ],
    "party system": [
        "mlss",
        "pokemon_crystal",
        "xenobladex",
        "kh1",
        "gstla",
        "ffta",
        "pokemon_emerald",
        "earthbound",
        "ffmq",
        "papermario"
    ],
    "party": [
        "pokemon_emerald",
        "mlss",
        "pokemon_crystal",
        "xenobladex",
        "kh1",
        "gstla",
        "mk64",
        "placidplasticducksim",
        "ffta",
        "overcooked2",
        "earthbound",
        "ffmq",
        "papermario"
    ],
    "censored version": [
        "oot",
        "residentevil2remake",
        "earthbound",
        "xenobladex"
    ],
    "censored": [
        "oot",
        "residentevil2remake",
        "earthbound",
        "xenobladex"
    ],
    "version": [
        "pokemon_emerald",
        "pokemon_crystal",
        "pokemon_rb",
        "xenobladex",
        "residentevil2remake",
        "oot",
        "earthbound",
        "pokemon_frlg"
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
        "oribf",
        "hcniko",
        "enderlilies",
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
        "marioland2",
        "getting_over_it",
        "factorio_saws",
        "sc2"
    ],
    "faxanadu": [
        "faxanadu"
    ],
    "family computer": [
        "faxanadu",
        "ff1",
        "tloz"
    ],
    "family": [
        "powerwashsimulator",
        "zelda2",
        "faxanadu",
        "sims4",
        "tloz",
        "shorthike",
        "ff1",
        "tunic"
    ],
    "computer": [
        "faxanadu",
        "ff1",
        "tloz",
        "zelda2"
    ],
    "nintendo entertainment system": [
        "faxanadu",
        "ff1",
        "tloz",
        "zelda2"
    ],
    "final fantasy": [
        "ff1"
    ],
    "final": [
        "ffta",
        "ff1",
        "ff4fe",
        "ffmq"
    ],
    "kids": [
        "pokemon_emerald",
        "pokemon_crystal",
        "pokemon_rb",
        "tetrisattack",
        "yoshisisland",
        "mario_kart_double_dash",
        "overcooked2",
        "minecraft",
        "mk64",
        "placidplasticducksim",
        "ff1",
        "pmd_eos",
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
        "getting_over_it",
        "sims4",
        "musedash",
        "placidplasticducksim",
        "shorthike",
        "ffmq"
    ],
    "ninja": [
        "ffta",
        "rogue_legacy",
        "messenger",
        "ffmq"
    ],
    "final fantasy tactics advance": [
        "ffta"
    ],
    "tactics": [
        "ffta"
    ],
    "tactical": [
        "ffta",
        "overcooked2",
        "wargroove"
    ],
    "grinding": [
        "tloz_oos",
        "osrs",
        "kh1",
        "seaofthieves",
        "ffta"
    ],
    "random encounter": [
        "pokemon_crystal",
        "kh1",
        "gstla",
        "ffta",
        "pokemon_emerald"
    ],
    "random": [
        "pokemon_crystal",
        "kh1",
        "gstla",
        "ffta",
        "pokemon_emerald"
    ],
    "encounter": [
        "pokemon_crystal",
        "kh1",
        "gstla",
        "ffta",
        "pokemon_emerald"
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
    "generic": [
        "generic"
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
        "getting_over_it",
        "undertale",
        "mm_recomp"
    ],
    "psychological": [
        "lethal_company",
        "getting_over_it",
        "undertale",
        "mm_recomp"
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
        "gstla",
        "ss"
    ],
    "ancient": [
        "jakanddaxter",
        "metroidprime",
        "gstla",
        "ss"
    ],
    "advanced": [
        "jakanddaxter",
        "metroidprime",
        "gstla",
        "ss"
    ],
    "technology": [
        "jakanddaxter",
        "metroidprime",
        "gstla",
        "ss"
    ],
    "battle screen": [
        "mlss",
        "pokemon_crystal",
        "gstla",
        "pokemon_emerald",
        "papermario"
    ],
    "battle": [
        "mlss",
        "pokemon_crystal",
        "mmbn3",
        "sa2b",
        "gstla",
        "pokemon_emerald",
        "papermario"
    ],
    "screen": [
        "mlss",
        "pokemon_crystal",
        "gstla",
        "pokemon_emerald",
        "papermario"
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
        "hylics2",
        "hades",
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
        "stardew_valley",
        "terraria",
        "minecraft",
        "shorthike",
        "hcniko",
        "ladx"
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
        "pokemon_emerald",
        "sotn",
        "metroidprime",
        "hk"
    ],
    "creature": [
        "pokemon_emerald",
        "sotn",
        "metroidprime",
        "hk"
    ],
    "compendium": [
        "pokemon_emerald",
        "sotn",
        "metroidprime",
        "hk"
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
        "stardew_valley",
        "huniepop"
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
        "rogue_legacy"
    ],
    "language selection": [
        "sly1",
        "jakanddaxter",
        "minecraft",
        "yugiohddm"
    ],
    "language": [
        "sly1",
        "jakanddaxter",
        "minecraft",
        "yugiohddm"
    ],
    "selection": [
        "sly1",
        "jakanddaxter",
        "minecraft",
        "yugiohddm"
    ],
    "auto-saving": [
        "jakanddaxter",
        "minecraft",
        "spyro3",
        "witness"
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
        "pokemon_crystal",
        "k64"
    ],
    "shards": [
        "k64"
    ],
    "kid friendly": [
        "openrct2",
        "pokemon_emerald",
        "pokemon_crystal",
        "k64"
    ],
    "kid": [
        "openrct2",
        "pokemon_emerald",
        "pokemon_crystal",
        "k64"
    ],
    "friendly": [
        "powerwashsimulator",
        "pokemon_crystal",
        "openrct2",
        "sims4",
        "shorthike",
        "k64",
        "pokemon_emerald",
        "tunic"
    ],
    "whale": [
        "kh1",
        "kdl3",
        "marioland2",
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
        "wl4",
        "marioland2",
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
        "ladx",
        "pokemon_crystal"
    ],
    "color": [
        "tloz_oos",
        "tloz_ooa",
        "ladx",
        "pokemon_crystal"
    ],
    "chicken": [
        "oot",
        "minecraft",
        "ladx",
        "stardew_valley"
    ],
    "tentacles": [
        "sms",
        "mlss",
        "pokemon_crystal",
        "metroidprime",
        "pokemon_emerald",
        "ladx",
        "papermario"
    ],
    "animal cruelty": [
        "oot",
        "pokemon_emerald",
        "ladx",
        "pokemon_crystal"
    ],
    "cruelty": [
        "oot",
        "pokemon_emerald",
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
        "zillion",
        "landstalker"
    ],
    "mega": [
        "mm2",
        "megamix",
        "mmbn3",
        "landstalker"
    ],
    "drive/genesis": [
        "landstalker"
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
        "yugiohddm",
        "yugioh06",
        "minecraft",
        "lethal_company",
        "stardew_valley",
        "pokemon_frlg"
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
        "sms",
        "sm64hacks",
        "wl",
        "mlss",
        "marioland2",
        "smo",
        "yoshisisland",
        "mario_kart_double_dash",
        "mk64",
        "smw",
        "sm64ex",
        "papermario"
    ],
    "6": [
        "marioland2"
    ],
    "coins": [
        "marioland2"
    ],
    "game boy": [
        "mm2",
        "wl",
        "pokemon_rb",
        "marioland2"
    ],
    "turtle": [
        "sms",
        "sly1",
        "mlss",
        "marioland2",
        "mk64",
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
        "smw",
        "yoshisisland",
        "sms"
    ],
    "princess peach": [
        "sms",
        "sm64hacks",
        "mlss",
        "mario_kart_double_dash",
        "sm64ex"
    ],
    "peach": [
        "sms",
        "sm64hacks",
        "mlss",
        "mario_kart_double_dash",
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
    "metroid prime": [
        "metroidprime"
    ],
    "metroid": [
        "sm",
        "sm_map_rando",
        "metroidprime",
        "smz3"
    ],
    "prime": [
        "metroidprime"
    ],
    "time limit": [
        "sms",
        "rogue_legacy",
        "sm_map_rando",
        "witness",
        "metroidprime",
        "sm",
        "ror1",
        "wl4"
    ],
    "limit": [
        "sms",
        "rogue_legacy",
        "sm_map_rando",
        "witness",
        "metroidprime",
        "sm",
        "ror1",
        "wl4"
    ],
    "countdown timer": [
        "rogue_legacy",
        "sm_map_rando",
        "mzm",
        "metroidprime",
        "sm",
        "oot",
        "wl4"
    ],
    "countdown": [
        "rogue_legacy",
        "sm_map_rando",
        "mzm",
        "metroidprime",
        "sm",
        "oot",
        "wl4"
    ],
    "timer": [
        "rogue_legacy",
        "sm_map_rando",
        "mzm",
        "metroidprime",
        "sm",
        "oot",
        "wl4"
    ],
    "auto-aim": [
        "tww",
        "ss",
        "metroidprime",
        "oot",
        "mm_recomp"
    ],
    "linear gameplay": [
        "sms",
        "sm64ex",
        "metroidprime",
        "sm64hacks"
    ],
    "linear": [
        "sms",
        "sm64ex",
        "metroidprime",
        "sm64hacks"
    ],
    "meme origin": [
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz",
        "metroidprime",
        "mm_recomp",
        "sotn"
    ],
    "meme": [
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz",
        "metroidprime",
        "mm_recomp",
        "sotn"
    ],
    "origin": [
        "zelda2",
        "star_fox_64",
        "minecraft",
        "tloz",
        "metroidprime",
        "mm_recomp",
        "sotn"
    ],
    "isolation": [
        "sm_map_rando",
        "mzm",
        "metroidprime",
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
    "procedural generation": [
        "terraria",
        "minecraft",
        "rogue_legacy",
        "witness"
    ],
    "procedural": [
        "terraria",
        "minecraft",
        "rogue_legacy",
        "witness"
    ],
    "generation": [
        "terraria",
        "minecraft",
        "rogue_legacy",
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
    "saga": [
        "mlss"
    ],
    "super-ness": [
        "sms",
        "sm64ex",
        "mlss",
        "sm64hacks"
    ],
    "wiggler": [
        "sms",
        "sm64hacks",
        "smo",
        "mlss",
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
        "mmbn3"
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
        "rogue_legacy",
        "sm_map_rando",
        "timespinner",
        "sm",
        "oot"
    ],
    "openrct2": [
        "openrct2"
    ],
    "business": [
        "stardew_valley",
        "powerwashsimulator",
        "openrct2"
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
        "sm",
        "oribf",
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
        "pokemon_emerald",
        "rogue_legacy",
        "pokemon_crystal",
        "papermario"
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
        "sims4",
        "powerwashsimulator",
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
        "v6",
        "rogue_legacy",
        "timespinner",
        "terraria",
        "undertale",
        "stardew_valley",
        "ror1"
    ],
    "vita": [
        "v6",
        "rogue_legacy",
        "timespinner",
        "terraria",
        "undertale",
        "stardew_valley",
        "ror1"
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
        "sadx",
        "sa2b",
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
        "sm64ex",
        "sm64hacks"
    ],
    "rabbit": [
        "sm64hacks",
        "smo",
        "terraria",
        "tloz_ooa",
        "sonic_heroes",
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
    "star": [
        "star_fox_64",
        "swr"
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
    "wars:": [
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