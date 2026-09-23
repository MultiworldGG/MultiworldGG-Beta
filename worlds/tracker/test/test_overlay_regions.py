"""group_reachable_by_top_level_branch: the region grouping behind the console's Logic view.

Builds fake region graphs rather than generating a world, so the branch
descent, the category classification and the sort order are pinned without
a multiworld.
"""

import unittest
from types import SimpleNamespace

from BaseClasses import LocationProgressType
from worlds.tracker.overlay_features import (
    CATEGORY_DEFAULT,
    CATEGORY_EXCLUDED,
    CATEGORY_GLITCHED,
    CATEGORY_HINTED,
    CATEGORY_HINTED_GLITCHED,
    group_reachable_by_top_level_branch,
)

_UNREACHABLE = "(Unreachable)"


class _Region:
    def __init__(self, name: str):
        self.name = name
        self.exits: list = []
        self.locations: list = []

    def connect(self, *targets: "_Region") -> None:
        for target in targets:
            self.exits.append(SimpleNamespace(connected_region=target))

    def place(self, name: str, address, excluded: bool = False) -> None:
        self.locations.append(SimpleNamespace(
            name=name, address=address,
            progress_type=(LocationProgressType.EXCLUDED if excluded
                           else LocationProgressType.DEFAULT),
        ))


class _MultiWorld:
    def __init__(self, *regions: _Region, origin: str | None = None):
        self._regions = list(regions)
        if origin is not None:
            self.worlds = {1: SimpleNamespace(origin_region_name=origin)}

    def get_region(self, name: str, player_id: int) -> _Region:
        for region in self._regions:
            if region.name == name:
                return region
        raise KeyError(name)

    def get_regions(self, player_id: int) -> list:
        return list(self._regions)


def _core(multiworld, *, available=(), glitched=(), hints=(), hide_excluded=False,
          player_id=1) -> SimpleNamespace:
    return SimpleNamespace(
        multiworld=multiworld, player_id=player_id,
        locations_available=set(available), glitched_locations=set(glitched),
        hints={addr: None for addr in hints}, hide_excluded=hide_excluded,
    )


def _linear_world(child_count: int = 4) -> tuple[_MultiWorld, list[_Region]]:
    """Menu -> Root -> N children, the shape every world has by contract."""
    menu, root = _Region("Menu"), _Region("Root")
    children = [_Region(f"Branch{i}") for i in range(child_count)]
    menu.connect(root)
    root.connect(*children)
    for i, child in enumerate(children):
        child.place(f"Check {i}", 100 + i)
    return _MultiWorld(menu, root, *children), children


class TestBranchDescent(unittest.TestCase):
    def test_descends_past_the_single_root(self):
        multiworld, children = _linear_world()
        core = _core(multiworld, available=range(100, 104))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual([name for name, _ in branches],
                         [child.name for child in children])

    def test_descent_stops_when_it_stalls(self):
        """Two dead-end children stay the branches -- there is nothing below them."""
        multiworld, children = _linear_world(child_count=2)
        core = _core(multiworld, available=(100, 101))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual([name for name, _ in branches], ["Branch0", "Branch1"])

    def test_regions_below_a_branch_fold_into_it(self):
        multiworld, children = _linear_world()
        deep = _Region("Deep")
        deep.place("Deep Check", 200)
        children[0].connect(deep)
        multiworld._regions.append(deep)
        core = _core(multiworld, available=(100, 200))

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertEqual(sorted(name for name, _ in branches["Branch0"]),
                         ["Check 0", "Deep Check"])

    def test_expanded_region_keeps_its_own_locations(self):
        """Fewer exits than min_branches makes the descent expand a child into
        its children; the expanded child's own locations stay under its name."""
        menu, root = _Region("Menu"), _Region("Root")
        hub, leaf = _Region("Hub"), _Region("Leaf")
        deep_a, deep_b = _Region("Deep A"), _Region("Deep B")
        menu.connect(root)
        root.connect(hub, leaf)
        hub.connect(deep_a, deep_b)
        hub.place("Hub Check", 100)
        leaf.place("Leaf Check", 101)
        deep_a.place("Deep A Check", 102)
        deep_b.place("Deep B Check", 103)
        core = _core(_MultiWorld(menu, root, hub, leaf, deep_a, deep_b),
                     available=(100, 101, 102, 103))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual([name for name, _ in branches], ["Deep A", "Deep B", "Hub", "Leaf"])
        self.assertEqual(dict(branches)["Hub"], [("Hub Check", CATEGORY_DEFAULT)])

    def test_region_off_the_menu_graph_is_unreachable(self):
        multiworld, _children = _linear_world()
        orphan = _Region("Orphan")
        orphan.place("Orphan Check", 300)
        multiworld._regions.append(orphan)
        core = _core(multiworld, available=(100, 300))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual(branches[-1][0], _UNREACHABLE)
        self.assertEqual(branches[-1][1], [("Orphan Check", CATEGORY_DEFAULT)])

    def test_origin_region_comes_from_the_world(self):
        """Manual worlds start at "Manual", APQuest at "Overworld"; none has a Menu."""
        start, room = _Region("Overworld"), _Region("Room")
        start.connect(room)
        room.place("Room Check", 100)
        core = _core(_MultiWorld(start, room, origin="Overworld"), available=(100,))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual(branches, [("Room", [("Room Check", CATEGORY_DEFAULT)])])

    def test_origin_region_locations_are_listed_under_its_name(self):
        """A Manual world keeps every location in its origin region."""
        start = _Region("Manual")
        start.place("Check B", 101)
        start.place("Check A", 100)
        core = _core(_MultiWorld(start, origin="Manual"), available=(100, 101))

        branches = group_reachable_by_top_level_branch(core)

        self.assertEqual(branches, [("Manual", [
            ("Check A", CATEGORY_DEFAULT), ("Check B", CATEGORY_DEFAULT)])])

    def test_no_menu_region_yields_nothing(self):
        region = _Region("Somewhere")
        region.place("Check", 100)
        core = _core(_MultiWorld(region), available=(100,))

        self.assertEqual(group_reachable_by_top_level_branch(core), [])

    def test_uninitialized_core_yields_nothing(self):
        multiworld, _children = _linear_world()
        self.assertEqual(group_reachable_by_top_level_branch(
            _core(multiworld, available=(100,), player_id=None)), [])
        self.assertEqual(group_reachable_by_top_level_branch(
            _core(None, available=(100,))), [])


class TestLocationSelection(unittest.TestCase):
    def _one_branch_core(self, **kwargs) -> tuple[SimpleNamespace, _Region]:
        multiworld, children = _linear_world()
        return _core(multiworld, **kwargs), children[0]

    def test_out_of_logic_locations_are_dropped(self):
        core, branch = self._one_branch_core(available=(101,))
        branch.place("Unreachable Check", 999)

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertNotIn("Branch0", branches)
        self.assertEqual(branches["Branch1"], [("Check 1", CATEGORY_DEFAULT)])

    def test_event_locations_are_dropped(self):
        core, branch = self._one_branch_core(available=(100,))
        branch.place("Victory", None)

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertEqual(branches["Branch0"], [("Check 0", CATEGORY_DEFAULT)])

    def test_glitched_locations_are_opt_out(self):
        multiworld, _children = _linear_world()
        core = _core(multiworld, available=(100,), glitched=(101,))

        with_glitched = dict(group_reachable_by_top_level_branch(core))
        without = dict(group_reachable_by_top_level_branch(core, include_glitched=False))

        self.assertEqual(with_glitched["Branch1"], [("Check 1", CATEGORY_GLITCHED)])
        self.assertNotIn("Branch1", without)

    def test_hinted_and_excluded_classification(self):
        multiworld, _children = _linear_world()
        core = _core(multiworld, available=(100, 102), glitched=(101,), hints=(100, 101))
        multiworld.get_region("Branch2", 1).locations[0].progress_type = \
            LocationProgressType.EXCLUDED

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertEqual(branches["Branch0"], [("Check 0", CATEGORY_HINTED)])
        self.assertEqual(branches["Branch1"], [("Check 1", CATEGORY_HINTED_GLITCHED)])
        self.assertEqual(branches["Branch2"], [("Check 2", CATEGORY_EXCLUDED)])

    def test_hide_excluded_drops_excluded_locations(self):
        multiworld, _children = _linear_world()
        multiworld.get_region("Branch0", 1).locations[0].progress_type = \
            LocationProgressType.EXCLUDED
        core = _core(multiworld, available=(100, 101), hide_excluded=True)

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertNotIn("Branch0", branches)
        self.assertIn("Branch1", branches)

    def test_locations_sort_by_category_then_name(self):
        multiworld, children = _linear_world(child_count=4)
        branch = children[0]
        branch.place("Zebra", 200)
        branch.place("Alpha", 201)
        branch.place("Glitched Check", 202)
        branch.place("Excluded Check", 203, excluded=True)
        core = _core(multiworld, available=(100, 200, 201, 203), glitched=(202,))

        branches = dict(group_reachable_by_top_level_branch(core))

        self.assertEqual(branches["Branch0"], [
            ("Alpha", CATEGORY_DEFAULT),
            ("Check 0", CATEGORY_DEFAULT),
            ("Zebra", CATEGORY_DEFAULT),
            ("Glitched Check", CATEGORY_GLITCHED),
            ("Excluded Check", CATEGORY_EXCLUDED),
        ])


if __name__ == "__main__":
    unittest.main()
