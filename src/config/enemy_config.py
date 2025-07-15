from .settings import *

# Enemy-specific configurations
ENEMY_CONFIGS = {
    'enemy1': {
        'size': ENEMY1_SIZE,
        'speed': ENEMY1_SPEED,
        'health': ENEMY1_HEALTH,
        'value': ENEMY1_VALUE,
        'explosion_color': ENEMY1_COLOR
    },
    'enemy2': {
        'size': ENEMY2_SIZE,
        'speed': ENEMY2_SPEED,
        'health': ENEMY2_HEALTH,
        'value': ENEMY2_VALUE,
        'explosion_color': ENEMY2_COLOR,
        'zigzag_period': ENEMY2_ZIGZAG_TIMER
    },
    'enemy3': {
        'size': ENEMY3_SIZE,
        'speed': ENEMY3_SPEED,
        'health': ENEMY3_HEALTH,
        'value': ENEMY3_VALUE,
        'explosion_color': ENEMY3_COLOR,
        'shoot_delay': ENEMY3_SHOOT_DELAY
    },
    'enemy4': {
        'size': ENEMY4_SIZE,
        'speed': ENEMY4_SPEED,
        'health': ENEMY4_HEALTH,
        'value': ENEMY4_VALUE,
        'explosion_color': ENEMY4_COLOR,
        'dash_cooldown': ENEMY4_DASH_COOLDOWN,
        'dash_duration': ENEMY4_DASH_DURATION,
        'dash_speed': ENEMY4_DASH_SPEED
    },
    'enemy5': {
        'size': ENEMY5_SIZE,
        'speed': ENEMY5_SPEED,
        'health': ENEMY5_HEALTH,
        'value': ENEMY5_VALUE,
        'explosion_color': ENEMY5_COLOR,
        'shoot_delay': ENEMY5_SHOOT_DELAY,
        'spread_angles': [-15, 0, 15]
    }
}

# Wave configuration
WAVE_CONFIGS = {
    1: [(1, 100)],                          # Wave 1: Only Enemy1
    2: [(1, 70), (2, 30)],                  # Wave 2: Enemy1 & Enemy2
    3: [(1, 50), (2, 30), (3, 20)],        # Wave 3: Enemy1, 2 & 3
    4: [(1, 40), (2, 25), (3, 20), (4, 15)], # Wave 4: Enemy1-4
    5: [(1, 30), (2, 25), (3, 20), (4, 15), (5, 10)]  # Wave 5: All enemies
}
