from enum import Enum


class Action(Enum):
    STAND = "s"
    HIT = "h"
    DOUBLE = "d"
    DOUBLE_STAND = "ds"
    SPLIT = "y"
    SURRENDER = "r"
    SURRENDER_SPLIT = "rp"
    SURRENDER_STAND = "rs"
