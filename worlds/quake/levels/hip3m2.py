from BaseClasses import Region

from ..base_classes import Q1Level


class hip3m2(Q1Level):
    name = "Pandemonium"
    mapfile = "hip3m2"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Large Medkit (1)",
            "classname": "item_health",
            "uuid": 15145817813951549608,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Silver Key (2)",
            "classname": "item_key1",
            "uuid": 12573627132475621875,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Secret (3)",
            "classname": "trigger_secret",
            "uuid": 18161503178758547760,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Secret (4)",
            "classname": "trigger_secret",
            "uuid": 12187081299642247404,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Secret (5)",
            "classname": "trigger_secret",
            "uuid": 10718805727911961408,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Gold Key (6)",
            "classname": "item_key2",
            "uuid": 15418020758901909434,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Nailgun (7)",
            "classname": "weapon_nailgun",
            "uuid": 344325386930243490,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Spikes (8)",
            "classname": "item_spikes",
            "uuid": 18361586609309956353,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 341770656463234094,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Yellow Armor (10)",
            "classname": "item_armor2",
            "uuid": 16539760608183606749,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Green Armor (11)",
            "classname": "item_armor1",
            "uuid": 2548651823040367621,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 5568154449737700784,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 17197052973936840428,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 1745752871830831783,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Rockets (15)",
            "classname": "item_rockets",
            "uuid": 6926587167637557704,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Lightning (16)",
            "classname": "weapon_lightning",
            "uuid": 16386181100175474296,
            "mp": 1,
        },
        {
            "id": 17,
            "name": "Quad Damage (17)",
            "classname": "item_artifact_super_damage",
            "uuid": 2542305561846396782,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Megahealth (18)",
            "classname": "item_health",
            "uuid": 17393989963906192763,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 739419800755811548,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 2588724553276836813,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 7850772105159474122,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Rockets (22)",
            "classname": "item_rockets",
            "uuid": 11888616486172639936,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Rockets (23)",
            "classname": "item_rockets",
            "uuid": 398154560763873051,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Cells (24)",
            "classname": "item_cells",
            "uuid": 9540958074715280478,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Cells (25)",
            "classname": "item_cells",
            "uuid": 12310993365167301958,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Large Medkit (26)",
            "classname": "item_health",
            "uuid": 6134822120422111524,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Lightning (27)",
            "classname": "weapon_lightning",
            "uuid": 8840560957249101252,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Cells (28)",
            "classname": "item_cells",
            "uuid": 5105958414339974548,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Laser (29)",
            "classname": "weapon_laser_gun",
            "uuid": 2257561769887754414,
            "mp": 1,
        },
        {
            "id": 30,
            "name": "Supershotgun (30)",
            "classname": "weapon_supershotgun",
            "uuid": 14869713395596496988,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 10027378558871060181,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 3282007602906868865,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Grenadelauncher (33)",
            "classname": "weapon_grenadelauncher",
            "uuid": 17100470569025155493,
            "mp": 1,
        },
        {
            "id": 34,
            "name": "Rockets (34)",
            "classname": "item_rockets",
            "uuid": 7520555459159966220,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Rockets (35)",
            "classname": "item_rockets",
            "uuid": 10198221296040335845,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Rocketlauncher (36)",
            "classname": "weapon_rocketlauncher",
            "uuid": 13399470227219629434,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Rocketlauncher (37)",
            "classname": "weapon_rocketlauncher",
            "uuid": 3893496474977902806,
            "mp": 1,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 2005666350489262075,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 8268511455481030560,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Rockets (40)",
            "classname": "item_rockets",
            "uuid": 5346343452501876010,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Proximity (41)",
            "classname": "weapon_proximity_gun",
            "uuid": 6724318941238340014,
            "mp": 1,
        },
        {
            "id": 42,
            "name": "Supernailgun (42)",
            "classname": "weapon_supernailgun",
            "uuid": 13042914488213555115,
            "mp": 1,
        },
        {
            "id": 43,
            "name": "Shells (43)",
            "classname": "item_shells",
            "uuid": 15526888275014887541,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 5122123261788761881,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 11593801392910744109,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 971305503643621531,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Red Armor (47)",
            "classname": "item_armorInv",
            "uuid": 11531556487331793483,
            "mp": 1,
        },
        {
            "id": 48,
            "name": "Secret (48)",
            "classname": "trigger_secret",
            "uuid": 13181355541821394997,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Shells (49)",
            "classname": "item_shells",
            "uuid": 17910234605356955949,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Shells (50)",
            "classname": "item_shells",
            "uuid": 8255175675984650245,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Large Medkit (51)",
            "classname": "item_health",
            "uuid": 13630334046185902861,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 3405202043106625154,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 12428141463779018304,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 3280908121273302508,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Spikes (55)",
            "classname": "item_spikes",
            "uuid": 16804104462633926205,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Spikes (56)",
            "classname": "item_spikes",
            "uuid": 10614787885352519172,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Mjolnir (57)",
            "classname": "weapon_mjolnir",
            "uuid": 1862702462410107028,
            "mp": 1,
        },
        {
            "id": 58,
            "name": "Cells (58)",
            "classname": "item_cells",
            "uuid": 11246760447590391057,
            "mp": 1,
        },
        {
            "id": 59,
            "name": "Cells (59)",
            "classname": "item_cells",
            "uuid": 10335834431611673585,
            "mp": 1,
        },
        {
            "id": 60,
            "name": "Yellow Armor (60)",
            "classname": "item_armor2",
            "uuid": 4933669121293432778,
            "mp": 1,
        },
        {
            "id": 61,
            "name": "Shells (61)",
            "classname": "item_shells",
            "uuid": 9229588308824319794,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 9684189993359902896,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Spikes (63)",
            "classname": "item_spikes",
            "uuid": 2238854482864440666,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Spikes (64)",
            "classname": "item_spikes",
            "uuid": 1863025049961653812,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 13751905639675646281,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Shells (66)",
            "classname": "item_shells",
            "uuid": 3778060791111636296,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Invulnerability (67)",
            "classname": "item_artifact_invulnerability",
            "uuid": 828070396671096567,
            "mp": 1,
        },
        {
            "id": 68,
            "name": "All Kills (68)",
            "classname": "all_kills",
            "uuid": 17503102345979133724,
            "mp": 0,
        },
    ]

    events = ["Button Pressed"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Spikes (9)",
                "Spikes (8)",
                "Lightning (16)",
                "Rockets (14)",
                "Rockets (15)",
                "Supershotgun (30)",
                "Large Medkit (32)",
                "Large Medkit (31)",
                "Spikes (62)",
                "Shells (66)",
                "Cells (28)",
                "Shells (65)",
                "Spikes (38)",
                "Spikes (39)",
            ],
        )

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Secret (48)",
                "Nailgun (7)",
                "Secret (4)",
                "Yellow Armor (10)",
                "Green Armor (11)",
                "Shells (12)",
                "Shells (13)",
            ],
        )
        self.connect(ret, shootswitch_area, r.can_shootswitch)

        jump_area = self.region(
            "Jump Area",
            [
                "Proximity (41)",
                "Rockets (40)",
                "Shells (43)",
                "Shells (44)",
                "Large Medkit (1)",
                "Supernailgun (42)",
                "Shells (49)",
                "Yellow Armor (60)",
                "Shells (50)",
                "Large Medkit (51)",
                "Large Medkit (52)",
                "Cells (58)",
                "Cells (59)",
                "Mjolnir (57)",
                "Large Medkit (54)",
                "Spikes (56)",
                "Spikes (55)",
                "Large Medkit (53)",
                "Invulnerability (67)",
                "Button Pressed",
            ],
        )
        self.connect(ret, jump_area, r.jump)

        self.restrict("Invulnerability (67)", r.can_shootswitch & r.can_door)
        self.restrict("Button Pressed", r.can_shootswitch & r.can_door & r.can_button)

        past_barrier_area = self.region(
            "Past Barrier",
            [
                "Shells (61)",
                "Secret (46)",
                "Lightning (27)",
                "Red Armor (47)",
                "Secret (5)",
                "Large Medkit (19)",
                "Large Medkit (20)",
                "Large Medkit (21)",
                "Rockets (23)",
                "Rockets (22)",
                "Cells (25)",
                "Cells (24)",
                "Silver Key (2)",
                "Laser (29)",
                "Large Medkit (26)",
            ],
        )
        self.connect(ret, past_barrier_area, self.event("Button Pressed"))

        self.restrict("Secret (46)", r.can_shootswitch)
        self.restrict("Lightning (27)", r.can_shootswitch)
        self.restrict("Red Armor (47)", r.can_shootswitch)
        self.restrict("Secret (5)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Large Medkit (19)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Large Medkit (20)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Large Medkit (21)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Rockets (23)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Rockets (22)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Cells (25)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Cells (24)", r.can_shootswitch | r.bigjump_hard)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Spikes (64)",
                "Rocketlauncher (36)",
                "Spikes (63)",
                "Rockets (35)",
                "Rockets (34)",
                "Gold Key (6)",
                "Grenadelauncher (33)",
                "Secret (3)",
                "Quad Damage (17)",
                "Megahealth (18)",
            ],
        )
        self.connect(
            ret,
            past_silver_door_area,
            self.silver_key | r.bigjump_hard,
        )

        self.restrict("Secret (3)", r.can_shootswitch)
        self.restrict("Quad Damage (17)", r.can_shootswitch)
        self.restrict("Megahealth (18)", r.can_shootswitch)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Rocketlauncher (37)",
                "Exit",
                "All Kills (68)",
            ],
        )
        self.connect(ret, past_gold_door_area, self.gold_key | r.bigjump_hard)

        self.restrict(
            "All Kills (68)", r.difficult_combat & self.event("Button Pressed")
        )

        self.restrict("Exit", r.can_door)

        return ret
