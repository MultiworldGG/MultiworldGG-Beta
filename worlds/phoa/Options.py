from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions, DeathLink, Choice

class EnableNpcGifts(Toggle):
    """Include free gifts from NPCs"""
    display_name = "Include NPC gifts"

class EnableMisc(Toggle):
    """Include miscellaneous locations and items"""
    display_name = "Include miscellaneous"

class EnableShopSanity(Toggle):
    """Includes items that can be bought it shops"""
    display_name = "Shop sanity"

class EnableSmallAnimalDrops(Toggle):
    """Includes drops from animals like lizards, mice, scorpions and birds"""
    display_name = "Include small animal drops"

class EnableRinLocations(Choice):
    """Includes rin pickups from chests and other breakables that give at least 5 rin"""
    display_name = "Include rin locations"
    options_No = 0
    option_Chests_only = 1
    option_Everything = 2

@dataclass
class PhoaOptions(PerGameCommonOptions):
    enable_npc_gifts: EnableNpcGifts
    enable_misc: EnableMisc
    shop_sanity: EnableShopSanity
    enable_small_animal_drops: EnableSmallAnimalDrops
    enable_rin_locations: EnableRinLocations
    death_link: DeathLink
