from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink, TextChoice


class ProgressiveKeys(Choice):
    """Makes the keys progressive items

    Off - Keys are not progressive items

    On - Keys are progressive items, you get Key 1 first and then Key 2
    May make generation impossible if there's only Key 2
    
    Reverse - Keys are progressive items, you get Key 2 first, and then Key 1
    May make generation impossible if there's only Key 1
    
    JSON - Go with the recommended value for the hack you are playing in the JSON
    Will only work with newer JSONs"""
    display_name = "Make keys progressive"
    option_off = 0
    option_on = 1
    option_reverse = 2
    option_json = 3
    default = 3

class TrollStars(Choice):
    """Enables checks for grabbing troll stars, if the JSON supports it. But beware! Every new check created by troll stars adds one trap to the pool!
    In asyncs, traps received while you are not playing will not be received all immediately but will activate randomly while you are playing the game
    Note: Each world has 1 check shared among all its troll stars, not one check per troll star.
    
    Off - Troll stars are not randomized
    
    On - Troll stars are randomized and traps are added to the pool
    
    On (no traps) - Troll stars are randomized and traps are not added into the pool. Instead singular coins will be added"""
    option_off = 0
    option_on = 1
    option_on_no_traps = 2
    display_name = "Troll Stars"

class JsonFile(TextChoice):
    """Name of the hack to use.
    Custom jsons can be used with offline generation by placing the json in the data/sm64hacks folder. Note that Custom Value is not supported in web generation."""
    auto_display_name = True
    display_name = "Hack to Use"
    option_24_hour_hack                = 1
    option_aventure_alpha_redone       = 2
    option_cursed_castles              = 3
    option_despair_marios_gambit_64    = 4
    option_eureka                      = 5
    option_grand_star                  = 6
    option_kaizo_mario_64              = 7
    option_koopa_power                 = 8
    option_lugs_delightful_dioramas    = 9
    option_marios_new_earth            = 10
    option_peachs_memory               = 11
    option_phenomena                   = 12
    option_plutonium_mario_64          = 13
    option_sapphire                    = 14
    option_shining_stars_repainted     = 15
    option_sm64_the_green_stars        = 16
    option_sm74_tya                    = 17
    option_star_revenge_0              = 18
    option_star_revenge_1_dot_5        = 19
    option_star_revenge_2_to_the_moon  = 20
    option_star_revenge_3_dot_5        = 21
    option_star_revenge_3              = 22
    option_star_revenge_4              = 23
    option_star_revenge_4_dot_5        = 24
    option_star_revenge_5              = 25
    option_star_revenge_6_dot_25       = 26
    option_star_revenge_6_dot_5        = 27
    option_star_revenge_6              = 28
    option_star_revenge_7_dot_5        = 29
    option_star_revenge_7_dot_5_expert = 30
    option_star_revenge_7              = 31
    option_star_revenge_7_no_badges    = 32
    option_star_revenge_8              = 33
    option_star_revenge_8_advanced     = 34
    option_star_revenge_8_no_badges    = 35
    option_super_donkey_kong_64        = 36
    option_super_mario_64              = 37
    option_super_mario_74              = 38
    option_super_mario_fantasy_64      = 39
    option_super_mario_star_road       = 40
    option_super_mario_treasure_world  = 41
    option_timeless_rrendezvous        = 42
    option_unoriginal_cringe_meme_hack = 43
    option_ztar_attack_2               = 44
    option_ztar_attack_rebooted        = 45
    default = 37

    @classmethod
    def get_option_name(cls, value) -> str:
        if cls.auto_display_name:
            option_name = cls.name_lookup[value]
            if "_dot_" in cls.name_lookup[value]:
                option_name = option_name.replace("_dot_", ".")
            return option_name.replace("_", " ").title()
        else:
            return cls.name_lookup[value]

    
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    progressive_keys: ProgressiveKeys
    troll_stars: TrollStars
    json_file: JsonFile
    death_link: DeathLink

