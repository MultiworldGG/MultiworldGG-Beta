from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class AncientWoodsTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_center_locked_door(self):
        # Test from Center2
        self.assertNotAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1", [])
        self.assertNotAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1",
                                 ["Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1",
                                 ["Ancient Woods key", "Ancient Woods key"])

        # Test from Center5
        self.assertNotAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0", [])
        self.assertNotAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0",
                                 ["Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0",
                                 ["Ancient Woods key", "Ancient Woods key"])

    def test_north_locked_door(self):
        self.assertNotAccessible("AncientWoods_North2", "AncientWoods_North3_10", [])
        self.assertNotAccessible("AncientWoods_North2", "AncientWoods_North3_10",
                                 ["Ancient Woods key"])
        self.assertNotAccessible("AncientWoods_North2", "AncientWoods_North3_10",
                                 ["Ancient Woods key", "Ancient Woods key"])

        self.assertAccessible("AncientWoods_North2", "AncientWoods_North3_10",
                              ["Ancient Woods key", "Ancient Woods key", "Ancient Woods key"])

    def test_east_shortcut(self):
        self.assertNotAccessible("AncientWoods_East1", "ancient_woods_east_shortcut", [])
        self.assertAccessible("AncientWoods_East1", "ancient_woods_east_shortcut", ["Ancient Woods East Shortcut"])

    def test_dark_rooms(self):
        self.assertNotAccessible("AncientWoods_WestDescent_Middle", "AncientWoods_SouthHidden1_West_3",
                                 [])
        self.assertNotAccessible("AncientWoods_WestDescent_Middle", "AncientWoods_SouthHidden1_West_3",
                                 ["Yowie"])
        self.assertAccessible("AncientWoods_WestDescent_Middle", "AncientWoods_SouthHidden1_West_3",
                              ["Yowie", "Glowfly", "Double Jump Boots", "Silvaero"])

    def test_backwards_brutus_access(self):
        self.assertNotAccessible("AncientWoods_SouthHidden4", "AncientWoods_South4_1", [])
        self.assertNotAccessible("AncientWoods_SouthHidden4", "AncientWoods_South4_1", ["Yowie"])
        self.assertNotAccessible("AncientWoods_SouthHidden4", "AncientWoods_South4_1",
                              ["Ancient Woods Brutus Access"])
        self.assertAccessible("AncientWoods_SouthHidden4", "AncientWoods_South4_1",
                              ["Double Jump Boots", "Nightwing", "Ancient Woods Brutus Access"])

        self.assertNotAccessible("AncientWoods_South4", "ancient_woods_brutus_access", [])
        self.assertAccessible("AncientWoods_South4", "ancient_woods_brutus_access", ["Yowie", "Nightwing"])

        self.assertNotAccessible("AncientWoods_South4", "AncientWoods_SouthHidden4_1_0", [])
        self.assertAccessible("AncientWoods_South4", "AncientWoods_SouthHidden4_1_0",
                              ["Ancient Woods Brutus Access"])

    def test_magma_chamber_shortcut(self):
        self.assertNotAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2", [])
        self.assertNotAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2", ["Ancient Woods to Magma Chamber Shortcut"])
        self.assertAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2",
                              ["Ancient Woods to Magma Chamber Shortcut", "Ancient Woods to Magma Chamber Shortcut"])


class AncientWoodsMinimalLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_north_accessible_with_no_keys(self):
        self.assertAccessible("AncientWoods_North2", "AncientWoods_North3_10", [])

    def test_center_locked_door(self):
        self.assertNotAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1", [])
        self.assertNotAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1",
                                 ["Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1",
                              ["Ancient Woods key", "Ancient Woods key"])

        self.assertNotAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0", [])
        self.assertNotAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0",
                                 ["Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center5", "AncientWoods_Center2_1_0",
                              ["Ancient Woods key", "Ancient Woods key"])


class AncientWoodsNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_north_accessible_with_no_keys(self):
        self.assertAccessible("AncientWoods_North2", "AncientWoods_North3_10", [])

    def test_center_accessible_with_no_keys(self):
        self.assertAccessible("AncientWoods_Center2", "AncientWoods_Center5_1_1", [])


class AncientWoodsWithOpenEntrances(TestArea):
    options = {
        "open_ancient_woods": 1
    }

    def test_east_shortcut(self):
        self.assertAccessible("AncientWoods_East1", "ancient_woods_east_shortcut", [])

    def test_backwards_brutus_is_open(self):
        self.assertAccessible("AncientWoods_SouthChampion", "AncientWoods_South4_1",
                              ["Double Jump Boots", "Nightwing"])

        self.assertAccessible("AncientWoods_South4", "AncientWoods_SouthChampion_1_0",
                              ["Double Jump Boots", "Nightwing"])