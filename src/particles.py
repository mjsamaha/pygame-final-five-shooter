import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, speed=3, size=5, lifetime=35):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.alpha = 255

        # Random direction
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, speed)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.age += 1
        self.alpha = int(255 * (1 - self.age / self.lifetime))
        return self.age < self.lifetime

    def draw(self, screen):
        if self.alpha > 0:
            # Draw a pixel-perfect square instead of a circle
            pygame.draw.rect(screen,
                             (*self.color, self.alpha),
                             (int(self.x), int(self.y), self.size, self.size))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def _create_trail_particles(self, x, y, colors, count, base_speed, base_size, base_lifetime):
        """Helper method to create trail particles with common logic"""
        for i in range(count):
            # Randomize the position slightly
            offset_x = random.uniform(-1, 1)
            offset_y = random.uniform(-1, 1)

            # Create main particle
            particle = Particle(
                x + offset_x,
                y + offset_y,
                colors[i % len(colors)],
                speed=base_speed,
                size=base_size,
                lifetime=base_lifetime + i * 2
            )
            self.particles.append(particle)

            # Add sparkle with adjusted parameters
            if random.random() < 0.2:  # 20% chance for sparkle
                sparkle_color = colors[1] if len(colors) > 1 else colors[0]  # Use lighter color if available
                sparkle = Particle(
                    x + offset_x,
                    y + offset_y,
                    sparkle_color,
                    speed=base_speed * 2,
                    size=1,
                    lifetime=3
                )
                self.particles.append(sparkle)

    def create_explosion(self, x, y, color=(255, 200, 0), count=20):
        for _ in range(count):
            particle = Particle(x, y, color, speed=5, size=random.randint(3, 5), lifetime=35)
            self.particles.append(particle)

    def create_enemy_laser_trail(self, x, y, color, count=2):
        """Create trail particles for enemy lasers"""
        colors = [
            color,  # Base color
            tuple(min(255, c + 70) for c in color),  # Lighter
            tuple(max(0, c - 40) for c in color)  # Darker
        ]
        self._create_trail_particles(x, y, colors, count, base_speed=1, base_size=2, base_lifetime=4)

    def create_laser_trail(self, x, y, color=(0, 255, 255), count=3):
        """Create trail particles for player laser"""
        colors = [
            (0, 255, 255),  # Cyan
            (100, 255, 255),  # Lighter cyan
            (0, 200, 255)  # Slightly bluer cyan
        ]
        self._create_trail_particles(x, y, colors, count, base_speed=1, base_size=1, base_lifetime=5)

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)