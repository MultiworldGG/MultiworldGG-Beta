from BaseClasses import Region

from ..base_classes import Q1Level


class mge1m3(Q1Level):
    name = "Sandy's Room"
    mapfile = "mge1m3"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Secret (1)",
            "classname": "trigger_secret",
            "uuid": 13944246476474026735,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Secret (2)",
            "classname": "trigger_secret",
            "uuid": 17267498245802922435,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 18290416896128442572,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Silver Key (4)",
            "classname": "item_key1",
            "uuid": 18382046792216814063,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 12488439080452572816,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 5587560923286767517,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Shells (7)",
            "classname": "item_shells",
            "uuid": 2895282950948205060,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Supershotgun (8)",
            "classname": "weapon_supershotgun",
            "uuid": 14092187543601739627,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 15152513875910962358,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Large Medkit (10)",
            "classname": "item_health",
            "uuid": 14229118384935244879,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 7536059295424821244,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Spikes (12)",
            "classname": "item_spikes",
            "uuid": 15673664140223687252,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Spikes (13)",
            "classname": "item_spikes",
            "uuid": 4359664596894912553,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 14804688345448209252,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 1336268205483624856,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Nailgun (16)",
            "classname": "weapon_nailgun",
            "uuid": 7663226349778655737,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Grenadelauncher (17)",
            "classname": "weapon_grenadelauncher",
            "uuid": 8741337901999560676,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Gold Key (18)",
            "classname": "item_key2",
            "uuid": 4676969843977041666,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Lightning (19)",
            "classname": "weapon_lightning",
            "uuid": 17491717148298091649,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rockets (20)",
            "classname": "item_rockets",
            "uuid": 7902604290717164507,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Rockets (21)",
            "classname": "item_rockets",
            "uuid": 7893371921082094362,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Rockets (22)",
            "classname": "item_rockets",
            "uuid": 2756939334713489811,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 2982199053111344590,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Megahealth (24)",
            "classname": "item_health",
            "uuid": 14597159699518639170,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 9438242707726556726,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Shells (26)",
            "classname": "item_shells",
            "uuid": 16133404516683582115,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 4707752928615758264,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Green Armor (28)",
            "classname": "item_armor1",
            "uuid": 12363209196872448785,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 7832361075532443506,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 3464737365549555637,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Spikes (31)",
            "classname": "item_spikes",
            "uuid": 12614192635371393706,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Spikes (32)",
            "classname": "item_spikes",
            "uuid": 14796695794823189016,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Large Medkit (33)",
            "classname": "item_health",
            "uuid": 17691741957770429400,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 15842031968403049666,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 17470019395414596338,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 7451003438462570432,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Shells (37)",
            "classname": "item_shells",
            "uuid": 1066845128425731239,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 3808312615535844963,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Shells (39)",
            "classname": "item_shells",
            "uuid": 10458724388773652788,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 3591545606893533975,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Shells (41)",
            "classname": "item_shells",
            "uuid": 482561202969134034,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 725524784985680166,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Supernailgun (43)",
            "classname": "weapon_supernailgun",
            "uuid": 16088396203359728992,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Cells (44)",
            "classname": "item_cells",
            "uuid": 14037099262294456427,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Cells (45)",
            "classname": "item_cells",
            "uuid": 16724730807631053031,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 16746935760910347421,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Megahealth (47)",
            "classname": "item_health",
            "uuid": 15901561995583003981,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 13679833146283170007,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 16520794047954705442,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Large Medkit (50)",
            "classname": "item_health",
            "uuid": 10802835368505820176,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Large Medkit (51)",
            "classname": "item_health",
            "uuid": 9399741815602677762,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 16374414092485535862,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 558712954563436450,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Spikes (54)",
            "classname": "item_spikes",
            "uuid": 7777711880421007306,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 469414890828644916,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Rockets (56)",
            "classname": "item_rockets",
            "uuid": 3057702168622916854,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Rockets (57)",
            "classname": "item_rockets",
            "uuid": 18300764329633105088,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Rockets (58)",
            "classname": "item_rockets",
            "uuid": 11033640208132561242,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Megahealth (59)",
            "classname": "item_health",
            "uuid": 10873680471356485592,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 7927117338886022738,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Shells (61)",
            "classname": "item_shells",
            "uuid": 1812369758600198988,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 10767501178497487259,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Secret (63)",
            "classname": "trigger_secret",
            "uuid": 3047379449048972933,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Rockets (64)",
            "classname": "item_rockets",
            "uuid": 11123341066755816908,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Spikes (65)",
            "classname": "item_spikes",
            "uuid": 11243826083812601829,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Shells (66)",
            "classname": "item_shells",
            "uuid": 5751042155752472918,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Spikes (67)",
            "classname": "item_spikes",
            "uuid": 2341989106233812439,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Small Medkit (68)",
            "classname": "item_health",
            "uuid": 8841910198521409560,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Large Medkit (69)",
            "classname": "item_health",
            "uuid": 6985663571998386562,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Large Medkit (70)",
            "classname": "item_health",
            "uuid": 15383462914857638600,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 11658516365780629275,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Rockets (72)",
            "classname": "item_rockets",
            "uuid": 7433764563799685737,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Shells (73)",
            "classname": "item_shells",
            "uuid": 17920944518657688569,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 6192435362415543016,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "All Kills (75)",
            "classname": "all_kills",
            "uuid": 9096936053200014321,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (8)",
                "Green Armor (28)",
                "Secret (2)",
            ],
        )
        self.restrict(
            "Green Armor (28)", r.can_shootswitch & (r.difficulty("hard") | r.jump)
        )
        self.restrict("Secret (2)", r.can_shootswitch & (r.difficulty("hard") | r.jump))

        past_door_area = self.region(
            "Past Door Area",
            [
                "Shells (7)",
                "Spikes (9)",
                "Nailgun (16)",
                "Large Medkit (6)",
                "Grenadelauncher (17)",
                "Rockets (22)",
                "Rockets (21)",
                "Spikes (54)",
                "Large Medkit (23)",
                "Small Medkit (68)",
                "Shells (41)",
                "Large Medkit (48)",
                "Large Medkit (49)",
                "Large Medkit (50)",
                "Spikes (42)",
                "Large Medkit (51)",
                "Large Medkit (52)",
                "Large Medkit (53)",
                "Megahealth (47)",
                "Secret (46)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)
        self.restrict("Megahealth (47)", r.can_shootswitch & r.jump)
        self.restrict("Secret (46)", r.can_shootswitch & r.jump)

        past_door_upper_area = self.region(
            "Past Door Upper",
            [
                "Silver Key (4)",
                "Shells (39)",
                "Spikes (15)",
                "Large Medkit (10)",
                "Large Medkit (11)",
                "Shells (60)",
            ],
        )
        self.connect(
            past_door_area,
            past_door_upper_area,
            r.bigjump_hard | (r.can_button & r.can_shootswitch),
        )
        self.restrict("Shells (60)", r.can_button)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Megahealth (24)",
                "Spikes (62)",
                "Shells (61)",
                "Spikes (32)",
                "Supernailgun (43)",
                "Shells (66)",
                "Spikes (65)",
                "Shells (29)",
                "Spikes (12)",
                "Large Medkit (25)",
                "Shells (26)",
                "Large Medkit (40)",
                "Large Medkit (27)",
                "Spikes (13)",
                "Shells (14)",
                "Rockets (64)",
                "Secret (63)",
            ],
        )
        self.connect(ret, past_silver_door_area, self.silver_key)
        self.restrict("Rockets (64)", r.can_shootswitch & r.jump)
        self.restrict("Secret (63)", r.can_shootswitch & r.jump)

        past_silver_button_area = self.region(
            "Past Silver Button Area",
            [
                "Shells (37)",
                "Spikes (38)",
            ],
        )
        self.connect(past_silver_door_area, past_silver_button_area, r.can_button)

        past_silver_jump_area = self.region(
            "Past Silver Jump Area",
            [
                "Large Medkit (69)",
                "Large Medkit (70)",
                "Large Medkit (71)",
                "Rockets (72)",
                "Rockets (20)",
                "Gold Key (18)",
                "Shells (73)",
                "Spikes (74)",
                "Shells (35)",
                "Spikes (36)",
                "Large Medkit (34)",
                "Large Medkit (33)",
                "Lightning (19)",
                "Secret (1)",
                "Cells (45)",
                "Rockets (56)",
                "Megahealth (59)",
            ],
        )
        self.connect(past_silver_button_area, past_silver_jump_area, r.jump)
        self.connect(past_silver_door_area, past_silver_jump_area, r.bigjump_hard)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Spikes (67)",
                "Shells (55)",
                "Spikes (31)",
                "Rockets (57)",
                "Rockets (58)",
                "Shells (30)",
                "Exit",
                "All Kills (75)",
            ],
        )
        self.connect(past_silver_door_area, past_gold_door_area, self.gold_key)
        self.restrict("Exit", r.can_button)
        self.restrict("All Kills (75)", r.difficult_combat)

        return ret
