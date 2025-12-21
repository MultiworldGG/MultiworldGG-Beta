import asyncio

from Connector.Packets import PacketHeader, PacketType, Packet, ConnectionType
from Connector.Data import  shop_items, inverse_shop_items, get_item_type, inverse_moon_items
from Connector.Player import SMOPlayer

async def run_client():
    try:
        reader, writer = await (asyncio.open_connection("127.0.0.1",1027))
        player = SMOPlayer()
        init_packet = Packet(guid="test".encode("UTF8"), packet_type=PacketType.Connect)
        writer.write(init_packet.serialize())
        await writer.drain()
        while True:
            data: bytearray = bytearray(await reader.read(PacketHeader.SIZE))
            packet = Packet(header_bytes=data)
            packet_size: int = packet.header.packet_size.value
            data = bytearray(await reader.read(packet_size))
            packet.deserialize(data)
            match packet.header.packet_type:
                case PacketType.Item:
                    print(f"Item Packet {packet.packet.name} of type {packet.packet.item_type.value}.")
            collect = input("Enter Moon or Item Name/ID: ")
            if collect in inverse_shop_items or collect in shop_items:
                if collect.isnumeric():
                    collect = int(collect)
                    name = inverse_shop_items[collect].removesuffix("Cap").removesuffix("Clothes")
                    packet = Packet(guid="test".encode("utf8"), packet_type=PacketType.Item, packet_data=[name, get_item_type(collect)])
                    writer.write(packet.serialize())
                    await writer.drain()
                else:
                    name : str = collect
                    name = name.removesuffix("Cap").removesuffix("Clothes")
                    packet = Packet(guid="test".encode("utf8"), packet_type=PacketType.Item, packet_data=[name, get_item_type(inverse_shop_items[collect])])
                    writer.write(packet.serialize())
                    await writer.drain()
            if collect in inverse_moon_items or collect in inverse_moon_items.values() or collect.isnumeric():
                if collect.isnumeric():
                    collect = int(collect)
                    moon = player.get_next_moon(collect)
                    print(moon)
                    packet = Packet(guid="test".encode("utf8"), packet_type=PacketType.Shine, packet_data=[moon])
                    writer.write(packet.serialize())
                    await writer.drain()
                else:
                    for key in inverse_moon_items.keys():
                        if inverse_moon_items[key] == collect:
                            collect = key
                            break
                    moon = player.get_next_moon(collect)
                    print(moon)
                    packet = Packet(guid="test".encode("utf8"), packet_type=PacketType.Shine, packet_data=[moon])
                    writer.write(packet.serialize())
                    await writer.drain()

    except Exception as e:
        print("Failed to connect ", e)


asyncio.run(run_client())
print("dead")