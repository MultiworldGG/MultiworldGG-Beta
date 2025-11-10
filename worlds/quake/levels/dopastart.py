from BaseClasses import Region

from ..base_classes import Q1Level


class dopastart(Q1Level):
    name = "Dimension of the Past"
    mapfile = "start_dopa"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 6339693313276421543,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "All Kills (2)",
            "classname": "all_kills",
            "uuid": 11891092947304516721,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Exit",
                "All Kills (2)",
            ],
        )
        return ret
