import unittest

from BaseClasses import PlandoOptions
from Options import Choice, TextChoice, ItemLinks, OptionSet, PlandoConnections, PlandoItems, PlandoTexts
from Utils import restricted_dumps

from worlds.AutoWorld import AutoWorldRegister


class TestOptions(unittest.TestCase):
    world_relevant = True

    def test_options_have_doc_string(self):
        """Test that submitted options have their own specified docstring"""
        for gamename, world_type in AutoWorldRegister.testable_worlds.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        self.assertTrue(option.__doc__)

    def test_option_defaults(self):
        """Test that defaults for submitted options are valid."""
        for gamename, world_type in AutoWorldRegister.testable_worlds.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        if issubclass(option, TextChoice):
                            self.assertTrue(option.default in option.name_lookup,
                                f"Default value {option.default} for TextChoice option {option.__name__} in"
                                f" {gamename} does not resolve to a listed value!"
                            )
                        # Standard "can default generate" test
                        err_raised = None
                        try:
                            option.from_any(option.default)
                        except Exception as ex:
                            err_raised = ex
                        self.assertIsNone(err_raised,
                            f"Default value {option.default} for option {option.__name__} in {gamename}"
                            f" is not valid! Exception: {err_raised}"
                        )


    def test_options_are_not_set_by_world(self):
        """Test that options attribute is not already set"""
        for gamename, world_type in AutoWorldRegister.testable_worlds.items():
            with self.subTest(game=gamename):
                self.assertFalse(hasattr(world_type, "options"),
                                 f"Unexpected assignment to {world_type.__name__}.options!")

    def test_duplicate_options(self) -> None:
        """Tests that a world doesn't reuse the same option class."""
        for game_name, world_type in AutoWorldRegister.testable_worlds.items():
            with self.subTest(game=game_name):
                seen_options = set()
                for option in world_type.options_dataclass.type_hints.values():
                    if not option.visibility:
                        continue
                    self.assertFalse(option in seen_options, f"{option} found in assigned options multiple times.")
                    seen_options.add(option)

    def test_item_links_name_groups(self):
        """Tests that item links successfully unfold item_name_groups"""
        item_link_groups = [
            [{
                "name": "ItemLinkGroup",
                "item_pool": ["Everything"],
                "link_replacement": False,
                "replacement_item": None,
            }],
            [{
                "name": "ItemLinkGroup",
                "item_pool": ["TestItem1", "TestItem2"],
                "link_replacement": False,
                "replacement_item": None,
            }]
        ]
        # Using debug which is a minimal debug world
        world = AutoWorldRegister.world_types["debug"]
        plando_options = PlandoOptions.from_option_string("bosses")
        item_links = [ItemLinks.from_any(item_link_groups[0]), ItemLinks.from_any(item_link_groups[1])]
        for link in item_links:
            link.verify(world, "tester", plando_options)
            self.assertIn("TestItem1", link.value[0]["item_pool"])
            self.assertIn("TestItem2", link.value[0]["item_pool"])
        
        # TODO test that the group created using these options has the items

    def test_item_links_resolve(self):
        """Test that ItemLinks.verify expands item groups and fills defaults."""
        world = AutoWorldRegister.world_types["debug"]
        plando_options = PlandoOptions.from_option_string("items")

        item_links = ItemLinks.from_any([{
            "name": "ItemLinkTest",
            "item_pool": ["Everything"],
            "replacement_item": None,
        }])
        item_links.verify(world, "tester", plando_options)
        resolved = item_links.value[0]

        # "Everything" is the auto-generated group containing every item of the world.
        self.assertCountEqual(resolved["item_pool"], world.item_names)
        self.assertEqual(set(resolved["item_pool"]), set(world.item_names))
        # verify() fills in link_replacement when the player omits it.
        self.assertIsNone(resolved["link_replacement"])

    def test_item_links_name_truncated_and_unique(self):
        """Test that ItemLinks names are truncated to 16 chars and must stay unique."""
        world = AutoWorldRegister.world_types["debug"]
        plando_options = PlandoOptions.from_option_string("items")

        # A name longer than 16 characters is truncated to its first 16 (then re-stripped).
        long_name = ItemLinks.from_any([{
            "name": "ThisNameIsWayTooLongToFitInSixteen",
            "item_pool": ["TestItem1"],
            "replacement_item": None,
        }])
        long_name.verify(world, "tester", plando_options)
        self.assertEqual(long_name.value[0]["name"], "ThisNameIsWayToo")

        # Two links whose names collide after the 16-char truncation are rejected.
        # "SixteenCharsName" is exactly 16 characters, so both truncate to the same value.
        colliding = ItemLinks.from_any([
            {"name": "SixteenCharsNameAlpha", "item_pool": ["TestItem1"], "replacement_item": None},
            {"name": "SixteenCharsNameBeta", "item_pool": ["TestItem2"], "replacement_item": None},
        ])
        with self.assertRaises(Exception) as ctx:
            colliding.verify(world, "tester", plando_options)
        self.assertIn("must be unique", str(ctx.exception))

    def test_item_links_unknown_item_rejected(self):
        """Test that ItemLinks.verify rejects an item that is not in the world."""
        world = AutoWorldRegister.world_types["debug"]
        plando_options = PlandoOptions.from_option_string("items")

        bad = ItemLinks.from_any([{
            "name": "BadPool",
            "item_pool": ["NotARealItem"],
            "replacement_item": None,
        }])
        with self.assertRaises(Exception) as ctx:
            bad.verify(world, "tester", plando_options)
        self.assertIn("NotARealItem", str(ctx.exception))

    def test_pickle_dumps_default(self):
        """Test that default option values can be pickled into database for WebHost generation"""
        for gamename, world_type in AutoWorldRegister.testable_worlds.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        restricted_dumps(option.from_any(option.default))
                        if issubclass(option, Choice) and option.default in option.name_lookup:
                            restricted_dumps(option.from_text(option.name_lookup[option.default]))

    def test_option_set_keys_random(self):
        """Tests that option sets do not contain 'random' and its variants as valid keys"""
        for game_name, world_type in AutoWorldRegister.testable_worlds.items():
            if game_name not in ("Archipelago", "Super Metroid"):
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    if issubclass(option, OptionSet):
                        with self.subTest(game=game_name, option=option_key):
                            self.assertFalse(any(random_key in option.valid_keys for random_key in ("random",
                                                                                                    "random-high",
                                                                                                    "random-low")))
                            for key in option.valid_keys:
                                self.assertFalse("random-range" in key)
    
    def test_pickle_dumps_plando(self):
        """Test that plando options using containers of a custom type can be pickled"""
        # The base PlandoConnections class can't be instantiated directly, create a subclass and then cast it
        class TestPlandoConnections(PlandoConnections):
            entrances = {"An Entrance"}
            exits = {"An Exit"}
        plando_connection_value = PlandoConnections(
            TestPlandoConnections.from_any([{"entrance": "An Entrance", "exit": "An Exit"}])
        )

        plando_values = {
            "PlandoConnections": plando_connection_value,
            "PlandoItems": PlandoItems.from_any([{"item": "Something", "location": "Somewhere"}]),
            "PlandoTexts": PlandoTexts.from_any([{"text": "Some text.", "at": "text_box"}]),
        }

        for option_key, value in plando_values.items():
            with self.subTest(option=option_key):
                restricted_dumps(value)
