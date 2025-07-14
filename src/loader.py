# load images, audio...
import os
import pygame


class AssetLoader:
    _sound_cache = {}
    _music_cache = {}
    _image_cache = {}

    @staticmethod
    def get_asset_path(filename, subfolder=None):
        # Get the path to the assets directory (one level up from src)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        assets_path = os.path.join(project_root, 'assets')

        if subfolder:
            assets_path = os.path.join(assets_path, subfolder)

        return os.path.join(assets_path, filename)

    @staticmethod
    def load_image(filename, size=None, pixel_perfect=True):
        """
        Load an image and optionally resize it with pixel-perfect scaling
        Args:
            filename: Name of the image file
            size: Target size (width and height will be equal)
            pixel_perfect: If True, use nearest-neighbor scaling for pixel art
        """
        cache_key = f"{filename}_{size}_{pixel_perfect}"
        if cache_key in AssetLoader._image_cache:
            return AssetLoader._image_cache[cache_key]

        try:
            # Load the image
            image = pygame.image.load(AssetLoader.get_asset_path(filename, 'images')).convert_alpha()

            if size:
                if pixel_perfect:
                    # Use nearest neighbor scaling for pixel art
                    scaled = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.transform.scale(image, (size, size), scaled)
                    image = scaled
                else:
                    # Use smooth scaling for non-pixel art
                    image = pygame.transform.smoothscale(image, (size, size))

            AssetLoader._image_cache[cache_key] = image
            return image

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {filename}: {e}")
            # Create a default surface with magenta color to make missing textures obvious
            surface = pygame.Surface((size or 32, size or 32))
            surface.fill((255, 0, 255))  # Magenta color
            return surface


    @staticmethod
    def load_sound(filename):
            """Load a sound effect"""
            if filename in AssetLoader._sound_cache:
                return AssetLoader._sound_cache[filename]

            try:
                sound = pygame.mixer.Sound(AssetLoader.get_asset_path(filename, 'audio'))
                AssetLoader._sound_cache[filename] = sound
                return sound
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading sound {filename}: {e}")
                return None

    @staticmethod
    def load_music(filename):
        """Load and play background music"""
        try:
            pygame.mixer.music.load(AssetLoader.get_asset_path(filename, 'audio'))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading music {filename}: {e}")

    @staticmethod
    def play_music(volume=1.0, loops=-1):
        """Play the loaded background music"""
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)

    @staticmethod
    def stop_music():
        """Stop the background music"""
        pygame.mixer.music.stop()

