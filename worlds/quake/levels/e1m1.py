from BaseClasses import Region

from ..base_classes import Q1Level


class e1m1(Q1Level):
    name = "The Slipgate Complex"
    mapfile = "e1m1"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Green Armor (1)",
            "classname": "item_armor1",
            "uuid": 6610718619188254382,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Nailgun (2)",
            "classname": "weapon_nailgun",
            "uuid": 13320891562038546991,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Spikes (3)",
            "classname": "item_spikes",
            "uuid": 11912450227820366622,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Quad Damage (4)",
            "classname": "item_artifact_super_damage",
            "uuid": 9288653396544557442,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Megahealth (5)",
            "classname": "item_health",
            "uuid": 13350395829577830209,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Rocketlauncher (6)",
            "classname": "weapon_rocketlauncher",
            "uuid": 10084965594753817405,
            "mp": 1,
        },
        {
            "id": 7,
            "name": "Grenadelauncher (7)",
            "classname": "weapon_grenadelauncher",
            "uuid": 9627481481911349299,
            "mp": 1,
        },
        {
            "id": 8,
            "name": "Rockets (8)",
            "classname": "item_rockets",
            "uuid": 8051529558218231085,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Supernailgun (9)",
            "classname": "weapon_supernailgun",
            "uuid": 548979412660274366,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Supershotgun (10)",
            "classname": "weapon_supershotgun",
            "uuid": 661354647876697793,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 8615351773526995969,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Small Medkit (12)",
            "classname": "item_health",
            "uuid": 15649103764220925922,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Large Medkit (13)",
            "classname": "item_health",
            "uuid": 5934872414195265557,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Large Medkit (14)",
            "classname": "item_health",
            "uuid": 12539581847147454997,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 3008841193810691088,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 14600749735767863259,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Small Medkit (17)",
            "classname": "item_health",
            "uuid": 4671148356986342893,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Small Medkit (18)",
            "classname": "item_health",
            "uuid": 12948082842089389505,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Nailgun (19)",
            "classname": "weapon_nailgun",
            "uuid": 2314463324332959819,
            "mp": 1,
        },
        {
            "id": 20,
            "name": "Spikes (20)",
            "classname": "item_spikes",
            "uuid": 11192222604772713992,
            "mp": 1,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 11180455415551487437,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 13259462705102753645,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Small Medkit (23)",
            "classname": "item_health",
            "uuid": 13358390004484254425,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Rockets (24)",
            "classname": "item_rockets",
            "uuid": 3487654706338424238,
            "mp": 1,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 3047006270236727183,
            "mp": 1,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 7724601833083741887,
            "mp": 1,
        },
        {
            "id": 27,
            "name": "Invulnerability (27)",
            "classname": "item_artifact_invulnerability",
            "uuid": 6840728164698730359,
            "mp": 1,
        },
        {
            "id": 28,
            "name": "Biosuit (28)",
            "classname": "item_artifact_envirosuit",
            "uuid": 5321694546448041705,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Rockets (29)",
            "classname": "item_rockets",
            "uuid": 4767999347332704160,
            "mp": 1,
        },
        {
            "id": 30,
            "name": "Megahealth (30)",
            "classname": "item_health",
            "uuid": 17345129212048338456,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Supershotgun (31)",
            "classname": "weapon_supershotgun",
            "uuid": 17275541876409197547,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Shells (32)",
            "classname": "item_shells",
            "uuid": 15986156168938543858,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Small Medkit (33)",
            "classname": "item_health",
            "uuid": 2432654977108383760,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 8830019655236077195,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Secret (35)",
            "classname": "trigger_secret",
            "uuid": 17916216988706394990,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Secret (36)",
            "classname": "trigger_secret",
            "uuid": 6062628971448709872,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Secret (37)",
            "classname": "trigger_secret",
            "uuid": 9575803044735894181,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Secret (38)",
            "classname": "trigger_secret",
            "uuid": 5924692660255888563,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Secret (39)",
            "classname": "trigger_secret",
            "uuid": 6784646313187716299,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Secret (40)",
            "classname": "trigger_secret",
            "uuid": 16226739629616339165,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Small Medkit (41)",
            "classname": "item_health",
            "uuid": 12036445004670391445,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 15870832541145036607,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Small Medkit (43)",
            "classname": "item_health",
            "uuid": 17924871343896339303,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Yellow Armor (44)",
            "classname": "item_armor2",
            "uuid": 13722753575330671210,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "All Kills (45)",
            "classname": "all_kills",
            "uuid": 6624414443276030093,
            "mp": 0,
        },
    ]

    must_bio = True
    must_invuln = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Nailgun (19)",
            ],
        )

        secret_ledge = self.region(
            "Ledge Secret Area",
            [
                "Secret (35)",
                "Shells (34)",
            ],
        )
        self.connect(ret, secret_ledge, r.jump & r.can_shootswitch)

        start_ledge = self.region(
            "Start Ledge Area",
            [
                "Spikes (20)",
                "Shells (32)",
                "Green Armor (1)",
            ],
        )
        self.connect(ret, start_ledge, r.jump)

        # Requires door + button to go down the elevator
        past_door = self.region(
            "Past Start Door",
            [
                "Large Medkit (21)",
                "Large Medkit (22)",
                "Supershotgun (10)",
                "Small Medkit (33)",
                "Secret (36)",
                "Megahealth (5)",
                "Shells (11)",
                "Small Medkit (23)",
                "Rockets (24)",
                "Nailgun (2)",
                "Rocketlauncher (6)",
                "Shells (25)",
                "Rockets (26)",
                "Spikes (3)",
                "Small Medkit (43)",
                "Biosuit (28)",
                "Small Medkit (18)",
                "Spikes (15)",
                "Large Medkit (16)",
                "Small Medkit (17)",
                "Supernailgun (9)",
                # shootswitch things
                "Small Medkit (41)",
                "Secret (39)",
                "Quad Damage (4)",
                "Secret (40)",
                "Supershotgun (31)",
                "Exit",
                # can get all kills with shotgun and backpack drops
                "All Kills (45)",
            ],
        )
        self.connect(ret, past_door, r.can_button & r.can_door)
        self.restrict("All Kills (45)", r.backpack(5))

        self.restrict("Small Medkit (41)", r.can_shootswitch | r.bigjump)

        self.restrict("Supershotgun (31)", r.can_shootswitch)
        self.restrict("Secret (40)", r.can_shootswitch)

        self.restrict("Secret (39)", r.can_shootswitch)
        self.restrict("Quad Damage (4)", r.can_shootswitch)

        upper_spiral = self.region(
            "Upper Spiral Area",
            [
                "Secret (38)",
                "Megahealth (30)",
            ],
        )
        # very difficult in-place grenade jump when standing on top of the light/switch
        self.connect(
            past_door,
            upper_spiral,
            r.can_jump | r.can_rj_ez | r.can_gj_extr,
        )

        spiral_dive = self.region(
            "Spiral Dive Area",
            [
                "Secret (37)",
                "Grenadelauncher (7)",
                "Large Medkit (14)",
                "Rockets (8)",
                "Small Medkit (12)",
                "Large Medkit (13)",
                "Yellow Armor (44)",
                "Rockets (29)",
            ],
        )
        # Can dive through with 100 health
        self.connect(
            past_door,
            spiral_dive,
            r.jump
            & r.can_dive
            & ((r.difficulty("hard") | r.biosuit(1) | r.invuln(1) | r.heal(75))),
        )

        above_door = self.region(
            "Above Entrance Door Area",
            [
                "Invulnerability (27)",
            ],
        )

        # special item above entrance door, can teleport through secret or jump up
        self.connect(
            past_door,
            above_door,
            (r.bigjump)
            | (
                r.jump
                & r.can_dive
                & ((r.difficulty("hard") | r.biosuit(1) | r.invuln(1) | r.heal(75)))
            ),
        )

        return ret
