# GameState, UpgradeTypes, etc..
from enum import Enum

class GameState(Enum):
    MENU = "MENU"
    PLAYING = "PLAYING"
    UPGRADE = "UPGRADE"
    GAME_OVER = "GAME_OVER"

class UpgradeType(Enum):
    DOUBLE_SHOT = "DOUBLE_SHOT"
    FASTER_SHOOTING = "FASTER_SHOOTING"
    PIERCING_SHOT = "PIERCING_SHOT"
    SPEED_BOOST = "SPEED_BOOST"
    LASER_SPREAD = "LASER_SPREAD"