# Enemy manager
import random
from settings import *
from .enemy1 import Enemy1


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 60  # Frames between spawns
        self.wave_number = 1
        self.enemies_per_wave = 15
        self.enemies_spawned = 0

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

    def spawn_enemy(self):
        """Spawn enemy at a random edge position"""
        # Random edge selection
        side = random.randint(0, 3)
        spawn_offset = 20  # How far outside the visible area enemies spawn

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

        self.enemies.append(Enemy1(x, y))

    def start_new_wave(self):
        """Start a new wave with increased difficulty"""
        self.wave_number += 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 5 + (self.wave_number * 2)  # Increase enemies per wave
        self.spawn_delay = max(30, 60 - (self.wave_number * 3))  # Decrease spawn delay

    def draw(self, screen):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(screen)

    def check_collisions(self, lasers):
        """Check collisions between enemies and lasers"""
        score = 0
        for laser in lasers[:]:
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(laser.x - laser.size, laser.y - laser.size,
                                          laser.size * 2, laser.size * 2):
                    if enemy.take_damage(34):  # 3 hits to kill
                        score += enemy.value
                        self.enemies.remove(enemy)
                    lasers.remove(laser)
                    break
        return score
