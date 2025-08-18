from BaseClasses import Region

from ..base_classes import Q1Level


class r1m4(Q1Level):
    name = "Cave of Death"
    mapfile = "r1m4"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Random (1)",
            "classname": "item_random_powerup",
            "uuid": 14779737789379406199,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Flag (2)",
            "classname": "item_flag",
            "uuid": 15266775142551297130,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Flag (3)",
            "classname": "item_flag_team2",
            "uuid": 15010687513530850420,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Flag (4)",
            "classname": "item_flag_team1",
            "uuid": 11776378556973319992,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Yellow Armor (5)",
            "classname": "item_armor2",
            "uuid": 10161434129294339661,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 414646658756727139,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 15796042733282836653,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 2809529110492176780,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Large Medkit (9)",
            "classname": "item_health",
            "uuid": 14797100721312036824,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Shells (10)",
            "classname": "item_shells",
            "uuid": 13831259249499016926,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 7087992229321516880,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Small Medkit (12)",
            "classname": "item_health",
            "uuid": 1983865346573657203,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Invisibility (13)",
            "classname": "item_artifact_invisibility",
            "uuid": 9074234737387588279,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Nailgun (14)",
            "classname": "weapon_nailgun",
            "uuid": 15574398365580143230,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 4951854497673976228,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 4012121201486319160,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 14031130480342284744,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Rockets (18)",
            "classname": "item_rockets",
            "uuid": 7808432327721466456,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Cells (19)",
            "classname": "item_cells",
            "uuid": 7078837023230932579,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Spikes (20)",
            "classname": "item_spikes",
            "uuid": 5747828568242987365,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 858542514719877646,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 3716640137276316221,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Grenadelauncher (23)",
            "classname": "weapon_grenadelauncher",
            "uuid": 11532268179321720259,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Rockets (24)",
            "classname": "item_rockets",
            "uuid": 3179837758089413072,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 5054627072656199533,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Lava (26)",
            "classname": "item_lava_spikes",
            "uuid": 296833190460521260,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 12329797202942034259,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 11354841726868183720,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Gold Key (29)",
            "classname": "item_key2",
            "uuid": 5641772618810361828,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 11116772364683911631,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Small Medkit (31)",
            "classname": "item_health",
            "uuid": 17903665163721859180,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Small Medkit (32)",
            "classname": "item_health",
            "uuid": 10348687606470045523,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Lava (33)",
            "classname": "item_lava_spikes",
            "uuid": 15484701334817387353,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Supershotgun (34)",
            "classname": "weapon_supershotgun",
            "uuid": 16465830685663994012,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Cells (35)",
            "classname": "item_cells",
            "uuid": 17599586608133928376,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Large Medkit (36)",
            "classname": "item_health",
            "uuid": 14392470602726963799,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Lava (37)",
            "classname": "item_lava_spikes",
            "uuid": 14991242525266867417,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Rockets (38)",
            "classname": "item_rockets",
            "uuid": 13467496448163109338,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Large Medkit (39)",
            "classname": "item_health",
            "uuid": 16285822683112535877,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Grenadelauncher (40)",
            "classname": "weapon_grenadelauncher",
            "uuid": 7538507855253345949,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 4421043089899835686,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Lava (42)",
            "classname": "item_lava_spikes",
            "uuid": 4865476247081698537,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 10868140085926679217,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Multi (44)",
            "classname": "item_multi_rockets",
            "uuid": 15410681730588509220,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Secret (45)",
            "classname": "trigger_secret",
            "uuid": 14858405203371289026,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Shells (46)",
            "classname": "item_shells",
            "uuid": 4812293773410914886,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Megahealth (47)",
            "classname": "item_health",
            "uuid": 18031861081532565529,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Cells (48)",
            "classname": "item_cells",
            "uuid": 3958812107485225301,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 3749284890788700950,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Spikes (50)",
            "classname": "item_spikes",
            "uuid": 6673044607165004307,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Lava (51)",
            "classname": "item_lava_spikes",
            "uuid": 7811187552784323469,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Shells (52)",
            "classname": "item_shells",
            "uuid": 3535214180819825423,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Green Armor (53)",
            "classname": "item_armor1",
            "uuid": 7569290051507643272,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Rocketlauncher (54)",
            "classname": "weapon_rocketlauncher",
            "uuid": 15673336383260860434,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Large Medkit (55)",
            "classname": "item_health",
            "uuid": 3073738229889787947,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Multi (56)",
            "classname": "item_multi_rockets",
            "uuid": 15855242952846302649,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Cells (57)",
            "classname": "item_cells",
            "uuid": 4071906862509695565,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Cells (58)",
            "classname": "item_cells",
            "uuid": 15064978736584495848,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Shells (59)",
            "classname": "item_shells",
            "uuid": 13025432563038551161,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Large Medkit (60)",
            "classname": "item_health",
            "uuid": 4172050974892462315,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Large Medkit (61)",
            "classname": "item_health",
            "uuid": 10909710136009047706,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Large Medkit (62)",
            "classname": "item_health",
            "uuid": 2386332673682397669,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Large Medkit (63)",
            "classname": "item_health",
            "uuid": 16572336049936538752,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Rockets (64)",
            "classname": "item_rockets",
            "uuid": 16127729244579226313,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 17326883566314053768,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Large Medkit (66)",
            "classname": "item_health",
            "uuid": 2096014338226685392,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Large Medkit (67)",
            "classname": "item_health",
            "uuid": 11380942647541828267,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Lava (68)",
            "classname": "item_lava_spikes",
            "uuid": 13459616883056950726,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Large Medkit (69)",
            "classname": "item_health",
            "uuid": 13461523060017533102,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Spikes (70)",
            "classname": "item_spikes",
            "uuid": 9587986310252419802,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Supernailgun (71)",
            "classname": "weapon_supernailgun",
            "uuid": 1092111372461738811,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Green Armor (72)",
            "classname": "item_armor1",
            "uuid": 8905661256002691414,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Lava (73)",
            "classname": "item_lava_spikes",
            "uuid": 17515420132010754577,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Shells (74)",
            "classname": "item_shells",
            "uuid": 6594463045717552850,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Large Medkit (75)",
            "classname": "item_health",
            "uuid": 5094448146824593574,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Secret (76)",
            "classname": "trigger_secret",
            "uuid": 11577957394711816168,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Shells (77)",
            "classname": "item_shells",
            "uuid": 7399357259581038527,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Large Medkit (78)",
            "classname": "item_health",
            "uuid": 9309131167696533128,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Large Medkit (79)",
            "classname": "item_health",
            "uuid": 17282509636594304905,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Biosuit (80)",
            "classname": "item_artifact_envirosuit",
            "uuid": 17860217929689611039,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Large Medkit (81)",
            "classname": "item_health",
            "uuid": 12422011866615031397,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Large Medkit (82)",
            "classname": "item_health",
            "uuid": 8756060087204249572,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Lava (83)",
            "classname": "item_lava_spikes",
            "uuid": 6248795127742954827,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Multi (84)",
            "classname": "item_multi_rockets",
            "uuid": 16716642778520531635,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Secret (85)",
            "classname": "trigger_secret",
            "uuid": 7026957060831680981,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Red Armor (86)",
            "classname": "item_armorInv",
            "uuid": 15354267848324935718,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Cells (87)",
            "classname": "item_cells",
            "uuid": 15234173337322584899,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Spikes (88)",
            "classname": "item_spikes",
            "uuid": 4462780696752126277,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Large Medkit (89)",
            "classname": "item_health",
            "uuid": 11395151051856955809,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Spikes (90)",
            "classname": "item_spikes",
            "uuid": 15242029083982899146,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Shells (91)",
            "classname": "item_shells",
            "uuid": 16380535927358094861,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Spikes (92)",
            "classname": "item_spikes",
            "uuid": 3647062961017644298,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Large Medkit (93)",
            "classname": "item_health",
            "uuid": 14374673027909028241,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Large Medkit (94)",
            "classname": "item_health",
            "uuid": 16326550411559305186,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Lightning (95)",
            "classname": "weapon_lightning",
            "uuid": 15697442568576584783,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "Lava (96)",
            "classname": "item_lava_spikes",
            "uuid": 2100239810447150847,
            "mp": 0,
        },
        {
            "id": 97,
            "name": "Large Medkit (97)",
            "classname": "item_health",
            "uuid": 13785481407380697185,
            "mp": 0,
        },
        {
            "id": 98,
            "name": "Large Medkit (98)",
            "classname": "item_health",
            "uuid": 10344666290123400159,
            "mp": 0,
        },
        {
            "id": 99,
            "name": "Large Medkit (99)",
            "classname": "item_health",
            "uuid": 13883383670690695292,
            "mp": 0,
        },
        {
            "id": 100,
            "name": "Lava (100)",
            "classname": "item_lava_spikes",
            "uuid": 15329046581816559631,
            "mp": 0,
        },
        {
            "id": 101,
            "name": "Powerup (101)",
            "classname": "item_powerup_shield",
            "uuid": 7175273306215954142,
            "mp": 1,
        },
        {
            "id": 102,
            "name": "Large Medkit (102)",
            "classname": "item_health",
            "uuid": 10427864444004031914,
            "mp": 0,
        },
        {
            "id": 103,
            "name": "Large Medkit (103)",
            "classname": "item_health",
            "uuid": 1062922974054529387,
            "mp": 0,
        },
        {
            "id": 104,
            "name": "Secret (104)",
            "classname": "trigger_secret",
            "uuid": 6575452460004204841,
            "mp": 0,
        },
        {
            "id": 105,
            "name": "Shells (105)",
            "classname": "item_shells",
            "uuid": 13511958843714748174,
            "mp": 0,
        },
        {
            "id": 106,
            "name": "Rockets (106)",
            "classname": "item_rockets",
            "uuid": 17601427680062467142,
            "mp": 0,
        },
        {
            "id": 107,
            "name": "Spikes (107)",
            "classname": "item_spikes",
            "uuid": 869251685692884843,
            "mp": 0,
        },
        {
            "id": 108,
            "name": "Quad Damage (108)",
            "classname": "item_artifact_super_damage",
            "uuid": 3055307111857571144,
            "mp": 1,
        },
        {
            "id": 109,
            "name": "Invulnerability (109)",
            "classname": "item_artifact_invulnerability",
            "uuid": 1659453511233759196,
            "mp": 1,
        },
        {
            "id": 110,
            "name": "Supernailgun (110)",
            "classname": "weapon_supernailgun",
            "uuid": 8223683996835451242,
            "mp": 1,
        },
        {
            "id": 111,
            "name": "Quad Damage (111)",
            "classname": "item_artifact_super_damage",
            "uuid": 16358313142869826906,
            "mp": 1,
        },
        {
            "id": 112,
            "name": "Powerup (112)",
            "classname": "item_powerup_belt",
            "uuid": 15759903422255602731,
            "mp": 1,
        },
        {
            "id": 113,
            "name": "Rockets (113)",
            "classname": "item_rockets",
            "uuid": 17932475570027320437,
            "mp": 0,
        },
        {
            "id": 114,
            "name": "Rockets (114)",
            "classname": "item_rockets",
            "uuid": 3324153609114749567,
            "mp": 0,
        },
        {
            "id": 115,
            "name": "Red Armor (115)",
            "classname": "item_armorInv",
            "uuid": 743207039222086807,
            "mp": 0,
        },
        {
            "id": 116,
            "name": "All Kills (116)",
            "classname": "all_kills",
            "uuid": 15105216357138164432,
            "mp": 0,
        },
    ]
    events = [
        "Underwater Barrier Open",
        "Bar Moved",
        "Water Brige Raised",
        "Middle Door Open",
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Small Medkit (32)",
                "Small Medkit (31)",
                "Supershotgun (34)",
                "Rockets (113)",
            ],
        )

        past_bridge_area = self.region(
            "Past Bridge Area",
            [
                "Powerup (112)",
                "Lava (26)",
                "Shells (25)",
                "Large Medkit (27)",
                "Large Medkit (28)",
                "Grenadelauncher (23)",
                "Rockets (24)",
                "Large Medkit (22)",
                "Nailgun (14)",
                "Shells (105)",
                "Large Medkit (75)",
                "Shells (15)",
                "Shells (74)",
                "Large Medkit (16)",
                "Large Medkit (17)",
                "Flag (4)",
                "Rockets (18)",
                "Lava (73)",
                "Green Armor (72)",
                "Rockets (114)",
                "Spikes (20)",
                "Large Medkit (21)",
                "Cells (19)",
                "Large Medkit (11)",
                "Small Medkit (12)",
                "Secret (76)",
                "Invisibility (13)",
                "Shells (77)",
            ],
        )
        self.connect(ret, past_bridge_area, r.can_shootswitch | r.bigjump_hard),
        self.restrict("Secret (76)", r.can_shootswitch)
        self.restrict("Invisibility (13)", r.can_shootswitch)
        self.restrict("Shells (77)", r.can_shootswitch)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Cells (35)",
                "Large Medkit (36)",
                "Rockets (106)",
                "Large Medkit (78)",
                "Large Medkit (39)",
                "Rockets (38)",
                "Grenadelauncher (40)",
                "Biosuit (80)",
                "Large Medkit (79)",
                "Spikes (107)",
                "Supernailgun (110)",
                "Underwater Barrier Open",
            ],
        )
        self.connect(past_bridge_area, past_button_area, r.can_button)
        self.restrict("Underwater Barrier Open", r.can_button)

        dive_area = self.region(
            "Dive Area",
            [
                "Large Medkit (82)",
                "Large Medkit (81)",
                "Cells (87)",
                "Spikes (88)",
                "Red Armor (86)",
                "Secret (85)",
            ],
        )
        self.connect(past_button_area, dive_area, r.can_dive)

        dive_barrier_area = self.region(
            "Dive Barrier",
            [
                "Spikes (90)",
                "Large Medkit (89)",
                "Flag (2)",
                "Large Medkit (66)",
                "Large Medkit (67)",
                "Quad Damage (111)",
                "Bar Moved",
            ],
        )
        self.connect(
            dive_area,
            dive_barrier_area,
            r.can_dive & self.event("Underwater Barrier Open"),
        )
        self.restrict("Bar Moved", r.can_door & r.can_shootswitch)
        self.restrict("Quad Damage (111)", r.can_door)

        moving_platform_area = self.region(
            "Moving Platform Area",
            [
                "Spikes (70)",
                "Supernailgun (71)",
                "Large Medkit (69)",
                "Water Brige Raised",
            ],
        )
        self.connect(
            dive_barrier_area,
            moving_platform_area,
            self.event("Bar Moved") | r.bigjump_hard,
        )
        self.restrict("Water Brige Raised", r.can_door & r.can_button)

        past_button_top_area = self.region(
            "Past Button Top",
            [
                "Spikes (92)",
                "Shells (91)",
                "Invulnerability (109)",
                "Random (1)",
            ],
        )

        self.connect(
            past_button_area,
            past_button_top_area,
            r.bigjump_hard | self.event("Water Brige Raised"),
        )
        self.restrict("Spikes (92)", r.can_door)
        self.restrict("Shells (91)", r.can_door)
        self.restrict("Random (1)", r.jump)

        minecart_area = self.region(
            "Minecart Area",
            [
                "Large Medkit (41)",
                "Lava (42)",
            ],
        )
        # TODO: Is 200 heal enough?
        self.connect(ret, minecart_area, r.bigjump_hard & r.heal(200))
        self.connect(minecart_area, past_button_top_area, r.can_door)
        self.connect(past_button_top_area, minecart_area, r.can_door)

        self.restrict("Large Medkit (41)", r.jump)
        self.restrict("Lava (42)", r.jump)

        right_path_area = self.region(
            "Right Path",
            [
                "Multi (44)",
                "Large Medkit (43)",
                "Green Armor (53)",
                "Large Medkit (49)",
                "Spikes (50)",
                "Secret (45)",
                "Cells (48)",
                "Shells (46)",
                "Megahealth (47)",
            ],
        )
        self.connect(minecart_area, right_path_area)
        self.connect(ret, right_path_area, r.bigjump_hard)
        self.restrict("Secret (45)", r.can_shootswitch)
        self.restrict("Cells (48)", r.can_shootswitch)
        self.restrict("Shells (46)", r.can_shootswitch)
        self.restrict("Megahealth (47)", r.can_shootswitch)

        past_right_door_area = self.region(
            "Past Right Door Area",
            [
                "Large Medkit (9)",
                "Shells (52)",
                "Large Medkit (7)",
                "Large Medkit (8)",
            ],
        )
        self.connect(right_path_area, past_right_door_area, r.can_door)

        past_right_button_area = self.region(
            "Past Right Button Area",
            [
                "Large Medkit (55)",
                "Flag (3)",
                "Yellow Armor (5)",
                "Cells (57)",
                "Cells (58)",
                "Shells (59)",
                "Large Medkit (6)",
                "Rocketlauncher (54)",
                "Multi (56)",
                "Middle Door Open",
            ],
        )
        self.connect(
            past_right_door_area, past_right_button_area, r.can_button | r.bigjump_hard
        )
        self.restrict("Middle Door Open", r.can_button)

        middle_door_area = self.region(
            "Middle Door Area",
            [
                "Large Medkit (61)",
                "Large Medkit (60)",
                "Shells (10)",
                "Large Medkit (93)",
                "Large Medkit (94)",
                "Rockets (64)",
                "Shells (65)",
                "Lightning (95)",
                "Large Medkit (62)",
                "Large Medkit (63)",
                "Powerup (101)",
                "Gold Key (29)",
                "Lava (96)",
                "Large Medkit (97)",
            ],
        )

        self.connect(past_right_button_area, middle_door_area, r.can_door)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (98)",
                "Large Medkit (99)",
            ],
        )
        self.connect(middle_door_area, past_gold_door_area, self.gold_key)

        past_gold_door_upper_area = self.region(
            "Past Gold Door Upper",
            [
                "Secret (104)",
                "Red Armor (115)",
                "Large Medkit (103)",
                "Large Medkit (102)",
                "Exit",
                "All Kills (116)",
            ],
        )
        self.connect(past_gold_door_area, past_gold_door_upper_area, r.jump)
        self.restrict("All Kills (116)", r.difficult_combat & r.can_dive & r.can_button)

        return ret
