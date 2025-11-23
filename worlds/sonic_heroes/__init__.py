from typing import TextIO, Callable, Any

from BaseClasses import *
from worlds.AutoWorld import World, WebWorld
from . import csvdata
from .constants import *
from .csvdata import *
from .items import *
from .logic_mapping_sonic import *
from .options import *  # type: ignore
from .regions import *


class SonicHeroesWeb(WebWorld):
    theme = PARTYTIMETHEME
    setup_en = (Tutorial(
        tutorial_name=TUTORIALNAME,
        description=TUTORIALDESC,
        language=TUTORIALLANGUAGE,
        file_name=TUTORIALFILENAME,
        link=TUTORIALLINK,
        authors=TUTORIALAUTHORS
    ))

    tutorials = [setup_en]
    #option_groups = sonic_heroes_option_groups


class SonicHeroesWorld(World):
    """
    Sonic Heroes is a 2003 platform game developed by Sonic Team USA. The player races a team of series characters through levels to amass rings, 
    defeat robots, and collect the seven Chaos Emeralds needed to defeat Doctor Eggman. Within each level, the player switches between the team's three characters, 
    who each have unique abilities, to overcome obstacles.
    """
    game = SONICHEROES
    web = SonicHeroesWeb()
    options_dataclass = SonicHeroesOptions
    options: SonicHeroesOptions
    item_name_to_id: ClassVar[dict[str, int]] = \
    {item.name: item.code for item in itemList}
    location_name_to_id: ClassVar[dict[str, int]] = {loc.name: loc.code for loc in get_full_location_list()}
    #{k: v for k, v in full_location_dict.items()}

    topology_present = True

    #UT Stuff Here
    ut_can_gen_without_yaml = True

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data


    def __init__(self, multiworld: MultiWorld, player: int):
        #PUT STUFF HERE
        #self.loc_id_to_loc = {}

        self.secret: bool = False
        self.level_goal_event_locations: list[str] = []
        self.team_level_goal_event_locations: dict[str, list[str]] = {}
        self.bonus_key_event_items_per_team: dict[str, dict[str, list[str]]] = {}
        self.bonus_keys_needed_for_bonus_stage: int = 1
        self.region_to_location: dict[str, list[LocationCSVData]] = {}
        self.region_list: list[RegionCSVData] = []
        self.connection_list: list[ConnectionCSVData] = []
        self.logic_mapping_dict: dict[str, dict[str, dict[str, CollectionState]]] = {}
        self.spoiler_string: str = ""
        self.extra_items: int = 0

        self.regular_regions = \
        [
            OCEANREGION,
            HOTPLANTREGION,
            CASINOREGION,
            TRAINREGION,
            BIGPLANTREGION,
            GHOSTREGION,
            SKYREGION,
        ]

        self.enabled_teams = \
        [
            SONIC,
            #DARK,
            #ROSE,
            #CHAOTIX,
            #SUPERHARD,
        ]

        self.regular_levels = \
        [
            SEASIDEHILL,
            OCEANPALACE,
            GRANDMETROPOLIS,
            POWERPLANT,
            CASINOPARK,
            BINGOHIGHWAY,
            RAILCANYON,
            BULLETSTATION,
            FROGFOREST,
            LOSTJUNGLE,
            HANGCASTLE,
            MYSTICMANSION,
            EGGFLEET,
            FINALFORTRESS,
        ]

        #self.allowed_levels = []

        self.allowed_levels_per_team: dict[str, list[str]] = {}

        self.should_make_puml: bool = False

        self.is_ut_gen: bool = False

        super().__init__(multiworld, player)


    def create_item(self, name: str) -> "Item":
        tempitems = [x for x in itemList if x.name == name]
        if len(tempitems) == 0:
            return SonicHeroesItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        return SonicHeroesItem(name, tempitems[0].classification, self.item_name_to_id[name], self.player)

    def generate_early(self) -> None:


        #UT Stuff Here
        self.handle_ut_yamlless(None)



        #Check invalid options here
        check_invalid_options(self)

        if self.options.goal_unlock_condition == 1:
            self.options.goal_level_completions.value = 0


        """
        #UT Stuff Here
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if SONICHEROES not in self.multiworld.re_gen_passthrough:
                return
            passthrough = self.multiworld.re_gen_passthrough[SONICHEROES]
            self.options.goal_unlock_condition = passthrough["goal_unlock_condition"]
        """

        create_special_region_csv_data(self)

        if self.options.sonic_story > 0:
            self.allowed_levels_per_team[SONIC] = self.regular_levels

            # handle rule mapping here
            self.logic_mapping_dict[SONIC] = self.init_logic_mapping_sonic()

            #import csv data
            self.import_csv_data(SONIC)


            #level completion event locs
            self.team_level_goal_event_locations[SONIC] = []
            self.bonus_key_event_items_per_team[SONIC] = {}

            for level in self.allowed_levels_per_team[SONIC]:
                self.bonus_key_event_items_per_team[SONIC][level] = []

            #map regions
            #map_sonic_regions(self)
            #map locations
            #map_sonic_locations(self)
            #map connections
            #map_sonic_connections(self)

        pass




    def create_regions(self) -> None:
        create_regions(self)

        victory_item = SonicHeroesItem(VICTORYITEM, ItemClassification.progression,
                                       None, self.player)
        self.get_location(VICTORYLOCATION).place_locked_item(victory_item)

        #print(self.level_goal_event_locations)

        index = 1 if self.secret else 0

        for team in self.allowed_levels_per_team.keys():
            for loc_name in self.team_level_goal_event_locations[team]:
                goal_unlock_item = SonicHeroesItem(f"{team} {loc_name} {COMPLETIONEVENT}", ItemClassification.progression, None, self.player)
                self.get_location(f"{loc_name} {team} Goal Event Location").place_locked_item(goal_unlock_item)

            for level in self.allowed_levels_per_team[team]:
                for key in range(bonus_key_amounts[team][level][index]):
                    self.bonus_key_event_items_per_team[team][level].append(f"{team} {level} Bonus Key #{key + 1} Event")
                    key_event_item = SonicHeroesItem(f"{team} {level} Bonus Key #{key + 1} Event", ItemClassification.progression, None, self.player)
                    self.get_location(f"{level} {team} Bonus Key {key + 1} Event").place_locked_item(key_event_item)
        pass


    def create_items(self) -> None:
        create_items(self)

        if self.options.sonic_story_starting_character == 0:
            self.multiworld.push_precollected(self.create_item(PLAYABLESONIC))
        if self.options.sonic_story_starting_character == 1:
            self.multiworld.push_precollected(self.create_item(PLAYABLETAILS))
        if self.options.sonic_story_starting_character == 2:
            self.multiworld.push_precollected(self.create_item(PLAYABLEKNUCKLES))
        pass


    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(VICTORYITEM, self.player)
        pass

    def connect_entrances(self) -> None:
        connect_entrances(self)
        pass

    def generate_basic(self) -> None:
        pass

    def pre_fill(self) -> None:
        pass

    def post_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str) -> None:
        pass

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        #Location: "Hint"
        pass

    def fill_slot_data(self) -> Mapping[str, Any]:
        if self.should_make_puml:
            from Utils import visualize_regions
            state = self.multiworld.get_all_state(False)
            state.update_reachable_regions(self.player)
            visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
            # !pragma layout smetana
            # put this at top to display PUML (after start UML)
        return \
        {
            "APWorldVersion": "2.0.0",
            "Goal": 0,
            "GoalUnlockCondition": self.options.goal_unlock_condition.value,
            "GoalLevelCompletions": self.options.goal_level_completions.value,
            "AbilityUnlocks": self.options.ability_unlocks.value,
            "SkipMetalMadness": 1,
            "RequiredRank": 0,
            "DontLoseBonusKey": 1,
            "SonicStory": self.options.sonic_story.value,
            "SonicStoryStartingCharacter": self.options.sonic_story_starting_character.value,
            "SuperHardModeSonicAct2": 0,
            "SonicKeySanity": self.options.sonic_key_sanity.value,
            "SonicCheckpointSanity": self.options.sonic_checkpoint_sanity.value,
            "DarkStory": 0,
            "DarkSanity": 0,
            "DarkKeySanity": 0,
            "DarkCheckpointSanity": 0,
            "RoseStory": 0,
            "RoseSanity": 0,
            "RoseKeySanity": 0,
            "RoseCheckpointSanity": 0,
            "ChaotixStory": 0,
            "ChaotixSanity": 0,
            "ChaotixKeySanity": 0,
            "ChaotixCheckpointSanity": 0,
            "SecretLocations": self.secret,
            "RingLink": 1,
            "RingLinkOverlord": 0,
            "ModernRingLoss": 1,
            "DeathLink": 0,

            "RemoveCasinoParkVIPTableLaserGate": self.options.remove_casino_park_vip_table_laser_gate.value,

            "GateEmblemCosts": [1],
            "ShuffledLevels": [f"S{x}" for x in range(2, 16)],
            #"ShuffledLevels": ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11"],
            "ShuffledBosses": ["B23"],
            "GateLevelCounts": [14],
        }

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(self.spoiler_string)
        pass

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
        pass




    def import_csv_data(self, team: str):
        #Regions First
        import_region_csv(self, team)
        #Locations Next
        import_location_csv(self, team)
        #Connections Third
        import_connection_csv(self, team)



    def init_logic_mapping_sonic(self) -> dict[str, dict[str, CollectionState]]:
        return \
            {
                SEASIDEHILL: create_logic_mapping_dict_seaside_hill_sonic(self),
                OCEANPALACE: create_logic_mapping_dict_ocean_palace_sonic(self),
                GRANDMETROPOLIS: create_logic_mapping_dict_grand_metropolis_sonic(self),
                POWERPLANT: create_logic_mapping_dict_power_plant_sonic(self),
                CASINOPARK: create_logic_mapping_dict_casino_park_sonic(self),
                BINGOHIGHWAY: create_logic_mapping_dict_bingo_highway_sonic(self),
                RAILCANYON: create_logic_mapping_dict_rail_canyon_sonic(self),
                BULLETSTATION: create_logic_mapping_dict_bullet_station_sonic(self),
                FROGFOREST: create_logic_mapping_dict_frog_forest_sonic(self),
                LOSTJUNGLE: create_logic_mapping_dict_lost_jungle_sonic(self),
                HANGCASTLE: create_logic_mapping_dict_hang_castle_sonic(self),
                MYSTICMANSION: create_logic_mapping_dict_mystic_mansion_sonic(self),
                EGGFLEET: create_logic_mapping_dict_egg_fleet_sonic(self),
                FINALFORTRESS: create_logic_mapping_dict_final_fortress_sonic(self),
            }


    def init_logic_mapping_any_team(self) -> dict[str, dict[str, CollectionState]]:

        # noinspection PyTypeChecker
        rule_dict: dict[str, dict[str, CollectionState]] = \
        {
            METALMADNESS:
                {
                    "": lambda state: True,  # type: ignore
                },
        }
        rule_dict.update({name: {"": lambda state: True} for name in bonus_and_emerald_stages})  # type: ignore
        return rule_dict


    def handle_ut_yamlless(self, slot_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:

        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]

        if not slot_data:
            return None

        self.is_ut_gen = True

        self.options.goal_unlock_condition.value = slot_data["GoalUnlockCondition"]
        self.options.goal_level_completions.value = slot_data["GoalLevelCompletions"]
        self.options.ability_unlocks.value = slot_data["AbilityUnlocks"]
        self.options.sonic_story.value = slot_data["SonicStory"]
        self.options.sonic_story_starting_character.value = slot_data["SonicStoryStartingCharacter"]
        self.options.sonic_key_sanity.value = slot_data["SonicKeySanity"]
        self.options.sonic_checkpoint_sanity.value = slot_data["SonicCheckpointSanity"]
        self.secret = slot_data["SecretLocations"]
        self.options.remove_casino_park_vip_table_laser_gate.value = \
            slot_data["RemoveCasinoParkVIPTableLaserGate"]
        self.options.death_link.value = slot_data["DeathLink"]

        return slot_data
