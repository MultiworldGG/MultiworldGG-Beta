import typing

from BaseClasses import Region
from .Locations import (TTYDLocation, rogueport, sewers, sewers_westside, sewers_westside_ground, petal_left,
                        petal_right, hooktails_castle, boggly_woods, great_tree, glitzville, twilight_trail,
                        twilight_town, creepy_steeple, keelhaul_key, pirates_grotto, excess_express, riverside,
                        poshley_heights, fahr_outpost, xnaut_fortress, palace, pit, rogueport_westside, riddle_tower,
                        shadow_queen, LocationData, tattlesanity_region)
from . import StateLogic

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def get_regions_dict() -> dict[str, list[LocationData]]:
    """
    Returns a dictionary mapping region names to their corresponding location data lists.
    """
    return {
        "Rogueport": rogueport,
        "Rogueport (Westside)": rogueport_westside,
        "Rogueport Sewers": sewers,
        "Rogueport Sewers Westside": sewers_westside,
        "Rogueport Sewers Westside Ground": sewers_westside_ground,
        "Petal Meadows (Left)": petal_left,
        "Petal Meadows (Right)": petal_right,
        "Hooktail's Castle": hooktails_castle,
        "Boggly Woods": boggly_woods,
        "Great Tree": great_tree,
        "Glitzville": glitzville,
        "Twilight Town": twilight_town,
        "Twilight Trail": twilight_trail,
        "Creepy Steeple": creepy_steeple,
        "Keelhaul Key": keelhaul_key,
        "Pirate's Grotto": pirates_grotto,
        "Excess Express": excess_express,
        "Riverside Station": riverside,
        "Poshley Heights": poshley_heights,
        "Fahr Outpost": fahr_outpost,
        "X-Naut Fortress": xnaut_fortress,
        "Palace of Shadow": palace,
        "Palace of Shadow (Post-Riddle Tower)": riddle_tower,
        "Pit of 100 Trials": pit,
        "Shadow Queen": shadow_queen,
        "Tattlesanity": tattlesanity_region
    }


def get_region_connections_dict(world: "TTYDWorld") -> dict[tuple[str, str], typing.Optional[typing.Callable]]:
    """
    Returns a dictionary mapping region connections (source, target) to their access rules.
    If a rule is None, the connection is always available.
    """
    return {
        ("Menu", "Rogueport"): None,
        ("Menu", "Rogueport (Westside)"): None,
        ("Menu", "Tattlesanity"): None,
        ("Rogueport", "Rogueport Sewers"): None,
        ("Rogueport", "Rogueport Sewers Westside"):
            lambda state: StateLogic.sewer_westside(state, world.player),
        ("Rogueport Sewers Westside", "Twilight Town"):
            lambda state: state.has("Yoshi", world.player),
        ("Rogueport", "Rogueport Sewers Westside Ground"):
            lambda state: StateLogic.sewer_westside_ground(state, world.player),
        ("Rogueport Sewers Westside Ground", "Pit of 100 Trials"):
            lambda state: StateLogic.pit_westside_ground(state, world.player),
        ("Rogueport Sewers Westside Ground", "Rogueport (Westside)"): None,
        ("Rogueport Sewers Westside Ground", "Twilight Town"):
            lambda state: StateLogic.ultra_boots(state, world.player),
        ("Rogueport Sewers", "Pit of 100 Trials"):
            lambda state: StateLogic.pit(state, world.player),
        ("Rogueport", "Shadow Queen"):
            lambda state: StateLogic.palace(state, world.player, world.options.chapter_clears.value),
        ("Rogueport", "Palace of Shadow"):
            lambda state: StateLogic.palace(state, world.player, world.options.chapter_clears.value),
        ("Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"):
            lambda state: StateLogic.riddle_tower(state, world.player),
        ("Palace of Shadow (Post-Riddle Tower)", "Shadow Queen"):
            lambda state: state.can_reach("Palace of Shadow Final Staircase: Ultra Shroom", "Location", world.player),
        ("Rogueport", "Poshley Heights"):
            lambda state: StateLogic.ultra_hammer(state, world.player) and StateLogic.super_boots(state, world.player),
        ("Rogueport", "Fahr Outpost"):
            lambda state: StateLogic.fahr_outpost(state, world.player),
        ("Rogueport", "Keelhaul Key"):
            lambda state: StateLogic.keelhaul_key(state, world.player),
        ("Keelhaul Key", "Pirate's Grotto"):
            lambda state: StateLogic.pirates_grottos(state, world.player),
        ("Rogueport", "Rogueport (Westside)"):
            lambda state: StateLogic.westside(state, world.player),
        ("Rogueport (Westside)", "Glitzville"):
            lambda state: StateLogic.glitzville(state, world.player),
        ("Rogueport (Westside)", "Excess Express"):
            lambda state: StateLogic.excess_express(state, world.player),
        ("Excess Express", "Riverside Station"):
            lambda state: StateLogic.riverside(state, world.player),
        ("Riverside Station", "Poshley Heights"):
            lambda state: StateLogic.poshley_heights(state, world.player),
        ("Rogueport Sewers", "Petal Meadows (Left)"):
            lambda state: StateLogic.petal_left(state, world.player),
        ("Rogueport Sewers", "Boggly Woods"):
            lambda state: StateLogic.boggly_woods(state, world.player),
        ("Twilight Town", "Twilight Trail"):
            lambda state: StateLogic.twilight_trail(state, world.player),
        ("Twilight Trail", "Creepy Steeple"):
            lambda state: StateLogic.steeple(state, world.player),
        ("Rogueport Sewers", "Petal Meadows (Right)"):
            lambda state: StateLogic.petal_right(state, world.player),
        ("Petal Meadows (Left)", "Petal Meadows (Right)"): None,
        ("Petal Meadows (Left)", "Hooktail's Castle"):
            lambda state: StateLogic.hooktails_castle(state, world.player),
        ("Boggly Woods", "Great Tree"):
            lambda state: StateLogic.great_tree(state, world.player),
        ("Fahr Outpost", "X-Naut Fortress"):
            lambda state: StateLogic.moon(state, world.player)
    }


def create_regions(world: "TTYDWorld"):
    # Create menu region (always included)
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # Create other regions from dictionary, excluding any in excluded_regions
    regions_dict = get_regions_dict()
    for name, locations in regions_dict.items():
        if name not in world.excluded_regions:
            create_region(world, name, locations)
        else:
            world.disabled_locations.update([loc.name for loc in locations if loc.name not in world.disabled_locations])


def connect_regions(world: "TTYDWorld"):


    connections_dict = get_region_connections_dict(world)
    names: typing.Dict[str, int] = {}

    # Connect regions based on the connections dictionary, excluding any with excluded regions
    for (source, target), rule in connections_dict.items():
        # Skip connections where either the source or target is in excluded_regions
        if source in world.excluded_regions or target in world.excluded_regions:
            continue
        if source == "Rogueport" and target == "Shadow Queen" and not world.options.palace_skip:
            continue
        if source == "Menu" and target == "Rogueport (Westside)" and not world.options.open_westside:
            continue

        # Verify that both regions exist before trying to connect them
        try:
            world.multiworld.get_region(source, world.player)
            world.multiworld.get_region(target, world.player)
            connect(world, names, source, target, rule)
        except Exception:
            # Skip connections where the region doesn't exist
            # This could happen if one region was excluded by a different mechanism
            continue


def create_region(world: "TTYDWorld", name: str, locations: list[LocationData]):
    """Create a region with the given name and locations."""
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, TTYDLocation)
    world.multiworld.regions.append(reg)


def connect(world: "TTYDWorld",
            used_names: typing.Dict[str, int],
            source: str,
            target: str,
            rule: typing.Optional[typing.Callable] = None):
    """Connect two regions with an optional access rule."""
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    source_region.connect(target_region, name, rule)
