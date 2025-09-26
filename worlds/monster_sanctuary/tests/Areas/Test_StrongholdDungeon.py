from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class StrongholdDungeonTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_east1_traversal(self):
        # Make sure that if the player falls into the bottom half of this room, that they can get back out
        self.assertAccessible("StrongholdDungeon_East1_SW", "StrongholdDungeon_East1_NE_7",
                              ["Double Jump Boots"])
        self.assertAccessible("StrongholdDungeon_East1_SW", "StrongholdDungeon_East1_NE_7",
                              ["Kongamato"])

    def test_south_locked_door(self):
        self.assertNotAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0", [])
        self.assertNotAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0",
                                 ["Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0",
                              ["Stronghold Dungeon key", "Stronghold Dungeon key"])


class StrongholdDungeonMinimumLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_south_locked_door(self):
        self.assertNotAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0", [])
        self.assertAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0",
                              ["Stronghold Dungeon key"])


class StrongholdDungeonNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_south_accessible_with_no_keys(self):
        self.assertAccessible("StrongholdDungeon_South3", "StrongholdDungeon_South4_4_0", [])


class StrongholdDungeonWithOpenEntrances(TestArea):
    options = {
        "open_stronghold_dungeon": "entrances"
    }

    def test_west_shortcut(self):
        self.assertAccessible("StrongholdDungeon_West4", "BlueCave_East4_0", ["Double Jump Boots"])
        self.assertAccessible("StrongholdDungeon_West4", "BlueCave_East4_0", ["Vaero"])


class StrongholdDungeonWithOpenShortcuts(TestArea):
    options = {
        "open_stronghold_dungeon": "shortcuts"
    }

    def test_south_shortcut(self):
        self.assertAccessible("StrongholdDungeon_West2", "stronghold_dungeon_south_3_shortcut", [])

    def test_west_shortcut(self):
        self.assertNotAccessible("StrongholdDungeon_West4", "BlueCave_East4_0", [])
