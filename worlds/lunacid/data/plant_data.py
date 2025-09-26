from dataclasses import dataclass
from typing import List

from .. import LunacidRegion
from ..strings.items import Alchemy


@dataclass(frozen=True)
class AlchemyPlantData:
    drop: str
    regions: List[str]

    def __repr__(self):
        return f"{self.drop} (Regions: {self.regions}"


all_plants: List[AlchemyPlantData] = []


def create_alchemy_data(drop: str, regions: List[str]):
    plant_data = AlchemyPlantData(drop, regions)
    all_plants.append(plant_data)
    return plant_data


all_alchemy_plant_data = [
    create_alchemy_data(Alchemy.ashes, [LunacidRegion.hollow_basin, LunacidRegion.accursed_tomb, LunacidRegion.fetid_mire, LunacidRegion.castle_le_fanu_main_halls,
                                        LunacidRegion.terminus_prison_3f]),
    create_alchemy_data(Alchemy.lotus_seed_pod, [LunacidRegion.fetid_mire]),
    create_alchemy_data(Alchemy.yellow_morel, [LunacidRegion.yosei_forest]),
    create_alchemy_data(Alchemy.destroying_angel_mushroom, [LunacidRegion.yosei_forest]),
    create_alchemy_data(Alchemy.moon_petal, [LunacidRegion.castle_le_fanu_entrance]),
    create_alchemy_data(Alchemy.bloodweed, [LunacidRegion.castle_le_fanu_main_halls]),
    create_alchemy_data(Alchemy.fire_coral, [LunacidRegion.boiling_grotto]),
    create_alchemy_data(Alchemy.fiddlehead, [LunacidRegion.forlorn_arena])
]
