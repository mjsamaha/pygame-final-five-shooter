"""Configuration file for game settings"""
from .settings import *

GAME_CONFIG = {
    'window': {
        'width': WINDOW_W,
        'height': WINDOW_H,
        'title': TITLE,
        'fps': FPS,
        'icon_path': 'icon.png'
    },
    'audio': {
        'music': {
            'menu': {
                'path': 'DSSongRager.mp3',
                'volume': 1.0
            },
            'game': {
                'path': 'DSSongRager.mp3',
                'volume': 0.5
            }
        },
        'sounds': {
            'laser': {
                'path': 'laser_shoot.wav',
                'volume': 0.2
            },
            'explosion': {
                'path': 'laser_explosion.wav',
                'volume': 0.5
            }
        }
    },
    'player': {
        'spawn': {
            'x': WINDOW_W // 2 - PLAYER_SIZE // 2,
            'y': WINDOW_H // 2 - PLAYER_SIZE // 2
        }
    },
    'particles': {
        'laser_trail': {
            'chance': 0.8
        }
    }
}