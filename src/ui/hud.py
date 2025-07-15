# continuously displays score, curr level, remaining enemies, indicators..

import pygame
from config.settings import *


# TODO: upgrade visual hud
# TODO: pixel art HUD components?

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # Default Pygame font, size 36

    def draw(self, screen, score, wave_number, enemies_remaining):
        # Draw score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw wave number
        wave_text = self.font.render(f"Wave: {wave_number}", True, WHITE)
        screen.blit(wave_text, (10, 50))

        # Draw enemies remaining
        enemies_text = self.font.render(f"Enemies: {enemies_remaining}", True, WHITE)
        screen.blit(enemies_text, (10, 90))
