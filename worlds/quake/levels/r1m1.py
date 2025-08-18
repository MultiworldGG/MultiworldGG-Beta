from BaseClasses import Region

from ..base_classes import Q1Level


class r1m1(Q1Level):
    name = "Deviant's Domain"
    mapfile = "r1m1"
    keys = ["Silver"]
    location_defs = [
        {
            "id": 1,
            "name": "Powerup (1)",
            "classname": "item_powerup_shield",
            "uuid": 8116671032036847541,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Secret (2)",
            "classname": "trigger_secret",
            "uuid": 2699176222021751318,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Shells (3)",
            "classname": "item_shells",
            "uuid": 7041914791091972428,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 6955534618572876533,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Large Medkit (5)",
            "classname": "item_health",
            "uuid": 13350795686388804689,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Invisibility (6)",
            "classname": "item_artifact_invisibility",
            "uuid": 2999960480295535279,
            "mp": 1,
        },
        {
            "id": 7,
            "name": "Biosuit (7)",
            "classname": "item_artifact_envirosuit",
            "uuid": 7281306576847327394,
            "mp": 1,
        },
        {
            "id": 8,
            "name": "Invulnerability (8)",
            "classname": "item_artifact_invulnerability",
            "uuid": 17206551527570687836,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Cells (9)",
            "classname": "item_cells",
            "uuid": 15213793936144745205,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Red Armor (10)",
            "classname": "item_armorInv",
            "uuid": 8403138373888442300,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 5910658735426854318,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Yellow Armor (12)",
            "classname": "item_armor2",
            "uuid": 3878998287505431792,
            "mp": 1,
        },
        {
            "id": 13,
            "name": "Grenadelauncher (13)",
            "classname": "weapon_grenadelauncher",
            "uuid": 14553326045856960227,
            "mp": 1,
        },
        {
            "id": 14,
            "name": "Nailgun (14)",
            "classname": "weapon_nailgun",
            "uuid": 11571245743586359043,
            "mp": 1,
        },
        {
            "id": 15,
            "name": "Rockets (15)",
            "classname": "item_rockets",
            "uuid": 1764073239967109768,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Small Medkit (16)",
            "classname": "item_health",
            "uuid": 13995585114655346219,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Small Medkit (17)",
            "classname": "item_health",
            "uuid": 10531011449979498036,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Lava (18)",
            "classname": "item_lava_spikes",
            "uuid": 5867957282286571574,
            "mp": 1,
        },
        {
            "id": 19,
            "name": "Secret (19)",
            "classname": "trigger_secret",
            "uuid": 17453202376817155519,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Biosuit (20)",
            "classname": "item_artifact_envirosuit",
            "uuid": 7210899996825697430,
            "mp": 1,
        },
        {
            "id": 21,
            "name": "Cells (21)",
            "classname": "item_cells",
            "uuid": 6795315596871557041,
            "mp": 1,
        },
        {
            "id": 22,
            "name": "Cells (22)",
            "classname": "item_cells",
            "uuid": 12348532952632657602,
            "mp": 1,
        },
        {
            "id": 23,
            "name": "Lightning (23)",
            "classname": "weapon_lightning",
            "uuid": 7136123579256787838,
            "mp": 1,
        },
        {
            "id": 24,
            "name": "Grenadelauncher (24)",
            "classname": "weapon_grenadelauncher",
            "uuid": 1670206693626329778,
            "mp": 1,
        },
        {
            "id": 25,
            "name": "Supernailgun (25)",
            "classname": "weapon_supernailgun",
            "uuid": 13830960584488152289,
            "mp": 1,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 17939498824527660017,
            "mp": 1,
        },
        {
            "id": 27,
            "name": "Rocketlauncher (27)",
            "classname": "weapon_rocketlauncher",
            "uuid": 15824305429594476881,
            "mp": 1,
        },
        {
            "id": 28,
            "name": "Spikes (28)",
            "classname": "item_spikes",
            "uuid": 8145291229567787078,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Lava (29)",
            "classname": "item_lava_spikes",
            "uuid": 14692391224228825158,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Spikes (30)",
            "classname": "item_spikes",
            "uuid": 5550894090355090093,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 4064018215976441493,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 10507699293509820407,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Large Medkit (33)",
            "classname": "item_health",
            "uuid": 10245358200345177244,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 16481614444904285301,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 11132499826705714001,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 13620422412930984601,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 5937248560440398585,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 11809620145660716090,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Lava (39)",
            "classname": "item_lava_spikes",
            "uuid": 2075059036337776529,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 4663648019742044757,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Shells (41)",
            "classname": "item_shells",
            "uuid": 5622193431130098588,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Rockets (42)",
            "classname": "item_rockets",
            "uuid": 16318512062942256315,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Lava (43)",
            "classname": "item_lava_spikes",
            "uuid": 10725775014742425303,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Small Medkit (44)",
            "classname": "item_health",
            "uuid": 17237821845591761823,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Small Medkit (45)",
            "classname": "item_health",
            "uuid": 12505450617876253963,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Lava (46)",
            "classname": "item_lava_spikes",
            "uuid": 12795289713243867662,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Shells (47)",
            "classname": "item_shells",
            "uuid": 8431362163542217386,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Spikes (48)",
            "classname": "item_spikes",
            "uuid": 11065918139404699224,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Shells (49)",
            "classname": "item_shells",
            "uuid": 8861278249870229629,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Small Medkit (50)",
            "classname": "item_health",
            "uuid": 4224234562613818288,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Small Medkit (51)",
            "classname": "item_health",
            "uuid": 6742089923553155274,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Rockets (52)",
            "classname": "item_rockets",
            "uuid": 2603366053152503705,
            "mp": 1,
        },
        {
            "id": 53,
            "name": "Green Armor (53)",
            "classname": "item_armor1",
            "uuid": 4031279808690895081,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Megahealth (54)",
            "classname": "item_health",
            "uuid": 18170673462922159861,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Secret (55)",
            "classname": "trigger_secret",
            "uuid": 13959779029986181328,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Secret (56)",
            "classname": "trigger_secret",
            "uuid": 7892355820652956103,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Shells (57)",
            "classname": "item_shells",
            "uuid": 2440112000740292229,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Spikes (58)",
            "classname": "item_spikes",
            "uuid": 17806296901267018967,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Supershotgun (59)",
            "classname": "weapon_supershotgun",
            "uuid": 16539243512619335704,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Large Medkit (60)",
            "classname": "item_health",
            "uuid": 1052316693653490164,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Shells (61)",
            "classname": "item_shells",
            "uuid": 559678873799118193,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Yellow Armor (62)",
            "classname": "item_armor2",
            "uuid": 8521345373231544838,
            "mp": 1,
        },
        {
            "id": 63,
            "name": "Nailgun (63)",
            "classname": "weapon_nailgun",
            "uuid": 15329200069029256121,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Spikes (64)",
            "classname": "item_spikes",
            "uuid": 14940607433339924317,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Large Medkit (65)",
            "classname": "item_health",
            "uuid": 17892511749997030316,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Small Medkit (66)",
            "classname": "item_health",
            "uuid": 719359938610114965,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Shells (67)",
            "classname": "item_shells",
            "uuid": 15127003638184968992,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Lava (68)",
            "classname": "item_lava_spikes",
            "uuid": 356989904636685178,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Small Medkit (69)",
            "classname": "item_health",
            "uuid": 11786206521635232282,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Spikes (70)",
            "classname": "item_spikes",
            "uuid": 8216866810528172998,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 18394635240528001037,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Shells (72)",
            "classname": "item_shells",
            "uuid": 12009265109867128070,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Shells (73)",
            "classname": "item_shells",
            "uuid": 10482974568760351149,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Small Medkit (74)",
            "classname": "item_health",
            "uuid": 7260256710766140851,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Small Medkit (75)",
            "classname": "item_health",
            "uuid": 4989153753721847929,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Biosuit (76)",
            "classname": "item_artifact_envirosuit",
            "uuid": 7494678041956854354,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Large Medkit (77)",
            "classname": "item_health",
            "uuid": 3731372827104019625,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Large Medkit (78)",
            "classname": "item_health",
            "uuid": 6343012736222357197,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Rocketlauncher (79)",
            "classname": "weapon_rocketlauncher",
            "uuid": 11981561810925280905,
            "mp": 1,
        },
        {
            "id": 80,
            "name": "Large Medkit (80)",
            "classname": "item_health",
            "uuid": 13124036083339955510,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Large Medkit (81)",
            "classname": "item_health",
            "uuid": 5008519348906515992,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Quad Damage (82)",
            "classname": "item_artifact_super_damage",
            "uuid": 14039329001952622135,
            "mp": 1,
        },
        {
            "id": 83,
            "name": "Cells (83)",
            "classname": "item_cells",
            "uuid": 12504130783054634663,
            "mp": 1,
        },
        {
            "id": 84,
            "name": "Lightning (84)",
            "classname": "weapon_lightning",
            "uuid": 8478889996626050022,
            "mp": 1,
        },
        {
            "id": 85,
            "name": "Small Medkit (85)",
            "classname": "item_health",
            "uuid": 17379927949413547226,
            "mp": 0,
        },
        {
            "id": 86,
            "name": "Spikes (86)",
            "classname": "item_spikes",
            "uuid": 4911399963376547752,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Rockets (87)",
            "classname": "item_rockets",
            "uuid": 15947635794313689082,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Large Medkit (88)",
            "classname": "item_health",
            "uuid": 16645197783209994391,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Small Medkit (89)",
            "classname": "item_health",
            "uuid": 4093105525354478596,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Shells (90)",
            "classname": "item_shells",
            "uuid": 13414821225621387019,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Large Medkit (91)",
            "classname": "item_health",
            "uuid": 8224509560168405582,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Biosuit (92)",
            "classname": "item_artifact_envirosuit",
            "uuid": 15793009586892456638,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Large Medkit (93)",
            "classname": "item_health",
            "uuid": 6522319254767371158,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "Large Medkit (94)",
            "classname": "item_health",
            "uuid": 17567399247898782324,
            "mp": 0,
        },
        {
            "id": 95,
            "name": "Spikes (95)",
            "classname": "item_spikes",
            "uuid": 10727885741375555617,
            "mp": 0,
        },
        {
            "id": 96,
            "name": "Green Armor (96)",
            "classname": "item_armor1",
            "uuid": 6080082282930664629,
            "mp": 0,
        },
        {
            "id": 97,
            "name": "Shells (97)",
            "classname": "item_shells",
            "uuid": 8419887655492578773,
            "mp": 0,
        },
        {
            "id": 98,
            "name": "Supershotgun (98)",
            "classname": "weapon_supershotgun",
            "uuid": 8565383620856412323,
            "mp": 0,
        },
        {
            "id": 99,
            "name": "Shells (99)",
            "classname": "item_shells",
            "uuid": 11380862336784088470,
            "mp": 0,
        },
        {
            "id": 100,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 14575902659314564059,
            "mp": 0,
        },
        {
            "id": 101,
            "name": "Silver Key (101)",
            "classname": "item_key1",
            "uuid": 11478952767810804630,
            "mp": 0,
        },
        {
            "id": 102,
            "name": "Sphere (102)",
            "classname": "item_sphere",
            "uuid": 16786786672667901552,
            "mp": 1,
        },
        {
            "id": 103,
            "name": "Sphere (103)",
            "classname": "item_sphere",
            "uuid": 1330220084196787127,
            "mp": 1,
        },
        {
            "id": 104,
            "name": "Large Medkit (104)",
            "classname": "item_health",
            "uuid": 14408011764023988218,
            "mp": 0,
        },
        {
            "id": 105,
            "name": "Multi (105)",
            "classname": "item_multi_rockets",
            "uuid": 4856804371120993317,
            "mp": 1,
        },
        {
            "id": 106,
            "name": "Large Medkit (106)",
            "classname": "item_health",
            "uuid": 9994045424250199361,
            "mp": 0,
        },
        {
            "id": 107,
            "name": "Plasma (107)",
            "classname": "item_plasma",
            "uuid": 9564866455815674386,
            "mp": 1,
        },
        {
            "id": 108,
            "name": "Rockets (108)",
            "classname": "item_rockets",
            "uuid": 4064006626307524108,
            "mp": 0,
        },
        {
            "id": 109,
            "name": "Powerup (109)",
            "classname": "item_powerup_belt",
            "uuid": 11226436856492299855,
            "mp": 1,
        },
        {
            "id": 110,
            "name": "Flag (110)",
            "classname": "item_flag_team2",
            "uuid": 2690000836100156784,
            "mp": 0,
        },
        {
            "id": 111,
            "name": "Flag (111)",
            "classname": "item_flag_team1",
            "uuid": 7846382760727859727,
            "mp": 0,
        },
        {
            "id": 112,
            "name": "Spikes (112)",
            "classname": "item_spikes",
            "uuid": 17688907439330455739,
            "mp": 0,
        },
        {
            "id": 113,
            "name": "Shells (113)",
            "classname": "item_shells",
            "uuid": 14313698315355752745,
            "mp": 0,
        },
        {
            "id": 114,
            "name": "Flag (114)",
            "classname": "item_flag",
            "uuid": 14448294574302139201,
            "mp": 0,
        },
        {
            "id": 115,
            "name": "Multi (115)",
            "classname": "item_multi_rockets",
            "uuid": 15701540279120511869,
            "mp": 1,
        },
        {
            "id": 116,
            "name": "Multi (116)",
            "classname": "item_multi_rockets",
            "uuid": 275770548655440854,
            "mp": 1,
        },
        {
            "id": 117,
            "name": "Multi (117)",
            "classname": "item_multi_rockets",
            "uuid": 8169963845766979562,
            "mp": 1,
        },
        {
            "id": 118,
            "name": "Multi (118)",
            "classname": "item_multi_rockets",
            "uuid": 17033688624808029943,
            "mp": 1,
        },
        {
            "id": 119,
            "name": "Multi (119)",
            "classname": "item_multi_rockets",
            "uuid": 15344383828754224998,
            "mp": 1,
        },
        {
            "id": 120,
            "name": "All Kills (120)",
            "classname": "all_kills",
            "uuid": 5544790637148386333,
            "mp": 0,
        },
    ]

    events = ["Drawbridge Active"]

    must_bio = True
    must_invuln = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Sphere (102)",
                "Multi (105)",
                "Shells (72)",
                "Large Medkit (106)",
                "Large Medkit (104)",
                "Shells (99)",
                "Shells (49)",
                "Secret (19)",
            ],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Large Medkit (80)",
                "Large Medkit (94)",
                "Shells (90)",
                "Large Medkit (91)",
                "Flag (111)",
                "Spikes (112)",
                "Shells (113)",
                "Grenadelauncher (13)",
                "Small Medkit (74)",
                "Small Medkit (75)",
                "Secret (56)",
                "Supershotgun (98)",
                "Shells (97)",
                "Spikes (95)",
                "Green Armor (96)",
                "Shells (73)",
                "Yellow Armor (62)",
                "Large Medkit (81)",
                "Rockets (108)",
                "Plasma (107)",
            ],
        )

        self.connect(ret, past_door_area, r.can_door | r.bigjump_hard)
        self.restrict("Rockets (108)", r.bigjump | (r.jump & r.can_door))
        self.restrict("Plasma (107)", r.bigjump | (r.jump & r.can_door))

        dive_area = self.region(
            "Dive Area",
            [
                "Shells (67)",
                "Large Medkit (88)",
                "Rockets (87)",
                "Biosuit (76)",
                "Lightning (84)",
                "Cells (83)",
                "Small Medkit (89)",
                "Spikes (86)",
                "Small Medkit (85)",
                "Multi (115)",
            ],
        )
        self.connect(ret, dive_area, r.can_dive & (r.biosuit(1) | r.invuln(1)))

        button_bridge_area = self.region(
            "Button Bridge",
            [
                "Nailgun (63)",
                "Large Medkit (71)",
            ],
        )
        self.connect(
            past_door_area,
            button_bridge_area,
            (r.bigjump & r.difficulty("medium")) | r.can_button,
        )

        past_button_area = self.region(
            "Past Button Area",
            [
                "Small Medkit (66)",
                "Multi (116)",
                "Spikes (64)",
                "Rocketlauncher (79)",
                "Large Medkit (77)",
                "Large Medkit (78)",
                "Large Medkit (5)",
                "Shells (61)",
            ],
        )
        self.connect(button_bridge_area, past_button_area, r.can_button)

        past_dropbridge_area = self.region(
            "Past Drop Bridge",
            [
                "Flag (114)",
                "Silver Key (101)",
                "Spikes (70)",
                "Quad Damage (82)",
            ],
        )
        self.connect(
            past_button_area,
            past_dropbridge_area,
            r.can_rj_hard
            | r.can_gj_extr
            | (r.can_jump & r.difficulty("hard"))
            | r.can_door,
        )

        past_moat_area = self.region(
            "Past Moat",
            [
                "Small Medkit (17)",
                "Small Medkit (16)",
                "Lava (18)",
            ],
        )
        self.connect(
            ret,
            past_moat_area,
            r.bigjump_hard | self.event("Drawbridge Active"),
        )
        self.connect(past_door_area, past_moat_area, r.jump)

        past_moat_upper_area = self.region(
            "Past Moat Upper",
            [
                "Invulnerability (8)",
            ],
        )
        self.connect(
            past_door_area, past_moat_upper_area, r.jump & r.difficulty("hard")
        )
        self.connect(past_moat_area, past_moat_upper_area, r.bigjump)

        past_moat_door_area = self.region(
            "Past Moat Door",
            [
                "Lava (29)",
                "Nailgun (14)",
                "Spikes (28)",
                "Rockets (15)",
                "Exit",
                "All Kills (120)",
            ],
        )
        self.connect(ret, past_moat_door_area, self.event("Drawbridge Active"))
        self.restrict("Exit", r.can_door)
        self.restrict("All Kills (120)", r.difficult_combat)

        boat_area = self.region(
            "Boat Area",
            [
                "Large Medkit (93)",
                "Large Medkit (65)",
                "Spikes (48)",
                "Biosuit (20)",
                "Small Medkit (69)",
                "Biosuit (92)",
                "Secret (55)",
                "Megahealth (54)",
            ],
        )
        self.connect(past_dropbridge_area, boat_area, r.can_door)
        self.restrict("Biosuit (92)", r.can_dive & (r.biosuit(1) | r.invuln(1)))
        self.restrict("Secret (55)", r.can_dive & (r.biosuit(1) | r.invuln(1)))
        self.restrict("Megahealth (54)", r.can_dive & (r.biosuit(1) | r.invuln(1)))

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Supershotgun (59)",
                "Small Medkit (51)",
                "Small Medkit (50)",
                "Shells (47)",
                "Spikes (58)",
                "Grenadelauncher (24)",
            ],
        )
        self.connect(boat_area, past_silver_door_area, self.silver_key)

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Shells (57)",
                "Sphere (103)",
                "Large Medkit (60)",
                "Rockets (52)",
                "Red Armor (10)",
                "Green Armor (53)",
            ],
        )
        self.connect(
            boat_area,
            shootswitch_area,
            r.can_shootswitch | (r.jump & r.difficulty("medium")),
        )
        self.restrict("Large Medkit (60)", r.jump)
        self.restrict("Rockets (52)", r.jump)
        self.restrict("Red Armor (10)", r.jump)
        self.restrict("Green Armor (53)", r.jump)

        silver_dive_area = self.region(
            "Silver Dive Area",
            [
                "Multi (118)",
                "Cells (21)",
                "Cells (22)",
                "Lightning (23)",
            ],
        )
        self.connect(
            boat_area, silver_dive_area, r.can_dive & (r.biosuit(1) | r.invuln(1))
        )

        second_boat_area = self.region(
            "Second Boat Area",
            [
                "Small Medkit (45)",
                "Small Medkit (44)",
                "Lava (43)",
                "Large Medkit (4)",
                "Shells (41)",
                "Rockets (42)",
                "Large Medkit (37)",
                "Large Medkit (40)",
                "Flag (110)",
                "Rockets (26)",
                "Large Medkit (38)",
                "Large Medkit (35)",
                "Powerup (109)",
                "Shells (34)",
                "Yellow Armor (12)",
                "Shells (3)",
                "Spikes (36)",
                "Large Medkit (33)",
                "Large Medkit (32)",
                "Supernailgun (25)",
                "Cells (9)",
                "Spikes (30)",
                "Multi (119)",
                "Large Medkit (31)",
                "Shells (11)",
                "Powerup (1)",
                "Secret (2)",
                "Multi (117)",
                "Lava (39)",
                "Rocketlauncher (27)",
                "Biosuit (7)",
                "Invisibility (6)",
                "Drawbridge Active",
            ],
        )
        self.connect(past_silver_door_area, second_boat_area, r.can_door)

        self.restrict("Powerup (1)", r.can_shootswitch)
        self.restrict("Secret (2)", r.can_shootswitch)
        self.restrict("Multi (117)", r.jump)
        self.restrict("Lava (39)", r.jump)
        self.restrict("Rocketlauncher (27)", r.jump)
        self.restrict("Biosuit (7)", r.can_dive)
        self.restrict("Invisibility (6)", r.can_dive)

        return ret
