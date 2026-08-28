import unittest

from BaseClasses import PlandoOptions
from worlds import AutoWorldRegister
from Options import OptionCounter, NamedRange, NumericOption, OptionList, OptionSet, Visibility


class TestOptionPresets(unittest.TestCase):
    world_relevant = True

    def test_option_presets_have_valid_options(self):
        """Test that all predefined option presets are valid options."""
        checked = 0
        for game_name, world_type in AutoWorldRegister.testable_worlds.items():
            presets = world_type.web.options_presets
            for preset_name, preset in presets.items():
                for option_name, option_value in preset.items():
                    checked += 1
                    with self.subTest(game=game_name, preset=preset_name, option=option_name):
                        try:
                            option = world_type.options_dataclass.type_hints[option_name].from_any(option_value)
                            # some options may need verification to ensure the provided option is actually valid
                            # pass in all plando options in case a preset wants to require certain plando options
                            # for some reason
                            option.verify(world_type, "Test Player", PlandoOptions(sum(PlandoOptions)))
                            if not (Visibility.complex_ui in option.visibility or Visibility.simple_ui in option.visibility):
                                self.fail(f"'{option_name}' in preset '{preset_name}' for game '{game_name}' is not "
                                          f"visible in any supported UI.")
                            supported_types = [NumericOption, OptionSet, OptionList, OptionCounter]
                            if not any([issubclass(option.__class__, t) for t in supported_types]):
                                self.fail(f"'{option_name}' in preset '{preset_name}' for game '{game_name}' "
                                          f"is not a supported type for webhost. "
                                          f"Supported types: {', '.join([t.__name__ for t in supported_types])}")
                        except AssertionError as ex:
                            self.fail(f"Option '{option_name}': '{option_value}' in preset '{preset_name}' for game "
                                      f"'{game_name}' is not valid. Error: {ex}")
                        except KeyError as ex:
                            self.fail(f"Option '{option_name}' in preset '{preset_name}' for game '{game_name}' is "
                                      f"not a defined option. Error: {ex}")
        # Guard against a vacuous pass: the bundled APQuest/MWQuest worlds always
        # ship presets, so the validation loop above must have actually run.
        self.assertGreater(checked, 0, "No option presets were validated; the world registry "
                                       "appears to be empty or no world exposes options_presets.")

    def test_option_preset_values_are_explicitly_defined(self):
        """Test that option preset values are not a special flavor of 'random' or use from_text to resolve another
        value.
        """
        checked = 0
        for game_name, world_type in AutoWorldRegister.testable_worlds.items():
            presets = world_type.web.options_presets
            for preset_name, preset in presets.items():
                for option_name, option_value in preset.items():
                    checked += 1
                    with self.subTest(game=game_name, preset=preset_name, option=option_name):
                        # Check for non-standard random values.
                        self.assertFalse(
                            str(option_value).startswith("random-"),
                            f"'{option_name}': '{option_value}' in preset '{preset_name}' for game '{game_name}' "
                            f"is not supported for webhost. Special random values are not supported for presets."
                        )

                        option = world_type.options_dataclass.type_hints[option_name].from_any(option_value)

                        # Check for from_text resolving to a different value. ("random" is allowed though.)
                        if option_value != "random" and isinstance(option_value, str):
                            # Allow special named values for NamedRange option presets.
                            if isinstance(option, NamedRange):
                                self.assertTrue(
                                    option_value in option.special_range_names,
                                    f"Invalid preset '{option_name}': '{option_value}' in preset '{preset_name}' "
                                    f"for game '{game_name}'. Expected {option.special_range_names.keys()} or "
                                    f"{option.range_start}-{option.range_end}."
                                )
                            else:
                                self.assertTrue(
                                    option.name_lookup.get(option.value, None) == option_value,
                                    f"'{option_name}': '{option_value}' in preset '{preset_name}' for game "
                                    f"'{game_name}' is not supported for webhost. Values must not be resolved to a "
                                    f"different option via option.from_text (or an alias)."
                                )
        # Guard against a vacuous pass: see note in test_option_presets_have_valid_options.
        self.assertGreater(checked, 0, "No option presets were validated; the world registry "
                                       "appears to be empty or no world exposes options_presets.")

    def test_apquest_preset_options_resolve_to_expected_values(self):
        """Pin the concrete behavior the preset-validation loops rely on against a known, always-bundled
        world (APQuest). A regression in ``from_any``/``from_text``/``name_lookup`` resolution for Toggle,
        Range, or Choice options must fail here, independent of which third-party worlds happen to be
        registered.
        """
        world_type = AutoWorldRegister.world_types["APQuest"]
        type_hints = world_type.options_dataclass.type_hints
        plando = PlandoOptions(sum(PlandoOptions))

        def resolved(option_name, value):
            option = type_hints[option_name].from_any(value)
            option.verify(world_type, "Test Player", plando)
            return option

        # Toggle: booleans resolve to their canonical 0/1 ints.
        self.assertEqual(resolved("hard_mode", False).value, 0)
        self.assertEqual(resolved("hard_mode", True).value, 1)

        # Range: numeric values are preserved exactly and stay within declared bounds.
        confetti = type_hints["confetti_explosiveness"]
        self.assertEqual((confetti.range_start, confetti.range_end), (0, 10))
        self.assertEqual(resolved("confetti_explosiveness", confetti.range_start).value, 0)
        self.assertEqual(resolved("confetti_explosiveness", confetti.range_end).value, 10)
        self.assertEqual(resolved("trap_chance", 50).value, 50)

        # Choice: the preset's enum-int resolves to the matching member and round-trips through name_lookup.
        sprite = type_hints["player_sprite"]
        human = resolved("player_sprite", sprite.option_human)
        duck = resolved("player_sprite", sprite.option_duck)
        self.assertEqual(human.value, sprite.option_human)
        self.assertEqual(human.current_key, "human")
        self.assertEqual(duck.value, sprite.option_duck)
        self.assertEqual(duck.current_key, "duck")

        # Every value in APQuest's shipped presets must satisfy the webhost contracts the loops enforce:
        # supported numeric type and visible in at least one UI.
        for preset_name, preset in world_type.web.options_presets.items():
            for option_name, option_value in preset.items():
                option = resolved(option_name, option_value)
                self.assertIsInstance(option, NumericOption,
                                      f"{option_name} in preset {preset_name} is not webhost-supported")
                self.assertTrue(
                    Visibility.complex_ui in option.visibility or Visibility.simple_ui in option.visibility,
                    f"{option_name} in preset {preset_name} is not visible in any supported UI",
                )

    def test_preset_value_resolution_guard_rejects_alias_values(self):
        """Pin the alias/``name_lookup`` contract enforced by ``test_option_preset_values_are_explicitly_defined``.

        A canonical option key must round-trip (``name_lookup[from_any(key).value] == key``), while a value
        that resolves to a *different* member via an alias must not -- that is precisely what flags a preset
        value as unsupported for the webhost.
        """
        sprite = AutoWorldRegister.world_types["APQuest"].options_dataclass.type_hints["player_sprite"]

        # Canonical key resolves to itself -> accepted by the guard.
        human = sprite.from_any("human")
        self.assertEqual(human.value, sprite.option_human)
        self.assertEqual(human.name_lookup.get(human.value), "human")

        # "kitty" is an alias of "cat": it resolves to the cat member, so name_lookup yields "cat", not
        # "kitty". The guard's ``name_lookup.get(value) == option_value`` check must therefore be False,
        # i.e. an alias preset value is rejected.
        kitty = sprite.from_any("kitty")
        self.assertEqual(kitty.value, sprite.option_cat)
        self.assertEqual(kitty.current_key, "cat")
        self.assertNotEqual(kitty.name_lookup.get(kitty.value), "kitty")
