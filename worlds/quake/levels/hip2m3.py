from BaseClasses import Region

from ..base_classes import Q1Level


class hip2m3(Q1Level):
    name = "The Catacombs"
    mapfile = "hip2m3"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Red Armor (1)",
            "classname": "item_armorInv",
            "uuid": 15823190502636151865,
            "mp": 1,
        },
        {
            "id": 2,
            "name": "Spikes (2)",
            "classname": "item_spikes",
            "uuid": 18059727873835761682,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Small Medkit (3)",
            "classname": "item_health",
            "uuid": 6442578964485443617,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Silver Key (4)",
            "classname": "item_key1",
            "uuid": 13296311409379557689,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Supernailgun (5)",
            "classname": "weapon_supernailgun",
            "uuid": 4036269813481742242,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 372163639618700326,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 2035138029206480093,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Shells (8)",
            "classname": "item_shells",
            "uuid": 10022654113632817569,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Megahealth (9)",
            "classname": "item_health",
            "uuid": 3303664217642425782,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Secret (10)",
            "classname": "trigger_secret",
            "uuid": 5559943787532936301,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Spikes (11)",
            "classname": "item_spikes",
            "uuid": 11984792095226875031,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Megahealth (12)",
            "classname": "item_health",
            "uuid": 7120475074688157206,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Rockets (13)",
            "classname": "item_rockets",
            "uuid": 12240610071451489730,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Spikes (14)",
            "classname": "item_spikes",
            "uuid": 9791277026819861528,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 1613387368437346564,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Spikes (16)",
            "classname": "item_spikes",
            "uuid": 2125600035387386822,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 6475006729479234696,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 4968551791578861523,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 9787992370405726304,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Cells (20)",
            "classname": "item_cells",
            "uuid": 17271302794762526936,
            "mp": 1,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 10948663210326296389,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 800174257119892661,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Cells (23)",
            "classname": "item_cells",
            "uuid": 16421500964406619881,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Secret (24)",
            "classname": "trigger_secret",
            "uuid": 1634206227959730325,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Spikes (25)",
            "classname": "item_spikes",
            "uuid": 9470574977405516876,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Large Medkit (26)",
            "classname": "item_health",
            "uuid": 8112331880544740689,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Rockets (27)",
            "classname": "item_rockets",
            "uuid": 1171087408104563676,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Rockets (28)",
            "classname": "item_rockets",
            "uuid": 8121593267027986559,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 10453877798729337760,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 18228203895326536386,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 47438321439825607,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Spikes (32)",
            "classname": "item_spikes",
            "uuid": 8530241491419859495,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Spikes (33)",
            "classname": "item_spikes",
            "uuid": 6464230079631540767,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Rockets (34)",
            "classname": "item_rockets",
            "uuid": 4768948216295223541,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Gold Key (35)",
            "classname": "item_key2",
            "uuid": 7487343033480619459,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Lightning (36)",
            "classname": "weapon_lightning",
            "uuid": 7944468850101846910,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 4780082808915794301,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Rocketlauncher (38)",
            "classname": "weapon_rocketlauncher",
            "uuid": 7466323825700886750,
            "mp": 1,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 3919932588222073893,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Laser (40)",
            "classname": "weapon_laser_gun",
            "uuid": 3178005388528432218,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Cells (41)",
            "classname": "item_cells",
            "uuid": 7163553445113045448,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Supershotgun (42)",
            "classname": "weapon_supershotgun",
            "uuid": 17720419094687088152,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Rocketlauncher (43)",
            "classname": "weapon_rocketlauncher",
            "uuid": 17870195657258003087,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Cells (44)",
            "classname": "item_cells",
            "uuid": 817730546964219678,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Large Medkit (45)",
            "classname": "item_health",
            "uuid": 8753359392602318547,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Cells (46)",
            "classname": "item_cells",
            "uuid": 3196662661424516770,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 10498928077015236848,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 7774462612504728981,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Secret (49)",
            "classname": "trigger_secret",
            "uuid": 18369516754464748605,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Cells (50)",
            "classname": "item_cells",
            "uuid": 7084761101874790276,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Cells (51)",
            "classname": "item_cells",
            "uuid": 10930258450398332643,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Cells (52)",
            "classname": "item_cells",
            "uuid": 3226597222813568977,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Rockets (53)",
            "classname": "item_rockets",
            "uuid": 3364083815210058761,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Rockets (54)",
            "classname": "item_rockets",
            "uuid": 8481368149362294344,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Yellow Armor (55)",
            "classname": "item_armor2",
            "uuid": 446865717219555834,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Large Medkit (56)",
            "classname": "item_health",
            "uuid": 15673751017391714011,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Large Medkit (57)",
            "classname": "item_health",
            "uuid": 14710516496706539765,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 16403827032665616444,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Spikes (59)",
            "classname": "item_spikes",
            "uuid": 4122440826797214010,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 11200674665514818564,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Proximity (61)",
            "classname": "weapon_proximity_gun",
            "uuid": 10381230365117542332,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Megahealth (62)",
            "classname": "item_health",
            "uuid": 5835640613800876492,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Mjolnir (63)",
            "classname": "weapon_mjolnir",
            "uuid": 1777287566458121024,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Empathy (64)",
            "classname": "item_artifact_empathy_shields",
            "uuid": 10415907732819981662,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Cells (65)",
            "classname": "item_cells",
            "uuid": 13059880826764834000,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Large Medkit (66)",
            "classname": "item_health",
            "uuid": 12339125327065610643,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Spikes (67)",
            "classname": "item_spikes",
            "uuid": 7007186217182701629,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Megahealth (68)",
            "classname": "item_health",
            "uuid": 14765734314835689986,
            "mp": 1,
        },
        {
            "id": 69,
            "name": "Megahealth (69)",
            "classname": "item_health",
            "uuid": 1635989179337859232,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Large Medkit (70)",
            "classname": "item_health",
            "uuid": 17973742925545683185,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 18201638566599914803,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Red Armor (72)",
            "classname": "item_armorInv",
            "uuid": 8874348323715116019,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Cells (73)",
            "classname": "item_cells",
            "uuid": 17865721679619184552,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 2162402296378713835,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Rockets (75)",
            "classname": "item_rockets",
            "uuid": 5488512268755278528,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Lightning (76)",
            "classname": "weapon_lightning",
            "uuid": 12382491499721919341,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Mjolnir (77)",
            "classname": "weapon_mjolnir",
            "uuid": 17364924176771248399,
            "mp": 1,
        },
        {
            "id": 78,
            "name": "Rockets (78)",
            "classname": "item_rockets",
            "uuid": 12387402200043956348,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Large Medkit (79)",
            "classname": "item_health",
            "uuid": 4469153872970859701,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Large Medkit (80)",
            "classname": "item_health",
            "uuid": 17097867052310962515,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Large Medkit (81)",
            "classname": "item_health",
            "uuid": 13050356263226666239,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Megahealth (82)",
            "classname": "item_health",
            "uuid": 3852890918270914388,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Spikes (83)",
            "classname": "item_spikes",
            "uuid": 6140849682158547064,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Shells (84)",
            "classname": "item_shells",
            "uuid": 6045809983446803883,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Yellow Armor (85)",
            "classname": "item_armor2",
            "uuid": 17981627100934815925,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 4897198961965516524,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Hornofconjuring (87)",
            "classname": "item_hornofconjuring",
            "uuid": 12675231819382488977,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Quad Damage (88)",
            "classname": "item_artifact_super_damage",
            "uuid": 8220140367023946918,
            "mp": 1,
        },
        {
            "id": 89,
            "name": "Invulnerability (89)",
            "classname": "item_artifact_invulnerability",
            "uuid": 16630604409495472621,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Grenadelauncher (90)",
            "classname": "weapon_grenadelauncher",
            "uuid": 15716126382515741490,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Red Armor (91)",
            "classname": "item_armorInv",
            "uuid": 12618315209874590463,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Rockets (92)",
            "classname": "item_rockets",
            "uuid": 15540915871457598154,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Cells (93)",
            "classname": "item_cells",
            "uuid": 1080038618794841692,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Rockets (94)",
            "classname": "item_rockets",
            "uuid": 16787307468249596954,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Large Medkit (95)",
            "classname": "item_health",
            "uuid": 10974641723972327222,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "Large Medkit (96)",
            "classname": "item_health",
            "uuid": 9122472780279721908,
            "mp": 0,
        },
        {
            "id": 97,
            "name": "Large Medkit (97)",
            "classname": "item_health",
            "uuid": 2777552634077723753,
            "mp": 0,
        },
        {
            "id": 98,
            "name": "Cells (98)",
            "classname": "item_cells",
            "uuid": 6393066683049356228,
            "mp": 0,
        },
        {
            "id": 99,
            "name": "Shells (99)",
            "classname": "item_shells",
            "uuid": 4938949840158425747,
            "mp": 0,
        },
        {
            "id": 100,
            "name": "Shells (100)",
            "classname": "item_shells",
            "uuid": 15322334394678940923,
            "mp": 0,
        },
        {
            "id": 101,
            "name": "Cells (101)",
            "classname": "item_cells",
            "uuid": 7221408440625681660,
            "mp": 0,
        },
        {
            "id": 102,
            "name": "Shells (102)",
            "classname": "item_shells",
            "uuid": 16578100395368467390,
            "mp": 0,
        },
        {
            "id": 103,
            "name": "Large Medkit (103)",
            "classname": "item_health",
            "uuid": 8324689950450379424,
            "mp": 0,
        },
        {
            "id": 104,
            "name": "Large Medkit (104)",
            "classname": "item_health",
            "uuid": 16684089479641499222,
            "mp": 0,
        },
        {
            "id": 105,
            "name": "All Kills (105)",
            "classname": "all_kills",
            "uuid": 13210782701399484018,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Small Medkit (3)",
                "Cells (41)",
                "Large Medkit (17)",
                "Shells (15)",
                "Cells (98)",
                "Laser (40)",
                "Supershotgun (42)",
                "Large Medkit (47)",
                "Large Medkit (48)",
                "Cells (93)",
                "Cells (44)",
                "Rockets (92)",
                "Rockets (75)",
                "Rocketlauncher (43)",
                "Spikes (74)",
                "Shells (8)",
                "Megahealth (9)",
                "Cells (73)",
                "Rockets (27)",
                "Rockets (94)",
                "Invulnerability (89)",
                "Cells (46)",
                "Large Medkit (96)",
                "Large Medkit (95)",
                "Large Medkit (45)",
                "Cells (51)",
                "Lightning (76)",
                "Cells (52)",
                "Large Medkit (58)",
                "Large Medkit (80)",
                "Rockets (78)",
                "Large Medkit (79)",
                "Red Armor (91)",
                "Secret (49)",
                "Cells (50)",
            ],
        )
        self.restrict("Red Armor (91)", r.jump)
        self.restrict("Secret (49)", r.jump)
        self.restrict("Cells (50)", r.jump)
        # there is a wooden bridge which spawns here on skill 0
        self.restrict("Cells (73)", r.skill_eq(0) | r.jump)
        self.restrict("Rockets (27)", r.skill_eq(0) | r.jump)
        self.restrict("Rockets (94)", r.skill_eq(0) | r.jump)
        self.restrict("Invulnerability (89)", r.skill_eq(0) | r.jump)
        self.restrict("Cells (46)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (96)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (95)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (45)", r.skill_eq(0) | r.jump)
        self.restrict("Cells (51)", r.skill_eq(0) | r.jump)
        self.restrict("Lightning (76)", r.skill_eq(0) | r.jump)
        self.restrict("Cells (52)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (58)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (80)", r.skill_eq(0) | r.jump)
        self.restrict("Rockets (78)", r.skill_eq(0) | r.jump)
        self.restrict("Large Medkit (79)", r.skill_eq(0) | r.jump)
        self.restrict("Red Armor (91)", r.skill_eq(0) | r.jump)
        self.restrict("Secret (49)", r.skill_eq(0) | r.jump)
        self.restrict("Cells (50)", r.skill_eq(0) | r.jump)

        castle_inside_area = self.region(
            "Castle Inside",
            [
                "Rockets (54)",
                "Yellow Armor (55)",
                "Rockets (53)",
                "Shells (99)",
                "Shells (100)",
                "Large Medkit (97)",
                "Large Medkit (57)",
                "Large Medkit (66)",
                "Large Medkit (56)",
                "Shells (30)",
                "Cells (65)",
                "Spikes (2)",
            ],
        )
        self.connect(
            ret, castle_inside_area, r.can_door | (r.jump & r.difficulty("hard"))
        )

        wall_secret_area = self.region(
            "Wall Secret",
            [
                "Secret (10)",
                "Megahealth (69)",
                "Spikes (11)",
                "Supernailgun (5)",
                "Megahealth (68)",
                "Large Medkit (7)",
                "Large Medkit (6)",
            ],
        )
        self.connect(castle_inside_area, wall_secret_area, r.can_button & r.jump)

        castle_upper_area = self.region(
            "Castle Upper",
            [
                "Hornofconjuring (87)",
                "Quad Damage (88)",
                "Spikes (59)",
                "Shells (60)",
                "Proximity (61)",
                "Large Medkit (70)",
                "Large Medkit (71)",
                "Spikes (16)",
                "Spikes (67)",
                "Grenadelauncher (90)",
            ],
        )
        self.connect(castle_inside_area, castle_upper_area, r.can_door)
        self.connect(castle_inside_area, castle_upper_area, r.bigjump_hard)

        sewer_area = self.region(
            "Sewer Area",
            [
                "Secret (39)",
                "Megahealth (12)",
            ],
        )
        self.connect(castle_upper_area, sewer_area, r.can_button)
        self.restrict("Secret (39)", r.can_shootswitch)
        self.restrict("Megahealth (12)", r.can_shootswitch)

        sewer_past_door_area = self.region(
            "Sewer Past Door",
            [
                "Silver Key (4)",
                "Red Armor (1)",
                "Spikes (33)",
                "Large Medkit (29)",
                "Large Medkit (26)",
                "Megahealth (62)",
                "Large Medkit (19)",
                "Rockets (28)",
            ],
        )
        self.connect(sewer_area, sewer_past_door_area, r.can_door)
        self.connect(castle_upper_area, sewer_past_door_area, r.bigjump_hard)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Spikes (14)",
                "Rockets (13)",
                "Red Armor (72)",
                "Large Medkit (21)",
                "Cells (20)",
                "Large Medkit (103)",
                "Large Medkit (104)",
                "Cells (101)",
                "Shells (102)",
                "Mjolnir (77)",
                "Secret (24)",
                "Rockets (34)",
                "Large Medkit (31)",
                "Empathy (64)",
            ],
        )
        self.connect(sewer_area, past_silver_door_area, self.silver_key)
        self.connect(sewer_area, past_silver_door_area, r.bigjump_hard)
        self.restrict("Secret (24)", r.jump)
        self.restrict("Rockets (34)", r.jump)
        self.restrict("Large Medkit (31)", r.jump)
        self.restrict("Empathy (64)", r.jump)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (22)",
                "Spikes (25)",
                "Cells (23)",
                "Rocketlauncher (38)",
                "Exit",
            ],
        )
        self.connect(sewer_area, past_gold_door_area, self.gold_key)

        lava_area = self.region(
            "Lava Area",
            [
                "Mjolnir (63)",
                "Large Medkit (18)",
                "Spikes (32)",
            ],
        )
        self.connect(past_silver_door_area, lava_area, r.jump | r.can_button)

        lava_jump_area = self.region(
            "Lava Jump Area",
            [
                "Spikes (83)",
                "Large Medkit (81)",
                "Yellow Armor (85)",
                "Megahealth (82)",
                "Shells (84)",
                "Large Medkit (37)",
                "Lightning (36)",
                "Gold Key (35)",
                "All Kills (105)",
            ],
        )
        self.connect(
            lava_area, lava_jump_area, r.can_jump | r.can_rj_hard | r.can_gj_extr
        )
        self.restrict("All Kills (105)", r.difficult_combat & self.gold_key)

        return ret
