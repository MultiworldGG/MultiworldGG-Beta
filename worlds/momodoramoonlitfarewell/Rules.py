from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MomodoraWorld


def set_rules(world: "MomodoraWorld"):
    player = world.player
    multiworld = world.multiworld
    
    #def to help with continous writing of the same function
    def item(item):
        return item, player
    
    def region(region):
        return region, player
    
    set_rule(multiworld.get_entrance(*region("SP_SPC")), 
             lambda state: state.has(*item("Awakened Sacred Leaf")) or
             bool(world.options.open_springleaf_path.value))
    set_rule(multiworld.get_entrance(*region("SPC_LTR")), 
             lambda state: state.has(*item("Sacred Anemone")) or
             bool(world.options.open_springleaf_path.value))
    set_rule(multiworld.get_entrance(*region("SPC_FS")), 
             lambda state: (state.has(*item("Crescent Moonflower")) or
                            state.has(*item("Spiral Shell"))) and
             (bool(world.options.open_springleaf_path.value) or 
             (state.has(*item("Sacred Anemone")))))
    set_rule(multiworld.get_entrance(*region("LTR_FS")), lambda state: state.has(*item("Crescent Moonflower")))
    set_rule(multiworld.get_entrance(*region("KV_OS")), 
             lambda state: state.has(*item("Spiral Shell")) or 
             (state.has(*item("Crescent Moonflower")) and
             (world.options.bell_hover_generation.value or
              state.has(*item("Lunar Attunement")))))
    set_rule(multiworld.get_entrance(*region("OS_OSC")), 
             lambda state: state.has(*item("Spiral Shell")) or
                            (world.options.bell_hover_generation.value and state.has(*item("Lunar Attunement")) and state.has(*item("Crescent Moonflower"))))
    set_rule(multiworld.get_entrance(*region("LTR_DF")), 
             lambda state: state.has(*item("Spiral Shell")) or
             (state.has(*item("Crescent Moonflower")) and world.options.bell_hover_generation.value and (state.has(*item("Progressive Magic Upgrade"), 1) if world.options.progressive_magic_upgrade.value else True)))
    set_rule(multiworld.get_entrance(*region("DF_AH")),
             lambda state: (world.options.bell_hover_generation.value and state.has(*item("Spiral Shell")) and
                            (state.has(*item("Sacred Anemone")) or
                            state.has(*item("Perfect Chime")))) or
                            state.has(*item("Crescent Moonflower"))),
    set_rule(multiworld.get_entrance(*region("LTR_MR")), 
             lambda state: state.has(*item("Spiral Shell")) and
             (state.has("Awakened Sacred Leaf", player) or
              world.options.open_springleaf_path.value))
    set_rule(multiworld.get_entrance(*region("AH_AHC")), lambda state: state.has(*item("Spiral Shell")))
    set_rule(multiworld.get_entrance(*region("DF_DFC")), 
             lambda state: (state.has(*item("Crescent Moonflower")) and
                            (state.has(*item("Spiral Shell")) or state.has(*item("Lunar Attunement")))) or
                            (state.has(*item("Spiral Shell")) and 
                             (state.has(*item("Sacred Anemone")) or state.has(*item("Perfect Chime")))))
    set_rule(multiworld.get_entrance(*region("DFC_MV")), 
             lambda state: state.has(*item("Lunar Attunement")) and
             (state.has(*item("Crescent Moonflower")) if world.options.bell_hover_generation.value else True or
              state.has(*item("Spiral Shell")))),
    set_rule(multiworld.get_entrance(*region("MV_MVW")), 
             lambda state: (state.has("Windmill Key", player) if world.options.randomize_key_items.value else True) and 
             state.has(*item("Spiral Shell")) and
             (state.has(*item("Crescent Moonflower")) or
              world.options.bell_hover_generation.value)),
    set_rule(multiworld.get_entrance(*region("MVW_FOR")), lambda state: 
             state.has(*item("Crescent Moonflower")) and 
              (state.has(*item("Windmill Key")) if world.options.randomize_key_items.value else True)),
    set_rule(multiworld.get_entrance(*region("FOR_SELIN")), lambda state: state.has(*item("Progressive Final Boss Key"), 4) if world.options.final_boss_keys.value else True),
    
    set_rule(multiworld.get_location(*item("Sacred Anemone")), lambda state: world.options.open_springleaf_path.value or state.has(*item("Awakened Sacred Leaf")))

    set_rule(multiworld.get_location(*item("Serval")),
             lambda state: state.has(*item("Crescent Moonflower")) or
             (state.has(*item("Spiral Shell")) if world.options.bell_hover_generation.value else True))
    set_rule(multiworld.get_location(*item("Perfect Chime")), 
             lambda state: state.has(*item("Spiral Shell")) and 
             (world.options.bell_hover_generation.value or 
              state.has(*item("Crescent Moonflower"))))
    set_rule(multiworld.get_location(*item("Mending Resonance")), lambda state: state.has(*item("Lunar Attunement"))),
    set_rule(multiworld.get_location(*item("Resolve")), lambda state: state.has(*item("Lunar Attunement")))
    set_rule(multiworld.get_location(*item("Welkin Leaf")), 
             lambda state: state.has(*item("Crescent Moonflower")) and
             state.has(*item("Spiral Shell")))
    set_rule(multiworld.get_location(*item("Moon Goddess Lineth")),
             lambda state: state.can_reach("Fount of Rebirth", "Region", player))
    set_rule(multiworld.get_location(*item("Harpy Archdemon")),
             lambda state: state.has(*item("Awakened Sacred Leaf")) or
              world.options.open_springleaf_path.value)

    if world.options.randomize_key_items:
        set_rule(multiworld.get_location(*item("Gold Moonlit Dust")), 
                 lambda state: state.has(*item("Crescent Moonflower")) or 
                 (state.has(*item("Spiral Shell")) and
                  (state.has(*item("Sacred Anemone")) or
                   state.has(*item("Perfect Chime")))))
    set_rule(multiworld.get_location(*item("Lunar Attunement")),
             lambda state:
             not world.options.randomize_key_items.value or
             (state.has(*item("Gold Moonlit Dust")) and
             state.has(*item("Silver Moonlit Dust"))))
    set_rule(multiworld.get_location(*item("Magic Blade")), lambda state: state.has(*item("Awakened Sacred Leaf")) or world.options.open_springleaf_path.value)

    if world.options.oracle_sigil:
        set_rule(multiworld.get_location(*item("Oracle")), 
                 lambda state: state.has(*item("Progressive Lumen Fairy"), 30) if world.options.progressive_lumen_fairies.value else True 
                 or state.can_reach("Fount of Rebirth", "Region", player))
        
    if world.options.progressive_damage_upgrade:
        set_rule(multiworld.get_location(*item("Heavenly Lily - Koho Village")), lambda state: state.has(*item("Crescent Moonflower")) and state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Heavenly Lily 1 - Fairy Village")), 
                 lambda state: state.has(*item("Crescent Moonflower")) or (state.has(*item("Spiral Shell")) and world.options.bell_hover_generation.value))
        set_rule(multiworld.get_location(*item("Heavenly Lily 2 - Ashen Hinterlands")), lambda state: state.has(*item("Crescent Moonflower")) and state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Heavenly Lily 3 - Ashen Hinterlands")), lambda state: state.has(*item("Crescent Moonflower")) and state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Heavenly Lily 3 - Meikan Village")), lambda state: state.can_reach("Fount of Rebirth", "Region", player))
   
    if world.options.progressive_health_upgrade:
        set_rule(multiworld.get_location(*item("Dotted Berry 1 - Lun Tree Roots")), lambda state: state.has(*item("Awakened Sacred Leaf")) or world.options.open_springleaf_path.value)
        set_rule(multiworld.get_location(*item("Dotted Berry 1 - Demon Frontier")), lambda state: state.has(*item("Crescent Moonflower")))
        set_rule(multiworld.get_location(*item("Dotted Berry 2 - Ashen Hinterlands")), lambda state: state.has(*item("Crescent Moonflower")) and (state.has(*item("Spiral Shell"))) or state.has(*item("Lunar Attunement")))
        set_rule(multiworld.get_location(*item("Dotted Berry 3 - Meikan Village")), lambda state: state.can_reach("Fount of Rebirth", "Region", player))
    
    if world.options.progressive_magic_upgrade:
        set_rule(multiworld.get_location(*item("Lun Berry - Koho Village")), lambda state: state.has(*item("Crescent Moonflower")) or state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lun Berry - Springleaf Path")), lambda state: world.options.open_springleaf_path.value or state.has(*item("Awakened Sacred Leaf")) or state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lun Berry - Lun Tree Roots")), lambda state: state.has(*item("Awakened Sacred Leaf")) or world.options.open_springleaf_path.value)
        set_rule(multiworld.get_location(*item("Lun Berry - Ashen Hinterlands")), lambda state: state.has(*item("Crescent Moonflower")) and state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lun Berry - Demon Frontier")), lambda state: state.has(*item("Crescent Moonflower")) and state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lun Berry - Fount of Rebirth")), lambda state: state.can_reach("Selin", "Region", player))
    
    if world.options.progressive_stamina_upgrade:
        set_rule(multiworld.get_location(*item("Peach - Ashen Hinterlands")), lambda state: state.has(*item("Lunar Attunement")))
        set_rule(multiworld.get_location(*item("Peach - Springleaf Path")), lambda state: (world.options.open_springleaf_path.value or state.has(*item("Awakened Sacred Leaf"))))
    
    if world.options.progressive_lumen_fairies:
        set_rule(multiworld.get_location(*item("Lumen Fairy 2 - Springleaf Path")), lambda state: (world.options.open_springleaf_path.value or state.has(*item("Awakened Sacred Leaf"))) and (state.has(*item("Crescent Moonflower")) or state.has(*item("Spiral Shell"))))
        set_rule(multiworld.get_location(*item("Lumen Fairy 4 - Lun Tree Roots")), lambda state: world.options.bell_hover_generation.value or state.has(*item("Crescent Moonflower")) or state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lumen Fairy - Moonlight Repose")), lambda state: state.has(*item("Crescent Moonflower")))
        set_rule(multiworld.get_location(*item("Lumen Fairy 5 - Lun Tree Roots")), lambda state: state.has(*item("Crescent Moonflower")) or (state.has(*item("Spiral Shell")) and (state.has(*item("Sacred Anemone")) or state.has(*item("Perfect Chime")))))
        set_rule(multiworld.get_location(*item("Lumen Fairy 1 - Fairy Springs")), lambda state: state.has(*item("Crescent Moonflower")) or (world.options.bell_hover_generation.value and ((state.has(*item("Sacred Anemone")) or state.has(*item("Perfect Chime"))))))
        set_rule(multiworld.get_location(*item("Lumen Fairy 2 - Fairy Springs")), lambda state: state.has(*item("Crescent Moonflower")) or (state.has(*item("Spiral Shell"))))
        set_rule(multiworld.get_location(*item("Lumen Fairy 3 - Fairy Springs")), lambda state: world.options.bell_hover_generation.value or state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lumen Fairy 4 - Fairy Springs")), lambda state: state.has(*item("Crescent Moonflower")))
        set_rule(multiworld.get_location(*item("Lumen Fairy - Fairy Village")), lambda state: state.has(*item("Crescent Moonflower")) or (state.has(*item("Spiral Shell")) and world.options.bell_hover_generation.value))
        set_rule(multiworld.get_location(*item("Lumen Fairy 4 - Demon Frontier")), lambda state: state.has(*item("Crescent Moonflower")))
        set_rule(multiworld.get_location(*item("Lumen Fairy 5 - Demon Frontier")), lambda state: state.can_reach("Ashen Hinterlands", "Region", player) and (state.has(*item("Crescent Moonflower")) or state.has(*item("The Blessed"))))
        set_rule(multiworld.get_location(*item("Lumen Fairy 5 - Ashen Hinterlands")), lambda state: state.has(*item("Spiral Shell")))
        set_rule(multiworld.get_location(*item("Lumen Fairy 4 - Springleaf Path")), lambda state: state.has(*item("Crescent Moonflower")) or state.has(*item("Spiral Shell")))

def set_completion_rules(world: "MomodoraWorld"):
    player = world.player
    multiworld = world.multiworld
    multiworld.completion_condition[player] = lambda state: state.can_reach("Dora", "Region", player)
    