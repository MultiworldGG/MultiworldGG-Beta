from BaseClasses import Region

from ..base_classes import Q1Level


class e5m3(Q1Level):
    name = "The Dark Days"
    mapfile = "e5m3"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Secret (1)",
            "classname": "trigger_secret",
            "uuid": 10163080154079592946,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Yellow Armor (2)",
            "classname": "item_armor2",
            "uuid": 8920584253097214206,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Rockets (3)",
            "classname": "item_rockets",
            "uuid": 9423002277174667382,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Small Medkit (4)",
            "classname": "item_health",
            "uuid": 10094593276749180761,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Rockets (5)",
            "classname": "item_rockets",
            "uuid": 11807157160925591819,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Silver Key (6)",
            "classname": "item_key1",
            "uuid": 6214535259624553212,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Gold Key (7)",
            "classname": "item_key2",
            "uuid": 13253155051664547816,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Rockets (8)",
            "classname": "item_rockets",
            "uuid": 4874624421252739597,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Biosuit (9)",
            "classname": "item_artifact_envirosuit",
            "uuid": 5894134165403926971,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Supershotgun (10)",
            "classname": "weapon_supershotgun",
            "uuid": 12736354937092557944,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 10203813436210538099,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 9937009026566821997,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Secret (13)",
            "classname": "trigger_secret",
            "uuid": 16237100582923136517,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Megahealth (14)",
            "classname": "item_health",
            "uuid": 12297411878962379038,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 5602807497131676076,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Spikes (16)",
            "classname": "item_spikes",
            "uuid": 12916802837960848313,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 2018014649568954895,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Spikes (18)",
            "classname": "item_spikes",
            "uuid": 2042736443836099695,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Grenadelauncher (19)",
            "classname": "weapon_grenadelauncher",
            "uuid": 8160504849667330419,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Nailgun (20)",
            "classname": "weapon_nailgun",
            "uuid": 17772263444255843920,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Small Medkit (21)",
            "classname": "item_health",
            "uuid": 297178563520121433,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Red Armor (22)",
            "classname": "item_armorInv",
            "uuid": 17689917395976127950,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 13672361627769187872,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 6090358884046418376,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 1130477286155059160,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Secret (26)",
            "classname": "trigger_secret",
            "uuid": 5176525661562149401,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Spikes (27)",
            "classname": "item_spikes",
            "uuid": 12920189860744378868,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 2056350036394354336,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 5178058276572032739,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 820152058115471597,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 4005417737400199397,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Secret (32)",
            "classname": "trigger_secret",
            "uuid": 4221573761379403351,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 18008371679855036148,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 4015240050330003417,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 13042954282488501304,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 14790753607040049108,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Spikes (37)",
            "classname": "item_spikes",
            "uuid": 15174394593906066562,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Supernailgun (38)",
            "classname": "weapon_supernailgun",
            "uuid": 14280614784045799839,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 8221615369820658670,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 14918032117128146280,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Secret Exit",
            "classname": "trigger_changelevel",
            "uuid": 4983633995260535825,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "All Kills (42)",
            "classname": "all_kills",
            "uuid": 2159785634115119958,
            "mp": 0,
        },
    ]
    events = ["Silver Button", "Gold Button"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Shells (35)",
                "Small Medkit (4)",
                "Rockets (5)",
                "Grenadelauncher (19)",
                "Supershotgun (10)",
                "Rockets (3)",
                "Secret (1)",
                "Yellow Armor (2)",
            ],
        )
        self.restrict("Secret (1)", r.can_shootswitch)
        self.restrict("Yellow Armor (2)", r.can_shootswitch)

        past_silver_door_area = self.region(
            "Past Silver Door",
            ["Shells (34)", "Silver Button"],
        )
        self.connect(ret, past_silver_door_area, self.silver_key)
        self.restrict("Silver Button", r.can_button)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Gold Button",
            ],
        )
        self.connect(ret, past_gold_door_area, self.gold_key)
        self.restrict("Gold Button", r.can_button)

        dive_left_area = self.region(
            "Dive Left Area",
            [
                "Spikes (37)",
                "Spikes (36)",
                "Silver Key (6)",
                "Shells (30)",
                "Shells (31)",
                "Large Medkit (23)",
                "Red Armor (22)",
                "Secret (32)",
            ],
        )
        self.connect(ret, dive_left_area, r.can_dive & r.can_button)

        dive_front_area = self.region(
            "Dive Front Area",
            [
                "Large Medkit (15)",
                "Spikes (16)",
                "Supernailgun (38)",
                "Large Medkit (29)",
                "Large Medkit (28)",
                "Exit",
                "Secret Exit",
                "Shells (40)",
                "Spikes (18)",
                "Secret (39)",
                "All Kills (42)",
            ],
        )
        self.connect(ret, dive_front_area, r.can_dive & self.event("Gold Button"))

        self.restrict("Secret Exit", r.can_shootswitch & r.jump)
        self.restrict("Shells (40)", r.can_shootswitch)
        self.restrict("Spikes (18)", r.can_shootswitch)
        self.restrict("Secret (39)", r.can_shootswitch)

        self.restrict("All Kills (42)", r.difficult_combat)

        dive_right_area = self.region(
            "Dive Right Area",
            [
                "Shells (12)",
                "Shells (11)",
                "Nailgun (20)",
                "Spikes (24)",
                "Small Medkit (21)",
                "Biosuit (9)",
                "Rockets (8)",
                "Secret (13)",
                "Megahealth (14)",
                "Secret (26)",
                "Spikes (27)",
                "Large Medkit (25)",
                "Shells (33)",
                "Gold Key (7)",
            ],
        )
        self.connect(ret, dive_right_area, r.can_dive & self.event("Silver Button"))

        self.restrict("Small Medkit (21)", r.jump)
        self.restrict("Secret (26)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Spikes (27)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Large Medkit (25)", r.can_shootswitch | r.bigjump_hard)

        return ret
