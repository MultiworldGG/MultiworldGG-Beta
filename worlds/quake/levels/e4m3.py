from BaseClasses import Region

from ..base_classes import Q1Level


class e4m3(Q1Level):
    name = "The Elder God Shrine"
    mapfile = "e4m3"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Large Medkit (1)",
            "classname": "item_health",
            "uuid": 15761594790704459630,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Large Medkit (2)",
            "classname": "item_health",
            "uuid": 1546782975300533748,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Shells (3)",
            "classname": "item_shells",
            "uuid": 5547300218547497500,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 2001476606140063734,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Spikes (5)",
            "classname": "item_spikes",
            "uuid": 6806182981768470147,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Small Medkit (6)",
            "classname": "item_health",
            "uuid": 16387035033250039981,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 14138847767242433499,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Small Medkit (8)",
            "classname": "item_health",
            "uuid": 5787274399497723785,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Shells (9)",
            "classname": "item_shells",
            "uuid": 1357767518778708256,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Small Medkit (10)",
            "classname": "item_health",
            "uuid": 11360400561200938862,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 13434800103865653178,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Rockets (12)",
            "classname": "item_rockets",
            "uuid": 2957638148678929655,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Large Medkit (13)",
            "classname": "item_health",
            "uuid": 14736648646704306427,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Spikes (14)",
            "classname": "item_spikes",
            "uuid": 5166229677132794929,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 14721216815415919625,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Spikes (16)",
            "classname": "item_spikes",
            "uuid": 5927983445365849722,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Spikes (17)",
            "classname": "item_spikes",
            "uuid": 1843834661303079561,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Green Armor (18)",
            "classname": "item_armor1",
            "uuid": 12791722574774038454,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 450912705831782071,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Grenadelauncher (20)",
            "classname": "weapon_grenadelauncher",
            "uuid": 9249338313042502260,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Megahealth (21)",
            "classname": "item_health",
            "uuid": 9227556425277965061,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Rockets (22)",
            "classname": "item_rockets",
            "uuid": 4586290731985904368,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Rockets (23)",
            "classname": "item_rockets",
            "uuid": 3027725418530133852,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 12290200673017846063,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Silver Key (25)",
            "classname": "item_key1",
            "uuid": 825675624028462295,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 13038678942923309466,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Spikes (27)",
            "classname": "item_spikes",
            "uuid": 9044593715553557543,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Megahealth (28)",
            "classname": "item_health",
            "uuid": 2383680860032180268,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Rockets (29)",
            "classname": "item_rockets",
            "uuid": 15718620762711007246,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Yellow Armor (30)",
            "classname": "item_armor2",
            "uuid": 5072611397776792033,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 15790624122476084801,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Gold Key (32)",
            "classname": "item_key2",
            "uuid": 9686135577733236203,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Red Armor (33)",
            "classname": "item_armorInv",
            "uuid": 8042962346297145277,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Rockets (34)",
            "classname": "item_rockets",
            "uuid": 27938546152472179,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 15090734116213717924,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Large Medkit (36)",
            "classname": "item_health",
            "uuid": 3686106775282685508,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 16047288600720490627,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Small Medkit (38)",
            "classname": "item_health",
            "uuid": 14000711451726154924,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 10689808719492275355,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 1386062936536695671,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Rockets (41)",
            "classname": "item_rockets",
            "uuid": 12551735446659766530,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Shells (42)",
            "classname": "item_shells",
            "uuid": 11930615074492784659,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 6506115811545609464,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 6363355446907782727,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Shells (45)",
            "classname": "item_shells",
            "uuid": 6920247562713562573,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Grenadelauncher (46)",
            "classname": "weapon_grenadelauncher",
            "uuid": 11060361246207066901,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 1956855501681883748,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 5906250631573590341,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Spikes (49)",
            "classname": "item_spikes",
            "uuid": 18171277084260661413,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Small Medkit (50)",
            "classname": "item_health",
            "uuid": 1095849690209467905,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 8903821253751488702,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 9649386200592751538,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Quad Damage (53)",
            "classname": "item_artifact_super_damage",
            "uuid": 395572097508428641,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Quad Damage (54)",
            "classname": "item_artifact_super_damage",
            "uuid": 6854484422833493608,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Megahealth (55)",
            "classname": "item_health",
            "uuid": 4971549929756561070,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Large Medkit (56)",
            "classname": "item_health",
            "uuid": 17780958345382264192,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Large Medkit (57)",
            "classname": "item_health",
            "uuid": 3626534716533468672,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Secret (58)",
            "classname": "trigger_secret",
            "uuid": 12365435492275040287,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Secret (59)",
            "classname": "trigger_secret",
            "uuid": 16637844468135486844,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Nailgun (60)",
            "classname": "weapon_nailgun",
            "uuid": 10686753102538252514,
            "mp": 1,
        },
        {
            "id": 61,
            "name": "Nailgun (61)",
            "classname": "weapon_nailgun",
            "uuid": 9875881924555297743,
            "mp": 1,
        },
        {
            "id": 62,
            "name": "Supershotgun (62)",
            "classname": "weapon_supershotgun",
            "uuid": 16781770318278403430,
            "mp": 1,
        },
        {
            "id": 63,
            "name": "Lightning (63)",
            "classname": "weapon_lightning",
            "uuid": 9128240606266942570,
            "mp": 1,
        },
        {
            "id": 64,
            "name": "Grenadelauncher (64)",
            "classname": "weapon_grenadelauncher",
            "uuid": 5776456715938692422,
            "mp": 1,
        },
        {
            "id": 65,
            "name": "Cells (65)",
            "classname": "item_cells",
            "uuid": 1768573811119980636,
            "mp": 1,
        },
        {
            "id": 66,
            "name": "Cells (66)",
            "classname": "item_cells",
            "uuid": 9448358355178499635,
            "mp": 1,
        },
        {
            "id": 67,
            "name": "Quad Damage (67)",
            "classname": "item_artifact_super_damage",
            "uuid": 6453202365945630338,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Green Armor (68)",
            "classname": "item_armor1",
            "uuid": 15726711857217927346,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Supershotgun (69)",
            "classname": "weapon_supershotgun",
            "uuid": 10783040152594567380,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Rocketlauncher (70)",
            "classname": "weapon_rocketlauncher",
            "uuid": 6082195541732975394,
            "mp": 1,
        },
        {
            "id": 71,
            "name": "Lightning (71)",
            "classname": "weapon_lightning",
            "uuid": 1697945015819249631,
            "mp": 1,
        },
        {
            "id": 72,
            "name": "Quad Damage (72)",
            "classname": "item_artifact_super_damage",
            "uuid": 16408695099182349000,
            "mp": 1,
        },
        {
            "id": 73,
            "name": "Invisibility (73)",
            "classname": "item_artifact_invisibility",
            "uuid": 3008524786920849077,
            "mp": 1,
        },
        {
            "id": 74,
            "name": "Rocketlauncher (74)",
            "classname": "weapon_rocketlauncher",
            "uuid": 6883320408120858277,
            "mp": 1,
        },
        {
            "id": 75,
            "name": "Supernailgun (75)",
            "classname": "weapon_supernailgun",
            "uuid": 4543417612369120164,
            "mp": 1,
        },
        {
            "id": 76,
            "name": "Shells (76)",
            "classname": "item_shells",
            "uuid": 16962521192401290665,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Spikes (77)",
            "classname": "item_spikes",
            "uuid": 2482273266167427553,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Quad Damage (78)",
            "classname": "item_artifact_super_damage",
            "uuid": 9190210804979694049,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Spikes (79)",
            "classname": "item_spikes",
            "uuid": 4841839984631187964,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Spikes (80)",
            "classname": "item_spikes",
            "uuid": 2857707764206758069,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Rockets (81)",
            "classname": "item_rockets",
            "uuid": 4574549905671064064,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Spikes (82)",
            "classname": "item_spikes",
            "uuid": 3072411123897089079,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Invisibility (83)",
            "classname": "item_artifact_invisibility",
            "uuid": 9702844477754384125,
            "mp": 1,
        },
        {
            "id": 84,
            "name": "Secret (84)",
            "classname": "trigger_secret",
            "uuid": 1483928915432705123,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Spikes (85)",
            "classname": "item_spikes",
            "uuid": 5808282553179752183,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Shells (86)",
            "classname": "item_shells",
            "uuid": 190652569478174030,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Invisibility (87)",
            "classname": "item_artifact_invisibility",
            "uuid": 14562135202562479897,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Small Medkit (88)",
            "classname": "item_health",
            "uuid": 6938794786215391761,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Invisibility (89)",
            "classname": "item_artifact_invisibility",
            "uuid": 10111509878285745578,
            "mp": 1,
        },
        {
            "id": 90,
            "name": "Shells (90)",
            "classname": "item_shells",
            "uuid": 11886205458535022059,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Shells (91)",
            "classname": "item_shells",
            "uuid": 15147524366737799050,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Quad Damage (92)",
            "classname": "item_artifact_super_damage",
            "uuid": 7547614093850721080,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Small Medkit (93)",
            "classname": "item_health",
            "uuid": 17238516651199192632,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "All Kills (94)",
            "classname": "all_kills",
            "uuid": 8292261081458252020,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Small Medkit (6)",
                "Nailgun (61)",
                "Small Medkit (10)",
                "Spikes (39)",
                "Megahealth (55)",
            ],
        )

        start_upper_area = self.region(
            "Start Upper",
            [
                "Megahealth (28)",
                "Rockets (29)",
            ],
        )
        self.connect(
            ret,
            start_upper_area,
            (r.can_jump & r.difficulty("hard"))
            | r.can_gj_extr
            | r.can_rj_hard
            | r.bigjump_hard,
        )

        upper_past_door_area = self.region(
            "Upper Past Door",
            [
                "Spikes (85)",
                "Shells (90)",
                "Spikes (26)",
                "Spikes (27)",
                "Shells (86)",
                "Yellow Armor (30)",
                "Supernailgun (75)",
                "Small Medkit (38)",
                "Invisibility (87)",
                "Large Medkit (37)",
                "Small Medkit (88)",
                "Rockets (81)",
                "Shells (76)",
                "Shells (40)",
                "Shells (91)",
                "Large Medkit (4)",
                "Grenadelauncher (64)",
                "Quad Damage (54)",
                "Secret (58)",
                "Large Medkit (57)",
                "Large Medkit (56)",
                "Rockets (12)",
                "Large Medkit (13)",
                "Spikes (5)",
                "Large Medkit (48)",
                "Rockets (41)",
                "Shells (42)",
            ],
        )
        self.connect(start_upper_area, upper_past_door_area, r.can_door)
        self.connect(upper_past_door_area, start_upper_area, r.can_door)

        past_timed_floor_area = self.region(
            "Past Timed Floor",
            [
                "Invisibility (73)",
                "Spikes (79)",
                "Large Medkit (43)",
                "Grenadelauncher (46)",
                "Quad Damage (72)",
                "Rockets (47)",
                "Large Medkit (31)",
                "Silver Key (25)",
                "Lightning (71)",
            ],
        )
        self.connect(
            upper_past_door_area,
            past_timed_floor_area,
            r.difficulty("hard") | r.can_run,
        )

        start_past_shoot_area = self.region(
            "Shootswitch Area",
            [
                "Quad Damage (53)",
                "Spikes (15)",
                "Shells (11)",
                "Spikes (82)",
                "Spikes (49)",
            ],
        )
        self.connect(ret, start_past_shoot_area, r.can_shootswitch)

        past_lower_door_area = self.region(
            "Past Lower Door",
            [
                "Small Medkit (8)",
                "Shells (3)",
                "Large Medkit (2)",
                "Spikes (19)",
                "Spikes (16)",
                "Large Medkit (1)",
                "Supershotgun (62)",
                "Green Armor (18)",
                "Spikes (17)",
                "Shells (9)",
            ],
        )
        self.connect(start_past_shoot_area, past_lower_door_area, r.can_door)

        past_button_area = self.region(
            "Past Button",
            [
                "Spikes (14)",
                "Large Medkit (52)",
                "Shells (45)",
                "Invisibility (83)",
                "Spikes (24)",
                "Large Medkit (7)",
            ],
        )
        self.connect(past_lower_door_area, past_button_area, r.can_button)

        past_button_jumpdive_area = self.region(
            "Past Button Jump-dive",
            [
                "Small Medkit (50)",
                "Grenadelauncher (20)",
                "Quad Damage (78)",
                "Megahealth (21)",
                "Rockets (22)",
                "Nailgun (60)",
                "Rockets (23)",
            ],
        )
        self.connect(past_button_area, past_button_jumpdive_area, r.can_dive & r.jump)
        self.connect(past_button_jumpdive_area, upper_past_door_area)

        button_secret_area = self.region(
            "Button Secret",
            [
                "Secret (59)",
                "Green Armor (68)",
                "Shells (44)",
                "Cells (65)",
                "Supershotgun (69)",
                "Spikes (80)",
                "Quad Damage (67)",
                "Cells (66)",
            ],
        )
        self.connect(upper_past_door_area, button_secret_area, r.can_button)

        button_secret_upper_area = self.region(
            "Button Secret Upper",
            [
                "Red Armor (33)",
                "Large Medkit (36)",
                "Lightning (63)",
                "Rockets (34)",
                "Secret (84)",
                "Spikes (77)",
                "Large Medkit (35)",
            ],
        )
        self.connect(
            upper_past_door_area,
            button_secret_upper_area,
            r.bigjump_hard,
        )
        self.connect(button_secret_area, button_secret_upper_area)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Rocketlauncher (70)",
                "Exit",
            ],
        )
        self.connect(upper_past_door_area, past_gold_door_area, self.gold_key)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Quad Damage (92)",
                "Invisibility (89)",
                "Small Medkit (93)",
                "Rocketlauncher (74)",
                "Gold Key (32)",
                "All Kills (94)",
            ],
        )
        self.connect(upper_past_door_area, past_silver_door_area, self.silver_key)

        self.restrict("All Kills (94)", r.can_dive & r.jump & r.difficult_combat)

        return ret
