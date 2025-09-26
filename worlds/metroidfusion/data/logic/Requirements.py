from typing import TYPE_CHECKING

from .Requirement import Requirement
if TYPE_CHECKING:
    from ... import MetroidFusionOptions

level_1_e_tanks = 3
level_2_e_tanks = 5
level_3_e_tanks = 7
level_4_e_tanks = 10

#region Individual Item Requirements
class HasMorph(Requirement):
    items_needed = ["Morph Ball"]

class HasVaria(Requirement):
    items_needed = ["Varia Suit"]

class HasGravity(Requirement):
    items_needed = ["Gravity Suit"]

class HasHiJump(Requirement):
    items_needed = ["Hi-Jump"]

class HasSpaceJump(Requirement):
    items_needed = ["Space Jump"]

class HasSpeedBooster(Requirement):
    items_needed = ["Speed Booster"]

class HasScrewAttack(Requirement):
    items_needed = ["Screw Attack"]

class HasMissile(Requirement):
    items_needed = ["Missile Data"]

class HasChargeBeam(Requirement):
    items_needed = ["Charge Beam"]

class HasWaveBeam(Requirement):
    items_needed = ["Wave Beam"]

#endregion

#region Combined Item Requirements
class CanJumpHigh(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], []),
        Requirement(["Space Jump"], [])
    ]

class CanLavaDive(Requirement):
    items_needed = ["Varia Suit", "Gravity Suit"]

class CanBomb(Requirement):
    items_needed = ["Morph Ball", "Bomb Data"]

class CanPowerBomb(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]

class CanBombOrPowerBomb(Requirement):
    other_requirements = [CanBomb, CanPowerBomb]

class CanPowerBombAndJumpHigh(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanJumpHigh]

class CanBallJump(Requirement):
    items_needed = ["Morph Ball"]
    other_requirements = [
        Requirement(["Bomb Data"], []),
        Requirement(["Hi-Jump"], [])
    ]

class CanBallJumpAndBomb(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], []),
        Requirement(["Hi-Jump"], [CanPowerBomb])
    ]

class CanScrewAttackAndSpaceJump(Requirement):
    items_needed = ["Screw Attack", "Space Jump"]

class CanJumpHighUnderwater(Requirement):
    items_needed = ["Gravity Suit"]
    other_requirements = [CanJumpHigh]

class CanSpeedBoosterUnderwater(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]

class CanFreezeEnemies(Requirement):
    other_requirements = [
        Requirement(["Ice Missile"], [HasMissile]),
        Requirement(["Diffusion Missile"], [HasMissile]),
        Requirement(["Ice Beam"], [])
    ]

class CanActivatePillar(Requirement):
    other_requirements = [CanBombOrPowerBomb, HasWaveBeam]

class CanDiffusionMissile(Requirement):
    items_needed = ["Missile Data", "Diffusion Missile"]

class CanDestroyBombBlocks(Requirement):
    other_requirements = [CanBombOrPowerBomb, HasScrewAttack]

class CanChargedWaveShot(Requirement):
    items_needed = ["Charge Beam", "Wave Beam"]

#endregion

#region Optional Requirements

class CanDoBeginnerShinespark(Requirement):
    items_needed = ["Speed Booster"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.TrickyShinesparksInRegionLogic.value)
                or options.ShinesparkTrickDifficulty.value >= options.ShinesparkTrickDifficulty.option_beginner)

class CanDoAdvancedShinespark(Requirement):
    items_needed = ["Speed Booster"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.TrickyShinesparksInRegionLogic.value)
                or options.ShinesparkTrickDifficulty >= options.ShinesparkTrickDifficulty.option_advanced)

class CanDoSimpleWallJump(Requirement):
    items_needed = []

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner)

class CanDoSimpleWallJumpWithHiJump(Requirement):
    items_needed = ["Hi-Jump"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner)

class CanDoSimpleWallJumpWithScrewAttack(Requirement):
    items_needed = ["Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner)

class CanDoSimpleWallJumpWithHiJumpAndScrewAttack(Requirement):
    items_needed = ["Hi-Jump", "Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner)

class CanDoSimpleWallJumpAndFreezeEnemies(Requirement):
    other_requirements = [CanFreezeEnemies]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner)

class CanDoAdvancedWallJump(Requirement):
    items_needed = []

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced)

class CanDoAdvancedWallJumpWithHiJump(Requirement):
    items_needed = ["Hi-Jump"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced)

class CanDoAdvancedWallJumpWithScrewAttack(Requirement):
    items_needed = ["Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return (bool(options.SimpleWallJumpsInRegionLogic.value)
                or options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced)

class CanFightBossOnAdvanced(Requirement):
    items_needed = ["Missile Data", "Charge Beam"]
    energy_tanks_needed = level_1_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_advanced

class CanFightLategameBossOnAdvanced(Requirement):
    items_needed = ["Missile Data", "Charge Beam", "Super Missile"]
    energy_tanks_needed = level_2_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_advanced

class CanFightBossOnExpert(Requirement):
    items_needed = ["Missile Data", "Charge Beam"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_expert

class SectorHubLevel1KeycardRequirement(Requirement):
    items_needed = ["Level 1 Keycard"]
    energy_tanks_needed = level_1_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        return options.GameMode == options.GameMode.option_vanilla


class SectorHubLevel1And2KeycardRequirement(Requirement):
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]
    energy_tanks_needed = level_2_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        return options.GameMode == options.GameMode.option_vanilla


# endregion

#region Keycard Requirements
class HasKeycard1(Requirement):
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Level 1 Keycard"]

class HasKeycard2(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 2 Keycard"]

class HasKeycard1And2(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]

class HasKeycard3(Requirement):
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Level 3 Keycard"]

class HasKeycard4(Requirement):
    energy_tanks_needed = level_4_e_tanks
    items_needed = ["Level 4 Keycard"]

class Level1KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")

class Level2KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 2 Keycard")

class Level1And2KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")
        self.items_needed.append("Level 2 Keycard")

class Level3KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=7):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 3 Keycard")

class Level4KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=10):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 4 Keycard")
#endregion

#region Enemy Requirements
class CanDefeatSmallGeron(Requirement):
    other_requirements = [
        Requirement(["Missile Data"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatMediumGeron(Requirement):
    other_requirements = [
        Requirement(["Missile Data", "Super Missile"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatLargeGeron(Requirement):
    other_requirements = [
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanBeatToughEnemy(Requirement):
    other_requirements = [HasChargeBeam, HasMissile]

class CanBeatToughEnemyAndJumpHigh(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBeatToughEnemy]),
        Requirement(["Space Jump"], [CanBeatToughEnemy])
    ]

class CanDefeatStabilizer(Requirement):
    other_requirements = [
        Requirement(["Screw Attack"], []),
        Requirement(["Charge Beam"], []),
        Requirement(["Missile Data"], []),
        CanPowerBomb
    ]

class CanDefeatThirdStabilizer(Requirement):
    other_requirements = [
        Requirement(["Screw Attack"], [
            CanDoAdvancedWallJump,
            CanDoSimpleWallJumpWithHiJump
        ]),
        Requirement(["Charge Beam"], []),
        Requirement(["Missile Data"], []),
        CanPowerBomb
    ]

#endregion

#region Boss Requirements
class CanFightBeginnerBoss(Requirement):
    items_needed = ["Missile Data"]

class CanFightBoss(Requirement):
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Missile Data", "Charge Beam"]

class CanFightMidgameBoss(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Super Missile"]
    other_requirements = [CanFightBoss]

class CanFightLateGameBoss(Requirement):
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Plasma Beam", "Space Jump"]
    other_requirements = [CanFightMidgameBoss]

#endregion

#region Individual Location Requirements

#region Sector Hub Individual Requirements
class CanReachAnimals(Requirement):
    items_needed = ["Speed Booster"]
    other_requirements = [
        Requirement(["Hi-Jump"], [CanFreezeEnemies]),
        HasSpaceJump
    ]

class CanReachGenesisSpeedway(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [
        Requirement(["Bomb Data"], [CanDoSimpleWallJump, CanJumpHigh]),
        HasHiJump
    ]

class CanCrossFromReactorToSector2(Requirement):
    items_needed = ["Space Jump", "Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanAccessYakuza(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Wave Beam"], [CanBeatToughEnemy]),
        Requirement(
            ["Morph Ball", "Missile Data", "Diffusion Missile"],
            [CanBeatToughEnemy]
        )
    ]
#endregion

#region Sector 1 Individual Requirements
class CanReachAnimorphs(Requirement):
    other_requirements = [
        # Wave or PB for the crab, Supers for the other two.
        Requirement(["Missile Data", "Super Missile"], [CanChargedWaveShot, CanPowerBomb]),
        # Wave or PB for the crab, Screw Attack for the other two
        Requirement(["Screw Attack"], [CanChargedWaveShot, CanPowerBomb]),
        # Technically don't need Supers with enough of other missiles but we don't have ammo requirements in logic yet.
    ]

class CanAccessWallJumpTutorialWithSpaceJump(Requirement):
    items_needed = ["Space Jump"]
    other_requirements = [CanBallJump]

class CanAccessWallJumpTutorialWithWallJump(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Hi-Jump"], [CanDoSimpleWallJump]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDoSimpleWallJump]),
    ]
#endregion

#region Sector 2 Individual Requirements
class CanReachOasisStorage(Requirement):
    other_requirements = [
        CanPowerBomb,
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Morph Ball", "Screw Attack"], [CanJumpHighUnderwater])
    ]

class CanAccessZazabiSpeedway(Requirement):
    items_needed = ["Space Jump", "Speed Booster", "Screw Attack"]
    other_requirements = [CanFightBoss]

class CanAccessWateringHole(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]
    other_requirements = [
        Requirement(["Charge Beam"], [CanBallJump]),
        Requirement(["Plasma Beam"], [CanBallJump]),
        Requirement(["Missile Data"], [CanBallJump])

    ]

class CanBacktrackToCultivationStation(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ]
#endregion

#region Sector 3 Individual Requirements
class CanAscendBOXRoom(Requirement):
    items_needed = ["Charge Beam", "Missile Data"]
    other_requirements = [CanJumpHigh, CanDoSimpleWallJump]

class CanNavigateLavaMaze(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanLavaDive]

class CanAccessL2SecurityRoom(Requirement):
    items_needed = ["Speed Booster"]
    other_requirements = [CanBallJumpAndBomb]

class CanAccessFieryStorage(Requirement):
    items_needed = ["Varia Suit"]
    other_requirements = [
        CanBeatToughEnemy,
        CanLavaDive,
        CanDoBeginnerShinespark
    ]

class CanAccessFieryStorageUpper(Requirement):
    items_needed = ["Speed Booster"]
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"],[CanActivatePillar, HasSpaceJump]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanActivatePillar, HasSpaceJump]),
        Requirement(["Screw Attack"], [CanActivatePillar, HasSpaceJump]),
    ]

class CanAccessGlassTubeItem(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBomb]),
        CanPowerBomb,
        Requirement(["Screw Attack"], []),
    ]

class CanAccessGarbageChute(Requirement):
    items_needed = ["Screw Attack", "Speed Booster"]
    other_requirements = [
        CanLavaDive
    ]

class CanAccessSector3LowerAlcove(Requirement):
    items_needed = ["Morph Ball"]
    other_requirements = [
        CanBombOrPowerBomb,
        Requirement(["Screw Attack"], [CanActivatePillar, HasSpeedBooster, CanJumpHigh])
    ]
#endregion

#region Sector 4 Individual Requirements
class CanDrainAQA(Requirement):
    items_needed = ["Speed Booster", "Level 1 Keycard"]
    other_requirements = [CanBombOrPowerBomb]

class CanAscendCheddarBay(Requirement):
    items_needed = ["Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanAccessReservoirVault(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump", "Morph Ball", "Bomb Data"], [CanDoSimpleWallJump]),
        Requirement(["Hi-Jump", "Morph Ball", "Power Bomb Data"], [CanDoSimpleWallJump]),
        Requirement(["Space Jump"], [CanBallJumpAndBomb])
    ]

class CanAccessSanctuaryCache(Requirement):
    other_requirements = [
        Requirement(["Wave Beam", "Charge Beam"], [CanDoSimpleWallJump, HasSpaceJump]),
        Requirement(
            ["Wave Beam", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Charge Beam", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
    ]

class CanCrossSector4RightWaterCorner(Requirement):
    items_needed = ["Missile Data", "Morph Ball", "Gravity Suit"]
    other_requirements = [
        CanFreezeEnemies,
        Requirement(["Space Jump"], []),
    ]

class CanCrossSector4LowerSecurityToRightWaterZone(Requirement):
    items_needed = ["Morph Ball", "Level 4 Keycard"]
    other_requirements = [
        Requirement(["Speed Booster"], [CanFreezeEnemies]),
        HasScrewAttack
    ]
    energy_tanks_needed = level_4_e_tanks
#endregion

#region Sector 5 Individual Requirements
class CanEscapeNightmareRoom(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]
    other_requirements = [
        CanFightLateGameBoss, CanFightLategameBossOnAdvanced, CanFightBossOnExpert
    ]

class CanAccessRipperRoad(Requirement):
    items_needed = ["Morph Ball", "Hi-Jump"]
    other_requirements = [
        Requirement(["Bomb Data", "Screw Attack"], [CanFreezeEnemies]),
        Requirement(["Power Bomb Data"], [CanFreezeEnemies]),
    ]

class CanAccessRipperTreasure(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [
        HasSpaceJump,
        Requirement(["Hi-Jump"], [CanFreezeEnemies]),
        Requirement(["Ice Beam"], [CanDoSimpleWallJump]),
        Requirement(["Missile Data", "Ice Missile"], [CanDoSimpleWallJump]),
        Requirement(["Missile Data", "Diffusion Missile"], [CanDoSimpleWallJump])
    ]
#endregion

#region Sector 6 Individual Requirements
#endregion

#endregion

#region Event Requirements
class CanDrainAQARequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Pump Control Activated")
#endregion