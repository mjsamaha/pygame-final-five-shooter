import pygame
import math
from loader import AssetLoader


class EnemyLaser:
    def __init__(self, x, y, target_x, target_y, color=(255, 0, 0), speed=8):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 15
        self.color = color

        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = (dx / distance) * speed if distance > 0 else 0
        self.dy = (dy / distance) * speed if distance > 0 else 0

        # Load and scale enemy laser image
        self.image = AssetLoader.load_image('enemy_laser.png', self.size, pixel_perfect=True)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return (self.x < 0 or self.x > 800 or
                self.y < 0 or self.y > 600)