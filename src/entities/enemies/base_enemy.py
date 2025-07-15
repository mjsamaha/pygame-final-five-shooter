# Super class for Enemy
import math
import os
import sys

import pygame

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from config.settings import *


class BaseEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20  # Can be overridden by child classes
        self.color = RED  # Default color, can be overridden
        self.speed = 2  # Base speed, can be overridden
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.health = 100  # Base health, can be overridden
        self.value = 10  # Score value when destroyed
        self.explosion_color = (255, 200, 0)  # Default explosion color

    def move(self, player_x, player_y):
        """Base movement behavior - straight line towards player"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.x += dx
            self.y += dy

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        """Basic drawing method - can be overridden for more complex shapes"""
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, amount):
        """Returns True if enemy is destroyed"""
        self.health -= amount
        return self.health <= 0

    def update(self, player_x, player_y):
        """Main update method called each frame"""
        self.move(player_x, player_y)
