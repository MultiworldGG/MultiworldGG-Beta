from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class UnderworldTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_east_catacomb_shortcut(self):
        self.assertNotAccessible("Underworld_EastCatacomb6_East", "underworld_east_catacomb_6_shortcut", [])
        self.assertAccessible("Underworld_EastCatacomb6_East", "underworld_east_catacomb_6_shortcut",
                              ["Underworld East Catacomb 6 Shortcut"])

    def test_east_catacomb_pillar_control_shortcut(self):
        self.assertNotAccessible("Underworld_EastCatacomb3", "underworld_east_catacomb_pillar_control", [])
        self.assertAccessible("Underworld_EastCatacomb3", "underworld_east_catacomb_pillar_control",
                              ["Underworld East Catacomb 8 Shortcut"])

    def test_west_catacomb_4_shortcut(self):
        self.assertNotAccessible("Underworld_WestCatacomb4_Upper", "Underworld_WestCatacomb4_Lower_11", [])
        self.assertAccessible("Underworld_WestCatacomb4_Upper", "Underworld_WestCatacomb4_Lower_11",
                              ["Underworld West Catacomb 4 Shortcut"])

    def test_west_catacomb_7_shortcut(self):
        self.assertNotAccessible("Underworld_WestCatacomb7_Shortcut", "underworld_west_catacomb_7_shortcut", [])
        self.assertAccessible("Underworld_WestCatacomb7_Shortcut", "underworld_west_catacomb_7_shortcut",
                              ["Underworld West Catacomb 7 Shortcut"])

    def test_east_catacomb_locked_door(self):
        self.assertNotAccessible("Underworld_EastCatacomb3", "Underworld_EastCatacomb4_3", [])
        self.assertAccessible("Underworld_EastCatacomb3", "Underworld_EastCatacomb4_3",
                              ["Underworld key"])

        self.assertNotAccessible("Underworld_EastCatacomb4", "Underworld_EastCatacomb3_13",
                                 ["Underworld East Catacomb Pillar Control"])
        self.assertAccessible("Underworld_EastCatacomb4", "Underworld_EastCatacomb3_13",
                              ["Underworld East Catacomb Pillar Control", "Underworld key"])

    def test_east_catacomb_progression(self):
        # First check that we can't access the end right away
        self.assertNotAccessible("Underworld_Entrance", "underworld_east_catacomb_pillar_control", [])
        self.assertNotAccessible("Underworld_Entrance", "Underworld_Center1_29000021", [])

        # Then check if we can get the key, which is the first logical part of this
        self.assertNotAccessible("Underworld_Entrance", "underworld_east_catacomb_7_access", [])
        self.assertAccessible("Underworld_Entrance", "Underworld_EastCatacomb6_East_4", [])

        # After getting the key, check that we have access to this room
        self.assertAccessible("Underworld_Entrance", "underworld_east_catacomb_7_access",
                              ["Underworld key"])

        # Once catacomb 7 is accessible, test that we can go to the controls, and then progress on
        self.assertAccessible("Underworld_Entrance", "underworld_east_catacomb_pillar_control",
                              ["Underworld East Catacomb 7 Access"])
        self.assertAccessible("Underworld_Entrance", "Underworld_Center1_29000021",
                              ["Underworld East Catacomb Pillar Control"])

    def test_west_catacomb_progression(self):
        # Test that we can't get to the end right away
        self.assertNotAccessible("Underworld_Center2", "Underworld_WestCatacomb9_Interior_Champion", [])
        self.assertNotAccessible("Underworld_Center2", "Underworld_WestCatacomb1_8", [])

        # First check that we can get in to the catacomb from both directions
        self.assertAccessible("Underworld_Center2", "Underworld_WestCatacomb1_8",
                              ["Double Jump Boots", "Kongamato"])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_center_entrance",
                              ["Double Jump Boots", "Kongamato"])
        self.assertNotAccessible("Underworld_Center2", "underworld_west_catacomb_4_shortcut", [])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_4_shortcut",
                              ["Underworld West Catacomb Center Entrance", "Vaero"])

        # Once inside, you need to access the west half of catacomb 4 through catacomb 3
        self.assertNotAccessible("Underworld_Center2", "underworld_west_catacomb_4_access", [])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_4_access",
                              ["Double Jump Boots", "Kongamato", "Brutus"])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_4_access",
                              ["Double Jump Boots", "Kongamato", "Underworld West Catacomb 4 Access"])

        # Now get access to the catacomb 7 shortcut
        # There might be another requirement to get to this location, but that will require player experience
        self.assertNotAccessible("Underworld_Center2", "underworld_west_catacomb_7_shortcut", [])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_7_shortcut",
                              ["Double Jump Boots", "Kongamato", "Underworld West Catacomb 4 Access"])

        # Now the player needs roof access so they can do the final loop around the building
        # There might be another requirement to get to this location, but that will require player experience
        self.assertNotAccessible("Underworld_Center2", "underworld_west_catacomb_roof_access", [])
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_roof_access",
                              ["Double Jump Boots", "Kongamato", "Worm", "Underworld West Catacomb 4 Access"])

        # Finally put it all together to get to the end
        self.assertAccessible("Underworld_Center2", "underworld_west_catacomb_9_interior_access",
                              ["Double Jump Boots", "Kongamato",
                               "Underworld West Catacomb Center Entrance",
                               "Underworld West Catacomb 4 Shortcut",
                               "Underworld West Catacomb 4 Access",
                               "Underworld West Catacomb 7 Shortcut",
                               "Underworld West Catacomb Roof Access"])


class UnderworldMinimumLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_east_catacomb_locked_door(self):
        self.assertNotAccessible("Underworld_EastCatacomb3", "Underworld_EastCatacomb4_3", [])
        self.assertAccessible("Underworld_EastCatacomb3", "Underworld_EastCatacomb4_3",
                              ["Underworld key"])

        self.assertNotAccessible("Underworld_EastCatacomb4", "Underworld_EastCatacomb3_13",
                                 ["Underworld East Catacomb Pillar Control"])
        self.assertAccessible("Underworld_EastCatacomb4", "Underworld_EastCatacomb3_13",
                              ["Underworld East Catacomb Pillar Control", "Underworld key"])


class UnderworldNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_east_accessible_with_no_keys(self):
        self.assertAccessible("Underworld_EastCatacomb3", "Underworld_EastCatacomb4_3", [])
        self.assertAccessible("Underworld_EastCatacomb4", "Underworld_EastCatacomb3_13",
                              ["Underworld East Catacomb Pillar Control"])


class UnderworldWithOpenEntrances(TestArea):
    options = {
        "open_underworld": "entrances",
        "skip_plot": True
    }

    def test_sanctuary_tokens_are_not_needed(self):
        self.assertAccessible(
            "BlueCave_South5",
            "Underworld_East2_1_0",
            []
        )

    def test_sun_palace_shortcut_is_accessible(self):
        self.assertAccessible(
            "SunPalace_EastSewers6",
            "underworld_to_sun_palace_shortcut",
            []
        )


class UnderworldWithOpenShortcuts(TestArea):
    options = {
        "open_underworld": "shortcuts"
    }

    def test_east_catacomb_shortcuts(self):
        self.assertAccessible(
            "Underworld_EastCatacomb6_East",
            "underworld_east_catacomb_6_shortcut",
            []
        )

        self.assertAccessible(
            "Underworld_EastCatacomb3",
            "underworld_east_catacomb_8_shortcut",
            []
        )

    def test_west_catacomb_shortcuts(self):
        self.assertAccessible(
            "Underworld_WestCatacomb4_Upper",
            "Underworld_WestCatacomb4_Lower_11",
            []
        )

        self.assertAccessible(
            "Underworld_WestCatacomb1",
            "underworld_west_catacomb_7_shortcut",
            []
        )

        self.assertAccessible(
            "Underworld_WestCatacomb9_ExteriorEast",
            "Underworld_WestCatacomb9_Roof_12",
            ["Arachlich"]
        )
