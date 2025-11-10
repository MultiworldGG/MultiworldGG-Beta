from BaseClasses import Region

from ..base_classes import Q1Level


class e5m2(Q1Level):
    name = "The Power Supply"
    mapfile = "e5m2"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Green Armor (1)",
            "classname": "item_armor1",
            "uuid": 17329273601367769873,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Secret (2)",
            "classname": "trigger_secret",
            "uuid": 7529456031693229975,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Nailgun (3)",
            "classname": "weapon_nailgun",
            "uuid": 16784275686467452827,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Spikes (4)",
            "classname": "item_spikes",
            "uuid": 13200641442792702939,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Spikes (5)",
            "classname": "item_spikes",
            "uuid": 6843304689839773372,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Supershotgun (6)",
            "classname": "weapon_supershotgun",
            "uuid": 4769341577534833394,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Invisibility (7)",
            "classname": "item_artifact_invisibility",
            "uuid": 7415061933247581734,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Secret (8)",
            "classname": "trigger_secret",
            "uuid": 8866763655681253577,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Quad Damage (9)",
            "classname": "item_artifact_super_damage",
            "uuid": 17993333037767449233,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Large Medkit (10)",
            "classname": "item_health",
            "uuid": 9849722142783924155,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 9152273587367698577,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Megahealth (12)",
            "classname": "item_health",
            "uuid": 1064025097972657263,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Small Medkit (13)",
            "classname": "item_health",
            "uuid": 7524869836833400579,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 5409031769145156809,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Shells (15)",
            "classname": "item_shells",
            "uuid": 12428551537894437821,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Small Medkit (16)",
            "classname": "item_health",
            "uuid": 1902457709471515013,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 3976643073800170302,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Small Medkit (18)",
            "classname": "item_health",
            "uuid": 4427149419037133780,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 2701202710048943143,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Spikes (20)",
            "classname": "item_spikes",
            "uuid": 10606472659936421072,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Green Armor (21)",
            "classname": "item_armor1",
            "uuid": 12259327765976468398,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Small Medkit (22)",
            "classname": "item_health",
            "uuid": 18059751550355456557,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Small Medkit (23)",
            "classname": "item_health",
            "uuid": 1257777195414990457,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 1892854044053457313,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Large Medkit (25)",
            "classname": "item_health",
            "uuid": 11389307195720653385,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Large Medkit (26)",
            "classname": "item_health",
            "uuid": 7184775464632995040,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Shells (27)",
            "classname": "item_shells",
            "uuid": 9683807754841607123,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 14516762939009688384,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Spikes (29)",
            "classname": "item_spikes",
            "uuid": 7546096702668299139,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Small Medkit (30)",
            "classname": "item_health",
            "uuid": 5657196898274504399,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Gold Key (31)",
            "classname": "item_key2",
            "uuid": 4458034210847930475,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Shells (32)",
            "classname": "item_shells",
            "uuid": 15814794453093503347,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 7923829026882428017,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Spikes (34)",
            "classname": "item_spikes",
            "uuid": 6328036444717994407,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 5343675257374002984,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 4180902387406130053,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Green Armor (37)",
            "classname": "item_armor1",
            "uuid": 11460375337392119277,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Small Medkit (38)",
            "classname": "item_health",
            "uuid": 14325165661678335531,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Shells (39)",
            "classname": "item_shells",
            "uuid": 11884578291100859072,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 5209313165320094874,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Yellow Armor (41)",
            "classname": "item_armor2",
            "uuid": 1333075817356868866,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Secret (42)",
            "classname": "trigger_secret",
            "uuid": 1771298407343477670,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Secret (43)",
            "classname": "trigger_secret",
            "uuid": 2936848277302139248,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 8856599356664505898,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Small Medkit (45)",
            "classname": "item_health",
            "uuid": 14540976226610592067,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 15414689152685014661,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "All Kills (47)",
            "classname": "all_kills",
            "uuid": 10401866007363014359,
            "mp": 0,
        },
    ]
    events = ["Power On Button"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Small Medkit (13)",
                "Shells (15)",
                "Shells (14)",
                "Green Armor (1)",
                "Small Medkit (16)",
                "Shells (17)",
                "Secret (2)",
                "Small Medkit (18)",
                "Nailgun (3)",
                "Spikes (4)",
                "Spikes (5)",
            ],
        )

        dive_area = self.region(
            "Dive Area",
            [
                "Small Medkit (13)",
                "Shells (15)",
                "Shells (14)",
                "Green Armor (1)",
                "Small Medkit (16)",
                "Shells (17)",
                "Secret (2)",
                "Small Medkit (18)",
                "Nailgun (3)",
                "Spikes (4)",
                "Spikes (5)",
                "Secret (42)",
                "Yellow Armor (41)",
                "Large Medkit (25)",
                "Secret (8)",
                "Invisibility (7)",
                "Quad Damage (9)",
                "Shells (11)",
                "Large Medkit (10)",
                "Small Medkit (38)",
                "Spikes (36)",
                "Shells (39)",
                "Shells (40)",
                "Green Armor (37)",
                "Power On Button",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)
        self.restrict("Power On Button", r.can_button)

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Secret (42)",
                "Yellow Armor (41)",
            ],
        )
        self.connect(ret, shootswitch_area, r.can_shootswitch)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Spikes (34)",
                "Shells (33)",
                "Megahealth (12)",
                "Secret (46)",
                "Gold Key (31)",
                "Shells (44)",
                "Shells (32)",
            ],
        )
        self.connect(
            ret,
            past_door_area,
            (r.can_door & self.event("Power On Button")) | (r.can_dive & r.can_rj_hard),
        )

        past_side_door_area = self.region(
            "Past Side Door",
            [
                "Supershotgun (6)",
                "Spikes (20)",
                "Spikes (19)",
                "Small Medkit (23)",
                "Small Medkit (22)",
                "Shells (24)",
                "Secret (43)",
                "Green Armor (21)",
                "Small Medkit (30)",
                "Shells (27)",
                "Shells (28)",
                "Large Medkit (26)",
                "Spikes (29)",
                "All Kills (47)",
            ],
        )
        self.connect(ret, past_side_door_area, self.event("Power On Button"))
        self.restrict("Shells (27)", r.can_jump | r.can_gj_extr | r.can_rj_hard)
        self.restrict("Shells (28)", r.can_jump | r.can_gj_extr | r.can_rj_hard)
        self.restrict("Large Medkit (26)", r.can_jump | r.can_gj_extr | r.can_rj_hard)
        self.restrict("Spikes (29)", r.can_jump | r.can_gj_extr | r.can_rj_hard)
        self.restrict("All Kills (47)", r.backpack(5))

        self.connect(shootswitch_area, past_door_area, r.jump)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Small Medkit (45)",
                "Exit",
            ],
        )
        self.connect(
            past_door_area,
            past_gold_door_area,
            self.gold_key
            & (
                r.can_button
                | (
                    r.difficulty("extreme")
                    & r.invuln(1)
                    & r.quad_dmg(1)
                    & r.bigjump_hard
                )
            ),
        )

        return ret
