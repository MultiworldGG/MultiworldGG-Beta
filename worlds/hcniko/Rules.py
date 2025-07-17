from BaseClasses import CollectionState

TICKETS = ["Hairball City Ticket", "Turbine Town Ticket", "Salmon Creek Forest Ticket", "Public Pool Ticket",
           "Bathhouse Ticket", "Tadpole HQ Ticket", "Gary's Garden Ticket"]


def has_all_coins(state: CollectionState, player):
    return state.has("Coin", player, 76)


def can_talk_to_peper(state: CollectionState, player, count: int):
    return state.has("Coin", player, count)


def has_enough_cassettes(state: CollectionState, player, count: int):
    return state.has("Cassette", player, count * 5)


def has_all_tickets(state: CollectionState, player):
    return (state.has("Hairball City Ticket", player)
            and state.has("Turbine Town Ticket", player)
            and state.has("Salmon Creek Forest Ticket", player)
            and state.has("Public Pool Ticket", player)
            and state.has("Bathhouse Ticket", player)
            and state.has("Tadpole HQ Ticket", player))


def has_tickets(state: CollectionState, player, required_tickets):
    ticket_count = sum(1 for ticket in TICKETS if state.has(ticket, player))
    return ticket_count >= required_tickets


def has_access_garden(state: CollectionState, player, world):
    access_option = world.options.access_garys_garden.value
    if access_option == 1:
        return (state.has("Gary's Garden Ticket", player)
                and state.has("Tadpole HQ Ticket", player)
                and (world.options.textbox.value != 1 or state.has("Textbox", player))
                and (world.options.swimming.value != 1 or state.has("Swim Course", player)))
    elif access_option == 2:
        return (state.has("Gary's Garden Ticket", player)
                and (world.options.textbox.value != 1 or state.has("Textbox", player)))
    else:
        return (state.has("Tadpole HQ Ticket", player)
                and (world.options.textbox.value != 1 or state.has("Textbox", player))
                and (world.options.swimming.value != 1 or state.has("Swim Course", player)))


def has_party_ticket(state: CollectionState, player, world):
    if world.options.textbox.value == 1 and world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player) and state.has("Textbox", player)
    elif world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player)
    else:
        return state.can_reach_region("Home", player)


def has_access_to(state: CollectionState, player, location):
    return state.can_reach_location(location, player)


def get_region_rules(player, world):
    if world.options.min_elevator_cost.value == world.options.max_elevator_cost.value:
        world.kiosk_cost["Elevator"] = world.options.max_elevator_cost.value
    else:
        world.kiosk_cost["Elevator"] = world.random.randint(world.options.min_elevator_cost.value,
                                                            world.options.max_elevator_cost.value)
    return {
        "Home -> Hairball City":
            lambda state: state.has("Hairball City Ticket", player),
        "Home -> Turbine Town":
            lambda state: state.has("Turbine Town Ticket", player),
        "Home -> Salmon Creek Forest":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Home -> Public Pool":
            lambda state: state.has("Public Pool Ticket", player),
        "Home -> Bathhouse":
            lambda state: state.has("Bathhouse Ticket", player),
        "Home -> Tadpole HQ":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Home -> Gary's Garden":
            lambda state: has_access_garden(state, player, world),
        "Tadpole HQ -> Home Party":
            lambda state: can_talk_to_peper(state, player, world.kiosk_cost["Elevator"]),
        "Home -> ChatHome":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Home -> ChatParty":
            lambda state: has_party_ticket(state, player, world),
        "Home -> Chatsanity":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City -> ChatHC":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town -> ChatTT":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest -> ChatSCF":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool -> ChatPP":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse -> ChatBath":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ -> ChatHQ":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Gary's Garden -> ChatGarden":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City -> BugsHC":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Turbine Town -> BugsTT":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Salmon Creek Forest -> BugsSCF":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool -> BugsPP":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse -> BugsBath":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Tadpole HQ -> BugsHQ":
            lambda state: (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Hairball City -> ApplesHC":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Turbine Town -> ApplesTT":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Salmon Creek Forest -> ApplesSCF":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Public Pool -> ApplesPP":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Bathhouse -> ApplesBath":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Tadpole HQ -> ApplesHQ":
            lambda state: (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
    }


def get_location_rules(player, world):
    lowest_cost: int = world.options.min_kiosk_cost.value
    highest_cost: int = world.options.max_kiosk_cost.value
    cost_increment: int = (highest_cost - lowest_cost) // len(world.kiosk_cost)
    min_difference = 4
    last_cost = 0

    kiosk_names = list(world.kiosk_cost.keys())
    kiosk_names.remove("Elevator")
    if world.options.shuffle_kiosk_reward.value == 1:
        world.random.shuffle(kiosk_names)

    if world.options.shuffle_kiosk_reward.value == 0:
        for i, kiosk_name in enumerate(kiosk_names):
            if i >= 3:
                cost = 1 + 5 + (5 * i)
            else:
                cost = 1 + (5 * i)
            world.kiosk_cost[kiosk_name] = cost
    else:
        for i, kiosk_name in enumerate(kiosk_names):
            min_range: int = lowest_cost + (cost_increment * i)
            if min_range >= highest_cost:
                min_range = highest_cost - 1

            value: int = world.random.randint(min_range,
                                              min(highest_cost, max(lowest_cost, last_cost + cost_increment)))
            cost = world.random.randint(value, min(value + cost_increment, highest_cost))
            if i >= 1:
                if last_cost + min_difference > cost:
                    cost = last_cost + min_difference

            cost = min(cost, highest_cost)
            world.kiosk_cost[kiosk_name] = cost
            last_cost = cost

    if world.options.cassette_logic.value == 2:
        cassette_values = list(range(1, 14 + 1))
        world.random.shuffle(cassette_values)
        cassette_locations = list(world.cassette_cost.keys())
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]
    elif world.options.cassette_logic.value == 0:
        cassette_locations = list(world.cassette_cost.keys())
        for i, location_name in enumerate(cassette_locations):
            if "Mitch" in location_name:
                world.cassette_cost[location_name] = 5
            elif "Mai" in location_name:
                world.cassette_cost[location_name] = 10
    else:
        cassette_values = list(range(1, 14 + 1))
        cassette_locations = list(world.cassette_cost.keys())
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]

    return {
        "Home - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Home"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Hairball City"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Turbine Town"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Salmon Creek Forest"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Public Pool"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Bathhouse"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Achievement - Employee Of The Month!":
            lambda state: has_all_coins(state, player),
        "Achievement - Bottled Up":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and (state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player))
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and state.has("Tadpole HQ Ticket", player)
                          and can_talk_to_peper(state, player, world.kiosk_cost["Elevator"]),
        "Achievement - Hopeless Romantic":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Achievement - Volley Dreams":
            lambda state: has_all_tickets(state, player)
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Achievement - Snail Fashion Show":
            lambda state: has_all_tickets(state, player),
        "Best Employee!":
            lambda state: has_all_coins(state, player),
        "Turbine Town - Dustan on Wind Turbine":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Turbine Town Key", player))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Public Pool Key", player))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Poppy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Tadpole HQ - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Tadpole HQ Key", player))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Above Frog Statue":
            lambda state: state.has("Key", player, 7)
                          or state.has("Hairball City Key", player)
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Salmon Creek Forest - Inside Locked Cave":
            lambda state: state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player),
        "Bathhouse - Mahjong Hideout":
            lambda state: state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2),
        "Salmon Creek Forest - Fish with Fischer":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                           and (world.options.fishsanity.value != 2 or state.has("Salmon Creek Forest Fish", player, 5))
                           and (world.options.textbox.value != 1 or state.has("Textbox", player))
                           and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - SPORTVIVAL":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Nina":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Moomy":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.seedsanity.value != 2 or state.has("Hairball City Seed", player, 10))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Game Kid":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Blippy Dog":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.bonesanity.value != 2 or state.has("Hairball City Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Hairball City - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Blippy Dog":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.bonesanity.value != 2 or state.has("Turbine Town Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)
                          and (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Turbine Town - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Game Kid":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - SPORTVIVAL VOLLEY":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Blessley":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool - Little Gabi's Flowers":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.flowersanity.value != 2 or state.has("Public Pool Flower", player, 3))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Fish with Fischer":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                           and (world.options.fishsanity.value != 2 or state.has("Bathhouse Fish", player, 5))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Blessley":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse - Little Gabi's Flowers":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.flowersanity.value != 2 or state.has("Bathhouse Flower", player, 3))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Blippy Dog":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.bonesanity.value != 2 or state.has("Bathhouse Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2)) and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Dustan - Meeting First Time":
            lambda state: (has_access_to(state, player, "Hairball City - Dustan on Lighthouse")
                           or has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine")
                           or has_access_to(state, player, "Salmon Creek Forest - Dustan on Mountain")
                           or has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        # Cassette
        "Hairball City - Mitch":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mitch"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mitch"])))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Mai":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mai"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mai"])))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Mitch":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mitch"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mitch"])))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Mai":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mai"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mai"])))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Mai":
            lambda state: ((has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mai"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mai"]))
                          and (state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player))
                          and (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mitch"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mitch"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - Mitch":
            lambda state: ((state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mitch"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mitch"])))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mai"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mai"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mitch"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mitch"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mai"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mai"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mai"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mai"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mitch"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mitch"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Gary's Garden - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mai"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mai"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Gary's Garden - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mitch"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mitch"]))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        # Fish
        "Salmon Creek Forest - Bass":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Catfish":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Pike":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Salmon":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Trout":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Anglerfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Clione":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Little Wiggly Guy":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Jellyfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Pufferfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Fish with Fischer":
            lambda state: (world.options.fishsanity.value != 2 or state.has("Hairball City Fish", player, 5))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Fish with Fischer":
            lambda state: (world.options.fishsanity.value != 2 or state.has("Turbine Town Fish", player, 5))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Fish with Fischer":
            lambda state: (world.options.fishsanity.value != 2 or state.has("Public Pool Fish", player, 5))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Fish with Fischer":
            lambda state: (world.options.fishsanity.value != 2 or state.has("Tadpole HQ Fish", player, 5))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        # Snail Shop
        "Snail Shop - Bowtie":
            lambda state: has_tickets(state, player, 4),  # 10000$
        "Snail Shop - Motorcycle":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Sunglasses":
            lambda state: has_tickets(state, player, 3),  # 2000$
        "Snail Shop - Mahjong":
            lambda state: has_tickets(state, player, 1),  # 100$
        "Snail Shop - Cap":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - King Staff":
            lambda state: has_tickets(state, player, 4),  # 10000$
        "Snail Shop - Mouse":
            lambda state: has_tickets(state, player, 3),  # 1000$
        "Snail Shop - Clown Face":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Cat":
            lambda state: has_tickets(state, player, 3),  # 1000$
        "Snail Shop - Bandanna":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Stars":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Sword":
            lambda state: has_tickets(state, player, 3),  # 3000$
        "Snail Shop - Top hat":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Glasses":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Flower":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Small Hat":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Tadpole HQ - Ledge Above Elevator":
            lambda state: can_talk_to_peper(state, player, world.kiosk_cost["Elevator"]),
        # Seedsanity
        "Hairball City - Seed 1":
            lambda state: state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 2":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 3":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 4":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 5":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 6":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 7":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 8":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 9":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed 10":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Salmon Creek Forest - Moomy":
            lambda state: (world.options.seedsanity.value != 2 or state.has("Salmon Creek Forest Seed", player, 10))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Moomy":
            lambda state: (world.options.seedsanity.value != 2 or state.has("Bathhouse Seed", player, 10))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        # Flowersanity
        "Public Pool - Flowerbed 1":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Public Pool - Flowerbed 2":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Public Pool - Flowerbed 3":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed 1":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed 2":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed 3":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Hairball City - Little Gabi's Flowers":
            lambda state: (world.options.flowersanity.value != 2 or state.has("Hairball City Flower", player, 3))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Little Gabi's Flowers":
            lambda state: (world.options.flowersanity.value != 2 or state.has("Turbine Town Flower", player, 3))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Little Gabi's Flowers":
            lambda state: (world.options.flowersanity.value != 2 or state.has("Salmon Creek Forest Flower", player, 6))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ - Little Gabi's Flowers":
            lambda state: (world.options.flowersanity.value != 2 or state.has("Tadpole HQ Flower", player, 4))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        # Progressive Cassette Logic
        "Mitch/Mai - 1":
            lambda state: (has_enough_cassettes(state, player, 1)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 2":
            lambda state: (has_enough_cassettes(state, player, 2) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 3":
            lambda state: (has_enough_cassettes(state, player, 3) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 4":
            lambda state: (has_enough_cassettes(state, player, 4) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 5":
            lambda state: (has_enough_cassettes(state, player, 5) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 6":
            lambda state: (has_enough_cassettes(state, player, 6) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 7":
            lambda state: (has_enough_cassettes(state, player, 7) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 8":
            lambda state: (has_enough_cassettes(state, player, 8) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 9":
            lambda state: (has_enough_cassettes(state, player, 9) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 10":
            lambda state: (has_enough_cassettes(state, player, 10) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 11":
            lambda state: (has_enough_cassettes(state, player, 11) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 12":
            lambda state: (has_enough_cassettes(state, player, 12) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 13":
            lambda state: (has_enough_cassettes(state, player, 13) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 14":
            lambda state: (has_enough_cassettes(state, player, 14) and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player)))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player))
                          or (state.has("Tadpole HQ Ticket", player))
                          or (state.has("Gary's Garden Ticket", player))))
                          and (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Apple On Frog Statue Island Pier 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug 53":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug 56":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug 38":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug 29":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug 51":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Salmon Creek Forest - Blippy Dog":
            lambda state: (world.options.bonesanity.value != 2 or state.has("Salmon Creek Forest Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Blippy Dog":
            lambda state: (world.options.bonesanity.value != 2 or state.has("Public Pool Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blippy Dog":
            lambda state: (world.options.bonesanity.value != 2 or state.has("Tadpole HQ Bone", player, 5))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blessley":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Hairball City - Blessley":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Turbine Town - Blessley":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Salmon Creek Forest - Blessley":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Turbine Town - Shipping Container With Breakable Boxes":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Bathhouse - Breakable Box Inside Bathhouse Box":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Hairball City - Breakable Boxes Near Frog Of Destruction":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Salmon Creek Forest - Inside Boxes (Waterfall Cave)":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Breakable Boxes Near Frogtective":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Above Small Island":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                          and (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Tadpole HQ - Breakable Boxes near Blessley":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),

        "Hairball City - Big Umbrella":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Stone Pillar Behind Wind Turbine":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 4":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 5":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 6":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Public Pool - Far Away Island":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Far Away Island Left Side":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Public Pool - Far Away Island Right Side":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Niko & 2D (Thought)":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Public Pool - Apple On Far Away Island 1":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 2":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 3":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 4":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 5":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 6":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 7":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 8":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 9":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 10":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 11":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 12":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 13":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 14":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 15":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 16":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 17":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 18":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 19":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 20":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 21":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 22":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 23":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 24":
            lambda state: (world.options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),

        "Turbine Town - Near Fishing Containers":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Niko is a ninja (Thought)":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Fan to Fan":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 8":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 1":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 7":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 6":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 5":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 4":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 3":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 2":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed 7":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed 8":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed 10":
            lambda state: (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),

        "Achievement - Lost at Sea":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Home - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Frog Statue Crown":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Moorish Idol":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Not Nemo":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Eel":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Flying Fish":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Orange Fish":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Hairball City - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Niko admires a Frog Statue (Thought)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Nervous Frog (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Turbine Town - Albino Corydoras":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Axolotl":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Prianha":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Mantaray":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Sand Shrimp":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Salmon Creek Forest - Beneath Pond":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Woodisch (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Divin' Doe (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Niko & a rock (Thought)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug 79":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug 65":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug 12":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug 16":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug 62":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Public Pool - Inside BIG Pool":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Inside Pool":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Shark":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Squid":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Turtle":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Gramma Loreto":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Baby Crocodile":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Bathhouse - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),

        "Tadpole HQ - Bone 1":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone 2":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone 3":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone 4":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Tadpole HQ - Bone 5":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blue Fairy Shrimp":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bluestreak Cleaner Wrasse":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Honey Gourami":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Loach":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Neon Tetra":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Hasselhop (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blippy (Chatsanity)":
            lambda state: state.has("Tadpole HQ Key", player),

        "Home - Give High Frog Lunchbox":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - BIG VOLLEY":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Dustan on Lighthouse":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Hairball City - Gunter on Skyscraper":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Hairball City - Handsome Frog":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),

        "Turbine Town - AIR VOLLEY":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Handsome Frog":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Turbine Town - Pelly the Engineer":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),

        "Salmon Creek Forest - Dustan on Mountain":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Handsome Frog":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Nina":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Stijn & Melissa":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Salmon Creek Forest - Treeman":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),

        "Public Pool - Frogtective":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Public Pool - Handsome Frog":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),

        "Bathhouse - Dustan on Bathhouse":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Game Kid":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Handsome Frog":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - LONG VOLLEY":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Nina":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Bathhouse - Serschel & Louist":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),

        "Tadpole HQ - Dojo Guy":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player))
                          and (world.options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Tadpole HQ - Serschel & Louist":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ - Frog King":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),
        "Tadpole HQ - HUGE VOLLEY":
            lambda state: (world.options.textbox.value != 1 or state.has("Textbox", player)),

        "Hairball City - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Game Kid (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Louist (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Serschel & Louist"),
        "Hairball City - Serschel (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Serschel & Louist"),
        "Hairball City - Nina (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Melissa (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Moomy (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Dustan (Chatsanity)":
            lambda state: (world.options.parasols.value != 1 or state.has("Parasol Repair", player)),

        "Turbine Town - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Turbine Town - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Serschel (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Serschel & Louist"),
        "Turbine Town - Louist (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Serschel & Louist"),
        "Turbine Town - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine"),
        "Turbine Town - Melissa & Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa"),

        "Salmon Creek Forest - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Fischer (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Salmon Creek Forest - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (state.has("Key", player, 7)
                           or state.has("Salmon Creek Forest Key", player)),
        "Salmon Creek Forest - Serschel (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Louist (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Trixie (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Game Kid (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Clint (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Clover (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Coco (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Culley (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - David D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Flippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Jippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Marry D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Mippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Paul (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Poppy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Tippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Skippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Pine Frog (Chatsanity)":
            lambda state: (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),

        "Public Pool - Blessley (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Public Pool Key", player)),
        "Public Pool - Little Gabi (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Trixie (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Vlog Frog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Poppy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Paul (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Flippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Jippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Mippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Skippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Tippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),

        "Bathhouse - Blessley (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Vlog Frog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Fischer (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Little Gabi (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Gashadokuro (Chatsanity)":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Mahjong Frogs (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Penny (Chatsanity)":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Poppy (Chatsanity)":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Clint (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Coco (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Culley (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Clover (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Marry D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - David D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"),

        # Chatsanity Global
        "Chatsanity - (Ex) Employee of the month":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - AC Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Accountant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Alice":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Assistant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Baby Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Baby Gull (TT)":
            lambda state: state.has("Public Pool Ticket", player)
                          or state.has("Turbine Town Ticket", player),
        "Chatsanity - Big Bro Stag":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Biki":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Bird":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Blessley":
            lambda state: state.has("Party Invitation", player)
                          or state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player)
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Blippy":
            lambda state: state.has("Party Invitation", player)
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Tadpole HQ Ticket", player)
                              and (state.has("Key", player,7)
                                   or state.has("Tadpole HQ Key", player))),
        "Chatsanity - Blippy Dog":
            lambda state: state.has("Party Invitation", player)
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or state.has("Salmon Creek Forest Ticket", player)
                          or state.has("Public Pool Ticket", player)
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Bobby":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Borbie":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Britney":
            lambda state: state.has("Hairball City Ticket", player)
                          or (state.has("Turbine Town Ticket", player)
                              and (world.options.swimming.value != 1
                              or world.options.precisejumps.value == 1
                              or state.has("Swim Course", player)))
                          or state.has("Public Pool Ticket", player),
        "Chatsanity - Brooklyn Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Button Bird":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Carl":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Carrot":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Clint":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Clover":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Coco":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Code Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Coffee Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Conspiracy Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Culley":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Culture Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Dance Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Danger Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - David D. Carota":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Dirk":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Divin' Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Doe of Darkness":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Dream Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Dustan":
            lambda state: state.has("Party Invitation", player)
                          or has_access_to(state, player, "Dustan - Meeting First Time"),
        "Chatsanity - Elizabeth IV":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Fear Deer":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Fear Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Fischer":
            lambda state: state.has("Party Invitation", player)
                          or state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or state.has("Public Pool Ticket", player)
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Fix Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Fizzy the Frog":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Flippy":
            lambda state: (state.has("Public Pool Ticket", player)
                           or state.has("Salmon Creek Forest Ticket", player))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Flower Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Flowery Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Friendly Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Frog (Frogbucks)":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Frog King":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Frog of Destruction":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Frogtective":
            lambda state: state.has("Public Pool Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Frogucus the Green":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Fry Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Fry loving Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Game Kid":
            lambda state: (state.has("Hairball City Ticket", player)
                           and (state.has("Contact List 2", player)
                                or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Gamedev Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Gary":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Gashadokuro":
            lambda state: state.has("Bathhouse Ticket", player)
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Chatsanity - Gull Friend":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Gull Friend 2":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Gunter":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Party Invitation", player)
                          or has_access_garden(state, player, world),
        "Chatsanity - HUD Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Handsome Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player)
                          or state.has("Public Pool Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player)
                          or has_access_garden(state, player, world),
        "Chatsanity - Hasselhop":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Chatsanity - Hat Kid":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Hungry Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Impatient Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Jess":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Jiji":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Jippy":
            lambda state: (state.has("Public Pool Ticket", player)
                           or state.has("Salmon Creek Forest Ticket", player))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Knowledgeable Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Lil' Sis Doe":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Little Gabi":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player)
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Lock Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Loud Stag":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Louist":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Maggie":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Mahjong Frog":
            lambda state: (state.has("Bathhouse Ticket", player)
                           and (state.has("Key", player, 7)
                                or state.has("Bathhouse Key", player, 2)))
                          or state.has("Party Invitation", player),
        "Chatsanity - Mai":
            lambda state: state.has("Party Invitation", player)
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and state.has("Key", player, 7)
                                   or state.has("Salmon Creek Forest Key", player))
                          or state.has("Public Pool Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Marry D. Carota":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Master":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Melissa":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or state.has("Bathhouse Ticket", player)
                          or has_access_to(state, player, "Hairball City - Nina")
                          or state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Mickey":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Miki":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Minoes":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Mippy":
            lambda state: (state.has("Public Pool Ticket", player)
                           or state.has("Salmon Creek Forest Ticket", player))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Mitch":
            lambda state: state.has("Party Invitation", player)
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or state.has("Salmon Creek Forest Ticket", player)
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Moe":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Mom Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Mom Gull (TT)":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Monty":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Moomy":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or state.has("Salmon Creek Forest Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Mysterious Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Mythology Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Nervous Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Chatsanity - Niko a0.45":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Nina":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or state.has("Salmon Creek Forest Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Noah":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Paul":
            lambda state: state.has("Bathhouse Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Pelly the Engineer":
            lambda state: state.has("Turbine Town Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Penny":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Pine Frog":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and (world.options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Chatsanity - Poppy":
            lambda state: state.has("Party Invitation", player)
                          or has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - R&D Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - R&D Frog 2":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - R&D Frog 3":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Ricky":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Robo Fr0g":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Salty Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Scare Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Serschel":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Shovelin' Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Simon":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Skippy":
            lambda state: (state.has("Salmon Creek Forest Ticket", player)
                           or state.has("Public Pool Ticket", player))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Slack Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Small Talk Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Snip Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Snow Frog Frog":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Steamy Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Steamy Frog":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Stijn":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or state.has("Bathhouse Ticket", player)
                          or has_access_to(state, player, "Hairball City - Nina")
                          or state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Stijn's Dad":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Stijn's Mom":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Superstitious Gull":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Sushi Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Swimming Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Tax Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Tip Frog":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Tippy":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Tough Frog":
            lambda state: state.has("Hairball City Ticket", player),
        "Chatsanity - Tourist Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Train Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player)
                          or state.has("Public Pool Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Travis":
            lambda state: state.has("Hairball City Ticket", player)
                          or state.has("Bathhouse Ticket", player)
                          or state.has("Tadpole HQ Ticket", player)
                          or state.has("Party Invitation", player),
        "Chatsanity - Treeman":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Turbine Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Chatsanity - Trixie":
            lambda state: state.has("Party Invitation", player)
                          or state.has("Turbine Town Ticket", player)
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1)))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))),
        "Chatsanity - VR Frog":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Vlog Frog":
            lambda state: state.has("Party Invitation", player)
                          or state.has("Hairball City Ticket", player)
                          or state.has("Turbine Town Ticket", player)
                          or state.has("Salmon Creek Forest Ticket", player)
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2)))
                          or state.has("Tadpole HQ Ticket", player),
        "Chatsanity - Vacation Frog":
            lambda state: state.has("Public Pool Ticket", player),
        "Chatsanity - Wess":
            lambda state: state.has("Bathhouse Ticket", player),
        "Chatsanity - Wind Dragon":
            lambda state: state.has("Turbine Town Ticket", player),
        "Chatsanity - Woodisch":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and (world.options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Niko & 2D(Thought)":
            lambda state: has_access_to(state, player, "Public Pool - Far Away Island Right Side"),
        "Turbine Town - Inside Partially Sunken Shipping Container":
            lambda state: (world.options.swimming.value != 1 or state.has("Swim Course", player))
                          or world.options.precisejumps.value == 1,
        "Turbine Town - Above Partially Sunken Shipping Container":
            lambda state: (world.options.swimming.value != 1
                          or world.options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Turbine Town - Bug 48":
            lambda state: (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug 10":
            lambda state: (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug 2":
            lambda state: (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug 32":
            lambda state: (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug 52":
            lambda state: (world.options.swimming.value != 1
                           or world.options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Tadpole HQ - Borbie (Chatsanity)":
            lambda state: can_talk_to_peper(state, player, world.kiosk_cost["Elevator"]),
        "Tadpole HQ - Pepper (Chatsanity)":
            lambda state: can_talk_to_peper(state, player, world.kiosk_cost["Elevator"]),
    }
