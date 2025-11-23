from BaseClasses import Region

from ..base_classes import Q1Level


class mge4m1(Q1Level):
    name = "Grave Machine"
    mapfile = "mge4m1"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Nailgun (1)",
            "classname": "weapon_nailgun",
            "uuid": 1426118013202723455,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Spikes (2)",
            "classname": "item_spikes",
            "uuid": 12182583862319673651,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Spikes (3)",
            "classname": "item_spikes",
            "uuid": 9106797404600489658,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 16158766744405103944,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Shells (5)",
            "classname": "item_shells",
            "uuid": 13512094805188994583,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Spikes (6)",
            "classname": "item_spikes",
            "uuid": 482625981421867836,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Spikes (7)",
            "classname": "item_spikes",
            "uuid": 1142317102509831621,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 636413824276797141,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Large Medkit (9)",
            "classname": "item_health",
            "uuid": 12906986955462117444,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Rockets (10)",
            "classname": "item_rockets",
            "uuid": 5335343097926388345,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Rockets (11)",
            "classname": "item_rockets",
            "uuid": 6042538444821699920,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Green Armor (12)",
            "classname": "item_armor1",
            "uuid": 2902843771065928223,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Rockets (13)",
            "classname": "item_rockets",
            "uuid": 5366125822331483695,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Grenadelauncher (14)",
            "classname": "weapon_grenadelauncher",
            "uuid": 2158549451945391228,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 9938408534069326732,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Shells (16)",
            "classname": "item_shells",
            "uuid": 13520324711075662444,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Shells (17)",
            "classname": "item_shells",
            "uuid": 4375894178550200821,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Rockets (18)",
            "classname": "item_rockets",
            "uuid": 16058289454318889985,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Shells (19)",
            "classname": "item_shells",
            "uuid": 8282287761305027889,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 5331190226105326528,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 8692220324816034893,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Secret (22)",
            "classname": "trigger_secret",
            "uuid": 13881509578535528887,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Shells (23)",
            "classname": "item_shells",
            "uuid": 6163406642755198749,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 1592163673986524915,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 11543561630947899703,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 6124580009532169349,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Rockets (27)",
            "classname": "item_rockets",
            "uuid": 6050788063969005550,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Invulnerability (28)",
            "classname": "item_artifact_invulnerability",
            "uuid": 9046317671189227321,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 4220493550373726910,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 6032711713718884875,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 4124288816854567032,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Shells (32)",
            "classname": "item_shells",
            "uuid": 604543407076199900,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 7203111275559953733,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 5431306748956172292,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Secret (35)",
            "classname": "trigger_secret",
            "uuid": 11354694199223465064,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Rocketlauncher (36)",
            "classname": "weapon_rocketlauncher",
            "uuid": 5965711365085956134,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Rockets (37)",
            "classname": "item_rockets",
            "uuid": 6366387960508110549,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Rockets (38)",
            "classname": "item_rockets",
            "uuid": 17795725599673479198,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 5582797145090308412,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Spikes (40)",
            "classname": "item_spikes",
            "uuid": 8293756855897971188,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 6577734034083889096,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Large Medkit (42)",
            "classname": "item_health",
            "uuid": 2506075301900555974,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Shells (43)",
            "classname": "item_shells",
            "uuid": 13667514603178137564,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 10498736375300736025,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Shells (45)",
            "classname": "item_shells",
            "uuid": 12410469955592801627,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Shells (46)",
            "classname": "item_shells",
            "uuid": 16101071520786471380,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 9965164208121008532,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 14286183583256343765,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Spikes (49)",
            "classname": "item_spikes",
            "uuid": 10866828613990095904,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Spikes (50)",
            "classname": "item_spikes",
            "uuid": 10961859722638951721,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Shells (51)",
            "classname": "item_shells",
            "uuid": 10014958127107166439,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Shells (52)",
            "classname": "item_shells",
            "uuid": 14521127880708741587,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 5037359785275061425,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 8042848472686893865,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 3267173963738549628,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Supershotgun (56)",
            "classname": "weapon_supershotgun",
            "uuid": 5788219882233188987,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 4372623230319324531,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Shells (58)",
            "classname": "item_shells",
            "uuid": 15436185813846022872,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Green Armor (59)",
            "classname": "item_armor1",
            "uuid": 10611040097651026256,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Spikes (60)",
            "classname": "item_spikes",
            "uuid": 9748232328320957731,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Spikes (61)",
            "classname": "item_spikes",
            "uuid": 12806242664460607198,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Shells (62)",
            "classname": "item_shells",
            "uuid": 16394539594332310309,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Shells (63)",
            "classname": "item_shells",
            "uuid": 9301858243935498120,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Spikes (64)",
            "classname": "item_spikes",
            "uuid": 16133381998861797785,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Spikes (65)",
            "classname": "item_spikes",
            "uuid": 16296500878209387392,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Supernailgun (66)",
            "classname": "weapon_supernailgun",
            "uuid": 14074098662514165117,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Rockets (67)",
            "classname": "item_rockets",
            "uuid": 12272185507343206541,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Shells (68)",
            "classname": "item_shells",
            "uuid": 4789972711798903238,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Large Medkit (69)",
            "classname": "item_health",
            "uuid": 17893279654271623463,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Large Medkit (70)",
            "classname": "item_health",
            "uuid": 13183397708787003506,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Yellow Armor (71)",
            "classname": "item_armor2",
            "uuid": 8169404153046088686,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Red Armor (72)",
            "classname": "item_armorInv",
            "uuid": 15235742196101579065,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Yellow Armor (73)",
            "classname": "item_armor2",
            "uuid": 5356526560863344204,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Spikes (74)",
            "classname": "item_spikes",
            "uuid": 4197478164413350527,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Spikes (75)",
            "classname": "item_spikes",
            "uuid": 4327116356293476472,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Spikes (76)",
            "classname": "item_spikes",
            "uuid": 2135007436074636440,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Shells (77)",
            "classname": "item_shells",
            "uuid": 8613672260143411599,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Spikes (78)",
            "classname": "item_spikes",
            "uuid": 6007431622706994772,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Rockets (79)",
            "classname": "item_rockets",
            "uuid": 12688167305090402393,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Large Medkit (80)",
            "classname": "item_health",
            "uuid": 2332321037739547869,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Biosuit (81)",
            "classname": "item_artifact_envirosuit",
            "uuid": 6213879747313504073,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Secret (82)",
            "classname": "trigger_secret",
            "uuid": 9588731314613796113,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "All Kills (83)",
            "classname": "all_kills",
            "uuid": 13445617324489743839,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Shells (31)",
                "Shells (25)",
                "Shells (33)",
                "Large Medkit (4)",
                "Shells (5)",
                "Shells (19)",
                "Large Medkit (20)",
                "Shells (32)",
                "Nailgun (1)",
                "Spikes (3)",
                "Spikes (2)",
                "Shells (16)",
                "Large Medkit (24)",
                "Shells (30)",
                "Large Medkit (15)",
                "Shells (23)",
                "Rockets (18)",
                "Grenadelauncher (14)",
                "Rockets (13)",
                "Large Medkit (9)",
                # button
                "Green Armor (12)",
                "Spikes (6)",
                "Large Medkit (21)",
                "Spikes (7)",
                # shootswitch
                "Rockets (27)",
                "Secret (22)",
                "Invulnerability (28)",
                "Rockets (26)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door | r.can_gj_extr | r.can_rj_hard)
        self.restrict("Rockets (27)", r.can_shootswitch)
        self.restrict("Secret (22)", r.can_shootswitch)
        self.restrict("Invulnerability (28)", r.can_shootswitch)
        self.restrict("Rockets (26)", r.can_shootswitch)
        self.restrict(
            "Green Armor (12)",
            r.can_button | (r.can_jump & (r.can_gj_extr | r.can_rj_hard)),
        )
        self.restrict(
            "Spikes (6)", r.can_button | (r.can_jump & (r.can_gj_extr | r.can_rj_hard))
        )
        self.restrict(
            "Large Medkit (21)",
            r.can_button | (r.can_jump & (r.can_gj_extr | r.can_rj_hard)),
        )
        self.restrict(
            "Spikes (7)", r.can_button | (r.can_jump & (r.can_gj_extr | r.can_rj_hard))
        )

        underground_area = self.region(
            "Underground Area",
            [
                "Rockets (10)",
                "Rockets (11)",
            ],
        )
        self.connect(past_door_area, underground_area, r.can_button)

        underground_door_area = self.region(
            "Underground Door Area",
            [
                "Large Medkit (47)",
                "Large Medkit (48)",
                "Spikes (49)",
                "Spikes (50)",
                "Large Medkit (80)",
                "Secret (82)",
                "Yellow Armor (73)",
                "Shells (51)",
                "Shells (52)",
                "Shells (43)",
                "Shells (44)",
                "Red Armor (72)",
                "Secret (35)",
                "Spikes (74)",
                "Spikes (75)",
                "Large Medkit (41)",
                "Spikes (39)",
                "Spikes (40)",
                "Large Medkit (42)",
                "Biosuit (81)",
                "Rockets (38)",
                "Rocketlauncher (36)",
                "Large Medkit (53)",
                "Shells (55)",
                "Large Medkit (8)",
            ],
        )
        self.connect(underground_area, underground_door_area, r.can_door)

        self.restrict("Secret (82)", r.can_shootswitch)
        self.restrict("Yellow Armor (73)", r.can_shootswitch)

        self.restrict("Red Armor (72)", r.can_dive)
        self.restrict("Secret (35)", r.can_dive)
        self.restrict("Spikes (74)", r.can_dive)
        self.restrict("Spikes (75)", r.can_dive)

        self.restrict("Rocketlauncher (36)", r.jump)
        self.restrict("Large Medkit (53)", r.jump)

        jump_area = self.region(
            "Jump Area",
            [
                "Supershotgun (56)",
                "Shells (57)",
                "Green Armor (59)",
                "Large Medkit (54)",
                "Shells (58)",
                "Spikes (61)",
                "Spikes (60)",
                "Shells (63)",
                "Spikes (76)",
                "Spikes (78)",
                "Rockets (67)",
                "Large Medkit (69)",
                "Yellow Armor (71)",
                "Large Medkit (70)",
                "Rockets (79)",
                "Shells (77)",
                "Shells (68)",
                "Supernailgun (66)",
                "Exit",
                "All Kills (83)",
            ],
        )
        self.connect(underground_door_area, jump_area, r.jump)
        self.restrict("All Kills (83)", r.difficult_combat)

        return ret
