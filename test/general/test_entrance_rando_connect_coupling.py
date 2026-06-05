import unittest

from BaseClasses import Region, EntranceType
from entrance_rando import ERPlacementState, EntranceLookup
from test.general import generate_test_multiworld


def _make_two_way_pair(region: Region, name: str, group: int = 1) -> None:
    """Creates a TWO_WAY exit and a matching-named ER target on the region."""
    exit_ = region.create_exit(name)
    exit_.randomization_type = EntranceType.TWO_WAY
    exit_.randomization_group = group
    target = region.create_er_target(name)
    target.randomization_type = EntranceType.TWO_WAY
    target.randomization_group = group


def _build_state(coupled: bool) -> tuple[ERPlacementState, Region, Region]:
    multiworld = generate_test_multiworld()
    a = Region("A", 1, multiworld)
    b = Region("B", 1, multiworld)
    multiworld.regions += [a, b]
    # A has exit "A_door" and a matching-named ER target (the reverse entrance into A);
    # B has exit "B_door" and a matching-named ER target (the target entrance into B).
    _make_two_way_pair(a, "A_door")
    _make_two_way_pair(b, "B_door")

    targets = [e for region in (a, b) for e in region.entrances if not e.parent_region]
    usable_exits = {ex for region in (a, b) for ex in region.exits if not ex.connected_region}
    lookup = EntranceLookup(multiworld.worlds[1].random, coupled, usable_exits, targets)
    state = ERPlacementState(multiworld.worlds[1], lookup, coupled)
    return state, a, b


class TestConnectCoupling(unittest.TestCase):
    def test_coupled_connect_places_reverse_transition(self):
        state, a, b = _build_state(coupled=True)
        source_exit = next(ex for ex in a.exits if ex.name == "A_door")
        target_entrance = next(en for en in b.entrances if en.name == "B_door")

        placed_exits, paired_entrances = state.connect(source_exit, target_entrance)

        # coupled TWO_WAY connect places both the forward and the reverse transition
        self.assertEqual(2, len(placed_exits))
        self.assertEqual(2, len(paired_entrances))
        reverse_exit = next(ex for ex in placed_exits if ex is not source_exit)
        # the reverse exit is B's "B_door" exit, now connected back into A
        self.assertEqual("B_door", reverse_exit.name)
        self.assertEqual(a, reverse_exit.connected_region)
        self.assertEqual(b, source_exit.connected_region)
        # both placements are recorded on the state
        self.assertEqual(2, len(state.placements))
        self.assertEqual(
            {("A_door", "B_door"), ("B_door", "A_door")},
            set(state.pairings),
        )

    def test_uncoupled_connect_does_not_place_reverse_transition(self):
        state, a, b = _build_state(coupled=False)
        source_exit = next(ex for ex in a.exits if ex.name == "A_door")
        target_entrance = next(en for en in b.entrances if en.name == "B_door")

        placed_exits, paired_entrances = state.connect(source_exit, target_entrance)

        # uncoupled connect places only the single forward transition
        self.assertEqual([source_exit], placed_exits)
        self.assertEqual([target_entrance], paired_entrances)
        self.assertEqual(1, len(state.placements))
        # B's reverse exit is left dangling (unconnected)
        reverse_exit = next(ex for ex in b.exits if ex.name == "B_door")
        self.assertIsNone(reverse_exit.connected_region)


if __name__ == "__main__":
    unittest.main()
