from typing import Dict, Callable, Optional

from BaseClasses import MultiWorld, Region, Location, CollectionState
from worlds.phoa import get_location_data, PhoaOptions
from worlds.phoa.Locations import PhoaLocationData
from worlds.phoa.LogicExtensions import PhoaLogic


def create_regions_and_locations(world: MultiWorld, player: int, options: PhoaOptions):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = split_locations_per_region(
        get_location_data(player, options))

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Overworld"),
        create_region(world, player, locations_per_region, "Anuri Temple")
    ]

    world.regions += regions

    logic = PhoaLogic(player)

    connect(world, player, 'Menu', 'Overworld')
    connect(world, player, 'Overworld', 'Anuri Temple', lambda state: logic.has_anuri_temple_access(state))
    connect(world, player, 'Anuri Temple', 'Overworld')


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, Dict[str, PhoaLocationData]],
                  name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_name, location_data in locations_per_region[name].items():
            location = create_location(player, location_name, location_data, region)
            region.locations.append(location)

    return region


def create_location(player: int, location_name: str, location_data: PhoaLocationData, region: Region):
    location = Location(player, location_data.region + " - " + location_name, location_data.address, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    return location


def connect(world: MultiWorld, player: int, source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    source_region.connect(target_region, rule=rule)


def split_locations_per_region(locations: Dict[str, PhoaLocationData]):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = {}

    for location_name, location_data in locations.items():
        if location_data.region not in locations_per_region:
            locations_per_region[location_data.region] = {}

        locations_per_region[location_data.region][location_name] = location_data

    return locations_per_region
