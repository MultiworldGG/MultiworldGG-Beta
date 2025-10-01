from random import randint

from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import item_table, HP2Item, fairy_wings_table, gift_unique_table, girl_unlock_table, pair_unlock_table, \
    tokekn_lvup_table, gift_shoe_table, baggage_table, outfits_table, itemgen_to_name

from .Locations import location_table, HP2Location, locationgen_to_name
from .Options import HP2Options, starting_pairs, starting_girls
from .Rules import set_rules
from ..generic.Rules import  set_rule


class HuniePop2Web(WebWorld):
    rating: str = "nsfw"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Hunie Pop 2 randomizer connected to an MWGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["dotsofdarkness"]
    )]

class HuniePop2(World):
    """
    HuniePop 2: Double Date is a 2021 tile-matching and dating sim adult video game. The game follows the dating adventures of the main character 
    as they try to woo several different women in their home town; its characters are drawn in anime art style and they have a fully-voiced and animated dialog.
    """

    from BaseUtils import get_archipelago_json
    GAME_NAME, AUTHOR, AP_VERSION, WORLD_VERSION = get_archipelago_json("huniepop2")

    game = GAME_NAME
    author: str = AUTHOR
    igdb_id: int = IGDB_ID
    worldversion = "2.0.0"
    item_name_to_id = item_table
    item_id_to_name = {item_table[name]: name for name in item_table}
    item_name_groups = {
        "wings": fairy_wings_table,
        "girls": girl_unlock_table,
        "pairs": pair_unlock_table
    }

    options_dataclass = HP2Options
    options: HP2Options

    web = HuniePop2Web()
    startingpairs = []
    startinggirls = []
    shopslots = 0
    trashitems = 0
    wingval = 0

    totall = 0
    totali = 0



    location_name_to_id = location_table

    pair_order = (
        "(abia/lola)",
        "(lola/nora)",
        "(candace/nora)",
        "(ashley/polly)",
        "(ashley/lillian)",
        "(lillian/zoey)",
        "(lailani/sarah)",
        "(jessie/lailani)",
        "(brooke/jessie)",
        "(jessie/lola)",
        "(lola/zoey)",
        "(abia/jessie)",
        "(lailani/lillian)",
        "(abia/lillian)",
        "(sarah/zoey)",
        "(polly/zoey)",
        "(nora/sarah)",
        "(brooke/sarah)",
        "(candace/lailani)",
        "(abia/candace)",
        "(candace/polly)",
        "(ashley/nora)",
        "(ashley/brooke)",
        "(brooke/polly)"
    )
    girl_order = (
        "lola",
        "jessie",
        "lillian",
        "zoey",
        "sarah",
        "lailani",
        "candace",
        "nora",
        "brooke",
        "ashley",
        "abia",
        "polly"
    )

    girls_enabled = set()
    pairs_enabled = set()


    def generate_early(self):
        numpairs = self.options.number_of_starting_pairs.value
        numgirls = self.options.number_of_starting_girls.value

        self.startingpairs = []
        self.startinggirls = []

        self.girls_enabled = self.options.enabled_girls.value

        pair_girls = set()

        if "lola" in self.girls_enabled:
            if "abia" in self.girls_enabled:
                pair_girls.add(("(abia/lola)", "abia", "lola"))
            if "nora" in self.girls_enabled:
                pair_girls.add(("(lola/nora)", "lola", "nora"))
            if "jessie" in self.girls_enabled:
                pair_girls.add(("(jessie/lola)", "jessie", "lola"))
            if "zoey" in self.girls_enabled:
                pair_girls.add(("(lola/zoey)", "lola", "zoey"))
        if "jessie" in self.girls_enabled:
            if "lailani" in self.girls_enabled:
                pair_girls.add(("(jessie/lailani)", "jessie", "lailani"))
            if "brooke" in self.girls_enabled:
                pair_girls.add(("(brooke/jessie)", "brooke", "jessie"))
            #if "lola" in self.girls_enabled:
            #    pair_girls.add(("(jessie/lola)", "jessie", "lola"))
            if "abia" in self.girls_enabled:
                pair_girls.add(("(abia/jessie)", "abia", "jessie"))
        if "lillian" in self.girls_enabled:
            if "ashley" in self.girls_enabled:
                pair_girls.add(("(ashley/lillian)", "ashley", "lillian"))
            if "zoey" in self.girls_enabled:
                pair_girls.add(("(lillian/zoey)", "lillian", "zoey"))
            if "lailani" in self.girls_enabled:
                pair_girls.add(("(lailani/lillian)", "lailani", "lillian"))
            if "abia" in self.girls_enabled:
                pair_girls.add(("(abia/lillian)", "abia", "lillian"))
        if "zoey" in self.girls_enabled:
            #if "lillian" in self.girls_enabled:
            #    pair_girls.add(("(lillian/zoey)", "lillian", "zoey"))
            #if "lola" in self.girls_enabled:
            #    pair_girls.add(("(lola/zoey)", "lola", "zoey"))
            if "sarah" in self.girls_enabled:
                pair_girls.add(("(sarah/zoey)", "sarah", "zoey"))
            if "polly" in self.girls_enabled:
                pair_girls.add(("(polly/zoey)", "polly", "zoey"))
        if "sarah" in self.girls_enabled:
            if "lailani" in self.girls_enabled:
                pair_girls.add(("(lailani/sarah)", "lailani", "sarah"))
            #if "zoey" in self.girls_enabled:
            #    pair_girls.add(("(sarah/zoey)", "sarah", "zoey"))
            if "nora" in self.girls_enabled:
                pair_girls.add(("(nora/sarah)", "nora", "sarah"))
            if "brooke" in self.girls_enabled:
                pair_girls.add(("(brooke/sarah)", "brooke", "sarah"))
        if "lailani" in self.girls_enabled:
            #if "sarah" in self.girls_enabled:
            #    pair_girls.add(("(lailani/sarah)", "lailani", "sarah"))
            #if "jessie" in self.girls_enabled:
            #    pair_girls.add(("(jessie/lailani)", "jessie", "lailani"))
            #if "lillian" in self.girls_enabled:
            #    pair_girls.add(("(lailani/lillian)", "lailani", "lillian"))
            if "candace" in self.girls_enabled:
                pair_girls.add(("(candace/lailani)", "candace", "lailani"))
        if "candace" in self.girls_enabled:
            if "nora" in self.girls_enabled:
                pair_girls.add(("(candace/nora)", "candace", "nora"))
            #if "lailani" in self.girls_enabled:
            #    pair_girls.add(("(candace/lailani)", "candace", "lailani"))
            if "abia" in self.girls_enabled:
                pair_girls.add(("(abia/candace)", "abia", "candace"))
            if "polly" in self.girls_enabled:
                pair_girls.add(("(candace/polly)", "candace", "polly"))
        if "nora" in self.girls_enabled:
            #if "lola" in self.girls_enabled:
            #    pair_girls.add(("(lola/nora)", "lola", "nora"))
            #if "candace" in self.girls_enabled:
            #    pair_girls.add(("(candace/nora)", "candace", "nora"))
            #if "sarah" in self.girls_enabled:
            #    pair_girls.add(("(nora/sarah)", "nora", "sarah"))
            if "ashley" in self.girls_enabled:
                pair_girls.add(("(ashley/nora)", "ashley", "nora"))
        if "brooke" in self.girls_enabled:
            #if "jessie" in self.girls_enabled:
            #    pair_girls.add(("(brooke/jessie)", "brooke", "jessie"))
            #if "sarah" in self.girls_enabled:
            #    pair_girls.add(("(brooke/sarah)", "brooke", "sarah"))
            if "ashley" in self.girls_enabled:
                pair_girls.add(("(ashley/brooke)", "ashley", "brooke"))
            if "polly" in self.girls_enabled:
                pair_girls.add(("(brooke/polly)", "brooke", "polly"))
        if "ashley" in self.girls_enabled:
            if "polly" in self.girls_enabled:
                pair_girls.add(("(ashley/polly)", "ashley", "polly"))
            #if "lillian" in self.girls_enabled:
            #    pair_girls.add(("(ashley/lillian)", "ashley", "lillian"))
            #if "nora" in self.girls_enabled:
            #    pair_girls.add(("(ashley/nora)", "ashley", "nora"))
            #if "brooke" in self.girls_enabled:
            #    pair_girls.add(("(ashley/brooke)", "ashley", "brooke"))
        if "abia" in self.girls_enabled:
            hi=""
            #if "lola" in self.girls_enabled:
            #    pair_girls.add(("(abia/lola)", "abia", "lola"))
            #if "jessie" in self.girls_enabled:
            #    pair_girls.add(("(abia/jessie)", "abia", "jessie"))
            #if "lillian" in self.girls_enabled:
            #    pair_girls.add(("(abia/lillian)", "abia", "lillian"))
            #if "candace" in self.girls_enabled:
            #    pair_girls.add(("(abia/candace)", "abia", "candace"))
        if "polly" in self.girls_enabled:
            hi=""
            #if "ashley" in self.girls_enabled:
            #    pair_girls.add(("(ashley/polly)", "ashley", "polly"),)
            #if "zoey" in self.girls_enabled:
            #    pair_girls.add(("(polly/zoey)", "polly", "zoey"))
            #if "candace" in self.girls_enabled:
            #    pair_girls.add(("(candace/polly)", "candace", "polly"))
            #if "brooke" in self.girls_enabled:
            #    pair_girls.add(("(brooke/polly)", "brooke", "polly"))

        for pair in pair_girls:
            self.pairs_enabled.add(pair[0])

        if len(pair_girls) < self.options.boss_wings_requirement.value:
            print(f"ENABLED PAIRS LESS THAN BOSS WING REQUIREMENT SETTING VALUE TO MATCH NUMBER OF PAIRS:{len(pair_girls)}")
            self.options.boss_wings_requirement.value = len(pair_girls)

        self.wingval = self.options.boss_wings_requirement.value

        if len(self.pairs_enabled) != 24:
            self.options.boss_wings_requirement.value = min(24, (self.options.boss_wings_requirement.value + (24-len(self.pairs_enabled))))

        #get random number of pairs based on what's set in options
        temppairs = pair_girls.copy()
        tempgirl = []
        i=1
        while i<=numpairs:
            pair = temppairs.pop()
            self.startingpairs.append(f"Pair Unlock {pair[0]}")
            tempgirl.append(pair[1])
            tempgirl.append(pair[2])
            i+=1

        #add all the girls required for the starting pairs
        y = 0
        for g in tempgirl:
            xstr = f"Unlock Girl({g})"
            if not xstr in self.startinggirls:
                self.startinggirls.append(xstr)
                y += 1

        #add more starting girls if needed
        if y < numgirls:
            girllist = self.girls_enabled.copy()
            while y < numgirls:
                girl = girllist.pop()
                gstr = f"Unlock Girl({girl})"
                if not gstr in self.startinggirls:
                    self.startinggirls.append(gstr)
                    y += 1

                if len(girllist)<1:
                    break

        totallocations = 0
        totalitems = 0

        #get number of items that will in the itempool
        if not self.options.lovers_instead_wings.value: #fairy wings
            totalitems += len(self.pairs_enabled)
        if True: #tokenlvups
            totalitems += 32
        if True: #girl unlocks
            totalitems += len(self.girls_enabled) - len(self.startinggirls)
        if True: #pair unlocks
            totalitems += len(self.pairs_enabled) - len(self.startingpairs)
        if True: #gift unique
            totalitems += (len(self.girls_enabled) * 4)
        if True: #gift shoe
            totalitems += (len(self.girls_enabled) * 4)
        if not self.options.disable_baggage.value: #baggagage
            totalitems += (len(self.girls_enabled) * 3)
        if not self.options.disable_outfits.value:
            totalitems += (len(self.girls_enabled) * 9)

        #get the number of location that will be in the starting pool
        if True: #pair attracted/lovers
            totallocations += (len(self.pairs_enabled) * 2)
        if True: #unique gift
            totallocations += (len(self.girls_enabled) * 4)
        if True: #shoe gift
            totallocations += (len(self.girls_enabled) * 4)
        if self.options.enable_questions.value: #favroute question
            totallocations += (len(self.girls_enabled) * 20)
        if self.options.number_shop_items.value > 0: #shop locations
            totallocations += self.options.number_shop_items.value
        if not self.options.disable_outfits.value:
            totallocations += (len(self.girls_enabled) * 10)

        if totallocations != totalitems:
            if totallocations > totalitems:
                self.trashitems = totallocations-totalitems
                self.shopslots = self.options.number_shop_items.value
            else:
                self.shopslots = totalitems - (totallocations - self.options.number_shop_items.value)

        self.totall = totalitems + self.trashitems + 1
        self.totali = totalitems + self.trashitems + len(self.startinggirls) + len(self.startingpairs)
        self.options.number_shop_items.value = self.shopslots

    def create_regions(self):
        hub_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(hub_region)

        boss_region = Region("Boss Region", self.player, self.multiworld)
        boss_region.add_locations({"boss_location": 69420505}, HP2Location)
        hub_region.connect(boss_region, "hub-boss")

        #print(f"total shop slots:{self.shopslots}")
        if self.shopslots > 0:
            shop_region = Region("Shop Region", self.player, self.multiworld)
            hub_region.connect(shop_region, "hub-shop")
            for i in range(self.shopslots):
                #self.location_name_to_id[f"shop_location: {i+1}"] = 69420506+i
                shop_region.add_locations({f"shop_location: {i+1}" : 69420506+i}, HP2Location)

        for pair in self.pairs_enabled:
            pairregion = Region(f"{pair} Region", self.player, self.multiworld)
            pairregion.add_locations({
                f"Pair Attracted {pair}":self.location_name_to_id[f"Pair Attracted {pair}"],
                f"Pair Lovers {pair}":self.location_name_to_id[f"Pair Lovers {pair}"]
            }, HP2Location)
            hub_region.connect(pairregion, f"hub-pair{pair}")

        for girl in self.girls_enabled:
            girlregion = Region(f"{girl} Region", self.player, self.multiworld)
            if self.options.enable_questions:
                girlregion.add_locations({
                    f"{girl} favourite drink": self.location_name_to_id[f"{girl} favourite drink"],
                    f"{girl} favourite Ice Cream Flavor": self.location_name_to_id[f"{girl} favourite Ice Cream Flavor"],
                    f"{girl} favourite Music Genre": self.location_name_to_id[f"{girl} favourite Music Genre"],
                    f"{girl} favourite Movie Genre": self.location_name_to_id[f"{girl} favourite Movie Genre"],
                    f"{girl} favourite Online Activity": self.location_name_to_id[f"{girl} favourite Online Activity"],
                    f"{girl} favourite Phone App": self.location_name_to_id[f"{girl} favourite Phone App"],
                    f"{girl} favourite Type Of Exercise": self.location_name_to_id[f"{girl} favourite Type Of Exercise"],
                    f"{girl} favourite Outdoor Activity": self.location_name_to_id[f"{girl} favourite Outdoor Activity"],
                    f"{girl} favourite Theme Park Ride": self.location_name_to_id[f"{girl} favourite Theme Park Ride"],
                    f"{girl} favourite Friday Night": self.location_name_to_id[f"{girl} favourite Friday Night"],
                    f"{girl} favourite Sunday Morning": self.location_name_to_id[f"{girl} favourite Sunday Morning"],
                    f"{girl} favourite Weather": self.location_name_to_id[f"{girl} favourite Weather"],
                    f"{girl} favourite Holiday": self.location_name_to_id[f"{girl} favourite Holiday"],
                    f"{girl} favourite Pet": self.location_name_to_id[f"{girl} favourite Pet"],
                    f"{girl} favourite School Subject": self.location_name_to_id[f"{girl} favourite School Subject"],
                    f"{girl} favourite Place to shop": self.location_name_to_id[f"{girl} favourite Place to shop"],
                    f"{girl} favourite Trait In Partner": self.location_name_to_id[f"{girl} favourite Trait In Partner"],
                    f"{girl} favourite Own Body Part": self.location_name_to_id[f"{girl} favourite Own Body Part"],
                    f"{girl} favourite Sex Position": self.location_name_to_id[f"{girl} favourite Sex Position"],
                    f"{girl} favourite Porn Category": self.location_name_to_id[f"{girl} favourite Porn Category"]
                }, HP2Location)

            girlregion.add_locations({
                locationgen_to_name[f"{girl} unique gift 1"]: self.location_name_to_id[locationgen_to_name[f"{girl} unique gift 1"]],
                locationgen_to_name[f"{girl} unique gift 2"]: self.location_name_to_id[locationgen_to_name[f"{girl} unique gift 2"]],
                locationgen_to_name[f"{girl} unique gift 3"]: self.location_name_to_id[locationgen_to_name[f"{girl} unique gift 3"]],
                locationgen_to_name[f"{girl} unique gift 4"]: self.location_name_to_id[locationgen_to_name[f"{girl} unique gift 4"]],
                locationgen_to_name[f"{girl} shoe gift 1"]: self.location_name_to_id[locationgen_to_name[f"{girl} shoe gift 1"]],
                locationgen_to_name[f"{girl} shoe gift 2"]: self.location_name_to_id[locationgen_to_name[f"{girl} shoe gift 2"]],
                locationgen_to_name[f"{girl} shoe gift 3"]: self.location_name_to_id[locationgen_to_name[f"{girl} shoe gift 3"]],
                locationgen_to_name[f"{girl} shoe gift 4"]: self.location_name_to_id[locationgen_to_name[f"{girl} shoe gift 4"]]}, HP2Location)

            if not self.options.disable_outfits.value:
                girlregion.add_locations({
                    locationgen_to_name[f"{girl} outfit 1"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 1"]],
                    locationgen_to_name[f"{girl} outfit 2"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 2"]],
                    locationgen_to_name[f"{girl} outfit 3"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 3"]],
                    locationgen_to_name[f"{girl} outfit 4"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 4"]],
                    locationgen_to_name[f"{girl} outfit 5"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 5"]],
                    locationgen_to_name[f"{girl} outfit 6"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 6"]],
                    locationgen_to_name[f"{girl} outfit 7"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 7"]],
                    locationgen_to_name[f"{girl} outfit 8"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 8"]],
                    locationgen_to_name[f"{girl} outfit 9"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 9"]],
                    locationgen_to_name[f"{girl} outfit 10"]: self.location_name_to_id[locationgen_to_name[f"{girl} outfit 10"]]}, HP2Location)


            hub_region.connect(girlregion, f"hub-{girl}1")
            hub_region.connect(girlregion, f"hub-{girl}2")
            hub_region.connect(girlregion, f"hub-{girl}3")
            hub_region.connect(girlregion, f"hub-{girl}4")





    def create_item(self, name: str) -> HP2Item:
        if (name ==  "Victory"):
            return HP2Item(name, ItemClassification.progression, 69420346, self.player)
        if name in girl_unlock_table or name in pair_unlock_table or name in gift_unique_table or name in gift_shoe_table or name in fairy_wings_table or name in outfits_table:
            #print(f"{name}: is progression")
            return HP2Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        if name in tokekn_lvup_table:
            #print(f"{name}: is useful")
            return HP2Item(name, ItemClassification.useful, self.item_name_to_id[name], self.player)
        #print(f"{name}: is none")
        return HP2Item(name, ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_items(self):
        for pair in self.pairs_enabled:
            if f"Pair Unlock {pair}" in self.startingpairs:
                self.multiworld.push_precollected(self.create_item(f"Pair Unlock {pair}"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Pair Unlock {pair}"))

        for girl in self.girls_enabled:
            if f"Unlock Girl({girl})" in self.startinggirls:
                self.multiworld.push_precollected(self.create_item(f"Unlock Girl({girl})"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Unlock Girl({girl})"))

            if not self.options.disable_baggage.value:
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} baggage 1"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} baggage 2"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} baggage 3"]))

            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} shoe item 1"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} shoe item 2"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} shoe item 3"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} shoe item 4"]))

            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} unique item 1"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} unique item 2"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} unique item 3"]))
            self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} unique item 4"]))

            if not self.options.disable_outfits.value:
                if not(girl == "abia" or girl == "nora" or girl == "zoey"):
                    self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 1"]))
                if girl == "abia" or girl == "nora" or girl == "zoey" or girl == "polly":
                    self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 2"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 3"]))
                if girl != "polly":
                    self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 4"]))

                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 5"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 6"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 7"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 8"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 9"]))
                self.multiworld.itempool.append(self.create_item(itemgen_to_name[f"{girl} outfit item 10"]))



        if not self.options.lovers_instead_wings.value:
            for pair in self.pairs_enabled:
                self.multiworld.itempool.append(self.create_item(f"Fairy Wings {pair}"))

        if True:
            for token in tokekn_lvup_table:
                self.multiworld.itempool.append(self.create_item(token))


        #if self.trashitems > 0:
        #    for i in range(self.trashitems):
        #        self.multiworld.itempool.append(self.create_item("nothing"))




        if self.trashitems > 0:
            for i in range(self.trashitems):
                if self.options.filler_item.value == 1:
                    self.multiworld.itempool.append(self.create_item("nothing"))
                elif self.options.filler_item.value == 2:
                    self.multiworld.itempool.append(self.create_item("Fruit Seeds"))
                elif self.options.filler_item.value == 3:
                    i = randint(69420346,69420420)
                    self.multiworld.itempool.append(self.create_item(self.item_id_to_name[i]))



    def set_rules(self):

        self.multiworld.get_location("boss_location", self.player).place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        set_rules(self.multiworld, self.player, self.girls_enabled, self.pairs_enabled, self.startingpairs, self.options.enable_questions.value, self.options.disable_outfits.value)

        if self.shopslots > self.options.exclude_shop_items:
            for i in range(self.shopslots):
                if i>=self.options.exclude_shop_items:
                    self.multiworld.get_location(f"shop_location: {i+1}", self.player).progress_type = LocationProgressType.EXCLUDED

        if self.options.lovers_instead_wings.value:
            boss = set()
            for pair in self.pairs_enabled:
                boss.add(f"Pair Unlock {pair}")
            for girl in self.girls_enabled:
                boss.add(f"Unlock Girl({girl})")
            set_rule(self.multiworld.get_entrance("hub-boss", self.player), lambda state: state.has_all(boss, self.player))
        else:
            wings = set()
            for pair in self.pairs_enabled:
                wings.add(f"Fairy Wings {pair}")
            set_rule(self.multiworld.get_entrance("hub-boss", self.player), lambda state: state.has_from_list(wings, self.player, self.wingval))


        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def fill_slot_data(self) -> dict:
        returndict = {
            "number_blue_seed": self.options.number_blue_seed.value,
            "number_green_seed": self.options.number_green_seed.value,
            "number_orange_seed": self.options.number_orange_seed.value,
            "number_red_seed": self.options.number_red_seed.value,
            "number_shop_items": self.options.number_shop_items.value,
            "enable_questions": self.options.enable_questions.value,
            "disable_baggage": self.options.disable_baggage.value,
            "lovers_instead_wings": self.options.lovers_instead_wings.value,
            "affection_start": self.options.puzzle_goal_start.value,
            "affection_add": self.options.puzzle_goal_add.value,
            "boss_affection": self.options.puzzle_goal_boss.value,
            "start_moves": self.options.puzzle_moves.value,
            "hide_shop_item_details": self.options.hide_shop_item_details.value,
            "world_version": self.worldversion,
            "outfit_date_complete": self.options.outfits_require_date_completion.value,
            "boss_wing_requirement": self.options.boss_wings_requirement.value,
            "player_gender": self.options.player_gender.value,
            "polly_gender": self.options.polly_gender.value,
            "game_difficulty": self.options.game_difficulty.value,
            "total_items": self.totali,
            "total_locations": self.totall,
        }

        if "lola" in self.girls_enabled:
            returndict["lola"] = 0
        else:
            returndict["lola"] = 1

        if "jessie" in self.girls_enabled:
            returndict["jessie"] = 0
        else:
            returndict["jessie"] = 1

        if "lillian" in self.girls_enabled:
            returndict["lillian"] = 0
        else:
            returndict["lillian"] = 1

        if "zoey" in self.girls_enabled:
            returndict["zoey"] = 0
        else:
            returndict["zoey"] = 1

        if "sarah" in self.girls_enabled:
            returndict["sarah"] = 0
        else:
            returndict["sarah"] = 1

        if "lailani" in self.girls_enabled:
            returndict["lailani"] = 0
        else:
            returndict["lailani"] = 1

        if "candace" in self.girls_enabled:
            returndict["candace"] = 0
        else:
            returndict["candace"] = 1

        if "nora" in self.girls_enabled:
            returndict["nora"] = 0
        else:
            returndict["nora"] = 1

        if "brooke" in self.girls_enabled:
            returndict["brooke"] = 0
        else:
            returndict["brooke"] = 1

        if "ashley" in self.girls_enabled:
            returndict["ashley"] = 0
        else:
            returndict["ashley"] = 1

        if "abia" in self.girls_enabled:
            returndict["abia"] = 0
        else:
            returndict["abia"] = 1

        if "polly" in self.girls_enabled:
            returndict["polly"] = 0
        else:
            returndict["polly"] = 1



        return returndict