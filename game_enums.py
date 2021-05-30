import enum


class CoinTypes(enum.Enum):
    GOLD = 0
    SILVER = 1
    BRONZE = 2


class PlayerBarTypes(enum.Enum):
    HEALTH = 0
    MANA = 1


class AttackTypes(enum.Enum):
    FIREBALL = 0
    LIGHTING = 1
