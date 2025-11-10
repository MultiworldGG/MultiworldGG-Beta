import importlib
import os

from ..base_classes import Q1Episode
from .e1m1 import e1m1
from .e1m2 import e1m2
from .e1m3 import e1m3
from .e1m4 import e1m4
from .e1m5 import e1m5
from .e1m6 import e1m6
from .e1m7 import e1m7
from .e1m8 import e1m8
from .e2m1 import e2m1
from .e2m2 import e2m2
from .e2m3 import e2m3
from .e2m4 import e2m4
from .e2m5 import e2m5
from .e2m6 import e2m6
from .e2m7 import e2m7
from .e3m1 import e3m1
from .e3m2 import e3m2
from .e3m3 import e3m3
from .e3m4 import e3m4
from .e3m5 import e3m5
from .e3m6 import e3m6
from .e3m7 import e3m7
from .e4m1 import e4m1
from .e4m2 import e4m2
from .e4m3 import e4m3
from .e4m4 import e4m4
from .e4m5 import e4m5
from .e4m6 import e4m6
from .e4m7 import e4m7
from .e4m8 import e4m8
from .start import start
from .end import end

# hipnotic
from .hip1m1 import hip1m1
from .hip1m2 import hip1m2
from .hip1m3 import hip1m3
from .hip1m4 import hip1m4
from .hip1m5 import hip1m5
from .hip2m1 import hip2m1
from .hip2m2 import hip2m2
from .hip2m3 import hip2m3
from .hip2m4 import hip2m4
from .hip2m5 import hip2m5
from .hip2m6 import hip2m6
from .hip3m1 import hip3m1
from .hip3m2 import hip3m2
from .hip3m3 import hip3m3
from .hip3m4 import hip3m4
from .hipdm1 import hipdm1
from .hipstart import hipstart
from .hipend import hipend

# rogue
from .r1m1 import r1m1
from .r1m2 import r1m2
from .r1m3 import r1m3
from .r1m4 import r1m4
from .r1m5 import r1m5
from .r1m6 import r1m6
from .r1m7 import r1m7
from .r2m1 import r2m1
from .r2m2 import r2m2
from .r2m3 import r2m3
from .r2m4 import r2m4
from .r2m5 import r2m5
from .r2m6 import r2m6
from .r2m7 import r2m7
from .r2m8 import r2m8
from .roguestart import roguestart

# mg1
from .mge1m1 import mge1m1
from .mge1m2 import mge1m2
from .mge1m3 import mge1m3
from .mge2m1 import mge2m1
from .mge2m2 import mge2m2
from .mge3m1 import mge3m1
from .mge3m2 import mge3m2
from .mge4m1 import mge4m1
from .mge4m2 import mge4m2
from .mge5m1 import mge5m1
from .mge5m2 import mge5m2
from .mg1start import mg1start
from .mgend import mgend

# dopa
from .e5m1 import e5m1
from .e5m2 import e5m2
from .e5m3 import e5m3
from .e5m4 import e5m4
from .e5m5 import e5m5
from .e5m6 import e5m6
from .e5m7 import e5m7
from .e5sm1 import e5sm1
from .e5sm2 import e5sm2
from .e5end import e5end
from .dopastart import dopastart


class E1(Q1Episode):
    name = "Doomed Dimension"
    levels = [e1m1(), e1m2(), e1m3(), e1m4(), e1m5(), e1m6(), e1m7(), e1m8()]
    maxlevel = len(levels)


class E2(Q1Episode):
    name = "Realm of Black Magic"
    levels = [e2m1(), e2m2(), e2m3(), e2m4(), e2m5(), e2m6(), e2m7()]
    maxlevel = len(levels)


class E3(Q1Episode):
    name = "Netherworld"
    levels = [e3m1(), e3m2(), e3m3(), e3m4(), e3m5(), e3m6(), e3m7()]
    maxlevel = len(levels)


class E4(Q1Episode):
    name = "The Elder World"
    levels = [e4m1(), e4m2(), e4m3(), e4m4(), e4m5(), e4m6(), e4m7(), e4m8()]
    maxlevel = len(levels)


class SL(Q1Episode):
    name = "Special Levels Quake 1"
    levels = [start(), end()]
    maxlevel = len(levels)


# Hipnotic
class HIPE1(Q1Episode):
    name = "Fortress of the Dead"
    levels = [hip1m1(), hip1m2(), hip1m3(), hip1m4(), hip1m5()]
    maxlevel = len(levels)


class HIPE2(Q1Episode):
    name = "Dominion of Darkness"
    levels = [hip2m1(), hip2m2(), hip2m3(), hip2m4(), hip2m5(), hip2m6()]
    maxlevel = len(levels)


class HIPE3(Q1Episode):
    name = "The Rift"
    levels = [hip3m1(), hip3m2(), hip3m3(), hip3m4(), hipdm1()]
    maxlevel = len(levels)


class HIPSL(Q1Episode):
    name = "Special Levels Hipnotic"
    levels = [hipstart(), hipend()]
    maxlevel = len(levels)


# Rogue
class ROGUEE1(Q1Episode):
    name = "Hell's Fortress"
    levels = [r1m1(), r1m2(), r1m3(), r1m4(), r1m5(), r1m6(), r1m7()]
    maxlevel = len(levels)


class ROGUEE2(Q1Episode):
    name = "The Corridors of Time"
    levels = [r2m1(), r2m2(), r2m3(), r2m4(), r2m5(), r2m6(), r2m7()]
    maxlevel = len(levels)


class ROGUESL(Q1Episode):
    name = "Special Levels Rogue"
    levels = [roguestart(), r2m8()]
    maxlevel = len(levels)


class MG1E1(Q1Episode):
    name = "Realm of the Machinists"
    levels = [mge1m1(), mge1m2(), mge1m3()]
    maxlevel = len(levels)


class MG1E2(Q1Episode):
    name = "Realm of the Blacksmiths"
    levels = [mge2m1(), mge2m2()]
    maxlevel = len(levels)


class MG1E3(Q1Episode):
    name = "Realm of the Stonemasons"
    levels = [mge3m1(), mge3m2()]
    maxlevel = len(levels)


class MG1E4(Q1Episode):
    name = "Realm of the Cultists"
    levels = [mge4m1(), mge4m2()]
    maxlevel = len(levels)


class MG1E5(Q1Episode):
    name = "Realm of the Astrologers"
    levels = [mge5m1(), mge5m2()]
    maxlevel = len(levels)


class MG1SL(Q1Episode):
    name = "Special Levels MG1"
    levels = [mg1start(), mgend()]
    maxlevel = len(levels)


class DOPAE1(Q1Episode):
    name = "Dimension of the Past"
    levels = [e5m1(), e5m2(), e5m3(), e5m4(), e5m5(), e5m6(), e5m7()]
    maxlevel = len(levels)


class DOPASL(Q1Episode):
    name = "Special Levels DOPA"
    levels = [dopastart(), e5end()]
    maxlevel = len(levels)


all_episodes_q1 = [E1(), E2(), E3(), E4()]
all_episodes_hip = [HIPE1(), HIPE2(), HIPE3()]
all_episodes_rogue = [ROGUEE1(), ROGUEE2()]
all_episodes_mg1 = [MG1E1(), MG1E2(), MG1E3(), MG1E4(), MG1E5(), MG1SL()]
all_episodes_dopa = [DOPAE1(), DOPASL()]

all_eps_incl_special = [
    E1(),
    E2(),
    E3(),
    E4(),
    SL(),
    HIPE1(),
    HIPE2(),
    HIPE3(),
    HIPSL(),
    ROGUEE1(),
    ROGUEE2(),
    ROGUESL(),
    MG1E1(),
    MG1E2(),
    MG1E3(),
    MG1E4(),
    MG1E5(),
    MG1SL(),
    DOPAE1(),
    DOPASL(),
]

all_levels_incl_special = [level for ep in all_eps_incl_special for level in ep.levels]
