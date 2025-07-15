from entities.enemies.base_enemy import BaseEnemy
from utils.loader import AssetLoader
from config.enemy_config import ENEMY_CONFIGS

class Enemy1(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        config = ENEMY_CONFIGS['enemy1']
        self.size = config['size']
        self.speed = config['speed']
        self.health = config['health']
        self.value = config['value']
        self.explosion_color = config['explosion_color']

        self.image = AssetLoader.load_image('enemy1.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)



