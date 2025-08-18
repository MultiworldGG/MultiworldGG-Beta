from BaseClasses import Region

from ..base_classes import Q1Level


class e4m1(Q1Level):
    name = "The Sewage System"
    mapfile = "e4m1"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Large Medkit (1)",
            "classname": "item_health",
            "uuid": 7132594547277374166,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Large Medkit (2)",
            "classname": "item_health",
            "uuid": 16352635313599248030,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Spikes (3)",
            "classname": "item_spikes",
            "uuid": 16634528568094003305,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 10826655254934480226,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Megahealth (5)",
            "classname": "item_health",
            "uuid": 15881191443873164432,
            "mp": 1,
        },
        {
            "id": 6,
            "name": "Shells (6)",
            "classname": "item_shells",
            "uuid": 12951672116675753755,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Small Medkit (7)",
            "classname": "item_health",
            "uuid": 9763050775850514908,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Shells (8)",
            "classname": "item_shells",
            "uuid": 8844115622594911122,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Large Medkit (9)",
            "classname": "item_health",
            "uuid": 5855780863277045973,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Gold Key (10)",
            "classname": "item_key2",
            "uuid": 3675073283884618902,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 18031718796071084886,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 15510353585570182368,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Megahealth (13)",
            "classname": "item_health",
            "uuid": 12483084706172775617,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Small Medkit (14)",
            "classname": "item_health",
            "uuid": 3244984565514697441,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Small Medkit (15)",
            "classname": "item_health",
            "uuid": 4010206937848875204,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Nailgun (16)",
            "classname": "weapon_nailgun",
            "uuid": 8314060073568363209,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 2364299471323034123,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 3525207056013501987,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 5530772115389981582,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Spikes (20)",
            "classname": "item_spikes",
            "uuid": 17343134148661379252,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 16792894854297454050,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Secret (22)",
            "classname": "trigger_secret",
            "uuid": 17053051451865467749,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 4537833876636135611,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 12853908263900761446,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Secret (25)",
            "classname": "trigger_secret",
            "uuid": 11110553528781610133,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Yellow Armor (26)",
            "classname": "item_armor2",
            "uuid": 7260437175655548899,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Small Medkit (27)",
            "classname": "item_health",
            "uuid": 5989568045423454142,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Spikes (28)",
            "classname": "item_spikes",
            "uuid": 16765726839905236607,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 5497625931614068642,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Small Medkit (30)",
            "classname": "item_health",
            "uuid": 16670017555035577658,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Spikes (31)",
            "classname": "item_spikes",
            "uuid": 3538383643373976286,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 6109495640324126969,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Yellow Armor (33)",
            "classname": "item_armor2",
            "uuid": 11082918774468293599,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 1025162785863734982,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 1563109665128797850,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Large Medkit (36)",
            "classname": "item_health",
            "uuid": 16791825783624741764,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Spikes (37)",
            "classname": "item_spikes",
            "uuid": 7575129365343261218,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 5890646486411705291,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 17373293200695449568,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Red Armor (40)",
            "classname": "item_armorInv",
            "uuid": 5040501708732388587,
            "mp": 1,
        },
        {
            "id": 41,
            "name": "Grenadelauncher (41)",
            "classname": "weapon_grenadelauncher",
            "uuid": 950574402471909073,
            "mp": 1,
        },
        {
            "id": 42,
            "name": "Rocketlauncher (42)",
            "classname": "weapon_rocketlauncher",
            "uuid": 17966463332681666893,
            "mp": 1,
        },
        {
            "id": 43,
            "name": "Nailgun (43)",
            "classname": "weapon_nailgun",
            "uuid": 15618637858208198733,
            "mp": 1,
        },
        {
            "id": 44,
            "name": "Rockets (44)",
            "classname": "item_rockets",
            "uuid": 7209457317264422438,
            "mp": 1,
        },
        {
            "id": 45,
            "name": "Lightning (45)",
            "classname": "weapon_lightning",
            "uuid": 13500996286903488619,
            "mp": 1,
        },
        {
            "id": 46,
            "name": "Supernailgun (46)",
            "classname": "weapon_supernailgun",
            "uuid": 13594926574861269713,
            "mp": 1,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 2126382142436920890,
            "mp": 1,
        },
        {
            "id": 48,
            "name": "Green Armor (48)",
            "classname": "item_armor1",
            "uuid": 1279203359905440303,
            "mp": 1,
        },
        {
            "id": 49,
            "name": "Quad Damage (49)",
            "classname": "item_artifact_super_damage",
            "uuid": 18182920970464655333,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Quad Damage (50)",
            "classname": "item_artifact_super_damage",
            "uuid": 5066089691463681274,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Large Medkit (51)",
            "classname": "item_health",
            "uuid": 8932248327340766211,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 5381430387611287685,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 5942375302964987521,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 14855266531868964768,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Large Medkit (55)",
            "classname": "item_health",
            "uuid": 12062427995827461212,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Large Medkit (56)",
            "classname": "item_health",
            "uuid": 1364539874994381135,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 6910229280871846237,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 7400680535218420302,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Small Medkit (59)",
            "classname": "item_health",
            "uuid": 3323642700806430650,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 6785562237057170914,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Large Medkit (61)",
            "classname": "item_health",
            "uuid": 3964155852955635342,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Large Medkit (62)",
            "classname": "item_health",
            "uuid": 7143293772245221187,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Biosuit (63)",
            "classname": "item_artifact_envirosuit",
            "uuid": 12541573994439095429,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Large Medkit (64)",
            "classname": "item_health",
            "uuid": 723367897584867259,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Large Medkit (65)",
            "classname": "item_health",
            "uuid": 3830879310262226464,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Small Medkit (66)",
            "classname": "item_health",
            "uuid": 4917332342622371904,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Small Medkit (67)",
            "classname": "item_health",
            "uuid": 11269121687211920487,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Biosuit (68)",
            "classname": "item_artifact_envirosuit",
            "uuid": 17313152375725691934,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Large Medkit (69)",
            "classname": "item_health",
            "uuid": 4048764863242650418,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Large Medkit (70)",
            "classname": "item_health",
            "uuid": 7765203352928696764,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Spikes (71)",
            "classname": "item_spikes",
            "uuid": 16795069444196991756,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Invulnerability (72)",
            "classname": "item_artifact_invulnerability",
            "uuid": 18362524322063983332,
            "mp": 1,
        },
        {
            "id": 73,
            "name": "Supershotgun (73)",
            "classname": "weapon_supershotgun",
            "uuid": 11527588278303808362,
            "mp": 1,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 11406041997149617536,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Shells (75)",
            "classname": "item_shells",
            "uuid": 5555238756745767680,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Shells (76)",
            "classname": "item_shells",
            "uuid": 13932357017201648844,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Large Medkit (77)",
            "classname": "item_health",
            "uuid": 7207473998790924447,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Spikes (78)",
            "classname": "item_spikes",
            "uuid": 15990183755453215974,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Invisibility (79)",
            "classname": "item_artifact_invisibility",
            "uuid": 1041207459903093010,
            "mp": 1,
        },
        {
            "id": 80,
            "name": "Secret (80)",
            "classname": "trigger_secret",
            "uuid": 9301485794535011264,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Green Armor (81)",
            "classname": "item_armor1",
            "uuid": 1236350357210915656,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "All Kills (82)",
            "classname": "all_kills",
            "uuid": 6465982793973390474,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Shells (11)",
                "Green Armor (81)",
                "Invisibility (79)",
                "Large Medkit (4)",
                "Large Medkit (34)",
                "Large Medkit (35)",
                "Biosuit (68)",
                "Rockets (44)",
                "Shells (6)",
                "Small Medkit (7)",
                "Large Medkit (58)",
                "Yellow Armor (33)",
                "Large Medkit (32)",
            ],
        )

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Spikes (20)",
                "Supernailgun (46)",
                "Large Medkit (52)",
                "Large Medkit (51)",
                "Small Medkit (14)",
                "Small Medkit (15)",
                "Large Medkit (38)",
                "Large Medkit (53)",
                "Large Medkit (54)",
                "Lightning (45)",
                "Spikes (28)",
                "Spikes (78)",
                "Rockets (47)",
            ],
        )
        # drop from above to top floor with airstrafes
        self.connect(ret, past_gold_door_area, self.gold_key | r.difficulty("extreme"))
        self.restrict("Spikes (20)", r.can_door)
        self.restrict("Supernailgun (46)", r.can_door)
        self.restrict("Large Medkit (52)", r.can_door)
        self.restrict("Large Medkit (51)", r.can_door)

        button_secret_area = self.region(
            "Button Secret",
            [
                "Secret (22)",
                "Quad Damage (49)",
                "Megahealth (13)",
                "Green Armor (48)",
            ],
        )
        self.connect(
            past_gold_door_area,
            button_secret_area,
            (r.can_button & r.jump) | (r.jump & r.difficulty("hard")),
        )

        dive_area = self.region(
            "Dive Area",
            [
                "Megahealth (5)",
                "Large Medkit (55)",
                "Large Medkit (56)",
                "Large Medkit (64)",
                "Large Medkit (65)",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)

        lower_gate_area = self.region(
            "Lower Gate Area",
            [
                "Spikes (24)",
                "Large Medkit (23)",
                "Spikes (37)",
                "Supershotgun (73)",
                "Shells (8)",
                "Large Medkit (77)",
                "Large Medkit (21)",
            ],
        )
        self.connect(dive_area, lower_gate_area)

        past_gate_area = self.region(
            "Past Gate",
            [
                "Small Medkit (27)",
                "Large Medkit (36)",
                "Nailgun (43)",
                "Large Medkit (12)",
                "Shells (76)",
                "Large Medkit (29)",
                "Small Medkit (30)",
                "Gold Key (10)",
                "Spikes (19)",
                "Large Medkit (18)",
                "Large Medkit (17)",
                "Nailgun (16)",
                "Rocketlauncher (42)",
                "Quad Damage (50)",
                "Secret (25)",
                "Yellow Armor (26)",
            ],
        )

        self.connect(past_gate_area, lower_gate_area)

        self.connect(
            dive_area, past_gate_area, r.can_door | (r.jump & r.difficulty("hard"))
        )
        self.connect(ret, past_gate_area, r.bigjump_hard)
        self.restrict("Large Medkit (36)", r.can_door)
        self.restrict("Quad Damage (50)", r.can_shootswitch)
        self.restrict("Secret (25)", r.can_shootswitch)
        self.restrict("Yellow Armor (26)", r.can_shootswitch)

        past_button_area = self.region(
            "Past Button",
            [
                "Large Medkit (69)",
                "Large Medkit (70)",
                "Large Medkit (1)",
                "Large Medkit (2)",
                "Grenadelauncher (41)",
                "Spikes (3)",
                "Spikes (74)",
                "Large Medkit (9)",
                "Biosuit (63)",
                "Invulnerability (72)",
                "Spikes (71)",
                "Small Medkit (66)",
                "Small Medkit (67)",
                "Large Medkit (61)",
                "Large Medkit (62)",
                "Shells (60)",
                "Small Medkit (59)",
                "Secret (80)",
                "Red Armor (40)",
                "Spikes (31)",
                "Secret (39)",
                "Exit",
                "All Kills (82)",
            ],
        )
        self.connect(past_gold_door_area, past_button_area, r.can_button & r.can_dive)
        self.restrict("Spikes (31)", r.can_shootswitch)
        self.restrict("Secret (39)", r.can_shootswitch)
        self.restrict(
            "All Kills (82)",
            # past gold door
            (self.gold_key | r.difficulty("extreme"))
            # upper area
            & (r.can_door | (r.jump & r.difficulty("hard"))) & r.backpack(5),
        )

        return ret
