from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class CliqueItem(Item):
    game = "Clique"


class CliqueItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


item_data: dict[str, CliqueItemData] = {
    # fmt: off
    "Feeling of Satisfaction":                         CliqueItemData(69696969, ItemClassification.progression),
    "Button Activation":                               CliqueItemData(69696968, ItemClassification.progression),
    "A Cool Filler Item (No Satisfaction Guaranteed)": CliqueItemData(69696967),
    # fmt: on
}
