from typing import Dict

from BaseClasses import ItemClassification


class DebugItemData:
    def __init__(self, code: int, classification: ItemClassification):
        self.code = code
        self.type = classification

item_data_table: Dict[str, DebugItemData] = {
    "TestItem1": DebugItemData(999001, ItemClassification.progression),
    "TestItem2": DebugItemData(999002, ItemClassification.useful),
    "TestItem3": DebugItemData(999003, ItemClassification.progression),
    "TestItem4": DebugItemData(999004, ItemClassification.useful),
    "TestItem5": DebugItemData(999005, ItemClassification.filler),
    "TestItem6": DebugItemData(999006, ItemClassification.progression),
    "TestItem7": DebugItemData(999007, ItemClassification.useful),
    "TestItem8": DebugItemData(999008, ItemClassification.filler),
    "TestItem9": DebugItemData(999009, ItemClassification.progression),
    "TestItem10": DebugItemData(999010, ItemClassification.useful),
}

item_table = {name: data.code for name, data in item_data_table.items()}
