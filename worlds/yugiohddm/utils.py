import typing

from dataclasses import dataclass

@dataclass
class Constants:
    # YGO DDM constants!
    GAME_NAME: str = "Yu-Gi-Oh! Dungeon Dice Monsters"
    VICTORY_ITEM_ID: int = 0x03E30A # Data is 2 Byte size
    VICTORY_ITEM_NAME: str = "Yami Yugi Defeated"
    DUEL_WINS_OFFSET: int = 0x03E30A # Data is 2 Byte size, technically a copy of Victory Item ID
    DUELIST_UNLOCK_OFFSET: int = 0x03E64E # Data is 1 Byte size
    DICE_COLLECTION_OFFSET: int = 0x03E565 # Data is 1 Byte size
    ACTIVE_DICE_OFFSET: int = 0x03E555 # Data is 1 Byte size
    MONEY_OFFSET: int = 0x03E304 # Data is 2 byte size
    SHOP_PROGRESS_OFFSET: int = 0x03E6C0 #Data is 2 byte size
    RECEIVED_DICE_COUNT_OFFSET: int = 0x03E3C4 # Data is 1 Byte size
    DICEPOOL_RANDOMIZED_OFFSET: int = 0x03E3C5 # Data is 1 Byte size
    RECEIVED_GOLD_COUNT_OFFSET: int = 0x03e480 # Data is 1 Byte size
    RECEIVED_SHOP_PROGRESS_COUNT_OFFSET: int = 0x03e481 # Data is 1 Byte size

    DIVISION_1_COMPLETION_OFFSET: int = 0x03E65E # Data is 1 Byte size
    DIVISION_2_COMPLETION_OFFSET: int = 0x03E65F # Data is 1 Byte size
    DIVISION_3_COMPLETION_OFFSET: int = 0x03E660 # Data is 1 Byte size
    DIVISION_COMPLETION_BITFLAG: int = 1 << 0 # 1
    VICTORY_ITEM_TOURNAMENT_NAME: str = "The Last Judgment"
    DIVISION_2_ITEM_NAME: str = "Reverse Division"
    DIVISION_3_ITEM_NAME: str = "Dark Division"
    SHOP_PROGRESSION_ITEM_NAME: str = "Shop Progression"
    SHOP_PROGRESSION_ITEM_ID: int = 0x1
    GOLD_FILLER_ITEM_NAME: str = "Bonus Gold"
    GOLD_FILLER_ITEM_ID: int = 0x2
    # Copies of Tournament offsets -0x10000 to use as ID's rather than the actual offsets (they clash with duelist offsets)
    DIVISION_1_COMPLETION_OFFSET_ID: int = 0x02E65E # Data is 1 Byte size
    DIVISION_2_COMPLETION_OFFSET_ID: int = 0x02E65F # Data is 1 Byte size
    DIVISION_3_COMPLETION_OFFSET_ID: int = 0x02E660 # Data is 1 Byte size
    VICTORY_ITEM_TOURNAMENT_ID: int = 0x02E660 # Data is 1 Byte size, techinically a copy of Division 3 Completion offset_ID

    GENERATED_WITH_KEY: str = "k"
    DUELIST_UNLOCK_ORDER_KEY: str = "d"
    DUELIST_START_UNLOCKED_KEY: str = "s"
    GAME_OPTIONS_KEY: str = "g"