UI_COLORS = {
    'primary': (220, 220, 220),    # Soft white
    'secondary': (128, 128, 128),   # Medium gray
    'accent': (255, 165, 0),       # Golden accent
    'background': (15, 15, 15),    # Rich black
    'text': (255, 255, 255),       # Pure white
    'text_secondary': (170, 170, 170), # Light gray
    'button': {
        'normal': (30, 30, 30),    # Dark gray
        'hover': (45, 45, 45),     # Slightly lighter gray
        'pressed': (20, 20, 20),   # Darker gray
        'border': (50, 50, 50),    # Button border color
    }
}

UI_SIZES = {
    'title': 82,          # Larger title
    'subtitle': 36,
    'text': 24,
    'button': {
        'width': 220,     # Slightly wider button
        'height': 60,     # Taller button
        'padding': 20,
        'border_radius': 8, # Subtle rounded corners
        'border_width': 2,  # Border thickness
    }
}

# Game constants
WINDOW_W = 800
WINDOW_H = 600
FPS = 60
TITLE = "Square Shooter Demo"
BORDER_SIZE = 32

# colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# player
PLAYER_SIZE = 35
PLAYER_SPEED = 5
PLAYER_COLOR = WHITE # used for debugging and proto
AIM_SPEED = 1.2

FIRE_RATE = 25

# game
MENU = "MENU"
PLAYING = "PLAYING"
UPGRADE = "UPGRADE"
GAME_OVER = "GAME_OVER"

# Enemy base attributes
ENEMY_BASE_SIZE = 20
ENEMY_BASE_SPEED = 2
ENEMY_BASE_HEALTH = 100
ENEMY_BASE_VALUE = 10

# Enemy specific attributes
ENEMY1_SIZE = 35
ENEMY1_SPEED = 2
ENEMY1_HEALTH = 50
ENEMY1_VALUE = 15

ENEMY2_SIZE = 35
ENEMY2_SPEED = 3
ENEMY2_HEALTH = 75
ENEMY2_VALUE = 25
ENEMY2_ZIGZAG_TIMER = 30

ENEMY3_SIZE = 40
ENEMY3_SPEED = 3.5
ENEMY3_HEALTH = 100
ENEMY3_VALUE = 35
ENEMY3_SHOOT_DELAY = 120

ENEMY4_SIZE = 45
ENEMY4_SPEED = 4
ENEMY4_HEALTH = 150
ENEMY4_VALUE = 45
ENEMY4_DASH_COOLDOWN = 180
ENEMY4_DASH_DURATION = 30
ENEMY4_DASH_SPEED = 8

ENEMY5_SIZE = 55
ENEMY5_SPEED = 5
ENEMY5_HEALTH = 200
ENEMY5_VALUE = 75
ENEMY5_SHOOT_DELAY = 180

# Enemy colors
ENEMY1_COLOR = (255, 0, 0)      # Red
ENEMY2_COLOR = (0, 255, 78)     # Green
ENEMY3_COLOR = (249, 255, 0)    # Yellow
ENEMY4_COLOR = (255, 11, 234)   # Pink
ENEMY5_COLOR = (0, 218, 255)    # Blue

