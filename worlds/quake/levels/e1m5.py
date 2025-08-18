from BaseClasses import Region

from ..base_classes import Q1Level


class e1m5(Q1Level):
    name = "Gloom Keep"
    mapfile = "e1m5"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Gold Key (1)",
            "classname": "item_key2",
            "uuid": 16125560866177265702,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Yellow Armor (2)",
            "classname": "item_armor2",
            "uuid": 4439364383753501467,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Large Medkit (3)",
            "classname": "item_health",
            "uuid": 13676195733289562831,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 9430958294397743102,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 6914799088154629961,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Small Medkit (6)",
            "classname": "item_health",
            "uuid": 5621620531337265267,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Small Medkit (7)",
            "classname": "item_health",
            "uuid": 11274873497183738128,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Small Medkit (8)",
            "classname": "item_health",
            "uuid": 6137761139936239883,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Small Medkit (9)",
            "classname": "item_health",
            "uuid": 9311104331202880245,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Grenadelauncher (10)",
            "classname": "weapon_grenadelauncher",
            "uuid": 7129365745165262439,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Nailgun (11)",
            "classname": "weapon_nailgun",
            "uuid": 2724088314546284886,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 5209494184718020690,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Large Medkit (13)",
            "classname": "item_health",
            "uuid": 9672859640803729669,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Large Medkit (14)",
            "classname": "item_health",
            "uuid": 16452644289304644313,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 9557127226453674183,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Small Medkit (16)",
            "classname": "item_health",
            "uuid": 9575453178057052322,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 15124556659184597908,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Shells (18)",
            "classname": "item_shells",
            "uuid": 10201524212019655495,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 3790485498214079999,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 11881329695690303825,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Shells (21)",
            "classname": "item_shells",
            "uuid": 9485705975665738558,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Small Medkit (22)",
            "classname": "item_health",
            "uuid": 7921207933775763948,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Spikes (23)",
            "classname": "item_spikes",
            "uuid": 13865828649245916789,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Rockets (24)",
            "classname": "item_rockets",
            "uuid": 16542567639201206680,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 5059523311456498747,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Large Medkit (26)",
            "classname": "item_health",
            "uuid": 15391240661707346890,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Shells (27)",
            "classname": "item_shells",
            "uuid": 8186220700088675844,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 14962382095534004234,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 4134996187644415436,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Large Medkit (30)",
            "classname": "item_health",
            "uuid": 16674345337688825537,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Small Medkit (31)",
            "classname": "item_health",
            "uuid": 14933063416312295626,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Small Medkit (32)",
            "classname": "item_health",
            "uuid": 16175530335691364581,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Large Medkit (33)",
            "classname": "item_health",
            "uuid": 7710876860415603887,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 6868741013602554859,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 18125714888217711559,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Rockets (36)",
            "classname": "item_rockets",
            "uuid": 423844409680717847,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Small Medkit (37)",
            "classname": "item_health",
            "uuid": 15432605283096712339,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Supershotgun (38)",
            "classname": "weapon_supershotgun",
            "uuid": 8139636666606980991,
            "mp": 1,
        },
        {
            "id": 39,
            "name": "Small Medkit (39)",
            "classname": "item_health",
            "uuid": 15851277072435615131,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Supernailgun (40)",
            "classname": "weapon_supernailgun",
            "uuid": 2122669380208200821,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Silver Key (41)",
            "classname": "item_key1",
            "uuid": 1948330678978844801,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 15348254036519729943,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 3577536244342448785,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Large Medkit (44)",
            "classname": "item_health",
            "uuid": 1318155809184769570,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Spikes (45)",
            "classname": "item_spikes",
            "uuid": 15817063558832744433,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Large Medkit (46)",
            "classname": "item_health",
            "uuid": 9388215241386223388,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 13255782976830225711,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Rocketlauncher (48)",
            "classname": "weapon_rocketlauncher",
            "uuid": 13419416781977565084,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 17548666794220537111,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Secret (50)",
            "classname": "trigger_secret",
            "uuid": 3882395843062441283,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Secret (51)",
            "classname": "trigger_secret",
            "uuid": 2565855567793439803,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 16583346295877223577,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 301662791857612574,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 13201081895517365464,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Spikes (55)",
            "classname": "item_spikes",
            "uuid": 12161159763028636141,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Shells (56)",
            "classname": "item_shells",
            "uuid": 12526083073198454621,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 7785049704763318039,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 11928329585272949280,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Large Medkit (59)",
            "classname": "item_health",
            "uuid": 14260551968354718264,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Spikes (60)",
            "classname": "item_spikes",
            "uuid": 18283767867220508142,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Spikes (61)",
            "classname": "item_spikes",
            "uuid": 9267847188991342944,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Yellow Armor (62)",
            "classname": "item_armor2",
            "uuid": 9089730518831181197,
            "mp": 1,
        },
        {
            "id": 63,
            "name": "Secret (63)",
            "classname": "trigger_secret",
            "uuid": 8654329511783467975,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Megahealth (64)",
            "classname": "item_health",
            "uuid": 15522018032547947515,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 1862089794509786858,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Shells (66)",
            "classname": "item_shells",
            "uuid": 18365763068738290690,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Spikes (67)",
            "classname": "item_spikes",
            "uuid": 14240757387408436411,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Shells (68)",
            "classname": "item_shells",
            "uuid": 3450856927319234844,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Rockets (69)",
            "classname": "item_rockets",
            "uuid": 3981675936910846738,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Spikes (70)",
            "classname": "item_spikes",
            "uuid": 5105299062601165163,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 3886694589111334563,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Large Medkit (72)",
            "classname": "item_health",
            "uuid": 3724969208392246238,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Spikes (73)",
            "classname": "item_spikes",
            "uuid": 3393593808837451177,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 8892333215912321862,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Green Armor (75)",
            "classname": "item_armor1",
            "uuid": 6259074625855650837,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Shells (76)",
            "classname": "item_shells",
            "uuid": 2368887189189681444,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Quad Damage (77)",
            "classname": "item_artifact_super_damage",
            "uuid": 1019938406637218827,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Yellow Armor (78)",
            "classname": "item_armor2",
            "uuid": 16440388243145497696,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Secret (79)",
            "classname": "trigger_secret",
            "uuid": 12764063929447562625,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Small Medkit (80)",
            "classname": "item_health",
            "uuid": 8604580800665489248,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Shells (81)",
            "classname": "item_shells",
            "uuid": 2548148555474967594,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Rockets (82)",
            "classname": "item_rockets",
            "uuid": 11285148164292377951,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Large Medkit (83)",
            "classname": "item_health",
            "uuid": 7844210974539422085,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Small Medkit (84)",
            "classname": "item_health",
            "uuid": 9638935129971060219,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Secret (85)",
            "classname": "trigger_secret",
            "uuid": 18351153984695979974,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "All Kills (86)",
            "classname": "all_kills",
            "uuid": 9108454064193211222,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (54)",
                "Large Medkit (53)",
                "Shells (35)",
                "Large Medkit (83)",
                "Shells (28)",
                "Large Medkit (49)",
                "Rocketlauncher (48)",
                "Rockets (82)",
                "Small Medkit (84)",
                "Small Medkit (22)",
                "Shells (21)",
                "Shells (17)",
                "Large Medkit (30)",
                "Large Medkit (29)",
                "Nailgun (11)",
                "Large Medkit (13)",
                "Large Medkit (12)",
                "Yellow Armor (62)",
                "Shells (65)",
                "Spikes (42)",
                "Shells (56)",
                "Small Medkit (16)",
                "Large Medkit (14)",
                "Large Medkit (15)",
                "Rockets (24)",
                "Spikes (45)",
                "Large Medkit (44)",
                "Supershotgun (38)",
                "Shells (76)",
                "Small Medkit (32)",
                "Small Medkit (31)",
                "Shells (81)",
                "Spikes (23)",
                "Grenadelauncher (10)",
                "Large Medkit (20)",
                "Large Medkit (19)",
                "Rockets (36)",
                "Shells (18)",
                "Supernailgun (40)",
                "Large Medkit (43)",
                "Spikes (55)",
                "Small Medkit (7)",
                "Small Medkit (8)",
                "Small Medkit (9)",
                "Rockets (69)",
            ],
        )

        underwater_cave_area = self.region(
            "Underwater Cave Secret Area",
            [
                "Secret (63)",
                "Megahealth (64)",
                "Spikes (70)",
            ],
        )
        self.connect(ret, underwater_cave_area, r.can_dive)

        tower_secret_area = self.region(
            "Tower Secret Area",
            [
                "Secret (50)",
                "Shells (66)",
                "Spikes (67)",
                "Quad Damage (77)",
            ],
        )
        self.connect(ret, tower_secret_area, r.bigjump | r.can_door)

        inside_secrets_area = self.region(
            "Inside Secrets Area",
            [
                "Secret (51)",
                "Yellow Armor (78)",
                "Small Medkit (80)",
                "Silver Key (41)",
            ],
        )
        self.connect(ret, inside_secrets_area)
        self.restrict("Small Medkit (80)", r.can_door)
        self.restrict(
            "Yellow Armor (78)",
            r.jump & r.can_button,
        )
        self.restrict(
            "Secret (51)",
            r.jump & r.can_button,
        )
        self.restrict("Silver Key (41)", r.bigjump_hard | r.can_button)

        inside_jump_secret_area = self.region(
            "Inside Jump Secret Area",
            [
                "Secret (85)",
                "Yellow Armor (2)",
                "Shells (57)",
            ],
        )
        self.connect(
            ret,
            inside_jump_secret_area,
            (r.bigjump & r.difficulty("medium"))
            | r.can_jump
            | r.can_rj_hard
            | r.can_gj_extr,
        )

        inside_portal_area = self.region(
            "Inside Portal Area",
            [
                "Gold Key (1)",
                "Large Medkit (4)",
                "Large Medkit (3)",
            ],
        )
        self.connect(ret, inside_portal_area)
        self.restrict("Supernailgun (40)", r.can_button | r.bigjump_hard)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Large Medkit (46)",
                "Shells (68)",
                "Shells (5)",
                "Spikes (60)",
                "Spikes (61)",
                "Small Medkit (6)",
                "Large Medkit (47)",
                "Large Medkit (71)",
                "Large Medkit (72)",
                "Spikes (73)",
                "Spikes (74)",
                "Large Medkit (58)",
                "Large Medkit (59)",
                "Large Medkit (25)",
                "Large Medkit (26)",
                "Shells (27)",
                "Small Medkit (37)",
            ],
        )

        self.connect(inside_portal_area, past_button_area, r.can_button)
        self.restrict("Small Medkit (37)", r.can_door)

        past_elevator_area = self.region(
            "Past Elevator Area",
            [
                "Shells (34)",
                "Large Medkit (33)",
            ],
        )
        self.connect(
            ret,
            past_elevator_area,
            # maybe medium difficulty jump?
            self.silver_key | r.bigjump_hard,
        )

        past_gold_key_door_area = self.region(
            "Past Gold Key Door Area",
            [
                "Small Medkit (39)",
                "Secret (79)",
                "Green Armor (75)",
                "Exit",
                "All Kills (86)",
            ],
        )
        self.connect(past_elevator_area, past_gold_key_door_area, self.gold_key)

        self.restrict("Secret (79)", r.can_shootswitch)
        self.restrict("Green Armor (75)", r.can_shootswitch)

        self.restrict("All Kills (86)", r.backpack(5))

        return ret
