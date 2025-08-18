from BaseClasses import Region

from ..base_classes import Q1Level


class hip1m2(Q1Level):
    name = "Storage Facility"
    mapfile = "hip1m2"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Yellow Armor (1)",
            "classname": "item_armor2",
            "uuid": 8867919509623082793,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Silver Key (2)",
            "classname": "item_key1",
            "uuid": 15824990106917642848,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Rockets (3)",
            "classname": "item_rockets",
            "uuid": 12125432776461585629,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Rockets (4)",
            "classname": "item_rockets",
            "uuid": 12798047819785757540,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Grenadelauncher (5)",
            "classname": "weapon_grenadelauncher",
            "uuid": 3115844549572080569,
            "mp": 1,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 10101729962990842386,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 12862355565731381785,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 14703974007559058337,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Shells (9)",
            "classname": "item_shells",
            "uuid": 5218615268402496151,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Invisibility (10)",
            "classname": "item_artifact_invisibility",
            "uuid": 16626709576968803928,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Secret (11)",
            "classname": "trigger_secret",
            "uuid": 6798592731772748043,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Proximity (12)",
            "classname": "weapon_proximity_gun",
            "uuid": 17617463600835155138,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Rockets (13)",
            "classname": "item_rockets",
            "uuid": 18411398519953763824,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Rockets (14)",
            "classname": "item_rockets",
            "uuid": 10367462427405133974,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Yellow Armor (15)",
            "classname": "item_armor2",
            "uuid": 4528076699612151995,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Cells (16)",
            "classname": "item_cells",
            "uuid": 10024315898457892082,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Cells (17)",
            "classname": "item_cells",
            "uuid": 9690263759164756707,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 14699683680198434657,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 10439438224947874416,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Shells (20)",
            "classname": "item_shells",
            "uuid": 235430388182755439,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Shells (21)",
            "classname": "item_shells",
            "uuid": 3380028155767231487,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Shells (22)",
            "classname": "item_shells",
            "uuid": 12611137448487288587,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Shells (23)",
            "classname": "item_shells",
            "uuid": 17144038713852852898,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Supernailgun (24)",
            "classname": "weapon_supernailgun",
            "uuid": 8191300322855786783,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 16236562464842976112,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Shells (26)",
            "classname": "item_shells",
            "uuid": 1857737010706592429,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Spikes (27)",
            "classname": "item_spikes",
            "uuid": 2550569562990521557,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 15662338236299289782,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Lightning (29)",
            "classname": "weapon_lightning",
            "uuid": 2304177502546486698,
            "mp": 1,
        },
        {
            "id": 30,
            "name": "Wetsuit (30)",
            "classname": "item_artifact_wetsuit",
            "uuid": 11810509143381629032,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Megahealth (31)",
            "classname": "item_health",
            "uuid": 6435280503827684399,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Megahealth (32)",
            "classname": "item_health",
            "uuid": 6083587383380996222,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Supershotgun (33)",
            "classname": "weapon_supershotgun",
            "uuid": 8196504982615379102,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Rocketlauncher (34)",
            "classname": "weapon_rocketlauncher",
            "uuid": 17574243407501257869,
            "mp": 1,
        },
        {
            "id": 35,
            "name": "Rockets (35)",
            "classname": "item_rockets",
            "uuid": 9385189020652391631,
            "mp": 1,
        },
        {
            "id": 36,
            "name": "Rockets (36)",
            "classname": "item_rockets",
            "uuid": 780604245060832807,
            "mp": 1,
        },
        {
            "id": 37,
            "name": "Quad Damage (37)",
            "classname": "item_artifact_super_damage",
            "uuid": 11694585146503212524,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Rockets (38)",
            "classname": "item_rockets",
            "uuid": 1039461427274046961,
            "mp": 1,
        },
        {
            "id": 39,
            "name": "Rockets (39)",
            "classname": "item_rockets",
            "uuid": 13448346178330076856,
            "mp": 1,
        },
        {
            "id": 40,
            "name": "Rockets (40)",
            "classname": "item_rockets",
            "uuid": 7801166969936817912,
            "mp": 1,
        },
        {
            "id": 41,
            "name": "Nailgun (41)",
            "classname": "weapon_nailgun",
            "uuid": 5642778036234598894,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 14248105803641530890,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Spikes (43)",
            "classname": "item_spikes",
            "uuid": 16190811070376851992,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Rockets (44)",
            "classname": "item_rockets",
            "uuid": 5601076019561235806,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Rockets (45)",
            "classname": "item_rockets",
            "uuid": 10031226541911699777,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Shells (46)",
            "classname": "item_shells",
            "uuid": 1013315814928003189,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Shells (47)",
            "classname": "item_shells",
            "uuid": 2430082874941484124,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 6584865854031090066,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Large Medkit (49)",
            "classname": "item_health",
            "uuid": 6445321811254048946,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Invulnerability (50)",
            "classname": "item_artifact_invulnerability",
            "uuid": 90217276647730445,
            "mp": 1,
        },
        {
            "id": 51,
            "name": "Laser (51)",
            "classname": "weapon_laser_gun",
            "uuid": 7134169349232778142,
            "mp": 1,
        },
        {
            "id": 52,
            "name": "Rockets (52)",
            "classname": "item_rockets",
            "uuid": 9627680820744958223,
            "mp": 1,
        },
        {
            "id": 53,
            "name": "Rockets (53)",
            "classname": "item_rockets",
            "uuid": 8173025936002388303,
            "mp": 1,
        },
        {
            "id": 54,
            "name": "Cells (54)",
            "classname": "item_cells",
            "uuid": 14399790584199378130,
            "mp": 1,
        },
        {
            "id": 55,
            "name": "Cells (55)",
            "classname": "item_cells",
            "uuid": 6692261787455855324,
            "mp": 1,
        },
        {
            "id": 56,
            "name": "Secret Exit",
            "classname": "trigger_changelevel",
            "uuid": 12187201812683399594,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Gold Key (57)",
            "classname": "item_key2",
            "uuid": 16488787756367712403,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Empathy (58)",
            "classname": "item_artifact_empathy_shields",
            "uuid": 5580242148392091545,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Cells (59)",
            "classname": "item_cells",
            "uuid": 16700025624114668449,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Cells (60)",
            "classname": "item_cells",
            "uuid": 11396970504873622023,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Rockets (61)",
            "classname": "item_rockets",
            "uuid": 13581357040908853524,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Rockets (62)",
            "classname": "item_rockets",
            "uuid": 5095358669911935505,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Megahealth (63)",
            "classname": "item_health",
            "uuid": 5492979006363078931,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Red Armor (64)",
            "classname": "item_armorInv",
            "uuid": 4251806478039870890,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Proximity (65)",
            "classname": "weapon_proximity_gun",
            "uuid": 11864314108101021774,
            "mp": 1,
        },
        {
            "id": 66,
            "name": "Spikes (66)",
            "classname": "item_spikes",
            "uuid": 15689876201726098447,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Shells (67)",
            "classname": "item_shells",
            "uuid": 2818306380931485841,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Large Medkit (68)",
            "classname": "item_health",
            "uuid": 4070479746270651238,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Small Medkit (69)",
            "classname": "item_health",
            "uuid": 12005837487859895382,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Green Armor (70)",
            "classname": "item_armor1",
            "uuid": 13585209808018651729,
            "mp": 1,
        },
        {
            "id": 71,
            "name": "Nailgun (71)",
            "classname": "weapon_nailgun",
            "uuid": 6578043607123923868,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Spikes (72)",
            "classname": "item_spikes",
            "uuid": 14938436452660404169,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Spikes (73)",
            "classname": "item_spikes",
            "uuid": 8732986070625954306,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Secret (74)",
            "classname": "trigger_secret",
            "uuid": 17596551570109627855,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 14574344323935134520,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Rocketlauncher (76)",
            "classname": "weapon_rocketlauncher",
            "uuid": 7320671550624458491,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Secret (77)",
            "classname": "trigger_secret",
            "uuid": 17680663467279871815,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Large Medkit (78)",
            "classname": "item_health",
            "uuid": 726246899015294920,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Small Medkit (79)",
            "classname": "item_health",
            "uuid": 13655227319563857709,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Large Medkit (80)",
            "classname": "item_health",
            "uuid": 13500484891714119854,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Large Medkit (81)",
            "classname": "item_health",
            "uuid": 13250735462565558608,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Large Medkit (82)",
            "classname": "item_health",
            "uuid": 17377965459545966746,
            "mp": 1,
        },
        {
            "id": 83,
            "name": "Large Medkit (83)",
            "classname": "item_health",
            "uuid": 10868408959577180051,
            "mp": 1,
        },
        {
            "id": 84,
            "name": "Shells (84)",
            "classname": "item_shells",
            "uuid": 9413341530866255327,
            "mp": 1,
        },
        {
            "id": 85,
            "name": "Cells (85)",
            "classname": "item_cells",
            "uuid": 2406488437164298079,
            "mp": 1,
        },
        {
            "id": 86,
            "name": "Large Medkit (86)",
            "classname": "item_health",
            "uuid": 11558667018996067900,
            "mp": 0,
        },
        {
            "id": 87,
            "name": "Large Medkit (87)",
            "classname": "item_health",
            "uuid": 15559529439950487184,
            "mp": 0,
        },
        {
            "id": 88,
            "name": "Large Medkit (88)",
            "classname": "item_health",
            "uuid": 17990661876342166977,
            "mp": 0,
        },
        {
            "id": 89,
            "name": "Large Medkit (89)",
            "classname": "item_health",
            "uuid": 2476404193286513055,
            "mp": 0,
        },
        {
            "id": 90,
            "name": "Spikes (90)",
            "classname": "item_spikes",
            "uuid": 8750963090914270640,
            "mp": 0,
        },
        {
            "id": 91,
            "name": "Spikes (91)",
            "classname": "item_spikes",
            "uuid": 9405758998056388798,
            "mp": 0,
        },
        {
            "id": 92,
            "name": "Large Medkit (92)",
            "classname": "item_health",
            "uuid": 8098060961985025373,
            "mp": 0,
        },
        {
            "id": 93,
            "name": "Large Medkit (93)",
            "classname": "item_health",
            "uuid": 16623053246904728262,
            "mp": 0,
        },
        {
            "id": 94,
            "name": "All Kills (94)",
            "classname": "all_kills",
            "uuid": 2351434457984010148,
            "mp": 0,
        },
    ]
    events = ["Laser Bridge Active"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (93)",
                "Large Medkit (92)",
                "Green Armor (70)",
                "Rockets (35)",
                "Rockets (36)",
                "Nailgun (71)",
                "Spikes (72)",
                "Spikes (73)",
                "Shells (28)",
                "Supershotgun (33)",
                "Shells (67)",
                "Shells (26)",
                "Shells (25)",
                "Large Medkit (78)",
                "Small Medkit (79)",
            ],
        )

        dive_area = self.region(
            "Dive Area",
            [
                "Megahealth (63)",
                "Megahealth (31)",
                "Rockets (61)",
                "Rockets (62)",
                "Empathy (58)",
                "Cells (59)",
                "Cells (60)",
                "Wetsuit (30)",
                "Laser Bridge Active",
            ],
        )
        self.connect(ret, dive_area, r.can_dive)
        self.restrict("Laser Bridge Active", r.can_button)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Large Medkit (68)",
                "Small Medkit (69)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)
        self.connect(dive_area, past_door_area, r.can_rj_extr & r.can_jump)

        past_laserbridge_area = self.region(
            "Past Laser Bridge",
            [
                "Proximity (65)",
                "Rockets (38)",
                "Rockets (40)",
                "Rockets (39)",
                "Red Armor (64)",
                "Rocketlauncher (34)",
                "Silver Key (2)",
            ],
        )
        self.connect(
            past_door_area,
            past_laserbridge_area,
            self.event("Laser Bridge Active") | (r.can_rj_extr & r.can_jump),
        )
        self.connect(dive_area, past_laserbridge_area, r.can_rj_extr & r.can_jump)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Cells (16)",
                "Cells (17)",
                "Shells (21)",
                "Shells (20)",
                "Large Medkit (18)",
                "Large Medkit (19)",
                "Rockets (13)",
                "Rockets (14)",
                "Rocketlauncher (76)",
                "Yellow Armor (15)",
            ],
        )
        self.connect(ret, past_silver_door_area, self.silver_key & r.can_dive)

        silver_key_top_area = self.region(
            "Silver Key Top",
            [
                "Shells (22)",
                "Shells (23)",
                "Large Medkit (80)",
                "Large Medkit (81)",
            ],
        )
        self.connect(
            ret,
            silver_key_top_area,
            r.bigjump_hard | r.can_gj_extr | r.can_rj_extr,
        )
        self.connect(
            past_silver_door_area,
            silver_key_top_area,
            r.can_button & (r.can_door | r.bigjump_hard),
        )

        silver_area_ceiling = self.region(
            "Silver Ceiling",
            [
                "Invulnerability (50)",
                "Rockets (52)",
                "Rockets (53)",
                "Cells (55)",
                "Cells (54)",
                "Laser (51)",
            ],
        )
        self.connect(silver_key_top_area, silver_area_ceiling, r.bigjump)

        past_rotating_bridge = self.region(
            "Past Rotating Bridge",
            [
                "Large Medkit (87)",
                "Large Medkit (86)",
                "Secret (74)",
                "Quad Damage (37)",
                "Large Medkit (8)",
                "Large Medkit (7)",
                "Large Medkit (6)",
                "Supernailgun (24)",
                "Spikes (66)",
                "Spikes (27)",
                "Spikes (43)",
                "Spikes (42)",
                "Large Medkit (48)",
                "Large Medkit (49)",
                "Shells (46)",
                "Shells (47)",
                "Rockets (45)",
                "Gold Key (57)",
                "Rockets (44)",
                "Megahealth (32)",
                "Shells (9)",
                "Yellow Armor (1)",
                "Secret (77)",
                "Rockets (4)",
                "Rockets (3)",
                "Nailgun (41)",
                "Grenadelauncher (5)",
                "Proximity (12)",
            ],
        )
        self.connect(
            ret,
            past_rotating_bridge,
            r.bigjump_hard | r.can_gj_extr | r.can_rj_extr,
        )
        self.connect(silver_key_top_area, past_rotating_bridge, r.can_button)

        self.restrict("Secret (74)", r.can_shootswitch)
        self.restrict("Quad Damage (37)", r.can_shootswitch)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Spikes (91)",
                "Spikes (90)",
                "Large Medkit (89)",
                "Large Medkit (88)",
                "Exit",
                "All Kills (94)",
            ],
        )
        self.connect(
            past_rotating_bridge,
            past_gold_door_area,
            self.gold_key
            & (
                r.can_button
                | (r.quad_dmg(1) & r.invuln(1) & (r.can_rj_extr | r.can_gj_extr))
            ),
        )
        # also need access to the laser bridge area for all kills
        self.restrict(
            "All Kills (94)",
            r.backpack(5) & self.event("Laser Bridge Active")
            | (r.can_rj_extr & r.can_jump),
        )

        secret_exit_area = self.region(
            "Secret Exit Area",
            [
                "Secret (11)",
                "Invisibility (10)",
                "Secret Exit",
            ],
        )
        self.connect(
            past_door_area,
            secret_exit_area,
            r.can_shootswitch & r.bigjump & r.difficulty("extreme"),
        )
        self.connect(
            past_laserbridge_area,
            secret_exit_area,
            self.event("Laser Bridge Active") & r.can_shootswitch & r.proximitygun,
        )

        return ret
