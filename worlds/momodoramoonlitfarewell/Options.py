from Options import Choice, Toggle, Range, PerGameCommonOptions
from dataclasses import dataclass

class OpenSpringleafPath(Toggle):
    """Remove Demon Strings and Wind Barriers in Springleaf Path to enable entering other areas before getting Awakened Sacred Leaf/Sacred Anemone."""
    display_name = "Open Springleaf Path"
    default = 1

class DeathLink(Toggle):
    """Link all player deaths together. If you die, all other players in the session (with deathlink enabled) also die. The same works the other way around."""
    display_name = "Deathlink"
    default = 1

class BellHover(Toggle):
    """Consider Bell Hover as a possible strat for world generation. Bell Hover is used to access certain areas without having the correct skill (i.e. Demon Frontier without Wall Jump) \n# With this setting on, you might need to get creative to access certain areas (i.e. using damage boost to reach a platform, speaking from experience)"""
    display_name = "Bell Hover Generation"
    default: 0

class RandomizeKeyItems(Toggle):
    """Add Key Items needed for progression to the randomization pool and as location checks. These items are: Gold Moonlit Dust, Silver Moonlit Dust and Windmill Key."""
    display_name = "Randomize Key items"
    default: 0

class OracleSigil(Toggle):
    """Add the Oracle Sigil to the item pool and as a location check. \n# Oracle requires to free all 30 Lumen Fairies, which can be a long task so it's recommended to have this setting off unless you really want to do this"""
    display_name = "Add Oracle Sigil"
    default = 0

class ProgressiveFinalBossKeys(Toggle):
    """Add 4 progressive keys required to open the door to the Final Boss to the randomization pool. \n# With this enabled, defeating the 4 bosses before the final boss will no longer help to unlock the door"""
    display_name = "Progressive Final Boss Keys"
    default = 0

class ProgressiveDamageUpgrade(Toggle):
    """Add the Heavenly Lilies to the item location check, as well as adding progressive damage upgrade to the itempool (each upgrade grants 2 extra damage)"""
    display_name = "Progressive Damage Upgrade"
    default = 0

class ProgressiveHealthUpgrade(Toggle):
    """Add the Dotted Berries to the item location check, as well as adding progressive health upgrade to the itempool (each upgrade grants 50 extra health)"""
    display_name = "Progressive Health Upgrade"
    default = 0

class ProgressiveMagicUpgrade(Toggle):
    """Add the Lun Berries to the item location check, as well as adding progressive magic upgrade to the itempool (each upgrade grants 10 extra magic)"""
    display_name = "Progressive Magic Upgrade"
    default = 0

class ProgressiveStaminaUpgrade(Toggle):
    """Add the Stamina Peaches to the item location check, as well as adding progressive stamina upgrade to the itempool"""
    display_name = "Progressive Stamina Upgrade"
    default = 0

class ProgressiveLumenFairies(Toggle):
    """Add the Lumen Fairies to the item location check, as well as adding progressive Lumen Fairies to the itempool (you need a total of 30 Lumen Fairies to unlock the Oracle Sigil)"""
    display_name = "Progressive Lumen Fairies"
    default = 0

class VictoryCondition(Choice):
    """Choose which boss must be defeated to be considered as having completed the game."""
    display_name = "Victory Condition"
    option_Moon_God_Selin = 0
    option_Dora = 1
    default = 0
# class FastTravel(Choice):
#     """Whether to start with Fast Travel, add it to the randomization pool, or keep it vanilla (Unlocking Fast Travel is still a location check)"""
#     display_name = "Fast Travel Choice"
#     option_vanilla = 0
#     option_start_with = 1
#     option_add_to_item_pool = 2
#     default = 2

@dataclass
class MomodoraOptions(PerGameCommonOptions):
    open_springleaf_path: OpenSpringleafPath
    deathlink: DeathLink
    bell_hover_generation: BellHover
    randomize_key_items: RandomizeKeyItems
    oracle_sigil: OracleSigil
    final_boss_keys: ProgressiveFinalBossKeys
    progressive_damage_upgrade: ProgressiveDamageUpgrade
    progressive_health_upgrade: ProgressiveHealthUpgrade
    progressive_magic_upgrade: ProgressiveMagicUpgrade
    progressive_stamina_upgrade: ProgressiveStaminaUpgrade
    progressive_lumen_fairies: ProgressiveLumenFairies
    victory_condition: VictoryCondition
    # fast_travel: FastTravel