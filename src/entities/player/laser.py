import pygame
import math
from config.settings import *
from utils.loader import AssetLoader
from config.player_config import LASER_CONFIG

class Laser:
    def __init__(self, x, y, angle, piercing=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = LASER_CONFIG['speed']
        self.size = LASER_CONFIG['size']
        self.piercing = piercing  # Add piercing attribute

        self.original_image = AssetLoader.load_image('laser.png', self.size)
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
        margin = self.size  # How far past the border before we remove the laser
        return (self.x < BORDER_SIZE - margin or
                self.x > WINDOW_W - BORDER_SIZE + margin or
                self.y < BORDER_SIZE - margin or
                self.y > WINDOW_H - BORDER_SIZE + margin)