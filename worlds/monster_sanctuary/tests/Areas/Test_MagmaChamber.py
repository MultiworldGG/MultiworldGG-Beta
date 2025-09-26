from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MagmaChamberTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_north_shortcut(self):
        self.assertNotAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut", [])
        self.assertAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut",
                              ["Magma Chamber North Shortcut"])

    def test_south_shortcut(self):
        self.assertNotAccessible("MagmaChamber_South3_West", "magma_chamber_south_shortcut", [])
        self.assertAccessible("MagmaChamber_South3_West", "magma_chamber_south_shortcut",
                              ["Magma Chamber South Shortcut"])

    def test_center_shortcut(self):
        self.assertNotAccessible("MagmaChamber_Center4_West", "magma_chamber_center_shortcut", [])
        self.assertAccessible("MagmaChamber_Center4_West", "magma_chamber_center_shortcut",
                              ["Magma Chamber Center Shortcut"])

    def test_east_shortcut(self):
        self.assertNotAccessible("MagmaChamber_East1", "magma_chamber_east_shortcut", [])
        self.assertAccessible("MagmaChamber_East1", "magma_chamber_east_shortcut",
                              ["Magma Chamber East Shortcut"])

    def test_forgotten_world_shortcut(self):
        self.assertNotAccessible("MagmaChamber_South9_East", "forgotten_world_to_magma_chamber_shortcut", [])
        self.assertNotAccessible("MagmaChamber_South9_East", "forgotten_world_to_magma_chamber_shortcut",
                              ["Forgotten World to Magma Chamber Shortcut"])
        self.assertAccessible("MagmaChamber_South9_East", "forgotten_world_to_magma_chamber_shortcut",
                                 ["Brutus", "Forgotten World to Magma Chamber Shortcut"])

    def test_forgotten_world_access(self):
        self.assertNotAccessible("MagmaChamber_South8", "MagmaChamber_South7_East_4", [])
        self.assertNotAccessible("MagmaChamber_South8", "MagmaChamber_South7_East_4", ["Yowie"])
        self.assertAccessible("MagmaChamber_South8", "MagmaChamber_South7_East_4", ["Magma Chamber Forgotten World Access"])

        self.assertNotAccessible("MagmaChamber_South7_East", "magma_chamber_forgotten_world_access", [])
        self.assertAccessible("MagmaChamber_South7_East", "magma_chamber_forgotten_world_access", ["Yowie"])

        self.assertNotAccessible("MagmaChamber_South7_East", "MagmaChamber_South8_0", [])
        self.assertAccessible("MagmaChamber_South7_East", "MagmaChamber_South8_0",
                              ["Magma Chamber Forgotten World Access"])

    def test_alchemist_lab_locked_door(self):
        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "MagmaChamber_AlchemistLab_East_27700082",
                                 [])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "MagmaChamber_AlchemistLab_East_27700082",
                              ["Magma Chamber key"])

        self.assertNotAccessible("MagmaChamber_AlchemistLab_East", "MagmaChamber_Center6_Upper_10_0",
                                 [])
        self.assertAccessible("MagmaChamber_AlchemistLab_East", "MagmaChamber_Center6_Upper_10_0",
                              ["Magma Chamber key", "Double Jump Boots"])

    def test_mozzie_room_locked_door(self):
        self.assertNotAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172", [])
        self.assertNotAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172",
                              ["Magma Chamber key", "Double Jump Boots"])
        self.assertAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172",
                              ["Magma Chamber key", "Magma Chamber key", "Double Jump Boots"])

    def test_runestone(self):
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava", [])
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                                 ["Stronghold Dungeon Library Access"])
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                                 ["Runestone Shard"])
        self.assertAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                              ["Stronghold Dungeon Library Access", "Runestone Shard"])

    def test_lava_lowered(self):
        self.assertNotAccessible("MagmaChamber_Center2_Middle", "MagmaChamber_Center2_Lower_16", [])
        self.assertAccessible("MagmaChamber_Center2_Middle", "MagmaChamber_Center2_Lower_16",
                              ["Magma Chamber Lowered Lava"])


class MagmaChamberMinimumLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_mozzie_room_accessible_with_no_keys(self):
        self.assertAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172",
                              ["Double Jump Boots"])

    def test_alchemist_lab_locked_door(self):
        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "MagmaChamber_AlchemistLab_East_27700082",
                                 [])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "MagmaChamber_AlchemistLab_East_27700082",
                              ["Magma Chamber key"])

        self.assertNotAccessible("MagmaChamber_AlchemistLab_East", "MagmaChamber_Center6_Upper_10_0",
                                 [])
        self.assertAccessible("MagmaChamber_AlchemistLab_East", "MagmaChamber_Center6_Upper_10_0",
                              ["Magma Chamber key", "Double Jump Boots"])


class MagmaChamberNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_mozzie_room_accessible_with_no_keys(self):
        self.assertNotAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172", [])
        self.assertAccessible("MagmaChamber_Center9_Middle", "MagmaChamber_PuppyRoom_44200172",
                              ["Double Jump Boots"])

    def test_alchemist_lab_accessible_with_no_keys(self):
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "MagmaChamber_AlchemistLab_East_27700082", [])
        self.assertAccessible("MagmaChamber_AlchemistLab_East", "MagmaChamber_Center6_Upper_10_0",
                              ["Double Jump Boots"])


class MagmaChamberPlotlessTests(TestArea):
    options = {
        "skip_plot": 1
    }

    def test_runestone_accessible(self):
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava", [])
        self.assertAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",["Runestone Shard"])


class MagmaChamberWithOpenEntrances(TestArea):
    options = {
        "open_magma_chamber": "entrances"
    }

    def test_magma_chamber_shortcut(self):
        self.assertAccessible("AncientWoods_South1_Lower", "MagmaChamber_North5_Upper_3", [])


class MagmaChamberWithLoweredLava(TestArea):
    options = {
        "open_magma_chamber": "lower_lava"
    }

    def test_lava_is_lowered(self):
        self.assertAccessible("MagmaChamber_Center2_Middle", "MagmaChamber_Center2_Lower_16", [])

    def test_north_shortcut(self):
        self.assertAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut", [])

    def test_center_shortcut(self):
        self.assertAccessible("MagmaChamber_Center4_West", "magma_chamber_center_shortcut", [])

    def test_east_shortcut(self):
        self.assertAccessible("MagmaChamber_East1", "magma_chamber_east_shortcut", [])

    def test_south_shortcut(self):
        self.assertAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut", [])
