from BaseClasses import Region

from ..base_classes import Q1Level


class e2m6(Q1Level):
    name = "The Dismal Oubliette"
    mapfile = "e2m6"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Gold Key (1)",
            "classname": "item_key2",
            "uuid": 5435099613562408699,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Sigil (2)",
            "classname": "item_sigil",
            "uuid": 15438837226874621034,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Supershotgun (3)",
            "classname": "weapon_supershotgun",
            "uuid": 16985491965581494575,
            "mp": 1,
        },
        {
            "id": 4,
            "name": "Secret (4)",
            "classname": "trigger_secret",
            "uuid": 2768521465823243188,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Invulnerability (5)",
            "classname": "item_artifact_invulnerability",
            "uuid": 17643219780063590623,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Megahealth (6)",
            "classname": "item_health",
            "uuid": 5030798606021350106,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Rockets (7)",
            "classname": "item_rockets",
            "uuid": 12299129550092297768,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Spikes (8)",
            "classname": "item_spikes",
            "uuid": 10401613658172094211,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Cells (9)",
            "classname": "item_cells",
            "uuid": 17005396291213635365,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Cells (10)",
            "classname": "item_cells",
            "uuid": 1208774540302612162,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Secret (11)",
            "classname": "trigger_secret",
            "uuid": 4658931274799666312,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Quad Damage (12)",
            "classname": "item_artifact_super_damage",
            "uuid": 17589802478298965306,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Rocketlauncher (13)",
            "classname": "weapon_rocketlauncher",
            "uuid": 12282079294329251222,
            "mp": 1,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 5326895085291115902,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 10785906880961620112,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Cells (16)",
            "classname": "item_cells",
            "uuid": 7905626464798991984,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Yellow Armor (17)",
            "classname": "item_armor2",
            "uuid": 13775144079922596917,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Shells (18)",
            "classname": "item_shells",
            "uuid": 18333751613534715297,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 4404051456278722577,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 6345568483823065369,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 12023977484478259608,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 4638456358609364849,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Rockets (23)",
            "classname": "item_rockets",
            "uuid": 9254899823828921187,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 4765558837466920820,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Rockets (25)",
            "classname": "item_rockets",
            "uuid": 7210560738047190331,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 1740217165822529438,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 6309512418729293943,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Small Medkit (28)",
            "classname": "item_health",
            "uuid": 16386287362017934800,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 14056245860618441987,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Large Medkit (30)",
            "classname": "item_health",
            "uuid": 944756586801313857,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 14501153142034680442,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 6215850116986806129,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 16248524060796006269,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 11332748866720768557,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Spikes (35)",
            "classname": "item_spikes",
            "uuid": 9507933440351467824,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Rockets (36)",
            "classname": "item_rockets",
            "uuid": 1026551650593883760,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Rockets (37)",
            "classname": "item_rockets",
            "uuid": 7783745338884515318,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Shells (38)",
            "classname": "item_shells",
            "uuid": 15349912403504332787,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 17214055932742296417,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 14670634761940444560,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 404530624217518188,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Shells (42)",
            "classname": "item_shells",
            "uuid": 16686301612359351492,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 10530789726966109461,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Yellow Armor (44)",
            "classname": "item_armor2",
            "uuid": 14043832435618685904,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Lightning (45)",
            "classname": "weapon_lightning",
            "uuid": 14364718657187398572,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Supernailgun (46)",
            "classname": "weapon_supernailgun",
            "uuid": 17099603803064314018,
            "mp": 1,
        },
        {
            "id": 47,
            "name": "Spikes (47)",
            "classname": "item_spikes",
            "uuid": 17601467055715093890,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Shells (48)",
            "classname": "item_shells",
            "uuid": 1284230159453919889,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Spikes (49)",
            "classname": "item_spikes",
            "uuid": 8211511613653953248,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Large Medkit (50)",
            "classname": "item_health",
            "uuid": 14382471845198807322,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Large Medkit (51)",
            "classname": "item_health",
            "uuid": 6386476306684059875,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 14347906500046098286,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 12168460323356762570,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Shells (54)",
            "classname": "item_shells",
            "uuid": 12260153580295760661,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Rockets (55)",
            "classname": "item_rockets",
            "uuid": 16192651672794536307,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Spikes (56)",
            "classname": "item_spikes",
            "uuid": 1162713239086965446,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 11746528704640664653,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 11628758695467411202,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Large Medkit (59)",
            "classname": "item_health",
            "uuid": 5564204118688374101,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Large Medkit (60)",
            "classname": "item_health",
            "uuid": 12794383394308240602,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Small Medkit (61)",
            "classname": "item_health",
            "uuid": 2935348102511805710,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 4601968521699766989,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Rockets (63)",
            "classname": "item_rockets",
            "uuid": 13038826509229691306,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Shells (64)",
            "classname": "item_shells",
            "uuid": 13517879174352908894,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Cells (65)",
            "classname": "item_cells",
            "uuid": 12074155132005907941,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Small Medkit (66)",
            "classname": "item_health",
            "uuid": 16343910575553774354,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Cells (67)",
            "classname": "item_cells",
            "uuid": 18079275408440965093,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Megahealth (68)",
            "classname": "item_health",
            "uuid": 11854967658115399639,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 5178792572392152397,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Spikes (70)",
            "classname": "item_spikes",
            "uuid": 13328221737392079989,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Spikes (71)",
            "classname": "item_spikes",
            "uuid": 17071545570712519699,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Spikes (72)",
            "classname": "item_spikes",
            "uuid": 13470497886850113481,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Spikes (73)",
            "classname": "item_spikes",
            "uuid": 11511387431494138125,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Rockets (74)",
            "classname": "item_rockets",
            "uuid": 13864322547433462912,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Large Medkit (75)",
            "classname": "item_health",
            "uuid": 11400908102092744226,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Spikes (76)",
            "classname": "item_spikes",
            "uuid": 12098964028303155865,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Quad Damage (77)",
            "classname": "item_artifact_super_damage",
            "uuid": 5605220978689694291,
            "mp": 1,
        },
        {
            "id": 78,
            "name": "Grenadelauncher (78)",
            "classname": "weapon_grenadelauncher",
            "uuid": 7288301709086225016,
            "mp": 1,
        },
        {
            "id": 79,
            "name": "Green Armor (79)",
            "classname": "item_armor1",
            "uuid": 7692398829496163578,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Shells (80)",
            "classname": "item_shells",
            "uuid": 2001220293625008128,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Large Medkit (81)",
            "classname": "item_health",
            "uuid": 14265511664691216755,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Large Medkit (82)",
            "classname": "item_health",
            "uuid": 14788860394989737296,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "All Kills (83)",
            "classname": "all_kills",
            "uuid": 6173825696376142737,
            "mp": 0,
        },
    ]
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (82)",
                "Shells (80)",
                "Quad Damage (77)",
                "Green Armor (79)",
                "Large Medkit (81)",
            ],
        )

        first_bridge_area = self.region(
            "First Bridge",
            [
                "Shells (14)",
                "Yellow Armor (17)",
                "Cells (16)",
                "Spikes (15)",
                "Large Medkit (29)",
                "Spikes (19)",
                "Shells (18)",
                "Rockets (23)",
                "Large Medkit (22)",
                "Large Medkit (21)",
                "Large Medkit (20)",
                "Large Medkit (40)",
                "Large Medkit (41)",
            ],
        )
        self.restrict("Large Medkit (40)", r.can_dive)
        self.restrict("Large Medkit (41)", r.can_dive)
        self.connect(
            ret,
            first_bridge_area,
            r.can_door | (r.can_gj_extr | r.can_rj_hard) | r.bigjump_hard,
        )

        castle_area = self.region(
            "Castle Area",
            [
                "Cells (9)",
                "Cells (10)",
                "Rockets (25)",
            ],
        )
        self.connect(first_bridge_area, castle_area, r.can_button)

        castle_exit_area = self.region(
            "Castle Exit",
            [
                "Spikes (39)",
                "Shells (38)",
                "Large Medkit (43)",
            ],
        )
        self.connect(castle_area, castle_exit_area, r.bigjump_hard)

        castle_entrance_area = self.region(
            "Castle Entrance",
            [
                "Rockets (26)",
                "Large Medkit (30)",
                "Shells (24)",
                "Large Medkit (31)",
                "Large Medkit (27)",
                "Small Medkit (28)",
                "Shells (33)",
                "Large Medkit (32)",
            ],
        )
        self.connect(castle_area, castle_entrance_area, r.can_dive)

        castle_climb_area = self.region(
            "Castle Climb",
            [
                "Large Medkit (34)",
                "Rocketlauncher (13)",
                "Spikes (35)",
                "Rockets (36)",
            ],
        )
        self.connect(
            castle_entrance_area,
            castle_climb_area,
            r.can_jump | r.can_gj_extr | r.can_rj_hard,
        )

        castle_bar_area = self.region(
            "Castle Bar Area",
            [
                "Shells (42)",
                "Grenadelauncher (78)",
                "Rockets (37)",
                "Secret (11)",
                "Quad Damage (12)",
            ],
        )
        self.restrict("Secret (11)", r.can_dive)
        self.restrict("Quad Damage (12)", r.can_dive)

        self.connect(castle_climb_area, castle_bar_area, r.can_button)
        self.connect(castle_bar_area, castle_exit_area, r.can_door)

        second_bridge_area = self.region(
            "Second Bridge",
            [
                "Yellow Armor (44)",
                "Spikes (47)",
                "Shells (48)",
                "Spikes (49)",
                "Large Medkit (50)",
                "Large Medkit (51)",
            ],
        )
        self.connect(
            first_bridge_area,
            second_bridge_area,
            (r.can_gj_extr | r.can_rj_hard) | r.bigjump_hard,
        )
        self.connect(castle_bar_area, second_bridge_area, r.can_door)

        second_floor_area = self.region(
            "Second Floor",
            [
                "Large Medkit (52)",
                "Large Medkit (53)",
                "Shells (54)",
                "Spikes (56)",
                "Rockets (55)",
                "Large Medkit (58)",
                "Shells (57)",
            ],
        )
        self.connect(second_bridge_area, second_floor_area, r.can_button)

        second_floor_secret_area = self.region(
            "Second Floor Secret",
            [
                "Secret (4)",
                "Spikes (8)",
                "Rockets (7)",
                "Megahealth (6)",
                "Invulnerability (5)",
            ],
        )
        self.connect(second_floor_area, second_floor_secret_area, r.can_shootswitch)

        third_floor_area = self.region(
            "Third Floor",
            [
                "Lightning (45)",
                "Spikes (70)",
                "Large Medkit (60)",
                "Large Medkit (59)",
                "Spikes (71)",
                "Spikes (72)",
                "Small Medkit (61)",
                "Spikes (62)",
                "Gold Key (1)",
            ],
        )
        self.connect(second_floor_area, third_floor_area)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Supershotgun (3)",
                "Shells (64)",
                "Cells (65)",
                "Rockets (63)",
                "Small Medkit (66)",
            ],
        )
        self.connect(second_bridge_area, past_gold_door_area, self.gold_key)

        third_bridge_area = self.region(
            "Third Bridge",
            [
                "Megahealth (68)",
                "Spikes (73)",
                "Cells (67)",
                "Supernailgun (46)",
                "Rockets (74)",
            ],
        )
        self.connect(
            first_bridge_area,
            third_bridge_area,
            (r.can_gj_extr | r.can_rj_hard) | r.bigjump_hard,
        )
        self.connect(past_gold_door_area, third_bridge_area)

        past_big_elevator_area = self.region(
            "Past Big Elevator",
            [
                "Large Medkit (75)",
                "Spikes (76)",
                "Sigil (2)",
                "Exit",
                "All Kills (83)",
            ],
        )
        self.connect(third_bridge_area, past_big_elevator_area, r.can_door)
        self.restrict(
            "All Kills (83)",
            r.can_dive & r.can_button & self.gold_key & r.difficult_combat,
        )

        return ret
