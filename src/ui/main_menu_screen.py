import pygame
from settings import *
from loader import AssetLoader

class MenuScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 64)
        self.text = self.font.render("Press SPACE to Start", True, WHITE)
        self.text_rect = self.text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))


    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.text, self.text_rect)
