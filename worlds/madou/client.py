import logging
import struct
import typing
import random
from typing import TYPE_CHECKING

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

from .data.item_data import hex_data_by_item
from .data.location_data import hex_by_location

if TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

MADOU_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

MADOU_INVENTORY = 0x001309
MADOU_INVENTORY_LENGTH = 0x2A
MADOU_INVENTORY_COUNT = 0x001333
MADOU_SAVE = 0x001300
MADOU_SAVE_LENGTH = 0x7F
MADOU_BESTIARY = 0x0014A8
MADOU_BESTIARY_LENGTH = 0x25
MADOU_HEALTH = 0x001346
MADOU_TOOLS = 0x0013C8
MADOU_LENGTH = 0x06
MADOU_TOOL_COUNT = 0x0013DA
MADOU_AP_SAVEINFO = 0x001390
MADOU_AP_SAVEINFO_LENGTH = 0x0A

MADOU_FREEZE = 0x001401
MADOU_MENU = 0x00172B

MADOU_RANDO_INFO = 0x0070c0


class MadouSNIClient(SNIClient):
    game = "Madou Monogatari Hanamaru Daiyouchienji"
    patch_suffix = ".apmmhd"
    item_queue: typing.List[int] = []
    client_random: random.Random = random.Random()

    async def add_item_to_inventory(self, ctx: "SNIContext", has_full_inventory: bool) -> None:
        from SNIClient import snes_buffered_write, snes_read, snes_logger
        if len(self.item_queue) > 0:
            item = self.item_queue.pop()
            if has_full_inventory:
                # can't handle this item right now, send it to the back and return to handle the rest
                self.item_queue.append(item)
                return
            inventory_list = bytearray(await snes_read(ctx, WRAM_START + MADOU_INVENTORY, MADOU_INVENTORY_LENGTH))
            for i in range(len(inventory_list)):
                if inventory_list[i] == 0x00:
                    inventory_list[i] = hex_data_by_item[item][1][0].value
                    snes_buffered_write(ctx, WRAM_START + MADOU_INVENTORY, inventory_list)
                    inventory_count = await snes_read(ctx, WRAM_START + MADOU_INVENTORY_COUNT, 0x01)
                    new_count = (inventory_count[0] + 1).to_bytes(1, "little")
                    snes_buffered_write(ctx, WRAM_START + MADOU_INVENTORY_COUNT, new_count)
                    # Some items actually are flag oriented, not inventory oriented, so the flag needs to exist anyway.
                    if len(hex_data_by_item[item][1]) > 1:
                        additional_info = hex_data_by_item[item][1][1]
                        current_state = await snes_read(ctx, WRAM_START + MADOU_SAVE + additional_info.hex_address, 0x01)
                        new_state = (current_state[0] | additional_info.value).to_bytes(1, "little")
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + additional_info.hex_address, new_state)
                    elif item == 39:  # Firefly Egg
                        first_case = await snes_read(ctx, WRAM_START + MADOU_SAVE + 0x93, 0x01)
                        if first_case[0] & 0x40 == 0:
                            new_case = (first_case[0] | 0x40).to_bytes(1, "little")
                            snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0x93, new_case)
                        else:
                            second_case = await snes_read(ctx, WRAM_START + MADOU_SAVE + 0x84, 0x01)
                            if second_case[0] & 0x40 == 0:
                                new_case = (second_case[0] | 0x40).to_bytes(1, "little")
                                snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0x84, new_case)
                    break
            else:
                self.item_queue.append(item)  # no more slots, get it next go around

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        rom = await snes_read(ctx, MADOU_ROMHASH_START, 0x15)
        if rom is None or rom == bytes([0] * 0x15) or rom[:5] != b"Madou":
            return False
        ctx.game = self.game
        ctx.rom = rom
        ctx.items_handling = 0b111  # default local items with remote start inventory
        ctx.allow_collect = False
        return True

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return
        # We need a read to check whether the game is "in-game", and if the game is paused or in a cutscene or a fight.
        pause_state = await snes_read(ctx, WRAM_START + MADOU_FREEZE, 0x01)
        menu_state = await snes_read(ctx, WRAM_START + MADOU_MENU, 0x01)
        intro = await snes_read(ctx, WRAM_START + 0x1379, 0x01)
        # For now, check for whether the player is in-game if the player's health is 0.
        main_menu_state = await snes_read(ctx, WRAM_START + MADOU_HEALTH, 0x01)
        # We need to find a place in the ROM to store the goal of the game, then do a read on it.
        goal_address = await snes_read(ctx, MADOU_RANDO_INFO, 0x01)
        goal_flag = await snes_read(ctx, MADOU_RANDO_INFO + 0x01, 0x01)
        necessary_stones = await snes_read(ctx, MADOU_RANDO_INFO + 0x02, 0x01)
        skip_fairy = await snes_read(ctx, MADOU_RANDO_INFO + 0x04, 0x01)

        is_paused = pause_state[0] > 0x00
        is_menued = menu_state[0] > 0x00
        is_in_game = main_menu_state[0] != 0x00
        intro_over = intro[0] & 0x01 == 0x01
        rom = await snes_read(ctx, MADOU_ROMHASH_START, 0x15)
        if rom != ctx.rom:
            ctx.rom = None
            return
        goal_state = await snes_read(ctx, WRAM_START + MADOU_SAVE + goal_address[0], 0x01)
        is_goaled = goal_state[0] & goal_flag[0] == goal_flag[0]
        if is_goaled and not ctx.finished_game:
            if goal_address[0] != 0xa1 or is_paused:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
        is_not_in_playable_state = is_paused or is_menued or not is_in_game or not intro_over

        if is_not_in_playable_state:
            return
        new_checks = []

        for loc_id, loc_data in hex_by_location.items():
            if loc_id not in ctx.locations_checked:
                if loc_id in range(150, 184, 1):
                    bestiary_info = await snes_read(ctx, WRAM_START + loc_data[0], 0x01)
                    if bestiary_info[0] != 0x0:
                        new_checks.append(loc_id)
                    continue
                # Otherwise, we use the flag method.
                save_data = await snes_read(ctx, WRAM_START + loc_data[0], 0x01)
                masked_data = save_data[0] & loc_data[1]  # The save data uses a flag system, so we need to do an and here to check it
                if masked_data == loc_data[1]:
                    new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            total_locations = len(ctx.missing_locations) + len(ctx.checked_locations)
            snes_logger.info(f"New Check: {location} ({len(ctx.locations_checked)}/{total_locations})")
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, WRAM_START + MADOU_AP_SAVEINFO, 2)
        recv_amount = struct.unpack("H", recv_count)[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            recv_amount += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

            snes_buffered_write(ctx, WRAM_START + MADOU_AP_SAVEINFO, struct.pack("H", recv_amount))
            group = hex_data_by_item[item.item][0]
            if group == "Equipment" or group == "Consumable" or group == "Gem" or group == "Souvenir" or group == "Special Item":
                self.item_queue.append(item.item)
            elif group != "Nothing":
                hex_commands_list = hex_data_by_item[item.item][1]
                for command in hex_commands_list:
                    if group == "Event Item" or group == "Flight Access":
                        value = await snes_read(ctx, WRAM_START + MADOU_SAVE + command.hex_address, 0x01)
                        new_value = (value[0] | command.value).to_bytes(1, "little")
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, new_value)
                    elif group == "Cookies":
                        value = await snes_read(ctx, WRAM_START + MADOU_SAVE + command.hex_address, 0x02)
                        int_value = int.from_bytes(value, "little")
                        new_value = min(0x270F, int_value + 0x01F4).to_bytes(2, "little")
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, new_value)
                    elif group == "Tool":
                        if item.item == 21:
                            snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, command.value.to_bytes(1, "little"))
                        else:
                            if command.hex_address == 0xFF:
                                for i in range(0, 6):
                                    tool_value = await snes_read(ctx, WRAM_START + MADOU_TOOLS + i, 0x01)
                                    if tool_value[0] == 0x00:
                                        snes_buffered_write(ctx, WRAM_START + MADOU_TOOLS + i, command.value.to_bytes(1, "little"))
                                        tool_count = bytearray(await snes_read(ctx, WRAM_START + MADOU_TOOL_COUNT, 0x02))
                                        if tool_count[0] == 0x00 and tool_count[1] > 0x00:
                                            tool_count[1] = min(6, tool_count[1] + 1)
                                        else:
                                            tool_count[0] = min(6, tool_count[1] + 1)
                                        snes_buffered_write(ctx, WRAM_START + MADOU_TOOL_COUNT, tool_count)
                                        break
                                    if tool_value[0] == command.value:
                                        break  # Was already given.
                            else:
                                save_value = await snes_read(ctx, WRAM_START + MADOU_SAVE + command.hex_address, 0x01)
                                new_value = (save_value[0] | command.value).to_bytes(1, "little")
                                snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, new_value)
                    elif group == "Secret Stone":
                        stone_count = await snes_read(ctx, WRAM_START + MADOU_SAVE + 0xe3, 0x01)
                        new_count = min(8, stone_count[0] + 1).to_bytes(1, "little")
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0xe3, new_count)
                        stone_icons = bytearray(await snes_read(ctx, WRAM_START + MADOU_SAVE + 0xe4, 0x08))
                        for i in range(len(stone_icons)):
                            if stone_icons[i] == 0x00:
                                stone_icons[i] = 0x01
                                break
                        snes_buffered_write(ctx,  WRAM_START + MADOU_SAVE + 0xe4, stone_icons)
                        # Set these values accordingly for the Suketoudara or Fairy interaction, since in-game its a simple compare.
                        # Perhaps when we move to remote, this can be put in the ROM instead.
                        if new_count[0] >= 7:
                            snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0x98, bytes([0x07]))
                        if new_count[0] >= necessary_stones[0]:
                            snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0x99, bytes([0x08]))
                            if skip_fairy[0] > 0:
                                fairy_cond = await snes_read(ctx, WRAM_START + MADOU_SAVE + 0x88, 0x01)
                                new_value = (fairy_cond[0] | 0x04).to_bytes(1, "little")
                                snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + 0x88, new_value)
                    elif group == "Spell":
                        spell_count = await snes_read(ctx, WRAM_START + MADOU_SAVE + command.hex_address, 0x01)
                        new_count = (min(command.value, spell_count[0] + 1)).to_bytes(1, "little")
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, new_count)
                    else:
                        value = await snes_read(ctx, WRAM_START + MADOU_SAVE + command.hex_address, 0x01)
                        new_value = value[0] + command.value
                        snes_buffered_write(ctx, WRAM_START + MADOU_SAVE + command.hex_address, struct.pack("H", new_value))
        inventory_count = await snes_read(ctx, WRAM_START + MADOU_INVENTORY_COUNT, 0x01)
        is_inventory_full = inventory_count[0] >= 0x2A
        await self.add_item_to_inventory(ctx, is_inventory_full)
        await snes_flush_writes(ctx)
