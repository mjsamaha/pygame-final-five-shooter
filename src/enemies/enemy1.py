import pygame
import math
from .base_enemy import BaseEnemy  # Changed back to relative import
from loader import AssetLoader


class Enemy1(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 35  # Adjust size as needed for your enemy1.png
        self.speed = 3  # Slightly faster than base enemy
        self.health = 100
        self.value = 15  # Worth more points than base enemy

        # Load and scale enemy image
        self.image = AssetLoader.load_image('enemy1.png', self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self, screen):
        """Override draw method to use sprite without rotation"""
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        # Draw the enemy
        screen.blit(self.image, self.rect)

    def update(self, player_x, player_y):
        """Just use basic movement without rotation"""
        super().update(player_x, player_y)


