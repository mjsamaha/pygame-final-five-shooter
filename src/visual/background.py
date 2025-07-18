import pygame
from config.settings import *
from utils.loader import AssetLoader

class Background:
    def __init__(self):
        # Load border images
        self.top_border = AssetLoader.load_image('top-border.png', pixel_perfect=False)
        self.bottom_border = AssetLoader.load_image('bottom-border.png', pixel_perfect=False)
        self.left_border = AssetLoader.load_image('left-border.png', pixel_perfect=False)
        self.right_border = AssetLoader.load_image('right-border.png', pixel_perfect=False)

        # Scale borders to fit window dimensions
        self.top_border = pygame.transform.scale(self.top_border, (WINDOW_W, BORDER_SIZE))
        self.bottom_border = pygame.transform.scale(self.bottom_border, (WINDOW_W, BORDER_SIZE))
        self.left_border = pygame.transform.scale(self.left_border, (BORDER_SIZE, WINDOW_H))
        self.right_border = pygame.transform.scale(self.right_border, (BORDER_SIZE, WINDOW_H))

    def draw(self, screen):
        # Draw borders
        screen.blit(self.top_border, (0, 0))
        screen.blit(self.bottom_border, (0, WINDOW_H - BORDER_SIZE))
        screen.blit(self.left_border, (0, 0))
        screen.blit(self.right_border, (WINDOW_W - BORDER_SIZE, 0))

