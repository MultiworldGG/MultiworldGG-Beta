
from typing import ClassVar, TextIO
import re

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region
from Options import OptionError
from worlds.AutoWorld import WebWorld, World

from .names import *
()
from .options import *
from .items import *
from .locations import *
from .regions import *


class SonicHeroesWeb(WebWorld):

    theme = "partyTime"
    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the Sonic Heroes randomizer connected to a MultiworldGG world.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["EthicalLogic"]
    )

    tutorials = [setup_en]
    option_groups = sonic_heroes_option_groups


class SonicHeroesWorld(World):
    """
    Sonic Heroes is a 2003 platform game developed by Sonic Team USA. The player races a team of series characters through levels to amass rings, 
    defeat robots, and collect the seven Chaos Emeralds needed to defeat Doctor Eggman. Within each level, the player switches between the team's three characters, 
    who each have unique abilities, to overcome obstacles.
    """
    game: str = "Sonic Heroes"
    
    author: str = AUTHOR
    web = SonicHeroesWeb()
    options_dataclass = SonicHeroesOptions
    options: SonicHeroesOptions

    item_name_to_id: ClassVar[dict[str, int]] = {item.itemName: item.code for item in itemList}  # noqa: F405
    location_name_to_id: ClassVar[dict[str, int]] = {v: k for k, v in location_id_name_dict.items()}  # noqa: F405

    topology_present = False


    def __init__(self, multiworld, player):

        self.location_name_to_region: dict[str, str] = {}
        """
        Dictionary to store location ids to region
        """
        self.default_emblem_pool_size: int = 0
        """
        Number of emblems for all stories and mission acts
        """
        self.emblem_pool_size = 0
        """
        Number of emblems in the itempool (including extra)
        """
        self.gate_emblem_costs = []
        """
        List of emblem costs for each gate boss
        """
        self.shuffleable_level_list: list[int] = []
        """
        List of levels that gets shuffled. Used by the client as well.
        """
        self.shuffleable_boss_list: list[int] = []
        """
        List of bosses/extras that gets shuffled. Used by the client as well.
        """
        self.story_list: list[str] = []
        """
        List of enabled Stories in order: ["Sonic", "Dark", "Rose", "Chaotix"]
        """
        self.required_emblems: int = 0
        """
        Number of required emblems for the final boss (can be 0)
        """
        self.gate_cost: int = 0
        """
        Cost for a gate boss (multiplied by the gate)
        As this is rounded down, the final boss can be different
        """
        self.gate_level_counts = []
        """
        Number of levels per gate: [4, 4, 3, 3]
        """
        self.placed_emeralds = []
        """
        List to ensure emeralds are only placed once
        """
        self.emerald_mission_numbers = [2, 4, 6, 8, 10, 12, 14]
        """
        List of Mission Numbers that contain an emerald bonus stage
        """
        self.spoiler_string = ""
        """
        String for printing to the spoiler log
        """
        self.excluded_sanity_locations = []
        """
        List of excluded sanity locations (by ID) for option SanityExcludedPercent
        """
        self.story_options = []
        """
        List of Story Options
        """
        self.key_sanity_options = []
        """
        List of Key Sanity Options
        """
        self.checkpoint_sanity_options = []
        """
        List of Checkpoint Sanity Options
        """
        self.key_sanity_key_amounts = [
            [
                3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
            ],
            [
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
            ],
            [
                2, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3
            ],
            [
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
            ]
        ]
        """
        List of the number of intended bonus keys in each level for each team (plus 1 hidden one)
        """
        self.checkpoint_amounts = [ #total 246
            [ #Sonic
                5, 4, 4, 4, 3, 4, 6, 4, 3, 5, 3, 4, 5, 3 #57
            ],
            [ #Dark
                4, 5, 4, 4, 3, 4, 6, 5, 3, 5, 3, 4, 5, 3 #58 not 50
            ],
            [ #Rose
                2, 2, 3, 2, 1, 3, 4, 2, 2, 3, 3, 2, 2, 2 #33
            ],
            [ #Chaotix
                4, 2, 4, 3, 3, 2, 5, 4, 3, 4, 2, 5, 4, 3 #48
            ],
            [ #SuperHard
                4, 5, 4, 4, 3, 4, 6, 4, 3, 5, 3, 5, 5, 3 #58
            ]
        ]
        """
        List of intended Checkpoints in each level (super hard is included)
        Sonic 57
        SuperHard 58
        Dark 58
        Rose 33
        Chaotix 48
        Total 254 
        
        
        Not Included:        
        Sonic: 4
        1 before start of level
        1 OOB
        2 mutually exclusive (right next to another, only 1 check)        
        
        SuperHard: 3
        1 before start of level
        1 OOB
        1 mutually exclusive (right next to another, only 1 check)
        
        Dark: 1
        1 mutually exclusive (right next to another, only 1 check)
        
        Rose: 20
        2 before start of level
        17 after goal
        1 at start position of level (lol)
        
        Chaotix: 5
        4 OOB
        1 does not exist (lol)     
        
        
        Total Excluded: 33
        4 before start of level
        17 after goal
        6 OOB
        4 mutually exclusive (right next to another, only 1 check)  
        1 at start position of level (lol)
        1 does not exist (lol)      
        
        
        Total of all:
        Sonic 57 + 4        61
        SuperHard 58 + 3    61
        Dark 58 + 1         59
        Rose 33 + 20        53
        Chaotix 48 + 5      53
        Total 254 + 33      287
        """

        super().__init__(multiworld, player)


    def generate_early(self) -> None:

        if self.options.super_hard_mode_sonic_act_2.value and self.options.sonic_story.value < 2:
            raise OptionError("[ERROR] Super Hard Mode Sonic Act 2 requires Sonic Act 2 to be enabled.")

        if (not self.options.super_hard_mode_sonic_act_2.value) and self.options.sonic_checkpoint_sanity.value == 2:
            raise OptionError("[ERROR] Super Hard Mode Checkpoint Sanity requires Sonic Super Hard.")

        if self.options.sonic_story == 2 and self.options.super_hard_mode_sonic_act_2.value and self.options.sonic_checkpoint_sanity.value == 1:
            raise OptionError("[ERROR] Only Sonic Normal Checkpoint Sanity cannot have only SuperHard Mode enabled.")


        self.story_options = \
            [
                self.options.sonic_story.value,
                self.options.dark_story.value,
                self.options.rose_story.value,
                self.options.chaotix_story.value,
            ]

        self.key_sanity_options = \
            [
                self.options.sonic_key_sanity.value,
                self.options.dark_key_sanity.value,
                self.options.rose_key_sanity.value,
                self.options.chaotix_key_sanity.value,
            ]
        self.checkpoint_sanity_options = \
            [
                self.options.sonic_checkpoint_sanity.value,
                self.options.dark_checkpoint_sanity.value,
                self.options.rose_checkpoint_sanity.value,
                self.options.chaotix_checkpoint_sanity.value,
            ]

        number_of_enabled_mission_blocks = 0
        max_allowed_emblems = 0
        if self.options.sonic_story.value > 0:
            if self.options.sonic_story.value == 1 or self.options.sonic_story.value == 3:
                number_of_enabled_mission_blocks += 1
            if self.options.sonic_story.value == 2 or self.options.sonic_story.value == 3:
                number_of_enabled_mission_blocks += 1
            self.story_list.append(sonic_heroes_story_names[0])

        if self.options.dark_story.value > 0:
            if self.options.dark_story.value == 1 or self.options.dark_story.value == 3:
                number_of_enabled_mission_blocks += 1
            if self.options.dark_story.value == 2 or self.options.dark_story.value == 3:
                number_of_enabled_mission_blocks += 1
                if self.options.dark_sanity.value > 0:
                    max_allowed_emblems += int(1400 / self.options.dark_sanity.value)
            self.story_list.append(sonic_heroes_story_names[1])


        if self.options.rose_story.value > 0:
            if self.options.rose_story.value == 1 or self.options.rose_story.value == 3:
                number_of_enabled_mission_blocks += 1
            if self.options.rose_story.value == 2 or self.options.rose_story.value == 3:
                number_of_enabled_mission_blocks += 1
                if self.options.rose_sanity.value > 0:
                    max_allowed_emblems += int(2800 / self.options.rose_sanity.value)
            self.story_list.append(sonic_heroes_story_names[2])

        if self.options.chaotix_story.value > 0:
            if self.options.chaotix_story.value == 1 or self.options.chaotix_story.value == 3:
                number_of_enabled_mission_blocks += 1
                if self.options.chaotix_sanity > 0:
                    max_allowed_emblems += 223 + int(200 / self.options.chaotix_sanity.value)
            if self.options.chaotix_story.value == 2 or self.options.chaotix_story.value == 3:
                number_of_enabled_mission_blocks += 1
                if self.options.chaotix_sanity > 0:
                    max_allowed_emblems += 266 + int(500 / self.options.chaotix_sanity.value)
            self.story_list.append(sonic_heroes_story_names[3])

        if len(self.story_list) < 1 or len(self.story_list) > 4:
            raise OptionError("[ERROR] Number of stories enabled is invalid.")

        if (self.options.stealth_trap_weight.value == 0 and
        self.options.freeze_trap_weight.value == 0 and
        self.options.no_swap_trap_weight.value == 0 and
        self.options.ring_trap_weight.value == 0 and
        self.options.charmy_trap_weight.value == 0):
            raise OptionError("[ERROR] The Trap Weights must not all be zero")

        self.emblem_pool_size = self.options.emblem_pool_size.value
        self.emblem_pool_size *= number_of_enabled_mission_blocks
        self.default_emblem_pool_size: int = self.emblem_pool_size

        #extra emblem math here
        max_allowed_emblems += self.emblem_pool_size
        if self.options.goal_unlock_condition.value == 1 and self.options.emerald_stage_location_type != 2:
            max_allowed_emblems += 7
        max_allowed_emblems += self.options.number_level_gates.value
        self.emblem_pool_size = min(self.emblem_pool_size, max_allowed_emblems)


        extra_itempool_space = (14 * number_of_enabled_mission_blocks) - self.emblem_pool_size

        if self.options.emerald_stage_location_type.value == 2:
            if max_allowed_emblems + extra_itempool_space - self.emblem_pool_size < 7:
                raise OptionError("[ERROR] Cannot set Emerald Stages to Excluded without enough space in the itempool")

        self.spoiler_string += f"THE EMBLEM POOL SIZE IS {self.emblem_pool_size}\n"

        self.required_emblems = math.floor(self.default_emblem_pool_size * self.options.required_emblems_percent.value / 100)


        self.gate_cost = math.floor(self.required_emblems / (self.options.number_level_gates.value + 1))

        for i in range(self.options.number_level_gates.value):
            self.gate_emblem_costs.append((i + 1) * self.gate_cost)

        self.gate_emblem_costs.append(self.required_emblems)

        for i in range(len(self.story_list)):
            for ii in range(14):
                self.shuffleable_level_list.append(14 * i + ii)

        for ii in range(7):
            self.shuffleable_boss_list.append(ii)



        #how to weight levels based on location counts
        shuffeable_test_list = []

        #sonic
        if self.options.sonic_story.value > 0:
            if self.options.sonic_story.value == 1:
                for i in range(14):
                    shuffeable_test_list.append([f"SA", i + 1, 1])
            elif self.options.sonic_story.value == 2:
                for i in range(14):
                    shuffeable_test_list.append([f"SB", i + 1, 1])
            else: #both acts enabled
                for i in range(14):
                    shuffeable_test_list.append([f"SC", i + 1, 2])

        #dark
        if self.options.dark_story.value > 0:
            if self.options.dark_story.value == 1:
                for i in range(14):
                    shuffeable_test_list.append([f"DA", i + 1, 1])
            elif self.options.dark_story.value == 2:
                for i in range(14):
                    shuffeable_test_list.append([f"DB", i + 1, 1])
            else:  # both acts enabled
                for i in range(14):
                    shuffeable_test_list.append([f"DC", i + 1, 2])

        #rose
        if self.options.rose_story.value > 0:
            if self.options.rose_story.value == 1:
                for i in range(14):
                    shuffeable_test_list.append([f"RA", i + 1, 1])
            elif self.options.rose_story.value == 2:
                for i in range(14):
                    shuffeable_test_list.append([f"RB", i + 1, 1])
            else:  # both acts enabled
                for i in range(14):
                    shuffeable_test_list.append([f"RC", i + 1, 2])

        #chaotix
        if self.options.chaotix_story.value > 0:
            if self.options.chaotix_story.value == 1:
                for i in range(14):
                    shuffeable_test_list.append([f"CA", i + 1, 1])
            elif self.options.chaotix_story.value == 2:
                for i in range(14):
                    shuffeable_test_list.append([f"CB", i + 1, 1])
            else:  # both acts enabled
                for i in range(14):
                    shuffeable_test_list.append([f"CC", i + 1, 2])


        #now shuffle
        self.random.shuffle(shuffeable_test_list)

        #shuffeable_test_list = [['DB', 1, 1], ['DB', 3, 1],['DB', 5, 1], ['DB', 7, 1],
         #['DB', 9, 1], ['DB', 11, 1],['DB', 13, 1], ['CC', 1, 2],
         #['CC', 2, 2], ['CC', 3, 2], ['CC', 4, 2], ['CC', 5, 2], ['CC', 6, 2], ['CC', 7, 2], ['CC', 8, 2], ['CC', 9, 2],
         #['CC', 10, 2], ['CC', 11, 2], ['CC', 12, 2], ['CC', 13, 2], ['CC', 14, 2], ['DB', 2, 1], ['DB', 4, 1], ['DB', 6, 1], ['DB', 8, 1], ['DB', 10, 1],  ['DB', 12, 1], ['DB', 14, 1]]





        placed_emeralds_test = [2, 4, 6, 8, 10, 12, 14]
        for entry in shuffeable_test_list:
            if entry[1] in placed_emeralds_test:
                if self.options.emerald_stage_location_type != 2:
                    entry[2] += 1
                placed_emeralds_test.remove(entry[1])

        test_levels_per_gate = []
        test_checks_per_gate = []
        test_level_list = []

        level_groups = self.options.number_level_gates + 1
        levels_per_gate = math.floor((len(self.story_list) * 14) / level_groups)
        total_levels = 14 * len(self.story_list)
        extra_levels = total_levels % level_groups

        shuffle_index = 0
        if self.options.number_level_gates > 0:
            for gate in range(self.options.number_level_gates.value + 1):
                extra_level_int = 0
                number_level_in_gate = 0
                number_check_in_gate = 0
                temp_int = 0
                if gate < extra_levels:
                    extra_level_int += 1
                while (number_check_in_gate < self.gate_emblem_costs[0] or number_level_in_gate < levels_per_gate + extra_level_int) and shuffle_index < len(shuffeable_test_list):
                    team = shuffeable_test_list[shuffle_index][0][:1]

                    for index in range(len(self.story_list)):
                        if team == self.story_list[index][0:1]:
                            temp_int = index
                            team = self.story_list[index]

                    temp_int = 14 * temp_int + shuffeable_test_list[shuffle_index][1] - 1
                    test_level_list.append(temp_int)
                    number_check_in_gate += shuffeable_test_list[shuffle_index][2]
                    number_level_in_gate += 1


                    if gate == self.options.number_level_gates.value:
                        number_check_in_gate -= shuffeable_test_list[shuffle_index][2]
                    shuffle_index += 1

                test_levels_per_gate.append(number_level_in_gate)
                test_checks_per_gate.append(number_check_in_gate)


        else:
            #do stuff here
            temp_int = 0
            for i in range(len(shuffeable_test_list)):
                team = shuffeable_test_list[i][0][:1]
                for index in range(len(self.story_list)):
                    if team == self.story_list[index][0:1]:
                        temp_int = index
                        team = self.story_list[index]
                temp_int = 14 * temp_int + shuffeable_test_list[i][1] - 1
                test_level_list.append(temp_int)
            #test_levels_per_gate.append(len(test_level_list))


        #print(f"Shuffle Test List: {shuffeable_test_list}")
        #print(f"test levels per gate: {test_levels_per_gate}")
        #print(f"test checks per gate: {test_checks_per_gate}")
        #print(f"Temp Level List: {test_level_list}")
        #print(f"Gate Emblem costs: {self.gate_emblem_costs}")


        self.shuffleable_level_list = test_level_list
        self.gate_level_counts = test_levels_per_gate



        self.random.shuffle(self.shuffleable_level_list)
        self.random.shuffle(self.shuffleable_boss_list)

        generate_locations(self)


    def create_regions(self):

        create_regions(self)

        victory_item = SonicHeroesItem("Victory", ItemClassification.progression, None, self.player)

        self.get_location("Victory Location").place_locked_item(victory_item)

        for i in range(self.options.number_level_gates.value):

            boss_gate_item = SonicHeroesItem(f"Boss Gate Item {i + 1}", ItemClassification.progression,
            None, self.player)    #0x93930009 + i + 1

            self.get_location(f"Boss Gate {i + 1}").place_locked_item(boss_gate_item)

        connect_entrances(self)



    def create_item(self, name: str) -> SonicHeroesItem:

        if name in junk_weights.keys():
            return SonicHeroesItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)

        return SonicHeroesItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)


    def create_items(self):
        create_items(self)


    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        if self.gate_cost > 0:
            self.multiworld.local_early_items[self.player]["Emblem"] = self.gate_cost


    def connect_entrances(self):
        #from Utils import visualize_regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])
        #!pragma layout smetana
        #put this at top to display PUML (after start UML)
        pass



    def write_spoiler_header(self, spoiler_handle: TextIO):

        self.spoiler_string += f"\nGate Costs is: {str(self.gate_emblem_costs)}\n"

        spoiler_handle.write(self.spoiler_string)


    def fill_slot_data(self):
        #s2-s15 sonic (Inclusive)
        #d2-d15 dark
        #r2-r15 rose
        #c2-c15 chaotix
        #b16-b22 bosses 23 is Madness
        templist = []
        for number in self.shuffleable_level_list:
            story = self.story_list[math.floor(number / 14)]
            templist.append(f'{story[:1].upper()}{(number % 14) + 2}')

        self.shuffleable_level_list = templist

        templist = []
        for number in self.shuffleable_boss_list:
            templist.append(f'B{number + 16}')

        #Truncate here to remove unneeded values
        templist = templist[0:self.options.number_level_gates.value]

        templist.append("B23")

        self.shuffleable_boss_list = templist

        return {
            "ModVersion": "1.4.0",
            "Goal": self.options.goal.value,
            "GoalUnlockCondition": self.options.goal_unlock_condition.value,
            "SkipMetalMadness": self.options.skip_metal_madness.value,
            "RequiredRank": self.options.required_rank.value,
            "DontLoseBonusKey": self.options.dont_lose_bonus_key.value,
            "SonicStory": self.options.sonic_story.value,
            "SuperHardModeSonicAct2": self.options.super_hard_mode_sonic_act_2.value,
            "SonicKeySanity": self.options.sonic_key_sanity.value,
            "SonicCheckpointSanity": self.options.sonic_checkpoint_sanity.value,
            "DarkStory": self.options.dark_story.value,
            "DarkSanity": self.options.dark_sanity.value,
            "DarkKeySanity": self.options.dark_key_sanity.value,
            "DarkCheckpointSanity": self.options.dark_checkpoint_sanity.value,
            "RoseStory": self.options.rose_story.value,
            "RoseSanity": self.options.rose_sanity.value,
            "RoseKeySanity": self.options.rose_key_sanity.value,
            "RoseCheckpointSanity": self.options.rose_checkpoint_sanity.value,
            "ChaotixStory": self.options.chaotix_story.value,
            "ChaotixSanity": self.options.chaotix_sanity.value,
            "ChaotixKeySanity": self.options.chaotix_key_sanity.value,
            "ChaotixCheckpointSanity": self.options.chaotix_checkpoint_sanity.value,
            "RingLink": self.options.ring_link.value,
            "RingLinkOverlord": self.options.ring_link_overlord.value,
            "ModernRingLoss": self.options.modern_ring_loss.value,
            "DeathLink": self.options.death_link.value,

            "GateEmblemCosts": self.gate_emblem_costs,
            "ShuffledLevels": self.shuffleable_level_list,
            "ShuffledBosses": self.shuffleable_boss_list,
            "GateLevelCounts": self.gate_level_counts,
        }




    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        new_hint_data = {}

        pattern = r"Gate (\d+)"
        for entrance in self.get_entrances():
            match = re.search(pattern, entrance.parent_region.name)
            if match:
                gate_number = int(match.group(1))
                for loc in entrance.connected_region.get_locations():
                    if loc.address is not None:
                        if loc.name == "Metal Overlord":
                            if self.options.goal_unlock_condition == 1: #Emblems only
                                new_hint_data[loc.address] = f"Final Boss after Gate {len(self.gate_emblem_costs) - 1}: Requires {self.gate_emblem_costs[-1]} Emblems"
                            elif self.options.goal_unlock_condition == 2: #Emeralds Only
                                if self.options.number_level_gates == 0:
                                    new_hint_data[loc.address] = f"Final Boss after Gate {len(self.gate_emblem_costs) - 1}: Requires the 7 Chaos Emeralds. Gate {len(self.gate_emblem_costs) - 1} is Available From Start"
                                else:
                                    new_hint_data[
                                        loc.address] = f"Final Boss after Gate {len(self.gate_emblem_costs) - 1}: Requires the 7 Chaos Emeralds. Gate {len(self.gate_emblem_costs) - 1} Requires {self.gate_emblem_costs[-2]} Emblems and {sonic_heroes_extra_names[self.shuffleable_boss_list[len(self.gate_emblem_costs) - 2]]}"
                            else: #Both
                                new_hint_data[loc.address] = f"Final Boss after Gate {len(self.gate_emblem_costs) - 1}: Requires {self.gate_emblem_costs[-1]} Emblems and the 7 Chaos Emeralds"

                        elif entrance.connected_region.name in sonic_heroes_extra_names.values():
                            new_hint_data[loc.address] = f"Gate {gate_number} Boss: Requires {self.gate_emblem_costs[gate_number]} Emblems and {sonic_heroes_extra_names[self.shuffleable_boss_list[gate_number]]}"
                            #self.spoiler_string += f"Adding Extended Hint Info for location: {loc.name} :::: Gate {gate_number} Boss: Requires {self.gate_emblem_costs[gate_number]} Emblems and {sonic_heroes_extra_names[self.shuffleable_boss_list[gate_number]]}\n"

                        else:
                            if gate_number == 0:
                                new_hint_data[loc.address] = f"Gate {gate_number}: Available from Start"
                                #self.spoiler_string += f"Adding Extended Hint Info for location: {loc.name} :::: Gate {gate_number}: Available from Start\n"
                            else:
                                new_hint_data[loc.address] = f"Gate {gate_number}: Requires {self.gate_emblem_costs[gate_number - 1]} Emblems and {sonic_heroes_extra_names[self.shuffleable_boss_list[gate_number - 1]]}"
                                #self.spoiler_string += f"Adding Extended Hint Info for location: {loc.name} :::: Gate {gate_number}: Requires {self.gate_emblem_costs[gate_number - 1]} Emblems and {sonic_heroes_extra_names[self.shuffleable_boss_list[gate_number - 1]]}\n"


        #for key, value in new_hint_data.items():
        #    self.spoiler_string += f"Hint for {location_id_name_dict[key]} is: {value}\n"
        #self.spoiler_string += f"\n\n"
        hint_data[self.player] = new_hint_data