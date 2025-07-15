# when player dies...
import math

import pygame
from config.settings import *
from ui.screens.main_menu_screen import Button  # Reuse the Button class

# TODO: upgrade visual game over screen

class GameOverScreen:
    def __init__(self):
        self.font_large = pygame.font.Font(None, UI_SIZES['title'])
        self.font_small = pygame.font.Font(None, UI_SIZES['subtitle'])

        # Create text elements with shadow effects
        self.game_over_text = self.font_large.render("GAME OVER", True, UI_COLORS['primary'])
        self.game_over_shadow = self.font_large.render("GAME OVER", True, UI_COLORS['secondary'])

        # Position game over text
        self.game_over_rect = self.game_over_text.get_rect(
            center=(WINDOW_W // 2, WINDOW_H // 3))
        self.game_over_shadow_rect = self.game_over_rect.copy()
        self.game_over_shadow_rect.x += 2
        self.game_over_shadow_rect.y += 2

        # Create retry button
        self.retry_button = Button(
            "RETRY",
            UI_SIZES['button']['width'],
            UI_SIZES['button']['height'],
            (WINDOW_W // 2 - UI_SIZES['button']['width'] // 2, WINDOW_H // 2 + 100)
        )

        # Animation
        self.title_offset = 0
        self.animation_speed = 0.3

    def draw(self, screen, score, high_score):
        # Draw background
        screen.fill(UI_COLORS['background'])

        # Animate title
        self.title_offset = (self.title_offset + self.animation_speed) % 360
        offset_y = math.sin(math.radians(self.title_offset)) * 6

        # Draw game over text with shadow
        screen.blit(self.game_over_shadow,
                   (self.game_over_shadow_rect.x, self.game_over_shadow_rect.y + offset_y))
        screen.blit(self.game_over_text,
                   (self.game_over_rect.x, self.game_over_rect.y + offset_y))

        # Draw scores with accent color
        score_text = self.font_small.render(f"Score: {score}", True, UI_COLORS['text'])
        high_score_text = self.font_small.render(f"High Score: {high_score}", True, UI_COLORS['accent'])

        score_rect = score_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 + 40))

        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)

        # Draw button with hover effect
        self.retry_button.hover(pygame.mouse.get_pos())
        self.retry_button.draw(screen)

    def handle_click(self, pos):
        return self.retry_button.check_click(pos)




