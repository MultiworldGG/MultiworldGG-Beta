from BaseClasses import Region

from ..base_classes import Q1Level


class e3m2(Q1Level):
    name = "The Vaults of Zin"
    mapfile = "e3m2"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Grenadelauncher (1)",
            "classname": "weapon_grenadelauncher",
            "uuid": 831645054965248171,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Rockets (2)",
            "classname": "item_rockets",
            "uuid": 38159291953668192,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Megahealth (3)",
            "classname": "item_health",
            "uuid": 11549776279039474348,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Silver Key (4)",
            "classname": "item_key1",
            "uuid": 15530835811125490588,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Rockets (5)",
            "classname": "item_rockets",
            "uuid": 13283188104736317060,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 17647825145005262373,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Yellow Armor (7)",
            "classname": "item_armor2",
            "uuid": 6776685637039154371,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 11209897224282191195,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Large Medkit (9)",
            "classname": "item_health",
            "uuid": 1635440573880684655,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Nailgun (10)",
            "classname": "weapon_nailgun",
            "uuid": 7600632728021946932,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 11244211062785145196,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 973259175531238942,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Large Medkit (13)",
            "classname": "item_health",
            "uuid": 4747117958394030001,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 12925904592497014334,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Supershotgun (15)",
            "classname": "weapon_supershotgun",
            "uuid": 11686812346729011832,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Shells (16)",
            "classname": "item_shells",
            "uuid": 4528664654979574610,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Rockets (17)",
            "classname": "item_rockets",
            "uuid": 4863347717397306974,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Rocketlauncher (18)",
            "classname": "weapon_rocketlauncher",
            "uuid": 15174925362105523340,
            "mp": 1,
        },
        {
            "id": 19,
            "name": "Rockets (19)",
            "classname": "item_rockets",
            "uuid": 17377404798369904464,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Shells (20)",
            "classname": "item_shells",
            "uuid": 4470636024274751168,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 539417650368911742,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Gold Key (22)",
            "classname": "item_key2",
            "uuid": 8751614444319043341,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 1034712951582089329,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 12925549714981927471,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Secret (25)",
            "classname": "trigger_secret",
            "uuid": 13502935702474560218,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Secret (26)",
            "classname": "trigger_secret",
            "uuid": 6328392589830750725,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 3078899312970357578,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 18434276651806980405,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Spikes (29)",
            "classname": "item_spikes",
            "uuid": 8711670006309039378,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Quad Damage (30)",
            "classname": "item_artifact_super_damage",
            "uuid": 5328725062645344916,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Invisibility (31)",
            "classname": "item_artifact_invisibility",
            "uuid": 3654070320029626353,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 10481441387658429871,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Large Medkit (33)",
            "classname": "item_health",
            "uuid": 14189460550956745755,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 2381203863454534401,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 15556978633693537982,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Large Medkit (36)",
            "classname": "item_health",
            "uuid": 11202954237815763568,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Small Medkit (37)",
            "classname": "item_health",
            "uuid": 7770036797911096043,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Small Medkit (38)",
            "classname": "item_health",
            "uuid": 8491830493114752969,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 10392077959307727168,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 17312979548343079034,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 927033328815991292,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 8001673132651058933,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Spikes (43)",
            "classname": "item_spikes",
            "uuid": 3955566843115011141,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Rockets (44)",
            "classname": "item_rockets",
            "uuid": 11600209157016705547,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Large Medkit (45)",
            "classname": "item_health",
            "uuid": 5518877482654268354,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Large Medkit (46)",
            "classname": "item_health",
            "uuid": 907054184461488406,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Grenadelauncher (47)",
            "classname": "weapon_grenadelauncher",
            "uuid": 14724576191904729752,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Quad Damage (48)",
            "classname": "item_artifact_super_damage",
            "uuid": 9725039897741985085,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Spikes (49)",
            "classname": "item_spikes",
            "uuid": 15752268596253117104,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Rockets (50)",
            "classname": "item_rockets",
            "uuid": 15493014573285582309,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Spikes (51)",
            "classname": "item_spikes",
            "uuid": 7260095550909629864,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Spikes (52)",
            "classname": "item_spikes",
            "uuid": 1228220577523975787,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Spikes (53)",
            "classname": "item_spikes",
            "uuid": 7695823787762202453,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Shells (54)",
            "classname": "item_shells",
            "uuid": 5197685194573738391,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 6928119390142849854,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Rockets (56)",
            "classname": "item_rockets",
            "uuid": 4878801624708651919,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 17296570047879412760,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "All Kills (58)",
            "classname": "all_kills",
            "uuid": 2935180640685079621,
            "mp": 0,
        },
    ]

    events = ["First Door Open"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Small Medkit (37)",
                "Small Medkit (38)",
                "Grenadelauncher (47)",
                "Silver Key (4)",
                "Megahealth (3)",
                "Secret (39)",
                "Grenadelauncher (1)",
                "Quad Damage (48)",
            ],
        )
        self.restrict("Grenadelauncher (1)", r.jump)
        self.restrict("Quad Damage (48)", r.jump)

        past_door_area = self.region(
            "Past Door",
            [
                "Rockets (2)",
                "First Door Open",
            ],
        )
        self.restrict("First Door Open", r.can_button)
        self.connect(ret, past_door_area, r.can_door)

        past_first_door_area = self.region(
            "Past First Door",
            [
                "Large Medkit (8)",
                "Large Medkit (9)",
                "Nailgun (10)",
                "Spikes (29)",
                "Spikes (52)",
                "Spikes (53)",
                "Large Medkit (6)",
                "Yellow Armor (7)",
                "Rockets (5)",
                "Quad Damage (30)",
                "Large Medkit (23)",
                "Large Medkit (24)",
                "Spikes (49)",
                "Rockets (14)",
                "Large Medkit (41)",
                "Large Medkit (40)",
                "Spikes (42)",
                "Shells (16)",
                "Spikes (43)",
                "Rockets (17)",
                "Large Medkit (28)",
                "Large Medkit (27)",
                "Secret (26)",
                "Rocketlauncher (18)",
                "Invisibility (31)",
            ],
        )
        self.connect(
            past_door_area, past_first_door_area, self.event("First Door Open")
        )
        self.restrict("Quad Damage (30)", r.can_shootswitch)
        self.restrict("Secret (26)", r.can_shootswitch)
        self.restrict("Rocketlauncher (18)", r.can_shootswitch)
        self.restrict("Invisibility (31)", r.can_shootswitch)

        secret_roof_area = self.region(
            "Secret Roof",
            [
                "Secret (25)",
                "Shells (20)",
                "Large Medkit (35)",
                "Large Medkit (36)",
                "Large Medkit (34)",
                "Rockets (19)",
            ],
        )
        self.connect(
            past_first_door_area,
            secret_roof_area,
            r.can_shootswitch | r.bigjump_hard,
        )

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Shells (57)",
                "Rockets (44)",
                "Large Medkit (11)",
                "Large Medkit (12)",
                "Spikes (51)",
                "Large Medkit (46)",
                "Large Medkit (13)",
                "Shells (55)",
                "Shells (54)",
            ],
        )
        self.connect(ret, past_silver_door_area, self.silver_key)

        silver_below_area = self.region(
            "Silver Below",
            [
                "Rockets (50)",
                "Gold Key (22)",
                "Large Medkit (32)",
                "Large Medkit (33)",
                "Rockets (56)",
                "Supershotgun (15)",
                "All Kills (58)",
            ],
        )
        self.connect(past_silver_door_area, silver_below_area, r.can_button)
        self.restrict("All Kills (58)", r.difficult_combat)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (45)",
                "Exit",
            ],
        )
        self.connect(past_silver_door_area, past_gold_door_area, self.gold_key)

        return ret
