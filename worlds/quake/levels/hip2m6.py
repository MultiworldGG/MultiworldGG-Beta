from BaseClasses import Region

from ..base_classes import Q1Level


class hip2m6(Q1Level):
    name = "The Gremlin's Domain"
    mapfile = "hip2m6"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Gold Key (1)",
            "classname": "item_key2",
            "uuid": 5680721550479372899,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Silver Key (2)",
            "classname": "item_key1",
            "uuid": 13122912758449211671,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Secret (3)",
            "classname": "trigger_secret",
            "uuid": 10869929697482596781,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Quad Damage (4)",
            "classname": "item_artifact_super_damage",
            "uuid": 17537939230353111004,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Secret (5)",
            "classname": "trigger_secret",
            "uuid": 17807790729178219537,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Grenadelauncher (6)",
            "classname": "weapon_grenadelauncher",
            "uuid": 16929868990491597009,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Supershotgun (7)",
            "classname": "weapon_supershotgun",
            "uuid": 1330537630130996096,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Rocketlauncher (8)",
            "classname": "weapon_rocketlauncher",
            "uuid": 3700798159822825859,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Large Medkit (9)",
            "classname": "item_health",
            "uuid": 16686510914859090449,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 1333250173700483136,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 14602400762498498616,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 17957362813102230030,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 13547075631735544924,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 8544082238279368017,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 15005142201436226482,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Shells (16)",
            "classname": "item_shells",
            "uuid": 12494934424999624133,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Small Medkit (17)",
            "classname": "item_health",
            "uuid": 12086621434782511161,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Megahealth (18)",
            "classname": "item_health",
            "uuid": 5728040401361362964,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Rockets (19)",
            "classname": "item_rockets",
            "uuid": 17354515440629318354,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Shells (20)",
            "classname": "item_shells",
            "uuid": 16846342516878879688,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Shells (21)",
            "classname": "item_shells",
            "uuid": 16428311240176744950,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Small Medkit (22)",
            "classname": "item_health",
            "uuid": 6776416886425677367,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Supernailgun (23)",
            "classname": "weapon_supernailgun",
            "uuid": 8260459988793582735,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 12087427089293269053,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 364640658668820375,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 4159843038241977329,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Shells (27)",
            "classname": "item_shells",
            "uuid": 18017009526019888886,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Spikes (28)",
            "classname": "item_spikes",
            "uuid": 5251294643832433554,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Invisibility (29)",
            "classname": "item_artifact_invisibility",
            "uuid": 15055466104867764059,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Secret (30)",
            "classname": "trigger_secret",
            "uuid": 1664294617321520960,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 6935770277502351993,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Secret (32)",
            "classname": "trigger_secret",
            "uuid": 16221542760412884437,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Small Medkit (33)",
            "classname": "item_health",
            "uuid": 13074932987753870916,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Mjolnir (34)",
            "classname": "weapon_mjolnir",
            "uuid": 14934529997302624503,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 13043457508023667550,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Shells (36)",
            "classname": "item_shells",
            "uuid": 17724829278324152210,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Spikes (37)",
            "classname": "item_spikes",
            "uuid": 12152122311207083562,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 15602192392822254859,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 5863411015713373605,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Spikes (40)",
            "classname": "item_spikes",
            "uuid": 7929691726470957005,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Spikes (41)",
            "classname": "item_spikes",
            "uuid": 17022649740131802598,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Shells (42)",
            "classname": "item_shells",
            "uuid": 10451338248602795292,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 16950620969337584878,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Large Medkit (44)",
            "classname": "item_health",
            "uuid": 4111210428913245313,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Rockets (45)",
            "classname": "item_rockets",
            "uuid": 17177035056264232947,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Shells (46)",
            "classname": "item_shells",
            "uuid": 18338702313512215121,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Small Medkit (47)",
            "classname": "item_health",
            "uuid": 6779425867035335046,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Small Medkit (48)",
            "classname": "item_health",
            "uuid": 9989203201100251438,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Shells (49)",
            "classname": "item_shells",
            "uuid": 7911098321504946454,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 11233115319186129821,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Shells (51)",
            "classname": "item_shells",
            "uuid": 5244371620697543970,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Rockets (52)",
            "classname": "item_rockets",
            "uuid": 5334519341318658111,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Lightning (53)",
            "classname": "weapon_lightning",
            "uuid": 6787460340440259065,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 6852713010847625087,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Small Medkit (55)",
            "classname": "item_health",
            "uuid": 3801920306887968172,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Small Medkit (56)",
            "classname": "item_health",
            "uuid": 17053906430513834842,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Large Medkit (57)",
            "classname": "item_health",
            "uuid": 467597315700683960,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Yellow Armor (58)",
            "classname": "item_armor2",
            "uuid": 13754671627339002028,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Secret (59)",
            "classname": "trigger_secret",
            "uuid": 96902847924101352,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 2493577604554460078,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Large Medkit (61)",
            "classname": "item_health",
            "uuid": 9488028707107656710,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Shells (62)",
            "classname": "item_shells",
            "uuid": 6388995427436061134,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Invulnerability (63)",
            "classname": "item_artifact_invulnerability",
            "uuid": 7296163413538562216,
            "mp": 1,
        },
        {
            "id": 64,
            "name": "Wetsuit (64)",
            "classname": "item_artifact_wetsuit",
            "uuid": 13956239184799489068,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Rockets (65)",
            "classname": "item_rockets",
            "uuid": 17427088754818716256,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Rockets (66)",
            "classname": "item_rockets",
            "uuid": 14459443435884814019,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Small Medkit (67)",
            "classname": "item_health",
            "uuid": 11266912945590326368,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Small Medkit (68)",
            "classname": "item_health",
            "uuid": 11341754964151860655,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Rocketlauncher (69)",
            "classname": "weapon_rocketlauncher",
            "uuid": 7391094288409747328,
            "mp": 1,
        },
        {
            "id": 70,
            "name": "Yellow Armor (70)",
            "classname": "item_armor2",
            "uuid": 11586231252886671463,
            "mp": 1,
        },
        {
            "id": 71,
            "name": "Supershotgun (71)",
            "classname": "weapon_supershotgun",
            "uuid": 10772300745259767520,
            "mp": 1,
        },
        {
            "id": 72,
            "name": "Red Armor (72)",
            "classname": "item_armorInv",
            "uuid": 16601291460407711285,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Nailgun (73)",
            "classname": "weapon_nailgun",
            "uuid": 4389573227409305766,
            "mp": 1,
        },
        {
            "id": 74,
            "name": "Mjolnir (74)",
            "classname": "weapon_mjolnir",
            "uuid": 11699736919563306276,
            "mp": 1,
        },
        {
            "id": 75,
            "name": "Cells (75)",
            "classname": "item_cells",
            "uuid": 17112294811637336144,
            "mp": 1,
        },
        {
            "id": 76,
            "name": "Cells (76)",
            "classname": "item_cells",
            "uuid": 17333722659639725159,
            "mp": 1,
        },
        {
            "id": 77,
            "name": "Laser (77)",
            "classname": "weapon_laser_gun",
            "uuid": 6698535431422159478,
            "mp": 1,
        },
        {
            "id": 78,
            "name": "Cells (78)",
            "classname": "item_cells",
            "uuid": 16258070448556944945,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Cells (79)",
            "classname": "item_cells",
            "uuid": 6377702319050715475,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Wetsuit (80)",
            "classname": "item_artifact_wetsuit",
            "uuid": 14228916372302851754,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Empathy (81)",
            "classname": "item_artifact_empathy_shields",
            "uuid": 2260892773588494511,
            "mp": 1,
        },
        {
            "id": 82,
            "name": "Proximity (82)",
            "classname": "weapon_proximity_gun",
            "uuid": 10587672312761717432,
            "mp": 1,
        },
        {
            "id": 83,
            "name": "Large Medkit (83)",
            "classname": "item_health",
            "uuid": 2623695703113163387,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Large Medkit (84)",
            "classname": "item_health",
            "uuid": 375389845487640401,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Nailgun (85)",
            "classname": "weapon_nailgun",
            "uuid": 2374613763247474002,
            "mp": 1,
        },
        {
            "id": 86,
            "name": "All Kills (86)",
            "classname": "all_kills",
            "uuid": 14288443555829193077,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Spikes (15)",
                "Rockets (19)",
                "Shells (16)",
                "Supershotgun (7)",
                "Small Medkit (17)",
                "Small Medkit (33)",
                "Shells (46)",
                "Shells (49)",
                "Small Medkit (47)",
                "Small Medkit (48)",
                "Large Medkit (11)",
                "Shells (13)",
                "Grenadelauncher (6)",
                "Large Medkit (12)",
                "Secret (59)",
                "Yellow Armor (58)",
            ],
        )

        self.restrict("Secret (59)", r.can_shootswitch)
        self.restrict("Yellow Armor (58)", r.can_shootswitch)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Shells (51)",
                "Large Medkit (54)",
                "Small Medkit (55)",
                "Small Medkit (56)",
                "Supernailgun (23)",
                "Supershotgun (71)",
                "Small Medkit (22)",
                "Shells (21)",
                "Rockets (52)",
                "Large Medkit (57)",
                "Shells (60)",
                "Large Medkit (38)",
                "Shells (20)",
                "Wetsuit (64)",
                "Rocketlauncher (8)",
                "Spikes (10)",
                "Nailgun (85)",
                "Large Medkit (9)",
                "Megahealth (18)",
                "Secret (39)",
                "Lightning (53)",
                "Silver Key (2)",
                "Secret (32)",
                "Mjolnir (34)",
                "Invulnerability (63)",
                "Secret (3)",
                "Quad Damage (4)",
                "Secret (5)",
                "Red Armor (72)",
                "Rockets (14)",
            ],
        )
        self.connect(ret, past_button_area, r.can_button)

        self.restrict("Megahealth (18)", r.can_shootswitch)
        self.restrict("Secret (5)", r.can_shootswitch)
        self.restrict("Red Armor (72)", r.can_shootswitch)
        self.restrict("Rockets (14)", r.can_shootswitch)

        self.restrict(
            "Secret (39)",
            r.bigjump_hard | (r.can_shootswitch & (r.can_door | r.jump)),
        )
        self.restrict(
            "Lightning (53)",
            r.bigjump_hard | (r.can_shootswitch & (r.can_door | r.jump)),
        )

        self.restrict("Silver Key (2)", r.can_dive & r.can_door)
        self.restrict("Secret (3)", r.can_dive & r.can_door & r.can_shootswitch)
        self.restrict("Quad Damage (4)", r.can_dive & r.can_door & r.can_shootswitch)
        self.restrict("Secret (32)", r.can_dive & r.can_door & r.can_shootswitch)
        self.restrict(
            "Mjolnir (34)",
            (r.can_dive & r.can_door & r.can_shootswitch) | r.bigjump_hard,
        )
        self.restrict(
            "Invulnerability (63)", r.can_dive & r.can_door & r.can_shootswitch
        )

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Laser (77)",
                "Cells (79)",
                "Shells (36)",
                "Cells (78)",
                "Large Medkit (35)",
                "Spikes (37)",
                "Large Medkit (61)",
                "Wetsuit (80)",
            ],
        )
        self.connect(past_button_area, past_silver_door_area, self.silver_key)

        silver_dive_area = self.region(
            "Silver Dive Area",
            [
                "Nailgun (73)",
                "Empathy (81)",
                "Large Medkit (44)",
                "Rockets (45)",
                "Shells (27)",
                "Shells (42)",
                "Cells (76)",
                "Gold Key (1)",
                "Mjolnir (74)",
                "Cells (75)",
                "Spikes (41)",
                "Spikes (40)",
                "Large Medkit (43)",
                "Spikes (26)",
                "Proximity (82)",
                "Large Medkit (24)",
                "Large Medkit (25)",
            ],
        )
        self.connect(past_silver_door_area, silver_dive_area, r.can_dive)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Shells (62)",
                "Spikes (28)",
                "Yellow Armor (70)",
                "Large Medkit (83)",
                "Large Medkit (84)",
                "Shells (31)",
                "Rockets (66)",
                "Rockets (65)",
                "Small Medkit (67)",
                "Small Medkit (68)",
                "Rocketlauncher (69)",
                "Exit",
                "Secret (30)",
                "Invisibility (29)",
                "All Kills (86)",
            ],
        )
        self.connect(past_button_area, past_gold_door_area, self.gold_key)

        self.restrict(
            "All Kills (86)", self.silver_key & r.can_dive & r.difficult_combat
        )

        self.restrict("Secret (30)", r.can_shootswitch)
        self.restrict("Invisibility (29)", r.can_shootswitch)

        return ret
