from BaseClasses import Location


class CliqueLocation(Location):
    game = "Clique"


location_table: dict[str, int] = {
    # fmt: off
    "The Button":    69696969,
    "The Free Item": 69696968,
    # fmt: on
}
