import math
import pygame
from config.settings import *


class Button:
    def __init__(self, text, width, height, pos, font_size=32):
        self.pressed = False
        self.elevation = 4  # Reduced elevation for subtlety
        self.dynamic_elevation = 4
        self.original_y_pos = pos[1]

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.original_top_rect = self.top_rect.copy()

        # Bottom rectangle (shadow)
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_rect.y += self.elevation

        # Text
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, UI_COLORS['text'])
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.color = UI_COLORS['button']['normal']
        self.border_color = UI_COLORS['button']['border']

    def draw(self, screen):
        # Update positions
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # Draw shadow
        pygame.draw.rect(screen, (0, 0, 0), self.bottom_rect,
                         border_radius=UI_SIZES['button']['border_radius'])

        # Draw main button
        pygame.draw.rect(screen, self.color, self.top_rect,
                         border_radius=UI_SIZES['button']['border_radius'])

        # Draw border
        pygame.draw.rect(screen, self.border_color, self.top_rect,
                         UI_SIZES['button']['border_width'],
                         border_radius=UI_SIZES['button']['border_radius'])

        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, mouse_pos):
        if self.top_rect.collidepoint(mouse_pos):
            self.color = UI_COLORS['button']['pressed']
            self.dynamic_elevation = 0
            return True
        return False

    def hover(self, mouse_pos):
        if self.top_rect.collidepoint(mouse_pos):
            self.color = UI_COLORS['button']['hover']
            self.dynamic_elevation = 2  # Slightly raise button
            self.border_color = UI_COLORS['accent']  # Highlight border on hover
        else:
            self.color = UI_COLORS['button']['normal']
            self.dynamic_elevation = self.elevation
            self.border_color = UI_COLORS['button']['border']


class MenuScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, UI_SIZES['title'])
        self.subtitle_font = pygame.font.Font(None, UI_SIZES['subtitle'])

        # Create title with shadow effect
        self.title = self.title_font.render("SQUARE", True, UI_COLORS['primary'])
        self.title_shadow = self.title_font.render("SQUARE", True, UI_COLORS['secondary'])
        self.title2 = self.title_font.render("SHOOTER", True, UI_COLORS['accent'])
        self.title2_shadow = self.title_font.render("SHOOTER", True, UI_COLORS['secondary'])

        self.subtitle = self.subtitle_font.render("Survive the Geometric Invasion",
                                                  True, UI_COLORS['text_secondary'])

        # Position elements
        self.title_rect = self.title.get_rect(centerx=WINDOW_W // 2, centery=WINDOW_H // 3)
        self.title2_rect = self.title2.get_rect(centerx=WINDOW_W // 2,
                                                centery=self.title_rect.bottom + 10)
        self.subtitle_rect = self.subtitle.get_rect(centerx=WINDOW_W // 2,
                                                    centery=self.title2_rect.bottom + 40)

        # Create shadow rects (offset by 2 pixels)
        self.title_shadow_rect = self.title_rect.copy()
        self.title_shadow_rect.x += 2
        self.title_shadow_rect.y += 2
        self.title2_shadow_rect = self.title2_rect.copy()
        self.title2_shadow_rect.x += 2
        self.title2_shadow_rect.y += 2

        # Create play button
        button_y = self.subtitle_rect.bottom + 60
        self.play_button = Button(
            "PLAY",
            UI_SIZES['button']['width'],
            UI_SIZES['button']['height'],
            (WINDOW_W // 2 - UI_SIZES['button']['width'] // 2, button_y)
        )

        # Animation
        self.title_offset = 0
        self.animation_speed = 0.3  # Slower, more subtle animation

    def draw(self, screen):
        # Draw background
        screen.fill(UI_COLORS['background'])

        # Calculate animation offset
        self.title_offset = (self.title_offset + self.animation_speed) % 360
        offset_y = math.sin(math.radians(self.title_offset)) * 6  # Reduced bounce

        # Draw title shadows first
        screen.blit(self.title_shadow,
                    (self.title_shadow_rect.x, self.title_shadow_rect.y + offset_y))
        screen.blit(self.title2_shadow,
                    (self.title2_shadow_rect.x, self.title2_shadow_rect.y + offset_y))

        # Draw main titles
        screen.blit(self.title, (self.title_rect.x, self.title_rect.y + offset_y))
        screen.blit(self.title2, (self.title2_rect.x, self.title2_rect.y + offset_y))

        # Draw subtitle
        screen.blit(self.subtitle, self.subtitle_rect)

        # Draw button with hover effect
        self.play_button.hover(pygame.mouse.get_pos())
        self.play_button.draw(screen)

