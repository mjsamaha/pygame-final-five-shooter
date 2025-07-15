from entities.enemies.base_enemy import BaseEnemy
from entities.enemies.behaviors import ShootingBehavior
from entities.enemies.enemy_laser import EnemyLaser
from utils.loader import AssetLoader
from config.enemy_config import ENEMY_CONFIGS

class Enemy3(BaseEnemy, ShootingBehavior):
    def __init__(self, x, y):
        super().__init__(x, y)
        config = ENEMY_CONFIGS['enemy3']
        self.size = config['size']
        self.speed = config['speed']
        self.health = config['health']
        self.value = config['value']
        self.explosion_color = config['explosion_color']

        self.image = AssetLoader.load_image('enemy3.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.init_shooting(shoot_delay=config['shoot_delay'])

    def shoot(self, player_x, player_y):
        laser = EnemyLaser(
            self.x + self.size / 2,
            self.y + self.size / 2,
            player_x,
            player_y,
            color=self.explosion_color
        )
        self.lasers.append(laser)

    def update(self, player_x, player_y):
        super().update(player_x, player_y)
        self.update_shooting(player_x, player_y)

    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)
        self.draw_lasers(screen)