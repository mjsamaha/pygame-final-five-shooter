# Game loop & state manager
import pygame
from settings import *
from enums import GameState
from player.player import Player
from player.laser import Laser
from src.enemies.enemy_manager import EnemyManager
from src.ui.hud import HUD
from src.score_manager import ScoreManager
from src.background import Background
from src.ui.game_over_screen import GameOverScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING

        self.background = Background()

        self.score_manager = ScoreManager()
        self.hud = HUD()

        self.player = Player(WINDOW_W // 2 - PLAYER_SIZE // 2, WINDOW_H // 2 - PLAYER_SIZE // 2)
        self.enemy_manager = EnemyManager()  # Add this line

        self.game_over_screen = GameOverScreen()
        self.reset_game()

    def reset_game(self):
        self.state = GameState.PLAYING
        self.player = Player(WINDOW_W // 2 - PLAYER_SIZE // 2, WINDOW_H // 2 - PLAYER_SIZE // 2)
        self.enemy_manager = EnemyManager()
        self.score_manager.reset()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.state == GameState.PLAYING:
                        self.shoot_laser()
                    elif self.state == GameState.GAME_OVER:
                        # Check if retry button was clicked
                        if self.game_over_screen.handle_click(event.pos):
                            self.reset_game()

    def shoot_laser(self):
        if self.player.can_shoot:  # Only shoot if cooldown is done
            laser = Laser(
                self.player.x + self.player.size / 2,
                self.player.y + self.player.size / 2,
                self.player.angle
            )
            self.player.lasers.append(laser)
            self.player.shoot_cooldown = FIRE_RATE

    def update(self):
        if self.state == GameState.PLAYING:
            # Update player
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.aim(pygame.mouse.get_pos())
            self.player.update()

            # Update enemy manager
            self.enemy_manager.update(self.player.x + self.player.size / 2,
                                      self.player.y + self.player.size / 2)
            # Update lasers
            for laser in self.player.lasers[:]:  # Copy list for safe removal
                laser.move()
                if laser.is_off_screen():
                    self.player.lasers.remove(laser)

            # Check collisions and update score
            points = self.enemy_manager.check_collisions(self.player.lasers)
            self.score_manager.add_score(points)

            if self.player.check_collision(self.enemy_manager.enemies):
                self.state = GameState.GAME_OVER

    def draw(self):
        # Clear screen and draw background
        self.screen.fill(BLACK)
        self.background.draw(self.screen)

        if self.state == GameState.PLAYING:
            # Draw game elements
            self.player.draw(self.screen)
            self.enemy_manager.draw(self.screen)
            for laser in self.player.lasers:
                laser.draw(self.screen)

            # Draw HUD
            enemies_remaining = (self.enemy_manager.enemies_per_wave -
                                 self.enemy_manager.enemies_spawned +
                                 len(self.enemy_manager.enemies))
            self.hud.draw(
                self.screen,
                self.score_manager.score,
                self.enemy_manager.wave_number,
                enemies_remaining
            )
        elif self.state == GameState.GAME_OVER:
            # Draw game over screen
            self.game_over_screen.draw(
                self.screen,
                self.score_manager.score,
                self.score_manager.high_score
            )

        # Update display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

