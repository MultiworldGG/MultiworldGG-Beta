from BaseClasses import Region

from ..base_classes import Q1Level


class e1m4(Q1Level):
    name = "The Grisly Grotto"
    mapfile = "e1m4"
    keys = ["Silver"]
    location_defs = [
        {
            "id": 1,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 15075437028369298457,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Yellow Armor (2)",
            "classname": "item_armor2",
            "uuid": 1555065542270898572,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Large Medkit (3)",
            "classname": "item_health",
            "uuid": 12474090675194010109,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 12758549677775835207,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 14137687452654241025,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 6371484894953130168,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Silver Key (7)",
            "classname": "item_key1",
            "uuid": 399406060548109491,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 5589893183977642434,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Small Medkit (9)",
            "classname": "item_health",
            "uuid": 15322787254569174121,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 11282183156626791608,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Spikes (11)",
            "classname": "item_spikes",
            "uuid": 17932066490361916570,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 5927395591391661898,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 17143932955064348185,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 1924373661662402772,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 619214712067352356,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 12952305794154845409,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 15837320639165395793,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 2563815924448049497,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Small Medkit (19)",
            "classname": "item_health",
            "uuid": 9281854624674257259,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 491980766011292978,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 17723865642069758010,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Yellow Armor (22)",
            "classname": "item_armor2",
            "uuid": 2749102365391713688,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Small Medkit (23)",
            "classname": "item_health",
            "uuid": 15040722786443812828,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 14941485961752350310,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Small Medkit (25)",
            "classname": "item_health",
            "uuid": 3009302055440591613,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Shells (26)",
            "classname": "item_shells",
            "uuid": 8794227398659205211,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 15712847686120480498,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Rockets (28)",
            "classname": "item_rockets",
            "uuid": 3674664050340926042,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Spikes (29)",
            "classname": "item_spikes",
            "uuid": 12362956808783195610,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Spikes (30)",
            "classname": "item_spikes",
            "uuid": 8837630391063600492,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 662744941360474769,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 15890618430332981592,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 4131801788505860557,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Supernailgun (34)",
            "classname": "weapon_supernailgun",
            "uuid": 6338935010740490376,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Spikes (35)",
            "classname": "item_spikes",
            "uuid": 15314014754050044566,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 10520725010791918813,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Shells (37)",
            "classname": "item_shells",
            "uuid": 3171236834305980408,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Shells (38)",
            "classname": "item_shells",
            "uuid": 14622841936204688852,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Shells (39)",
            "classname": "item_shells",
            "uuid": 5658048066775457059,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Spikes (40)",
            "classname": "item_spikes",
            "uuid": 15873906859187729548,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Spikes (41)",
            "classname": "item_spikes",
            "uuid": 15218320935421477302,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Secret (42)",
            "classname": "trigger_secret",
            "uuid": 3133215948021772165,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 15244779195613891587,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Large Medkit (44)",
            "classname": "item_health",
            "uuid": 5904073041145025586,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Large Medkit (45)",
            "classname": "item_health",
            "uuid": 2127241678382881349,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 15467368263044517771,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Secret Exit",
            "classname": "trigger_changelevel",
            "uuid": 3150179961539064980,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Spikes (48)",
            "classname": "item_spikes",
            "uuid": 7996423009852861844,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Supershotgun (49)",
            "classname": "weapon_supershotgun",
            "uuid": 3809557072603750452,
            "mp": 1,
        },
        {
            "id": 50,
            "name": "Rocketlauncher (50)",
            "classname": "weapon_rocketlauncher",
            "uuid": 11244280619215842405,
            "mp": 1,
        },
        {
            "id": 51,
            "name": "Nailgun (51)",
            "classname": "weapon_nailgun",
            "uuid": 13506794634462307725,
            "mp": 1,
        },
        {
            "id": 52,
            "name": "Grenadelauncher (52)",
            "classname": "weapon_grenadelauncher",
            "uuid": 15868875818614318975,
            "mp": 1,
        },
        {
            "id": 53,
            "name": "Rockets (53)",
            "classname": "item_rockets",
            "uuid": 14415904023868728731,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Shells (54)",
            "classname": "item_shells",
            "uuid": 15901690681324462141,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Large Medkit (55)",
            "classname": "item_health",
            "uuid": 3988568057990495925,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Small Medkit (56)",
            "classname": "item_health",
            "uuid": 17382964619174153964,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Spikes (57)",
            "classname": "item_spikes",
            "uuid": 498101731868541960,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Spikes (58)",
            "classname": "item_spikes",
            "uuid": 251978457804909385,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Invulnerability (59)",
            "classname": "item_artifact_invulnerability",
            "uuid": 14749899555361738840,
            "mp": 1,
        },
        {
            "id": 60,
            "name": "Biosuit (60)",
            "classname": "item_artifact_envirosuit",
            "uuid": 8573253084289095752,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Secret (61)",
            "classname": "trigger_secret",
            "uuid": 6243418930552557467,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 1968766640316090137,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Spikes (63)",
            "classname": "item_spikes",
            "uuid": 1821132892655176008,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Shells (64)",
            "classname": "item_shells",
            "uuid": 791522376903635605,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 7562800402260031820,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Spikes (66)",
            "classname": "item_spikes",
            "uuid": 13633520446632610199,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Invisibility (67)",
            "classname": "item_artifact_invisibility",
            "uuid": 18277576981745738723,
            "mp": 1,
        },
        {
            "id": 68,
            "name": "Grenadelauncher (68)",
            "classname": "weapon_grenadelauncher",
            "uuid": 15859813994129007404,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "All Kills (69)",
            "classname": "all_kills",
            "uuid": 8911686284948589309,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Shells (65)",
                "Large Medkit (55)",
                "Small Medkit (56)",
                "Supershotgun (49)",
                "Large Medkit (3)",
                "Large Medkit (4)",
            ],
        )

        past_spawn_door_area = self.region(
            "Past Spawn Door",
            [
                "Shells (5)",
                "Yellow Armor (2)",
                "Spikes (66)",
                "Shells (17)",
                "Spikes (48)",
                "Biosuit (60)",
                "Large Medkit (6)",
                "Secret (42)",
            ],
        )
        self.connect(ret, past_spawn_door_area, r.can_door)
        self.restrict("Secret (42)", r.can_shootswitch)

        self.restrict("Yellow Armor (2)", r.can_shootswitch)

        lake_platform_area = self.region(
            "Lake Platform",
            [
                "Silver Key (7)",
                "Rocketlauncher (50)",
                "Shells (39)",
                "Large Medkit (32)",
            ],
        )
        self.connect(
            past_spawn_door_area,
            lake_platform_area,
            (
                (((r.can_rj_hard) | (r.can_gj_extr & r.can_jump)))
                | (r.can_dive & r.can_button)
            ),
        )

        lake_cave_area = self.region(
            "Lake Secret Cave",
            [
                "Secret (61)",
                "Rockets (53)",
            ],
        )
        self.connect(past_spawn_door_area, lake_cave_area, r.can_dive)

        lake_underwater_area = self.region(
            "Lake Underwater Area",
            [
                "Small Medkit (19)",
                "Large Medkit (18)",
                "Supernailgun (34)",
                "Spikes (58)",
                "Spikes (36)",
                "Spikes (63)",
                "Large Medkit (12)",
                "Shells (13)",
                "Spikes (57)",
                "Small Medkit (25)",
                "Spikes (10)",
                "Spikes (11)",
                "Invulnerability (59)",
                "Large Medkit (8)",
                "Small Medkit (9)",
            ],
        )
        self.connect(past_spawn_door_area, lake_underwater_area, r.can_dive)
        # inside via button press
        self.connect(lake_underwater_area, lake_platform_area, r.can_button)

        lake_door_area = self.region(
            "Lake Secret Door",
            [
                "Spikes (40)",
                "Spikes (35)",
                "Shells (33)",
            ],
        )
        self.connect(lake_underwater_area, lake_door_area, r.can_button)
        self.connect(
            lake_platform_area, lake_door_area, r.can_door
        )  # does this require door?

        castle_area = self.region(
            "Castle Area",
            [
                "Spikes (62)",
                "Large Medkit (15)",
                "Large Medkit (16)",
                "Shells (14)",
            ],
        )
        self.connect(past_spawn_door_area, castle_area, r.can_dive)

        castle_upper_outside_area = self.region(
            "Castle Upper Outside Area",
            [
                "Large Medkit (27)",
                "Grenadelauncher (52)",
                "Shells (38)",
                "Shells (64)",
                "Shells (26)",
                "Exit",
                "All Kills (69)",
            ],
        )
        self.restrict("Exit", r.can_door)
        self.restrict("All Kills (69)", r.can_door & r.backpack(5))

        castle_inside_area = self.region(
            "Castle Inside Area",
            [
                "Shells (31)",
                "Small Medkit (23)",
                "Spikes (24)",
                "Yellow Armor (22)",
                "Nailgun (51)",
                "Shells (37)",
                "Large Medkit (21)",
                "Large Medkit (20)",
                "Spikes (30)",
                "Spikes (29)",
                "Shells (54)",
            ],
        )
        self.restrict("Yellow Armor (22)", r.can_button)
        self.restrict("Shells (54)", r.can_door)

        # rj/gj from the water sloped surface
        self.connect(
            castle_area,
            castle_inside_area,
            self.silver_key,
        )

        self.connect(castle_inside_area, castle_upper_outside_area, r.can_door)

        # TODO: Maybe extreme diff rj
        self.connect(
            castle_area,
            castle_upper_outside_area,
            (r.can_jump & ((r.can_rj_hard) | (r.can_gj_extr))),
        )

        castle_inside_sides_area = self.region(
            "Castle Inside Sides Area",
            [
                "Rockets (28)",
                "Spikes (41)",
                "Large Medkit (43)",
                "Large Medkit (44)",
            ],
        )
        self.connect(
            castle_inside_area,
            castle_inside_sides_area,
            r.can_button | (r.can_jump & ((r.can_rj_med) | (r.can_gj_hard))),
        )

        # secret cave needs buttons pressed
        lake_super_secret = self.region(
            "Lake Super Secret Area",
            [
                "Secret (46)",
                "Grenadelauncher (68)",
                "Large Medkit (45)",
                "Invisibility (67)",
                "Secret Exit",
            ],
        )
        # dive is already covered earlier
        self.connect(castle_inside_sides_area, lake_super_secret, r.can_button)

        # TODO: Is this required?
        self.restrict("Secret Exit", r.can_door)

        return ret
