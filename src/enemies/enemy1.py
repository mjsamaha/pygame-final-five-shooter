import pygame
import math
from .base_enemy import BaseEnemy  # Changed back to relative import
from loader import AssetLoader


class Enemy1(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 35  # Adjust size as needed for your enemy1.png
        self.speed = 3  # Slightly faster than base enemy
        self.health = 50
        self.value = 15  # Worth more points than base enemy

        # Load and scale enemy image
        self.original_image = AssetLoader.load_image('enemy1.png', self.size)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        """Override draw method to use sprite instead of rectangle"""
        # Calculate angle to face player
        dx = self.target_x - self.x if hasattr(self, 'target_x') else 0
        dy = self.target_y - self.y if hasattr(self, 'target_y') else 0
        angle = math.degrees(math.atan2(-dy, dx))

        # Rotate image to face player
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        # Keep the rotation centered
        self.rect = self.image.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))

        # Draw the enemy
        screen.blit(self.image, self.rect)

    def update(self, player_x, player_y):
        """Store target coordinates for rotation calculation"""
        self.target_x = player_x
        self.target_y = player_y
        super().update(player_x, player_y)


