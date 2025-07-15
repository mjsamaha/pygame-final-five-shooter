import random

from loader import AssetLoader
from settings import *
from .enemy1 import Enemy1
from .enemy2 import Enemy2
from .enemy3 import Enemy3
from .enemy4 import Enemy4
from .enemy5 import Enemy5


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 60
        self.wave_number = 1
        self.enemies_per_wave = 15
        self.enemies_spawned = 0
        self.explosion_sound = AssetLoader.load_sound('laser_explosion.wav')

        self.particle_system = None
        # Enemy type weights for different waves
        self.enemy_weights = {
            1: [(Enemy1, 100)],
            2: [(Enemy1, 70), (Enemy2, 30)],
            3: [(Enemy1, 50), (Enemy2, 30), (Enemy3, 20)],
            4: [(Enemy1, 40), (Enemy2, 25), (Enemy3, 20), (Enemy4, 15)],
            5: [(Enemy1, 30), (Enemy2, 25), (Enemy3, 20), (Enemy4, 15), (Enemy5, 10)]
        }

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    def get_enemy_type(self):
        # Get weights for current wave or use highest wave if beyond defined waves
        wave_weights = self.enemy_weights.get(
            min(self.wave_number, max(self.enemy_weights.keys())),
            self.enemy_weights[max(self.enemy_weights.keys())]
        )

        # Calculate total weight
        total_weight = sum(weight for _, weight in wave_weights)
        r = random.randint(1, total_weight)

        # Select enemy type based on weights
        current_weight = 0
        for enemy_type, weight in wave_weights:
            current_weight += weight
            if r <= current_weight:
                return enemy_type

        return Enemy1  # Fallback to basic enemy

    def spawn_enemy(self):
        """Spawn enemy at a random edge position"""
        # Random edge selection
        side = random.randint(0, 3)
        spawn_offset = 20

        if side == 0:  # Top
            x = random.randint(BORDER_SIZE, WINDOW_W - BORDER_SIZE)
            y = -spawn_offset
        elif side == 1:  # Right
            x = WINDOW_W + spawn_offset
            y = random.randint(BORDER_SIZE, WINDOW_H - BORDER_SIZE)
        elif side == 2:  # Bottom
            x = random.randint(BORDER_SIZE, WINDOW_W - BORDER_SIZE)
            y = WINDOW_H + spawn_offset
        else:  # Left
            x = -spawn_offset
            y = random.randint(BORDER_SIZE, WINDOW_H - BORDER_SIZE)

        enemy_type = self.get_enemy_type()
        enemy = enemy_type(x, y)
        if hasattr(enemy, 'particle_system'):
            enemy.particle_system = self.particle_system
        self.enemies.append(enemy)


    def check_collisions(self, player_lasers):
            """Check collisions between enemies and lasers"""
            score = 0

            # Check player lasers with enemies
            for laser in player_lasers[:]:
                for enemy in self.enemies[:]:
                    if enemy.rect.colliderect(laser.x - laser.size, laser.y - laser.size,
                                              laser.size * 2, laser.size * 2):
                        if enemy.take_damage(34):
                            score += enemy.value
                            # Create explosion particles with more dramatic effects
                            if self.particle_system:
                                # Create main explosion
                                self.particle_system.create_explosion(
                                    enemy.x + enemy.size / 2,
                                    enemy.y + enemy.size / 2,
                                    color=enemy.explosion_color,  # Orange explosion
                                    count=40  # More particles
                                )
                                # Create secondary explosion with different color
                                lighter_color = tuple(min(255, c + 50) for c in enemy.explosion_color)
                                self.particle_system.create_explosion(
                                    enemy.x + enemy.size / 2,
                                    enemy.y + enemy.size / 2,
                                    color=lighter_color,
                                    count=20  # Fewer particles for secondary explosion
                                )

                            self.enemies.remove(enemy)
                            if self.explosion_sound:
                                self.explosion_sound.play()
                        player_lasers.remove(laser)
                        break

            return score

    def update(self, player_x, player_y):
        # Update spawn timer
        self.spawn_timer += 1

        # Handle wave spawning
        if self.spawn_timer >= self.spawn_delay and self.enemies_spawned < self.enemies_per_wave:
            self.spawn_enemy()
            self.enemies_spawned += 1
            self.spawn_timer = 0

        # Update all enemies
        for enemy in self.enemies:
            enemy.update(player_x, player_y)

        # Check if wave is complete
        if len(self.enemies) == 0 and self.enemies_spawned >= self.enemies_per_wave:
            self.start_new_wave()

    def start_new_wave(self):
        """Start a new wave with increased difficulty"""
        self.wave_number += 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 5 + (self.wave_number * 2)
        self.spawn_delay = max(30, 60 - (self.wave_number * 3))

        # Signal that it's time for an upgrade
        return self.wave_number <= 5
