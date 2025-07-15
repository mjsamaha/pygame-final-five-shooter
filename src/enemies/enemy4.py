import pygame
import random
from .base_enemy import BaseEnemy
from loader import AssetLoader


class Enemy4(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 45
        self.speed = 4
        self.health = 150
        self.value = 45
        self.explosion_color = (255, 11, 234)  # Red explosion

        self.image = AssetLoader.load_image('enemy4.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Dash attack
        self.dash_cooldown = 180
        self.dash_timer = self.dash_cooldown
        self.is_dashing = False
        self.dash_speed = 8

    def draw(self, screen):
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        # Draw the enemy image
        screen.blit(self.image, self.rect)


    def update(self, player_x, player_y):
        if self.is_dashing:
            # Continue dash movement
            super().move(player_x, player_y)
            self.speed = self.dash_speed
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.speed = 3.5
                self.dash_timer = self.dash_cooldown
        else:
            super().update(player_x, player_y)
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = True
                self.dash_timer = 30  # Dash duration
