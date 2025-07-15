import random
import pygame

# Config imports
from config.game_configurations import GAME_CONFIG
from config.settings import BLACK

# Entity imports
from entities.player.player import Player
from entities.enemies.enemy_manager import EnemyManager

# UI imports
from ui.hud import HUD
from ui.screens.game_over_screen import GameOverScreen
from ui.screens.main_menu_screen import MenuScreen
from ui.screens.upgrade_screen import UpgradeScreen

# Core imports
from core.game_state_manager import GameStateManager
from core.score_manager import ScoreManager

# Utils imports
from utils.loader import AssetLoader
from utils.enums import GameState
from utils.particles import ParticleSystem

# Visual imports
from visual.background import Background

# Mechanics imports
from core.upgrade_manager import UpgradeManager

class Game:
    def __init__(self):
        self._init_pygame()
        self._init_game_components()
        self._init_audio()
        self.reset_game()

    def _init_pygame(self):
        """Initialize Pygame and create the game window"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(
            (GAME_CONFIG['window']['width'], GAME_CONFIG['window']['height'])
        )
        pygame.display.set_caption(GAME_CONFIG['window']['title'])
        self._set_window_icon()
        self.clock = pygame.time.Clock()
        self.running = True

    def _set_window_icon(self):
        try:
            icon = AssetLoader.load_image(GAME_CONFIG['window']['icon_path'])
            if icon:
                pygame.display.set_icon(icon)
        except Exception:
            pass

    def _init_game_components(self):
        """Initialize game components and managers"""
        self.state_manager = GameStateManager()
        self.background = Background()
        self.score_manager = ScoreManager()
        self.hud = HUD()
        self.particle_system = ParticleSystem()
        self.enemy_manager = self._create_enemy_manager()
        self.player = self._create_player()
        self.upgrade_manager = UpgradeManager()
        self.upgrade_screen = UpgradeScreen()
        self.menu_screen = MenuScreen()
        self.game_over_screen = GameOverScreen()
        self.current_upgrade_options = None

    def _init_audio(self):
        """Initialize game audio"""
        audio_config = GAME_CONFIG['audio']

        # Load and configure laser sound
        self.laser_sound = AssetLoader.load_sound(audio_config['sounds']['laser']['path'])
        if self.laser_sound:  # Add null check
            self.laser_sound.set_volume(audio_config['sounds']['laser']['volume'])

        # Load and configure explosion sound
        self.explosion_sound = AssetLoader.load_sound(audio_config['sounds']['explosion']['path'])
        if self.explosion_sound:  # Add null check
            self.explosion_sound.set_volume(audio_config['sounds']['explosion']['volume'])

        # Load and play music
        if AssetLoader.load_music(audio_config['music']['menu']['path']):
            AssetLoader.play_music(volume=audio_config['music']['menu']['volume'])

    def _create_player(self):
        """Create and return a new player instance"""
        return Player(
            GAME_CONFIG['player']['spawn']['x'],
            GAME_CONFIG['player']['spawn']['y']
        )

    def _create_enemy_manager(self):
        """Create and return a new enemy manager instance"""
        manager = EnemyManager()
        manager.particle_system = self.particle_system
        return manager

    def reset_game(self):
        """Reset the game state"""
        self.player = self._create_player()
        self.enemy_manager = self._create_enemy_manager()
        self.score_manager.reset()
        self.upgrade_manager = UpgradeManager()
        self.current_upgrade_options = None
        self.state_manager.switch_to_menu()

    def _handle_playing_state(self):
        """Update game logic when in playing state"""
        self._update_player()
        self._update_enemies()
        self._update_particles()
        self._check_collisions()
        self._check_wave_completion()

    def _update_player(self):
        """Update player state"""
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.aim(pygame.mouse.get_pos())
        if self.player.can_shoot:
            self.shoot_laser()
        self.player.update()

    def _update_enemies(self):
        """Update enemy states"""
        self.enemy_manager.update(
            self.player.x + self.player.size / 2,
            self.player.y + self.player.size / 2
        )

    def _update_particles(self):
        """Update particle effects"""
        self.particle_system.update()
        self._update_laser_particles()

    def _update_laser_particles(self):
        """Update laser movement and particles"""
        for laser in self.player.lasers[:]:
            laser.move()
            if random.random() < GAME_CONFIG['particles']['laser_trail']['chance']:
                self.particle_system.create_laser_trail(laser.x, laser.y)
            if laser.is_off_screen():
                self.player.lasers.remove(laser)

    def _check_collisions(self):
        """Check for collisions between game objects"""
        self._check_enemy_laser_collisions()
        points = self.enemy_manager.check_collisions(self.player.lasers)
        self.score_manager.add_score(points)

        if self.player.check_collision(self.enemy_manager.enemies):
            self.state_manager.switch_to_game_over()

    def _check_enemy_laser_collisions(self):
        """Check collisions between enemy lasers and player"""
        for enemy in self.enemy_manager.enemies:
            if hasattr(enemy, 'lasers'):
                for laser in enemy.lasers[:]:
                    if self.player.rect.colliderect(laser.rect):
                        self.state_manager.switch_to_game_over()
                        return

    def _check_wave_completion(self):
        """Check if current wave is complete"""
        if (len(self.enemy_manager.enemies) == 0 and
                self.enemy_manager.enemies_spawned >= self.enemy_manager.enemies_per_wave):
            if self.enemy_manager.wave_number < 5:
                self.current_upgrade_options = self.upgrade_manager.get_upgrade_options(
                    self.enemy_manager.wave_number)
                if self.current_upgrade_options:
                    self.state_manager.switch_to_upgrade()

    def shoot_laser(self):
        """Create a new laser and play sound effect"""
        self.player.shoot()
        if self.laser_sound:
            self.laser_sound.play()



    def update(self):
        """Update game state"""
        if self.state_manager.state == GameState.PLAYING:
            self._handle_playing_state()

    def draw(self):
        """Render the game"""
        self.screen.fill(BLACK)

        if self.state_manager.state == GameState.MENU:
            self.menu_screen.draw(self.screen)
        else:
            self._draw_game_state()

        pygame.display.flip()

    def _draw_game_state(self):
        """Draw the current game state"""
        self.background.draw(self.screen)

        if self.state_manager.state in [GameState.PLAYING, GameState.UPGRADE]:
            self._draw_playing_state()
        elif self.state_manager.state == GameState.GAME_OVER:
            self._draw_game_over_state()

        self.particle_system.draw(self.screen)

    def _draw_playing_state(self):
        """Draw the playing state elements"""
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        for laser in self.player.lasers:
            laser.draw(self.screen)

        enemies_remaining = (self.enemy_manager.enemies_per_wave -
                             self.enemy_manager.enemies_spawned +
                             len(self.enemy_manager.enemies))
        self.hud.draw(
            self.screen,
            self.score_manager.score,
            self.enemy_manager.wave_number,
            enemies_remaining
        )

        if self.state_manager.state == GameState.UPGRADE:
            self.upgrade_screen.draw(self.screen, self.current_upgrade_options)

    def _draw_game_over_state(self):
        """Draw the game over state"""
        self.game_over_screen.draw(
            self.screen,
            self.score_manager.score,
            self.score_manager.high_score
        )

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.state_manager.state == GameState.MENU:
                        self.state_manager.switch_to_playing()
                    elif self.state_manager.state == GameState.GAME_OVER:
                        if self.game_over_screen.handle_click(event.pos):
                            self.reset_game()
                            self.state_manager.switch_to_playing()
                    elif self.state_manager.state == GameState.UPGRADE:
                        selected_index = self.upgrade_screen.handle_click(event.pos)
                        if selected_index is not None:
                            # Get the actual upgrade type from current_upgrade_options
                            selected_upgrade = self.current_upgrade_options[selected_index][0]
                            self.upgrade_manager.apply_upgrade(self.player, selected_upgrade)
                            self.state_manager.switch_to_playing(restart_music=False)
                            self.enemy_manager.start_new_wave()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(GAME_CONFIG['window']['fps'])

        AssetLoader.stop_music()
        pygame.quit()

