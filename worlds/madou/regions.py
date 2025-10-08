from dataclasses import dataclass, field
from typing import Protocol, Iterable, List, Optional, Tuple, Dict

from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from .strings.region_entrances import MadouRegion, MadouEntrance


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class EntranceData:
    entrance_name: str
    region_exit: Optional[str] = None
    randomized: bool = False
    dead_end: bool = False
    type: EntranceType = EntranceType.ONE_WAY


madou_regions = [
    RegionData("Menu", ["Menu to House"]),  # One day we can make this vague for starting town setting or whatever.
    RegionData(MadouRegion.arle_house, [MadouEntrance.arle_to_village]),
    RegionData(MadouRegion.magic_village, [MadouEntrance.village_to_arle, MadouEntrance.village_to_school,
                                           MadouEntrance.village_to_forest_of_light, MadouEntrance.village_to_sfj,
                                           MadouEntrance.village_to_nw_cave, MadouEntrance.magic_village_to_tower,
                                           MadouEntrance.magic_to_squirrel, MadouEntrance.magic_to_lookout]),
    RegionData(MadouRegion.suke_house),
    RegionData(MadouRegion.lookout_mountain),
    RegionData(MadouRegion.school, [MadouEntrance.school_to_village, MadouEntrance.school_to_penny, MadouEntrance.school_to_schoolyard,
                                    MadouEntrance.school_to_back_schoolyard]),
    RegionData(MadouRegion.penny_room),
    RegionData(MadouRegion.magic_village_squirrel, [MadouEntrance.flight_magic_to_sage, MadouEntrance.flight_magic_to_ruins,
                                                    MadouEntrance.flight_magic_to_wolf, MadouEntrance.flight_magic_to_ancient,
                                                    MadouEntrance.squirrel_to_magic]),
    RegionData(MadouRegion.back_schoolyard, [MadouEntrance.back_schoolyard_to_school, MadouEntrance.back_schoolyard_to_library]),
    RegionData(MadouRegion.library, [MadouEntrance.library_to_back_schoolyard, MadouEntrance.library_to_secret_library]),
    RegionData(MadouRegion.library_secret),
    RegionData(MadouRegion.schoolyard, [MadouEntrance.schoolyard_to_school, MadouEntrance.schoolyard_to_headmaster]),
    RegionData(MadouRegion.headmaster_office, [MadouEntrance.headmaster_to_school_maze]),
    RegionData(MadouRegion.school_maze),
    RegionData(MadouRegion.magical_tower),

    RegionData(MadouRegion.forest_of_light, [MadouEntrance.forest_of_light_to_village, MadouEntrance.forest_to_frog]),
    RegionData(MadouRegion.frog_swamp, [MadouEntrance.frog_to_forest, MadouEntrance.frog_to_rain_forest]),
    RegionData(MadouRegion.rain_forest, [MadouEntrance.rain_forest_to_ancient_village]),
    RegionData(MadouRegion.ancient_village, [MadouEntrance.ancient_village_to_rain_forest, MadouEntrance.ancient_village_to_squirrel]),
    RegionData(MadouRegion.ancient_village_squirrel, [MadouEntrance.flight_ancient_to_magic, MadouEntrance.squirrel_to_ancient_village,
                                                      MadouEntrance.flight_ancient_to_ruins, MadouEntrance.flight_ancient_to_wolf,
                                                      MadouEntrance.flight_ancient_to_sage]),

    RegionData(MadouRegion.northwest_cave, [MadouEntrance.nw_cave_to_village, MadouEntrance.nw_cave_to_fairy, MadouEntrance.nw_cave_to_smoky]),
    RegionData(MadouRegion.smoky_cave_left, [MadouEntrance.smoky_to_nw_cave, MadouEntrance.smoky_left_to_right, MadouEntrance.smoky_to_bazaar,
                                             MadouEntrance.smoky_to_graveyard]),
    RegionData(MadouRegion.smoky_cave_right, [MadouEntrance.smoky_to_temple]),
    RegionData(MadouRegion.bazaar, [MadouEntrance.bazaar_to_smoky, MadouEntrance.bazaar_to_death]),
    RegionData(MadouRegion.dragon_graveyard),
    RegionData(MadouRegion.dragon_temple),
    RegionData(MadouRegion.fairy_cove, [MadouEntrance.fairy_to_death, MadouEntrance.fairy_to_nw_cave, MadouEntrance.fairy_to_harpy]),
    RegionData(MadouRegion.harpy_mountain),
    RegionData(MadouRegion.death_valley, [MadouEntrance.death_to_bazaar, MadouEntrance.death_to_fairy, MadouEntrance.death_to_ruins_town]),

    RegionData(MadouRegion.ruins_town, [MadouEntrance.ruins_to_cave, MadouEntrance.ruins_to_ancient_ruins, MadouEntrance.ruin_to_squirrel,
                                        MadouEntrance.ruin_to_wolf]),
    RegionData(MadouRegion.ruins_town_squirrel, [MadouEntrance.squirrel_to_ruins, MadouEntrance.flight_ruins_to_magic, MadouEntrance.flight_ruins_to_wolf,
                                                 MadouEntrance.flight_ruins_to_ancient, MadouEntrance.flight_ruins_to_sage]),
    RegionData(MadouRegion.ancient_ruins, [MadouEntrance.ancient_to_zoh]),
    RegionData(MadouRegion.zoh_daimaoh_room),
    RegionData(MadouRegion.wolf_town, [MadouEntrance.wolf_to_squirrel, MadouEntrance.wolf_to_dark_forest, MadouEntrance.wolf_to_sage]),
    RegionData(MadouRegion.wolf_town_squirrel, [MadouEntrance.squirrel_to_wolf, MadouEntrance.flight_wolf_to_magic,
                                                MadouEntrance.flight_wolf_to_ruins, MadouEntrance.flight_wolf_to_ancient,
                                                MadouEntrance.flight_wolf_to_sage]),
    RegionData(MadouRegion.dark_forest, [MadouEntrance.dark_forest_to_maze, MadouEntrance.dark_forest_to_dark_orb,
                                         MadouEntrance.dark_forest_to_wolf, MadouEntrance.dark_forest_to_satan, MadouEntrance.dark_forest_to_well]),
    RegionData(MadouRegion.dark_orb_clearing),
    RegionData(MadouRegion.well),
    RegionData(MadouRegion.satan_mansion),
    RegionData(MadouRegion.dark_maze),

    RegionData(MadouRegion.sage_mountain, [MadouEntrance.sage_to_wolf, MadouEntrance.sage_to_squirrel, MadouEntrance.sage_to_summit]),
    RegionData(MadouRegion.sage_mountain_summit),
    RegionData(MadouRegion.sage_mountain_squirrel, [MadouEntrance.squirrel_to_sage, MadouEntrance.flight_sage_to_ruins,
                                                    MadouEntrance.flight_sage_to_magic, MadouEntrance.flight_sage_to_ancient,
                                                    MadouEntrance.flight_sage_to_wolf]),
]

madou_entrances = [
    EntranceData("Menu to House", MadouRegion.arle_house),
    EntranceData(MadouEntrance.arle_to_village, MadouRegion.magic_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.village_to_arle, MadouRegion.arle_house, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.village_to_school, MadouRegion.school, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.magic_village_to_tower, MadouRegion.magical_tower),
    EntranceData(MadouEntrance.magic_to_squirrel, MadouRegion.magic_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.squirrel_to_magic, MadouRegion.magic_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.school_to_village, MadouRegion.magic_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.village_to_sfj, MadouRegion.suke_house),
    EntranceData(MadouEntrance.magic_to_lookout, MadouRegion.lookout_mountain),

    EntranceData(MadouEntrance.school_to_back_schoolyard, MadouRegion.back_schoolyard, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.back_schoolyard_to_school, MadouRegion.school, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.back_schoolyard_to_library, MadouRegion.library, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.library_to_back_schoolyard, MadouRegion.back_schoolyard, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.school_to_penny, MadouRegion.penny_room, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.school_to_schoolyard, MadouRegion.schoolyard, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.schoolyard_to_school, MadouRegion.school, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.schoolyard_to_headmaster, MadouRegion.headmaster_office, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.library_to_secret_library, MadouRegion.library_secret),
    EntranceData(MadouEntrance.headmaster_to_school_maze, MadouRegion.school_maze),

    EntranceData(MadouEntrance.village_to_nw_cave, MadouRegion.northwest_cave, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.village_to_forest_of_light, MadouRegion.forest_of_light, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.forest_of_light_to_village, MadouRegion.magic_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.forest_to_frog, MadouRegion.frog_swamp, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.frog_to_forest, MadouRegion.forest_of_light, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.frog_to_rain_forest, MadouRegion.rain_forest),
    EntranceData(MadouEntrance.rain_forest_to_ancient_village, MadouRegion.ancient_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.ancient_village_to_rain_forest, MadouRegion.rain_forest, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.ancient_village_to_squirrel, MadouRegion.ancient_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.squirrel_to_ancient_village, MadouRegion.ancient_village, type=EntranceType.TWO_WAY),

    EntranceData(MadouEntrance.nw_cave_to_village, MadouRegion.magic_village, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.nw_cave_to_fairy, MadouRegion.fairy_cove, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.fairy_to_nw_cave, MadouRegion.northwest_cave, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.fairy_to_death, MadouRegion.death_valley, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.death_to_fairy, MadouRegion.fairy_cove, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.death_to_ruins_town, MadouRegion.ruins_town, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.smoky_to_nw_cave, MadouRegion.northwest_cave, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.bazaar_to_death, MadouRegion.death_valley, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.smoky_to_bazaar, MadouRegion.bazaar, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.bazaar_to_smoky, MadouRegion.smoky_cave_left, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.smoky_left_to_right, MadouRegion.smoky_cave_right),
    EntranceData(MadouEntrance.smoky_to_graveyard, MadouRegion.dragon_graveyard),
    EntranceData(MadouEntrance.smoky_to_temple, MadouRegion.dragon_temple),
    EntranceData(MadouEntrance.fairy_to_harpy, MadouRegion.harpy_mountain),
    EntranceData(MadouEntrance.nw_cave_to_smoky, MadouRegion.smoky_cave_left),
    EntranceData(MadouEntrance.death_to_bazaar, MadouRegion.bazaar),

    EntranceData(MadouEntrance.ruins_to_cave, MadouRegion.northwest_cave, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.ruins_to_ancient_ruins, MadouRegion.ancient_ruins, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.ancient_to_zoh, MadouRegion.zoh_daimaoh_room),
    EntranceData(MadouEntrance.ruin_to_wolf, MadouRegion.wolf_town),
    EntranceData(MadouEntrance.ruin_to_squirrel, MadouRegion.ruins_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.squirrel_to_ruins, MadouRegion.ruins_town, type=EntranceType.TWO_WAY),

    EntranceData(MadouEntrance.wolf_to_dark_forest, MadouRegion.dark_forest, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.dark_forest_to_wolf, MadouRegion.wolf_town, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.dark_forest_to_dark_orb, MadouRegion.dark_orb_clearing),
    EntranceData(MadouEntrance.dark_forest_to_satan, MadouRegion.satan_mansion),
    EntranceData(MadouEntrance.dark_forest_to_maze, MadouRegion.dark_maze),
    EntranceData(MadouEntrance.wolf_to_squirrel, MadouRegion.wolf_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.squirrel_to_wolf, MadouRegion.wolf_town, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.wolf_to_sage, MadouRegion.sage_mountain, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.sage_to_wolf, MadouRegion.wolf_town, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.sage_to_squirrel, MadouRegion.sage_mountain_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.squirrel_to_sage, MadouRegion.sage_mountain, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.dark_forest_to_well, MadouRegion.well),
    EntranceData(MadouEntrance.sage_to_summit, MadouRegion.sage_mountain_summit),

    EntranceData(MadouEntrance.flight_magic_to_ruins, MadouRegion.ruins_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ruins_to_magic, MadouRegion.magic_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_magic_to_wolf, MadouRegion.wolf_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_wolf_to_magic, MadouRegion.magic_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_magic_to_ancient, MadouRegion.ancient_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ancient_to_magic, MadouRegion.magic_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_magic_to_sage, MadouRegion.sage_mountain_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_sage_to_magic, MadouRegion.magic_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ancient_to_wolf, MadouRegion.wolf_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ancient_to_ruins, MadouRegion.ruins_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ancient_to_sage, MadouRegion.sage_mountain_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ruins_to_ancient, MadouRegion.ancient_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ruins_to_wolf, MadouRegion.wolf_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_ruins_to_sage, MadouRegion.sage_mountain_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_wolf_to_ruins, MadouRegion.ruins_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_wolf_to_ancient, MadouRegion.ancient_village_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_wolf_to_sage, MadouRegion.sage_mountain_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_sage_to_ruins, MadouRegion.ruins_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_sage_to_wolf, MadouRegion.wolf_town_squirrel, type=EntranceType.TWO_WAY),
    EntranceData(MadouEntrance.flight_sage_to_ancient, MadouRegion.ancient_village_squirrel, type=EntranceType.TWO_WAY),

]


def create_regions(region_factory: RegionFactory, multiworld: MultiWorld) -> Tuple[Dict[str, Region], Dict[str, Entrance]]:
    final_regions = madou_regions.copy()
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  final_regions}
    entrances: Dict[str: Entrance] = {}
    for region in regions.values():
        for entrance in region.exits:
            multiworld.register_indirect_condition(region, entrance)
            entrances[entrance.name] = entrance

    for connection in madou_entrances:
        if connection.entrance_name in entrances:
            entrances[connection.entrance_name].randomization_type = connection.type
            entrances[connection.entrance_name].connect(regions[connection.region_exit])
    return regions, entrances
