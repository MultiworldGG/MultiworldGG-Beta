from .ApworldLocations import raw_objectsanity_dict

land_vehicles = [
    "Van",
    "Vintage Car",
    "Grandpa Miller's Car",
    "Fire Truck",
    "Dirt Bike",
    "Penny Farthing",
    "Recreation Vehicle",
    "Golf Cart",
    "Motorbike and Sidecar",
    "SUV",
    "Drill",
    "Monster Truck",
]

water_vehicles = [
    "Frolic Boat",
    "Fishing Boat",
]

air_vehicles = [
    "Fire Helicopter",
    "Private Jet",
    "Stunt Plane",
    "Recreational Vehicle (Again)",
]

places = [
    "Back Garden",
    "Bungalow",
    "Playground",
    "Detached House",
    "Shoe House",
    "Fire Station",
    "Skatepark",
    "Forest Cottage",
    "Mayor's Mansion",
    "Carousel",
    "Tree House",
    "Temple",
    "Washroom",
    "Helter Skelter",
    "Ferris Wheel",
    "Subway Platform",
    "Fortune Teller's Wagon",
    "Ancient Statue",
    "Ancient Monument",
    "Lost City Palace",
]

bonus_jobs = [
    "Mars Rover",
    "Gnome Fountain",
    "Mini Golf Course",
    "Steam Locomotive",
    "Food Truck",
    "Satellite Dish",
    "Solar Station",
    "Paintball Arena",
    "Spanish Villa",
    "Excavator",
    "Aquarium",
    "Submarine",
    "Modern Mansion",
    "Fire Plane",
    "Dessert Parlor",
    "Subway Train",
    "Sculpture Park",
]

midgar = [
    "Scorpion Sentinel",
    "Hardy-Daytona & Shinra Hauler",
    "Seventh Heaven",
    "Mako Energy Exhibit",
    "Airbuster",
]

tomb_raider = [
    "Croft Manor",
    "Lara Croft's Obstacle Course and Quad Bike",
    "Lara Croft's Jeep and Motorboat",
    "Croft Manor's Maze",
    "Croft Manor's Treasure Room",
]

wallace_and_gromit = [
    "Wallace & Gromit's Dining Room & Kitchen",
    "Wallace & Gromit's House",
    "The Knit-O-Matic",
    "Wallace & Gromit's Vehicles",
    "The Moon Rocket",
]

shrek = [
    "Shrek's Swamp",
    "Duloc",
    "Fairy Godmother's Potion Factory",
    "Dragon's Lair",
    "Hansel's Honeymoon Hideaway",
]

alice = [
    "Wonderland Entrance Hall",
    "White Rabbit's House",
    "Caterpillar's Mushroom",
    "Mad Tea Party",
    "Queen of Hearts' Court",
]

warhammer_40k = [
    "Land Raider",
    "Redemptor Dreadnought",
    "Imperial Knight Paladin",
    "Rogal Dorn Battle Tank",
    "Thunderhawk",
]

back_to_the_future = [
    "Doc Brown's Van",
    "The Time Machine",
    "Hill Valley Clocktower",
    "The Holomax Theater",
    "Doc's Time Train",
]

spongebob = [
    "Conch Street",
    "Bikini Bottom Buss",
    "Krusty Krab",
    "Patty Wagon",
    "The Invisible Boatmobile",
    "The Mermalair",
]

raw_location_dict = land_vehicles + water_vehicles + air_vehicles + places + bonus_jobs + midgar + tomb_raider + wallace_and_gromit + shrek + alice + warhammer_40k + back_to_the_future + spongebob
addendums = [f"{num}%" for num in range(1, 101)]

locations_percentages = {location: [f"{location} {addendum}" for addendum in addendums] for location in
                         raw_location_dict}
objectsanity_dict = {location: [f"{location}: {part}" for part in parts] for location, parts in
                     raw_objectsanity_dict.items()}

flat_locations_percentages = [location for _, percentages in locations_percentages.items() for location in percentages]
flat_objectsanity_dict = [part for _, parts in objectsanity_dict.items() for part in parts]

location_dict = flat_locations_percentages + flat_objectsanity_dict
