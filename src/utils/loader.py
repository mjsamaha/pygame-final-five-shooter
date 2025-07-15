# load images, audio...
import os
import sys

import pygame


class AssetLoader:
    _sound_cache = {}
    _music_cache = {}
    _image_cache = {}

    @staticmethod
    def get_asset_path(filename, subfolder=None):
        try:
            if getattr(sys, '_MEIPASS', None):
                base_path = sys._MEIPASS
            else:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                src_dir = os.path.dirname(current_dir)
                base_path = os.path.dirname(src_dir)

            if subfolder:
                full_path = os.path.join(base_path, 'assets', subfolder, filename)
            else:
                full_path = os.path.join(base_path, 'assets', filename)

            return full_path

        except Exception:
            return os.path.join('assets', subfolder, filename) if subfolder else os.path.join('assets', filename)

    @staticmethod
    def load_image(filename, size=None, pixel_perfect=True):
        cache_key = f"{filename}_{size}_{pixel_perfect}"
        if cache_key in AssetLoader._image_cache:
            return AssetLoader._image_cache[cache_key]

        try:
            image = pygame.image.load(AssetLoader.get_asset_path(filename, 'images')).convert_alpha()

            if size:
                if pixel_perfect:
                    scaled = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.transform.scale(image, (size, size), scaled)
                    image = scaled
                else:
                    image = pygame.transform.smoothscale(image, (size, size))

            AssetLoader._image_cache[cache_key] = image
            return image

        except (pygame.error, FileNotFoundError):
            surface = pygame.Surface((size or 32, size or 32))
            surface.fill((255, 0, 255))
            return surface

    @staticmethod
    def load_sound(filename):
        if filename in AssetLoader._sound_cache:
            return AssetLoader._sound_cache[filename]

        try:
            sound = pygame.mixer.Sound(AssetLoader.get_asset_path(filename, 'audio'))
            AssetLoader._sound_cache[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError):
            return None

    @staticmethod
    def load_music(filename):
        try:
            pygame.mixer.music.load(AssetLoader.get_asset_path(filename, 'audio'))
            return True
        except (pygame.error, FileNotFoundError):
            return False

    @staticmethod
    def play_music(volume=1.0, loops=-1):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()


