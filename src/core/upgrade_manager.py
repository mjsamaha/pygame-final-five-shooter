from utils.enums import UpgradeType
from config.player_config import UPGRADE_CONFIGS
import random



class UpgradeManager:
    def __init__(self):
        self.available_upgrades = {
            UpgradeType.FASTER_SHOOTING: "Decrease firing cooldown by 25%",
            UpgradeType.DOUBLE_SHOT: "Fire two bullets at once",
            UpgradeType.TRIPLE_SHOT: "Fire three bullets in a spread",
            UpgradeType.PIERCING_SHOT: "Bullets penetrate through enemies",
            UpgradeType.SPEED_BOOST: "Increase movement speed by 25%",
            UpgradeType.LASER_SPREAD: "Increase spread of multiple shots",
        }
        self.acquired_upgrades = set()
        self.faster_shooting_count = 0

    def get_upgrade_options(self, wave_number):
        """Return available upgrades based on current wave and previous upgrades"""
        if wave_number == 1:
            # After first wave: only faster shooting or double shot
            options = [
                (UpgradeType.FASTER_SHOOTING, self.available_upgrades[UpgradeType.FASTER_SHOOTING]),
                (UpgradeType.DOUBLE_SHOT, self.available_upgrades[UpgradeType.DOUBLE_SHOT])
            ]
        elif wave_number == 2:
            options = []
            # Can get triple shot if double shot was acquired
            if UpgradeType.DOUBLE_SHOT in self.acquired_upgrades:
                options.append(
                    (UpgradeType.TRIPLE_SHOT, self.available_upgrades[UpgradeType.TRIPLE_SHOT])
                )
            # Can always get faster shooting
            options.append(
                (UpgradeType.FASTER_SHOOTING, self.available_upgrades[UpgradeType.FASTER_SHOOTING])
            )
            # If we don't have double shot yet, it's still available
            if UpgradeType.DOUBLE_SHOT not in self.acquired_upgrades:
                options.append(
                    (UpgradeType.DOUBLE_SHOT, self.available_upgrades[UpgradeType.DOUBLE_SHOT])
                )
        elif wave_number == 3:
            # Similar to wave 2, but might want to add other options
            options = []
            if UpgradeType.DOUBLE_SHOT in self.acquired_upgrades and \
               UpgradeType.TRIPLE_SHOT not in self.acquired_upgrades:
                options.append(
                    (UpgradeType.TRIPLE_SHOT, self.available_upgrades[UpgradeType.TRIPLE_SHOT])
                )
            options.append(
                (UpgradeType.FASTER_SHOOTING, self.available_upgrades[UpgradeType.FASTER_SHOOTING])
            )
        elif wave_number >= 4:
            # Late game upgrades
            options = []
            if UpgradeType.PIERCING_SHOT not in self.acquired_upgrades:
                options.append(
                    (UpgradeType.PIERCING_SHOT, self.available_upgrades[UpgradeType.PIERCING_SHOT])
                )
            if UpgradeType.SPEED_BOOST not in self.acquired_upgrades:
                options.append(
                    (UpgradeType.SPEED_BOOST, self.available_upgrades[UpgradeType.SPEED_BOOST])
                )
            if UpgradeType.LASER_SPREAD not in self.acquired_upgrades and \
               (UpgradeType.DOUBLE_SHOT in self.acquired_upgrades or
                UpgradeType.TRIPLE_SHOT in self.acquired_upgrades):
                options.append(
                    (UpgradeType.LASER_SPREAD, self.available_upgrades[UpgradeType.LASER_SPREAD])
                )
            if len(options) == 0:  # If no new upgrades available
                options.append(
                    (UpgradeType.FASTER_SHOOTING, self.available_upgrades[UpgradeType.FASTER_SHOOTING])
                )

        # Return 2 random options if we have more than 2, otherwise return all available
        if len(options) > 2:
            return random.sample(options, 2)
        return options

    def apply_upgrade(self, player, upgrade_type):
        """Apply the selected upgrade to the player"""
        self.acquired_upgrades.add(upgrade_type)

        if upgrade_type == UpgradeType.FASTER_SHOOTING:
            config = UPGRADE_CONFIGS['faster_shooting']
            player.fire_rate = int(player.fire_rate * config['fire_rate_multiplier'])
            self.faster_shooting_count += 1
        elif upgrade_type == UpgradeType.DOUBLE_SHOT:
            config = UPGRADE_CONFIGS['double_shot']
            player.shot_count = config['shot_count']
            player.shot_spread = config['shot_spread']
        elif upgrade_type == UpgradeType.TRIPLE_SHOT:
            config = UPGRADE_CONFIGS['triple_shot']
            player.shot_count = config['shot_count']
            player.shot_spread = config['shot_spread']
        elif upgrade_type == UpgradeType.PIERCING_SHOT:
            player.piercing_shot = True
        elif upgrade_type == UpgradeType.SPEED_BOOST:
            config = UPGRADE_CONFIGS['speed_boost']
            player.speed *= config['speed_multiplier']
        elif upgrade_type == UpgradeType.LASER_SPREAD:
            config = UPGRADE_CONFIGS['laser_spread']
            player.shot_spread += config['spread_increase']
