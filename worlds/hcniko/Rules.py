from BaseClasses import CollectionState

TICKETS = ["Hairball City Ticket", "Turbine Town Ticket", "Salmon Creek Forest Ticket", "Public Pool Ticket",
           "Bathhouse Ticket", "Tadpole HQ Ticket", "Gary's Garden Ticket"]


def is_employee(state: CollectionState, player):
    return state.has("Coin", player, 76)


def has_enough_coins(state: CollectionState, player, count: int):
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


def has_textbox(state: CollectionState, player, world, level):
    textbox = world.options.textbox.value
    if textbox == 1:
        return state.has("Textbox", player)
    elif textbox == 2:
        if level == "Gary's Garden" and not world.options.shuffle_garys_garden.value:
            return True
        return state.has(f"{level} Textbox", player)
    else:
        return True


def has_contact_list(state: CollectionState, player, count: int):
    return (state.has(f"Contact List {count}", player)
        or state.has("Progressive Contact List", player, count))


def can_swim(state: CollectionState, player, world, is_precise: bool = False):
    return (world.options.swimming.value != 1
            or (world.options.precisejumps.value == 1 and is_precise)
            or state.has("Swim Course", player))


def can_ac(state: CollectionState, player, world):
    return (world.options.ac_repair.value != 1
            or state.has("AC Repair", player))


def can_parasol(state: CollectionState, player, world):
    return (world.options.parasols.value != 1
            or state.has("Parasol Repair", player))


def can_soda(state: CollectionState, player, world):
    return (world.options.soda_cans.value != 1
            or state.has("Soda Repair", player))


def can_bonk(state: CollectionState, player, world):
    return (world.options.bonk_permit.value != 1
            or state.has("Safety Helmet", player))


def can_catch(state: CollectionState, player, world):
    return (world.options.bug_catching.value != 1
            or state.has("Bug Net", player))


def can_collect(state: CollectionState, player, world):
    return (world.options.applebasket.value != 1
            or state.has("Apple Basket", player))


def can_talk_everywhere(state: CollectionState, player, world):
    return ((state.has("Hairball City Ticket", player)
             and has_textbox(state, player, world, "Hairball City"))
            or (state.has("Turbine Town Ticket", player)
                and has_textbox(state, player, world, "Turbine Town"))
            or (state.has("Salmon Creek Forest Ticket", player)
                and has_textbox(state, player, world, "Salmon Creek Forest"))
            or (state.has("Public Pool Ticket", player)
                and has_textbox(state, player, world, "Public Pool"))
            or (state.has("Bathhouse Ticket", player)
                and has_textbox(state, player, world, "Bathhouse"))
            or (state.has("Tadpole HQ Ticket", player)
                and has_textbox(state, player, world, "Tadpole HQ"))
            or has_textbox(state, player, world, "Home"))


def has_access_garden(state: CollectionState, player, world):
    access_option = world.options.access_garys_garden.value
    if access_option == 1:
        return (state.has("Gary's Garden Ticket", player)
                and state.has("Tadpole HQ Ticket", player)
                and (has_textbox(state, player, world, "Tadpole HQ"))
                and can_swim(state, player, world))
    elif access_option == 2:
        return (state.has("Gary's Garden Ticket", player)
                and (has_textbox(state, player, world, "Gary's Garden")))
    else:
        return (state.has("Tadpole HQ Ticket", player)
                and (has_textbox(state, player, world, "Tadpole HQ"))
                and can_swim(state, player, world))


def has_party_ticket(state: CollectionState, player, world):
    if world.options.textbox.value != 0 and world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player) and (state.has("Textbox", player) or state.has("Home Textbox", player))
    elif world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player)
    else:
        return state.can_reach_region("Home", player)


def has_enough_seeds(state: CollectionState, player, world, count: int):
    if world.options.goal_completion.value == 3:
        return state.has("Gary's Garden Seed", player, count)
    else:
        return True


def has_helped_everyone(state: CollectionState, player, world):
    if world.options.goal_completion.value == 4:
        return (state.can_reach_location("Home - Give High Frog Lunchbox", player)
                and state.can_reach_location("Hairball City - BIG VOLLEY", player)
                and state.can_reach_location("Hairball City - Dustan on Lighthouse", player)
                and state.can_reach_location("Hairball City - Gunter on Skyscraper", player)
                and state.can_reach_location("Hairball City - Nina", player)
                and state.can_reach_location("Hairball City - Moomy", player)
                and state.can_reach_location("Hairball City - Fish with Fischer", player)
                and state.can_reach_location("Hairball City - Game Kid", player)
                and state.can_reach_location("Hairball City - Blippy Dog", player)
                and state.can_reach_location("Hairball City - Blippy", player)
                and state.can_reach_location("Hairball City - Serschel & Louist", player)
                and state.can_reach_location("Hairball City - Little Gabi's Flowers", player)
                and state.can_reach_location("Hairball City - Blessley", player)
                and state.can_reach_location("Turbine Town - Blippy Dog", player)
                and state.can_reach_location("Turbine Town - Blippy", player)
                and state.can_reach_location("Turbine Town - Serschel & Louist", player)
                and state.can_reach_location("Turbine Town - Dustan on Wind Turbine", player)
                and state.can_reach_location("Turbine Town - Little Gabi's Flowers", player)
                and state.can_reach_location("Turbine Town - Blessley", player)
                and state.can_reach_location("Turbine Town - AIR VOLLEY", player)
                and state.can_reach_location("Turbine Town - Pelly the Engineer", player)
                and state.can_reach_location("Turbine Town - Fish with Fischer", player)
                and state.can_reach_location("Salmon Creek Forest - Dustan on Mountain", player)
                and state.can_reach_location("Salmon Creek Forest - Nina", player)
                and state.can_reach_location("Salmon Creek Forest - Stijn & Melissa", player)
                and state.can_reach_location("Salmon Creek Forest - Treeman", player)
                and state.can_reach_location("Salmon Creek Forest - Blessley", player)
                and state.can_reach_location("Salmon Creek Forest - Little Gabi's Flowers", player)
                and state.can_reach_location("Salmon Creek Forest - Game Kid", player)
                and state.can_reach_location("Salmon Creek Forest - Blippy", player)
                and state.can_reach_location("Salmon Creek Forest - Serschel & Louist", player)
                and state.can_reach_location("Salmon Creek Forest - Blippy Dog", player)
                and state.can_reach_location("Salmon Creek Forest - Fish with Fischer", player)
                and state.can_reach_location("Salmon Creek Forest - SPORTVIVAL", player)
                and state.can_reach_location("Salmon Creek Forest - Moomy", player)
                and state.can_reach_location("Public Pool - Blippy", player)
                and state.can_reach_location("Public Pool - Frogtective", player)
                and state.can_reach_location("Public Pool - Blippy Dog", player)
                and state.can_reach_location("Public Pool - Little Gabi's Flowers", player)
                and state.can_reach_location("Public Pool - Blessley", player)
                and state.can_reach_location("Public Pool - WATER VOLLEY", player)
                and state.can_reach_location("Public Pool - Fish with Fischer", player)
                and state.can_reach_location("Bathhouse - Poppy", player)
                and state.can_reach_location("Bathhouse - Fish with Fischer", player)
                and state.can_reach_location("Bathhouse - Blessley", player)
                and state.can_reach_location("Bathhouse - Little Gabi's Flowers", player)
                and state.can_reach_location("Bathhouse - Blippy Dog", player)
                and state.can_reach_location("Bathhouse - Blippy", player)
                and state.can_reach_location("Bathhouse - Dustan on Bathhouse", player)
                and state.can_reach_location("Bathhouse - Game Kid", player)
                and state.can_reach_location("Bathhouse - LONG VOLLEY", player)
                and state.can_reach_location("Bathhouse - Nina", player)
                and state.can_reach_location("Bathhouse - Serschel & Louist", player)
                and state.can_reach_location("Bathhouse - Moomy", player)
                and state.can_reach_location("Tadpole HQ - Blippy", player)
                and state.can_reach_location("Tadpole HQ - Little Gabi's Flowers", player)
                and state.can_reach_location("Tadpole HQ - Blippy Dog", player)
                and state.can_reach_location("Tadpole HQ - Blessley", player)
                and state.can_reach_location("Tadpole HQ - Serschel & Louist", player)
                and state.can_reach_location("Tadpole HQ - Frog King", player)
                and state.can_reach_location("Tadpole HQ - HUGE VOLLEY", player)
                and state.can_reach_location("Tadpole HQ - Fish with Fischer", player)
                and state.can_reach_location("Gary's Garden - Gunter & Little Gabi", player)
                and state.can_reach_location("Hairball City - Mitch", player)
                and state.can_reach_location("Hairball City - Mai", player)
                and state.can_reach_location("Turbine Town - Mitch", player)
                and state.can_reach_location("Turbine Town - Mai", player)
                and state.can_reach_location("Salmon Creek Forest - Mai", player)
                and state.can_reach_location("Salmon Creek Forest - Mitch", player)
                and state.can_reach_location("Public Pool - Mitch", player)
                and state.can_reach_location("Public Pool - Mai", player)
                and state.can_reach_location("Bathhouse - Mitch", player)
                and state.can_reach_location("Bathhouse - Mai", player)
                and state.can_reach_location("Tadpole HQ - Mai", player)
                and state.can_reach_location("Tadpole HQ - Mitch", player)
                and state.can_reach_location("Gary's Garden - Mai", player)
                and state.can_reach_location("Gary's Garden - Mitch", player))
    else:
        return True


def has_access_to(state: CollectionState, player, location):
    return state.can_reach_location(location, player)


def get_region_rules(player, world):
    options = world.options
    if options.min_elevator_cost.value == options.max_elevator_cost.value:
        world.kiosk_cost["Elevator"] = options.max_elevator_cost.value
    else:
        world.kiosk_cost["Elevator"] = world.random.randint(options.min_elevator_cost.value,
                                                            options.max_elevator_cost.value)
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
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"])
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Home -> ChatHome":
            lambda state: has_textbox(state, player, world, "Home"),
        "Home -> ChatParty":
            lambda state: has_party_ticket(state, player, world),
        #"Home -> Chatsanity":
        #    lambda state: has_textbox(state, player, world, "Home"),
        "Hairball City -> ChatHC":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Turbine Town -> ChatTT":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest -> ChatSCF":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool -> ChatPP":
            lambda state: has_textbox(state, player, world, "Public Pool"),
        "Bathhouse -> ChatBath":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Tadpole HQ -> ChatHQ":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),
        "Gary's Garden -> ChatGarden":
            lambda state: has_textbox(state, player, world, "Gary's Garden"),
        "Hairball City -> BugsHC":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Turbine Town -> BugsTT":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Salmon Creek Forest -> BugsSCF":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool -> BugsPP":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse -> BugsBath":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Tadpole HQ -> BugsHQ":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Hairball City -> ApplesHC":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Turbine Town -> ApplesTT":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Salmon Creek Forest -> ApplesSCF":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Public Pool -> ApplesPP":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Bathhouse -> ApplesBath":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Tadpole HQ -> ApplesHQ":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
    }

def get_location_rules(player, world):
    options = world.options
    lowest_cost: int = options.min_kiosk_cost.value
    highest_cost: int = options.max_kiosk_cost.value
    cost_increment: int = (highest_cost - lowest_cost) // len(world.kiosk_cost)
    min_difference = 4
    last_cost = 0

    kiosk_names = list(world.kiosk_cost.keys())
    kiosk_names.remove("Elevator")
    if options.shuffle_kiosk_reward.value == 1:
        world.random.shuffle(kiosk_names)

    if options.shuffle_kiosk_reward.value == 0:
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

    # Don't count Gary's Garden locations when they are disabled
    cassette_locations = list(world.cassette_cost.keys())
    if not options.shuffle_garys_garden.value:
        cassette_locations = [
            loc for loc in cassette_locations
            if not loc.startswith("Gary's Garden")
        ]
    cassette_location_count = len(cassette_locations)
    cassette_values = list(range(1, cassette_location_count + 1))
           # mulitiple entries due to Mitch and Mai having different conditions in Salmon Creek Forest and Public pool
    MitchMaiProgressiveList = [lambda state: (state.has("Hairball City Ticket", player)
            and has_contact_list(state, player, 1)
            and has_textbox(state, player, world, "Hairball City")),
        lambda state: (state.has("Hairball City Ticket", player)
            and has_contact_list(state, player, 1)
            and has_textbox(state, player, world, "Hairball City")),
        lambda state: (state.has("Turbine Town Ticket", player)
            and has_contact_list(state, player, 1)
            and has_textbox(state, player, world, "Turbine Town")),
        lambda state: (state.has("Turbine Town Ticket", player)
            and has_contact_list(state, player, 1)
            and has_textbox(state, player, world, "Turbine Town")),
           # Mitch needs only contact list 1
        lambda state: (state.has("Salmon Creek Forest Ticket", player)
            and has_contact_list(state, player, 1)
            and has_textbox(state, player, world, "Salmon Creek Forest")),
           # Mai needs only a key
        lambda state: (state.has("Salmon Creek Forest Ticket", player)
            and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
            and has_textbox(state, player, world, "Salmon Creek Forest")),
            # Mitch needs contact list 2
        lambda state: (state.has("Public Pool Ticket", player)
            and has_contact_list(state, player, 2)
            and has_textbox(state, player, world, "Public Pool")),
           # Mai is always there
        lambda state: (state.has("Public Pool Ticket", player)
            and has_textbox(state, player, world, "Public Pool")),
        lambda state: (state.has("Bathhouse Ticket", player)
            and has_textbox(state, player, world, "Bathhouse")),
        lambda state: (state.has("Bathhouse Ticket", player)
            and has_textbox(state, player, world, "Bathhouse")),
        lambda state: (state.has("Tadpole HQ Ticket", player)
            and has_textbox(state, player, world, "Tadpole HQ")),
        lambda state: (state.has("Tadpole HQ Ticket", player)
            and has_textbox(state, player, world, "Tadpole HQ")),
        lambda state: has_access_garden(state, player, world),
        lambda state: has_access_garden(state, player, world)]

    if options.cassette_logic.value == 2:
        world.random.shuffle(cassette_values)
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]
    elif options.cassette_logic.value == 0:
        cassette_locations = list(world.cassette_cost.keys())
        for i, location_name in enumerate(cassette_locations):
            if "Mitch" in location_name:
                world.cassette_cost[location_name] = 5
            elif "Mai" in location_name:
                world.cassette_cost[location_name] = 10
    else:
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]

    if options.min_custom_goal_cost.value == options.max_custom_goal_cost.value:
        world.custom_goal_required = options.max_custom_goal_cost.value
    else:
        world.custom_goal_required = world.random.randint(options.min_custom_goal_cost.value, options.max_custom_goal_cost.value)

    return {
        # Victory
        "Best Employee!":
            lambda state: is_employee(state, player),
        "Coin Collector!":
            lambda state: has_enough_coins(state, player, world.custom_goal_required),
        "Restored Gary's Garden!":
            lambda state: has_enough_seeds(state, player, world, 10),
        "Helped Everyone!":
            lambda state: has_helped_everyone(state, player, world),

        "Home - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Home"]))
                          and has_textbox(state, player, world, "Home"),
        "Hairball City - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Hairball City"]))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Turbine Town"]))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Salmon Creek Forest"]))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Public Pool"]))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Bathhouse"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Achievement - Employee Of The Month!":
            lambda state: is_employee(state, player),
        "Achievement - Bottled Up":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and (state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player))
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and state.has("Tadpole HQ Ticket", player)
                          and has_enough_coins(state, player, world.kiosk_cost["Elevator"])
                          and can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Achievement - Hopeless Romantic":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Hairball City")
                          and has_textbox(state, player, world, "Turbine Town")
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and has_textbox(state, player, world, "Public Pool")
                          and has_textbox(state, player, world, "Bathhouse"),
        "Achievement - Volley Dreams":
            lambda state: has_all_tickets(state, player)
                          and has_contact_list(state, player, 1)
                          and has_contact_list(state, player, 2)
                          and can_swim(state, player, world, True),
        "Achievement - Snail Fashion Show":
            lambda state: has_all_tickets(state, player),
        "Turbine Town - Dustan on Wind Turbine":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Turbine Town Key", player))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Public Pool - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Public Pool Key", player))
                          and has_textbox(state, player, world, "Public Pool")
                          and can_swim(state, player, world),
        "Bathhouse - Poppy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2))
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world, True),
        "Tadpole HQ - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Tadpole HQ Key", player))
                          and has_textbox(state, player, world, "Tadpole HQ")
                          and can_swim(state, player, world),
        "Hairball City - Above Frog Statue":
            lambda state: state.has("Key", player, 7)
                          or state.has("Hairball City Key", player)
                          and can_swim(state, player, world)
                          and can_soda(state, player, world),
        "Salmon Creek Forest - Inside Locked Cave":
            lambda state: state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player),
        "Bathhouse - Mahjong Hideout":
            lambda state: state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2),
        "Salmon Creek Forest - Fish with Fischer":
            lambda state: has_contact_list(state, player, 1)
                           and (options.fishsanity.value != 2 or state.has("Salmon Creek Forest Fish", player, 5))
                           and has_textbox(state, player, world, "Salmon Creek Forest")
                           and can_swim(state, player, world),
        "Salmon Creek Forest - SPORTVIVAL":
            lambda state: has_contact_list(state, player, 1)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Hairball City - Nina":
            lambda state: has_contact_list(state, player, 1)
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Moomy":
            lambda state: has_contact_list(state, player, 1)
                          and (options.seedsanity.value != 2 or state.has("Hairball City Seed", player, 10))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Game Kid":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Hairball City")
                          and can_swim(state, player, world),
        "Hairball City - Blippy Dog":
            lambda state: has_contact_list(state, player, 1)
                          and (options.bonesanity.value != 2 or state.has("Hairball City Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Hairball City - Blippy":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Serschel & Louist":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Hairball City")
                          and can_soda(state, player, world),
        "Turbine Town - Blippy Dog":
            lambda state: has_contact_list(state, player, 1)
                          and (options.bonesanity.value != 2 or state.has("Turbine Town Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_parasol(state, player, world),
        "Turbine Town - Blippy":
            lambda state: has_contact_list(state, player, 2)
                          and can_ac(state, player, world),
        "Turbine Town - Serschel & Louist":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Turbine Town")
                          and can_ac(state, player, world),
        "Salmon Creek Forest - Game Kid":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Blippy":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Serschel & Louist":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and can_swim(state, player, world),
        "Public Pool - WATER VOLLEY":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Public Pool")
                          and can_swim(state, player, world),
        "Public Pool - Blessley":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool - Little Gabi's Flowers":
            lambda state: has_contact_list(state, player, 2)
                          and (options.flowersanity.value != 2 or state.has("Public Pool Flower", player, 3))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Fish with Fischer":
            lambda state: has_contact_list(state, player, 2)
                           and (options.fishsanity.value != 2 or state.has("Bathhouse Fish", player, 5))
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Bathhouse - Blessley":
            lambda state: has_contact_list(state, player, 2)
                          and has_textbox(state, player, world, "Bathhouse")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse - Little Gabi's Flowers":
            lambda state: has_contact_list(state, player, 2)
                          and (options.flowersanity.value != 2 or state.has("Bathhouse Flower", player, 3))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Blippy Dog":
            lambda state: has_contact_list(state, player, 2)
                          and (options.bonesanity.value != 2 or state.has("Bathhouse Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_parasol(state, player, world),
        "Bathhouse - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2)) and has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Dustan - Meeting First Time":
            lambda state: (has_access_to(state, player, "Hairball City - Dustan on Lighthouse")
                           or has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine")
                           or has_access_to(state, player, "Salmon Creek Forest - Dustan on Mountain")
                           or has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"))
                          and (has_textbox(state, player, world, "Hairball City")
                           or has_textbox(state, player, world, "Turbine Town")
                           or has_textbox(state, player, world, "Salmon Creek Forest")
                           or has_textbox(state, player, world, "Bathhouse")),
        # Cassette
        "Hairball City - Mitch":
            lambda state: (has_contact_list(state, player, 1)
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mitch"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mitch"])))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Mai":
            lambda state: (has_contact_list(state, player, 1)
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mai"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mai"])))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Mitch":
            lambda state: (has_contact_list(state, player, 1)
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mitch"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mitch"])))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Mai":
            lambda state: (has_contact_list(state, player, 1)
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mai"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mai"])))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Mai":
            lambda state: ((has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mai"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mai"]))
                          and (state.has("Key", player, 7)
                               or state.has("Salmon Creek Forest Key", player))
                          and has_contact_list(state, player, 1))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mitch"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mitch"]))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool - Mitch":
            lambda state: (has_contact_list(state, player, 2)
                          and (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mitch"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mitch"])))
                          and has_textbox(state, player, world, "Public Pool"),
        "Public Pool - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mai"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mai"]))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mitch"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mitch"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mai"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mai"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Tadpole HQ - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mai"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mai"]))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Tadpole HQ - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mitch"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mitch"]))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Gary's Garden - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mai"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mai"]))
                          and has_textbox(state, player, world, "Gary's Garden"),
        "Gary's Garden - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mitch"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mitch"]))
                          and has_textbox(state, player, world, "Gary's Garden"),
        # Fish
        "Salmon Creek Forest - Bass":
            lambda state: has_contact_list(state, player, 1)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Catfish":
            lambda state: has_contact_list(state, player, 1)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Pike":
            lambda state: has_contact_list(state, player, 1)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Salmon":
            lambda state: has_contact_list(state, player, 1)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Trout":
            lambda state: has_contact_list(state, player, 1)
                          and can_swim(state, player, world),
        "Bathhouse - Anglerfish":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Bathhouse - Clione":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Bathhouse - Little Wiggly Guy":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Bathhouse - Jellyfish":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Bathhouse - Pufferfish":
            lambda state: has_contact_list(state, player, 2)
                          and can_swim(state, player, world),
        "Hairball City - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Hairball City Fish", player, 5))
                          and has_textbox(state, player, world, "Hairball City")
                          and can_swim(state, player, world),
        "Turbine Town - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Turbine Town Fish", player, 5))
                          and has_textbox(state, player, world, "Turbine Town")
                          and can_swim(state, player, world),
        "Public Pool - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Public Pool Fish", player, 5))
                          and has_textbox(state, player, world, "Public Pool")
                          and can_swim(state, player, world),
        "Tadpole HQ - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Tadpole HQ Fish", player, 5))
                          and has_textbox(state, player, world, "Tadpole HQ")
                          and can_swim(state, player, world),
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
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"])
                          and has_textbox(state, player, world, "Tadpole HQ"),
        # Seedsanity
        "Hairball City - Seed By Nina":
            lambda state: state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Upper Flowerbed":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed On Top Of Lighthouse":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed On Top Of Palm Tree":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Train":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Wood Posts In Water":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Frog Of Destruction":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Frog Statue":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Mitch":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Seed By Turbine":
            lambda state: has_contact_list(state, player, 1),
        "Salmon Creek Forest - Moomy":
            lambda state: (options.seedsanity.value != 2 or state.has("Salmon Creek Forest Seed", player, 10))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Bathhouse - Moomy":
            lambda state: (options.seedsanity.value != 2 or state.has("Bathhouse Seed", player, 10))
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_ac(state, player, world),
        # Flowersanity
        "Public Pool - Left Flowerbed":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Middle Flowerbed":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Right Flowerbed":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Flowerbed By Gabi":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Flowerbed By Axolotl Family":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Flowerbed Above Axolotl Family":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Hairball City Flower", player, 3))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Turbine Town Flower", player, 3))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Salmon Creek Forest Flower", player, 6))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Tadpole HQ - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Tadpole HQ Flower", player, 4))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        # Progressive Cassette Logic
        "Mitch/Mai - 1":
            lambda state: (has_enough_cassettes(state, player, 1)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 1))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 2":
            lambda state: (has_enough_cassettes(state, player, 2)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 2))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 3":
            lambda state: (has_enough_cassettes(state, player, 3)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 3))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 4":
            lambda state: (has_enough_cassettes(state, player, 4)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 4))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 5":
            lambda state: (has_enough_cassettes(state, player, 5)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 5))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 6":
            lambda state: (has_enough_cassettes(state, player, 6)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 6))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 7":
            lambda state: (has_enough_cassettes(state, player, 7)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 7))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 8":
            lambda state: (has_enough_cassettes(state, player, 8)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 8))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 9":
            lambda state: (has_enough_cassettes(state, player, 9)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 9))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 10":
            lambda state: (has_enough_cassettes(state, player, 10)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 10))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 11":
            lambda state: (has_enough_cassettes(state, player, 11)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 11))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 12":
            lambda state: (has_enough_cassettes(state, player, 12)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 12))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 13":
            lambda state: (has_enough_cassettes(state, player, 13)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 13))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 14":
            lambda state: (has_enough_cassettes(state, player, 14)
                          and (sum(func(state) for func in MitchMaiProgressiveList) >= 14))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),

        "Hairball City - Apple On Frog Statue Island Pier 1":
            lambda state: can_swim(state, player, world),
        "Hairball City - Apple On Frog Statue Island Pier 2":
            lambda state: can_swim(state, player, world),
        "Hairball City - Apple On Frog Statue Island Pier 3":
            lambda state: can_swim(state, player, world),
        "Hairball City - Apple On Frog Statue Island Pier 4":
            lambda state: can_swim(state, player, world),
        "Hairball City - Apple On Frog Statue Island Pier 5":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bug On Frog Statue Island 1":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bug On Frog Statue Island 2":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bug On Frog Statue Island 4":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bug On Frog Statue Island 5":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bug On Frog Statue Island 3":
            lambda state: can_swim(state, player, world),

        "Salmon Creek Forest - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Salmon Creek Forest Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Public Pool Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Tadpole HQ - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Tadpole HQ Bone", player, 5))
                          and can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Tadpole HQ - Blessley":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Hairball City - Blessley":
            lambda state: (has_textbox(state, player, world, "Hairball City")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Turbine Town - Blessley":
            lambda state: (has_textbox(state, player, world, "Turbine Town")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Salmon Creek Forest - Blessley":
            lambda state: (has_textbox(state, player, world, "Salmon Creek Forest")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Turbine Town - Shipping Container With Breakable Boxes":
            lambda state: can_bonk(state, player, world),
        "Bathhouse - Breakable Box Inside Bathhouse Box":
            lambda state: can_bonk(state, player, world),
        "Hairball City - Breakable Boxes Near Frog Of Destruction":
            lambda state: can_bonk(state, player, world),
        "Salmon Creek Forest - Inside Boxes (Waterfall Cave)":
            lambda state: can_bonk(state, player, world),
        "Public Pool - Breakable Boxes Near Frogtective":
            lambda state: can_bonk(state, player, world)
                          and can_swim(state, player, world),
        "Public Pool - Above Small Island":
            lambda state: can_bonk(state, player, world)
                          and can_ac(state, player, world),
        "Tadpole HQ - Breakable Boxes near Blessley":
            lambda state: can_bonk(state, player, world),

        "Hairball City - Big Umbrella":
            lambda state: can_parasol(state, player, world),
        "Hairball City - Palm Tree":
            lambda state: can_parasol(state, player, world),
        "Hairball City - Bug On Tall Palm Tree Platform 1":
            lambda state: can_parasol(state, player, world),
        "Hairball City - Bug On Tall Palm Tree Platform 2":
            lambda state: can_parasol(state, player, world),
        "Turbine Town - Stone Pillar Behind Wind Turbine":
            lambda state: can_parasol(state, player, world),
        "Turbine Town - Bug On Stone Pillar Behind Wind Turbine 1":
            lambda state: can_parasol(state, player, world),
        "Turbine Town - Bug On Stone Pillar Behind Wind Turbine 2":
            lambda state: can_parasol(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 1":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 2":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: can_parasol(state, player, world)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 4":
            lambda state: can_parasol(state, player, world)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 5":
            lambda state: can_parasol(state, player, world)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 6":
            lambda state: can_parasol(state, player, world)
                          and can_swim(state, player, world),
        "Salmon Creek Forest - Apple By Soda Cannon In Treetops 1":
            lambda state: can_soda(state, player, world),
        "Salmon Creek Forest - Apple By Soda Cannon In Treetops 2":
            lambda state: can_soda(state, player, world),
        "Salmon Creek Forest - Apple By Soda Cannon In Treetops 3":
            lambda state: can_soda(state, player, world),
        "Salmon Creek Forest - Apple By Soda Cannon In Treetops 4":
            lambda state: can_soda(state, player, world),
        "Salmon Creek Forest - Apple By Soda Cannon In Treetops 5":
            lambda state: can_soda(state, player, world),

        "Public Pool - Far Away Island":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Far Away Island Left Side":
            lambda state: can_soda(state, player, world),
        "Public Pool - Far Away Island Right Side":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Niko & 2D (Thought)":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 1":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 2":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 3":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 4":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 5":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 6":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 7":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 8":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 9":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 10":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 11":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 12":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 13":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 14":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 15":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 16":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 17":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 18":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 19":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 20":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 21":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 22":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 23":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Public Pool - Apple On Far Away Island 24":
            lambda state: can_soda(state, player, world)
                          and can_parasol(state, player, world),
        "Tadpole HQ - Big Tree Next To Louist":
            lambda state: can_soda(state, player, world),

        "Turbine Town - Near Fishing Containers":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Niko is a ninja (Thought)":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Fan to Fan":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 8":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 1":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 7":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 6":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 5":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 4":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 3":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple Near Dustan 2":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Seed On Lamp Near Office":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Seed In Office":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Seed By Serschel & Louist":
            lambda state: can_ac(state, player, world),
        "Bathhouse - Apple By Handsome Frog 1":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 2":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 3":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 4":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 5":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 6":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 7":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 8":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 9":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Apple By Handsome Frog 10":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Bug Near Handsome Frog 1":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Bug Near Handsome Frog 2":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - Bug Near Handsome Frog 3":
            lambda state: (can_soda(state, player, world) or can_ac(state, player, world)),

        "Achievement - Lost at Sea":
            lambda state: can_swim(state, player, world)
                          or (has_enough_seeds(state, player, world, 10)
                          and can_ac(state, player, world)
                          and can_soda(state, player, world)),
        "Hairball City - Behind The Train":
            lambda state: can_swim(state, player, world, True),
        "Home - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Hairball City - Frog Statue Crown":
            lambda state: can_swim(state, player, world),
        "Hairball City - Moorish Idol":
            lambda state: can_swim(state, player, world),
        "Hairball City - Not Nemo":
            lambda state: can_swim(state, player, world),
        "Hairball City - Eel":
            lambda state: can_swim(state, player, world),
        "Hairball City - Flying Fish":
            lambda state: can_swim(state, player, world),
        "Hairball City - Orange Fish":
            lambda state: can_swim(state, player, world),
        "Hairball City - Bone In Bush Ring":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Bone In Breakable Boxes On Left Building":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Bone On Back Building":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Bone On Right Building":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Bone Between Middle Buildings":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Hairball City - Kappa (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Dog (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Dog 2 (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Hairball City - Niko admires a Frog Statue (Thought)":
            lambda state: can_swim(state, player, world),
        "Hairball City - Nervous Frog (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Hairball City - Next to Breakable Boxes Under Ramp":
            lambda state: can_swim(state, player, world, True),

        "Turbine Town - Albino Corydoras":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Axolotl":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Piranha":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Mantaray":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Sand Shrimp":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Bone Above Big Parasol":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Bone On Edge Of Pig Parasol":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Bone Under Big Parasol":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Bone Above Back Parasol":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Bone Above Right Parasol":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 1),
        "Turbine Town - Dog 2 (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Turbine Town - Kappa (Chatsanity)":
            lambda state: has_contact_list(state, player, 2)
                          and can_ac(state, player, world),
        "Turbine Town - Dog (Chatsanity)":
            lambda state: has_contact_list(state, player, 2)
                          and can_ac(state, player, world),
        "Turbine Town - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Britney (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Turbine Town - Next To Torii Gates":
            lambda state: can_swim(state, player, world, True)
                          or can_parasol(state, player, world),

        "Salmon Creek Forest - Beneath Pond":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bone On Building":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bone Above Parasol":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world),
        "Salmon Creek Forest - Bone On Left Of Bone Dog":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bone On Right Of Bone Dog":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bone On Back Of Rock":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Woodisch (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Divin' Doe (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Niko & a rock (Thought)":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 1":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 2":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bug On Second Rock Cluster Near Submerged Building In Ocean":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bug On Fourth Rock Cluster Near Submerged Building In Ocean":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bug Around Lower Pond 6":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bug Below Treehouse In Bushes 2":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bug On Third Rock Cluster Near Submerged Building In Ocean":
            lambda state: can_swim(state, player, world),
        "Salmon Creek Forest - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world),

        "Public Pool - Inside BIG Pool":
            lambda state: can_swim(state, player, world),
        "Public Pool - Inside Pool":
            lambda state: can_swim(state, player, world),
        "Public Pool - Bone In Breakable Boxes 1":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Public Pool - Bone In Breakable Boxes 2":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Public Pool - Bone In Breakable Boxes 3":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Public Pool - Bone In Breakable Boxes 4":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Public Pool - Bone In Breakable Boxes 5":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Public Pool - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Public Pool - Shark":
            lambda state: can_swim(state, player, world),
        "Public Pool - Squid":
            lambda state: can_swim(state, player, world),
        "Public Pool - Turtle":
            lambda state: can_swim(state, player, world),
        "Public Pool - Gramma Loreto":
            lambda state: can_swim(state, player, world),
        "Public Pool - Baby Crocodile":
            lambda state: can_swim(state, player, world),
        "Public Pool - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Public Pool - Britney (Chatsanity)":
            lambda state: can_swim(state, player, world, True),
        "Public Pool - Niko, Pink Frog & King Frog (Thought)":
            lambda state: can_swim(state, player, world, True),
        "Public Pool - Frog Hint (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Frog Hint 2 (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Behind Frog Statue":
            lambda state: can_swim(state, player, world),
        "Public Pool - Bug On Frog Statue 1":
            lambda state: can_swim(state, player, world, True),
        "Public Pool - Bug On Frog Statue 2":
            lambda state: can_swim(state, player, world, True),
        "Public Pool - First Apple Group Near Shallow Pool First Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - First Apple Group Near Shallow Pool First Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - First Apple Group Near Shallow Pool First Palm Tree 3":
            lambda state: can_swim(state, player, world),
        "Public Pool - First Apple Group Near Shallow Pool Second Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - First Apple Group Near Shallow Pool Second Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - First Apple Group Near Shallow Pool Second Palm Tree 3":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool First Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool First Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool First Palm Tree 3":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool Second Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool Second Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - Second Apple Group Near Shallow Pool Second Palm Tree 3":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool First Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool First Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool First Palm Tree 3":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool Second Palm Tree 1":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool Second Palm Tree 2":
            lambda state: can_swim(state, player, world),
        "Public Pool - Third Apple Group Near Shallow Pool Second Palm Tree 3":
            lambda state: can_swim(state, player, world),

        "Bathhouse - Bone Above Middle Bathhouse":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Bone In Middle Bathhouse":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Bone Above Right Bathhouse":
            lambda state: can_swim(state, player, world)
                          and can_parasol(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Bone In Water In Left Bathhouse":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Bone On Right Bathhouse":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world)
                          and has_contact_list(state, player, 2),
        "Bathhouse - Hut in Water":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Steamy Frog (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Mickey (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Moe (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Marshal (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Lil' Sis Doe (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Carl (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Biki (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Wess (Chatsanity)":
            lambda state: can_swim(state, player, world),

        "Tadpole HQ - Bone On Wood Board On Side Of Right Building":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Bone Above Right Building":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Bone On Small Building Behind Big Building":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Bone In Breakable Boxes On Middle Building":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world),
        "Tadpole HQ - Bone On Net Near Left Building":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Blue Fairy Shrimp":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Bluestreak Cleaner Wrasse":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Honey Gourami":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Loach":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Neon Tetra":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Hasselhop (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Blippy (Chatsanity)":
            lambda state: (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player)),
        "Tadpole HQ - Bone Dog (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Dog (Chatsanity)":
            lambda state: can_swim(state, player, world)
                          and can_bonk(state, player, world)
                          and (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player)),
        "Tadpole HQ - Apple On Xylophone":
            lambda state: can_swim(state, player, world),
        "Tadpole HQ - Bug Near Fischer 1":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Fischer 2":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Fischer 3":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Fischer 4":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Apple Behind Bench Near Fischer":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Fischer's Pond":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Apple Behind Fischer Towards Rocks":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Rocks Behind Fischer 1":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Bug Near Rocks Behind Fischer 2":
            lambda state: can_swim(state, player, world, True),
        "Tadpole HQ - Behind Fischer On A Rock":
            lambda state: can_swim(state, player, world, True),

        "Home - Give High Frog Lunchbox":
            lambda state: has_textbox(state, player, world, "Home"),
        "Hairball City - BIG VOLLEY":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Dustan on Lighthouse":
            lambda state: (has_textbox(state, player, world, "Hairball City")
                          and can_parasol(state, player, world)),
        "Hairball City - Gunter on Skyscraper":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Hairball City"),

        "Turbine Town - AIR VOLLEY":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Pelly the Engineer":
            lambda state: has_textbox(state, player, world, "Turbine Town"),

        "Salmon Creek Forest - Dustan on Mountain":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Nina":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Stijn & Melissa":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Treeman":
            lambda state: (has_textbox(state, player, world, "Salmon Creek Forest")
                          and can_bonk(state, player, world)),

        "Public Pool - Frogtective":
            lambda state: has_textbox(state, player, world, "Public Pool"),
        "Public Pool - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Public Pool"),

        "Bathhouse - Dustan on Bathhouse":
            lambda state: (has_textbox(state, player, world, "Bathhouse")
                          and can_ac(state, player, world)),
        "Bathhouse - Game Kid":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Bathhouse")
                          and (can_soda(state, player, world) or can_ac(state, player, world)),
        "Bathhouse - LONG VOLLEY":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Nina":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Serschel & Louist":
            lambda state: has_textbox(state, player, world, "Bathhouse"),

        "Tadpole HQ - Dojo Guy":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and (options.applebasket.value != 1 or state.has("Apple Basket", player))),
        "Tadpole HQ - Serschel & Louist":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and can_parasol(state, player, world)),
        "Tadpole HQ - Frog King":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),
        "Tadpole HQ - HUGE VOLLEY":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),

        "Hairball City - Blippy (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Blippy Dog (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Game Kid (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Louist (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Serschel (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Hairball City - Nina (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Melissa (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Mitch (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Mai (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Moomy (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Hairball City - Dustan (Chatsanity)":
            lambda state: can_parasol(state, player, world),

        "Turbine Town - Blippy (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Turbine Town - Blippy Dog (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Turbine Town - Serschel (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Turbine Town - Louist (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Turbine Town - Mitch (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Turbine Town - Mai (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Turbine Town - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine"),
        "Turbine Town - Melissa & Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa"),

        "Salmon Creek Forest - Blippy (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Salmon Creek Forest - Fischer (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Salmon Creek Forest - Mai (Chatsanity)":
            lambda state: has_contact_list(state, player, 1)
                          and (state.has("Key", player, 7)
                           or state.has("Salmon Creek Forest Key", player)),
        "Salmon Creek Forest - Serschel (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Salmon Creek Forest - Louist (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Salmon Creek Forest - Trixie (Chatsanity)":
            lambda state: has_contact_list(state, player, 1),
        "Salmon Creek Forest - Game Kid (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
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
            lambda state: can_bonk(state, player, world),

        "Public Pool - Blessley (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Clint (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Public Pool - Mitch (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Blippy (Chatsanity)":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Public Pool Key", player)),
        "Public Pool - Little Gabi (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Trixie (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Public Pool - Vlog Frog (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
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
        "Public Pool - Melissa & Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa"),

        "Bathhouse - Blessley (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Vlog Frog (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Fischer (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Little Gabi (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Blippy (Chatsanity)":
            lambda state: has_contact_list(state, player, 2)
                          and (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Blippy Dog (Chatsanity)":
            lambda state: has_contact_list(state, player, 2),
        "Bathhouse - Gashadokuro (Chatsanity)":
            lambda state: can_swim(state, player, world),
        "Bathhouse - Mahjong Frogs (Chatsanity)":
            lambda state: has_contact_list(state, player, 2)
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
            lambda state: has_access_to(state, player, "Public Pool - Frogtective")
                          and can_swim(state, player, world),
        "Bathhouse - David D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective")
                          and can_swim(state, player, world),
        "Bathhouse - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"),

        # Chatsanity Global
        "Chatsanity - (Ex) Employee of the month":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - AC Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Accountant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Alice":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Assistant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Baby Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Baby Gull (TT)":
            lambda state: (state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town")),
        "Chatsanity - Big Bro Stag":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Biki":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Bird":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 4)
                          and can_ac(state, player, world),
        "Chatsanity - Blast Frog":
            lambda state: has_textbox(state, player, world, "Home"),
        "Chatsanity - Blessley":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Blippy":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and (state.has("Key", player,7)
                                   or state.has("Tadpole HQ Key", player))
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Blippy Dog":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Bobby":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Borbie":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ")
                          and has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Chatsanity - Britney":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and can_swim(state, player, world, True)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Public Pool Ticket", player)
                              and can_swim(state, player, world, True)
                              and has_textbox(state, player, world, "Public Pool")),
        "Chatsanity - Brooklyn Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Button Bird":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Carl":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Carrot":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Clint":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool")
                          and can_swim(state, player, world),
        "Chatsanity - Clover":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Coco":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Code Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Coffee Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Conspiracy Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 2),
        "Chatsanity - Culley":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Culture Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Dance Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 8)
                          and can_ac(state, player, world),
        "Chatsanity - Danger Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 5)
                          and can_ac(state, player, world),
        "Chatsanity - David D. Carota":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Dirk":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Dispatcher":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City")
                          or state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town")
                          or state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          or state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool")
                          or state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or has_textbox(state, player, world, "Home"),
        "Chatsanity - Divin' Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and can_swim(state, player, world),
        "Chatsanity - Doe of Darkness":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Dream Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 3)
                          and can_ac(state, player, world),
        "Chatsanity - Dustan":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or has_access_to(state, player, "Dustan - Meeting First Time"),
        "Chatsanity - Elizabeth IV":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Fear Deer":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Fear Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 7)
                          and can_ac(state, player, world),
        "Chatsanity - Fischer":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Fix Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Fizzy the Frog":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Flippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Flower Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 1),
        "Chatsanity - Flowery Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Friendly Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Frog (Frogbucks)":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Frog King":
            lambda state: (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Frog of Destruction":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Frogtective":
            lambda state: (state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Frogucus the Green":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Fry Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Fry loving Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Game Kid":
            lambda state: (state.has("Hairball City Ticket", player)
                           and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Gamedev Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Gary":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Gashadokuro":
            lambda state: state.has("Bathhouse Ticket", player)
                          and can_swim(state, player, world)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Gull Friend":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Gull Friend 2":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Gunter":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (has_access_garden(state, player, world)
                              and has_enough_seeds(state, player, world, 10)
                              and can_ac(state, player, world)
                              and can_soda(state, player, world)),
        "Chatsanity - HUD Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - High Frog":
            lambda state: has_textbox(state, player, world, "Home"),
        "Chatsanity - Handsome Frog":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                              and (can_soda(state, player, world) or can_ac(state, player, world))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (has_access_garden(state, player, world)
                              and has_enough_seeds(state, player, world, 2)),
        "Chatsanity - Hasselhop":
            lambda state: (can_swim(state, player, world)
                           and can_talk_everywhere(state, player, world))
                          or (has_access_garden(state, player, world)
                              and has_enough_seeds(state, player, world, 10)
                              and can_soda(state, player, world)
                              and can_ac(state, player, world)),
        "Chatsanity - Hat Kid":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Hint Frog":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool")
                          and has_contact_list(state, player, 2),
        "Chatsanity - Hint Frog 2":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool")
                          and has_contact_list(state, player, 2),
        "Chatsanity - Hungry Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 9)
                          and can_soda(state, player, world)
                          and can_ac(state, player, world),
        "Chatsanity - Impatient Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Jess":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Jiji":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Jippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Knowledgeable Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Lil' Sis Doe":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Little Gabi":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Low Frog":
            lambda state: has_textbox(state, player, world, "Home"),
        "Chatsanity - Lock Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Loud Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Louist":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Maggie":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mahjong Frog":
            lambda state: (state.has("Bathhouse Ticket", player)
                           and (state.has("Key", player, 7)
                                or state.has("Bathhouse Key", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mai":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 1)
                              and state.has("Key", player, 7)
                                   or state.has("Salmon Creek Forest Key", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Marry D. Carota":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Marshal":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Master":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Melissa":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or has_access_to(state, player, "Hairball City - Nina")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mata":
            lambda state: has_textbox(state, player, world, "Home"),
        "Chatsanity - Mickey":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Miki":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Minoes":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Mitch":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Moe":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Mom Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Mom Gull (TT)":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Monty":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Moomy":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mysterious Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Mythology Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Nervous Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and can_swim(state, player, world)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Niko a0.45":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Nina":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Noah":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Paul":
            lambda state: (state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Pepper":
            lambda state: state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City")
                          or state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town")
                          or state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest")
                          or state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool")
                          or state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")
                              and has_enough_coins(state, player, world.kiosk_cost["Elevator"]))
                          or has_textbox(state, player, world, "Home"),
        "Chatsanity - Pelly the Engineer":
            lambda state: (state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Penny":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2))
                          and state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Pine Frog":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and can_bonk(state, player, world),
        "Chatsanity - Poppy":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                           or ((state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2))
                          and state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")),
        "Chatsanity - R&D Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - R&D Frog 2":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - R&D Frog 3":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Ricky":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Robo Fr0g":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Salty Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Scare Frog":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest")),
        "Chatsanity - Serschel":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Shovelin' Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Simon":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Skippy":
            lambda state: ((state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                           or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool")))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Slack Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Small Talk Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Snip Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Snow Frog Frog":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Steamy Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Steamy Frog":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Stijn":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or has_access_to(state, player, "Hairball City - Nina")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Stijn's Dad":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Stijn's Mom":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Superstitious Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Sushi Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Swimming Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Tax Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Tip Frog":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Tippy":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Tough Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Tourist Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 6)
                          and can_ac(state, player, world),
        "Chatsanity - Train Frog":
            lambda state: state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City")
                          or state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town")
                          or state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest")
                          or state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool")
                          or state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Travis":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Treeman":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Turbine Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Trixie":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_contact_list(state, player, 1)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool")),
        "Chatsanity - VR Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Vlog Frog":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Vacation Frog":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Wess":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse")
                          and can_swim(state, player, world),
        "Chatsanity - Wind Dragon":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Woodisch":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and can_swim(state, player, world)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Turbine Town - Inside Partially Sunken Shipping Container":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Above Partially Sunken Shipping Container":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug By Sunken Container 4":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug By Sunken Container 2":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug By Sunken Container 3":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug By Sunken Container 1":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug By Sunken Container 5":
            lambda state: can_swim(state, player, world, True),
        "Turbine Town - Bug On Top Of Wind Turbine":
            lambda state: state.has("Key", player, 7)
                          or state.has("Turbine Town Key", player),
        "Tadpole HQ - Borbie (Chatsanity)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Tadpole HQ - Pepper (Chatsanity)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Chatsanity - Bone Dog":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 1)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 1)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_contact_list(state, player, 2)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and can_swim(state, player, world)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Kappa":
            lambda state:(state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Turbine Town")),
        "Chatsanity - Dog":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and can_ac(state, player, world)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and can_swim(state, player, world)
                              and can_bonk(state, player, world)
                              and (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player))
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Dog 2":
            lambda state: (state.has("Hairball City Ticket", player)
                           and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_contact_list(state, player, 2)
                              and has_textbox(state, player, world, "Turbine Town")),
        "Tadpole HQ - Niko has nightmares (Thought)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Tadpole HQ - Inbetween Four Skyscrapers":
            lambda state: can_swim(state, player, world, True),
        # Gary's Garden Seeds
        "Gary's Garden - Seed 2":
            lambda state: state.has("Gary's Garden Seed", player, 1),
        "Gary's Garden - Seed 3":
            lambda state: state.has("Gary's Garden Seed", player, 2),
        "Gary's Garden - Seed 4":
            lambda state: state.has("Gary's Garden Seed", player, 3)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 5":
            lambda state: state.has("Gary's Garden Seed", player, 4)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 6":
            lambda state: state.has("Gary's Garden Seed", player, 5)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 7":
            lambda state: state.has("Gary's Garden Seed", player, 6)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 8":
            lambda state: state.has("Gary's Garden Seed", player, 7)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 9":
            lambda state: state.has("Gary's Garden Seed", player, 8)
                          and can_ac(state, player, world),
        "Gary's Garden - Seed 10":
            lambda state: state.has("Gary's Garden Seed", player, 9)
                          and can_soda(state, player, world)
                          and can_ac(state, player, world),

        "Gary's Garden - Flower Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 1),
        "Gary's Garden - Small Rocks In Water":
            lambda state: has_enough_seeds(state, player, world, 1),
        "Gary's Garden - Handsome Frog":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Handsome Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Conspiracy Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Dream Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 3)
                          and can_ac(state, player, world),
        "Gary's Garden - Behind Large Rock":
            lambda state: has_enough_seeds(state, player, world, 3)
                          and can_ac(state, player, world),
        "Gary's Garden - Bird (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 4)
                          and can_ac(state, player, world),
        "Gary's Garden - On Tree Branch":
            lambda state: has_enough_seeds(state, player, world, 4)
                          and can_ac(state, player, world),
        "Gary's Garden - Danger Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 5)
                          and can_ac(state, player, world),
        "Gary's Garden - Next To Smaller Tree":
            lambda state: has_enough_seeds(state, player, world, 5)
                          and can_ac(state, player, world),
        "Gary's Garden - Tourist Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 6)
                          and can_ac(state, player, world),
        "Gary's Garden - Next Garden Seed On Rocks":
            lambda state: has_enough_seeds(state, player, world, 6)
                          and can_ac(state, player, world),
        "Gary's Garden - Fear Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 7)
                          and can_ac(state, player, world),
        "Gary's Garden - Beginning Of Giant Gold Scissor":
            lambda state: has_enough_seeds(state, player, world, 7)
                          and can_ac(state, player, world),
        "Gary's Garden - Near End Of Giant Gold Scissor":
            lambda state: has_enough_seeds(state, player, world, 7)
                          and can_ac(state, player, world),
        "Gary's Garden - Dance Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 8)
                          and can_ac(state, player, world),
        "Gary's Garden - Tree Branch Near Gold Scissor Row":
            lambda state: has_enough_seeds(state, player, world, 8)
                          and can_ac(state, player, world),
        "Gary's Garden - Hungry Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 9)
                          and can_soda(state, player, world)
                          and can_ac(state, player, world),
        "Gary's Garden - Tree Branch Near The Top":
            lambda state: has_enough_seeds(state, player, world, 9)
                          and can_soda(state, player, world)
                          and can_ac(state, player, world),
        "Gary's Garden - Gunter (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 10)
                          and can_ac(state, player, world)
                          and can_soda(state, player, world),
        "Gary's Garden - Hasselhop (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 10)
                          and can_ac(state, player, world)
                          and can_soda(state, player, world),
        "Gary's Garden - Gunter & Little Gabi":
            lambda state: can_ac(state, player, world)
                          and can_soda(state, player, world),
    }
