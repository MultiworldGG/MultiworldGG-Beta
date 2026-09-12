from BaseClasses import Region

from ..base_classes import Q1Level


class E1M1(Q1Level):
    name = "mapname"
    mapfile = "e1m1"
    keys = []
    location_defs = []

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )
        return ret
