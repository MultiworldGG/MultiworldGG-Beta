import logging
import struct
import typing
import time
from struct import pack

from NetUtils import ClientStatus, color
from worlds._sni.client import SNIClient
from worlds.tetrisattack import item_table, location_table
from worlds.tetrisattack.Items import progressive_items
from worlds.tetrisattack.Rom import GOALS_POSITION, DEATHLINKHINT, MASKED_VERSION, SRAM_FACTOR

if typing.TYPE_CHECKING:
    from worlds._sni.context import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

TETRISATTACK_APVERSION = ROM_START + 0x007FB0
APVERSION_SIZE = 0x06
TETRISATTACK_ROMHASH_START = ROM_START + 0x007FC0
ROMHASH_SIZE = 0x15

GAME_STATE = WRAM_START + 0x02A0
SRAM_SNI_BAND_START = SRAM_START + 0x0400
SNI_BAND_SIZE = 0x10
SNI_RECEIVED_ITEM_NUMBER = 0x0
SNI_RECEIVED_ITEM_ID = 0x2
SNI_RECEIVED_ITEM_ACTION = 0x4
SNI_RECEIVED_ITEM_ARG = 0x6
SNI_RECEIVE_CHECK = 0x08
SNI_DEATHLINK_TRIGGER = 0xC
SNI_DEATHLINK_EVENT = 0xE
STAGECLEARLASTSTAGE_COMPLETED = SRAM_START + location_table["Stage Clear Last Stage Clear"].code
PUZZLEL6_COMPLETED = SRAM_START + location_table["Puzzle Round 6 Clear"].code
EXTRAPUZZLEL6_COMPLETED = SRAM_START + location_table["Extra Puzzle Round 6 Clear"].code
VSSTAGES_COMPLETED = SRAM_START + 0x225
SRAM_AP_REGION_OFFSET = 0x020
SRAM_AP_REGION_END = pow(2, SRAM_FACTOR)
SRAM_AP_REGION_LENGTH = SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET

ACTION_CODE_NOOP = 0
ACTION_CODE_RECEIVED_ITEM = 2
ACTION_CODE_LAST_STAGE = 3
ACTION_CODE_MARK_COMPLETE = 5
ACTION_CODE_RECEIVED_SCORE = 7

STAGE_CLEAR_ROUND_6_CLEAR = SRAM_START + location_table["Stage Clear Round 6 Clear"].code
STAGE_CLEAR_LAST_STAGE_UNLOCK = SRAM_START + item_table["Stage Clear Last Stage"].code
STAGE_CLEAR_SPECIAL_STAGE_TRAP = SRAM_START + item_table["Stage Clear Special Stage Trap"].code


class TetrisAttackSNIClient(SNIClient):
    game = "Tetris Attack"
    patch_suffix = ".aptatk"
    awaiting_deathlink_event = False
    currently_dead = False
    all_goals = None
    deathlink_hint = None
    looked_through_locations = False

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from worlds._sni.client import snes_read
        from Utils import __version__

        rom_prefix = await snes_read(ctx, TETRISATTACK_APVERSION, APVERSION_SIZE)
        expected_prefix = f'ATK{__version__.replace(".", "")[0:3]}'
        prefix_bytes = bytearray(expected_prefix, 'utf8')
        if rom_prefix is None or not rom_prefix.startswith(prefix_bytes):
            return False
        rom_hash = await snes_read(ctx, TETRISATTACK_ROMHASH_START, ROMHASH_SIZE)
        expected_hash = f'{format(MASKED_VERSION, 'X')}'
        hash_bytes = bytearray(expected_hash, 'utf8')
        if rom_hash is None or not rom_hash.startswith(hash_bytes):
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_hash

        return True

    async def deathlink_kill_player(self, ctx):
        from worlds._sni.client import snes_buffered_write, snes_flush_writes, DeathState
        self.awaiting_deathlink_event = True
        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_DEATHLINK_EVENT, pack("H", 1))
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from worlds._sni.client import snes_buffered_write, snes_flush_writes, snes_read

        rom = await snes_read(ctx, TETRISATTACK_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            self.all_goals = None
            self.deathlink_hint = None
            self.looked_through_locations = False
            return

        if self.all_goals is None:
            self.all_goals = await snes_read(ctx, GOALS_POSITION, 0x3)
        if self.deathlink_hint is None:
            self.deathlink_hint = await snes_read(ctx, DEATHLINKHINT, 0x1)

        # Initial conditions are good, let's interact
        if "Deathlink" not in ctx.tags:
            if self.deathlink_hint is not None and self.deathlink_hint[0] != 0:
                await ctx.update_death_link(True)

        # Check if topped out or ran out of moves
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            game_state = await snes_read(ctx, GAME_STATE, 0x1)
            if game_state is not None:
                message = ""
                deathlink_trigger = await snes_read(ctx, SRAM_SNI_BAND_START + SNI_DEATHLINK_TRIGGER, 0x1)
                if deathlink_trigger is not None and deathlink_trigger[0] > 0:
                    if self.awaiting_deathlink_event:
                        self.awaiting_deathlink_event = False
                    else:
                        if ctx.slot:
                            message = get_deathlink_message(ctx.player_names[ctx.slot], deathlink_trigger[0])
                    self.currently_dead = True
                    ctx.last_death_link = time.time()
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_DEATHLINK_TRIGGER, pack("H", 0))
                elif game_state[0] != 5:
                    self.currently_dead = False
                if not self.awaiting_deathlink_event:
                    await ctx.handle_deathlink_state(self.currently_dead, message)

        # Check if game is ready to receive
        sni_data = await snes_read(ctx, SRAM_SNI_BAND_START, SNI_BAND_SIZE)
        if sni_data is None:
            return
        sni_16_bit_data = struct.unpack("8H", sni_data)
        if sni_16_bit_data[SNI_RECEIVED_ITEM_ACTION >> 1] > 0x00:
            return
        received_item_count = sni_16_bit_data[SNI_RECEIVED_ITEM_NUMBER >> 1]
        receive_check = sni_16_bit_data[SNI_RECEIVE_CHECK >> 1]
        if receive_check < received_item_count and receive_check < 32768:
            return

        # Grab the entire Archipelago SRAM region
        sram_bytes = await snes_read(ctx, SRAM_START + SRAM_AP_REGION_OFFSET, SRAM_AP_REGION_LENGTH)

        # Look through goal checks
        if not ctx.finished_game:
            goals_met = False
            if self.all_goals is not None:
                goals_met = True
                if self.all_goals[0] != 0:
                    sc_last_stage_clear = sram_bytes[
                        STAGECLEARLASTSTAGE_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if sc_last_stage_clear is None or sc_last_stage_clear == 0:
                        goals_met = False
                    else:
                        sc_last_stage_clear = sram_bytes[
                            (STAGECLEARLASTSTAGE_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if sc_last_stage_clear is None or sc_last_stage_clear == 0:
                            goals_met = False
                puzzle_goaled = True
                extra_goaled = True
                if (self.all_goals[1] & 1) != 0:
                    pz_6_10_clear = sram_bytes[PUZZLEL6_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if pz_6_10_clear is None or pz_6_10_clear == 0:
                        puzzle_goaled = False
                    else:
                        pz_6_10_clear = sram_bytes[
                            (PUZZLEL6_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if pz_6_10_clear is None or pz_6_10_clear == 0:
                            puzzle_goaled = False
                if (self.all_goals[1] & 2) != 0:
                    pz_s_6_10_clear = sram_bytes[EXTRAPUZZLEL6_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if pz_s_6_10_clear is None or pz_s_6_10_clear == 0:
                        extra_goaled = False
                    else:
                        pz_s_6_10_clear = sram_bytes[
                            (EXTRAPUZZLEL6_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if pz_s_6_10_clear is None or pz_s_6_10_clear == 0:
                            extra_goaled = False
                if (self.all_goals[1] & 4) != 0:  # Flag for one goal being enough
                    if not puzzle_goaled and not extra_goaled:
                        goals_met = False
                elif not puzzle_goaled or not extra_goaled:
                    goals_met = False
                if self.all_goals[2] != 0:
                    goal_difficulty = self.all_goals[2] & 3
                    goal_stage = ((self.all_goals[2] >> 2) & 3) + 8
                    goal_stage_clear = sram_bytes[
                        (VSSTAGES_COMPLETED + goal_stage) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if (goal_stage_clear & (8 << goal_difficulty)) == 0:
                        goals_met = False
            if goals_met:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        # Look through location checks
        new_checks = []
        for loc_id in ctx.missing_locations:
            if not loc_id in ctx.locations_checked:
                # Locations that are separated by a multiple of 1 KiB are the same, meaning they give multiple items
                # The game fills up to bit 6 with the value 0x7F
                loc_obtained = sram_bytes[loc_id % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                bitmask = 1 << (loc_id // SRAM_AP_REGION_END)
                if (loc_obtained & bitmask) != 0:
                    location = ctx.location_names.lookup_in_game(loc_id)
                    new_checks.append(loc_id)
                    snes_logger.info(
                        f"New check: {location} ({len(ctx.checked_locations) + len(new_checks)}/{len(ctx.server_locations)})")
        if len(new_checks) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])
            ctx.locations_checked.update(new_checks)
        elif not self.looked_through_locations:
            snes_logger.info(f"No new location checks ({len(ctx.checked_locations)}/{len(ctx.server_locations)})")
        self.looked_through_locations = True

        # Check for new items
        old_item_count = received_item_count
        if received_item_count >= 32768:
            received_item_count = 0
            old_item_count = -1
        action_code = ACTION_CODE_NOOP
        while received_item_count < len(ctx.items_received):
            item = ctx.items_received[received_item_count]
            received_item_count += 1
            progressive_count = 0
            for i in range(received_item_count):
                if ctx.items_received[i].item == item.item:
                    progressive_count += 1
            if item.item < SRAM_AP_REGION_OFFSET:  # Progressive item
                current_count = get_current_progressive_count(item.item, sram_bytes)
                if current_count < progressive_count:
                    logging.info("Received %s #%d from %s (%s) (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        current_count + 1,
                        color(ctx.player_names[item.player], "yellow"),
                        ctx.location_names.lookup_in_slot(item.location, item.player), received_item_count,
                        len(ctx.items_received)))
                    snes_logger.info("Granting %s #%d (%d/%d)" % (
                        ctx.item_names.lookup_in_game(item.item),
                        current_count + 1, received_item_count, len(ctx.items_received)))
                    item_id_range = get_progressive_item_addr_range(item.item)
                    new_item_id = item_id_range[0] + current_count
                    if new_item_id >= item_id_range[1]:
                        snes_logger.warning(
                            f"Too many copies of {ctx.item_names.lookup_in_game(item.item)} to fit into SRAM, maximum of {item_id_range[1] - item_id_range[0]}")
                    else:
                        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", new_item_id))
                        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG, pack("H", 1))
                        action_code = ACTION_CODE_RECEIVED_ITEM
                        break
                else:
                    logging.info("Already have %d copies of %s (%d/%d in list)" % (
                        current_count,
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        received_item_count,
                        len(ctx.items_received)))
            else:  # Unique item
                already_obtained = sram_bytes[item.item % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                if already_obtained < progressive_count:
                    logging.info("Received %s from %s (%s) (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        color(ctx.player_names[item.player], "yellow"),
                        ctx.location_names.lookup_in_slot(item.location, item.player), received_item_count,
                        len(ctx.items_received)))
                    snes_logger.info("Granting %s (%d/%d)" % (
                        ctx.item_names.lookup_in_game(item.item),
                        received_item_count, len(ctx.items_received)))
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", item.item))
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG, pack("H", progressive_count))
                    action_code = ACTION_CODE_RECEIVED_ITEM
                    if item.item == 0x10E or item.item == 0x111:
                        pass
                    elif 0x100 <= item.item <= 0x125:
                        action_code = ACTION_CODE_RECEIVED_SCORE
                    break
                else:
                    logging.info("Already have %s (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"), received_item_count,
                        len(ctx.items_received)))
        if received_item_count > old_item_count:
            snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ACTION, pack("H", action_code))
            snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_NUMBER, pack("H", received_item_count))
        else:  # Check for collected locations
            collected_loc = 0
            collection_bitmask = 0
            for loc_id in ctx.checked_locations:
                # The multiple of 0x400 determines the bit to look at; if enough bits are set this way,
                #   the game will stop displaying the AP sprite even if not completed locally
                loc_obtained = sram_bytes[loc_id % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                bitmask = 1 << (loc_id // SRAM_AP_REGION_END)
                if (loc_obtained & bitmask) == 0:
                    location = ctx.location_names.lookup_in_game(loc_id)
                    snes_logger.info(f"Marking as collected ingame: {location}")
                    collected_loc = loc_id % SRAM_AP_REGION_END
                    collection_bitmask = bitmask
                    break
            if collected_loc != 0:
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", collected_loc))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG, pack("H", collection_bitmask))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ACTION,
                                    pack("H", ACTION_CODE_MARK_COMPLETE))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVE_CHECK, pack("H", 0xFFFF))

        await snes_flush_writes(ctx)


def get_current_progressive_count(item_id: int, sram_bytes: bytes) -> int:
    item_id_range = get_progressive_item_addr_range(item_id)
    if item_id_range[1] <= item_id_range[0] + 1:
        return sram_bytes[item_id_range[0] - SRAM_AP_REGION_OFFSET]
    current_count = 0
    for i in range(item_id_range[0], item_id_range[1]):
        if sram_bytes[i - SRAM_AP_REGION_OFFSET] > 0:
            current_count += 1
    return current_count


def get_progressive_item_addr_range(item_id) -> (int, int):
    """Returns the address range of the provided item ID, exclusive end"""
    item = progressive_items[item_id]
    return item.starting_id, item.starting_id + item.amount


def get_deathlink_message(player_name: str, deathlink_code: int) -> str:
    match deathlink_code:
        case 1:
            return f"{player_name} topped out"
        case 2:
            return f"{player_name} couldn't keep things simple"
        case 3:
            return f"{player_name} couldn't do Chains and Combos"
        case 4:
            return f"{player_name} ran out of moves"
        case 5:
            return f"{player_name} let the puzzle rise too high"
        case 16:
            return f"{player_name} lost to Lakitu"
        case 17:
            return f"{player_name} lost to Bumpty"
        case 18:
            return f"{player_name} lost to Poochy"
        case 19:
            return f"{player_name} lost to Flying Wiggler"
        case 20:
            return f"{player_name} lost to Froggy"
        case 21:
            return f"{player_name} lost to Gargantua Blargg"
        case 22:
            return f"{player_name} lost to Lunge Fish"
        case 23:
            return f"{player_name} lost to Raphael the Raven"
        case 24:
            return f"{player_name} lost to Hookbill the Koopa"
        case 25:
            return f"{player_name} lost to Naval Piranha"
        case 26:
            return f"{player_name} lost to Kamek"
        case 27:
            return f"{player_name} lost to Bowser"
        case 32:
            return f"{player_name} topped out simultaneously with Lakitu"
        case 33:
            return f"{player_name} topped out simultaneously with Bumpty"
        case 34:
            return f"{player_name} topped out simultaneously with Poochy"
        case 35:
            return f"{player_name} topped out simultaneously with Flying Wiggler"
        case 36:
            return f"{player_name} topped out simultaneously with Froggy"
        case 37:
            return f"{player_name} topped out simultaneously with Gargantua Blargg"
        case 38:
            return f"{player_name} topped out simultaneously with Lunge Fish"
        case 39:
            return f"{player_name} topped out simultaneously with Raphael the Raven"
        case 40:
            return f"{player_name} topped out simultaneously with Hookbill the Koopa"
        case 41:
            return f"{player_name} topped out simultaneously with Naval Piranha"
        case 42:
            return f"{player_name} topped out simultaneously with Kamek"
        case 43:
            return f"{player_name} topped out simultaneously with Bowser"
        case _:
            return f"{player_name} died somehow ({deathlink_code})"
