from .Items import MomodoraItem, item_table, skill_items, extra_skill_items, sigil_items, optional_sigil_items, grimoire_items, key_items, selin_door, progressive_upgrade_table
GAME_NAME, AUTHOR, VERSION, AP_VERSION = get_archipelago_json()
from .Locations import MomodoraAdvancement, advancement_table, exclusion_table
from .Regions import momodora_regions, link_momodora_areas
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Region, Entrance, Tutorial, Item, ItemClassification
from .Options import MomodoraOptions
from .Rules import set_rules, set_completion_rules
from worlds.AutoWorld import World, WebWorld
from multiprocessing import Process


class MomodoraWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the Momodora Moonlit Farewell Randomizer for MultiworldGG multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["alditto"]
        )
    ]


class MomodoraWorld(World):
    """
    Momodora: Moonlit Farewell is a 2D side-scrolling Metroidvania. 
    The player controls priestess Momo Reinol as she explores an interconnected series of areas. 
    As she explores, she collects items which make her more powerful, and unlocks new abilities 
    which can be used to access different areas of the game world.
    """
    game = GAME_NAME
    igdb_id = IGDB_ID
    author: str = AUTHOR
    options_dataclass = MomodoraOptions
    options: MomodoraOptions
    web = MomodoraWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}
    

    def _get_momodora_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "open_springleaf_path": bool(self.options.open_springleaf_path.value),
            "deathlink": bool(self.options.deathlink.value),
            "oracle_sigil": bool(self.options.oracle_sigil.value),
            "bell_hover_generation": bool(self.options.bell_hover_generation.value),
            "randomize_key_items": bool(self.options.randomize_key_items.value),
            "final_boss_keys": bool(self.options.final_boss_keys.value),
            "progressive_damage_upgrade": bool(self.options.progressive_damage_upgrade.value),
            "progressive_health_upgrade": bool(self.options.progressive_health_upgrade.value),
            "progressive_magic_upgrade": bool(self.options.progressive_magic_upgrade.value),
            "progressive_stamina_upgrade": bool(self.options.progressive_stamina_upgrade.value),
            "progressive_lumen_fairies": bool(self.options.progressive_lumen_fairies.value),
            "victory_condition": self.options.victory_condition.current_key,
            # "fast_travel": self.options.fast_travel.current_key
        }
    
    def get_filler_item_name(self):
        return "100 Lunar Crystals"
    
    def create_items(self):
        # Generate item pool
        itempool = []
        # Add all required progression items
        for name, num in skill_items.items():
            itempool += [name] * num
        #Add useful skill items
        # if self.options.fast_travel.current_key == 2:
        for name, num in extra_skill_items.items():
            itempool += [name] * num
        #Add all sigil items
        for name, num in sigil_items.items():
            itempool += [name] * num
        #Add Grimoire items
        for name, num in grimoire_items.items():
            itempool += [name] * num
        #Add Key Items
        if self.options.randomize_key_items:
            for name, num in key_items.items():
                itempool += [name] * num    
       #Add Oracle Sigil if enabled
        if self.options.oracle_sigil:
            item_table["Progressive Lumen Fairy"] = item_table["Progressive Lumen Fairy"]._replace(classification=ItemClassification.progression)
            for name, num in optional_sigil_items.items():
                itempool += [name] * num
      
        ##Add Final Boss Door if enabled
        if self.options.final_boss_keys:
            for name, num in selin_door.items():
                itempool += [name] * num

        if self.options.progressive_damage_upgrade:
            for name, num in progressive_upgrade_table["progressive_damage"].items():
                itempool += [name] * num

        if self.options.progressive_health_upgrade:
            for name, num in progressive_upgrade_table["progressive_health"].items():
                itempool += [name] * num
        
        if self.options.progressive_magic_upgrade:
            for name, num in progressive_upgrade_table["progressive_magic"].items():
                itempool += [name] * num

        if self.options.progressive_stamina_upgrade:
            for name, num in progressive_upgrade_table["progressive_stamina"].items():
                itempool += [name] * num

        if self.options.progressive_lumen_fairies:
            for name, num in progressive_upgrade_table["progressive_fairy"].items():
                itempool += [name] * num
        
        #Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        # if not self.options.randomize_key_items:
        #     exclusion_pool.update(exclusion_table["random_key_items"])
        # if not self.options.oracle_sigil:
        #     exclusion_pool.update(exclusion_table["oracle_sigil"])

        exclusion_rules(self.multiworld, self.player, exclusion_pool)

        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

    def create_regions(self):
        def MomodoraRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [MomodoraAdvancement(self.player, loc_name, loc_data.id, ret)
                              for loc_name, loc_data in advancement_table.items()
                                if loc_data.region == region_name and
                                (self.options.randomize_key_items or 
                                 loc_name not in exclusion_table["random_key_items"]) and
                                 (self.options.oracle_sigil or
                                  loc_name not in exclusion_table["oracle_sigil"]) and
                                  (self.options.progressive_damage_upgrade or
                                   loc_name not in exclusion_table["progressive_damage"]) and
                                   (self.options.progressive_health_upgrade or
                                    loc_name not in exclusion_table["progressive_health"]) and
                                    (self.options.progressive_magic_upgrade or
                                     loc_name not in exclusion_table["progressive_magic"]) and
                                     (self.options.progressive_stamina_upgrade or
                                      loc_name not in exclusion_table["progressive_stamina"]) and
                                      (self.options.progressive_lumen_fairies or
                                       loc_name not in exclusion_table["progressive_fairy"])]

            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret
        
        self.multiworld.regions += [MomodoraRegion(*r) for r in momodora_regions]
        link_momodora_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        return self._get_momodora_data()
    
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = MomodoraItem(name, item_data.classification, item_data.code, self.player)
        return item