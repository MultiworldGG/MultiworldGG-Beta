from BaseClasses import Region

from ..base_classes import Q1Level


class e5m6(Q1Level):
    name = "The Underworld"
    mapfile = "e5m6"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Silver Key (1)",
            "classname": "item_key1",
            "uuid": 7837776699425727064,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Gold Key (2)",
            "classname": "item_key2",
            "uuid": 7189009630953251234,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Supernailgun (3)",
            "classname": "weapon_supernailgun",
            "uuid": 9568839579728877547,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Grenadelauncher (4)",
            "classname": "weapon_grenadelauncher",
            "uuid": 10821149365352336885,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Green Armor (5)",
            "classname": "item_armor1",
            "uuid": 8704801133444550156,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Lightning (6)",
            "classname": "weapon_lightning",
            "uuid": 706220780484367221,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Cells (7)",
            "classname": "item_cells",
            "uuid": 17639963561804487655,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 4345672852327216007,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 15564798464664393329,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 14809708043256997172,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Yellow Armor (11)",
            "classname": "item_armor2",
            "uuid": 3971058341813940618,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Secret (12)",
            "classname": "trigger_secret",
            "uuid": 11253912675731029946,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 2717822046378367444,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Spikes (14)",
            "classname": "item_spikes",
            "uuid": 3876464249589383904,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 1945890189495039296,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Shells (16)",
            "classname": "item_shells",
            "uuid": 14402636549180495136,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 12100121253769741833,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Supershotgun (18)",
            "classname": "weapon_supershotgun",
            "uuid": 10482177770586472985,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 16980301698656272268,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rocketlauncher (20)",
            "classname": "weapon_rocketlauncher",
            "uuid": 9001414194932162811,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Spikes (21)",
            "classname": "item_spikes",
            "uuid": 7741384559467285856,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Spikes (22)",
            "classname": "item_spikes",
            "uuid": 10569052915086850298,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 17916987524915584639,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 15545478479609814549,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Rockets (25)",
            "classname": "item_rockets",
            "uuid": 4487928747910075303,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Cells (26)",
            "classname": "item_cells",
            "uuid": 1272050510575734388,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 8998490631042801312,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 6489377013436273290,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 18317368090520754754,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Small Medkit (30)",
            "classname": "item_health",
            "uuid": 14720654485608640379,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Small Medkit (31)",
            "classname": "item_health",
            "uuid": 15086582820518539510,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 14456074759755421394,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Secret (33)",
            "classname": "trigger_secret",
            "uuid": 5432148646905757628,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Megahealth (34)",
            "classname": "item_health",
            "uuid": 2886964888572925849,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Spikes (35)",
            "classname": "item_spikes",
            "uuid": 7714231776139349209,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 2361895100973177328,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Green Armor (37)",
            "classname": "item_armor1",
            "uuid": 15673381131507460236,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 15962665758723083122,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Quad Damage (39)",
            "classname": "item_artifact_super_damage",
            "uuid": 3983444708186396639,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 16995993265310081839,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 10806273219793483528,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Yellow Armor (42)",
            "classname": "item_armor2",
            "uuid": 9818258994311246067,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Spikes (43)",
            "classname": "item_spikes",
            "uuid": 11398849678039128587,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 4940051000513770518,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Green Armor (45)",
            "classname": "item_armor1",
            "uuid": 12652749547415637696,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Rockets (46)",
            "classname": "item_rockets",
            "uuid": 7717761678837004435,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 4901441984109450717,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Secret (48)",
            "classname": "trigger_secret",
            "uuid": 5394656253374741403,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Secret Exit",
            "classname": "trigger_changelevel",
            "uuid": 1476787090648326191,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Cells (50)",
            "classname": "item_cells",
            "uuid": 3775822594441390242,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Small Medkit (51)",
            "classname": "item_health",
            "uuid": 14197134485403516052,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Secret (52)",
            "classname": "trigger_secret",
            "uuid": 14831347790110795118,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 8378237930351460500,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Rockets (54)",
            "classname": "item_rockets",
            "uuid": 13019667180111994372,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 5444120512220083516,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Shells (56)",
            "classname": "item_shells",
            "uuid": 11663317067076128770,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Cells (57)",
            "classname": "item_cells",
            "uuid": 343466567689197617,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Small Medkit (58)",
            "classname": "item_health",
            "uuid": 14800566451407206690,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Shells (59)",
            "classname": "item_shells",
            "uuid": 7626080704547617000,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 8116238305510824590,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "All Kills (61)",
            "classname": "all_kills",
            "uuid": 13571470943515360453,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supernailgun (3)",
                "Grenadelauncher (4)",
                "Supershotgun (18)",
                "Spikes (14)",
                "Spikes (15)",
                "Green Armor (45)",
                "Shells (17)",
                "Shells (16)",
                "Large Medkit (19)",
            ],
        )

        jump_area = self.region(
            "Jump Area",
            [
                "Rocketlauncher (20)",
                "Small Medkit (30)",
                "Small Medkit (31)",
                "Shells (29)",
                "Shells (28)",
            ],
        )
        self.connect(
            ret,
            jump_area,
            r.bigjump_hard
            | (r.can_door & (r.can_jump | r.can_rj_hard | r.can_gj_extr)),
        )

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Secret (52)",
                "Cells (50)",
                "Cells (57)",
                "Rockets (54)",
                "Small Medkit (58)",
                "Small Medkit (51)",
            ],
        )
        self.connect(jump_area, shootswitch_area, r.can_shootswitch)
        self.restrict("Rockets (54)", r.can_door)
        self.restrict("Small Medkit (58)", r.can_door)
        self.restrict("Small Medkit (51)", r.can_door)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Rockets (46)",
                "Rockets (47)",
                "Spikes (22)",
                "Spikes (21)",
                "Large Medkit (23)",
                "Shells (24)",
                "Large Medkit (41)",
                "Yellow Armor (42)",
                "Spikes (43)",
            ],
        )
        self.connect(jump_area, past_button_area, r.can_button)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Shells (44)",
                "Silver Key (1)",
            ],
        )
        self.connect(past_button_area, past_door_area, r.can_door)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Shells (60)",
                "Shells (59)",
                "Large Medkit (38)",
                "Lightning (6)",
            ],
        )
        self.connect(ret, past_silver_door_area, self.silver_key)

        past_button_silver_area = self.region(
            "Past Silver Button Area",
            [
                "Cells (26)",
                "Rockets (25)",
                "Green Armor (37)",
                "Spikes (35)",
                "Spikes (36)",
                "Megahealth (34)",
                "Shells (56)",
                "Shells (55)",
                "Large Medkit (27)",
                "Quad Damage (39)",
                "Secret (48)",
                "Shells (40)",
                "Gold Key (2)",
            ],
        )
        self.connect(past_silver_door_area, past_button_silver_area, r.can_button)

        self.restrict("Quad Damage (39)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Secret (48)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Shells (40)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Gold Key (2)", r.can_jump | r.can_rj_hard | r.can_gj_extr)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Green Armor (5)",
                "Cells (7)",
                "Large Medkit (8)",
                "Spikes (10)",
                "Spikes (9)",
                "Secret (12)",
                "Shells (13)",
                "Yellow Armor (11)",
            ],
        )
        self.connect(ret, past_gold_door_area, self.gold_key)

        self.restrict("Secret (12)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Shells (13)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Yellow Armor (11)", r.can_shootswitch | r.bigjump_hard)

        past_button_gold_area = self.region(
            "Past Gold Button Area",
            [
                "Exit",
                "Small Medkit (51)",
                "Small Medkit (58)",
                "Secret (33)",
                "Large Medkit (53)",
                "Secret Exit",
                "All Kills (61)",
            ],
        )
        self.connect(ret, past_button_gold_area, r.can_button)

        self.restrict("Secret (33)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Large Medkit (53)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Secret Exit", r.can_jump | r.can_rj_hard | r.can_gj_extr)

        self.restrict(
            "All Kills (61)", self.silver_key & r.can_door & r.difficult_combat
        )

        return ret
