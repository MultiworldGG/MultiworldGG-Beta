from BaseClasses import Region

from ..base_classes import Q1Level


class mg1start(Q1Level):
    name = "The Gateway"
    mapfile = "start_mg1"
    keys = []
    location_defs = [
        # {
        #     "id": 1,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 2115333524060900312,
        #     "mp": 0,
        # },
        # {
        #     "id": 2,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 8651750158097738161,
        #     "mp": 0,
        # },
        # {
        #     "id": 3,
        #     "name": "Exit",
        #     "classname": "trigger_changelevel",
        #     "uuid": 16595569416151077344,
        #     "mp": 0,
        # },
        {
            "id": 4,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 5928200913872680509,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "All Kills (5)",
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
                "All Kills (5)",
            ],
        )
        self.restrict("Exit", r.jump)

        return ret
