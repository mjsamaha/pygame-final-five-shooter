# Player movement, shooting, upgrades
# Player movement, shooting, upgrades
import pygame
import math
import os
import sys

from .laser import Laser

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from settings import *
from loader import AssetLoader

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.target_angle = 0
        self.aim_speed = AIM_SPEED # adjust
        self.angle = 0

        # Debug print to check asset loading
        print("Loading player image...")
        self.original_image = AssetLoader.load_image('player.png', self.size, pixel_perfect=True)
        print(f"Image loaded: {self.original_image}")

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x + self.size // 2
        self.rect.centery = y + self.size // 2
        self.lasers = []

        # Modified shooting variables
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.fire_rate = FIRE_RATE  # Make sure this constant is defined in settings.py

        # upgraded attributes
        self.shot_count = 1
        self.shot_spread = 0
        self.has_shield = False
        self.shield_bullets = []
        self.shield_angle = 0
        self.shield_rotation_speed = 3
        self.shield_radius = 50
        self.piercing_shot = False

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        # Keep player in bounds, accounting for borders
        self.x = max(BORDER_SIZE, min(self.x, WINDOW_W - BORDER_SIZE - self.size))
        self.y = max(BORDER_SIZE, min(self.y, WINDOW_H - BORDER_SIZE - self.size))
        self.rect.x = self.x
        self.rect.y = self.y

    def aim(self, mouse_pos):
        # Calculate target angle based on mouse position
        dx = mouse_pos[0] - (self.x + self.size / 2)
        dy = mouse_pos[1] - (self.y + self.size / 2)
        self.target_angle = math.degrees(math.atan2(-dy, dx))

        # Calculate the shortest rotation direction
        diff = self.target_angle - self.angle

        # Normalize the difference to [-180, 180]
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        # Smoothly interpolate the current angle towards the target
        self.angle += diff * self.aim_speed

        # Normalize the current angle to [0, 360]
        self.angle = self.angle % 360

        # Keep the rotation centered
        self.rect = self.image.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))

    def draw(self, screen):
        # Debug prints
        print(f"Player rect: {self.rect}")
        print(f"Player position: ({self.x}, {self.y})")

        # Draw rotated player image
        screen.blit(self.image, self.rect)

        # Draw a reference point at player center (for debugging)
        center = (self.x + self.size / 2, self.y + self.size / 2)
        # pygame.draw.circle(screen, RED, (int(center[0]), int(center[1])), 3)

        # Draw shield bullets
        if self.has_shield:
            for bullet in self.shield_bullets:
                bullet.draw(screen)


        # Draw aim line: debugging
        # end_pos = (
            # center[0] + math.cos(math.radians(self.angle)) * 20,
            # center[1] - math.sin(math.radians(self.angle)) * 20
        # )
        # pygame.draw.line(screen, WHITE, center, end_pos, 2)

    def check_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True

        return False

    def check_shield_collision(self, enemy):
        """Returns True if shield blocks the enemy"""
        if not self.has_shield:
            return False

        for bullet in self.shield_bullets[:]:
            if bullet.rect.colliderect(enemy.rect):
                self.shield_bullets.remove(bullet)
                return True
        return False

    def update(self):
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
                self.can_shoot = False
            else:
                self.can_shoot = True

                # Update shield bullets
                if self.has_shield:
                    self.shield_angle = (self.shield_angle + self.shield_rotation_speed) % 360
                    self._update_shield_positions()

    def _update_shield_positions(self):
        if not self.shield_bullets:
            # Create two shield bullets if they don't exist
            for angle in [0, 180]:
                self.shield_bullets.append(Laser(
                    self.x + self.size/2,
                    self.y + self.size/2,
                    angle
                ))

        # Update shield bullet positions
        for i, bullet in enumerate(self.shield_bullets):
            angle = self.shield_angle + (i * 180)  # Space bullets 180 degrees apart
            bullet.x = (self.x + self.size/2 +
                       math.cos(math.radians(angle)) * self.shield_radius)
            bullet.y = (self.y + self.size/2 +
                       math.sin(math.radians(angle)) * self.shield_radius)
            bullet.rect.center = (bullet.x, bullet.y)
