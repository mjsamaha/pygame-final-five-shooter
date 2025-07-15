from .enemy_laser import EnemyLaser

class ShootingBehavior:
    """Mixin for enemies that can shoot"""
    def init_shooting(self, shoot_delay):
        self.shoot_cooldown = 0
        self.shoot_delay = shoot_delay
        self.lasers = []

    def update_shooting(self, player_x, player_y):
        if self.shoot_cooldown <= 0:
            self.shoot(player_x, player_y)
            self.shoot_cooldown = self.shoot_delay
        else:
            self.shoot_cooldown -= 1
            self._update_lasers()

    def _update_lasers(self):
        for laser in self.lasers[:]:
            laser.move()
            if hasattr(self, 'particle_system') and self.particle_system:
                self.particle_system.create_enemy_laser_trail(
                    laser.x, laser.y, laser.color
                )
            if laser.is_off_screen():
                self.lasers.remove(laser)

    def draw_lasers(self, screen):
        for laser in self.lasers:
            laser.draw(screen)

class ZigzagBehavior:
    """Mixin for enemies with zigzag movement"""
    def init_zigzag(self, period=30, amplitude=2):
        self.zigzag_timer = 0
        self.zigzag_direction = 1
        self.zigzag_period = period
        self.zigzag_amplitude = amplitude

    def update_zigzag(self):
        self.zigzag_timer += 1
        if self.zigzag_timer >= self.zigzag_period:
            self.zigzag_direction *= -1
            self.zigzag_timer = 0
            self.x += self.zigzag_direction * self.zigzag_amplitude

class DashingBehavior:
    """Mixin for enemies that can dash"""
    def init_dashing(self, cooldown=180, duration=30, dash_speed=8):
        self.dash_cooldown = cooldown
        self.dash_duration = duration
        self.dash_speed = dash_speed
        self.dash_timer = self.dash_cooldown
        self.is_dashing = False
        self.normal_speed = self.speed

    def update_dashing(self, player_x, player_y):
        if self.is_dashing:
            self.speed = self.dash_speed
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.speed = self.normal_speed
                self.dash_timer = self.dash_cooldown
        else:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = True
                self.dash_timer = self.dash_duration
