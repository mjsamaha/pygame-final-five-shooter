import math

import pygame
from config.settings import *
from ui.screens.main_menu_screen import Button  # Reuse the Button class


class UpgradeScreen:
    def __init__(self):
        self.font_large = pygame.font.Font(None, UI_SIZES['title'])
        self.font_medium = pygame.font.Font(None, UI_SIZES['subtitle'])
        self.font_small = pygame.font.Font(None, UI_SIZES['text'])

        # Create title with shadow effect
        self.title = self.font_large.render("Choose Your Upgrade!", True, UI_COLORS['primary'])
        self.title_shadow = self.font_large.render("Choose Your Upgrade!", True, UI_COLORS['secondary'])

        # Position title
        self.title_rect = self.title.get_rect(center=(WINDOW_W // 2, WINDOW_H // 4))
        self.title_shadow_rect = self.title_rect.copy()
        self.title_shadow_rect.x += 2
        self.title_shadow_rect.y += 2

        # Create upgrade buttons
        button_w, button_h = 320, 120  # Larger buttons
        spacing = 60

        self.button1 = Button(
            "",  # Text will be set dynamically
            button_w,
            button_h,
            (WINDOW_W // 2 - button_w - spacing // 2, WINDOW_H // 2 - button_h // 2),
            font_size=UI_SIZES['subtitle']
        )

        self.button2 = Button(
            "",  # Text will be set dynamically
            button_w,
            button_h,
            (WINDOW_W // 2 + spacing // 2, WINDOW_H // 2 - button_h // 2),
            font_size=UI_SIZES['subtitle']
        )

        # Animation
        self.title_offset = 0
        self.animation_speed = 0.3

    def draw(self, screen, upgrade_options):
        # Draw background
        screen.fill(UI_COLORS['background'])

        # Animate title
        self.title_offset = (self.title_offset + self.animation_speed) % 360
        offset_y = math.sin(math.radians(self.title_offset)) * 6

        # Draw title with shadow
        screen.blit(self.title_shadow,
                    (self.title_shadow_rect.x, self.title_shadow_rect.y + offset_y))
        screen.blit(self.title,
                    (self.title_rect.x, self.title_rect.y + offset_y))

        # Draw upgrade buttons
        for i, (upgrade, desc) in enumerate(upgrade_options):
            button = self.button1 if i == 0 else self.button2

            # Update button text
            button.text_surf = self.font_medium.render(
                upgrade.value.replace("_", " "), True, UI_COLORS['text'])
            button.text_rect = button.text_surf.get_rect(
                center=(button.top_rect.centerx, button.top_rect.centery - 15))

            # Draw description below button
            desc_text = self.font_small.render(desc, True, UI_COLORS['text_secondary'])
            desc_rect = desc_text.get_rect(
                center=(button.top_rect.centerx, button.top_rect.bottom + 20))

            # Draw button and description
            button.hover(pygame.mouse.get_pos())
            button.draw(screen)
            screen.blit(desc_text, desc_rect)

    def handle_click(self, pos):
        if self.button1.check_click(pos):
            return 0
        elif self.button2.check_click(pos):
            return 1
        return None

