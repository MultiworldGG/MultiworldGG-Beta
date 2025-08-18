from BaseClasses import Region

from ..base_classes import Q1Level


class hip1m5(Q1Level):
    name = "Military Complex"
    mapfile = "hip1m5"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Megahealth (1)",
            "classname": "item_health",
            "uuid": 8561936030751665949,
            "mp": 1,
        },
        {
            "id": 2,
            "name": "Rockets (2)",
            "classname": "item_rockets",
            "uuid": 17267767740827252834,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Spikes (3)",
            "classname": "item_spikes",
            "uuid": 4461980848280883421,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 17479272044546905738,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Large Medkit (5)",
            "classname": "item_health",
            "uuid": 4774232969061603436,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Nailgun (6)",
            "classname": "weapon_nailgun",
            "uuid": 10724142504793094032,
            "mp": 1,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 7139320224878136051,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Shells (8)",
            "classname": "item_shells",
            "uuid": 2993354235290322151,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Supershotgun (9)",
            "classname": "weapon_supershotgun",
            "uuid": 16184725138431608978,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Large Medkit (10)",
            "classname": "item_health",
            "uuid": 18184812995802211941,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 4268012313851259343,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 15707403569874785445,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Cells (13)",
            "classname": "item_cells",
            "uuid": 12858390285078829943,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Cells (14)",
            "classname": "item_cells",
            "uuid": 17650041700703041639,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Invulnerability (15)",
            "classname": "item_artifact_invulnerability",
            "uuid": 10981522651420688569,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 15671585312873425129,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Lightning (17)",
            "classname": "weapon_lightning",
            "uuid": 4378149043403554029,
            "mp": 1,
        },
        {
            "id": 18,
            "name": "Grenadelauncher (18)",
            "classname": "weapon_grenadelauncher",
            "uuid": 8636603385391855066,
            "mp": 1,
        },
        {
            "id": 19,
            "name": "Rockets (19)",
            "classname": "item_rockets",
            "uuid": 10093273574178083292,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rockets (20)",
            "classname": "item_rockets",
            "uuid": 17546514409019542813,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Supershotgun (21)",
            "classname": "weapon_supershotgun",
            "uuid": 5897562795767712634,
            "mp": 1,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 1125329554353302321,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 11982587061451408637,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Wetsuit (24)",
            "classname": "item_artifact_wetsuit",
            "uuid": 11616648038390252060,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 7622982210963466160,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Mjolnir (26)",
            "classname": "weapon_mjolnir",
            "uuid": 10584441124049742223,
            "mp": 1,
        },
        {
            "id": 27,
            "name": "Small Medkit (27)",
            "classname": "item_health",
            "uuid": 9928924712047703215,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Small Medkit (28)",
            "classname": "item_health",
            "uuid": 14574279014784683129,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Yellow Armor (29)",
            "classname": "item_armor2",
            "uuid": 8982007166836521103,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 7942092681561351234,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 5465217367894795462,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 6313273210983991849,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 11692729674758869145,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Spikes (34)",
            "classname": "item_spikes",
            "uuid": 10176357081434314473,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Spikes (35)",
            "classname": "item_spikes",
            "uuid": 5454051360459634308,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Laser (36)",
            "classname": "weapon_laser_gun",
            "uuid": 689920756215599029,
            "mp": 1,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 13934837369767561974,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 259538122897545806,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 12489189277378253145,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Spikes (40)",
            "classname": "item_spikes",
            "uuid": 14346171996900119508,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Megahealth (41)",
            "classname": "item_health",
            "uuid": 1883942906451889367,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Nailgun (42)",
            "classname": "weapon_nailgun",
            "uuid": 13542733088212293304,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Supershotgun (43)",
            "classname": "weapon_supershotgun",
            "uuid": 18066635585733493123,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Secret (44)",
            "classname": "trigger_secret",
            "uuid": 10222819717484825339,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Quad Damage (45)",
            "classname": "item_artifact_super_damage",
            "uuid": 2425863265666921373,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Shells (46)",
            "classname": "item_shells",
            "uuid": 6258425072925996419,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 5003794320051686813,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 13788916446146448440,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Supernailgun (49)",
            "classname": "weapon_supernailgun",
            "uuid": 16672557766337773988,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Large Medkit (50)",
            "classname": "item_health",
            "uuid": 5133000545291405416,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Gold Key (51)",
            "classname": "item_key2",
            "uuid": 8246275663018757333,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Invisibility (52)",
            "classname": "item_artifact_invisibility",
            "uuid": 93732283235883422,
            "mp": 1,
        },
        {
            "id": 53,
            "name": "Secret (53)",
            "classname": "trigger_secret",
            "uuid": 12944809647667693742,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Megahealth (54)",
            "classname": "item_health",
            "uuid": 13546991218107250329,
            "mp": 1,
        },
        {
            "id": 55,
            "name": "Small Medkit (55)",
            "classname": "item_health",
            "uuid": 9083530676390455613,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Small Medkit (56)",
            "classname": "item_health",
            "uuid": 15400450905213388417,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Rockets (57)",
            "classname": "item_rockets",
            "uuid": 8110718133589763231,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Rockets (58)",
            "classname": "item_rockets",
            "uuid": 7540138122616526597,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Spikes (59)",
            "classname": "item_spikes",
            "uuid": 8020195760966682362,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Secret (60)",
            "classname": "trigger_secret",
            "uuid": 13541844755026705189,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Red Armor (61)",
            "classname": "item_armorInv",
            "uuid": 4657199978904677845,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Rocketlauncher (62)",
            "classname": "weapon_rocketlauncher",
            "uuid": 16448712366283217776,
            "mp": 1,
        },
        {
            "id": 63,
            "name": "Megahealth (63)",
            "classname": "item_health",
            "uuid": 16553374211000987597,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Silver Key (64)",
            "classname": "item_key1",
            "uuid": 17192612053662288720,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Supernailgun (65)",
            "classname": "weapon_supernailgun",
            "uuid": 11530213748893963092,
            "mp": 1,
        },
        {
            "id": 66,
            "name": "Rocketlauncher (66)",
            "classname": "weapon_rocketlauncher",
            "uuid": 13615502129910445863,
            "mp": 1,
        },
        {
            "id": 67,
            "name": "Secret (67)",
            "classname": "trigger_secret",
            "uuid": 11516486818228836902,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Rockets (68)",
            "classname": "item_rockets",
            "uuid": 7751000089230052234,
            "mp": 1,
        },
        {
            "id": 69,
            "name": "Rockets (69)",
            "classname": "item_rockets",
            "uuid": 8800411087817923983,
            "mp": 1,
        },
        {
            "id": 70,
            "name": "Rockets (70)",
            "classname": "item_rockets",
            "uuid": 14946923644504370609,
            "mp": 1,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 8071206372993829047,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Spikes (72)",
            "classname": "item_spikes",
            "uuid": 10283642301979582969,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Spikes (73)",
            "classname": "item_spikes",
            "uuid": 17991530160893703315,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 7004337804787559459,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Shells (75)",
            "classname": "item_shells",
            "uuid": 1178058805345639093,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Shells (76)",
            "classname": "item_shells",
            "uuid": 16510545493905011593,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Shells (77)",
            "classname": "item_shells",
            "uuid": 13999149723004660313,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Secret (78)",
            "classname": "trigger_secret",
            "uuid": 976507369871298295,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Quad Damage (79)",
            "classname": "item_artifact_super_damage",
            "uuid": 18303104812819662115,
            "mp": 1,
        },
        {
            "id": 80,
            "name": "Megahealth (80)",
            "classname": "item_health",
            "uuid": 6514910080828751123,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Secret (81)",
            "classname": "trigger_secret",
            "uuid": 15271364101119034321,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Yellow Armor (82)",
            "classname": "item_armor2",
            "uuid": 13499079583998609776,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Grenadelauncher (83)",
            "classname": "weapon_grenadelauncher",
            "uuid": 4550037855892293357,
            "mp": 1,
        },
        {
            "id": 84,
            "name": "Rockets (84)",
            "classname": "item_rockets",
            "uuid": 6767216257761524328,
            "mp": 1,
        },
        {
            "id": 85,
            "name": "Rockets (85)",
            "classname": "item_rockets",
            "uuid": 6549821227692463451,
            "mp": 1,
        },
        {
            "id": 86,
            "name": "Rockets (86)",
            "classname": "item_rockets",
            "uuid": 2247330164033318793,
            "mp": 1,
        },
        {
            "id": 87,
            "name": "Red Armor (87)",
            "classname": "item_armorInv",
            "uuid": 12626150349006345355,
            "mp": 1,
        },
        {
            "id": 88,
            "name": "Secret (88)",
            "classname": "trigger_secret",
            "uuid": 17201617767210800917,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Large Medkit (89)",
            "classname": "item_health",
            "uuid": 853804424200687968,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Small Medkit (90)",
            "classname": "item_health",
            "uuid": 7108840988559687311,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Small Medkit (91)",
            "classname": "item_health",
            "uuid": 9913840810372272144,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Large Medkit (92)",
            "classname": "item_health",
            "uuid": 14846003156887039050,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Large Medkit (93)",
            "classname": "item_health",
            "uuid": 2545149300190835161,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Large Medkit (94)",
            "classname": "item_health",
            "uuid": 15017447792373548448,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Large Medkit (95)",
            "classname": "item_health",
            "uuid": 8490694592190884024,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "All Kills (96)",
            "classname": "all_kills",
            "uuid": 4313451559484177453,
            "mp": 0,
        },
    ]
    events = [
        "Hit Button 1",
        "Hit Button 2",
        "Hit Button 3",
        "Underwater Barrier Open",
        "Sewage System Open",
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (43)",
                "Grenadelauncher (83)",
                "Quad Damage (79)",
                "Megahealth (80)",
                "Secret (81)",
            ],
        )
        self.restrict("Grenadelauncher (83)", r.can_dive | r.can_shootswitch)
        self.restrict("Quad Damage (79)", r.can_shootswitch)
        self.restrict("Megahealth (80)", r.can_shootswitch)
        self.restrict("Secret (81)", r.can_shootswitch)

        start_secret = self.region(
            "Start Secret",
            [
                "Secret (53)",
                "Supernailgun (49)",
                "Megahealth (54)",
            ],
        )
        self.connect(
            ret,
            start_secret,
            r.can_gj_extr
            | r.can_rj_hard
            | (r.can_jump & r.difficulty("hard"))
            | r.bigjump,
        )

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (11)",
                "Large Medkit (12)",
                "Large Medkit (10)",
                "Large Medkit (7)",
                "Supershotgun (9)",
                "Shells (8)",
                "Spikes (3)",
                "Megahealth (1)",
                "Rockets (2)",
                "Large Medkit (5)",
                "Nailgun (6)",
                "Large Medkit (4)",
                "Exit",
            ],
        )
        self.connect(ret, past_gold_door_area, self.gold_key)
        self.restrict("All Kills (96)", r.backpack(5) & ())

        dive_area = self.region(
            "Dive Area",
            [
                "Large Medkit (50)",
                "Large Medkit (71)",
                "Nailgun (42)",
                "Shells (77)",
                "Shells (75)",
                "Shells (76)",
                "Hit Button 1",
                "Hit Button 2",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)
        self.restrict("Hit Button 1", r.can_button)
        self.restrict("Hit Button 2", r.can_button)

        tower_secret_area = self.region(
            "Tower Secret",
            [
                "Secret (78)",
                "Megahealth (41)",
                "Rocketlauncher (66)",
            ],
        )
        self.connect(dive_area, tower_secret_area, r.bigjump | r.can_shootswitch)

        past_bridge_area = self.region(
            "Past Bridge",
            [
                "Secret (67)",
                "Rockets (69)",
                "Rockets (70)",
                "Spikes (74)",
                "Spikes (73)",
                "Rockets (68)",
                "Spikes (72)",
            ],
        )
        self.connect(dive_area, past_bridge_area, r.jump)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Large Medkit (32)",
                "Large Medkit (31)",
                "Grenadelauncher (18)",
                "Shells (30)",
                "Hit Button 3",
            ],
        )
        self.restrict("Hit Button 3", r.can_button)
        self.connect(dive_area, past_door_area, r.can_door)
        self.connect(
            ret, past_door_area, (r.bigjump | r.can_gj_hard) & r.difficulty("hard")
        )
        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Shells (46)",
                "Large Medkit (48)",
                "Supernailgun (65)",
                "Large Medkit (47)",
                "Rockets (84)",
                "Rockets (85)",
                "Rockets (86)",
                "Small Medkit (55)",
                "Small Medkit (56)",
                "Large Medkit (23)",
                "Large Medkit (22)",
                "Supershotgun (21)",
                "Secret (88)",
                "Yellow Armor (82)",
                "Red Armor (87)",
            ],
        )
        self.connect(past_door_area, past_silver_door_area, self.silver_key)
        self.connect(ret, past_silver_door_area, r.bigjump_hard)
        self.restrict("Secret (88)", r.can_shootswitch)
        self.restrict("Yellow Armor (82)", r.can_shootswitch)
        self.restrict("Red Armor (87)", r.can_shootswitch)

        silver_past_door_area = self.region(
            "Silver Past Door Area",
            ["Wetsuit (24)", "Rockets (19)", "Rockets (20)", "Underwater Barrier Open"],
        )
        self.connect(past_silver_door_area, silver_past_door_area, r.can_door)
        self.restrict("Underwater Barrier Open", r.can_button)

        silver_dive_area = self.region(
            "Silver Dive Area",
            [
                "Lightning (17)",
                "Large Medkit (16)",
                "Invulnerability (15)",
                "Cells (13)",
                "Cells (14)",
            ],
        )
        self.connect(past_silver_door_area, silver_dive_area, r.can_dive)

        silver_dive_past_barrier_area = self.region(
            "Silver Dive Past Barrier",
            [
                "Gold Key (51)",
                "Invisibility (52)",
                "Rocketlauncher (62)",
                "Silver Key (64)",
                "Yellow Armor (29)",
                "Secret (44)",
                "Quad Damage (45)",
            ],
        )
        self.connect(
            silver_dive_area,
            silver_dive_past_barrier_area,
            self.event("Underwater Barrier Open"),
        )

        past_threebutton_door_area = self.region(
            "Past Three Buttons",
            [
                "Large Medkit (37)",
                "Spikes (39)",
                "Large Medkit (38)",
                "Spikes (40)",
                "Laser (36)",
            ],
        )
        self.connect(
            past_door_area,
            past_threebutton_door_area,
            self.event("Hit Button 1")
            & self.event("Hit Button 2")
            & self.event("Hit Button 3"),
        )

        past_button_area = self.region(
            "Past Button Area",
            [
                "Large Medkit (92)",
                "Large Medkit (93)",
                "Large Medkit (94)",
                "Large Medkit (95)",
                "Spikes (35)",
                "Spikes (59)",
                "Rockets (57)",
                "Rockets (58)",
                "Shells (33)",
                "Megahealth (63)",
                "Sewage System Open",
                "Small Medkit (27)",
                "Small Medkit (28)",
                "All Kills (96)",
            ],
        )
        self.connect(past_threebutton_door_area, past_button_area, r.can_button)
        self.restrict(
            "All Kills (96)",
            r.backpack(5) & self.gold_key & (self.silver_key | r.bigjump_hard),
        )

        box_jump_area = self.region(
            "Box Jump Area",
            [
                "Spikes (34)",
                "Large Medkit (89)",
                "Small Medkit (91)",
                "Small Medkit (90)",
                "Mjolnir (26)",
                "Red Armor (61)",
                "Secret (60)",
            ],
        )
        self.connect(past_button_area, box_jump_area, r.jump)

        return ret
