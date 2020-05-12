from enum import Enum, unique

# Used for the names of the transactions. The keys represent the order of naming, for exemple the
# first transaction will be ALPHA, the second BETA...
@unique
class EGreekCharacters(Enum):
    ALPHA = 0
    BETA = 1
    GAMMA = 2
    DELTA = 3
    EPSILON = 4
    ZETA = 5
    ETA = 6
    THETA = 7
    IOTA = 8
    KAPPA = 9
    LAMBDA = 10
    MU = 11
    NU = 12
    KSI = 13
    OMICRON = 14
    PI = 15
    RHO = 16
    SIGMA = 17
    TAU = 18
    UPSILON = 19
    PHI = 20
    KHI = 21
    PSI = 22
    OMEGA = 23

    # this function property allows to bind greek characters to their unicode drawing
    @property
    def __str__(self):
        dic = {EGreekCharacters.ALPHA:u'\u03B1',
               EGreekCharacters.BETA:u'\u03B2',
               EGreekCharacters.GAMMA:u'\u03B3',
               EGreekCharacters.DELTA:u'\u03B4',
               EGreekCharacters.EPSILON:u'\u03B5',
                EGreekCharacters.ZETA:u'\u03B6',
                EGreekCharacters.ETA:u'\u03B7',
                EGreekCharacters.THETA:u'\u03B8',
                EGreekCharacters.IOTA:u'\u03B9',
                EGreekCharacters.KAPPA:u'\u03BA',
                EGreekCharacters.LAMBDA:u'\u03BB',
                EGreekCharacters.MU:u'\u03BC',
                EGreekCharacters.NU:u'\u03BD',
                EGreekCharacters.KSI:u'\u03BE',
                EGreekCharacters.OMICRON:u'\u03BF',
                EGreekCharacters.PI:u'\u03C0',
                EGreekCharacters.RHO:u'\u03C1',
                EGreekCharacters.SIGMA:u'\u03C2',
                EGreekCharacters.TAU:u'\u03C3',
                EGreekCharacters.UPSILON:u'\u03C4',
                EGreekCharacters.PHI:u'\u03C5',
                EGreekCharacters.KHI:u'\u03C6',
                EGreekCharacters.PSI:u'\u03C7'
        }
        return dic[self].encode("utf-8").decode()