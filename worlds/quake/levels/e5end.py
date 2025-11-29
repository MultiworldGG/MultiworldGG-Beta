from BaseClasses import Region

from ..base_classes import Q1Level


class e5end(Q1Level):
    name = "The Year Zero"
    mapfile = "e5end"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Lightning (1)",
            "classname": "weapon_lightning",
            "uuid": 4187375333631235227,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Supershotgun (2)",
            "classname": "weapon_supershotgun",
            "uuid": 11980174830964142303,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Shells (3)",
            "classname": "item_shells",
            "uuid": 2242024958209430567,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Shells (4)",
            "classname": "item_shells",
            "uuid": 11244706772655589622,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Yellow Armor (5)",
            "classname": "item_armor2",
            "uuid": 12679212541460604954,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Spikes (6)",
            "classname": "item_spikes",
            "uuid": 3316819304394932271,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Spikes (7)",
            "classname": "item_spikes",
            "uuid": 12833818593052410717,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Nailgun (8)",
            "classname": "weapon_nailgun",
            "uuid": 11609618231414755972,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Cells (9)",
            "classname": "item_cells",
            "uuid": 9066250306175072230,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Cells (10)",
            "classname": "item_cells",
            "uuid": 250860830737184073,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Cells (11)",
            "classname": "item_cells",
            "uuid": 5798414241680087520,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Rockets (12)",
            "classname": "item_rockets",
            "uuid": 11539240484721193515,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Grenadelauncher (13)",
            "classname": "weapon_grenadelauncher",
            "uuid": 833992118332714043,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Quad Damage (14)",
            "classname": "item_artifact_super_damage",
            "uuid": 9144504851476346493,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Rockets (15)",
            "classname": "item_rockets",
            "uuid": 11194102207365938864,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 11668376520133070286,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Secret (17)",
            "classname": "trigger_secret",
            "uuid": 9769849432335667460,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Rocketlauncher (18)",
            "classname": "weapon_rocketlauncher",
            "uuid": 11679970601862695257,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 2232006875201806801,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Supernailgun (20)",
            "classname": "weapon_supernailgun",
            "uuid": 6702412408980743278,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Secret (21)",
            "classname": "trigger_secret",
            "uuid": 17614924346764027258,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 4118037703423617689,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Small Medkit (23)",
            "classname": "item_health",
            "uuid": 6996728737637296952,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Spikes (24)",
            "classname": "item_spikes",
            "uuid": 3306915646103144016,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Spikes (25)",
            "classname": "item_spikes",
            "uuid": 7257420632249536006,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 10983776157475979193,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 5457453264950285805,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 11081246143704012811,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 3795044655720246345,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 16381402769136278641,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 12135959970626270360,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Green Armor (32)",
            "classname": "item_armor1",
            "uuid": 16364344295944089744,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Spikes (33)",
            "classname": "item_spikes",
            "uuid": 2778084863960035252,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Spikes (34)",
            "classname": "item_spikes",
            "uuid": 11436324267104200817,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "All Kills (35)",
            "classname": "all_kills",
            "uuid": 4350877316451410334,
            "mp": 0,
        },
    ]
    must_bio = True
    must_invuln = True
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )

        dive_area = self.region(
            "Dive Area",
            [
                "Spikes (7)",
                "Spikes (6)",
                "Nailgun (8)",
                "Yellow Armor (5)",
                "Secret (17)",
                "Lightning (1)",
                "Quad Damage (14)",
                "Secret (21)",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)

        upper_area = self.region(
            "Upper Area",
            [
                "Grenadelauncher (13)",
                "Rockets (12)",
                "Rockets (15)",
                "Large Medkit (16)",
                "Supershotgun (2)",
                "Shells (3)",
                "Shells (4)",
                "Cells (11)",
                "Cells (10)",
                "Cells (9)",
            ],
        )
        self.connect(dive_area, upper_area)
        self.connect(ret, upper_area, r.can_rj_hard)

        final_area = self.region(
            "Final Area",
            [
                "Green Armor (32)",
                "Supernailgun (20)",
                "Spikes (34)",
                "Spikes (33)",
                "Small Medkit (23)",
                "Large Medkit (22)",
                "Shells (31)",
                "Shells (30)",
                "Spikes (25)",
                "Spikes (24)",
                "Large Medkit (19)",
                "Rocketlauncher (18)",
            ],
        )
        self.connect(upper_area, final_area, r.difficult_combat | r.invuln(2))

        self.restrict("Large Medkit (19)", r.biosuit(1) | r.invuln(1))
        self.restrict("Rocketlauncher (18)", r.biosuit(1) | r.invuln(1))

        past_door_area = self.region(
            "Past Door Area",
            [
                "Shells (29)",
                "Shells (28)",
                "Large Medkit (27)",
                "Exit",
                "All Kills (35)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door & r.can_button)

        self.restrict("Exit", r.backpack(2))
        self.restrict("All Kills (35)", r.difficult_combat)

        return ret
