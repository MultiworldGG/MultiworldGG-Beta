import unittest

from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import (
    APAutoPatchInterface,
    AutoPatchRegister,
    ImproperlyConfiguredAutoPatchError,
)


class _RegistryGuard:
    """Snapshot the global AutoPatchRegister registries and restore them on exit.

    The metaclass mutates module-global dicts at class-definition time, so any
    fixture patch class defined inside a test leaks into the registries used by
    the rest of the suite unless it is removed afterward.
    """

    def __enter__(self) -> "_RegistryGuard":
        self._patch_types = dict(AutoPatchRegister.patch_types)
        self._file_endings = dict(AutoPatchRegister.file_endings)
        return self

    def __exit__(self, *exc: object) -> None:
        AutoPatchRegister.patch_types.clear()
        AutoPatchRegister.patch_types.update(self._patch_types)
        AutoPatchRegister.file_endings.clear()
        AutoPatchRegister.file_endings.update(self._file_endings)


def _matching_world_name() -> str:
    """A game name that is guaranteed to be a registered world in this run.

    `Test Game` is registered by ``test.general``'s import side effects, so it
    is always present when this test module runs.
    """
    name = "Test Game"
    assert name in AutoWorldRegister.world_types, \
        "test fixture world 'Test Game' is not registered; test.general import side effect changed"
    return name


def _absent_world_name() -> str:
    """A game name that is guaranteed NOT to be a registered world."""
    name = "Patch Without A World"
    assert name not in AutoWorldRegister.world_types
    return name


class TestPatches(unittest.TestCase):
    def test_patch_name_matches_game(self) -> None:
        """Every registered patch's `game` must be the name of a registered world.

        This is the real-world invariant: a patch is looked up by game name, so a
        patch whose ``game`` does not correspond to a world is unreachable. The
        production registries may legitimately contain zero patch types in this
        environment, so the loop is also exercised against controlled fixtures
        below to prove the membership check actually discriminates.
        """
        for game_name in AutoPatchRegister.patch_types:
            with self.subTest(game=game_name):
                self.assertIn(
                    game_name, AutoWorldRegister.world_types,
                    f"Patch '{game_name}' does not match the name of any world.",
                )

        # Make the invariant non-vacuous: a patch whose game IS a world satisfies
        # the membership predicate, and a patch whose game is NOT a world fails it.
        with _RegistryGuard():
            good_game = _matching_world_name()
            bad_game = _absent_world_name()

            class _MatchingPatch(APAutoPatchInterface):
                game = good_game
                patch_file_ending = ".test_matching"

                def patch(self, target: str) -> None:
                    pass

            class _MismatchedPatch(APAutoPatchInterface):
                game = bad_game
                patch_file_ending = ".test_mismatch"

                def patch(self, target: str) -> None:
                    pass

            self.assertIn(_MatchingPatch.game, AutoPatchRegister.patch_types)
            self.assertIn(_MismatchedPatch.game, AutoPatchRegister.patch_types)
            # The predicate the invariant relies on must accept the matching patch
            # and reject the mismatched one.
            self.assertIn(_MatchingPatch.game, AutoWorldRegister.world_types)
            self.assertNotIn(_MismatchedPatch.game, AutoWorldRegister.world_types)

    def test_patch_registration_populates_registries(self) -> None:
        """Defining a patch class registers it by game name and by file ending."""
        with _RegistryGuard():
            class _RegisteredPatch(APAutoPatchInterface):
                game = "Registration Probe Game"
                patch_file_ending = ".probepatch"

                def patch(self, target: str) -> None:
                    pass

            self.assertIs(
                AutoPatchRegister.patch_types["Registration Probe Game"],
                _RegisteredPatch,
            )
            self.assertIs(
                AutoPatchRegister.file_endings[".probepatch"],
                _RegisteredPatch,
            )
            self.assertIs(
                AutoPatchRegister.get_handler("some/output.probepatch"),
                _RegisteredPatch,
            )
            self.assertIsNone(AutoPatchRegister.get_handler("some/output.notapatch"))

    def test_patch_without_game_is_not_registered(self) -> None:
        """A subclass that omits `game` must not be added to the registries."""
        with _RegistryGuard():
            before = len(AutoPatchRegister.patch_types)

            class _AbstractMiddle(APAutoPatchInterface):
                # no `game` -> the metaclass must not register this class
                patch_file_ending = ".should_be_ignored"

                def patch(self, target: str) -> None:
                    pass

            self.assertEqual(len(AutoPatchRegister.patch_types), before)
            self.assertNotIn(".should_be_ignored", AutoPatchRegister.file_endings)

    def test_zip_file_ending_rejected(self) -> None:
        with _RegistryGuard():
            with self.assertRaises(ImproperlyConfiguredAutoPatchError) as ctx:
                class _ZipPatch(APAutoPatchInterface):
                    game = "Zip Ending Game"
                    patch_file_ending = ".zip"

                    def patch(self, target: str) -> None:
                        pass

            self.assertIn(".zip", str(ctx.exception))

    def test_missing_file_ending_rejected(self) -> None:
        with _RegistryGuard():
            with self.assertRaises(ImproperlyConfiguredAutoPatchError) as ctx:
                class _NoEndingPatch(APAutoPatchInterface):
                    game = "No Ending Game"

                    def patch(self, target: str) -> None:
                        pass

            self.assertIn("file ending", str(ctx.exception))

    def test_missing_patch_method_rejected(self) -> None:
        with _RegistryGuard():
            with self.assertRaises(ImproperlyConfiguredAutoPatchError) as ctx:
                class _NoPatchMethod(APAutoPatchInterface):
                    game = "No Patch Method Game"
                    patch_file_ending = ".nopatch"
                    patch = None  # type: ignore[assignment]

            self.assertIn("patch method", str(ctx.exception))

    def test_duplicate_file_ending_rejected(self) -> None:
        with _RegistryGuard():
            class _FirstPatch(APAutoPatchInterface):
                game = "First Dup Game"
                patch_file_ending = ".dupext"

                def patch(self, target: str) -> None:
                    pass

            with self.assertRaises(ImproperlyConfiguredAutoPatchError) as ctx:
                class _SecondPatch(APAutoPatchInterface):
                    game = "Second Dup Game"
                    patch_file_ending = ".dupext"

                    def patch(self, target: str) -> None:
                        pass

            self.assertIn("file extension", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
