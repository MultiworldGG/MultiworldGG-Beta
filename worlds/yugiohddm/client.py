import typing

from typing import TYPE_CHECKING
from NetUtils import ClientStatus
from collections import Counter
import random
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .utils import Constants
from .items import is_dice_item, convert_item_id_to_dice_id, item_id_to_item_name
from .locations import get_location_id_for_duelist, duelist_from_location_id, is_duelist_location_id, get_location_id_for_duelist_rematch, duelist_rematch_from_location_id, is_duelist_rematch_location_id, get_location_id_for_tournament
from .duelists import Duelist, all_duelists, name_to_duelist
from .dice import id_to_dice
from .tournament import Tournament, all_tournaments
from .version import __version__

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

COMBINED_WRAM: typing.Final[str] = "Combined WRAM"

def get_wins_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, "little")

def get_tournament_wins_from_bytes(b: typing.List[bytes]) -> typing.Dict[Tournament, bool]:
    wins_dict: typing.Dict[Tournament, bool] = {}
    for t in all_tournaments:
        wins_dict[t] = int.from_bytes(b[t.offset - Constants.DIVISION_1_COMPLETION_OFFSET], "little") & t.bitflag
    return wins_dict

class YGODDMClient(BizHawkClient):
    game: str = Constants.GAME_NAME
    system: str = "GBA"
    patch_suffix: str = ".apygoddm"
    local_checked_locations: typing.Set[int]
    checked_version_string: bool
    #random: Random

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:

        try:
            # this import down here to prevent circular import issue
            from CommonClient import logger
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 12, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            logger.info(rom_name + " rom_name")
            if not rom_name.startswith("YU-GI-OH DDM"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111 # Has this been set correctly? A little confusion
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        logger.info(f"YGO Dungeon Dice Monsters Client v{__version__}.")
        # Add updates section to logger info
        return True

    async def read_dice_collection(self, ctx: "BizHawkClientContext") -> bytes:
        return (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.DICE_COLLECTION_OFFSET, 200, COMBINED_WRAM)]
        ))[0]
    
    async def read_duelist_collection(self, ctx: "BizHawkClientContext") -> typing.List[int]:
        byte_list_duelists: typing.List[bytes] = []
        for duelist_unlock_byte in range(12):
            byte_list_duelists.append((await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.DUELIST_UNLOCK_OFFSET + duelist_unlock_byte, 1, COMBINED_WRAM)]
        ))[0])
        int_list_duelists: typing.List[int] = []
        for byte in byte_list_duelists:
            int_list_duelists.append(int.from_bytes(byte))
        return int_list_duelists
    
    async def randomize_starting_dice(self, ctx: "BizHawkClientContext"):
        # A byte of free space is used to track whether or not the game has had its dice pool randomized yet
        to_read: typing.Tuple[int, int, str] = [
                (Constants.DICEPOOL_RANDOMIZED_OFFSET, 1, COMBINED_WRAM)
            ]
        randomized_byte = (await bizhawk.read(ctx.bizhawk_ctx, to_read))[0]
        randomized_int = int.from_bytes(randomized_byte)
        # if randomized = 0, randomize. Then set to 1. Otherwise, it is already randomized.
        if randomized_int == 0:
            # Randomize
            rando_dice_ids: typing.Set[int] = set()
            while (len(rando_dice_ids) < 15):
                new_dice_id = random.randint(0, 200)
                while ((new_dice_id in rando_dice_ids) or (new_dice_id not in id_to_dice)):
                    new_dice_id = (new_dice_id + 1) % 201
                rando_dice_ids.add(new_dice_id)
            # Put the Randomized dice into the players collection
            number_of_dice = 1
            for count, dice_id in enumerate(rando_dice_ids):
                await bizhawk.write(ctx.bizhawk_ctx, [(
                    Constants.DICE_COLLECTION_OFFSET + dice_id,
                    number_of_dice.to_bytes(1, "little"),
                    COMBINED_WRAM
                )])
            # We have to obliterate the players real starting dice pool
            removed_dice_id = 0
            for count in range(15):
                await bizhawk.write(ctx.bizhawk_ctx, [(
                    Constants.ACTIVE_DICE_OFFSET + count,
                    removed_dice_id.to_bytes(1, "little"),
                    COMBINED_WRAM
                )])
            # Write to byte in memory to prevent this from happening again
            randomized_byte = 1
            await bizhawk.write(ctx.bizhawk_ctx, [(
                Constants.DICEPOOL_RANDOMIZED_OFFSET,
                randomized_byte.to_bytes(1, "little"),
                COMBINED_WRAM
            )])


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.slot_data is not None:

            # Free Duel Progression goal check
            if not ctx.finished_game and ctx.slot_data[Constants.GAME_OPTIONS_KEY]['progression'] == 0 and any((item.item == Constants.VICTORY_ITEM_ID) for item in ctx.items_received):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            # Tournament Progression goal check
            if not ctx.finished_game and ctx.slot_data[Constants.GAME_OPTIONS_KEY]['progression'] == 1 and any((item.item == Constants.VICTORY_ITEM_TOURNAMENT_ID) for item in ctx.items_received):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            # in YGO FM this is a version mismatch check between user vs generated world

            # Debugging
            from CommonClient import logger

            # Perform client-side starting dice pool randomization
            if (ctx.slot_data[Constants.GAME_OPTIONS_KEY]['randomize_starting_dice']):
                await self.randomize_starting_dice(ctx)

            new_local_check_locations: typing.Set[int]


            # Free Duel Progression in slot data
            if (ctx.slot_data[Constants.GAME_OPTIONS_KEY]['progression'] == 0):
                # Read number of wins over each duelist for 'duelist defeated' locations

                read_list: typing.List[typing.Tuple[int, int, str]] = [
                    (d.wins_address, 2, COMBINED_WRAM) for d in all_duelists
                ]
                wins_bytes: typing.List[bytes] = await bizhawk.read(ctx.bizhawk_ctx, read_list)
                duelists_to_wins: typing.Dict[Duelist, int] = {
                    d: get_wins_from_bytes(w) for d, w in zip(all_duelists, wins_bytes)
                }
                new_local_check_locations = set([
                    get_location_id_for_duelist(key) for key, value in duelists_to_wins.items() if value > 0
                ])

                # Unlock Duelists

                unlocked_duelist_bitflags: typing.List[int] = await self.read_duelist_collection(ctx)
                duelist_bitflag: int = 0
                duelist_bitflag_index: int
                duelist_count: int = 0

                # Unlock initially unlocked duelists

                for duelist_name in ctx.slot_data[Constants.DUELIST_START_UNLOCKED_KEY]:
                    duelist_count = duelist_count + 1
                    duelist_bitflag = name_to_duelist[duelist_name].bitflag
                    duelist_bitflag_index = 0
                    while duelist_bitflag >= 256:
                        duelist_bitflag = duelist_bitflag >> 8
                        duelist_bitflag_index = duelist_bitflag_index + 1
                    unlocked_duelist_bitflags[duelist_bitflag_index] |= duelist_bitflag


                # Unlock duelists based on who has been received
                
                for item in ctx.items_received:
                    if is_duelist_location_id(item.item):
                        duelist_count = duelist_count + 1
                        duelist_bitflag = duelist_from_location_id(item.item).bitflag
                        duelist_bitflag_index = 0
                        while duelist_bitflag >= 256:
                            duelist_bitflag = duelist_bitflag >> 8
                            duelist_bitflag_index = duelist_bitflag_index + 1
                        unlocked_duelist_bitflags[duelist_bitflag_index] |= duelist_bitflag
                
                # Check for Yami Yugi unlock based on number of duelists unlocked
                # If the 91 other duelists are all present, so is Yami Yugi
                if duelist_count >= 91:
                    unlocked_duelist_bitflags[0] |= Duelist.YAMI_YUGI.bitflag

                await bizhawk.write(ctx.bizhawk_ctx, [(
                    Constants.DUELIST_UNLOCK_OFFSET,
                    unlocked_duelist_bitflags,
                    COMBINED_WRAM
                )])
            else:
                # Progression is Tournament

                # Read tournament wins

                read_list: typing.List[typing.Tuple[int, int, str]] = [
                    (Constants.DIVISION_1_COMPLETION_OFFSET, 1, COMBINED_WRAM),
                    (Constants.DIVISION_2_COMPLETION_OFFSET, 1, COMBINED_WRAM),
                    (Constants.DIVISION_3_COMPLETION_OFFSET, 1, COMBINED_WRAM)
                ]
                tournament_wins_bytes: typing.List[bytes] = await bizhawk.read(ctx.bizhawk_ctx, read_list)
                tournaments_to_wins: typing.Dict[Tournament, bool] = get_tournament_wins_from_bytes(tournament_wins_bytes)

                new_local_check_locations = set([
                    get_location_id_for_tournament(key) for key, value in tournaments_to_wins.items() if value
                ])

                # Unlock/Lock Tournament Divisions

                division_2_lock: typing.List[int] = [int.from_bytes(tournament_wins_bytes[0], "little") & 0xFE]
                division_3_lock: typing.List[int] = [int.from_bytes(tournament_wins_bytes[1], "little") & 0xFE]

                for item in ctx.items_received:
                    if item_id_to_item_name[item.item] == Constants.DIVISION_2_ITEM_NAME:
                        division_2_lock[0] = division_2_lock[0] | 0x01
                    elif item_id_to_item_name[item.item] == Constants.DIVISION_3_ITEM_NAME:
                        division_3_lock[0] = division_3_lock[0] | 0x01

                await bizhawk.write(ctx.bizhawk_ctx, [(
                    Constants.DIVISION_1_COMPLETION_OFFSET,
                    division_2_lock,
                    COMBINED_WRAM
                ),
                (
                    Constants.DIVISION_2_COMPLETION_OFFSET,
                    division_3_lock,
                    COMBINED_WRAM
                )])

            # Give out received Dice
            last_dice_received_count: int = int.from_bytes(
                (await bizhawk.read(ctx.bizhawk_ctx, [(Constants.RECEIVED_DICE_COUNT_OFFSET, 1, COMBINED_WRAM)]))[0]
            )
            received_items: typing.List[int] = [
                item.item for item in ctx.items_received
            ]
            received_dice_ids: typing.List[int] = [id for id in received_items if is_dice_item(id)]

            if (len(received_dice_ids) > last_dice_received_count):
                new_received_dice_ids: typing.List[int] = received_dice_ids[last_dice_received_count:]
                new_dice_ids: typing.List[int] = [convert_item_id_to_dice_id(i) for i in new_received_dice_ids]
                # Check if valid Dice id?

                dice_collection_memory: bytes = await self.read_dice_collection(ctx)
                for dice_id, count in Counter(new_dice_ids).items():
                    await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.DICE_COLLECTION_OFFSET + dice_id,
                        (dice_collection_memory[dice_id - 1] + count).to_bytes(1, "little"),
                        COMBINED_WRAM
                    )])

                dice_collection_memory: bytes = await self.read_dice_collection(ctx)

                await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.RECEIVED_DICE_COUNT_OFFSET,
                        len(received_dice_ids).to_bytes(1, "little"),
                        COMBINED_WRAM
                    )])

            if (ctx.slot_data[Constants.GAME_OPTIONS_KEY]['progression'] == 0 and ctx.slot_data[Constants.GAME_OPTIONS_KEY]['duelist_rematches'] == 1):
                # Grab rematch checks
                more_local_check_locations: typing.Set[int] = set([
                    get_location_id_for_duelist_rematch(key) for key, value in duelists_to_wins.items() if value > 1
                ])

                new_local_check_locations = new_local_check_locations.union(more_local_check_locations)
                
            # Local checked checks handling
            if new_local_check_locations != self.local_checked_locations:
                self.local_checked_locations = new_local_check_locations
                if new_local_check_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(new_local_check_locations)
                    }])