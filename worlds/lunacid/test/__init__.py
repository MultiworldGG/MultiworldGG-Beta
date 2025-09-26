from test.bases import WorldTestBase
from worlds.lunacid import LunacidWorld


class LunacidTestBase(WorldTestBase):
    game = "Lunacid"
    world: LunacidWorld
