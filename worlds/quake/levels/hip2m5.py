from BaseClasses import Region

from ..base_classes import Q1Level


class hip2m5(Q1Level):
    name = "Mortum's Keep"
    mapfile = "hip2m5"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Secret (1)",
            "classname": "trigger_secret",
            "uuid": 2882061549783144377,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 2015910720317653005,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Secret (3)",
            "classname": "trigger_secret",
            "uuid": 10655195177412317000,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Proximity (4)",
            "classname": "weapon_proximity_gun",
            "uuid": 11501958799096538200,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Rockets (5)",
            "classname": "item_rockets",
            "uuid": 15880724586068616852,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Quad Damage (6)",
            "classname": "item_artifact_super_damage",
            "uuid": 16633840624568147797,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Supershotgun (7)",
            "classname": "weapon_supershotgun",
            "uuid": 9967559467600065682,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 8734378154740947253,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Cells (9)",
            "classname": "item_cells",
            "uuid": 15700744516456447433,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Cells (10)",
            "classname": "item_cells",
            "uuid": 17949335444680403423,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Lightning (11)",
            "classname": "weapon_lightning",
            "uuid": 3191999514291560304,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 5159447493954819886,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Spikes (13)",
            "classname": "item_spikes",
            "uuid": 6232882801971238066,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 2569728931726791904,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 10895241150327564486,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 13834031302918034304,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 2064908089532171671,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Shells (18)",
            "classname": "item_shells",
            "uuid": 229357092763644427,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Yellow Armor (19)",
            "classname": "item_armor2",
            "uuid": 6472328760625169723,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Yellow Armor (20)",
            "classname": "item_armor2",
            "uuid": 3835348382778552454,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Supernailgun (21)",
            "classname": "weapon_supernailgun",
            "uuid": 670598040751117243,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Spikes (22)",
            "classname": "item_spikes",
            "uuid": 11303179624068301503,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Spikes (23)",
            "classname": "item_spikes",
            "uuid": 712920737877442415,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Secret (24)",
            "classname": "trigger_secret",
            "uuid": 16856178413701279420,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Silver Key (25)",
            "classname": "item_key1",
            "uuid": 2248051865875505297,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Large Medkit (26)",
            "classname": "item_health",
            "uuid": 5603250634465322466,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 13685433049944092484,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 3370880537224251575,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 4762529494785418710,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Spikes (30)",
            "classname": "item_spikes",
            "uuid": 5105553229046244951,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Rockets (31)",
            "classname": "item_rockets",
            "uuid": 9083679330490896697,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Rockets (32)",
            "classname": "item_rockets",
            "uuid": 10299810625759375021,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Rocketlauncher (33)",
            "classname": "weapon_rocketlauncher",
            "uuid": 6190916573506160836,
            "mp": 1,
        },
        {
            "id": 34,
            "name": "Nailgun (34)",
            "classname": "weapon_nailgun",
            "uuid": 11249804593674825349,
            "mp": 1,
        },
        {
            "id": 35,
            "name": "Spikes (35)",
            "classname": "item_spikes",
            "uuid": 4159903486804360005,
            "mp": 1,
        },
        {
            "id": 36,
            "name": "Gold Key (36)",
            "classname": "item_key2",
            "uuid": 17842462235405329663,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Secret (37)",
            "classname": "trigger_secret",
            "uuid": 1500170625672317096,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 1422941882362934823,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 62752637255000176,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Rockets (40)",
            "classname": "item_rockets",
            "uuid": 722397865110083825,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Rockets (41)",
            "classname": "item_rockets",
            "uuid": 263890286796903098,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Secret (42)",
            "classname": "trigger_secret",
            "uuid": 16284532189464249475,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Mjolnir (43)",
            "classname": "weapon_mjolnir",
            "uuid": 12986065215136460371,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Cells (44)",
            "classname": "item_cells",
            "uuid": 17373035826277624476,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Cells (45)",
            "classname": "item_cells",
            "uuid": 11384777909829967936,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 2371160472593044021,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Nailgun (47)",
            "classname": "weapon_nailgun",
            "uuid": 12179901925600444014,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 9357447501424630548,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 17508544106974395220,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Rocketlauncher (50)",
            "classname": "weapon_rocketlauncher",
            "uuid": 2089888170082051015,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Shells (51)",
            "classname": "item_shells",
            "uuid": 10549258629631518430,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Hornofconjuring (52)",
            "classname": "item_hornofconjuring",
            "uuid": 10615352597770477896,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Spikes (53)",
            "classname": "item_spikes",
            "uuid": 5371024739242133191,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Empathy (54)",
            "classname": "item_artifact_empathy_shields",
            "uuid": 5881837293600802378,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Red Armor (55)",
            "classname": "item_armorInv",
            "uuid": 1893539253581339131,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Supernailgun (56)",
            "classname": "weapon_supernailgun",
            "uuid": 10702144577353424663,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Invisibility (57)",
            "classname": "item_artifact_invisibility",
            "uuid": 3896683116338806405,
            "mp": 1,
        },
        {
            "id": 58,
            "name": "Rocketlauncher (58)",
            "classname": "weapon_rocketlauncher",
            "uuid": 2646917126490224846,
            "mp": 1,
        },
        {
            "id": 59,
            "name": "Rockets (59)",
            "classname": "item_rockets",
            "uuid": 10823465421006035895,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Rockets (60)",
            "classname": "item_rockets",
            "uuid": 6886919441271887233,
            "mp": 1,
        },
        {
            "id": 61,
            "name": "Large Medkit (61)",
            "classname": "item_health",
            "uuid": 12292853592590424248,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Large Medkit (62)",
            "classname": "item_health",
            "uuid": 11069587403455945902,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Grenadelauncher (63)",
            "classname": "weapon_grenadelauncher",
            "uuid": 17571627820653381158,
            "mp": 1,
        },
        {
            "id": 64,
            "name": "Cells (64)",
            "classname": "item_cells",
            "uuid": 2600610239256451072,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Cells (65)",
            "classname": "item_cells",
            "uuid": 16144696138372152172,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Megahealth (66)",
            "classname": "item_health",
            "uuid": 1573833925706174966,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Invulnerability (67)",
            "classname": "item_artifact_invulnerability",
            "uuid": 16221739759720014603,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Rockets (68)",
            "classname": "item_rockets",
            "uuid": 13595517833709352797,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Rockets (69)",
            "classname": "item_rockets",
            "uuid": 2184401713688526262,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Rockets (70)",
            "classname": "item_rockets",
            "uuid": 2953051627673323556,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Megahealth (71)",
            "classname": "item_health",
            "uuid": 15074306468657955399,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Rockets (72)",
            "classname": "item_rockets",
            "uuid": 6202140030652208765,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "All Kills (73)",
            "classname": "all_kills",
            "uuid": 16438592234885930429,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Nailgun (47)",
                "Shells (51)",
                "Spikes (53)",
                "Supershotgun (7)",
                "Rocketlauncher (50)",
                "Large Medkit (48)",
                "Large Medkit (49)",
                "Large Medkit (8)",
                "Secret (37)",
                "Spikes (39)",
                "Spikes (38)",
                "Secret (46)",
                "Red Armor (55)",
            ],
        )

        self.restrict("Large Medkit (8)", r.jump)
        self.restrict("Secret (37)", r.can_shootswitch)
        self.restrict("Spikes (39)", r.can_shootswitch)
        self.restrict("Spikes (38)", r.can_shootswitch)
        self.restrict(
            "Red Armor (55)",
            r.can_door
            & (
                (r.bigjump & r.difficulty("medium"))
                | r.can_gj_extr
                | r.can_rj_hard
                | (r.can_jump & r.difficulty("hard"))
            ),
        )
        self.restrict(
            "Secret (46)",
            (
                (r.bigjump & r.difficulty("medium"))
                | r.can_gj_extr
                | r.can_rj_hard
                | (r.can_jump & r.difficulty("hard"))
                | r.can_shootswitch & r.jump
            ),
        )

        past_bridge_area = self.region(
            "Past Bridge",
            [
                "Spikes (13)",
                "Spikes (23)",
            ],
        )
        self.connect(
            ret,
            past_bridge_area,
            r.can_door
            | r.can_gj_extr
            | r.can_rj_hard
            | (r.can_jump & r.difficulty("medium")),
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Hornofconjuring (52)",
                "Invisibility (57)",
                "Shells (12)",
                "Shells (17)",
                "Spikes (22)",
                "Supernailgun (56)",
                "Rockets (5)",
                "Yellow Armor (20)",
                "Large Medkit (15)",
                "Large Medkit (16)",
                "Lightning (11)",
                "Silver Key (25)",
                "Secret (1)",
                "Quad Damage (6)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        self.restrict("Secret (1)", r.can_door & r.jump | r.bigjump_hard)
        self.restrict("Quad Damage (6)", r.can_door & r.jump | r.bigjump_hard)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Shells (18)",
                "Grenadelauncher (63)",
                "Secret (42)",
                "Cells (45)",
                "Mjolnir (43)",
                "Cells (44)",
                "Large Medkit (27)",
                "Rockets (14)",
                "Rockets (72)",
                "Large Medkit (26)",
                "Nailgun (34)",
                "Spikes (35)",
                "Spikes (30)",
                "Shells (29)",
                "Shells (28)",
                "Secret (24)",
                "Megahealth (66)",
            ],
        )
        self.connect(past_door_area, past_silver_door_area, self.silver_key)
        self.connect(ret, past_silver_door_area, r.bigjump_hard)

        self.restrict("Secret (24)", r.can_button)
        self.restrict("Megahealth (66)", r.can_door & (r.can_button | r.bigjump))

        self.restrict("Cells (45)", r.can_door)
        self.restrict("Mjolnir (43)", r.can_door)
        self.restrict("Cells (44)", r.can_door)

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Cells (64)",
                "Cells (65)",
                "Rockets (32)",
                "Rockets (31)",
                "Invulnerability (67)",
                "Rockets (40)",
                "Rockets (41)",
                "Rocketlauncher (33)",
                "Gold Key (36)",
            ],
        )
        self.connect(
            past_silver_door_area, shootswitch_area, r.can_shootswitch & r.can_door
        )

        dive_area = self.region(
            "Dive Area",
            [
                "Proximity (4)",
            ],
        )
        self.connect(past_door_area, dive_area, r.can_dive & r.jump)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (61)",
                "Supernailgun (21)",
                "Large Medkit (62)",
                "Cells (10)",
                "Cells (9)",
                "Rockets (60)",
                "Rockets (59)",
                "Secret (3)",
                "Yellow Armor (19)",
                "Empathy (54)",
            ],
        )
        self.connect(past_bridge_area, past_gold_door_area, self.gold_key)

        self.restrict("Secret (3)", r.can_button)
        self.restrict("Yellow Armor (19)", r.can_button)
        self.restrict("Empathy (54)", r.can_dive)

        final_area = self.region(
            "Final Area",
            [
                "Megahealth (71)",
                "Rocketlauncher (58)",
                "Rockets (69)",
                "Rockets (68)",
                "Rockets (70)",
                "Exit",
                "All Kills (73)",
            ],
        )
        self.connect(past_gold_door_area, final_area, r.can_button & r.can_dive)
        self.restrict("Exit", r.can_button & r.can_door)
        self.restrict("All Kills (73)", r.can_shootswitch & r.difficult_combat)

        return ret
