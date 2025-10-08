import logging
from random import Random
from typing import Protocol, Union, List, Dict

from BaseClasses import ItemClassification, Item
from . import MadouOptions
from .data.item_data import (MadouItemData, all_items, spell_items, tool_items, special_items, gem_items, souvenir_items, flight_items,
                                         consumable_items, filler_weights)

logger = logging.getLogger(__name__)


class MadouItemFactory(Protocol):
    def __call__(self, name: Union[str, MadouItemData], override_classification: ItemClassification = None) -> Item:
        raise NotImplementedError


item_table = all_items.copy()
complete_items_by_name = {item.name: item for item in item_table}
all_filler_items = [item.name for item in consumable_items]


def create_items(item_factory: MadouItemFactory, locations_count: int,
                 items_to_exclude: List[Item], options: MadouOptions, random: Random) -> List[Item]:
    items = []
    madou_items = create_madou_items(item_factory, random, options)
    for item in items_to_exclude:
        if item in madou_items:
            madou_items.remove(item)
    assert len(
        madou_items) <= locations_count, (f"There should be at least as many locations [{locations_count}] "
                                            f"as there are mandatory items [{len(madou_items)}]")
    items += madou_items
    logger.debug(f"Created {len(madou_items)} unique items")
    filler_slots = locations_count - len(items)
    create_filler(item_factory, random, filler_slots, items)

    return items


def create_madou_items(item_factory: MadouItemFactory, random: Random, options: MadouOptions) -> List[Item]:
    items = []
    create_spells(item_factory, options, items)
    create_tools(item_factory, items)
    create_gems(item_factory, items)
    create_special_items(item_factory, options, items)
    create_souvenirs(item_factory, options, items)
    create_flight_paths(item_factory, options, items)
    return items


def create_spells(item_factory: MadouItemFactory, options: MadouOptions, items: List[Item]) -> List[Item]:
    quad_spells = ["Progressive Healing", "Progressive Fire", "Progressive Ice Storm", "Progressive Thunder", "Progressive Diacute"]
    starting_spells_from_option = ["Progressive " + spell for spell in options.starting_magic.value]
    spell_item_names = [spell.name for spell in spell_items]
    for spell in spell_item_names:
        if spell not in quad_spells:
            items.append(item_factory(spell))
            continue
        if spell in starting_spells_from_option:
            items.extend(item_factory(item) for item in [spell]*3)
        else:
            items.extend(item_factory(item) for item in [spell]*4)
    return items


def create_tools(item_factory: MadouItemFactory, items: List[Item]) -> List[Item]:
    tool_item_names = [tool.name for tool in tool_items]
    for item in tool_item_names:
        items.append(item_factory(item))
    return items


def create_special_items(item_factory: MadouItemFactory, options: MadouOptions, items: List[Item]) -> List[Item]:
    special_item_names = [special.name for special in special_items]
    for item in special_item_names:
        if item == "Firefly Egg":
            items.extend(item_factory(x) for x in [item]*2)
            continue
        if item == "Secret Stone":
            items.extend(item_factory(x) for x in [item]*8)
        if item == "Rotted Cucumber":
            items.extend(item_factory(x) for x in [item]*9)
        items.append(item_factory(item))
    return items


def create_gems(item_factory: MadouItemFactory, items: List[Item]) -> List[Item]:
    gem_item_names = [gem.name for gem in gem_items]
    for item in gem_item_names:
        items.append(item_factory(item))
    return items


def create_souvenirs(item_factory: MadouItemFactory, options: MadouOptions, items: List[Item]) -> List[Item]:
    if not options.souvenir_hunt:
        return items
    souvenir_item_names = [souvenir.name for souvenir in souvenir_items]
    for item in souvenir_item_names:
        items.append(item_factory(item))
    return items


def create_flight_paths(item_factory: MadouItemFactory, options: MadouOptions, items: List[Item]) -> List[Item]:
    if not options.squirrel_stations:
        return items
    flight_item_names = [flight.name for flight in flight_items]
    for item in flight_item_names:
        items.append(item_factory(item))
    return items


def create_filler(item_factory: MadouItemFactory, random: Random,
                  filler_slots: int, items: List[Item]) -> List[Item]:
    filler_count = filler_slots
    if filler_count == 0:
        return items
    filler_table = random.choices(population=list(filler_weights.keys()), weights=list(filler_weights.values()), k=filler_count)
    for filler in filler_table:
        items.append(item_factory(filler))
    return items


