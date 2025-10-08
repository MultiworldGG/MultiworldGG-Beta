from typing import List

from . import MadouOptions
from .data.location_data import (all_locations, starting_spell_locations, souvenir_locations, flight_locations,
                                 bestiary_locations, MadouLocation, base_locations, school_lunch_locations)
from .strings.locations import Bestiary

location_table = all_locations
locations_by_name = {location.name: location for location in location_table}


def create_locations(options: MadouOptions) -> List[MadouLocation]:
    locations = base_locations.copy()
    create_starting_spell_locations(options, locations)
    create_souvenir_locations(options, locations)
    create_flight_locations(options, locations)
    create_bestiary_locations(options, locations)
    create_lunch_locations(options, locations)
    return locations


def create_starting_spell_locations(options: MadouOptions, locations: List[MadouLocation]) -> List[MadouLocation]:
    starting_spells = options.starting_magic.value
    if "Healing" not in starting_spells:
        locations.append(starting_spell_locations[0])
    if "Fire" not in starting_spells:
        locations.append(starting_spell_locations[1])
    if "Ice Storm" not in starting_spells:
        locations.append(starting_spell_locations[2])
    if "Thunder" not in starting_spells:
        locations.append(starting_spell_locations[3])
    return locations


def create_souvenir_locations(options: MadouOptions, locations: List[MadouLocation]) -> List[MadouLocation]:
    if not options.souvenir_hunt:
        return locations
    locations.extend(souvenir_locations)
    return locations


def create_flight_locations(options: MadouOptions, locations: List[MadouLocation]) -> List[MadouLocation]:
    if not options.squirrel_stations:
        return locations
    locations.extend(flight_locations)
    return locations


def create_bestiary_locations(options: MadouOptions, locations: List[MadouLocation]) -> List[MadouLocation]:
    if not options.bestiary:
        return locations
    excluded_locations = []
    if options.skip_fairy_search:
        excluded_locations.append(Bestiary.owlbear)
    included_locations = [location for location in bestiary_locations if location.name not in excluded_locations]
    locations.extend(included_locations)
    return locations


def create_lunch_locations(options: MadouOptions, locations: List[MadouLocation]) -> List[MadouLocation]:
    if options.school_lunch != options.school_lunch.option_anything:
        return locations
    locations.extend(school_lunch_locations)
    return locations
