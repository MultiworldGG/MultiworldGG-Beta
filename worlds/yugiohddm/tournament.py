import typing
from .utils import Constants

class Tournament:
    id: int
    name: str
    offset: int
    bitflag: int

    def __init__(self, _id: int, name: str, offset: int, bitflag: int):
        self.id = _id
        self.name = name
        self.offset = offset
        self.bitflag = bitflag

    def __str__(self) -> str:
        return (
            f"{self.name}"
        )

all_tournaments: typing.Tuple[Tournament, ...] = (
    Tournament(0, "Lunch Selects Cup", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 7),
    Tournament(1, "Black Clown Cup", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 6),
    Tournament(2, "Gammon Preliminaries", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 5),
    Tournament(3, "Domino Tournament", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 4),
    Tournament(4, "Japan Rep Tournament", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 3),
    Tournament(5, "World Championship", Constants.DIVISION_1_COMPLETION_OFFSET, 1 << 2),
    Tournament(6, "Pharaoh's Treasure Cup", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 7),
    Tournament(7, "Anubis's Disciple Cup", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 6),
    Tournament(8, "Dominator's Holy War", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 5),
    Tournament(9, "King's Title Cup", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 4),
    Tournament(10, "Millennium Kingdom Cup", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 3),
    Tournament(11, "Last Holy War Cup", Constants.DIVISION_2_COMPLETION_OFFSET, 1 << 2),
    Tournament(12, "Dark Carnival", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 7),
    Tournament(13, "Dark Ceremony", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 6),
    Tournament(14, "Corridor of the Dead", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 5),
    Tournament(15, "Sacrificial Guillotine", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 4),
    Tournament(16, "Coliseum of the Dead", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 3),
    Tournament(17, "The Last Judgment", Constants.DIVISION_3_COMPLETION_OFFSET, 1 << 2)
)

id_to_tournament = {tournament.id for tournament in all_tournaments}
name_to_tournament = {tournament.name: tournament for tournament in all_tournaments}