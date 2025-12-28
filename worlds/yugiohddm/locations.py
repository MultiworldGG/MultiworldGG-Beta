import typing

from BaseClasses import Location, Region, LocationProgressType, Item
from .dice import Dice, all_dice
from .utils import Constants
from .duelists import Duelist, get_duelist_defeat_location_name, ids_to_duelists
from .tournament import Tournament, all_tournaments

def get_location_name_for_dice(dice: Dice) -> str:
    return f"Collect {dice.name}"

def get_location_id_for_dice_id(dice_id: int) -> int:
    return Constants.DICE_COLLECTION_OFFSET + dice_id

def get_location_id_for_dice(dice: Dice) -> int:
    return get_location_id_for_dice_id(dice.id)

def get_location_name_for_duelist(duelist: Duelist) -> str:
    return get_duelist_defeat_location_name(duelist) + " 1"

def get_location_id_for_duelist(duelist: Duelist) -> int:
    return Constants.DUELIST_UNLOCK_OFFSET + duelist.id

def duelist_from_location_id(location_id: int) -> Duelist:
    return ids_to_duelists[location_id - Constants.DUELIST_UNLOCK_OFFSET]

def is_duelist_location_id(location_id: int) -> bool:
    # validate's input of duelist_from_location_id
    return (location_id - Constants.DUELIST_UNLOCK_OFFSET) in ids_to_duelists

def get_2nd_location_name_for_duelist(duelist: Duelist) -> str:
    return get_duelist_defeat_location_name(duelist) + " 2"

def get_2nd_location_id_for_duelist(duelist: Duelist) -> int:
    return (Constants.DUELIST_UNLOCK_OFFSET + duelist.id) * 2

def duelist_from_2nd_location_id(location_id: int) -> Duelist:
    return ids_to_duelists[(location_id // 2) - Constants.DUELIST_UNLOCK_OFFSET]

def is_duelist_2nd_location_id(location_id: int) -> bool:
    # validate's input of duelist_from_2nd_location_id
    return ((location_id //2) - Constants.DUELIST_UNLOCK_OFFSET) in ids_to_duelists

def get_location_name_for_tournament(tournament: Tournament) -> str:
    return f"{tournament} 1"

def get_location_id_for_tournament(tournament: Tournament) -> int:
    return Constants.DIVISION_1_COMPLETION_OFFSET_ID + tournament.id
    # As long as the locations ID's are unique it doesn't matter
    # If they match their proper division here

def get_2nd_location_name_for_tournament(tournament: Tournament) -> str:
    return f"{tournament} 2"

def get_2nd_location_id_for_tournament(tournament: Tournament) -> int:
    return (Constants.DIVISION_1_COMPLETION_OFFSET_ID * 2) + tournament.id

def get_3rd_location_name_for_tournament(tournament: Tournament) -> str:
    return f"{tournament} 3"

def get_3rd_location_id_for_tournament(tournament: Tournament) -> int:
    return (Constants.DIVISION_1_COMPLETION_OFFSET_ID * 3) + tournament.id

class YGODDMLocation(Location):
    game: str

    def __init__(self, region: Region, player: int, name: str, id: int):
        super().__init__(player, name, parent=region)
        self.game = Constants.GAME_NAME
        self.address = id

    def exclude(self) -> None:
        self.progress_type = LocationProgressType.EXCLUDED

    def place(self, item: Item) -> None:
        self.item = item
        item.location = self

class DuelistLocation(YGODDMLocation):
    # Check for a duelist being defeated
    duelist: Duelist

    def __init__(self, region: Region, player: int, duelist: Duelist):
        super().__init__(region, player, get_location_name_for_duelist(duelist), get_location_id_for_duelist(duelist))
        self.duelist = duelist

class Duelist2ndLocation(YGODDMLocation):
    # Check for a duelist being defeated
    duelist: Duelist

    def __init__(self, region: Region, player: int, duelist: Duelist):
        super().__init__(region, player, get_2nd_location_name_for_duelist(duelist), get_2nd_location_id_for_duelist(duelist))
        self.duelist = duelist

class TournamentLocation(YGODDMLocation):
    # Check for a tournament being completed
    tournament: Tournament

    def __init__(self, region: Region, player: int, tournament: Tournament):
        super().__init__(region, player, get_location_name_for_tournament(tournament), get_location_id_for_tournament(tournament))
        self.tournament = tournament

class Tournament2ndLocation(YGODDMLocation):
    # Check for a tournament being completed
    tournament: Tournament

    def __init__(self, region: Region, player: int, tournament: Tournament):
        super().__init__(region, player, get_2nd_location_name_for_tournament(tournament), get_2nd_location_id_for_tournament(tournament))
        self.tournament = tournament

class Tournament3rdLocation(YGODDMLocation):
    # Check for a tournament being completed
    tournament: Tournament

    def __init__(self, region: Region, player: int, tournament: Tournament):
        super().__init__(region, player, get_3rd_location_name_for_tournament(tournament), get_3rd_location_id_for_tournament(tournament))
        self.tournament = tournament

class DiceLocation(YGODDMLocation):
    # Check for a die being in the players collection
    dice: Dice

    def __init__(self, region: Region, player: int, dice: Dice):
        super().__init__(region, player, get_location_name_for_dice(dice), get_location_id_for_dice(dice))
        self.dice = dice

dice_location_name_to_id: typing.Dict[str, int] = {}
for dice in all_dice:
    dice_location_name_to_id[get_location_name_for_dice(dice)] = get_location_id_for_dice(dice)

duelist_location_name_to_id: typing.Dict[str, int] = {}
for duelist in Duelist:
    duelist_location_name_to_id[get_location_name_for_duelist(duelist)] = get_location_id_for_duelist(duelist)

duelist_2nd_location_name_to_id: typing.Dict[str, int] = {}
for duelist in Duelist:
    duelist_location_name_to_id[get_2nd_location_name_for_duelist(duelist)] = get_2nd_location_id_for_duelist(duelist)

tournament_location_name_to_id: typing.Dict[str, int] = {}
for tournament in all_tournaments:
    tournament_location_name_to_id[get_location_name_for_tournament(tournament)] = get_location_id_for_tournament(tournament)

tournament_2nd_location_name_to_id: typing.Dict[str, int] = {}
for tournament in all_tournaments:
    tournament_location_name_to_id[get_2nd_location_name_for_tournament(tournament)] = get_2nd_location_id_for_tournament(tournament)

tournament_3rd_location_name_to_id: typing.Dict[str, int] = {}
for tournament in all_tournaments:
    tournament_location_name_to_id[get_3rd_location_name_for_tournament(tournament)] = get_3rd_location_id_for_tournament(tournament)

# Not unless we have dice locations as checks
#location_name_to_id: typing.Dict[str, int] = {**dice_location_name_to_id, **duelist_location_name_to_id, **duelist_rematch_location_name_to_id}
location_name_to_id: typing.Dict[str, int] = {**duelist_location_name_to_id, **duelist_2nd_location_name_to_id, **tournament_location_name_to_id, **tournament_2nd_location_name_to_id, **tournament_3rd_location_name_to_id, **dice_location_name_to_id}