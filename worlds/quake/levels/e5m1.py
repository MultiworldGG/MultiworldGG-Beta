from BaseClasses import Region

from ..base_classes import Q1Level


class e5m1(Q1Level):
    name = "The Military Base"
    mapfile = "e5m1"
    keys = ["Silver"]
    location_defs = [
        {
            "id": 1,
            "name": "Nailgun (1)",
            "classname": "weapon_nailgun",
            "uuid": 4077847519060824121,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Green Armor (2)",
            "classname": "item_armor1",
            "uuid": 4128873528341087985,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Small Medkit (3)",
            "classname": "item_health",
            "uuid": 6833677172540381527,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Supershotgun (4)",
            "classname": "weapon_supershotgun",
            "uuid": 6702362101370474778,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 9081816496302114688,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Spikes (6)",
            "classname": "item_spikes",
            "uuid": 9504847605333147163,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Silver Key (7)",
            "classname": "item_key1",
            "uuid": 9305601502910644934,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Megahealth (8)",
            "classname": "item_health",
            "uuid": 14657574914412480911,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 3824399863615310711,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 18365770180947216266,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 5915242734453796936,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 8479338960889195358,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Biosuit (13)",
            "classname": "item_artifact_envirosuit",
            "uuid": 15158281165023501516,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Yellow Armor (14)",
            "classname": "item_armor2",
            "uuid": 13854947595317699214,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 1199276928934508272,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Spikes (16)",
            "classname": "item_spikes",
            "uuid": 2592088164778249918,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 7000108522470236889,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Spikes (18)",
            "classname": "item_spikes",
            "uuid": 13558314118624531443,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Shells (19)",
            "classname": "item_shells",
            "uuid": 10259659205618082533,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Small Medkit (20)",
            "classname": "item_health",
            "uuid": 3400536601570048804,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Secret (21)",
            "classname": "trigger_secret",
            "uuid": 14488277715512817362,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Quad Damage (22)",
            "classname": "item_artifact_super_damage",
            "uuid": 5397738360315614983,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Nailgun (23)",
            "classname": "weapon_nailgun",
            "uuid": 16272585310243625456,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 13917500877120528364,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 14903889672901399666,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Shells (26)",
            "classname": "item_shells",
            "uuid": 14019071230171239144,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Secret (27)",
            "classname": "trigger_secret",
            "uuid": 5133423073286909776,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Secret (28)",
            "classname": "trigger_secret",
            "uuid": 1794483469510819850,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Secret (29)",
            "classname": "trigger_secret",
            "uuid": 6600027405142429154,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Secret (30)",
            "classname": "trigger_secret",
            "uuid": 5208868341796930431,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Secret (31)",
            "classname": "trigger_secret",
            "uuid": 11498088527546522586,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "All Kills (32)",
            "classname": "all_kills",
            "uuid": 15932440387884858511,
            "mp": 0,
        },
    ]
    must_bio = True
    must_invuln = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Small Medkit (3)",
                "Shells (19)",
                "Secret (27)",
                "Green Armor (2)",
                "Small Medkit (20)",
                "Secret (28)",
                "Spikes (18)",
                "Secret (29)",
                "Nailgun (1)",
                "Spikes (6)",
                "Spikes (24)",
                "Shells (5)",
                "Secret (31)",
                "Megahealth (8)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)
        self.restrict("Secret (27)", r.jump)
        self.restrict("Green Armor (2)", r.jump)
        self.restrict("Secret (31)", r.can_shootswitch)
        self.restrict("Megahealth (8)", r.can_shootswitch | r.bigjump_hard)

        past_acid_pit_area = self.region(
            "Past Acid Pit",
            [
                "Large Medkit (25)",
                "Spikes (10)",
                "Nailgun (23)",
            ],
        )
        self.connect(past_door_area, past_acid_pit_area, r.can_button | r.bigjump_hard)

        past_jump_area = self.region(
            "Past Jump Area",
            [
                "Silver Key (7)",
                "Spikes (9)",
            ],
        )
        self.connect(past_acid_pit_area, past_jump_area, r.jump)
        self.connect(past_door_area, past_jump_area, r.bigjump_hard)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Secret (30)",
                "Supershotgun (4)",
                "Large Medkit (12)",
                "Quad Damage (22)",
                "Large Medkit (17)",
                "Biosuit (13)",
                "Shells (26)",
                "Exit",
                "All Kills (32)",
            ],
        )
        self.connect(past_acid_pit_area, past_silver_door_area, self.silver_key)
        self.restrict("All Kills (32)", r.backpack(5))

        self.restrict("Quad Damage (22)", r.jump)
        self.restrict("Shells (26)", r.can_button | r.bigjump_hard)
        self.restrict("Exit", r.can_button | r.bigjump_hard)

        dive_area = self.region(
            "Dive Area",
            [
                "Large Medkit (15)",
                "Yellow Armor (14)",
                "Secret (21)",
                "Spikes (16)",
            ],
        )
        self.connect(
            past_silver_door_area, dive_area, r.can_dive & r.invuln(1) | r.biosuit(1)
        )

        return ret
