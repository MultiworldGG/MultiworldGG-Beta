from BaseClasses import Region

from ..base_classes import Q1Level


class r1m6(Q1Level):
    name = "Temple of Pain"
    mapfile = "r1m6"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Flag (1)",
            "classname": "item_flag",
            "uuid": 1283671392388699392,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Flag (2)",
            "classname": "item_flag_team2",
            "uuid": 15481294914346628344,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Flag (3)",
            "classname": "item_flag_team1",
            "uuid": 3274106915687396708,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Supershotgun (4)",
            "classname": "weapon_supershotgun",
            "uuid": 5936915140175926562,
            "mp": 1,
        },
        {
            "id": 5,
            "name": "Powerup (5)",
            "classname": "item_powerup_belt",
            "uuid": 8006761137973110382,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Secret (6)",
            "classname": "trigger_secret",
            "uuid": 6220408537674758463,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Sphere (7)",
            "classname": "item_sphere",
            "uuid": 2351368028713123120,
            "mp": 1,
        },
        {
            "id": 8,
            "name": "Powerup (8)",
            "classname": "item_powerup_shield",
            "uuid": 13159524788117209725,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Invulnerability (9)",
            "classname": "item_artifact_invulnerability",
            "uuid": 5666190801275766613,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Invisibility (10)",
            "classname": "item_artifact_invisibility",
            "uuid": 15584501375777779482,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Cells (11)",
            "classname": "item_cells",
            "uuid": 1647475306326794333,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Rockets (12)",
            "classname": "item_rockets",
            "uuid": 13269664542681819700,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 3086101230435304355,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Large Medkit (14)",
            "classname": "item_health",
            "uuid": 8848407039269513449,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Secret (15)",
            "classname": "trigger_secret",
            "uuid": 10384999593195001029,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Secret (16)",
            "classname": "trigger_secret",
            "uuid": 8800293345453886577,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Secret (17)",
            "classname": "trigger_secret",
            "uuid": 12084216716968119321,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Secret (18)",
            "classname": "trigger_secret",
            "uuid": 7262033526179234441,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Gold Key (19)",
            "classname": "item_key2",
            "uuid": 11211646182511571127,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Silver Key (20)",
            "classname": "item_key1",
            "uuid": 11709313151756682326,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 4104941934221708366,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 15534492560653552403,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 16246486753991096359,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 8863739978913802092,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Lava (25)",
            "classname": "item_lava_spikes",
            "uuid": 4906822922560623901,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 3995840315060454250,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 11857267689602908812,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Plasma (28)",
            "classname": "item_plasma",
            "uuid": 9910133098609010567,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Spikes (29)",
            "classname": "item_spikes",
            "uuid": 2064501506358340387,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Supershotgun (30)",
            "classname": "weapon_supershotgun",
            "uuid": 12991418078702071720,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Nailgun (31)",
            "classname": "weapon_nailgun",
            "uuid": 10324755154112622599,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 5581766476600840652,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Multi (33)",
            "classname": "item_multi_rockets",
            "uuid": 2483736859323538488,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 15417835424608011367,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 10621560164883632640,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Lava (36)",
            "classname": "item_lava_spikes",
            "uuid": 8147103815106012609,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 14792523294386907740,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Cells (38)",
            "classname": "item_cells",
            "uuid": 16982632086959807725,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Large Medkit (39)",
            "classname": "item_health",
            "uuid": 17610609340338108139,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Supernailgun (40)",
            "classname": "weapon_supernailgun",
            "uuid": 11893267578405960498,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Grenadelauncher (41)",
            "classname": "weapon_grenadelauncher",
            "uuid": 16645586587735708568,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Rockets (42)",
            "classname": "item_rockets",
            "uuid": 12880724928869862997,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Large Medkit (43)",
            "classname": "item_health",
            "uuid": 10946978373987588885,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Shells (44)",
            "classname": "item_shells",
            "uuid": 15458681723107979747,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Large Medkit (45)",
            "classname": "item_health",
            "uuid": 11852877390152754704,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Red Armor (46)",
            "classname": "item_armorInv",
            "uuid": 10006067735121701918,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 2930107398476094036,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Shells (48)",
            "classname": "item_shells",
            "uuid": 10477277359632927670,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 11785077444188519071,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Powerup (50)",
            "classname": "item_powerup_shield",
            "uuid": 8125638665541203449,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Plasma (51)",
            "classname": "item_plasma",
            "uuid": 15005314755342816341,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 3255575514238535217,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Spikes (53)",
            "classname": "item_spikes",
            "uuid": 12544077821424508226,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Lava (54)",
            "classname": "item_lava_spikes",
            "uuid": 9750962934603861889,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Large Medkit (55)",
            "classname": "item_health",
            "uuid": 18289548959970179959,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Large Medkit (56)",
            "classname": "item_health",
            "uuid": 1472262641853930037,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 4629093945608240839,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Quad Damage (58)",
            "classname": "item_artifact_super_damage",
            "uuid": 14970414957389655530,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Cells (59)",
            "classname": "item_cells",
            "uuid": 14044868147033470680,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Large Medkit (60)",
            "classname": "item_health",
            "uuid": 7063169747637667870,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Lava (61)",
            "classname": "item_lava_spikes",
            "uuid": 13438659740375524418,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Multi (62)",
            "classname": "item_multi_rockets",
            "uuid": 6713835080669377190,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Large Medkit (63)",
            "classname": "item_health",
            "uuid": 2869629582354190,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Large Medkit (64)",
            "classname": "item_health",
            "uuid": 6422059514271418576,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 17600396229273701943,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Spikes (66)",
            "classname": "item_spikes",
            "uuid": 17767435304143381135,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Large Medkit (67)",
            "classname": "item_health",
            "uuid": 3838612216843103904,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Large Medkit (68)",
            "classname": "item_health",
            "uuid": 17206641553451872200,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Yellow Armor (69)",
            "classname": "item_armor2",
            "uuid": 16987472359336386647,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Megahealth (70)",
            "classname": "item_health",
            "uuid": 14638382985929482849,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Rocketlauncher (71)",
            "classname": "weapon_rocketlauncher",
            "uuid": 12574932648704901180,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Lightning (72)",
            "classname": "weapon_lightning",
            "uuid": 3858403954650876521,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Large Medkit (73)",
            "classname": "item_health",
            "uuid": 13180457999628184254,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Shells (74)",
            "classname": "item_shells",
            "uuid": 6355698829237267460,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Shells (75)",
            "classname": "item_shells",
            "uuid": 16502512636944111576,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Rockets (76)",
            "classname": "item_rockets",
            "uuid": 2958732861830375323,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Shells (77)",
            "classname": "item_shells",
            "uuid": 1084135220159401802,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Spikes (78)",
            "classname": "item_spikes",
            "uuid": 1205866651879449533,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Large Medkit (79)",
            "classname": "item_health",
            "uuid": 15529459332162977842,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Shells (80)",
            "classname": "item_shells",
            "uuid": 3831931427024492312,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Spikes (81)",
            "classname": "item_spikes",
            "uuid": 15218197093117766743,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Large Medkit (82)",
            "classname": "item_health",
            "uuid": 10140230449824025248,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "Multi (83)",
            "classname": "item_multi_rockets",
            "uuid": 16632469722011856919,
            "mp": 0,
        },
        {
            "id": 84,
            "name": "Spikes (84)",
            "classname": "item_spikes",
            "uuid": 7490823136768369733,
            "mp": 0,
        },
        {
            "id": 85,
            "name": "Large Medkit (85)",
            "classname": "item_health",
            "uuid": 850655847372208142,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Large Medkit (86)",
            "classname": "item_health",
            "uuid": 4661361871074586612,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Rockets (87)",
            "classname": "item_rockets",
            "uuid": 17339799471721420358,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Large Medkit (88)",
            "classname": "item_health",
            "uuid": 10447466096666117633,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Large Medkit (89)",
            "classname": "item_health",
            "uuid": 17437105545263582809,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Lava (90)",
            "classname": "item_lava_spikes",
            "uuid": 17789866985920903235,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Shells (91)",
            "classname": "item_shells",
            "uuid": 12592920342379585269,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Spikes (92)",
            "classname": "item_spikes",
            "uuid": 7823947269937665660,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Shells (93)",
            "classname": "item_shells",
            "uuid": 4381507117077352871,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Shells (94)",
            "classname": "item_shells",
            "uuid": 2720967358010578945,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Large Medkit (95)",
            "classname": "item_health",
            "uuid": 9368875573389435934,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "Quad Damage (96)",
            "classname": "item_artifact_super_damage",
            "uuid": 702839796718487845,
            "mp": 1,
        },
        {
            "id": 97,
            "name": "All Kills (97)",
            "classname": "all_kills",
            "uuid": 18148222885165962565,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Lava (25)",
                "Shells (24)",
                "Large Medkit (22)",
                "Large Medkit (23)",
                "Supershotgun (30)",
                "Rockets (26)",
                "Shells (77)",
            ],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Flag (3)",
                "Spikes (78)",
                "Large Medkit (27)",
                "Supershotgun (4)",
                "Large Medkit (73)",
                "Shells (93)",
                "Spikes (29)",
                "Shells (80)",
                "Large Medkit (79)",
                "Shells (74)",
                "Large Medkit (32)",
                "Nailgun (31)",
                "Quad Damage (96)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        dive_area = self.region(
            "Dive Area",
            [
                "Spikes (81)",
                "Large Medkit (34)",
                "Large Medkit (35)",
                "Shells (75)",
                "Rockets (76)",
                "Powerup (8)",
                "Large Medkit (37)",
                "Large Medkit (82)",
                "Large Medkit (39)",
                "Cells (38)",
            ],
        )
        self.connect(past_door_area, dive_area, r.can_dive)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Grenadelauncher (41)",
                "Large Medkit (43)",
                "Rockets (42)",
                "Large Medkit (14)",
                "Spikes (84)",
                "Rockets (12)",
                "Shells (13)",
                "Shells (44)",
                "Large Medkit (45)",
                "Secret (17)",
                "Red Armor (46)",
                "Large Medkit (85)",
                "Rockets (87)",
                "Large Medkit (86)",
            ],
        )
        self.connect(dive_area, past_button_area, r.can_button)
        self.restrict("Shells (44)", r.jump)
        self.restrict("Large Medkit (45)", r.jump | r.can_jump)
        self.restrict("Secret (17)", r.bigjump | r.can_jump)
        self.restrict("Red Armor (46)", r.bigjump | r.can_jump)
        self.restrict("Large Medkit (85)", r.bigjump | r.can_jump)
        self.restrict("Rockets (87)", r.bigjump | r.can_jump)
        self.restrict("Large Medkit (86)", r.bigjump | r.can_jump)

        graveyard_dive_area = self.region(
            "Graveyard Dive Area",
            [
                "Shells (48)",
                "Large Medkit (49)",
                "Large Medkit (47)",
                "Large Medkit (88)",
            ],
        )
        self.connect(past_button_area, graveyard_dive_area, r.can_dive)

        castle_final_area = self.region(
            "Castle Final Area",
            [
                "Plasma (51)",
                "Flag (1)",
                "Silver Key (20)",
                "Supernailgun (40)",
                "Spikes (53)",
                "Secret (6)",
                "Invulnerability (9)",
            ],
        )
        self.restrict("Secret (6)", r.jump & r.can_button)
        self.restrict("Invulnerability (9)", r.jump & r.can_button)
        self.connect(graveyard_dive_area, castle_final_area)

        altar_area = self.region(
            "Altar",
            [
                "Large Medkit (52)",
                "Secret (15)",
                "Lightning (72)",
            ],
        )
        self.connect(
            castle_final_area,
            altar_area,
            r.can_rj_med | r.can_gj_hard | (r.can_jump & r.difficulty("hard")),
        )

        past_gold_door_area = self.region(
            "Past Gold Door",
            ["Exit"],
        )
        self.connect(castle_final_area, past_gold_door_area, self.gold_key)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Large Medkit (56)",
                "Large Medkit (55)",
                "Lava (90)",
                "Large Medkit (89)",
                "Shells (57)",
                "Shells (91)",
                "Spikes (92)",
                "Large Medkit (95)",
                "Shells (94)",
                "Powerup (5)",
                "Large Medkit (63)",
                "Large Medkit (64)",
                "Shells (65)",
                "Spikes (66)",
                "Rocketlauncher (71)",
                "Large Medkit (68)",
                "Large Medkit (67)",
                "Flag (2)",
                "Gold Key (19)",
                "Megahealth (70)",
                "Yellow Armor (69)",
                "Cells (11)",
                "Secret (16)",
                "Quad Damage (58)",
                "Large Medkit (60)",
                "Cells (59)",
                "Secret (18)",
                "Powerup (50)",
                "Sphere (7)",
                "All Kills (97)",
            ],
        )
        self.connect(past_door_area, past_silver_door_area, self.silver_key)
        self.restrict("Secret (16)", (r.jump & r.can_button) | r.bigjump_hard)
        self.restrict("Quad Damage (58)", (r.jump & r.can_button) | r.bigjump_hard)
        self.restrict("Large Medkit (60)", (r.jump & r.can_button) | r.bigjump_hard)
        self.restrict("Cells (59)", (r.jump & r.can_button) | r.bigjump_hard)
        self.restrict("Secret (18)", r.can_dive)
        self.restrict("Powerup (50)", r.can_dive)
        self.restrict("Sphere (7)", r.can_dive)
        self.restrict("Megahealth (70)", r.jump)
        self.restrict("Yellow Armor (69)", r.jump)

        self.restrict("All Kills (97)", r.can_dive & r.can_button & r.difficult_combat)

        return ret
