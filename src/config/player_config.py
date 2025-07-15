"""Configuration file for player properties and upgrades"""
from .settings import *

# Base player configuration
PLAYER_CONFIG = {
    'size': PLAYER_SIZE,
    'speed': PLAYER_SPEED,
    'aim_speed': AIM_SPEED,
    'fire_rate': FIRE_RATE,
    'shot_count': 1,
    'shot_spread': 0,
    'shield_rotation_speed': 3,
    'shield_radius': 50
}

# Upgrade configurations
UPGRADE_CONFIGS = {
    'faster_shooting': {
        'fire_rate_multiplier': 0.75  # 25% faster
    },
    'double_shot': {
        'shot_count': 2,
        'shot_spread': 10
    },
    'triple_shot': {
        'shot_count': 3,
        'shot_spread': 15
    },
    'speed_boost': {
        'speed_multiplier': 1.25  # 25% faster movement
    },
    'laser_spread': {
        'spread_increase': 10  # Increase spread by 10 degrees
    }
}

# Laser configuration
LASER_CONFIG = {
    'size': 15,
    'speed': 15
}