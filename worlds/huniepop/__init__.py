import random

from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.huniepop.Items import HPItem, girl_unlock_table, item_table, panties_item_table, gift_item_table, \
    unique_item_table, girl_gift, progressive_token_item_table, itemgen_to_name
from worlds.huniepop.Locations import HPLocation, location_table, locationgen_to_name
from worlds.huniepop.Options import HPOptions
from worlds.huniepop.Rules import set_rules


class HuniePopWeb(WebWorld):
    rating: str = "nsfw"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Hunie Pop randomizer connected to an MWGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["dotsofdarkness"]
    )]


class HuniePop(World):
    """
    HuniePop is a unique sim experience around 8 girls.
    It's a gameplay first approach that's part dating sim, part puzzle game, with light RPG elements.
    """

    from BaseUtils import get_archipelago_json
    GAME_NAME, AUTHOR, AP_VERSION, WORLD_VERSION = get_archipelago_json("huniepop")

    game = GAME_NAME
    author: str = AUTHOR
    worldversion = {
        "major":1,
        "minor":1,
        "build":0
    }

    item_name_to_id = item_table
    item_id_to_name = {item_table[name]: name for name in item_table}
    location_name_to_id = location_table

    options_dataclass = HPOptions
    options: HPOptions

    web = HuniePopWeb()

    girllist = (
        "tiffany",
        "aiko",
        "kyanna",
        "audrey",
        "lola",
        "nikki",
        "jessie",
        "beli",
        "kyu",
        "momo",
        "celeste",
        "venus"
    )

    #giftsets = {
    #    "academy":0,
    #    "toys":0,
    #    "fitness":0,
    #    "rave":0,
    #    "sports":0,
    #    "artist":0,
    #    "baking":0,
    #    "yoga":0,
    #    "dancer":0,
    #    "aquarium":0,
    #    "scuba":0,
    #    "garden":0,
    #}

    startgirls = []
    startgirl = -1
    enabledgirls = []

    trashitems = 0
    shopslots = 0

    def generate_early(self):
        self.startgirls = []
        self.startgirl = -1

        if "kyu" not in self.options.enabled_girls.value and self.options.goal.value:
            self.options.enabled_girls.value.add("kyu")

        tmpgirls = list(self.options.enabled_girls.value.copy())
        #tmpgirls.add("kyu")
        self.enabledgirls = tmpgirls.copy()
        self.startgirls = random.sample(tmpgirls, self.options.number_of_starting_girls.value)
        self.startgirl = self.girllist.index(random.sample(self.startgirls, 1)[0])+1

        print(f"girls unlocked: {self.startgirls}")
        print(f"starting girl: {self.girllist[(self.startgirl-1)]}")



        totallocations = 0
        totalitems = 0

        #total locations
        if True: #date locations
            totallocations += (4*len(self.enabledgirls))
        if True: #pantie locations
            totallocations += len(self.enabledgirls)
        if True: #pantie turnin locations
            totallocations += len(self.enabledgirls)
        if True: #gift locations
            totallocations += (24*len(self.enabledgirls))
        if True: #question locations
            totallocations += (12*len(self.enabledgirls))
        if True: #shop locations
            totallocations += self.options.number_shop_items.value


        #total items
        if True: #girl unlock items
            totalitems += len(self.enabledgirls) - len(self.startgirls)
        if True: #pantie items
            totalitems += len(self.enabledgirls)
        if True: #gift items
            if "tiffany" in self.enabledgirls or "nikki" in self.enabledgirls or "celeste" in self.enabledgirls: totalitems +=6 #academy
            if "aiko" in self.enabledgirls or "audrey" in self.enabledgirls or "momo" in self.enabledgirls: totalitems +=6 #toys
            if "kyanna" in self.enabledgirls or "jessie" in self.enabledgirls or "celeste" in self.enabledgirls: totalitems +=6 #fitness
            if "tiffany" in self.enabledgirls or "audrey" in self.enabledgirls or "kyu" in self.enabledgirls: totalitems +=6 #rave
            if "lola" in self.enabledgirls or "beli" in self.enabledgirls or "momo" in self.enabledgirls: totalitems +=6 #sports
            if "aiko" in self.enabledgirls or "nikki" in self.enabledgirls or "kyu" in self.enabledgirls: totalitems +=6 #artist
            if "lola" in self.enabledgirls or "jessie" in self.enabledgirls or "venus" in self.enabledgirls: totalitems +=6 #baking
            if "kyanna" in self.enabledgirls or "beli" in self.enabledgirls or "venus" in self.enabledgirls: totalitems +=6 #yoga
            if "kyanna" in self.enabledgirls or "jessie" in self.enabledgirls or "kyu" in self.enabledgirls: totalitems +=6 #dancer
            if "audrey" in self.enabledgirls or "nikki" in self.enabledgirls or "momo" in self.enabledgirls: totalitems +=6 #aquarium
            if "tiffany" in self.enabledgirls or "lola" in self.enabledgirls or "celeste" in self.enabledgirls: totalitems +=6 #scuba
            if "aiko" in self.enabledgirls or "beli" in self.enabledgirls or "venus" in self.enabledgirls: totalitems +=6 #garden
        if True: #unique gift items
            totalitems += (len(self.enabledgirls) * 6)
        if True: #token items
            totalitems += (8*6)

        print(f"totalitems: {totalitems}")
        print(f"totallocations: {totallocations}")

        if totallocations != totalitems:
            if totallocations > totalitems:
                self.trashitems = totallocations-totalitems
                self.shopslots = self.options.number_shop_items.value
            else:
                self.shopslots = totalitems - (totallocations - self.options.number_shop_items.value)


    def create_regions(self):
        hub_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(hub_region)


        for girl in self.enabledgirls:
            girlregion = Region(f"{girl} Region", self.player, self.multiworld)

            girlregion.add_locations({
                f"{girl} date 1": self.location_name_to_id[f"{girl} date 1"],
                f"{girl} date 2": self.location_name_to_id[f"{girl} date 2"],
                f"{girl} date 3": self.location_name_to_id[f"{girl} date 3"],
                f"{girl} date 4": self.location_name_to_id[f"{girl} date 4"],
                f"received {girl}'s panties": self.location_name_to_id[f"received {girl}'s panties"],
                f"{girl}'s Last Name": self.location_name_to_id[f"{girl}'s Last Name"],
                f"{girl}'s Age": self.location_name_to_id[f"{girl}'s Age"],
                f"{girl}'s Height": self.location_name_to_id[f"{girl}'s Height"],
                f"{girl}'s Weight": self.location_name_to_id[f"{girl}'s Weight"],
                f"{girl}'s Occupation": self.location_name_to_id[f"{girl}'s Occupation"],
                f"{girl}'s Cup Size": self.location_name_to_id[f"{girl}'s Cup Size"],
                f"{girl}'s Birthday": self.location_name_to_id[f"{girl}'s Birthday"],
                f"{girl}'s Hobby": self.location_name_to_id[f"{girl}'s Hobby"],
                f"{girl}'s Favourite Color": self.location_name_to_id[f"{girl}'s Favourite Color"],
                f"{girl}'s Favourite Season": self.location_name_to_id[f"{girl}'s Favourite Season"],
                f"{girl}'s Favourite Hangout": self.location_name_to_id[f"{girl}'s Favourite Hangout"],
                locationgen_to_name[f"{girl} gift location 1"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 1"]],
                locationgen_to_name[f"{girl} gift location 2"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 2"]],
                locationgen_to_name[f"{girl} gift location 3"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 3"]],
                locationgen_to_name[f"{girl} gift location 4"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 4"]],
                locationgen_to_name[f"{girl} gift location 5"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 5"]],
                locationgen_to_name[f"{girl} gift location 6"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 6"]],
                locationgen_to_name[f"{girl} gift location 7"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 7"]],
                locationgen_to_name[f"{girl} gift location 8"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 8"]],
                locationgen_to_name[f"{girl} gift location 9"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 9"]],
                locationgen_to_name[f"{girl} gift location 10"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 10"]],
                locationgen_to_name[f"{girl} gift location 11"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 11"]],
                locationgen_to_name[f"{girl} gift location 12"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 12"]],
                locationgen_to_name[f"{girl} gift location 13"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 13"]],
                locationgen_to_name[f"{girl} gift location 14"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 14"]],
                locationgen_to_name[f"{girl} gift location 15"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 15"]],
                locationgen_to_name[f"{girl} gift location 16"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 16"]],
                locationgen_to_name[f"{girl} gift location 17"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 17"]],
                locationgen_to_name[f"{girl} gift location 18"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 18"]],
                locationgen_to_name[f"{girl} gift location 19"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 19"]],
                locationgen_to_name[f"{girl} gift location 20"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 20"]],
                locationgen_to_name[f"{girl} gift location 21"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 21"]],
                locationgen_to_name[f"{girl} gift location 22"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 22"]],
                locationgen_to_name[f"{girl} gift location 23"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 23"]],
                locationgen_to_name[f"{girl} gift location 24"]: self.location_name_to_id[locationgen_to_name[f"{girl} gift location 24"]]
            }, HPLocation)

            if girl == "kyu" or girl == "momo" or girl == "celeste" or girl == "venus":
                girlregion.add_locations({f"{girl}'s Homeworld": self.location_name_to_id[f"{girl}'s Homeworld"]}, HPLocation)
            else:
                girlregion.add_locations({f"{girl}'s Education": self.location_name_to_id[f"{girl}'s Education"]}, HPLocation)

            if girl == "kyu":
                if "tiffany" in self.enabledgirls:
                    girlregion.add_locations({"given kyu tiffany's panties": self.location_name_to_id["given kyu tiffany's panties"]}, HPLocation)
                if "aiko" in self.enabledgirls:
                    girlregion.add_locations({"given kyu aiko's panties": self.location_name_to_id["given kyu aiko's panties"]}, HPLocation)
                if "kyanna" in self.enabledgirls:
                    girlregion.add_locations({"given kyu kyanna's panties": self.location_name_to_id["given kyu kyanna's panties"]}, HPLocation)
                if "audrey" in self.enabledgirls:
                    girlregion.add_locations({"given kyu audrey's panties": self.location_name_to_id["given kyu audrey's panties"]}, HPLocation)
                if "lola" in self.enabledgirls:
                    girlregion.add_locations({"given kyu lola's panties": self.location_name_to_id["given kyu lola's panties"]}, HPLocation)
                if "nikki" in self.enabledgirls:
                    girlregion.add_locations({"given kyu nikki's panties": self.location_name_to_id["given kyu nikki's panties"]}, HPLocation)
                if "jessie" in self.enabledgirls:
                    girlregion.add_locations({"given kyu jessie's panties": self.location_name_to_id["given kyu jessie's panties"]}, HPLocation)
                if "beli" in self.enabledgirls:
                    girlregion.add_locations({"given kyu beli's panties": self.location_name_to_id["given kyu beli's panties"]}, HPLocation)
                if "kyu" in self.enabledgirls:
                    girlregion.add_locations({"given kyu kyu's panties": self.location_name_to_id["given kyu kyu's panties"]}, HPLocation)
                if "momo" in self.enabledgirls:
                    girlregion.add_locations({"given kyu momo's panties": self.location_name_to_id["given kyu momo's panties"]}, HPLocation)
                if "celeste" in self.enabledgirls:
                    girlregion.add_locations({"given kyu celeste's panties": self.location_name_to_id["given kyu celeste's panties"]}, HPLocation)
                if "venus" in self.enabledgirls:
                    girlregion.add_locations({"given kyu venus's panties": self.location_name_to_id["given kyu venus's panties"]}, HPLocation)

            hub_region.connect(girlregion, f"hub-{girl}")

        bossregion = Region("boss", self.player, self.multiworld)
        bossregion.add_locations({"boss": self.location_name_to_id["boss"]}, HPLocation)
        hub_region.connect(bossregion, "hub-boss")

        if self.shopslots > 0:
            shop_region = Region("shop", self.player, self.multiworld)
            for i in range(self.shopslots):
                #self.location_name_to_id[f"shop_location: {i+1}"] = 69420506+i
                shop_region.add_locations({f"shop_location: {i+1}" : 42069511+i}, HPLocation)
            hub_region.connect(shop_region, "hub-shop")




    def create_item(self, name: str) -> HPItem:
        if (name ==  "victory"):
            return HPItem(name, ItemClassification.progression, 42069999, self.player)
        if name in girl_unlock_table or name in panties_item_table or name in girl_unlock_table or name in gift_item_table or name in unique_item_table:
            return HPItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        if name in progressive_token_item_table:
            return HPItem(name, ItemClassification.useful, self.item_name_to_id[name], self.player)

        return HPItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)



    def create_items(self):
        for girl in self.enabledgirls:
            if girl in self.startgirls:
                self.multiworld.push_precollected(self.create_item(f"Unlock Girl({girl})"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Unlock Girl({girl})"))
            self.multiworld.itempool.append((self.create_item(f"{girl}'s panties")))

            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name[f"{girl} unique item 6"])))

        if "tiffany" in self.enabledgirls or "nikki" in self.enabledgirls or "celeste" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["academy gift item 6"])))
        if "aiko" in self.enabledgirls or "audrey" in self.enabledgirls or "momo" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["toys gift item 6"])))
        if "kyanna" in self.enabledgirls or "jessie" in self.enabledgirls or "celeste" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["fitness gift item 6"])))
        if "tiffany" in self.enabledgirls or "audrey" in self.enabledgirls or "kyu" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["rave gift item 6"])))
        if "lola" in self.enabledgirls or "beli" in self.enabledgirls or "momo" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["sports gift item 6"])))
        if "aiko" in self.enabledgirls or "nikki" in self.enabledgirls or "kyu" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["artist gift item 6"])))
        if "lola" in self.enabledgirls or "jessie" in self.enabledgirls or "venus" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["baking gift item 6"])))
        if "kyanna" in self.enabledgirls or "beli" in self.enabledgirls or "venus" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["yoga gift item 6"])))
        if "kyanna" in self.enabledgirls or "jessie" in self.enabledgirls or "kyu" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["dancer gift item 6"])))
        if "audrey" in self.enabledgirls or "nikki" in self.enabledgirls or "momo" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["aquarium gift item 6"])))
        if "tiffany" in self.enabledgirls or "lola" in self.enabledgirls or "celeste" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["scuba gift item 6"])))
        if "aiko" in self.enabledgirls or "beli" in self.enabledgirls or "venus" in self.enabledgirls:
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 1"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 2"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 3"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 4"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 5"])))
            self.multiworld.itempool.append((self.create_item(itemgen_to_name["garden gift item 6"])))

        for t in progressive_token_item_table:
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))


        if self.trashitems > 0:
            if self.options.filler_item.value == 1:
                for i in range(self.trashitems):
                    self.multiworld.itempool.append(self.create_item("nothing"))
            else:
                for i in range(self.trashitems):
                    r = random.randint(42069177, 42069260)
                    self.multiworld.itempool.append(self.create_item(self.item_id_to_name[r]))


    def set_rules(self):
        self.multiworld.get_location("boss", self.player).place_locked_item(self.create_item("victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("victory", self.player)

        set_rules(self.multiworld, self.player, self.enabledgirls, self.startgirls, self.options.goal.value)

        if self.shopslots > self.options.exclude_shop_items:
            for i in range(self.shopslots):
                if i>=self.options.exclude_shop_items:
                    self.multiworld.get_location(f"shop_location: {i + 1}", self.player).progress_type = LocationProgressType.EXCLUDED


    def fill_slot_data(self) -> dict:
        returndict = {
            "start_girl": self.startgirl,
            "number_of_shop_items": self.shopslots,
            "shop_item_cost": self.options.shop_item_cost.value,
            "shop_gift_cost": self.options.shop_gift_cost.value,
            "hunie_gift_cost": self.options.hunie_gift_cost.value,
            "puzzle_moves": self.options.puzzle_moves.value,
            "puzzle_affection_base": self.options.puzzle_affection_base.value,
            "puzzle_affection_add": self.options.puzzle_affection_add.value,
            "world_version": self.worldversion,
            "goal": self.options.goal.value
        }

        if "tiffany" in self.options.enabled_girls:
            returndict["tiffany_enabled"] = 1
        else:
            returndict["tiffany_enabled"] = 0

        if "aiko" in self.options.enabled_girls:
            returndict["aiko_enabled"] = 1
        else:
            returndict["aiko_enabled"] = 0

        if "kyanna" in self.options.enabled_girls:
            returndict["kyanna_enabled"] = 1
        else:
            returndict["kyanna_enabled"] = 0

        if "audrey" in self.options.enabled_girls:
            returndict["audrey_enabled"] = 1
        else:
            returndict["audrey_enabled"] = 0

        if "lola" in self.options.enabled_girls:
            returndict["lola_enabled"] = 1
        else:
            returndict["lola_enabled"] = 0

        if "nikki" in self.options.enabled_girls:
            returndict["nikki_enabled"] = 1
        else:
            returndict["nikki_enabled"] = 0

        if "jessie" in self.options.enabled_girls:
            returndict["jessie_enabled"] = 1
        else:
            returndict["jessie_enabled"] = 0

        if "beli" in self.options.enabled_girls:
            returndict["beli_enabled"] = 1
        else:
            returndict["beli_enabled"] = 0

        if "kyu" in self.options.enabled_girls:
            returndict["kyu_enabled"] = 1
        else:
            returndict["kyu_enabled"] = 0

        if "momo" in self.options.enabled_girls:
            returndict["momo_enabled"] = 1
        else:
            returndict["momo_enabled"] = 0

        if "celeste" in self.options.enabled_girls:
            returndict["celeste_enabled"] = 1
        else:
            returndict["celeste_enabled"] = 0

        if "venus" in self.options.enabled_girls:
            returndict["venus_enabled"] = 1
        else:
            returndict["venus_enabled"] = 0

        return returndict