import pygame
from config.settings import *


class UpgradeScreen:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # Upgrade option buttons
        button_w, button_h = 300, 100
        spacing = 50
        self.button1_rect = pygame.Rect(WINDOW_W // 2 - button_w - spacing // 2,
                                        WINDOW_H // 2 - button_h // 2,
                                        button_w, button_h)
        self.button2_rect = pygame.Rect(WINDOW_W // 2 + spacing // 2,
                                        WINDOW_H // 2 - button_h // 2,
                                        button_w, button_h)

    def draw(self, screen, upgrade_options):
        # Draw title
        title = self.font_large.render("Choose Your Upgrade!", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_W // 2, WINDOW_H // 4))
        screen.blit(title, title_rect)

        # Draw upgrade buttons
        for i, (upgrade, desc) in enumerate(upgrade_options):
            button_rect = self.button1_rect if i == 0 else self.button2_rect

            # Draw button background
            pygame.draw.rect(screen, WHITE, button_rect, 2)

            # Draw upgrade name
            name_text = self.font_medium.render(upgrade.value.replace("_", " "), True, WHITE)
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.centery - 15))
            screen.blit(name_text, name_rect)

            # Draw description
            desc_text = self.font_small.render(desc, True, WHITE)
            desc_rect = desc_text.get_rect(center=(button_rect.centerx, button_rect.centery + 15))
            screen.blit(desc_text, desc_rect)

    def handle_click(self, pos):
        if self.button1_rect.collidepoint(pos):
            return 0
        elif self.button2_rect.collidepoint(pos):
            return 1
        return None
