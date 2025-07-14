# Player projectile logic
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

class Laser:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.size = 15

        # Load and rotate laser image
        print("Loading laser image...")
        self.original_image = AssetLoader.load_image('laser.png', self.size)
        print(f"Image loaded: {self.original_image}")

        # Rotate the image to match the angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        # update rect position
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return (self.x < -self.size or self.x > WINDOW_W + self.size or
                self.y < -self.size or self.y > WINDOW_H + self.size)
