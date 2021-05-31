import enum


class CoinTypes(enum.Enum):
    GOLD = 0
    SILVER = 1
    BRONZE = 2


class AttackTypes(enum.Enum):
    FIREBALL = 0
    LIGHTING = 1


class PotionVolume(enum.Enum):
    SMALL = 0,
    LESSER = 1,
    MEDIUM = 2,
    GREATER = 3,
    HUGE = 4
