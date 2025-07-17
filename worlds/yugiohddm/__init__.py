# Credit to sg4e and the YuGiOh Forbidden Memories apworld for being the basis of this project

import typing
import warnings

from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, Region, Tutorial, LocationProgressType
from worlds.generic.Rules import set_rule

from .client import YGODDMClient
from .Constants import GAME_NAME, AUTHOR, IGDB_ID
from .utils import Constants
from .items import YGODDMItem, item_name_to_item_id, create_item as fabricate_item, create_victory_event, create_victory_event_tournament
from .locations import YGODDMLocation, DuelistLocation, DuelistFirstRematchLocation, location_name_to_id as location_map, TournamentLocation
from .dice import Dice, all_dice
from .options import YGODDMOptions, DuelistRematches, Progression
from .duelists import Duelist, all_duelists, map_duelists_to_ids, all_duelists_test
from .tournament import Tournament, all_tournaments, name_to_tournament
from .version import __version__

class YGODDMWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jumza"]
    )

    tutorials = [setup_en]

class YGODDMWorld(World):
    """Yu-Gi-Oh! Dungeon Dice Monsters is a Game Boy Advance dice-based tactics game based on an original board game
    featured in the Yu-Gi-Oh! storyline."""
    game: str = "Yu-Gi-Oh! Dungeon Dice Monsters"
    author: str = AUTHOR
    igdb_id: int = 49211
    options_dataclass = YGODDMOptions
    options: YGODDMOptions
    required_client_version = (0, 5, 0)
    web = YGODDMWeb()

    duelist_unlock_order: typing.List[Duelist]
    starting_unlocked_duelists: typing.List[Duelist]
    starting_unlocked_duelists_str: typing.List[str]

    location_name_to_id = location_map
    item_name_to_id = item_name_to_item_id
    
    def get_available_duelists(self, state: CollectionState) -> typing.List[Duelist]:
        available_duelists: typing.List[Duelist] = [duelist for duelist in self.starting_unlocked_duelists]
        for d in self.duelist_unlock_order:
            if d not in self.starting_unlocked_duelists:
                if state.has(d.name, self.player):
                    available_duelists.append(d)
        return available_duelists

    def generate_early(self) -> None:
        self.duelist_unlock_order = all_duelists
        self.tournament_locations = all_tournaments
        self.starting_unlocked_duelists = [Duelist.YUGI_MOTO]
        # Figure out which other duelists will start unlocked
        start_duelists: typing.List[Duelist] = [duelist for duelist in all_duelists]
        start_duelists.remove(Duelist.YUGI_MOTO)
        start_duelists.remove(Duelist.YAMI_YUGI)
        self.random.shuffle(start_duelists)
        self.starting_unlocked_duelists += start_duelists[0:self.options.starting_duelists.value - 1]
        self.starting_unlocked_duelists_str = [duelist.name for duelist in self.starting_unlocked_duelists]


    def create_item(self, name: str) -> YGODDMItem:
        return fabricate_item(name, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        if (self.options.progression.value == Progression.option_free_duel):
            # All duelists are accessible from Free Duel, so it is the only region
            free_duel_region = Region("Free Duel", self.player, self.multiworld)

            # Add duelist locations
            # Hold a reference to these to set locked items and victory event

            for duelist in self.duelist_unlock_order:
                if duelist is not Duelist.YAMI_YUGI:
                    duelist_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, duelist)
                    set_rule(duelist_location, (lambda state, d=duelist_location:
                                                d.duelist in self.get_available_duelists(state)))
                    free_duel_region.locations.append(duelist_location)

            # If enabled, add Duelist rematch 1 locations
            if (self.options.duelist_rematches.value == DuelistRematches.option_one_rematch):
                for duelist in self.duelist_unlock_order:
                    if duelist is not Duelist.YAMI_YUGI:
                        duelist_rematch_location: DuelistFirstRematchLocation = DuelistFirstRematchLocation(free_duel_region, self.player, duelist)
                        set_rule(duelist_rematch_location, (lambda state, d=duelist_rematch_location:
                                                    d.duelist in self.get_available_duelists(state)))
                        free_duel_region.locations.append(duelist_rematch_location)

            # if enabled, add money and shop progression locations
            #if (self.options.shop_progress_in_pool):
                
            
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Constants.VICTORY_ITEM_NAME, self.player
            )

            itempool: typing.List[YGODDMItem] = []
            for duelist in self.duelist_unlock_order:
                if duelist not in self.starting_unlocked_duelists and duelist is not Duelist.YAMI_YUGI:
                    itempool.append(self.create_item(duelist.name))

            # Add random Dice items from the pool to fill in empty locations
            filler_slots: int = len(free_duel_region.locations) - len(itempool)
            reward_dice: typing.List[Dice] = [dice for dice in all_dice]
            while len(reward_dice) < filler_slots:
                reward_dice += reward_dice
            self.random.shuffle(reward_dice)

            itempool += [self.create_item(dice.name) for dice in reward_dice][:filler_slots]

            # Set Yami Yugi's item to game victory
            # Set rule so it knows that Yami Yugi can't appear until you have all other duelist items
            yami_yugi_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, Duelist.YAMI_YUGI)
            duelist_names: typing.List[str] = []
            for d in self.duelist_unlock_order:
                if d not in self.starting_unlocked_duelists and d is not Duelist.YAMI_YUGI:
                    duelist_names.append(d.name)

            set_rule(yami_yugi_location, lambda state: state.has_all(duelist_names, self.player))
            yami_yugi_location.place_locked_item(create_victory_event(self.player))
            free_duel_region.locations.append(yami_yugi_location)
            

            self.multiworld.itempool.extend(itempool)

            menu_region.connect(free_duel_region)
            self.multiworld.regions.append(free_duel_region)
            self.multiworld.regions.append(menu_region)
        else:
            # else Progression is Tournament mode
            division_1_region = Region("Division 1", self.player, self.multiworld)
            division_2_region = Region("Division 2", self.player, self.multiworld)
            division_3_region = Region("Division 3", self.player, self.multiworld)

            for tournament in all_tournaments:
                if tournament.name != Constants.VICTORY_ITEM_TOURNAMENT_NAME:
                    if tournament.offset == Constants.DIVISION_1_COMPLETION_OFFSET:
                        tournament_location: TournamentLocation = TournamentLocation(division_1_region, self.player, tournament)
                        division_1_region.locations.append(tournament_location)
                    elif tournament.offset == Constants.DIVISION_2_COMPLETION_OFFSET:
                        tournament_location: TournamentLocation = TournamentLocation(division_2_region, self.player, tournament)
                        set_rule(tournament_location, lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                        division_2_region.locations.append(tournament_location)
                    else:
                        tournament_location: TournamentLocation = TournamentLocation(division_3_region, self.player, tournament)
                        set_rule(tournament_location, lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                        division_3_region.locations.append(tournament_location)
            
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Constants.VICTORY_ITEM_TOURNAMENT_NAME, self.player
            )

            itempool: typing.List[YGODDMItem] = []

            # Add Division 2 and 3 unlock items to pool
            itempool.append(self.create_item(Constants.DIVISION_2_ITEM_NAME))
            itempool.append(self.create_item(Constants.DIVISION_3_ITEM_NAME))

            # Add random Dice items from the pool to fill in empty locations
            filler_slots: int = len(division_1_region.locations) + len(division_2_region.locations) + len(division_3_region.locations) - len(itempool)
            reward_dice: typing.List[Dice] = [dice for dice in all_dice]
            while len(reward_dice) < filler_slots:
                reward_dice += reward_dice
            self.random.shuffle(reward_dice)
            itempool += [self.create_item(dice.name) for dice in reward_dice][:filler_slots]

            # Set The Last Judgment's item to game victory
            the_last_judgment_location: TournamentLocation = TournamentLocation(division_3_region, self.player, name_to_tournament["The Last Judgment"])
            the_last_judgment_location.place_locked_item(create_victory_event_tournament(self.player))
            division_3_region.locations.append(the_last_judgment_location)

            self.multiworld.itempool.extend(itempool)

            menu_region.connect(division_1_region)
            division_1_region.connect(
                division_2_region,
                None,
                lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player)
            )
            division_2_region.connect(
                division_3_region,
                None,
                lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player)
                )
            self.multiworld.regions.append(division_1_region)
            self.multiworld.regions.append(division_2_region)
            self.multiworld.regions.append(division_3_region)
            self.multiworld.regions.append(menu_region)



    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            Constants.DUELIST_UNLOCK_ORDER_KEY: map_duelists_to_ids(self.duelist_unlock_order),
            Constants.GAME_OPTIONS_KEY: self.options.serialize(),
            Constants.DUELIST_START_UNLOCKED_KEY: self.starting_unlocked_duelists_str
        }
