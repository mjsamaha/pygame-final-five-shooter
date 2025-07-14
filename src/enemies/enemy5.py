import pygame
import random
from .base_enemy import BaseEnemy
from loader import AssetLoader
from .enemy_laser import EnemyLaser


class Enemy5(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 55
        self.speed = 5
        self.health = 200
        self.value = 75

        self.image = AssetLoader.load_image('enemy5.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Multi-shot ability
        self.shoot_cooldown = 0
        self.shoot_delay = 180
        self.lasers = []

        # TODO: enemy laser sound


    def update(self, player_x, player_y):
        super().update(player_x, player_y)

        if self.shoot_cooldown <= 0:
            self.shoot_spread(player_x, player_y)
            self.shoot_cooldown = self.shoot_delay
        else:
            self.shoot_cooldown -= 1

        for laser in self.lasers[:]:
            laser.move()
            if laser.is_off_screen():
                self.lasers.remove(laser)

    def shoot_spread(self, player_x, player_y):
        # Shoot 3 lasers in a spread pattern
        angles = [-15, 0, 15]
        for angle in angles:
            laser = EnemyLaser(self.x + self.size / 2, self.y + self.size / 2,
                               player_x + angle, player_y + angle)
            self.lasers.append(laser)
            # if self.laser_sound:
                # self.laser_sound.play()

    def draw(self, screen):
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        # Draw the enemy image
        screen.blit(self.image, self.rect)
        # Draw the lasers
        for laser in self.lasers:
            laser.draw(screen)
