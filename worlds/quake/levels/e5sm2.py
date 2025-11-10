from BaseClasses import Region

from ..base_classes import Q1Level


class e5sm2(Q1Level):
    name = "The House of Doom"
    mapfile = "e5sm2"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Spikes (1)",
            "classname": "item_spikes",
            "uuid": 16427463483966761401,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Spikes (2)",
            "classname": "item_spikes",
            "uuid": 18332767007577359160,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Supershotgun (3)",
            "classname": "weapon_supershotgun",
            "uuid": 9111189965809134117,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Supernailgun (4)",
            "classname": "weapon_supernailgun",
            "uuid": 17810484804067055904,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 2162427973178765648,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Shells (6)",
            "classname": "item_shells",
            "uuid": 12808388924752834773,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Spikes (7)",
            "classname": "item_spikes",
            "uuid": 2831612606283325971,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Spikes (8)",
            "classname": "item_spikes",
            "uuid": 7891044776547357068,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Megahealth (9)",
            "classname": "item_health",
            "uuid": 1303912078686936893,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Shells (10)",
            "classname": "item_shells",
            "uuid": 14398661993522977882,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 13941912860098506394,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 2359884624256569050,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 9306620015047623373,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Cells (14)",
            "classname": "item_cells",
            "uuid": 12190170701818500905,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 992967450002807762,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Shells (16)",
            "classname": "item_shells",
            "uuid": 9227406509417754572,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Rockets (17)",
            "classname": "item_rockets",
            "uuid": 18334168211339440831,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Rockets (18)",
            "classname": "item_rockets",
            "uuid": 15441625496538532158,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Rocketlauncher (19)",
            "classname": "weapon_rocketlauncher",
            "uuid": 3465604283587299934,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 1638437983310400596,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Yellow Armor (21)",
            "classname": "item_armor2",
            "uuid": 4931797114691142337,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Rockets (22)",
            "classname": "item_rockets",
            "uuid": 7240444077427812730,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 2698371123415517621,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 1484491440096469536,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Cells (25)",
            "classname": "item_cells",
            "uuid": 2986229280388812830,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Lightning (26)",
            "classname": "weapon_lightning",
            "uuid": 11632809587343164279,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Grenadelauncher (27)",
            "classname": "weapon_grenadelauncher",
            "uuid": 9819925085863273588,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Invulnerability (28)",
            "classname": "item_artifact_invulnerability",
            "uuid": 3673525261942203536,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 6860598338526600126,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 15367310268351277248,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 14001426085073220699,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 14541209562224676307,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Secret (33)",
            "classname": "trigger_secret",
            "uuid": 8239463279931811773,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "All Kills (34)",
            "classname": "all_kills",
            "uuid": 2530812192175109947,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (3)",
                "Yellow Armor (21)",
                "Lightning (26)",
                "Cells (25)",
                "Large Medkit (23)",
                "Large Medkit (24)",
                "Shells (30)",
                "Shells (10)",
                "Shells (11)",
                "Spikes (1)",
                "Spikes (2)",
                "Supernailgun (4)",
                "Large Medkit (29)",
                "Grenadelauncher (27)",
                "Rockets (22)",
                "Shells (12)",
                "Shells (13)",
                "Rocketlauncher (19)",
                "Large Medkit (32)",
                "Large Medkit (31)",
                "Spikes (7)",
                "Spikes (8)",
                "Shells (5)",
                "Shells (6)",
                "Secret (33)",
                "Invulnerability (28)",
            ],
        )
        self.restrict("Secret (33)", r.can_shootswitch)
        self.restrict("Invulnerability (28)", r.can_shootswitch)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Cells (14)",
                "Megahealth (9)",
                "Shells (15)",
                "Shells (16)",
                "Rockets (18)",
                "Rockets (17)",
                "Exit",
                "All Kills (34)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door & r.can_button)
        # TODO: excluding grenade jumps for this currently
        self.restrict("Shells (15)", r.can_jump | r.can_rj_hard)
        self.restrict("Shells (16)", r.can_jump | r.can_rj_hard)
        self.restrict("Rockets (18)", r.can_jump | r.can_rj_hard)
        self.restrict("Rockets (17)", r.can_jump | r.can_rj_hard)

        self.restrict("Exit", r.can_jump | r.can_rj_hard)

        self.restrict("All Kills (34)", r.difficult_combat)

        return ret
