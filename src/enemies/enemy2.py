import pygame
from .base_enemy import BaseEnemy
from loader import AssetLoader

class Enemy2(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 35
        self.speed = 3  # Faster than Enemy1
        self.health = 75  # More health
        self.value = 25

        self.image = AssetLoader.load_image('enemy2.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Zigzag movement
        self.zigzag_timer = 0
        self.zigzag_direction = 1

    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        # draw enemy
        screen.blit(self.image, self.rect)

    def update(self, player_x, player_y):
        super().update(player_x, player_y)
        # Add zigzag movement
        self.zigzag_timer += 1
        if self.zigzag_timer >= 30:
            self.zigzag_direction *= -1
            self.zigzag_timer = 0
            self.x += self.zigzag_direction * 2