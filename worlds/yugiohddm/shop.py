import typing

class ShopProgress:
    id: int
    value: int

    def __init__(self, _id: int, value: int):
        self.id = _id
        self.value = value

    def __str__(self) -> str:
        return (
            f"Shop Progress {self.id} "
        )

all_shop_progress: typing.Tuple[ShopProgress, ...] = (
    ShopProgress(0, 0x00),
    ShopProgress(1, 0x1E),
    ShopProgress(2, 0x2D),
    ShopProgress(3, 0x3C),
    ShopProgress(4, 0x4B),
    ShopProgress(5, 0x5A),
    ShopProgress(6, 0x69),
    ShopProgress(7, 0x78),
    ShopProgress(8, 0x87),
    ShopProgress(9, 0x96),
    ShopProgress(10, 0xB4),
    ShopProgress(11, 0xC3),
    ShopProgress(12, 0xD2),
    ShopProgress(13, 0xE1),
    ShopProgress(14, 0xF0),
    ShopProgress(15, 0xFF),
    ShopProgress(16, 0x10E),
    ShopProgress(17, 0x11D),
    ShopProgress(18, 0xFFFF) # 12C truly
)

id_to_progress = {shop_progress.id for shop_progress in all_shop_progress}
value_to_progress = {shop_progress.value for shop_progress in all_shop_progress}