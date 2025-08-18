from BaseClasses import Region

from ..base_classes import Q1Level


class start(Q1Level):
    name = "Introduction"
    mapfile = "start_id1"
    keys = []
    location_defs = [
        # {
        #     "id": 1,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 8554482791614197809,
        #     "mp": 0,
        # },
        # {
        #     "id": 2,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 4408941846051231574,
        #     "mp": 0,
        # },
        # {
        #     "id": 3,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 2133634421480314523,
        #     "mp": 0,
        # },
        {
            "id": 4,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 7702252194662057792,
            "mp": 0,
        },
        # {
        #    "id": 5,
        #    "name": "Red Armor (5)",
        #    "classname": "item_armorInv",
        #    "uuid": 11567654261167815312,
        #    "mp": 1,
        # },
        {
            "id": 6,
            "name": "Supernailgun (6)",
            "classname": "weapon_supernailgun",
            "uuid": 12283938966905339944,
            "mp": 1,
        },
        {
            "id": 7,
            "name": "Spikes (7)",
            "classname": "item_spikes",
            "uuid": 5293833601732845787,
            "mp": 1,
        },
        {
            "id": 8,
            "name": "Rocketlauncher (8)",
            "classname": "weapon_rocketlauncher",
            "uuid": 7797356151763012046,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Rockets (9)",
            "classname": "item_rockets",
            "uuid": 5571522683068716523,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Rockets (10)",
            "classname": "item_rockets",
            "uuid": 5045184638420809693,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Grenadelauncher (11)",
            "classname": "weapon_grenadelauncher",
            "uuid": 5738640518439932899,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Rockets (12)",
            "classname": "item_rockets",
            "uuid": 5317071348859639016,
            "mp": 1,
        },
        {
            "id": 13,
            "name": "Yellow Armor (13)",
            "classname": "item_armor2",
            "uuid": 6548995305049438614,
            "mp": 1,
        },
        {
            "id": 14,
            "name": "Supershotgun (14)",
            "classname": "weapon_supershotgun",
            "uuid": 634456960205030828,
            "mp": 1,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 16053886205206742672,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Nailgun (16)",
            "classname": "weapon_nailgun",
            "uuid": 17783439308660416983,
            "mp": 1,
        },
        {
            "id": 17,
            "name": "Spikes (17)",
            "classname": "item_spikes",
            "uuid": 3045570840349075165,
            "mp": 1,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 1669312620459949558,
            "mp": 1,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 14365545259318315654,
            "mp": 1,
        },
        {
            "id": 20,
            "name": "Small Medkit (20)",
            "classname": "item_health",
            "uuid": 8655772202010422082,
            "mp": 1,
        },
        # {
        #    "id": 21,
        #    "name": "Exit",
        #    "classname": "trigger_changelevel",
        #    "uuid": 12091055948511171065,
        #    "mp": 0,
        # },
        {
            "id": 22,
            "name": "Lightning (22)",
            "classname": "weapon_lightning",
            "uuid": 2904182144168352817,
            "mp": 1,
        },
        {
            "id": 23,
            "name": "Cells (23)",
            "classname": "item_cells",
            "uuid": 10359962796941261686,
            "mp": 1,
        },
        {
            "id": 24,
            "name": "Cells (24)",
            "classname": "item_cells",
            "uuid": 12055309585962255546,
            "mp": 1,
        },
        # {
        #    "id": 25,
        #    "name": "Quad Damage (25)",
        #    "classname": "item_artifact_super_damage",
        #    "uuid": 8300546414222186416,
        #    "mp": 1,
        # },
        # {
        #    "id": 26,
        #    "name": "Rockets (26)",
        #    "classname": "item_rockets",
        #    "uuid": 16791421654163229405,
        #    "mp": 1,
        # },
        # {
        #    "id": 27,
        #    "name": "Cells (27)",
        #    "classname": "item_cells",
        #    "uuid": 3605277900404970710,
        #    "mp": 1,
        # },
        # {
        #    "id": 28,
        #    "name": "Shells (28)",
        #    "classname": "item_shells",
        #    "uuid": 11452283698894795066,
        #    "mp": 1,
        # },
        # {
        #     "id": 29,
        #     "name": "Spikes (29)",
        #     "classname": "item_spikes",
        #     "uuid": 10803487414465753661,
        #     "mp": 1,
        # },
        # {
        #    "id": 30,
        #    "name": "Megahealth (30)",
        #    "classname": "item_health",
        #    "uuid": 3893124854393944523,
        #    "mp": 1,
        # },
        {
            "id": 31,
            "name": "All Kills (31)",
            "classname": "all_kills",
            "uuid": 11891092947304516721,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (19)",
                "Large Medkit (18)",
                "Shells (15)",
                "Supershotgun (14)",
                "Rocketlauncher (8)",
                "Grenadelauncher (11)",
                "Nailgun (16)",
                "Spikes (17)",
                "Small Medkit (20)",
                "All Kills (31)",
            ],
        )
        self.restrict("Nailgun (16)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Spikes (17)", r.can_jump | r.can_rj_hard | r.can_gj_extr)
        self.restrict("Small Medkit (20)", r.can_jump | r.can_rj_hard | r.can_gj_extr)

        dive_area = self.region(
            "Dive Area",
            [
                "Spikes (7)",
                "Supernailgun (6)",
                "Exit",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)
        self.restrict("Supernailgun (6)", r.can_door)
        self.restrict("Exit", r.can_door)

        past_door_area = self.region(
            "Past Door",
            [
                "Lightning (22)",
                "Cells (23)",
                "Rockets (9)",
                "Cells (24)",
                "Rockets (10)",
                "Rockets (12)",
                "Yellow Armor (13)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        return ret
