class Elements:
    normal = "Normal"
    fire = "Fire"
    ice = "Ice"
    poison = "Poison"
    light = "Light"
    dark = "Dark"
    dark_and_light = "Dark and Light"
    normal_and_fire = "Normal and Fire"
    ice_and_poison = "Ice and Poison"
    dark_and_fire = "Dark and Fire"
    ignore = "IGNORE"

    all_elements = [normal, fire, ice, poison, light, dark, dark_and_fire, dark_and_light, normal_and_fire, ice_and_poison, dark_and_fire]
    spell_elements = [normal, fire, ice, poison, light, dark]
    poison_or_dark = [poison, ice_and_poison, dark, dark_and_light, dark_and_fire]
    fire_options = [fire, normal_and_fire, dark_and_fire]
    light_options = [light, dark_and_light]


class Types:
    melee = "Melee"
    ranged = "Ranged"
    both = "Both"
    support = "Support"
