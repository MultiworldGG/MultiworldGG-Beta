from BaseClasses import Region

from ..base_classes import Q1Level


class e5m7(Q1Level):
    name = "The Otherworld"
    mapfile = "e5m7"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Silver Key (1)",
            "classname": "item_key1",
            "uuid": 7362456093723451560,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Supershotgun (2)",
            "classname": "weapon_supershotgun",
            "uuid": 12314871658695082755,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Rocketlauncher (3)",
            "classname": "weapon_rocketlauncher",
            "uuid": 16341702883931823681,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Green Armor (4)",
            "classname": "item_armor1",
            "uuid": 9021829808791500473,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Rockets (5)",
            "classname": "item_rockets",
            "uuid": 8705182646144336637,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Rockets (6)",
            "classname": "item_rockets",
            "uuid": 7970184732550852203,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Spikes (7)",
            "classname": "item_spikes",
            "uuid": 4009534444195631446,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Small Medkit (8)",
            "classname": "item_health",
            "uuid": 17472945462417707826,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Small Medkit (9)",
            "classname": "item_health",
            "uuid": 3644381066833783707,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 2304732312834379476,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Spikes (11)",
            "classname": "item_spikes",
            "uuid": 654415519964396787,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Spikes (12)",
            "classname": "item_spikes",
            "uuid": 17699628359265231617,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Supernailgun (13)",
            "classname": "weapon_supernailgun",
            "uuid": 9389689033374251316,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 6707505873101956961,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 10855078082064969645,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Gold Key (16)",
            "classname": "item_key2",
            "uuid": 10999632342530962580,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 8095670766395169927,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Small Medkit (18)",
            "classname": "item_health",
            "uuid": 1649814958625123233,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Lightning (19)",
            "classname": "weapon_lightning",
            "uuid": 10668348898670356914,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rockets (20)",
            "classname": "item_rockets",
            "uuid": 2051587501778022567,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Yellow Armor (21)",
            "classname": "item_armor2",
            "uuid": 15954241699097675264,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Shells (22)",
            "classname": "item_shells",
            "uuid": 5039035758422268559,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Shells (23)",
            "classname": "item_shells",
            "uuid": 14135286533983114069,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Secret (24)",
            "classname": "trigger_secret",
            "uuid": 11603072377692013278,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Quad Damage (25)",
            "classname": "item_artifact_super_damage",
            "uuid": 17271175813949071885,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 13032122757544127103,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Spikes (27)",
            "classname": "item_spikes",
            "uuid": 16085616560686924833,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 17386162014008695560,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 1486946963646815210,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 9780466503878980257,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 15397274425293833573,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Cells (32)",
            "classname": "item_cells",
            "uuid": 13413728116048067205,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Large Medkit (33)",
            "classname": "item_health",
            "uuid": 17410787313208217647,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Secret (34)",
            "classname": "trigger_secret",
            "uuid": 8159805314941740806,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 13041668270833827186,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Shells (36)",
            "classname": "item_shells",
            "uuid": 4342946518430395083,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Small Medkit (37)",
            "classname": "item_health",
            "uuid": 11559943932275008223,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 2367430063444811147,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Large Medkit (39)",
            "classname": "item_health",
            "uuid": 9585456724295659467,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Megahealth (40)",
            "classname": "item_health",
            "uuid": 12486886900699487898,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Green Armor (41)",
            "classname": "item_armor1",
            "uuid": 12602943742245445710,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Secret (42)",
            "classname": "trigger_secret",
            "uuid": 11889243131491614208,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Grenadelauncher (43)",
            "classname": "weapon_grenadelauncher",
            "uuid": 14259698721856301920,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Spikes (44)",
            "classname": "item_spikes",
            "uuid": 10861448059197238285,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Megahealth (45)",
            "classname": "item_health",
            "uuid": 10697502671896856176,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 11677003329353435304,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 8760138839565521574,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 7308131138029121557,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Shells (49)",
            "classname": "item_shells",
            "uuid": 17191386813031839151,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Shells (50)",
            "classname": "item_shells",
            "uuid": 5061254053686874147,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Secret (51)",
            "classname": "trigger_secret",
            "uuid": 2114825071072988600,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "All Kills (52)",
            "classname": "all_kills",
            "uuid": 16045665076916456503,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Shells (15)",
                "Shells (14)",
            ],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Supershotgun (2)",
                "Silver Key (1)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Rocketlauncher (3)",
                "Rockets (5)",
                "Rockets (6)",
                "Green Armor (4)",
                "Secret (46)",
                "Megahealth (45)",
                "Rockets (47)",
            ],
        )
        self.connect(past_door_area, shootswitch_area, r.can_shootswitch)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Small Medkit (8)",
                "Small Medkit (9)",
                "Spikes (7)",
                "Supernailgun (13)",
                "Spikes (12)",
                "Spikes (11)",
                "Secret (51)",
                "Shells (49)",
                "Shells (50)",
                "Large Medkit (48)",
            ],
        )
        self.connect(shootswitch_area, past_button_area, r.can_button)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Small Medkit (18)",
                "Large Medkit (17)",
                "Gold Key (16)",
                "Grenadelauncher (43)",
                "Secret (42)",
                "Green Armor (41)",
                "Megahealth (40)",
            ],
        )
        self.connect(past_door_area, past_silver_door_area, self.silver_key)

        self.restrict("Secret (42)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Green Armor (41)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Megahealth (40)", r.can_shootswitch | r.bigjump_hard)

        dive_area = self.region(
            "Dive Area",
            [
                "Large Medkit (33)",
                "Rockets (20)",
                "Spikes (38)",
                "Spikes (44)",
                "Secret (34)",
                "Yellow Armor (21)",
                "Shells (35)",
                "Shells (36)",
                "Small Medkit (37)",
            ],
        )
        self.connect(past_silver_door_area, dive_area, r.can_dive)

        past_button_dive_area = self.region(
            "Past Button Dive Area",
            [
                "Large Medkit (39)",
                "Shells (22)",
                "Shells (23)",
                "Secret (24)",
                "Quad Damage (25)",
            ],
        )
        self.connect(dive_area, past_button_dive_area, r.can_button)

        self.restrict(
            "Secret (24)",
            (r.can_shootswitch & (r.can_jump | r.can_rj_hard | r.can_gj_extr))
            | r.bigjump_hard,
        )
        self.restrict(
            "Quad Damage (25)",
            (r.can_shootswitch & (r.can_jump | r.can_rj_hard | r.can_gj_extr))
            | r.bigjump_hard,
        )

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Lightning (19)",
                "Cells (32)",
                "Spikes (26)",
                "Spikes (27)",
                "Shells (31)",
                "Shells (30)",
                "Large Medkit (28)",
                "Large Medkit (29)",
                "Exit",
                "All Kills (52)",
            ],
        )
        self.connect(ret, past_gold_door_area, self.gold_key)
        self.restrict(
            "All Kills (52)",
            self.silver_key
            & r.can_dive
            & r.can_door
            & r.can_button
            & r.difficult_combat,
        )

        return ret
