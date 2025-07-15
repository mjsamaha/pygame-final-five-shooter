import pygame
import math
from .laser import Laser
from utils.loader import AssetLoader
from config.settings import *
from config.player_config import PLAYER_CONFIG


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Load configuration
        self.size = PLAYER_CONFIG['size']
        self.speed = PLAYER_CONFIG['speed']
        self.aim_speed = PLAYER_CONFIG['aim_speed']
        self.fire_rate = PLAYER_CONFIG['fire_rate']

        self.target_angle = 0
        self.angle = 0

        # Load image
        self.original_image = AssetLoader.load_image('player.png', self.size, pixel_perfect=True)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x + self.size // 2
        self.rect.centery = y + self.size // 2

        # Shooting attributes
        self.lasers = []
        self.can_shoot = True
        self.shoot_cooldown = 0

        # Upgradeable attributes
        self.shot_count = PLAYER_CONFIG['shot_count']
        self.shot_spread = PLAYER_CONFIG['shot_spread']
        self.piercing_shot = False

        # Shield attributes
        self.has_shield = False
        self.shield_bullets = []
        self.shield_angle = 0
        self.shield_rotation_speed = PLAYER_CONFIG['shield_rotation_speed']
        self.shield_radius = PLAYER_CONFIG['shield_radius']

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

    def shoot(self):
        """Create new laser(s) based on player's shot configuration"""
        from entities.player.laser import Laser  # Import here to avoid circular import

        self.shoot_cooldown = self.fire_rate
        self.can_shoot = False

        # Calculate spread angles
        if self.shot_count > 1:
            angle_between = self.shot_spread / (self.shot_count - 1)
            start_angle = self.angle - self.shot_spread / 2
        else:
            start_angle = self.angle
            angle_between = 0

        # Create lasers
        for i in range(self.shot_count):
            shot_angle = start_angle + (angle_between * i)
            laser = Laser(
                self.x + self.size / 2,
                self.y + self.size / 2,
                shot_angle,
                piercing=self.piercing_shot
            )
            self.lasers.append(laser)

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
