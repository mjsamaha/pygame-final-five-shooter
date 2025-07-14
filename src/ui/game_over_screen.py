# when player dies...
import pygame
from settings import *

class GameOverScreen:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.retry_button_rect = pygame.Rect(WINDOW_W // 2 - 100, WINDOW_H // 2 + 50, 200, 50)

    def draw(self, screen, score, high_score):
        # Draw game over text
        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Draw score
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))
        screen.blit(score_text, score_rect)

        # Draw high score
        high_score_text = self.font_small.render(f"High Score: {high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 + 30))
        screen.blit(high_score_text, high_score_rect)

        # Draw retry button
        pygame.draw.rect(screen, WHITE, self.retry_button_rect, 2)
        retry_text = self.font_small.render("Retry", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=self.retry_button_rect.center)
        screen.blit(retry_text, retry_text_rect)

    def handle_click(self, pos):
        return self.retry_button_rect.collidepoint(pos)



