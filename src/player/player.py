# Player movement, shooting, upgrades
# Player movement, shooting, upgrades
import pygame
import math
import os
import sys

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
        self.angle = 0

        # Debug print to check asset loading
        print("Loading player image...")
        self.original_image = AssetLoader.load_image('player.png', self.size)
        print(f"Image loaded: {self.original_image}")

        self.image = self.original_image  # No rotation applied to the image
        self.rect = self.image.get_rect()
        # Update rect position immediately
        self.rect.centerx = x + self.size // 2
        self.rect.centery = y + self.size // 2
        self.lasers = []
        self.shoot_cooldown = 0


    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        # Keep player in bounds
        self.x = max(0, min(self.x, WINDOW_W - self.size))
        self.y = max(0, min(self.y, WINDOW_H - self.size))
        self.rect.x = self.x
        self.rect.y = self.y

    def aim(self, mouse_pos):
        dx = mouse_pos[0] - (self.x + self.size / 2)
        dy = mouse_pos[1] - (self.y + self.size / 2)
        self.angle = math.degrees(math.atan2(-dy, dx))
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

        # Draw aim line: debugging
        # end_pos = (
            # center[0] + math.cos(math.radians(self.angle)) * 20,
            # center[1] - math.sin(math.radians(self.angle)) * 20
        # )
        # pygame.draw.line(screen, WHITE, center, end_pos, 2)

    def update(self):
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1