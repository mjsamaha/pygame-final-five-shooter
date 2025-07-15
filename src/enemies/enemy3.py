import pygame
import random
from .base_enemy import BaseEnemy
from loader import AssetLoader
from .enemy_laser import EnemyLaser


class Enemy3(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 40
        self.speed = 3.5  # Slower but shoots
        self.health = 100
        self.value = 35
        self.explosion_color = (249, 255, 0)  # Red explosion

        self.image = AssetLoader.load_image('enemy3.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.shoot_cooldown = 0
        self.shoot_delay = 120  # Frames between shots
        self.lasers = []



    def update(self, player_x, player_y):
        super().update(player_x, player_y)

        # Update shooting
        if self.shoot_cooldown <= 0:
            self.shoot(player_x, player_y)
            self.shoot_cooldown = self.shoot_delay
        else:
            self.shoot_cooldown -= 1

            # Update lasers
            for laser in self.lasers[:]:
                laser.move()
                # Create particle trail if particle system exists
                if hasattr(self, 'particle_system') and self.particle_system:
                    self.particle_system.create_enemy_laser_trail(
                        laser.x,
                        laser.y,
                        laser.color
                    )
                if laser.is_off_screen():
                    self.lasers.remove(laser)

    def shoot(self, player_x, player_y):
        laser = EnemyLaser(
            self.x + self.size / 2,
            self.y + self.size / 2,
            player_x,
            player_y,
            color=self.explosion_color  # Use the same color as explosions
        )
        self.lasers.append(laser)

    def draw(self, screen):
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        # Draw the enemy image
        screen.blit(self.image, self.rect)
        # Draw the lasers
        for laser in self.lasers:
            laser.draw(screen)

