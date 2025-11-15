from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification
from worlds.phoa import PhoaOptions


class PhoaItem(Item):
    game: str = "Phoenotopia: Awakening"


class PhoaItemData(NamedTuple):
    code: int
    type: ItemClassification = ItemClassification.filler
    amount: int = 1


def get_item_data(options: Optional[PhoaOptions]) -> Dict[str, PhoaItemData]:
    items: Dict[str, PhoaItemData] = {
        "Heart Ruby": PhoaItemData(
            code=3,
            type=ItemClassification.useful,
            amount=3,
        ),
        "Energy Gem": PhoaItemData(
            code=4,
            type=ItemClassification.useful,
            amount=2,
        ),
        "Moonstone": PhoaItemData(
            code=5,
            # type=ItemClassification.progression,
            amount=5,
        ),  # Actual amount is 9 (-4 for progression items) (Bart's Head is also replaced)
        "Life Saver": PhoaItemData(
            code=14,
            type=ItemClassification.progression,
        ),
        "Slingshot": PhoaItemData(
            code=30,
            type=ItemClassification.progression,
        ),
        "Bombs": PhoaItemData(
            code=31,
            type=ItemClassification.progression,
        ),
        "Crank Lamp": PhoaItemData(
            code=32,
            type=ItemClassification.progression,
        ),
        "Fishing Rod": PhoaItemData(
            code=40,
            type=ItemClassification.progression,
        ),
        "Doki Herb": PhoaItemData(
            code=45,
            amount=6,
        ),
        "Pumpkin Muffin": PhoaItemData(
            code=47,
        ),
        "Berry Fruit": PhoaItemData(
            code=50,
        ),
        "Perro Egg": PhoaItemData(
            code=52,
            amount=2,
        ),
        "Fruit Jam": PhoaItemData(
            code=57,
        ),
        "Cheese": PhoaItemData(
            code=64,
        ),
        "Milk": PhoaItemData(
            code=67,
        ),
        "Anuri Pearlstone": PhoaItemData(
            code=98,
            type=ItemClassification.progression,
            amount=10,
        ),
        "Lunar Frog": PhoaItemData(
            code=99,
        ),
        "Lunar Vase": PhoaItemData(
            code=100,
        ),
        "Dandelion": PhoaItemData(
            code=101,
            amount=4,
        ),
        "Panselo Potato": PhoaItemData(
            code= 102,
            amount=2,
        ),
        "Mystery Meat": PhoaItemData(
            code=112,
            amount=18,
        ),
        "Dragon's Scale": PhoaItemData(
            code=185,
        ),
        "5 Rin": PhoaItemData(
            code=305,
        ),
        "9 rin": PhoaItemData(
            code=309,
        ),
        "15 rin": PhoaItemData(
            code=315,
            amount=2
        ),
        "20 rin": PhoaItemData(
            code=320,
        ),
        "25 rin": PhoaItemData(
            code=325,
        ),
        "35 rin": PhoaItemData(
            code=335,
            amount=3,
        ),
        # "Sonic Spear": PhoaItemData(
        #     code=7676012,
        #     type=ItemClassification.progression,
        # ),
    }

    if not options:
        return items

    print("Items are being filtered")

    filters = [
        (options.enable_npc_gifts <= 0, [
            ("Pumpkin Muffin", 1),
            ("Panselo Potato", 1),
            ("Fruit Jam", 1),
            ("Mystery Meat", 1),
        ]),
        (options.enable_misc <= 0, [
            ("Dandelion", 4),
            ("Perro Egg", 1),
            ("Cheese", 1),
            ("Berry Fruit", 1),
            ("Doki Herb", 6),
        ]),
        (options.shop_sanity <= 0, [
            ("Panselo Potato", 1),
            ("Perro Egg", 1),
            ("Milk", 1),
        ]),
        (options.enable_small_animal_drops <= 0, [
            ("Mystery Meat", 17),
        ]),
        (options.enable_rin_locations <= 0, [
            ("5 rin", 1),
            ("9 rin", 1),
            ("15 rin", 2),
            ("20 rin", 1),
        ]),
        (options.enable_rin_locations <= 1, [
            ("25 rin", 1),
            ("35 rin", 3),
        ]),
    ]

    for option, adjustments in filters:
        if option:
            for item_name, amount in adjustments:
                items = lower_item_amount(items, item_name, amount)

    return items


def lower_item_amount(item_data: Dict[str, PhoaItemData], item_name: str, amount: int):
    print("removing"+ item_name)
    if item_name not in item_data: return item_data

    current_amount = item_data[item_name].amount
    new_amount = max(0, current_amount - amount)

    item_data[item_name] = item_data[item_name]._replace(amount=new_amount)

    return item_data


item_table = get_item_data(None)
