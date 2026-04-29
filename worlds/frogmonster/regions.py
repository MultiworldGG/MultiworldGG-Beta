from typing import Dict, NamedTuple, List, Callable

from .names import item_names as i
from .names import region_names as r
from .names import combat_names as c
from .rules_helpers import can_fight, can_fight_all, can_burn

class FrogmonsterRegionData(NamedTuple):
    connects: List[tuple[str, Callable]] = []

nothing = lambda player, dif, state: True

region_data_table: Dict[str, FrogmonsterRegionData] = {
r.lost_swamp: FrogmonsterRegionData(
    connects=[(r.lost_swamp_after_groth, lambda player, dif, state: can_fight(c.groth, player, dif, state))]
),
r.lost_swamp_after_groth: FrogmonsterRegionData(
    connects=[(r.marvins, nothing), 
              (r.lost_swamp, lambda player, dif, state: can_fight(c.groth, player, dif, state))]
),
r.marvins: FrogmonsterRegionData(
    connects=[(r.outskirts, lambda player, dif, state: can_fight(c.marvin, player, dif, state)), 
              (r.yellow_forest_side, lambda player, dif, state: state.has(i.sticky_hands, player))]
),
r.outskirts: FrogmonsterRegionData(
    connects=[(r.very_lost_swamp, lambda player, dif, state: can_fight_all([c.snake, c.outskirts_arena_1], player, dif, state) and state.has(i.sticky_hands, player))]
),
r.very_lost_swamp: FrogmonsterRegionData(
    connects=[(r.yellow_forest, lambda player, dif, state: can_fight(c.yanoy, player, dif, state)),
              (r.outskirts, lambda player, dif, state: can_fight(c.very_lost_swamp_general, player, dif, state))]
),
r.yellow_forest: FrogmonsterRegionData(
    connects=[(r.yellow_forest_town, lambda player, dif, state: can_fight_all([c.limbs, c.yellow_forest_arena_1], player, dif, state)),
              (r.yellow_forest_side, lambda player, dif, state: can_fight(c.yellow_forest_arena_2, player, dif, state)),
              (r.outskirts, nothing)]
),
r.yellow_forest_town: FrogmonsterRegionData(
    connects=[(r.yellow_forest, lambda player, dif, state: can_fight(c.limbs, player, dif, state)),
              (r.green_sea_before, nothing)]
),
r.yellow_forest_side: FrogmonsterRegionData(
    connects=[(r.yellow_forest, lambda player, dif, state: can_fight(c.yellow_forest_arena_2, player, dif, state)),
              (r.marvins, nothing)]
),
r.green_sea_before: FrogmonsterRegionData(
    connects=[(r.yellow_forest_town, nothing),
              (r.green_sea_key, lambda player, dif, state: can_fight(c.green_sea_arena_1, player, dif, state) and state.has(i.key, player, 3)),
              (r.green_sea_after, lambda player, dif, state: can_fight(c.green_sea_arena_1, player, dif, state))]
),
r.green_sea_after: FrogmonsterRegionData(
    connects=[(r.green_sea_before, lambda player, dif, state: can_fight(c.green_sea_arena_1, player, dif, state)),
              (r.green_sea_key, lambda player, dif, state: state.has(i.key, player, 3)),
              (r.city, nothing)]
),
r.green_sea_key: FrogmonsterRegionData(
),
r.city: FrogmonsterRegionData(
    connects=[(r.green_sea_after, nothing),
              (r.under_city, nothing),
              (r.workshop, nothing),
              (r.forest_floor, nothing),
              (r.old_road, nothing),
              (r.runi_arena, lambda player, dif, state: state.has(i.orchus_key, player))]
),
r.workshop: FrogmonsterRegionData(
),
r.old_road: FrogmonsterRegionData(
    connects=[(r.city, nothing),
              (r.hive, lambda player, dif, state: can_fight(c.old_road_general, player, dif, state)),
              (r.old_wood, lambda player, dif, state: can_burn(state, player)),
              (r.estate, lambda player, dif, state: state.has(i.runi_key, player) and can_fight(c.old_road_general, player, dif, state))]
),
r.old_wood: FrogmonsterRegionData(
    connects=[(r.thickness, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.old_wood_arenas, player, dif, state)),
              (r.well, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.old_wood_arenas, player, dif, state) and can_burn(state, player))]
),
r.thickness: FrogmonsterRegionData(
),
r.well: FrogmonsterRegionData(
),
r.estate: FrogmonsterRegionData(
    connects=[(r.fog_garden, lambda player, dif, state: can_fight(c.estate_general, player, dif, state))]
),
r.fog_garden: FrogmonsterRegionData(
    connects=[(r.fog_garden_key, lambda player, dif, state: can_fight_all([c.fog_garden_arena_2, c.fog_garden_arena_1], player, dif, state) and state.has(i.key, player, 3))]
),
r.fog_garden_key: FrogmonsterRegionData(
),
r.under_city: FrogmonsterRegionData(
    connects=[(r.city, nothing),
              (r.under_under_city, lambda player, dif, state: state.has(i.orchus_key, player))]
),
r.forest_floor: FrogmonsterRegionData(
    connects=[(r.city, nothing),
             (r.treetops, lambda player, dif, state: state.has(i.tongue_swing, player) and can_fight(c.forest_floor_general, player, dif, state)),
             (r.cicada_cove, lambda player, dif, state: state.has(i.tongue_swing, player) and can_fight(c.forest_floor_general, player, dif, state)),
             (r.hive, lambda player, dif, state: state.has_all([i.tongue_swing, i.dash], player) and can_fight(c.forest_floor_general, player, dif, state)),]
),
r.treetops: FrogmonsterRegionData(
    connects=[(r.forest_floor, nothing),
              (r.orchus_tree, lambda player, dif, state: state.has(i.wooden_cannon, player) and can_fight(c.treetops_arena_1, player, dif, state)),
              (r.treetops_key, lambda player, dif, state: state.has(i.key, player, 3) and state.has(i.tongue_swing, player) and can_fight(c.treetops_arena_1, player, dif, state))]
),
r.treetops_key: FrogmonsterRegionData(
),
r.cicada_cove: FrogmonsterRegionData(
),
r.hive: FrogmonsterRegionData(
    connects=[(r.forest_floor, lambda player, dif, state: can_fight(c.hive_general, player, dif, state)),
              (r.treetops, lambda player, dif, state: can_fight(c.hive_general, player, dif, state) and state.has_all([i.dash, i.tongue_swing], player)),
              (r.old_road, lambda player, dif, state: can_fight(c.hive_general, player, dif, state)),
              (r.cicada_cove, lambda player, dif, state: False)]  # Falsy connection that can be modified by the parkour rules]
),
r.orchus_tree: FrogmonsterRegionData(
    connects=[(r.runi_arena, lambda player, dif, state: can_fight(c.runi, player, dif, state))]
),
r.runi_arena: FrogmonsterRegionData(
    connects=[(r.under_under_city_lower, lambda player, dif, state: state.has_all([i.dash, i.sticky_hands], player) and can_fight(c.ridge_general, player, dif, state)),
               (r.moridonos, lambda player, dif, state: state.has(i.sticky_hands, player) and can_fight(c.ridge_general, player, dif, state)),
               (r.quarry, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.ridge_general, player, dif, state)),
               (r.myzand, lambda player, dif, state: state.has_group_unique("Gun Upgrade", player, 6))]
),
r.ridge: FrogmonsterRegionData(
    connects=[(r.moridonos, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.ridge_general, player, dif, state)),
              (r.drywood, lambda player, dif, state: state.has(i.tongue_swing, player) and can_fight(c.ridge_general, player, dif, state)),
              (r.quarry, lambda player, dif, state: state.has_all([i.dash, i.sticky_hands], player) and can_fight(c.ridge_general, player, dif, state))]
),
r.moridonos: FrogmonsterRegionData(
    connects=[(r.ridge, lambda player, dif, state: state.has(i.dash, player)),
              (r.runi_arena, lambda player, dif, state: state.has(i.dash, player)),
              (r.moridonos_layer_worm, lambda player, dif, state: (state.has(i.tongue_swing, player) or state.has_all([i.dash, i.cricket], player)) and can_fight(c.moridonos_general, player, dif, state)),
              (r.moridonos_layer_drill, lambda player, dif, state: can_fight(c.moridonos_general, player, dif, state)),
              (r.moridonos_layer_thumper, lambda player, dif, state: can_fight(c.moridonos_general, player, dif, state))]
),
r.moridonos_layer_worm: FrogmonsterRegionData(
    connects=[(r.moridonos, lambda player, dif, state: (state.has(i.tongue_swing, player) or state.has_all([i.dash, i.cricket], player)) and can_fight(c.moridonos_arena_1, player, dif, state)),
              (r.moridonos_warp, lambda player, dif, state: can_fight(c.moridonos_arena_1, player, dif, state))],
),
r.moridonos_layer_drill: FrogmonsterRegionData(
    connects=[(r.moridonos, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_arena_2, player, dif, state)),
              (r.moridonos_warp, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_arena_2, player, dif, state)),
              (r.moridonos_layer_turtle, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_arena_2, player, dif, state))],
),
r.moridonos_layer_thumper: FrogmonsterRegionData(
    connects=[(r.moridono_arena, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_arena_3, player, dif, state)),
              (r.moridonos_layer_drill, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_arena_3, player, dif, state))],
),
r.moridonos_layer_turtle: FrogmonsterRegionData(
    connects=[(r.moridono_arena, lambda player, dif, state: can_fight(c.moridonos_arena_4, player, dif, state)),
              (r.moridonos_layer_thumper, lambda player, dif, state: can_fight(c.moridonos_arena_4, player, dif, state)),
              (r.moridonos_layer_drill, lambda player, dif, state: can_fight(c.moridonos_arena_4, player, dif, state))],
),
r.moridonos_warp: FrogmonsterRegionData(
    connects=[(r.moridonos_layer_worm, lambda player, dif, state: can_fight(c.moridonos_arena_1, player, dif, state)),
              (r.moridonos_layer_drill, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.moridonos_general, player, dif, state)),
              (r.reef, nothing)],
),
r.moridono_arena: FrogmonsterRegionData(
),
r.reef: FrogmonsterRegionData(
    connects=[(r.moridonos_warp, lambda player, dif, state: can_fight(c.reef_arena_1, player, dif, state)),
              (r.krogar_arena, lambda player, dif, state: can_fight(c.reef_arena_1, player, dif, state)),]
),
r.deep: FrogmonsterRegionData(
    connects=[(r.drywood, lambda player, dif, state: state.has(i.tongue_swing, player) and can_fight(c.deep_arena_1, player, dif, state)),
              (r.krogar_arena, lambda player, dif, state: can_fight(c.deep_arena_1, player, dif, state)),]
),
r.krogar_arena: FrogmonsterRegionData(
    connects=[(r.deep, lambda player, dif, state: can_fight(c.krogar, player, dif, state)),
              (r.reef, lambda player, dif, state: can_fight(c.krogar, player, dif, state))]
),
r.drywood: FrogmonsterRegionData(
    connects=[(r.rootden, nothing),
              (r.deep, nothing),
              (r.quarry, nothing),
              (r.ridge, nothing)]
),
r.rootden: FrogmonsterRegionData(
),
r.temple: FrogmonsterRegionData(
    connects=[(r.temple_top, lambda player, dif, state: can_fight_all([c.temple_general, c.door_crab], player, dif, state))]
),
r.temple_top: FrogmonsterRegionData(
),
r.quarry: FrogmonsterRegionData(
    connects=[(r.temple, lambda player, dif, state: can_fight(c.quarry_arena_1, player, dif, state)),
              (r.drywood, lambda player, dif, state: state.has(i.tongue_swing, player)),
              (r.ridge, lambda player, dif, state: state.has_all([i.dash, i.sticky_hands], player) and can_fight(c.ridge_general, player, dif, state)),
              (r.under_under_city_lower, lambda player, dif, state: state.has_all([i.dash, i.sticky_hands], player) and can_fight(c.ridge_general, player, dif, state)),
              (r.runi_arena, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.ridge_general, player, dif, state))]
),
r.under_under_city: FrogmonsterRegionData(
    connects=[(r.under_city, lambda player, dif, state: state.has(i.sticky_hands, player) and can_fight(c.under_under_arena_1, player, dif, state)),
              (r.barge_arena, lambda player, dif, state: can_fight(c.under_under_arena_1, player, dif, state))]
),
r.barge_arena: FrogmonsterRegionData(
    connects=[(r.under_under_city, lambda player, dif, state: state.has(i.sticky_hands, player) and can_fight(c.barge, player, dif, state)),
              (r.under_under_city_lower, lambda player, dif, state: can_fight(c.barge, player, dif, state))]
),
r.under_under_city_lower: FrogmonsterRegionData(
    connects=[(r.barge_arena, lambda player, dif, state: state.has(i.sticky_hands, player) and can_fight(c.under_under_general, player, dif, state)),
              (r.runi_arena, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.under_under_general, player, dif, state)),
              (r.quarry, lambda player, dif, state: state.has(i.dash, player) and can_fight(c.under_under_general, player, dif, state))]
),
r.myzand: FrogmonsterRegionData(
),

r.anywhere: FrogmonsterRegionData(
    connects=[(r.lost_swamp, nothing)]
),
# r.bug: FrogmonsterRegionData(),
 }