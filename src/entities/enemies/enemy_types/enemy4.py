from entities.enemies.base_enemy import BaseEnemy
from entities.enemies.behaviors import DashingBehavior
from utils.loader import AssetLoader
from config.enemy_config import ENEMY_CONFIGS

class Enemy4(BaseEnemy, DashingBehavior):
    def __init__(self, x, y):
        super().__init__(x, y)
        config = ENEMY_CONFIGS['enemy4']
        self.size = config['size']
        self.speed = config['speed']
        self.health = config['health']
        self.value = config['value']
        self.explosion_color = config['explosion_color']

        self.image = AssetLoader.load_image('enemy4.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.init_dashing(
            cooldown=config['dash_cooldown'],
            duration=config['dash_duration'],
            dash_speed=config['dash_speed']
        )

    def update(self, player_x, player_y):
        if self.is_dashing:
            super().move(player_x, player_y)
        else:
            super().update(player_x, player_y)
        self.update_dashing(player_x, player_y)

    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)