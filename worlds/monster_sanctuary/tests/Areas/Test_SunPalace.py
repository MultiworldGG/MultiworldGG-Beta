from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class SunPalaceTests(TestArea):
    def test_raise_center_1(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_1", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_1",
                              ["Double Jump Boots"])

    def test_raise_center_2(self):
        # Test without the water lowered
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Koi", "Double Jump Boots"])

        # Test with the water lowered
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Sun Palace Lower Water"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Double Jump Boots"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Kongamato"])

        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Sun Palace Lower Water", "Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Sun Palace Lower Water", "Sun Palace Lower Water", "Kongamato"])

    def test_raise_center_3(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3", [])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Koi"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Kongamato"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Double Jump Boots"])

        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                              ["Koi", "Kongamato"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                              ["Sun Palace Lower Water", "Sun Palace Lower Water", "Double Jump Boots"])

    def test_lower_water_1(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1", [])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                                 ["Double Jump Boots"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center"])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Kongamato"])

    def test_lower_water_2(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1", [])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                                 ["Double Jump Boots"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Sun Palace Raise Center"])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Sun Palace Raise Center", "Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Sun Palace Raise Center", "Kongamato"])

    # We don't need to test if we can get to the shortcut areas normally
    # because the above tests for the raise_center flags are in the same spots
    # as the shortcuts. So if we can get to one, we can get to the other
    def test_east_shortcut(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_east_shortcut", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_east_shortcut", ["Sun Palace East Shortcut", "Double Jump Boots"])

    def test_west_shortcut(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_west_shortcut", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_west_shortcut", ["Sun Palace West Shortcut"])


class SunPalaceWithOpenEntrances(TestArea):
    options = {
        "open_sun_palace": "entrances"
    }

    def test_sun_palace_entrance_shortcut(self):
        self.assertAccessible("SnowyPeaks_SunPalaceEntrance",
                              "snowy_peaks_sun_palace_entrance_shortcut",
                              [])


class SunPalaceWithRaisedPillars(TestArea):
    options = {
        "open_sun_palace": "raise_pillar"
    }

    def test_center_is_raised(self):
        self.assertAccessible("SunPalace_Center", "SunPalace_North3_3_0",["Kongamato", "Magmapillar"])
        self.assertAccessible("SunPalace_Center", "SunPalace_Center_13", ["Kongamato"])

    def test_water_is_lowered(self):
        self.assertAccessible("SunPalace_Center", "SunPalace_South1_Upper_13", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "SunPalace_South1_Lower_6", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "SunPalace_EastSewers2_6", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "SunPalace_EastSewers6_7", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "SunPalace_WestSewers3_0_0", ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "SunPalace_WestSewers4_4", ["Double Jump Boots", "Koi"])

    def test_east_shortcut(self):
        self.assertAccessible("SunPalace_Center", "sun_palace_east_shortcut", ["Double Jump Boots"])

    def test_west_shortcut(self):
        self.assertAccessible("SunPalace_Center", "sun_palace_west_shortcut", [])
