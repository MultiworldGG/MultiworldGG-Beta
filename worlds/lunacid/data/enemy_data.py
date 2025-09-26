from dataclasses import dataclass
from typing import Dict, List

from worlds.lunacid import Enemy
from worlds.lunacid.strings.properties import Elements


@dataclass(frozen=True)
class EnemyData:
    name: str
    immune: List[str]


all_enemy_data_by_name: Dict[str, EnemyData] = {}


def add_enemy_data(enemy_data: EnemyData):
    if enemy_data.name not in all_enemy_data_by_name:
        all_enemy_data_by_name[enemy_data.name] = enemy_data
    return enemy_data


all_enemy_data = [
    add_enemy_data(EnemyData(Enemy.kodama, [Elements.light])),
    add_enemy_data(EnemyData(Enemy.yakul, [Elements.light])),
    add_enemy_data(EnemyData(Enemy.poltergeist, [Elements.normal])),
    add_enemy_data(EnemyData(Enemy.phantom, [Elements.normal])),
    add_enemy_data(EnemyData(Enemy.mare, [Elements.normal, Elements.dark])),
    add_enemy_data(EnemyData(Enemy.mi_go, [Elements.normal])),
    add_enemy_data(EnemyData(Enemy.ikurrilb, [Elements.fire])),
    add_enemy_data(EnemyData(Enemy.lunam, [Elements.light])),
    add_enemy_data(EnemyData(Enemy.enlightened_one, [Elements.light, Elements.dark])),
    add_enemy_data(EnemyData(Enemy.centaur, [Elements.poison])),
    add_enemy_data(EnemyData(Enemy.umbra, [Elements.normal]))
]

