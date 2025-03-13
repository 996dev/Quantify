from enum import Enum


class Direction(Enum):
    """
    BUY：多头

    SELL：空头
    """
    BUY = "BUY"
    SELL = "SELL"


class Offset(Enum):
    """
    OPEN：开仓

    CLOSE：平仓

    CLOSETODAY:上期所和上期能源分平今 / 平昨, 平今用 "CLOSETODAY", 平昨用"CLOSE"

    """
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    CLOSETODAY = "CLOSETODAY"
