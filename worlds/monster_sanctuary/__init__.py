import copy
import threading
import types
from typing import List, Dict, Optional

from BaseClasses import MultiWorld, Tutorial, ItemClassification, Entrance, Item
from Options import Range, Toggle
from worlds.AutoWorld import World, WebWorld
from Utils import __version__, visualize_regions

from . import data_importer
from . import regions as REGIONS
from . import items as ITEMS
from . import locations as LOCATIONS
from . import rules as RULES
from . import flags as FLAGS
from . import encounters as ENCOUNTERS
from . import hints as HINTS
from .encounters import MonsterData, EncounterData

from .items import ItemData, MonsterSanctuaryItem, MonsterSanctuaryItemCategory
from .items import MonsterSanctuaryItemCategory as ItemCategory
from .locations import MonsterSanctuaryLocationCategory as LocationCategory, MonsterSanctuaryLocation, \
    MonsterSanctuaryLocationCategory, LocationData
from .options import MonsterSanctuaryOptions
from .regions import RegionData, MonsterSanctuaryRegion

GAME_NAME, AUTHOR, VERSION, AP_VERSION = get_archipelago_json()


class MonsterSanctuaryWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Monster Sanctuary with MultiworldGG",
        "English",
        "setup_en.md",
        "setup/en",
        ["Saagael"]
    )]
    theme = "jungle"


def load_data():
    # Load the item and monster data from the json file so that we have access to it anywhere else
    item_id: int = 970500
    item_id = data_importer.load_items(item_id)
    item_id = data_importer.load_monsters(item_id)

    # Load the world second, since this will require having ItemData and MonsterData
    data_importer.load_world()
    data_importer.load_hints()

    # We have to load flags last, as their location data is in world.json, but the item data exists in flags.json
    item_id = data_importer.load_flags(item_id)


class MonsterSanctuaryWorld(World):
    """
    Monster Sanctuary is a pixel art monster collecting game with metroidvania-like exploration and turn based combat developed by Denis Sinner.
    """
    game = GAME_NAME
    igdb_id = IGDB_ID
    author: str = AUTHOR
    web = MonsterSanctuaryWebWorld()
    options_dataclass = MonsterSanctuaryOptions
    options: MonsterSanctuaryOptions

    load_data()

    data_version = 0
    topology_present = True

    item_name_groups = ITEMS.build_item_groups()
    item_name_to_id = {item.name: item.id for item in ITEMS.item_data.values()}
    location_name_to_id = {location.name: location.location_id
                           for location in LOCATIONS.location_data.values()}
    location_names = [location.name for location in LOCATIONS.location_data.values()]
    encounters: Dict[str, EncounterData] = []

    key_of_power_location_id: Optional[int] = None

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.number_of_item_locations = 0

    # is a class method called at the start of generation to check the existence of prerequisite files,
    # usually a ROM for games which require one.
    @classmethod
    def stage_assert_generate(cls, world: MultiWorld):
        pass

    # called per player before any items or locations are created. You can set properties on your world here.
    # Already has access to player options and RNG.
    def generate_early(self) -> None:
        self.randomize_monsters()

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # First, go through and create all the regions
        self.multiworld.regions += [
            MonsterSanctuaryRegion(self.multiworld, self.player, region_name)
            for region_name in REGIONS.region_data
        ]

        self.create_item_locations()
        self.connect_regions()

        # These create locations and place items at those locations.
        # Needs to be done after location creation but before item placement
        self.place_events()
        self.handle_monster_eggs()
        self.place_monsters()

    def create_item_locations(self) -> None:
        """Creates all locations for items, gifts, and rank ups"""
        for location_name in LOCATIONS.location_data:
            location_data = LOCATIONS.location_data[location_name]

            # if the goal is to defeat the mad lord, then
            # we do not add any post-game locations
            if self.options.goal == "defeat_mad_lord" and location_data.postgame:
                continue

            # if the goal is to defeat the mad lord or defeat all champions, then we do not add any
            # locations that require a rank of keeper master
            if ((self.options.goal == "defeat_mad_lord" or self.options.goal == "defeat_all_champions")
                    and location_data.name in LOCATIONS.keeper_master_locations):
                continue

            # If the underworld starts opened, then don't add the item checks for the Eric fight
            if (self.options.open_underworld
                    and location_data.name in ["Blue Cave - Underworld Entrance 1",
                                               "Blue Cave - Underworld Entrance 2"]):
                continue

            # First we check if we should be ignoring these locations based on rando options
            # If we're never allowing shifting, then these locations should not be included, as they
            # require a shifted monster to get.
            if self.options.monster_shift_rule == "never" and location_data.name in [
                "Snowy Peaks - Cryomancer - Light Egg Reward",
                "Snowy Peaks - Cryomancer - Dark Egg Reward"
            ]:
                continue

            if (location_data.name == "Key of Power - Defeat X Champions"
                and self.options.key_of_power_champion_unlock == 0):
                continue

            region = self.multiworld.get_region(location_data.region, self.player)

            access_condition = location_data.access_condition or None

            location = MonsterSanctuaryLocation(
                self.player,
                location_data.name,
                location_name,
                location_data.location_id,
                region,
                access_condition)

            # This is a bit redundant, but we want to change the location name, not the location_data name
            # So we check again down here to update the name specifically.
            if location.name == "Key of Power - Defeat X Champions":
                location.name = f"Key of Power - Defeat {self.options.key_of_power_champion_unlock} Champions"
                location.place_locked_item(self.create_item(location_data.default_item))
                self.key_of_power_location_id = location.address

            if location_data.category == MonsterSanctuaryLocationCategory.RANK:
                # Champion Defeated items are not shown in the spoiler log
                location.show_in_spoiler = False

            # Chest and Gift locations go here
            else:
                # Handle all item rules here
                self.handle_location_placement_options(location, location_data)

                # If not item was locked on this location, we tick up the number of locations needing items
                if location.item is None:
                    location.item_rule = lambda item, world=self, loc=location.name: ITEMS.can_item_be_placed(
                        world, item, loc)
                    self.number_of_item_locations += 1

            region.locations.append(location)

    def handle_location_placement_options(self, location: MonsterSanctuaryLocation, location_data: LocationData):
        def handle_egg_option(option) -> bool:
            if option == "vanilla":
                location.place_locked_item(self.create_item(location_data.default_item))

        if location_data.name in [
            "Snowy Peaks - Cryomancer - Egg Reward 1",
            "Snowy Peaks - Cryomancer - Egg Reward 2",
            "Snowy Peaks - Cryomancer - Light Egg Reward",
            "Snowy Peaks - Cryomancer - Dark Egg Reward"]:
            handle_egg_option(self.options.cryomancer_check_restrictions)
        elif location_data.name == "Sun Palace - Caretaker 1":
            handle_egg_option(self.options.koi_egg_placement)
        elif location_data.name == "Magma Chamber - Bex":
            handle_egg_option(self.options.skorch_egg_placement)
        elif location_data.name == "Forgotten World - Wanderer Room":
            handle_egg_option(self.options.bard_egg_placement)
        elif location_data.name in [
            "Eternity's End - Spectral Wolf",
            "Eternity's End - Spectral Eagle",
            "Eternity's End - Spectral Toad",
            "Eternity's End - Spectral Lion",
        ]:
            handle_egg_option(self.options.spectral_familiar_egg_placement)

    def connect_regions(self) -> None:
        """Connects all regions according to their access conditions"""
        for region_name in REGIONS.region_data:
            region_data = REGIONS.region_data[region_name]
            region = self.multiworld.get_region(region_name, self.player)

            for connection in region_data.connections:
                # If target region isn't defined, continue on.
                # This is because we haven't mapped out the whole world yet and some connections are placeholders
                target_region_data = REGIONS.region_data.get(connection.region)
                if target_region_data is None:
                    continue

                access_condition = connection.access_rules or None

                # Build the Entrance data
                connection_name = f"{region_data.name} to {connection.region}"
                entrance = Entrance(self.player, connection_name, region)
                entrance.access_rule = lambda state, rules=access_condition: rules.has_access(state, self.player)

                # Add it to the region's exits, and connect to the other region's entrance
                region.exits.append(entrance)
                entrance.connect(self.multiworld.get_region(connection.region, self.player))

    def set_victory_condition(self) -> None:
        if self.options.goal == "defeat_mad_lord":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Victory", self.player))

        elif self.options.goal == "defeat_all_champions":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Champion Defeated", self.player, 27))

    def place_ranks(self) -> None:
        """Creates the locations for rank ups, and locks Champion Defeated items to those locations"""
        for location_name in [loc.name
                              for name, loc in LOCATIONS.location_data.items()
                              if LOCATIONS.location_data[name].category == MonsterSanctuaryLocationCategory.RANK]:
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(self.create_item("Champion Defeated"))

    def place_events(self) -> None:
        """Creates locations for all flags, and places flag items at those locations"""
        for location_name, data in FLAGS.flag_data.items():
            # If blob burg is unlocked, we don't need to place the blob key used events
            if (location_name in ["stronghold_dungeon_blob_key", "mystical_workshop_blob_key", "sun_palace_blob_key"]
                    and (self.options.open_blob_burg == "entrances" or self.options.open_blob_burg == "full")):
                continue

            # If magma chamber is open, don't place the flag to lower the lava
            if (location_name == "magma_chamber_lower_lava" and
                    (self.options.open_magma_chamber == "lower_lava" or self.options.open_magma_chamber == "full")):
                continue

            region = self.multiworld.get_region(data.region, self.player)
            access_condition = data.access_condition or None
            location = MonsterSanctuaryLocation(
                player=self.player,
                name=data.location_name,
                logical_name=location_name,
                parent=region,
                access_condition=access_condition)

            if not hasattr(data, "item_id"):
                breakpoint()

            event_item = MonsterSanctuaryItem(
                self.player,
                data.item_id,
                data.item_name,
                data.item_classification)

            location.place_locked_item(event_item)
            region.locations.append(location)

    def handle_monster_eggs(self):
        eggs = []

        def resolve_egg_item(monster_name: str) -> MonsterSanctuaryItem:
            if self.options.randomize_monsters == "by_specie":
                return self.create_item(self.species_swap[monster_name].egg_name())
            else:
                return self.create_item(ENCOUNTERS.get_monster(monster_name).egg_name())

        # If eggs are not found in their vanilla spot we add them to the item pool
        if self.options.cryomancer_check_restrictions != "vanilla":
            eggs.append(resolve_egg_item("Shockhopper"))

        if self.options.koi_egg_placement != "vanilla":
            eggs.append(resolve_egg_item("Koi"))

        if self.options.skorch_egg_placement != "vanilla":
            eggs.append(resolve_egg_item("Skorch"))

        if self.options.bard_egg_placement != "vanilla":
            eggs.append(resolve_egg_item("Bard"))

        if self.options.spectral_familiar_egg_placement != "vanilla":
            eggs.append(resolve_egg_item("Spectral Wolf"))
            eggs.append(resolve_egg_item("Spectral Eagle"))
            eggs.append(resolve_egg_item("Spectral Toad"))
            eggs.append(resolve_egg_item("Spectral Lion"))

        # These monsters are never encountered in the wild naturally, so if we're shuffling monsters
        # we need to make sure that they're available in the item pools so all locations are reachable
        if self.options.randomize_monsters == "by_specie":
            eggs += [
                resolve_egg_item("Mad Lord"),
                resolve_egg_item("Plague Egg"),
                resolve_egg_item("Tanuki"),
                resolve_egg_item("Sizzle Knight"),
                resolve_egg_item("Ninki"),

                self.create_item(ENCOUNTERS.get_monster("Akhlut").egg_name()),
                self.create_item(ENCOUNTERS.get_monster("Gryphonix").egg_name()),
                self.create_item(ENCOUNTERS.get_monster("Krakaturtle").egg_name()),
            ]

        # Always put dodo eggs in the pool
        dodo_egg = ENCOUNTERS.get_monster("Dodo").egg_name()
        eggs += [
            self.create_item(dodo_egg),
            self.create_item(f"Light-Shifted {dodo_egg}"),
            self.create_item(f"Dark-Shifted {dodo_egg}"),
        ]

        # Depending on the options, these eggs are either added to the pool, or locked
        # into their default location
        self.multiworld.itempool += list(egg for egg in eggs)
        self.number_of_item_locations -= len(eggs)

    def randomize_monsters(self):
        ENCOUNTERS.randomize(self)

    def place_monsters(self) -> None:
        """Creates event locations for all monsters, and places monster items at those locations"""
        for encounter_name, encounter in self.encounters.items():
            region = self.multiworld.get_region(encounter.region, self.player)

            monster_index = 0
            for monster in encounter.monsters:
                location = MonsterSanctuaryLocation(
                    player=self.player,
                    name=f"{encounter.name}_{monster_index}",
                    logical_name=f"{encounter.name}_{monster_index}",
                    parent=region,
                    access_condition=encounter.access_condition or None)
                location.show_in_spoiler = False

                monster_item = MonsterSanctuaryItem(
                    self.player,
                    monster.id,
                    monster.name,
                    ItemClassification.progression)

                location.place_locked_item(monster_item)
                region.locations.append(location)
                monster_index += 1

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        ITEMS.build_item_probability_table({
            MonsterSanctuaryItemCategory.CRAFTINGMATERIAL: self.options.drop_chance_craftingmaterial.value,
            MonsterSanctuaryItemCategory.CONSUMABLE: self.options.drop_chance_consumable.value,
            MonsterSanctuaryItemCategory.FOOD: self.options.drop_chance_food.value,
            MonsterSanctuaryItemCategory.CATALYST: self.options.drop_chance_catalyst.value,
            MonsterSanctuaryItemCategory.WEAPON: self.options.drop_chance_weapon.value,
            MonsterSanctuaryItemCategory.ACCESSORY: self.options.drop_chance_accessory.value,
            MonsterSanctuaryItemCategory.CURRENCY: self.options.drop_chance_currency.value,
        })
        pool: List[MonsterSanctuaryItem] = []

        # ITEMS
        # These items are not naturally put in the general item pool, and are handled separately
        item_exclusions = ["Multiple"]

        if self.options.automatically_scale_equipment.value != "disabled":
            item_exclusions += ["Leveled"]

        self.handle_relics(pool, item_exclusions)
        self.handle_key_items(pool)
        self.handle_explore_ability_items(pool)
        self.handle_area_keys(pool)

        while len(pool) < self.number_of_item_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                pool.append(self.create_item(item_name))

        self.multiworld.itempool += pool

    def handle_key_items(self, pool: List[MonsterSanctuaryItem]) -> None:
        key_items = [item_name for item_name in ITEMS.item_data
                     if ITEMS.item_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM
                     and not ITEMS.is_item_in_group(item_name, "Area Key")]

        # If the key of power is supposed to be given when defeating champions, then it doesn't go in the pool
        if (self.options.key_of_power_champion_unlock.value != 0 or
            (self.options.open_abandoned_tower == "entrances" or self.options.open_abandoned_tower == "full")):
            key_items.remove("Key of Power")

        # If blob burg is unlocked via options, then remove the blob key from the item pool
        if self.options.open_blob_burg == "entrances" or self.options.open_blob_burg == "full":
            key_items.remove("Blob Key")

        # If magma chamber has its lava lowered via options, remove runestone shard from the item pool
        if self.options.open_magma_chamber == "lower_lava" or self.options.open_magma_chamber == "full":
            key_items.remove("Runestone Shard")

        # If the underworld entrance is opened up, don't add sanctuary tokens to the item pool
        if self.options.open_underworld == "entrances" or self.options.open_underworld == "full":
            key_items.remove("Sanctuary Token")

        if not self.options.include_looters_handbook:
            key_items.remove("Looter's Handbook")

        # Add items that are not technically key items, but are progressions items and should be added
        key_items.append("Raw Hide")
        key_items.extend([name for name, item in ITEMS.item_data.items()
                          if item.category == MonsterSanctuaryItemCategory.CATALYST])

        for key_item in key_items:
            for i in range(ITEMS.item_data[key_item].count):
                pool.append(self.create_item(key_item))

    def handle_explore_ability_items(self, pool: List[MonsterSanctuaryItem]):
        explore_items = ITEMS.get_explore_ability_items(self.options.lock_explore_abilities.value)

        for item in explore_items:
            pool.append(self.create_item(item.name))

    def handle_area_keys(self, pool: List[MonsterSanctuaryItem]) -> None:
        # If all locked doors are being removed, then we don't need to consider adding keys
        if self.options.remove_locked_doors == "all":
            return

        keys = [item_name for item_name in ITEMS.item_data
                if ITEMS.item_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM
                and ITEMS.is_item_in_group(item_name, "Area Key")]

        for key in keys:
            item_count = ITEMS.item_data[key].count

            if self.options.remove_locked_doors == "minimal":
                # If we're opening some doors, then we modify the number of keys placed
                if key == "Ancient Woods key":
                    item_count = 2
                elif key == "Mystical Workshop key":
                    item_count = 3
                else:
                    item_count = 1

            for i in range(item_count):
                pool.append(self.create_item(key))

    def handle_relics(self, pool: List[MonsterSanctuaryItem], item_exclusions: List[str]):
        # Exclude relics of chaos if the option isn't enabled
        relics: List[ItemData] = []
        if self.options.include_chaos_relics == "off":
            item_exclusions.append("Relic")
        elif self.options.include_chaos_relics == "on":
            pass  # Relics can be randomly put in the item pool, nothing to do here.
        elif self.options.include_chaos_relics == "some":
            relics = self.random.sample(ITEMS.get_items_in_group("Relic"), 5)
        elif self.options.include_chaos_relics == "all":
            relics = ITEMS.get_items_in_group("Relic")

        for relic in relics:
            relic_name = ITEMS.roll_random_equipment_level(self, relic)
            pool.append(self.create_item(relic_name))

    def create_item(self, item_name: str) -> MonsterSanctuaryItem:
        data = ITEMS.item_data.get(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.id, item_name, data.classification)

        data = ENCOUNTERS.monster_data.get(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.id, data.name, ItemClassification.progression)

        data = FLAGS.get_flag_by_item_name(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.item_id, data.item_name, data.item_classification)

        raise KeyError(f"Item '{item_name}' has no data")

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    # Rules are handled as AccessCondition objects within locations and connections
    def set_rules(self) -> None:
        if self.options.local_area_keys:
            self.options.local_items.value |= self.item_name_groups["Area Key"]

        def only_allow_filler_at_location(loc_name: str):
            location = self.get_location(loc_name)
            if location is not None:
                location.item_rule = lambda item: item.classification == ItemClassification.filler

        if self.options.koi_egg_placement == "filler":
            only_allow_filler_at_location("Sun Palace - Caretaker 1")

        if self.options.skorch_egg_placement == "filler":
            only_allow_filler_at_location("Magma Chamber - Bex")

        if self.options.bard_egg_placement == "filler":
            only_allow_filler_at_location("Forgotten World - Wanderer Room")

        if self.options.spectral_familiar_egg_placement == "filler":
            only_allow_filler_at_location("Eternity's End - Spectral Wolf")
            only_allow_filler_at_location("Eternity's End - Spectral Eagle")
            only_allow_filler_at_location("Eternity's End - Spectral Toad")
            only_allow_filler_at_location("Eternity's End - Spectral Lion")

        if self.options.cryomancer_check_restrictions == "filler":
            only_allow_filler_at_location("Snowy Peaks - Cryomancer - Egg Reward 1")
            only_allow_filler_at_location("Snowy Peaks - Cryomancer - Egg Reward 2")

            if self.options.monster_shift_rule != "never":
                only_allow_filler_at_location("Snowy Peaks - Cryomancer - Light Egg Reward")
                only_allow_filler_at_location("Snowy Peaks - Cryomancer - Dark Egg Reward")

        if self.options.old_man_check_restrictions == "filler":
            only_allow_filler_at_location("Horizon Beach - Old Man by the Sea")

        if self.options.fisherman_check_restrictions == "filler":
            only_allow_filler_at_location("Horizon Beach - Fisherman")

        if self.options.wanderers_gift_check_restrictions == "filler":
            only_allow_filler_at_location("Forgotten World - Crystal Room - Defeat Dracomer Reward")


    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        self.set_victory_condition()
        self.place_ranks()

    # creates the output files if there is output to be generated. When this is called,
    # self.multiworld.get_locations(self.player) has all locations for the player, with attribute
    # item pointing to the item. location.item.player can be used to see if it's a local item.
    def generate_output(self, output_directory: str) -> None:
        visualize_regions(self.multiworld.get_region("Menu", self.player), "world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        if self.options.hints:
            self.hint_rng = self.random
            HINTS.generate_hints(self)

        slot_data = {
            "version": "1.3.7.0",
            "options": {
                "goal": self.options.goal.value,
                "logic_difficulty": self.options.logic_difficulty.value,
                "tedious_checks": self.options.tedious_checks.value,

                "starting_gold": self.options.starting_gold.value,
                "add_smoke_bombs": self.options.add_smoke_bombs.value,
                "include_chaos_relics": self.options.include_chaos_relics.value,
                "automatically_scale_equipment": self.options.automatically_scale_equipment.value,
                "key_of_power_champion_unlock": self.options.key_of_power_champion_unlock.value,
                
                "monsters_always_drop_egg": self.options.monsters_always_drop_egg.value,
                "monsters_always_drop_catalyst": self.options.monsters_always_drop_catalyst.value,
                "monster_shift_rule": self.options.monster_shift_rule.value,
                "randomize_monster_skill_trees": self.options.randomize_monster_skill_trees.value,
                "randomize_monster_ultimates": self.options.randomize_monster_ultimates.value,
                "randomize_monster_shift_skills": self.options.randomize_monster_shift_skills.value,
                "lock_explore_abilities": self.options.lock_explore_abilities.value,

                "skip_plot": self.options.skip_plot.value,
                "skip_keeper_battles": self.options.skip_keeper_battles.value,
                "remove_locked_doors": self.options.remove_locked_doors.value,
                "open_blue_caves": self.options.open_blue_caves.value,
                "open_stronghold_dungeon": self.options.open_stronghold_dungeon.value,
                "open_ancient_woods": self.options.open_ancient_woods.value,
                "open_snowy_peaks": self.options.open_snowy_peaks.value,
                "open_sun_palace": self.options.open_sun_palace.value,
                "open_horizon_beach": self.options.open_horizon_beach.value,
                "open_magma_chamber": self.options.open_magma_chamber.value,
                "open_forgotten_world": self.options.open_forgotten_world.value,
                "open_blob_burg": self.options.open_blob_burg.value,
                "open_underworld": self.options.open_underworld.value,
                "open_mystical_workshop": self.options.open_mystical_workshop.value,
                "open_abandoned_tower": self.options.open_abandoned_tower.value,

                "no_progression_in_underworld": self.options.no_progression_in_underworld.value,
                "no_progression_in_forgotten_world": self.options.no_progression_in_forgotten_world.value,
                "cryomancer_check_restrictions": self.options.cryomancer_check_restrictions.value,
                "old_man_check_restrictions": self.options.old_man_check_restrictions.value,
                "fisherman_check_restrictions": self.options.fisherman_check_restrictions.value,
                "wanderers_gift_check_restrictions": self.options.wanderers_gift_check_restrictions.value,
                "koi_egg_placement": self.options.koi_egg_placement.value,
                "skorch_egg_placement": self.options.skorch_egg_placement.value,
                "bard_egg_placement": self.options.bard_egg_placement.value,
                "spectral_familiar_egg_placement": self.options.spectral_familiar_egg_placement.value,

                "death_link": self.options.death_link.value
            }
        }

        if self.key_of_power_location_id is not None:
            slot_data["key_of_power_champion_unlock"] = self.key_of_power_location_id

        # Monster randos
        tanuki_location = self.multiworld.get_location("Menu_0_0", self.player)
        slot_data["monsters"] = {
            "tanuki": tanuki_location.item.name,
        }

        # If we're shuffling monsters, then we want to show what Bex and the Caretaker's monsters are
        # so the player knows if they are needed for progression
        if self.options.randomize_monsters == "by_specie":
            slot_data["monsters"]["bex_monster"] = self.species_swap["Skorch"].name

        slot_data["monsters"]["monster_locations"] = {}
        slot_data["monsters"]["champions"] = {}
        for encounter_name, encounter in self.encounters.items():
            parts = encounter_name.split('_')

            # location names for monsters need to be without the subsection, so we only
            # take the first two parts of the name, then append the monster id
            location_name_base = f"{parts[0]}_{parts[1]}_{encounter.encounter_id}"
            for i in range(len(encounter.monsters)):
                location_name = f"{location_name_base}_{i}"
                slot_data["monsters"]["monster_locations"][location_name] = encounter.monsters[i].name

            if encounter.champion:
                # Monster is either the first and only mon, or the second mon
                monster = encounter.monsters[0]
                i = 0
                if len(encounter.monsters) > 1:
                    monster = encounter.monsters[1]
                    i = 1
                # We only need the scene name to be able to map champions
                slot_data["monsters"]["champions"][f"{parts[0]}_{parts[1]}"] = monster.name

        slot_data["locations"] = {}
        slot_data["locations"]["ranks"] = {}
        for location in self.multiworld.get_locations(self.player):
            region = location.parent_region
            if region.name.startswith("Menu"):  # Ignore menu locations
                continue
            if '_' in location.name:  # Ignore monster locations and flags
                continue
            if location.item.code is None:  # Ignore events
                continue

            name = LOCATIONS.get_location_name_for_client(location.logical_name)
            if name is None:
                continue

            area = region.name.split("_")[0]
            if area not in slot_data["locations"]:
                slot_data["locations"][area] = {}

            slot_data["locations"][area][name] = location.address

            # If this is a champion defeated item, then add it to the ranks dictionary
            if location.logical_name.endswith("_Champion"):
                slot_data["locations"]["ranks"][name] = location.address

        if self.options.hints and hasattr(self, "hints"):
            # There's probably a much better way of doing this.
            # I just want an anonymous object that will serialize, but correctly
            # but using the actual Hint data type here will cause Multiesrver to crash
            slot_data["hints"] = []
            i = 0
            for hint in self.hints:
                slot_data["hints"].append({})
                slot_data["hints"][i]["id"] = hint.id
                slot_data["hints"][i]["text"] = hint.text
                slot_data["hints"][i]["ignore_other_text"] = hint.ignore_other_text
                i += 1

        return slot_data
