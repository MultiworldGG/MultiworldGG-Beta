from BaseClasses import Region

from ..base_classes import Q1Level


class e4m6(Q1Level):
    name = "The Pain Maze"
    mapfile = "e4m6"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Small Medkit (1)",
            "classname": "item_health",
            "uuid": 3241991499619994213,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Small Medkit (2)",
            "classname": "item_health",
            "uuid": 16230510781233273330,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Small Medkit (3)",
            "classname": "item_health",
            "uuid": 18009989094969172807,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Green Armor (4)",
            "classname": "item_armor1",
            "uuid": 2954397144726839186,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Large Medkit (5)",
            "classname": "item_health",
            "uuid": 15036005090308740564,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 11155913450479821573,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 5516197366552989128,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 3419634477161322570,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Shells (9)",
            "classname": "item_shells",
            "uuid": 14991345776168779070,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Rockets (10)",
            "classname": "item_rockets",
            "uuid": 3405265551329778163,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Small Medkit (11)",
            "classname": "item_health",
            "uuid": 7607514519658377932,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 12460486546417194025,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Megahealth (13)",
            "classname": "item_health",
            "uuid": 3779175773124223576,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 3931338066559878647,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 9119969489036561538,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Rocketlauncher (16)",
            "classname": "weapon_rocketlauncher",
            "uuid": 807489475606663094,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Red Armor (17)",
            "classname": "item_armorInv",
            "uuid": 6226334439525888364,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 7094661014039619768,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 12910235858775619069,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rockets (20)",
            "classname": "item_rockets",
            "uuid": 126427877187771144,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Cells (21)",
            "classname": "item_cells",
            "uuid": 8984878288388652603,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 6704086700416753038,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Quad Damage (23)",
            "classname": "item_artifact_super_damage",
            "uuid": 816645704491495731,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Gold Key (24)",
            "classname": "item_key2",
            "uuid": 14030519458621559022,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Biosuit (25)",
            "classname": "item_artifact_envirosuit",
            "uuid": 1692773301411291773,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 6392782454071631212,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Lightning (27)",
            "classname": "weapon_lightning",
            "uuid": 7891064772579920160,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 14776711580842596787,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 6181804916317801265,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Secret (30)",
            "classname": "trigger_secret",
            "uuid": 9073640025702237526,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Spikes (31)",
            "classname": "item_spikes",
            "uuid": 17900840802415414085,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Spikes (32)",
            "classname": "item_spikes",
            "uuid": 11323991683683577976,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 14203970097385008830,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Spikes (34)",
            "classname": "item_spikes",
            "uuid": 2354265642317168985,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Small Medkit (35)",
            "classname": "item_health",
            "uuid": 10227161144098900422,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 11016282988229602307,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Secret (37)",
            "classname": "trigger_secret",
            "uuid": 16758062640181617288,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Megahealth (38)",
            "classname": "item_health",
            "uuid": 5963029479358418593,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 11142423634343009027,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Silver Key (40)",
            "classname": "item_key1",
            "uuid": 7077883947081512418,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Cells (41)",
            "classname": "item_cells",
            "uuid": 5086600133107767009,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Yellow Armor (42)",
            "classname": "item_armor2",
            "uuid": 1501099682391748220,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 13300654535809231028,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Spikes (44)",
            "classname": "item_spikes",
            "uuid": 17899460053271584137,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Spikes (45)",
            "classname": "item_spikes",
            "uuid": 1327642106546401783,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Cells (46)",
            "classname": "item_cells",
            "uuid": 7988715494989981497,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 77335380236371715,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Quad Damage (48)",
            "classname": "item_artifact_super_damage",
            "uuid": 16157408852015428116,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Biosuit (49)",
            "classname": "item_artifact_envirosuit",
            "uuid": 14439331550158477004,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Biosuit (50)",
            "classname": "item_artifact_envirosuit",
            "uuid": 18202486902048245672,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Invisibility (51)",
            "classname": "item_artifact_invisibility",
            "uuid": 8757638924865279556,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Quad Damage (52)",
            "classname": "item_artifact_super_damage",
            "uuid": 4922085923044720118,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Cells (53)",
            "classname": "item_cells",
            "uuid": 600444409550613595,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Spikes (54)",
            "classname": "item_spikes",
            "uuid": 16404252450394255371,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 545018783130938208,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Shells (56)",
            "classname": "item_shells",
            "uuid": 5675297109981101763,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Large Medkit (57)",
            "classname": "item_health",
            "uuid": 14792954269797936340,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 10118946840249750374,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Grenadelauncher (59)",
            "classname": "weapon_grenadelauncher",
            "uuid": 14387557833676739692,
            "mp": 1,
        },
        {
            "id": 60,
            "name": "Supershotgun (60)",
            "classname": "weapon_supershotgun",
            "uuid": 4855951176610813452,
            "mp": 1,
        },
        {
            "id": 61,
            "name": "Supernailgun (61)",
            "classname": "weapon_supernailgun",
            "uuid": 9850550435285178492,
            "mp": 1,
        },
        {
            "id": 62,
            "name": "Supershotgun (62)",
            "classname": "weapon_supershotgun",
            "uuid": 11207499123901638362,
            "mp": 1,
        },
        {
            "id": 63,
            "name": "Nailgun (63)",
            "classname": "weapon_nailgun",
            "uuid": 2042750859683228227,
            "mp": 1,
        },
        {
            "id": 64,
            "name": "Grenadelauncher (64)",
            "classname": "weapon_grenadelauncher",
            "uuid": 3761554180971348998,
            "mp": 1,
        },
        {
            "id": 65,
            "name": "Lightning (65)",
            "classname": "weapon_lightning",
            "uuid": 3688878317910917410,
            "mp": 1,
        },
        {
            "id": 66,
            "name": "Supernailgun (66)",
            "classname": "weapon_supernailgun",
            "uuid": 5455626845061577766,
            "mp": 1,
        },
        {
            "id": 67,
            "name": "Grenadelauncher (67)",
            "classname": "weapon_grenadelauncher",
            "uuid": 16014039301811604021,
            "mp": 1,
        },
        {
            "id": 68,
            "name": "Supershotgun (68)",
            "classname": "weapon_supershotgun",
            "uuid": 13809994104295493558,
            "mp": 1,
        },
        {
            "id": 69,
            "name": "Secret (69)",
            "classname": "trigger_secret",
            "uuid": 2354242701640752168,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Cells (70)",
            "classname": "item_cells",
            "uuid": 4740718696902753013,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Invulnerability (71)",
            "classname": "item_artifact_invulnerability",
            "uuid": 677190920827159455,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Shells (72)",
            "classname": "item_shells",
            "uuid": 7807955512538568120,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Spikes (73)",
            "classname": "item_spikes",
            "uuid": 14734974882231107572,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 3013530119102883235,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Cells (75)",
            "classname": "item_cells",
            "uuid": 4811498264339447459,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Spikes (76)",
            "classname": "item_spikes",
            "uuid": 14766723846907126327,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Shells (77)",
            "classname": "item_shells",
            "uuid": 4077637652690902659,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Rockets (78)",
            "classname": "item_rockets",
            "uuid": 13566730638844453324,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Rockets (79)",
            "classname": "item_rockets",
            "uuid": 2531663305446298248,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Shells (80)",
            "classname": "item_shells",
            "uuid": 7263702051166490758,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Invisibility (81)",
            "classname": "item_artifact_invisibility",
            "uuid": 3980700796395144740,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Cells (82)",
            "classname": "item_cells",
            "uuid": 14092798681066147026,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Rockets (83)",
            "classname": "item_rockets",
            "uuid": 6251298929827883156,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Cells (84)",
            "classname": "item_cells",
            "uuid": 4838062628291922639,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Cells (85)",
            "classname": "item_cells",
            "uuid": 6120364231318970537,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Rockets (86)",
            "classname": "item_rockets",
            "uuid": 11978424628487148866,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Cells (87)",
            "classname": "item_cells",
            "uuid": 9140404119168103169,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Lightning (88)",
            "classname": "weapon_lightning",
            "uuid": 16368266876800551182,
            "mp": 1,
        },
        {
            "id": 89,
            "name": "Cells (89)",
            "classname": "item_cells",
            "uuid": 9489574961990181108,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Cells (90)",
            "classname": "item_cells",
            "uuid": 17303001235265146286,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Rockets (91)",
            "classname": "item_rockets",
            "uuid": 7169235666488221866,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Cells (92)",
            "classname": "item_cells",
            "uuid": 14199643005052730478,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Rockets (93)",
            "classname": "item_rockets",
            "uuid": 44558495097573837,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Shells (94)",
            "classname": "item_shells",
            "uuid": 14430420603403158559,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Spikes (95)",
            "classname": "item_spikes",
            "uuid": 2206045167334346280,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "Spikes (96)",
            "classname": "item_spikes",
            "uuid": 17305531274995786474,
            "mp": 0,
        },
        {
            "id": 97,
            "name": "Rockets (97)",
            "classname": "item_rockets",
            "uuid": 10527895509891626706,
            "mp": 0,
        },
        {
            "id": 98,
            "name": "Invisibility (98)",
            "classname": "item_artifact_invisibility",
            "uuid": 5443801904280597366,
            "mp": 0,
        },
        {
            "id": 99,
            "name": "All Kills (99)",
            "classname": "all_kills",
            "uuid": 14575534883812614608,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Grenadelauncher (59)",
                "Megahealth (38)",
                "Quad Damage (23)",
                "Cells (90)",
                "Invisibility (98)",
                "Cells (89)",
                "Small Medkit (1)",
                "Small Medkit (2)",
                "Small Medkit (3)",
                "Shells (14)",
                "Green Armor (4)",
                "Cells (82)",
                "Spikes (34)",
                "Rockets (91)",
            ],
        )

        past_bars_area = self.region(
            "Past Bars",
            [
                "Rockets (20)",
                "Large Medkit (18)",
                "Large Medkit (22)",
                "Cells (21)",
                "Shells (94)",
                "Large Medkit (19)",
                "Gold Key (24)",
            ],
        )
        self.connect(
            ret,
            past_bars_area,
            r.bigjump_hard | r.can_rj_hard | r.can_gj_extr | r.can_door,
        )
        self.restrict("Gold Key (24)", r.can_button)

        dive_area = self.region(
            "Dive Area",
            [
                "Small Medkit (35)",
                "Spikes (36)",
                "Supernailgun (61)",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [],
        )
        self.connect(dive_area, past_silver_door_area, self.silver_key)

        past_button_area = self.region(
            "Past Button",
            [
                "Secret (30)",
                "Cells (84)",
                "Spikes (95)",
                "Lightning (88)",
                "Rockets (83)",
            ],
        )
        self.connect(ret, past_button_area, r.can_button & r.jump)

        past_door_area = self.region(
            "Past Door",
            [
                "Large Medkit (6)",
                "Large Medkit (5)",
                "Spikes (31)",
                "Spikes (32)",
                "Supershotgun (60)",
                "Shells (33)",
                "Silver Key (40)",
                "Large Medkit (29)",
                "Cells (41)",
                "Cells (92)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        self.connect(past_button_area, past_door_area)
        self.connect(past_door_area, past_button_area, r.jump)
        self.restrict("Silver Key (40)", r.can_shootswitch)
        self.restrict("Large Medkit (29)", r.jump)
        self.restrict("Cells (41)", r.jump)
        self.restrict("Cells (92)", r.jump)

        past_door_dive_area = self.region(
            "Past Door Dive",
            [
                "Secret (39)",
                "Lightning (27)",
                "Large Medkit (28)",
                "Rockets (26)",
                "Rockets (93)",
                "Biosuit (25)",
                "Biosuit (49)",
                "Shells (77)",
                "Large Medkit (57)",
                "Invisibility (51)",
                "Shells (56)",
                "Cells (75)",
                "Shells (55)",
                "Spikes (76)",
                "Rockets (97)",
                "Large Medkit (58)",
                "Secret (69)",
                "Spikes (96)",
                "Cells (70)",
                "Cells (85)",
                "Invulnerability (71)",
            ],
        )
        self.connect(past_door_area, past_door_dive_area, r.can_dive)
        self.connect(past_silver_door_area, past_door_dive_area)
        self.restrict("Secret (69)", r.can_shootswitch)
        self.restrict("Spikes (96)", r.can_shootswitch)
        self.restrict("Cells (70)", r.can_shootswitch)
        self.restrict("Cells (85)", r.can_shootswitch)
        self.restrict("Invulnerability (71)", r.can_shootswitch)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Spikes (73)",
                "Spikes (74)",
                "Quad Damage (52)",
                "Shells (80)",
                "Cells (53)",
                "Secret (37)",
                "Red Armor (17)",
            ],
        )
        self.connect(
            past_silver_door_area,
            past_gold_door_area,
            self.gold_key | r.bigjump_hard,
        )
        self.restrict("Cells (53)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Secret (37)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Red Armor (17)", r.can_shootswitch | r.bigjump_hard)

        past_second_silver_door_area = self.region(
            "Second Silver Door",
            [
                "Shells (72)",
                "Invisibility (81)",
                "Large Medkit (7)",
                "Shells (9)",
                "Yellow Armor (42)",
                "Nailgun (63)",
                "Rockets (10)",
                "Grenadelauncher (64)",
                "Large Medkit (8)",
                "Spikes (44)",
                "Large Medkit (43)",
            ],
        )
        self.connect(
            past_gold_door_area, past_second_silver_door_area, self.silver_key & r.jump
        )

        top_teleporter_area = self.region(
            "Top Teleporter Area",
            [
                "Cells (87)",
                "Rockets (86)",
                "Rockets (79)",
                "Rockets (78)",
                "Lightning (65)",
                "Biosuit (50)",
                "Supershotgun (62)",
                "Rocketlauncher (16)",
                "Spikes (45)",
                "Rockets (47)",
                "Quad Damage (48)",
                "Spikes (54)",
                "Supernailgun (66)",
                "Small Medkit (11)",
                "Shells (12)",
                "Cells (46)",
                "Megahealth (13)",
                "All Kills (99)",
            ],
        )
        self.connect(
            past_second_silver_door_area, top_teleporter_area, r.can_button & r.jump
        )
        self.connect(past_gold_door_area, top_teleporter_area, r.bigjump_hard)
        self.restrict("All Kills (99)", r.difficult_combat)

        past_altar_area = self.region(
            "Past Altar",
            [
                "Supershotgun (68)",
                "Grenadelauncher (67)",
                "Exit",
            ],
        )
        self.connect(top_teleporter_area, past_altar_area, r.can_shootswitch)

        return ret
