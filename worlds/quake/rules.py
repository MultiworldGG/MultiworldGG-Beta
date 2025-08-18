import math
from typing import TYPE_CHECKING, Callable, Union

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import Q1World


class Rule(object):
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other: "Rule") -> "Rule":
        # short circuit
        if isinstance(other, RuleTrue):
            return other
        if isinstance(other, RuleFalse):
            return self
        return LambdaRule(lambda state: self(state) or other(state))

    def __and__(self, other: "Rule") -> "Rule":
        # short circuit
        if isinstance(other, RuleTrue):
            return self
        if isinstance(other, RuleFalse):
            return other
        return LambdaRule(lambda state: self(state) and other(state))


RULETYPE = Union[Rule, Callable[[CollectionState], bool]]


class LambdaRule(Rule):
    def __init__(self, func):
        self._func = func

    def __call__(self, state: dict) -> bool:
        return self._func(state)


class RuleTrue(Rule):
    def __call__(self, state: CollectionState) -> bool:
        return True

    def __or__(self, other: "Rule") -> "Rule":
        return self

    def __and__(self, other: "Rule") -> "Rule":
        return other


class RuleFalse(Rule):
    def __call__(self, state: CollectionState) -> bool:
        return False

    def __or__(self, other: "Rule") -> "Rule":
        return other

    def __and__(self, other: "Rule") -> "Rule":
        return self


class Rules(object):
    def __init__(self, world: "Q1World"):
        player = world.player

        self.true = RuleTrue()
        self.false = RuleFalse()

        class HasRule(Rule):
            def __init__(self, prop: str):
                self.prop = prop

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has(self.prop, player)

        self.has = HasRule

        class HasGroupRule(Rule):
            def __init__(self, prop: str):
                self.prop = prop

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has_group(self.prop, player)

        self.has_group = HasGroupRule

        class CountRule(Rule):
            def __init__(self, prop: str, count: int):
                self.prop = prop
                self.count = count

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has(self.prop, player, self.count)

        self.count = CountRule

        class CountGroupRule(Rule):
            def __init__(self, prop: str, count: int):
                self.prop = prop
                self.count = count

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has_group(self.prop, player, self.count)

        self.count_group = CountGroupRule

        class CanBP(Rule):
            def __init__(self, uses: int):
                self.uses = uses

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Backpack", player, self.uses)

        self.backpack = CanBP

        class CanQuadDmg(Rule):
            def __init__(self, uses: int):
                self.uses = uses

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Quad Damage", player, self.uses)

        self.quad_dmg = CanQuadDmg

        class CanBiosuit(Rule):
            def __init__(self, uses: int):
                self.uses = uses

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Biosuit", player, self.uses)

        self.biosuit = CanBiosuit

        class CanHeal(Rule):
            def __init__(self, amount_req: int):
                self.amount_req = amount_req
                self.amount = 0
                self.factor = world.DIFF_TO_FACTOR_MAPPING.get(world.options.difficulty)

            def __call__(self, state: CollectionState) -> bool:
                self.amount = (
                    state.count("Small Medkit", player) * 15 * self.factor
                    + state.count("Large Medkit", player) * 25 * self.factor
                    + state.count("Megahealth", player) * 100 * self.factor
                )
                # TODO: Work on health% generation for more precise total values
                # print("HP required:", self.amount_req, "amount:", self.amount)

                # TODO: Fix this hack
                # self.heal() does not work in UT
                # if "ut" in world.slot_data:
                #    return 1
                return self.amount > self.amount_req

        self.heal = CanHeal

        class CanInvuln(Rule):
            def __init__(self, uses: int):
                self.uses = uses

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Invulnerability", player, self.uses)

        self.invuln = CanInvuln

        if world.options.unlock_abilities:
            self.can_jump = HasRule("Jump")
            self.can_dive = HasRule("Dive")
            if world.options.basegame == world.options.basegame.option_rogue:
                self.can_rj = HasRule("Rocket Jump") & (
                    HasGroupRule("Rocket Launcher") & self.heal(100)
                )
            else:
                self.can_rj = (
                    HasRule("Rocket Jump")
                    & self.heal(100)
                    & HasGroupRule("Rocket Launcher")
                )
            if world.options.basegame == world.options.basegame.option_hipnotic:
                self.can_gj = (
                    HasRule("Grenade Jump")
                    & self.heal(100)
                    & (HasGroupRule("Grenade Launcher") | HasGroupRule("Proximity Gun"))
                )
            else:
                self.can_gj = (
                    HasRule("Grenade Jump")
                    & self.heal(100)
                    & HasGroupRule("Grenade Launcher")
                )
            self.can_run = HasRule("Run")
        else:
            self.can_jump = self.true
            self.can_dive = self.true
            self.can_rj = self.true
            self.can_gj = self.true
            self.can_run = self.true

        if world.options.unlock_interact:
            self.can_door = HasRule("Door")
            self.can_button = HasRule("Button")
            self.can_shootswitch = HasRule("Shoot Switch")
        else:
            self.can_door = self.true
            self.can_button = self.true
            self.can_shootswitch = self.true

        if world.options.damage_remover_abilities:
            self.can_remove_grenadedmg = HasRule("Grenade Damage Remover")
            self.can_remove_rocketdmg = HasRule("Rocket Damage Remover")
        else:
            self.can_remove_grenadedmg = self.false
            self.can_remove_rocketdmg = self.false

        # TODO: Maybe repurpose this for consumables like quad_dmg instead of the the approach above
        self.explosives = self.has_group("Explosives")
        self.explosives_count = lambda count: self.count_group("Explosives", count)

        self.jump = self.can_jump | self.can_rj | self.can_gj
        """Any singular rj/gj, otherwise health/medkit amount needs to be checked"""

        difficulty_map = {"easy": 0, "medium": 1, "hard": 2, "extreme": 3}
        self.difficulty = lambda difficulty: (
            self.true
            if difficulty_map.get(difficulty, 0) <= world.options.logic_difficulty
            else self.false
        )

        self.bigjump = (self.can_rj | self.can_gj) & (
            self.can_jump
            | (self.difficulty("extreme") & self.quad_dmg(1) & self.invuln(1))
        )
        """ RJ/GJ boosted with a regular jump or powerups"""

        self.bigjump_hard = self.bigjump & self.difficulty("hard")

        skill_map = {"easy": 0, "medium": 1, "hard": 2, "nightmare": 3}
        self.skill_lt = lambda skill: (
            self.true
            if skill_map.get(skill, 0) <= world.options.skill_level
            else self.false
        )
        self.skill_gt = lambda skill: (
            self.true
            if skill_map.get(skill, 0) >= world.options.skill_level
            else self.false
        )
        self.skill_eq = lambda skill: (
            self.true
            if skill_map.get(skill, 0) == world.options.skill_level
            else self.false
        )

        # TODO: Fix this
        # self.heal() does not work in UT

        # helper for difficult grenade jumps (it's almost all of them)
        self.can_gj_ez = self.can_gj & self.difficulty("easy")
        self.can_gj_med = self.can_gj & self.difficulty("medium")
        self.can_gj_hard = self.can_gj & self.difficulty("hard")
        self.can_gj_extr = self.can_gj & self.difficulty("extreme")
        # helper for difficult rocket jumps (most of them are hard difficulty)
        self.can_rj_ez = self.can_rj & self.difficulty("easy")
        self.can_rj_med = self.can_rj & self.difficulty("medium")
        self.can_rj_hard = self.can_rj & self.difficulty("hard")
        self.can_rj_extr = self.can_rj & self.difficulty("extreme")

        # Some simplifications for progressive items
        self.ssg = self.has_group("Super Shotgun")
        self.nailgun = self.has_group("Nailgun")
        self.supernailgun = self.has_group("Super Nailgun")
        self.grenadelauncher = self.has_group("Grenade Launcher")
        self.rocketlauncher = self.has_group("Rocket Launcher")
        self.thunderbolt = self.has_group("Thunderbolt")
        # hipnotic
        self.proximitygun = self.has_group("Proximity Gun")
        self.lasercannon = self.has_group("Laser Cannon")
        # rogue
        # self.multigrenadelauncher = self.has_group("Multi-Grenade Upgrade")
        # self.multirocketlauncher = self.has_group("Multi-Rocket Upgrade")
        # self.lavanailgun = self.has_group("Lava Nailgun Upgrade")
        # self.lavasupernailgun = self.has_group("Lava Super Nailgun Upgrade")
        # self.plasmagun = self.has_group("Plasma Gun Upgrade")

        # logic for all kills
        self.has_explosives = (
            self.rocketlauncher | self.grenadelauncher | self.proximitygun
        )
        self.can_gib = self.has_explosives | (
            self.difficulty("hard") & self.quad_dmg(1)
        )

        self.difficult_combat = (
            # Require explosives
            self.has_explosives
            &
            # a powerful weapon
            (self.thunderbolt | self.supernailgun | self.lasercannon)
            &
            # and a less powerful one
            (self.nailgun | self.ssg)
            &
            # one quad
            self.quad_dmg(1)
            &
            # and some backpacks
            self.backpack(5)
        )
        # General Stuff
        self.level = lambda level_cls: HasRule(level_cls.unlock)
