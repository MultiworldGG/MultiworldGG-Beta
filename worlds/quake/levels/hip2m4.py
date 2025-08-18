from BaseClasses import Region

from ..base_classes import Q1Level


class hip2m4(Q1Level):
    name = "The Crypt"
    mapfile = "hip2m4"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Spikes (1)",
            "classname": "item_spikes",
            "uuid": 15499296639067018489,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Rockets (2)",
            "classname": "item_rockets",
            "uuid": 10425702591309683984,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Empathy (3)",
            "classname": "item_artifact_empathy_shields",
            "uuid": 1892563785869512875,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Invisibility (4)",
            "classname": "item_artifact_invisibility",
            "uuid": 18319504851896194630,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Rockets (5)",
            "classname": "item_rockets",
            "uuid": 11593356770639704183,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Small Medkit (6)",
            "classname": "item_health",
            "uuid": 6240594994149390657,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Hornofconjuring (7)",
            "classname": "item_hornofconjuring",
            "uuid": 6478238670126956527,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 14783937958899033377,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Cells (9)",
            "classname": "item_cells",
            "uuid": 2268437961051756098,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Supershotgun (10)",
            "classname": "weapon_supershotgun",
            "uuid": 994071840838192430,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Small Medkit (11)",
            "classname": "item_health",
            "uuid": 11376759176009665259,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 2716025159600209751,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Small Medkit (13)",
            "classname": "item_health",
            "uuid": 4856106949980289751,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 9017339928192846448,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Grenadelauncher (15)",
            "classname": "weapon_grenadelauncher",
            "uuid": 18131072822335381198,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Silver Key (16)",
            "classname": "item_key1",
            "uuid": 9532416421061318099,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 3866805805398468865,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Spikes (18)",
            "classname": "item_spikes",
            "uuid": 13206031708243400287,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Gold Key (19)",
            "classname": "item_key2",
            "uuid": 1155655055977087893,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Small Medkit (20)",
            "classname": "item_health",
            "uuid": 1611429786984334803,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Lightning (21)",
            "classname": "weapon_lightning",
            "uuid": 16619257722318411930,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Shells (22)",
            "classname": "item_shells",
            "uuid": 4503334943058702483,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 2493434400611489370,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Green Armor (24)",
            "classname": "item_armor1",
            "uuid": 1601492201641541218,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 3181785724108123238,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Invulnerability (26)",
            "classname": "item_artifact_invulnerability",
            "uuid": 17516911097479468843,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Supernailgun (27)",
            "classname": "weapon_supernailgun",
            "uuid": 7422413106465860478,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 11161160325382092818,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Rockets (29)",
            "classname": "item_rockets",
            "uuid": 7162551151544332521,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Spikes (30)",
            "classname": "item_spikes",
            "uuid": 6333622876996524316,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 9090232956325795829,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Shells (32)",
            "classname": "item_shells",
            "uuid": 837528193124505660,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 11965913749201868598,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Yellow Armor (34)",
            "classname": "item_armor2",
            "uuid": 9680383207586444733,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 7261853191589729921,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Secret (36)",
            "classname": "trigger_secret",
            "uuid": 15235301764415315213,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Secret (37)",
            "classname": "trigger_secret",
            "uuid": 5461423198940459851,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 1588926341029821719,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Megahealth (39)",
            "classname": "item_health",
            "uuid": 14795836708969586373,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Spikes (40)",
            "classname": "item_spikes",
            "uuid": 14111449107615637216,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Secret (41)",
            "classname": "trigger_secret",
            "uuid": 14560433598496508563,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Rockets (42)",
            "classname": "item_rockets",
            "uuid": 6780375391813679603,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Rocketlauncher (43)",
            "classname": "weapon_rocketlauncher",
            "uuid": 6163236285703877824,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Large Medkit (44)",
            "classname": "item_health",
            "uuid": 11657664749569163494,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Secret (45)",
            "classname": "trigger_secret",
            "uuid": 4467865765448348712,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Red Armor (46)",
            "classname": "item_armorInv",
            "uuid": 16225296329615925044,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Nailgun (47)",
            "classname": "weapon_nailgun",
            "uuid": 1143510657494357736,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Secret (48)",
            "classname": "trigger_secret",
            "uuid": 13663751833149658005,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Quad Damage (49)",
            "classname": "item_artifact_super_damage",
            "uuid": 9724107077360167191,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Small Medkit (50)",
            "classname": "item_health",
            "uuid": 8289430104972711847,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Small Medkit (51)",
            "classname": "item_health",
            "uuid": 1572058312107221319,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Small Medkit (52)",
            "classname": "item_health",
            "uuid": 131302204098973391,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Shells (53)",
            "classname": "item_shells",
            "uuid": 16068018198573467931,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Spikes (54)",
            "classname": "item_spikes",
            "uuid": 18347761799564136657,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Spikes (55)",
            "classname": "item_spikes",
            "uuid": 1262010644418365937,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Secret (56)",
            "classname": "trigger_secret",
            "uuid": 10599748053025132802,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Megahealth (57)",
            "classname": "item_health",
            "uuid": 488137541226587582,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Proximity (58)",
            "classname": "weapon_proximity_gun",
            "uuid": 18361552271622708663,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Laser (59)",
            "classname": "weapon_laser_gun",
            "uuid": 4885551918212378905,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Cells (60)",
            "classname": "item_cells",
            "uuid": 8737916523581921206,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Cells (61)",
            "classname": "item_cells",
            "uuid": 11883126491030014720,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Mjolnir (62)",
            "classname": "weapon_mjolnir",
            "uuid": 13005957927998537785,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Rockets (63)",
            "classname": "item_rockets",
            "uuid": 9493512446951622145,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Rocketlauncher (64)",
            "classname": "weapon_rocketlauncher",
            "uuid": 3722702060670335295,
            "mp": 1,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 3885104949295722468,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Megahealth (66)",
            "classname": "item_health",
            "uuid": 18309488645229198265,
            "mp": 1,
        },
        {
            "id": 67,
            "name": "Quad Damage (67)",
            "classname": "item_artifact_super_damage",
            "uuid": 5566912806222034796,
            "mp": 1,
        },
        {
            "id": 68,
            "name": "All Kills (68)",
            "classname": "all_kills",
            "uuid": 15028427888759203171,
            "mp": 0,
        },
    ]
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
                "Large Medkit (23)",
                "Shells (22)",
                "Green Armor (24)",
                "Grenadelauncher (15)",
                "Spikes (40)",
                "Large Medkit (25)",
                "Secret (48)",
                "Rockets (42)",
                "Rocketlauncher (64)",
                "Rockets (63)",
                "Shells (32)",
                "Shells (33)",
                "Large Medkit (31)",
                "Spikes (30)",
                "Large Medkit (44)",
                "Rocketlauncher (43)",
                "Silver Key (16)",
                "Invulnerability (26)",
                "Nailgun (47)",
                "Quad Damage (49)",
                "Rockets (14)",
                "Rockets (5)",
                "Small Medkit (6)",
                "Supershotgun (10)",
                "Small Medkit (11)",
                "Small Medkit (13)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        jump_area = self.region(
            "Jump Area",
            [
                "Shells (12)",
                "Cells (9)",
                "Hornofconjuring (7)",
                "Megahealth (66)",
                "Secret (41)",
                "Secret (36)",
                "Laser (59)",
                "Shells (35)",
                "Spikes (38)",
                "Red Armor (46)",
                "Secret (45)",
                "Small Medkit (50)",
                "Small Medkit (51)",
                "Small Medkit (52)",
                "Mjolnir (62)",
                "Spikes (54)",
                "Shells (53)",
                "Secret (56)",
                "Megahealth (57)",
            ],
        )
        self.connect(
            past_door_area, jump_area, r.can_jump | r.can_gj_extr | r.can_rj_hard
        )
        self.restrict("Secret (56)", r.invuln(1))
        self.restrict("Megahealth (57)", r.invuln(1))
        self.restrict(
            "Hornofconjuring (7)",
            (r.difficulty("hard") & r.can_jump) | r.bigjump | (r.skill_eq(0) & r.jump),
        )
        self.restrict(
            "Secret (41)",
            (r.difficulty("hard") & r.can_jump) | r.bigjump | (r.skill_eq(0) & r.jump),
        )

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Megahealth (39)",
                "Spikes (55)",
                "Lightning (21)",
                "Cells (61)",
                "Cells (60)",
                "Quad Damage (67)",
                "Small Medkit (20)",
                "Yellow Armor (34)",
                "Supernailgun (27)",
                "Shells (65)",
                "Empathy (3)",
                "Secret (37)",
            ],
        )
        self.connect(past_door_area, past_silver_door_area, self.silver_key)
        self.restrict("Empathy (3)", r.jump)
        self.restrict("Secret (37)", r.jump)

        past_silver_upper_area = self.region(
            "Past Silver Door Upper",
            [
                "Spikes (1)",
                "Spikes (18)",
                "Gold Key (19)",
                "Large Medkit (17)",
                "Invisibility (4)",
                "Rockets (2)",
            ],
        )
        self.connect(
            past_door_area,
            past_silver_upper_area,
            r.can_jump | r.can_gj_extr | r.can_rj_hard,
        )
        self.connect(past_silver_door_area, past_silver_upper_area)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (28)",
                "Rockets (29)",
                "Proximity (58)",
                "Exit",
                "All Kills (68)",
            ],
        )
        self.connect(past_silver_door_area, past_gold_door_area, self.gold_key)

        self.restrict(
            "Exit",
            r.grenadelauncher
            | r.rocketlauncher
            | r.proximitygun
            | (r.difficulty("hard") & r.quad_dmg(1)),
        )

        # also requires access to upper part of the map
        self.restrict(
            "All Kills (68)",
            r.difficult_combat & self.silver_key,
        )

        return ret
